# PVDD 5V LDO Regulator — Design Audit & Redesign Plan

## 1. Current Architecture Summary

```
BVDD (5.4-10.5V)
  │
  ├── Pass Device (Block 01): 10x PFET W=100u L=0.5u (1mm total)
  │     source=bvdd, drain=pvdd, gate=gate
  │
  ├── Error Amp (Block 00): Two-stage Miller OTA
  │     Stage 1: PMOS diff pair (PVDD-powered) + NMOS mirror load
  │     Stage 2: PFET CS (BVDD-powered) + NFET current source
  │     Output: ea_out → drives gate through Rgate=1kΩ (Block 09)
  │     Internal Miller: Cc=30pF + Rc=25kΩ from d1 to ea_out
  │
  ├── Startup (Block 09): Just Rgate=1kΩ + startup_done detector
  │     ea_en always HIGH, no soft-start, no level shifter
  │
  ├── Feedback (Block 02): R_TOP=364kΩ + R_BOT=118kΩ (xhigh_po)
  │     vfb = pvdd × 0.2452 → 1.226V at 5.0V
  │
  ├── Compensation (Block 03): Outer Miller loop
  │     Cc=29pF MIM from ea_out to pvdd (through Rz=5kΩ)
  │     Cout=68pF MIM on pvdd
  │
  ├── Current Limiter (Block 04): Sense mirror + clamp PFET
  ├── UV/OV Comparators (Block 05): 1.8V-domain, resistive dividers
  ├── Level Shifter (Block 06): Cross-coupled PMOS, SVDD↔BVDD
  ├── Zener Clamp (Block 07): 5-device stack + 7-diode fast stack
  └── Mode Control (Block 08): Resistor ladder + Schmitt comparators + logic
```

## 2. Three Critical Failures

| # | Failure | Measured | Spec | Severity |
|---|---------|----------|------|----------|
| 1 | Startup overshoot | 6.54V | <5.5V | HIGH — damages 5V logic |
| 2 | PSRR at 1kHz | -18dB | >20dB | HIGH — amplifies supply noise |
| 3 | Load transient undershoot | 3.5V | <150mV | CRITICAL — kills downstream |

## 3. Root Cause Analysis

### FAILURE 1: Startup Overshoot (6.54V)

**Root cause: Missing soft-start + weak zener clamp response**

The top-level design.cir has a COMMENT about soft-start but **no actual implementation**:
```spice
* Soft-start reference: RC filter on avbg → vref_ss
*   R=100kΩ, C=1nF → tau=100µs
```
But then connects avbg DIRECTLY to the error amp:
```spice
XEA avbg vfb ea_out pvdd gnd ibias ea_en bvdd error_amp
```
**There is no Rss or Css.** The reference voltage jumps to 1.226V instantly.

During startup:
1. BVDD ramps up
2. EA Stage 2 PFET (source=BVDD) starts conducting immediately
3. With no soft-start, the EA demands full regulation voltage instantly
4. Pass device turns ON hard → dumps BVDD onto PVDD
5. PVDD overshoots to 6.54V before the loop settles

The zener clamp should catch this, but:
- Precision stack gate pulldown Rpd=500kΩ → RC time constant with gate capacitance is too slow
- Clamp NFET (W=400µm) has Cgs ≈ 100fF → τ = 500k × 100fF = 50ns (should be fast enough)
- But the 5-device precision stack has its own RC delays through each diode junction
- The 7-diode fast stack should clamp at ~7×0.7V ≈ 4.9V, but body effect raises Vth

**FIX:** Add actual soft-start components (Rss=100kΩ, Css=1nF between avbg and vref input to EA). This is a 2-component fix in the top-level design.cir.

### FAILURE 2: PSRR at 1kHz (-18dB)

**Root cause: BVDD-powered single-ended CS stage with no supply rejection**

The error amp Stage 2:
```spice
XMcs_p vout_gate d1  bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 w=10e-6 l=2e-6
XMcs_n vout_gate pb_cs gnd gnd sky130_fd_pr__nfet_g5v0d10v5 w=2e-6  l=4e-6
```

BVDD noise enters through THREE paths:
1. **PFET source:** AC on BVDD modulates Vgs of XMcs_p → direct gain to output
2. **PFET body effect:** BVDD on bulk changes Vth → modulates drain current
3. **Pass device feedthrough:** BVDD on pass device source → Cgd coupling to pvdd

For a single PFET CS stage: PSRR ≈ -gm_cs × ro_cs / gm_pass × ro_pass
At 1kHz, the loop gain is still moderate (~40dB), so PSRR should be ~40dB.
But measured -18dB means the BVDD coupling EXCEEDS the loop gain.

The issue: the PFET CS stage has its source directly on BVDD. Any BVDD ripple
appears as Vgs modulation (since gate d1 is in the PVDD domain and doesn't track BVDD).
The transconductance gain then amplifies this error to the gate node.

**PSRR of Stage 2 alone** ≈ gds/gm of the PFET ≈ 1/gm×ro ≈ -20 to -30dB.
This means the stage AMPLIFIES BVDD noise by 20-30dB before the loop can reject it.

**FIX options (in order of effectiveness):**
1. **Cascode the CS PFET:** Add a cascode PFET between XMcs_p and vout_gate. The cascode shields the CS PFET from BVDD variations. Expected improvement: +30-40dB PSRR.
2. **Regulate the CS stage supply:** Use a local regulator or LDO to create a clean supply for Stage 2 from BVDD. Overkill but bulletproof.
3. **Add BVDD bypass capacitor:** A large cap (100pF-1nF) from BVDD to gnd at the CS stage source. Simple but uses area.

### FAILURE 3: Load Transient Undershoot (3.5V)

**Root cause: Catastrophically insufficient output capacitance for the load step magnitude**

Math:
```
Total Cout = 68pF (Block 03) + 200pF (Cload) = 268pF
Load step = 10mA in 1µs
ΔV = ΔI × Δt / C = 10mA × 1µs / 268pF = 37.3V
```

**37.3V of theoretical undershoot.** The capacitor simply cannot supply 10mA for 1µs without massive voltage collapse. Even if the loop responds in 100ns, the undershoot would be 3.7V.

For 150mV max undershoot with 10mA step:
```
C_required = ΔI × Δt / ΔV = 10mA × 1µs / 150mV = 66.7nF
```

We need **66.7nF** but have **0.268nF** — we're **250× short** on capacitance.

The loop bandwidth makes this worse. With ~200kHz bandwidth (5µs response):
```
ΔV = ΔI × t_response / C = 10mA × 5µs / 268pF = 186V (theoretical)
```

**This is not fixable with loop tuning alone.** Options:

1. **Increase output capacitance dramatically:** Use 10nF+ MIM cap. At sky130 ~2fF/µm², 10nF needs 5M µm² = 2.2mm × 2.2mm. Large but feasible for a chip-level block.
2. **Add slew rate enhancement (SRE):** A fast auxiliary path that detects load transients and directly boosts/cuts pass device current. This is standard in capless LDOs.
3. **Reduce the load step spec:** Accept that 10mA steps require external capacitance. Document as a known limitation.
4. **Increase loop bandwidth to >5MHz:** Would need to remove or reduce Miller compensation, add feedforward path. Risk: stability at high loads.

## 4. Secondary Issues

### 4a. Double Miller Compensation Interaction

The design has TWO Miller compensation paths:
- **Inner (Block 00):** Cc=30pF + Rc=25kΩ from d1 to ea_out (across Stage 2)
- **Outer (Block 03):** Cc=29pF + Rz=5kΩ from ea_out to pvdd (across pass device)

Two Miller caps create a complex pole-zero landscape. The inner Cc splits the EA poles, but the outer Cc then re-splits the overall loop poles. This can create:
- A doublet (closely spaced pole-zero pair) that causes slow settling
- Reduced phase margin at intermediate frequencies
- Conditional stability at certain load currents

**Recommendation:** Remove the inner Miller comp from Block 00 and rely solely on the outer comp (Block 03) sized appropriately. Or: remove the outer comp and size the inner comp to stabilize the complete loop. Having both is dangerous.

### 4b. ea_en Always HIGH

Block 09 forces ea_en HIGH permanently:
```spice
Ren bvdd ea_en 100
```
This means the error amp is always on, even during startup before PVDD is valid.
The mode control block generates `mc_ea_en` but it's **never connected** to the actual `ea_en` that controls the error amp. This is a wiring bug in the top-level.

### 4c. Soft-Start Reference Not Implemented

As noted in Failure 1, the soft-start RC filter is commented but not present.
The vref_ss net doesn't exist in the top-level netlist.

### 4d. Mode Control Outputs Partially Unused

Mode control generates: bypass_en, mc_ea_en, ref_sel, uvov_en, ilim_en, pass_off.
Of these, only `uvov_en` is connected (to UV/OV comparator enable).
The others (bypass_en, mc_ea_en, ref_sel, ilim_en, pass_off) are **floating** —
they're generated but not wired to anything that uses them.

### 4e. Compensation Block Connected to Wrong Node

The compensation subcircuit port `vout_gate` is connected to `ea_out`:
```spice
XCOMP ea_out pvdd gnd compensation
```
But `ea_out` is the error amp output BEFORE the 1kΩ Rgate. The actual pass device gate is `gate` (after Rgate). The Miller comp should wrap around the complete gain path. Currently the Rgate is outside the compensation loop, adding a pole.

## 5. Block-by-Block Verdict

| Block | Status | Issues |
|-------|--------|--------|
| 00 Error Amp | NEEDS REDESIGN | BVDD CS stage has no PSRR; double Miller comp conflict; drives d1 not d2 (polarity workaround) |
| 01 Pass Device | OK | 1mm PFET, adequate for 50mA. L=0.5µm gives good gm but high Vdsat |
| 02 Feedback | OK | Clean resistive divider, good matching (same material) |
| 03 Compensation | NEEDS REWORK | Outer Miller comp + inner comp conflict; Cout far too small |
| 04 Current Limiter | OK | Works but PVT spread is 3.1× (135mA SS vs 43mA FF) |
| 05 UV/OV Comparators | OK | 1.8V domain, reasonable thresholds. Hysteresis needs tuning |
| 06 Level Shifter | OK | Cross-coupled topology, clean. Not in the critical path |
| 07 Zener Clamp | MARGINAL | Precision stack works; fast stack clamp voltage may be too high |
| 08 Mode Control | OK | Well-designed, 16/16 specs pass. Outputs mostly unwired at top level |
| 09 Startup | NEEDS REWORK | Gutted to just Rgate+detector. No soft-start, no controlled charge |

## 6. Recommended Redesign — Priority Order

### Priority 1: Add Soft-Start (fixes startup overshoot)
**Blocks affected:** Top-level design.cir only
**Change:** Add Rss=100kΩ and Css=1nF between avbg and EA vref input
```spice
Rss avbg vref_ss 100k
Css vref_ss gnd 1n
XEA vref_ss vfb ea_out pvdd gnd ibias ea_en bvdd error_amp
```
**Expected result:** vref ramps over ~500µs → PVDD follows smoothly → no overshoot
**Risk:** Low. Doesn't change any block.

### Priority 2: Increase Output Capacitance (fixes load transient)
**Blocks affected:** Block 03 compensation
**Change:** Increase Cout from 68pF to 10nF (or add 10nF at top level)
```spice
Cout_big pvdd gnd 10n
```
**Expected result:** ΔV = 10mA × 1µs / 10nF = 1V. Still over spec but 3.5× better.
With 50nF: ΔV = 200mV. With 100nF: ΔV = 100mV → PASS.
**Risk:** Medium. Large cap changes loop dynamics. Must re-verify stability.
**Area:** 100nF at 2fF/µm² = 50M µm² = 7mm×7mm. Probably needs off-chip or stacked MIM.

### Priority 3: Cascode Stage 2 for PSRR
**Blocks affected:** Block 00 error amp
**Change:** Add cascode PFET between XMcs_p and vout_gate:
```spice
XMcs_p  cas_mid d1    bvdd bvdd pfet_g5v0d10v5 w=10e-6 l=2e-6
XMcas_p vout_gate cas_bias cas_mid cas_mid pfet_g5v0d10v5 w=10e-6 l=2e-6
```
Where cas_bias is generated from a BVDD-referenced divider (~BVDD - 2V).
**Expected result:** +30-40dB PSRR improvement. The cascode shields CS PFET from BVDD.
**Risk:** Medium-High. Cascode reduces output swing, may affect regulation at low BVDD.

### Priority 4: Remove Double Miller Compensation
**Blocks affected:** Block 00 + Block 03
**Change:** Remove inner Cc/Rc from Block 00. Keep only outer Cc/Rz in Block 03.
Re-size outer Cc for stability across all loads.
**Risk:** Medium. Changes loop dynamics. Needs full re-verification.

### Priority 5: Wire Mode Control Outputs
**Blocks affected:** Top-level design.cir
**Change:** Connect mc_ea_en to ea_en (gated by startup_done), connect pass_off to gate pullup, connect bypass_en to bypass switch.
**Risk:** Low-Medium. Adds functionality but may affect startup sequence.

### Priority 6: Slew Rate Enhancement for Load Transient
**Blocks affected:** New sub-block or Block 00 modification
**Change:** Add a fast comparator that detects PVDD droop and directly pulls gate LOW (bypassing the slow EA loop). This is standard in capless LDO literature.
**Risk:** High. New circuit, needs careful design to avoid oscillation.

## 7. Minimum Viable Fix (Quick Wins Only)

If only 3 changes are allowed:

1. **Add Rss + Css** (soft-start) → fixes startup overshoot
2. **Add 10nF Cout** → reduces load transient from 3.5V to ~1V
3. **Add cascode to Stage 2** → fixes PSRR from -18dB to +20dB

These three changes affect only Block 00 and the top-level wiring. Blocks 01-09 unchanged.
