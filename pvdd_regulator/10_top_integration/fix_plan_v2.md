# Fix Plan v2 — PVDD LDO Regulator

**Date:** 2026-04-02
**Based on:** 10 parallel agent analyses + supervisor plot review

---

## Root Cause Diagnosis

**THE SINGLE CRITICAL BUG: pass_off polarity is INVERTED in mode_control.**

In `08_mode_control/design.cir`, lines 75-76, the pass_off output buffer uses `comp1b` as input instead of `comp1`:

```
CURRENT (BROKEN):
  pass_off = NOT(comp1b) = NOT(NOT(comp1)) = comp1
  → pass_off = HIGH when BVDD > 2.5V (normal operation)
  → Gate pullup PFET is ON, injecting ~200µA into gate, fighting EA

FIX:
  pass_off = NOT(comp1)
  → pass_off = LOW when BVDD > 2.5V (normal operation)
  → Gate pullup PFET is OFF, EA has full control
```

**Evidence from EA bias plot:** gate = 5.960V, ea_out = 5.756V → 204µA flowing backward through Rgate (1kΩ) into the EA, consistent with XMgate_pu being ON and sourcing current from BVDD into the gate.

**This bug explains ALL 5 symptoms:**
1. DC regulation fails >10mA → EA can't overcome 200µA pullup to drive gate low enough
2. PSRR = -7dB → XMgate_pu creates direct BVDD-to-gate AC path
3. Loop gain = 20dB → EA output loaded by pullup path, gain collapses
4. Gate oscillates during startup → EA vs pullup limit cycle
5. FS 150°C unstable → pullup current increases at hot/fast corners

---

## Fix #1: pass_off Polarity (CRITICAL — must fix first)

**File:** `../08_mode_control/design.cir`, lines 75-76

**Change:**
```spice
* BEFORE (wrong polarity):
XMpo_bufp pass_off comp1b pvdd pvdd sky130_fd_pr__pfet_g5v0d10v5 w=4e-6 l=2e-6
XMpo_bufn pass_off comp1b gnd  gnd  sky130_fd_pr__nfet_g5v0d10v5 w=2e-6 l=2e-6

* AFTER (correct polarity):
XMpo_bufp pass_off comp1 pvdd pvdd sky130_fd_pr__pfet_g5v0d10v5 w=4e-6 l=2e-6
XMpo_bufn pass_off comp1 gnd  gnd  sky130_fd_pr__nfet_g5v0d10v5 w=2e-6 l=2e-6
```

**Logic verification:**
- BVDD < 2.5V: comp1=LOW → pass_off=NOT(LOW)=HIGH → pullup ON → gate=BVDD → pass OFF ✓
- BVDD > 2.5V: comp1=HIGH → pass_off=NOT(comp1)=LOW → pullup OFF → EA controls ✓

---

## Fix #2: Current Limiter Cascode Vds Matching (IMPORTANT)

**File:** `../04_current_limiter/design.cir`, lines 31-32

**Change:** Swap resistor lengths to set cas_bias=4.0V (matching PVDD) instead of 3.0V:
```spice
* BEFORE: cas_bias = 7V × 300/700 = 3.0V → Vds_sense ≈ 3.0V (mismatched)
XRcas_top bvdd cas_bias gnd sky130_fd_pr__res_xhigh_po w=1 l=400
XRcas_bot cas_bias gnd gnd sky130_fd_pr__res_xhigh_po w=1 l=300

* AFTER: cas_bias = 7V × 400/700 = 4.0V → Vds_sense ≈ 2.0V (matched to pass)
XRcas_top bvdd cas_bias gnd sky130_fd_pr__res_xhigh_po w=1 l=300
XRcas_bot cas_bias gnd gnd sky130_fd_pr__res_xhigh_po w=1 l=400
```

**Why:** With matched Vds, the 1000:1 sense ratio is accurate. Trip point moves from ~43mA to ~50mA. No CLM-induced false trips.

---

## Fix #3: Compensation Tuning (IF NEEDED after Fix #1)

After fixing the polarity bug, the loop gain will jump from 20dB to ~70-80dB. The existing compensation (Cc=20pF, Rc=8kΩ) may or may not be adequate with the full gain restored.

**Check first:** Run Bode plot after Fix #1. If PM < 45° at any corner:

**File:** `../00_error_amp/design.cir`, line 69-70
```spice
* Option: Increase Cc for more phase margin
Cc d2 comp_mid 30p    (was 20p)
Rc comp_mid vout_gate 5k    (was 8k)
```

---

## Fix #4: Bode Testbench Correction (MEASUREMENT)

The current Bode testbench injects at the gate node with Middlebrook method — both sides have high impedance, giving incorrect results. After Fix #1, re-measure with injection at the PVDD node where there is a clear impedance split (high rds_pass vs low Rload).

---

## Implementation Order

1. **Fix #1** (pass_off polarity) — one-line change, test immediately
2. **Simulate:** DC sweep 0-60mA, startup transient, load transient, PSRR, Bode
3. **Fix #2** (cascode bias) if current limit trip is inaccurate
4. **Fix #3** (compensation) if ringing/instability remains
5. **Fix #4** (Bode testbench) to get accurate loop gain measurement
6. **Regenerate all 15 plots**
7. **Full PVT campaign** (15 corners × 4 specs = 60 checks)

---

## Expected Results After Fix #1

| Spec | Before (broken) | After (predicted) |
|------|-----------------|-------------------|
| DC regulation | Fails >10mA | Holds to ~50mA |
| PSRR at DC | -7dB | -50 to -60dB |
| Loop gain (DC) | 20dB | 60-80dB |
| Startup gate | Oscillates 7ms | Clean monotonic |
| FS 150°C | Unstable | Stable (PM >45°) |
| PVDD at 1mA | 4.92V | ~4.995V |
