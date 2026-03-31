# Block 10: Top Integration — Redesign Program

---

## 1. Setup

### Purpose

This program guides the systematic fixing of three critical failures in the PVDD 5V LDO regulator identified during audit. Each fix modifies a specific block's `design.cir`. Every change MUST be verified at block level first, then at top level, before committing.

### Read Before Starting

Read these files in order — they contain everything you need:

1. `10_top_integration/redesign.md` — complete root cause analysis of all failures
2. `10_top_integration/design.cir` — current top-level wiring
3. `00_error_amp/design.cir` — error amplifier (NEEDS REDESIGN)
4. `03_compensation/design.cir` — compensation network (NEEDS REWORK)
5. `09_startup/design.cir` — startup circuit (NEEDS REWORK)
6. All other block `design.cir` files (01, 02, 04-08) — understand interfaces

### Current State (v25b baseline)

What works:
- DC regulation: 4.936-5.101V across 0-50mA — PASS
- Load regulation: 1.9 mV/mA — PASS
- PVT: All 9 corners pass (4.984-5.076V) — PASS
- Iq: 52µA (spec ≤300µA) — PASS
- 19/19 evaluate.py specs pass

What fails:
| Failure | Measured | Spec | Root Cause |
|---------|----------|------|------------|
| Startup peak | 6.54V | <5.5V | Missing soft-start (commented but not wired) |
| PSRR @ 1kHz | -18dB | >20dB | BVDD-powered single CS stage amplifies noise |
| Load transient | 3.5V undershoot | <150mV | 268pF output cap vs 10mA step = 37V theoretical |

### Wiring Bugs Found

1. **ea_en hardwired HIGH** — Block 09 has `Ren bvdd ea_en 100`. Mode control generates `mc_ea_en` but it's never connected.
2. **Soft-start missing** — Comment says `Rss=100k Css=1n` but no components exist.
3. **Mode control outputs floating** — bypass_en, mc_ea_en, ref_sel, ilim_en, pass_off generated but not wired.
4. **Compensation on wrong node** — XCOMP connects to ea_out (before Rgate), should wrap around Rgate to gate.
5. **Double Miller comp** — Inner Cc/Rc in Block 00 AND outer Cc/Rz in Block 03. Dangerous interaction.

---

## 2. Fix Sequence

### CRITICAL RULE: Block-Level Verification First

For EVERY change to a block's design.cir:

```
1. Modify the block's design.cir
2. Write a minimal testbench in the block's directory
3. Run ngspice -b <testbench> and verify the block works standalone
4. Only then run top-level integration test
5. If top-level passes → commit both block and top-level changes
6. If top-level fails → debug. Do NOT revert to v25b.
```

### FIX 1: Soft-Start (Priority: HIGHEST, Risk: LOW)

**Problem:** Startup overshoot to 6.54V because vref jumps to 1.226V instantly.

**Change — Top-level design.cir ONLY:**
```spice
* Add before XEA:
Rss avbg vref_ss 100k
Css vref_ss gnd 1n
* Change XEA line:
XEA vref_ss vfb ea_out pvdd gnd ibias ea_en bvdd error_amp
```

**Block-level verify:** Not needed — only top-level wiring changes.

**Top-level verify:**
```spice
* Testbench: tb_fix1_startup.spice
* BVDD ramp 0→7V at 1V/µs, measure PVDD peak
* PASS if PVDD peak < 5.5V
* Also re-verify: DC regulation still 4.825-5.175V at 1/10/50mA
```

**Expected result:** vref ramps over τ=100µs → PVDD follows smoothly → overshoot eliminated.

### FIX 2: Output Capacitance (Priority: HIGH, Risk: MEDIUM)

**Problem:** 268pF output cap vs 10mA step = 37V theoretical undershoot.

**Option A — Add at top-level (simplest):**
```spice
* Add in top-level design.cir:
Cout_big pvdd gnd 100n
```
100nF gives ΔV = 10mA × 1µs / 100nF = 100mV → PASS.

**Option B — Increase Cout in Block 03:**
Replace `XCout pvdd gnd ... w=187 l=187` with much larger value.
But 100nF in MIM = 7mm × 7mm. For on-chip, 10nF (2.2mm×2.2mm) is more realistic.
10nF gives ΔV = 1V — still fails the 150mV spec but 3.5× better.

**Decision:** Use 100nF. If this is too large for on-chip, document it as requiring an external bypass cap and use 10nF on-chip + external 100nF.

**Block-level verify (Block 03):**
```spice
* Quick AC test: does the comp network still provide correct zero placement?
* Check impedance from vout_gate to pvdd at 1kHz, 100kHz, 1MHz
```

**Top-level verify:**
```spice
* Testbench: tb_fix2_transient.spice
* BVDD=7V, Iload step 1mA→10mA in 1µs
* PASS if undershoot < 150mV
* MUST ALSO verify: PM > 45° at all loads (stability with big cap)
* Run loop stability test at Iload = 0, 1mA, 10mA, 50mA
```

**Risk:** Large output cap changes the dominant pole. Miller compensation may need re-tuning. If PM drops below 45° → reduce Cc or increase Rz.

### FIX 3: Cascode Stage 2 for PSRR (Priority: HIGH, Risk: MEDIUM-HIGH)

**Problem:** BVDD-powered PFET CS stage has ~-20dB PSRR (amplifies noise).

**Change — Block 00 error_amp/design.cir:**

Replace:
```spice
XMcs_p vout_gate d1  bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 w=10e-6 l=2e-6
XMcs_n vout_gate pb_cs gnd gnd sky130_fd_pr__nfet_g5v0d10v5 w=2e-6  l=4e-6
```

With cascode version:
```spice
* CS PFET (input transistor)
XMcs_p  cas_mid  d1       bvdd    bvdd sky130_fd_pr__pfet_g5v0d10v5 w=10e-6 l=2e-6
* Cascode PFET (shields CS from BVDD variations)
XMcas_p vout_gate cas_bias cas_mid cas_mid sky130_fd_pr__pfet_g5v0d10v5 w=10e-6 l=2e-6
* Current source (unchanged)
XMcs_n  vout_gate pb_cs    gnd     gnd sky130_fd_pr__nfet_g5v0d10v5 w=2e-6  l=4e-6
* Cascode bias: BVDD - ~2V (sets cascode Vds headroom)
* Use resistive divider from BVDD
Rcas_top bvdd cas_bias 200k
Rcas_bot cas_bias gnd 800k
* cas_bias = BVDD × 800k/(200k+800k) = 0.8 × BVDD
* At BVDD=7V: cas_bias = 5.6V, Vsg_cas = 7-5.6 = 1.4V (above Vth) ✓
* At BVDD=5.4V: cas_bias = 4.32V, Vsg_cas = 5.4-4.32 = 1.08V (marginal) ⚠
```

**IMPORTANT:** The cascode reduces output swing by one Vdsat (~200mV). At BVDD=5.4V (dropout), the gate must reach ~4.9V for pass device ON. Check that the cascode still achieves this swing.

**Block-level verify (Block 00):**
```spice
* Test 1: DC — does ea_out swing from near-GND to near-BVDD?
*   Sweep vfb 1.0→1.4V, measure ea_out. Must reach within 500mV of GND and BVDD.
* Test 2: AC — open-loop gain and bandwidth
*   Break loop, AC sweep. Gain > 60dB at DC, UGB > 500kHz.
* Test 3: PSRR — AC on BVDD, measure ea_out
*   PSRR at ea_out node should be > 20dB at 1kHz (improvement from -20dB).
```

**Top-level verify:**
```spice
* Testbench: tb_fix3_psrr.spice
* AC source on BVDD (DC=7V + AC=1V), measure PVDD
* PASS if PSRR > 40dB at DC, > 20dB at 10kHz
* Also re-verify: DC regulation, startup, loop stability
```

### FIX 4: Remove Double Miller Compensation (Priority: MEDIUM)

**Problem:** Inner Cc/Rc in Block 00 AND outer Cc/Rz in Block 03 create complex pole-zero interaction.

**Change — Block 00:**
Remove internal Miller comp:
```spice
* DELETE these two lines:
* Cc d1 comp_mid 30p
* Rc comp_mid vout_gate 25k
```

**Change — Block 03:**
Re-size outer Miller comp for full loop stability. May need to increase Cc from 29pF to 50pF, adjust Rz.

**Block-level verify:** EA open-loop response (gain, bandwidth). Without internal comp, the EA has two high-frequency poles. The outer comp must handle everything.

**Top-level verify:** Full loop stability at all loads. PM > 45° everywhere.

### FIX 5: Wire Mode Control Outputs (Priority: LOW-MEDIUM)

**Change — Top-level design.cir:**
```spice
* Connect mc_ea_en to ea_en (replace Ren hack in Block 09)
* Connect pass_off to gate pull-up PFET
* Connect bypass_en to bypass transmission gate
```

This requires modifying Block 09 to accept mc_ea_en instead of hardwiring ea_en.

### FIX 6: Move Compensation to Gate Node (Priority: LOW)

**Change — Top-level design.cir:**
```spice
* Change from:
XCOMP ea_out pvdd gnd compensation
* To:
XCOMP gate pvdd gnd compensation
```

This wraps the Miller comp around Rgate, eliminating the extra pole.

---

## 3. Verification Protocol

### After Each Fix

Run these tests in order. Stop at first failure and debug before proceeding.

| # | Test | Command | Pass Condition |
|---|------|---------|----------------|
| 1 | DC Regulation | `ngspice -b tb_top_dc_reg.spice` | PVDD 4.825-5.175V at 0/1/10/50mA |
| 2 | Startup | `ngspice -b tb_fix1_startup.spice` | PVDD peak < 5.5V, monotonic |
| 3 | Load Transient | `ngspice -b tb_fix2_transient.spice` | Undershoot < 150mV |
| 4 | PSRR | `ngspice -b tb_fix3_psrr.spice` | >40dB DC, >20dB @ 10kHz |
| 5 | Loop Stability | `ngspice -b tb_top_lstb.spice` | PM > 45° at all loads |
| 6 | PVT Corners | `ngspice -b tb_top_pvt.spice` | All specs at all corners |

### After ALL Fixes

Regenerate ALL 14 plots with REAL simulation data:
```bash
for tb in dc_reg startup transient psrr lstb pvt modes; do
  ngspice -b tb_top_${tb}.spice
done
python3 plot_all.py
```

Update README.md with:
- All 14 plots embedded (REAL data, no estimations)
- Full spec table with measured values
- Honest documentation of any remaining limitations

---

## 4. The Experiment Loop

### LOOP FOREVER

```
1. Read this program and redesign.md
2. Identify the NEXT fix in the sequence (1→2→3→4→5→6)
3. Implement the fix in the relevant block's design.cir
4. Write a block-level testbench and verify standalone
5. If block fails → debug the block fix. Do NOT skip to top-level.
6. Run top-level verification (tests 1-6 above)
7. If top-level passes → git commit -m "exp(10): fix N — <description>"
8. If top-level fails but block passes → debug top-level wiring
9. If top-level fails AND block fails → revert block change, try different approach
10. Move to next fix
11. After all fixes: regenerate all plots, update README, commit
12. Go to step 1 — optimize: increase PM, reduce Iq, improve margins
```

### Commit Strategy

```bash
# Block-level change:
git add pvdd_regulator/XX_blockname/design.cir
git commit -m "exp(XX): <what changed in block>"

# Top-level integration change:
git add pvdd_regulator/10_top_integration/
git commit -m "exp(10): fix N — <measured improvement>"

# ALWAYS push after each successful fix:
git push origin master
```

### What You Can Change

- ANY block's design.cir (00 through 09)
- Top-level design.cir (10)
- Any testbench file
- README.md, plots

### What You CANNOT Change

- specification.json
- evaluate.py
- program.md (the original)
- program_top.md (this file)

### Improvement Criterion

**Keep** if: the fix resolves its target failure AND does not regress any previously passing test.
**Discard** if: any previously passing test now fails.

### NEVER STOP

Work through all 6 fixes. After all pass, optimize: maximize PM, minimize Iq, improve PSRR margins. Generate publication-quality plots. Every improvement gets committed and pushed.

---

## 5. Absolute Rules

1. **Block-level verification FIRST.** Never commit a block change without standalone testing.
2. **Real Sky130 PDK only.** No behavioral models, no ideal op-amps, no VerilogA.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Honest measurements.** Every number in README must come from a real ngspice simulation. No estimations, no placeholders, no synthetic curves.
5. **Every plot must be real.** If you can't simulate it, say "NOT YET MEASURED" — don't fake it.
6. **Push through difficulty.** The cascode and large cap changes WILL affect loop dynamics. Debug them — don't revert to v25b.
