# Fix Priority List — From Design Review (opinions.md)

Ordered by impact. Each fix must be verified at block level, then top level, then committed.

---

## P0 — CRITICAL (blocks the design from being credible)

### FIX-1: Current Limiter PVT Hardening (Block 04)
**Problem:** 3.1× PVT spread (44mA FF-40 to 137mA SS150). At FF-40, trips at 44mA — may false-trigger during normal 50mA load. At SS150, 137mA = 1.44W thermal risk.
**Root cause:** Vth-based detection (Vsense > Vth_nmos) compounds two uncontrolled TCs: Rs (xhigh_po TC1=-1.47e-3/°C) and Vth_nmos (-1 to -2 mV/°C). Both drift in same direction at hot corner.
**Also:** Cascode gate tied to PVDD — during short circuit PVDD≈0V, cascode turns OFF, sense path degenerates.
**Fix approach:**
1. Replace Vth-based detection with bandgap-referenced comparator:
   - Mirror ibias (1µA) through a ratio resistor to create Iref_trip
   - Compare Isense against Iref_trip using a current mirror comparator
   - Trip threshold set by Iref × Rs, where Iref comes from bandgap (±2% TC)
   - Expected PVT spread: ~20% instead of 300%
2. Fix cascode bias: tie to BVDD-derived reference (e.g., BVDD × 0.7 from divider) instead of PVDD, so it works during short circuit.
3. Connect ilim_en from mode control to gate the limiter.
**Verification:** Sweep Iload at TT27, SS150, FF-40. Trip must be 45-75mA at all corners.

### FIX-2: Zener Clamp PVT Hardening (Block 07)
**Problem:** 40% PVT failure (6/15 corners). At FF150, onset drops to 4.86V — BELOW regulated PVDD, clamp fights regulator. At SS-40, onset rises to 6.2V — too late for protection.
**Root cause:** MOS Vth-based stack has inherent ~3mV/°C TC per device × 5 devices = 15mV/°C total. Over 190°C range: 2.85V shift. Plus process corners shift ±500mV.
**Also:** Rpd=500kΩ is an ideal resistor, not PDK. No ESD protection.
**Fix approach:**
1. Replace ideal Rpd with PDK xhigh_po resistor
2. Add temperature compensation to the precision stack:
   - Option A: Add a PTAT current source that biases Rpd, shifting the gate voltage to compensate TC
   - Option B: Use a bandgap-referenced active clamp (comparator + shunt NMOS) instead of passive Vth stack
   - Option C: Tune the N-P-N-P-N stack device sizes (W, L) to minimize TC at the target onset voltage. L=4µm is already good; adjust W ratios for Vth fine-tuning.
3. Verify onset at ALL 15 PVT corners (5 process × 3 temp). Must be within 5.5-6.5V.
4. Add GGNMOS ESD clamp as separate structure (does not replace functional clamp).
**Verification:** DC sweep PVDD at all 15 PVT corners. Onset must stay within window.

---

## P1 — HIGH (design works without these but is fragile)

### FIX-3: Wire Mode Control Outputs (Block 08 → Block 10)
**Problem:** Mode control generates bypass_en, mc_ea_en, ref_sel, ilim_en, pass_off — ALL floating. No POR protection, no bypass mode, no retention mode. ea_en hardwired HIGH.
**Fix:** In top-level design.cir:
- Connect mc_ea_en to ea_en (replace Ren bvdd ea_en 100 in Block 09)
- Connect pass_off to gate pullup (PFET that pulls gate to BVDD)
- Connect ilim_en to current limiter enable
- Connect bypass_en to bypass transmission gate (if exists)
**Risk:** May affect startup sequence. Test startup transient carefully.
**Verification:** Sweep BVDD 0→10.5V, verify correct mode transitions and all outputs sequence properly.

### FIX-4: Fix Documentation Mismatches
**Problem:** Comments in Block 00 describe non-existent cascode. README cites Cc=98pF (actual: 2pF). Block 03 README describes components that don't exist.
**Fix:** Read every design.cir, update all comments to match actual circuit. Update README.md with actual component values.
**Verification:** Grep for discrepancies.

### FIX-5: Increase Inner Miller Cc (Block 00)
**Problem:** Cc=2pF provides almost no Miller effect. DC operating point of Stage 2 is weakly defined. May contribute to .op convergence failures at non-TT corners.
**Fix:** Increase Cc from 2pF to 15-25pF. Adjust Rc accordingly. This gives the EA meaningful standalone stability without relying 100% on external cap.
**Risk:** Changes loop dynamics. Must re-verify PM at all loads.
**Verification:** EA standalone AC (gain, bandwidth, PM). Top-level loop stability at 0/1/10/50mA.

---

## P2 — MEDIUM (improvements for robustness)

### FIX-6: UV/OV Replace Ideal Resistors (Block 05)
**Problem:** R_top, R_bot, R_hyst, R_bias are all ideal SPICE resistors. Trip points are optimistic — real silicon will show more spread.
**Fix:** Replace with sky130_fd_pr__res_xhigh_po. Recalculate divider ratios for PDK resistance formula: R = Rsheet × (L-DL)/(W-DW).
**Verification:** Sweep PVDD, verify UV/OV trip points still within spec.

### FIX-7: Fix Cascode Bias in Current Limiter (Block 04)
**Problem:** cas_bias=PVDD means during short circuit (PVDD≈0V), cascode turns OFF.
**Fix:** Replace cas_bias=pvdd with a BVDD-derived reference: Rcas_top/Rcas_bot divider from BVDD giving ~5V (matching normal PVDD). This stays valid during short circuit.
**Verification:** Short-circuit test at all corners. Clamp current must stay <80mA.

### FIX-8: Soft-Start Cap Realizability (Block 10)
**Problem:** Css=22nF is unrealizable on-chip (~11mm² in MIM). Must be external or replaced.
**Fix:** Either document as external requirement, or replace RC soft-start with current-source-based ramp (standard in production: charge a small cap with a µA-level current source).
**Verification:** Startup transient with new approach. No overshoot.

---

## P3 — LOW (polish)

### FIX-9: Connect startup_done signal (Block 09 → Block 10)
### FIX-10: Remove unused pvdd port from EA (Block 00)
### FIX-11: Add filter cap on feedback node (Block 02)
### FIX-12: Rename "Zener Clamp" to "MOS Voltage Clamp" (Block 07)
### FIX-13: Make Block 03 compensation consistent with actual circuit
