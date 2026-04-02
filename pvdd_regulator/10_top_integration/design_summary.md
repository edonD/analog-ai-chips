# PVDD 5.0V LDO Regulator — Design Summary

**Process:** SkyWater SKY130A (130nm, open-source)
**Date:** 2026-04-02
**Simulator:** ngspice-42
**Status:** Post-review redesign complete (FIX-1 through FIX-13)

---

## 1. Architecture Overview

External-capacitor LDO regulator generating 5.0V PVDD from 5.4–10.5V BVDD. BVDD-powered error amplifier eliminates the startup deadlock (EA works from the moment BVDD appears). 1µF external cap provides dominant pole for unconditional stability.

### Block Hierarchy

| Block | Function | Key Devices | Post-Fix Status |
|-------|----------|-------------|-----------------|
| 00 | Error Amplifier | Two-stage OTA: PMOS diff pair + NFET CS/PFET load. Cc=20pF, Rc=8kΩ | FIX-5: Cc 2→20pF. FIX-10: unused pvdd port removed |
| 01 | Pass Device | 10× PFET W=50µm L=0.5µm m=2 (1mm total) | No changes needed |
| 02 | Feedback Network | xhigh_po divider: R_TOP=364kΩ, R_BOT=118kΩ, ratio 0.2452 | FIX-11: 2pF filter cap on vfb |
| 03 | Compensation | Empty placeholder — all comp is EA-internal (Cc=20pF + Rc=8kΩ) | FIX-13: documented honestly |
| 04 | Current Limiter | Bandgap-referenced comparator: ibias mirror 50:1, BVDD cascode bias | FIX-1: replaced Vth detection. FIX-7: BVDD cascode bias |
| 05 | UV/OV Comparators | NMOS diff pair, 1.8V domain (SVDD). UV=4.39V, OV=5.51V | FIX-6: all resistors PDK xhigh_po |
| 06 | Level Shifter | Cross-coupled PMOS, SVDD↔BVDD | No changes needed |
| 07 | MOS Voltage Clamp | 4-device N-P-N-P stack + series Rstack + PTAT compensation | FIX-2: PTAT mirror. FIX-12: renamed from "Zener" |
| 08 | Mode Control | BVDD ladder, 4 Schmitt comparators, combinational logic | Dead vref port removed |
| 09 | Startup | Rgate=1kΩ, ea_en pullup, startup_done detector | FIX-8: Rss→PDK. FIX-9: startup_done to port |
| 10 | Top Integration | Soft-start RC, output caps, mode control wiring, POR pullup | FIX-3: mc_ea_en, pass_off wired. FIX-8: Css=22nF external |

### Signal Flow

```
BVDD (5.4-10.5V) ──┬── Pass PMOS (1mm) ──── PVDD (5.0V) ──┬── Load
                    │       ↑ gate                          │
                    │   Rgate=1kΩ                           ├── Feedback (364k/118k)
                    │       ↑                               │       ↓ vfb
                    │   Error Amp (BVDD-powered)            ├── Cfb (2pF)
                    │    ↑ vref_ss    ↓ vfb                 │
                    │   Soft-start RC ← avbg (1.226V)       ├── Cload (200pF)
                    │                                       ├── Cout_ext (1µF, EXTERNAL)
                    ├── Mode Control (BVDD ladder)          ├── UV/OV (SVDD domain)
                    │    ↓ mc_ea_en → ea_en                 ├── MOS Clamp (PTAT-comp)
                    │    ↓ pass_off → gate pullup           └── Current Limiter (bandgap-ref)
                    └── ibias (1µA bandgap) → mirror chains
```

### External Components Required

| Component | Value | Purpose |
|-----------|-------|---------|
| Cout_ext | 1µF ceramic | Load transient, dominant pole (MANDATORY) |
| Css | 22nF ceramic | Soft-start RC (MANDATORY, 11mm² unrealizable on-chip) |
| Vavbg | 1.226V bandgap | Voltage reference (from separate bandgap block) |
| Iibias | 1µA | Current reference (from bandgap, PTAT) |

---

## 2. Specification Summary — TT 27°C

| # | Specification | Measured | Limit | Result |
|---|---------------|----------|-------|--------|
| 1 | Output Voltage | 4.984 V | 4.825–5.175 V (±3.5%) | **PASS** |
| 2 | Startup Peak (1V/µs ramp) | 4.984 V | < 5.5 V | **PASS** |
| 3 | Startup Settling (1%) | ~10.4 ms | report | OK |
| 4 | Load Transient Undershoot (1→10mA) | 74 mV | < 150 mV | **PASS** |
| 5 | Line Regulation (5.5–10.5V) | 0.9 mV/V | < 5 mV/V | **PASS** |
| 6 | PSRR @ DC | -60.3 dB | < -40 dB | **PASS** |
| 7 | PSRR @ 1 kHz | -51.5 dB | < -20 dB | **PASS** |
| 8 | Current Limit Trip | ~50 mA | < 80 mA | **PASS** |
| 9 | UV Threshold | 4.39 V | 4.0–4.6 V | **PASS** |
| 10 | OV Threshold | 5.51 V | 5.3–5.7 V | **PASS** |
| 11 | Phase Margin (10mA) | ~80° | > 45° | **PASS** |
| 12 | UGB | ~2.4 kHz | report | OK (low, see §6) |
| 13 | Quiescent Current | ~269 µA | < 300 µA | **PASS** (marginal) |

---

## 3. Full PVT Results — 15 Corners

### 3.1 DC Regulation (PVDD at 1mA load)

**Spec: 4.825–5.175V (±3.5%)**

| Corner | -40°C | 27°C | 150°C |
|--------|-------|------|-------|
| TT | **5.728V ✗** | 4.984V ✓ | 4.980V ✓ |
| SS | 4.983V ✓ | 4.979V ✓ | 4.980V ✓ |
| FF | 4.985V ✓ | 4.985V ✓ | 4.979V ✓ |
| SF | 4.985V ✓ | 4.984V ✓ | 4.980V ✓ |
| FS | 4.984V ✓ | 4.983V ✓ | 4.978V ✓ |

**14/15 PASS.** TT -40°C fails at 5.728V (+14.6%).

### 3.2 Startup Peak

**Spec: < 5.5V**

| Corner | -40°C | 27°C | 150°C |
|--------|-------|------|-------|
| TT | **5.728V ✗** | 4.984V ✓ | 4.980V ✓ |
| SS | 4.983V ✓ | 4.979V ✓ | 4.980V ✓ |
| FF | 4.985V ✓ | 4.985V ✓ | 4.979V ✓ |
| SF | 4.985V ✓ | 4.984V ✓ | 4.980V ✓ |
| FS | 4.984V ✓ | 4.983V ✓ | 4.978V ✓ |

**14/15 PASS.** Same TT -40°C failure.

### 3.3 Load Transient (1→10mA step)

**Spec: undershoot < 150mV**

| Corner | -40°C | 27°C | 150°C |
|--------|-------|------|-------|
| TT | **6278mV ✗** | 68mV ✓ | 86mV ✓ |
| SS | 59mV ✓ | **786mV ✗** | 91mV ✓ |
| FF | 138mV ✓ | 65mV ✓ | 77mV ✓ |
| SF | 61mV ✓ | 69mV ✓ | 78mV ✓ |
| FS | 56mV ✓ | 66mV ✓ | **1067mV ✗** |

**10/15 PASS.** Failures at TT-40 (DC reg broken), SS 27°C (pass device drive), FS 150°C (slow PMOS + hot).

### 3.4 Current Limit (short circuit)

**Spec: < 80mA**

| Corner | -40°C | 27°C | 150°C |
|--------|-------|------|-------|
| TT | 52.6mA ✓ | 49.9mA ✓ | 45.9mA ✓ |
| SS | 56.0mA ✓ | 52.8mA ✓ | 48.3mA ✓ |
| FF | 49.4mA ✓ | 47.2mA ✓ | 43.8mA ✓ |
| SF | 51.9mA ✓ | 49.5mA ✓ | 45.8mA ✓ |
| FS | 53.7mA ✓ | 50.6mA ✓ | 46.3mA ✓ |

**15/15 PASS.** Range 43.8–56.0mA (1.28× spread). This is the biggest win from FIX-1 (was 3.1× spread, 44–137mA).

### 3.5 UV/OV Trip Points (from FIX-6 verification)

| Corner | UV Trip | OV Trip |
|--------|---------|---------|
| TT 27°C | 4.19–4.39V ✓ | 5.51V ✓ |
| SS 150°C | 4.20–4.38V ✓ | 5.51V ✓ |
| FF -40°C | 4.18–4.40V ✓ | 5.51V ✓ |

OV trip variation < 0.02% across corners (ratio-based TC cancellation).

### 3.6 Overall PVT Summary

| Spec | Tested | PASS | FAIL | Rate |
|------|--------|------|------|------|
| DC Regulation | 15 | 14 | 1 | 93% |
| Startup Peak | 15 | 14 | 1 | 93% |
| Load Transient | 15 | 10 | 5 | 67% |
| Current Limit | 15 | 15 | 0 | **100%** |
| **Total** | **60** | **53** | **7** | **88%** |

**10 of 15 corners pass all specs.** 5 corners have at least one failure.

---

## 4. Complete Fix Tracker

### P0 — Critical

| Fix | Issue | Solution | Before | After |
|-----|-------|----------|--------|-------|
| FIX-1 | Current limiter 3.1× PVT spread (Vth-based) | Bandgap-referenced comparator: ibias mirror 50:1 | 44–137mA | 43.8–56.0mA (1.28×) |
| FIX-2 | Zener clamp 40% PVT failure (Vth drift) | 4-device stack + series Rstack + PTAT mirror | 4.86–6.20V onset | 5.51–6.46V onset |

### P1 — High

| Fix | Issue | Solution |
|-----|-------|----------|
| FIX-3 | Mode control outputs floating | mc_ea_en→ea_en (100Ω), pass_off→inverter+PFET gate pullup |
| FIX-4 | Comments describe non-existent circuits | Removed ghost cascode refs, corrected all values in all design.cir |
| FIX-5 | Cc=2pF (no Miller effect, UGB=1.9kHz) | Cc=20pF, Rc=8kΩ. PM improved from ~130° to ~80° at 10mA |

### P2 — Medium

| Fix | Issue | Solution |
|-----|-------|----------|
| FIX-6 | UV/OV ideal resistors | All 8 resistors → PDK xhigh_po. Trip points TC-compensated |
| FIX-7 | Cascode bias tied to PVDD (fails during short circuit) | BVDD resistor divider (already done in FIX-1) |
| FIX-8 | 22nF Css unrealizable on-chip | Rss→PDK xhigh_po, Css documented as external pin requirement |

### P3 — Polish

| Fix | Issue | Solution |
|-----|-------|----------|
| FIX-9 | startup_done signal unused | Routed to top-level pvdd_regulator port |
| FIX-10 | EA pvdd port unused (EA is BVDD-powered) | Removed from subcircuit and top-level |
| FIX-11 | No HF filter on feedback node | Added 2pF cap across R_BOT |
| FIX-12 | "Zener Clamp" misnomer (no Zener diodes in SKY130) | Renamed to "MOS Voltage Clamp" |
| FIX-13 | Block 03 comp ghost README | Header rewritten to document empty status honestly |

### Additional cleanup (post P3)

- Removed dead `vref` port from mode_control subcircuit (was declared but never used internally)

---

## 5. Remaining Issues (Not Fixed)

These were identified in the design review (opinions.md) but not addressed because they require architectural changes or are beyond the scope of the fix campaign.

### 5.1 EA Stage 2 Has No Cascode

**Impact:** 15–20dB lower Stage 2 gain and PSRR than a cascoded version.
**Why not fixed:** Adding a cascode changes the output swing and requires re-tuning bias and compensation. The current PSRR (-60dB DC) meets spec. Would be a worthwhile improvement in a v2 redesign.

### 5.2 UGB Remains Low (~1–2.4 kHz)

**Impact:** Loop cannot suppress disturbances above ~2kHz. Transient response relies entirely on the 1µF cap.
**Why not fixed:** UGB is limited by the 1µF external cap creating a dominant pole at ~1.6Hz. Increasing Cc from 2→20pF helped (PM from 130°→80°) but cannot overcome the fundamental limit of a 1µF cap. Proper fix: reduce external cap to 100nF–470nF and retune compensation for 100–500kHz UGB. This requires significant re-verification.
**Industry context:** Published 50mA external-cap LDOs achieve 100–500kHz UGB with 1µF (TI TPS7A series, ADI ADP1740). The difference is they use 20–50pF Miller compensation to properly split the EA poles.

### 5.3 Quiescent Current (269µA)

**Impact:** 10–100× higher than state-of-the-art (TI TPS7A20: 1µA, ADI ADP150: 9µA).
**Why not fixed:** Main contributors are EA bias (~86µA via 40× mirror), feedback divider (~10µA), mode control ladder (~17µA). Reducing Iq would require redesigning the bias chain (lower mirror ratio), increasing feedback resistance, and optimizing the mode control ladder. All are feasible but each requires re-verification.

### 5.4 Mode Control PVDD-Powered Logic During POR

**Impact:** When BVDD is ramping and PVDD=0V, the mode control comparators have no supply. Outputs may be undefined.
**Mitigation:** pass_off gate pullup (FIX-3) ensures the pass device is OFF during POR regardless of mode control state. The BVDD-powered POR pullup inverter works from the moment BVDD appears.
**Proper fix:** Power mode control from BVDD, not PVDD.

### 5.5 Mode Control L=100µm Feedback NFETs

**Impact:** Enormous process variation on these very-long-channel devices. Hysteresis values will spread widely across corners.
**Why not fixed:** Would require redesigning the Schmitt trigger approach (replace with resistors or standard hysteresis topology). The mode control passes at TT 27°C; full PVT characterization of thresholds is needed but was not in scope.

### 5.6 No ESD Protection

**Impact:** No protection against ESD events on any pin.
**Why not fixed:** ESD requires dedicated GGNMOS or SCR clamp cells, which are a separate layout/design effort. The MOS voltage clamp (Block 07) provides functional OV protection but is far too slow for ESD (nanosecond) events.

### 5.7 No Monte Carlo Verification

**Impact:** The ±3.5% output accuracy spec depends on resistor matching and bandgap accuracy, neither verified with MC.
**Why not fixed:** MC requires 500+ runs per corner, which is computationally expensive. The PVT campaign (15 corners) validates process+temperature variation but not mismatch. MC is essential for tape-out readiness.

### 5.8 Pass Device SOA at Sustained Short Circuit

**Impact:** At SS 150°C, the current limiter allows 48.3mA. At BVDD=10.5V: P = 10.5V × 48.3mA = 507mW. For a 1mm PMOS, thermal analysis is needed.
**Mitigation:** Current limiter now trips at ≤56mA at all corners (was 137mA at SS 150°C before FIX-1).

---

## 6. Lessons Learned

### 6.1 Vth-Based Sensing is Fragile

The original current limiter used `Isense × Rs > Vth_nmos` as the trip condition. Both Rs (xhigh_po TC1=-1.47e-3/°C) and Vth (-1 to -2mV/°C) drift in the same direction at hot corners, compounding to give 3.1× variation (44–137mA). The fix (bandgap-referenced mirror comparator) reduced this to 1.28× by making the trip threshold proportional to ibias, which comes from a temperature-compensated bandgap.

**Takeaway:** Never use raw Vth as a threshold reference in any protection or precision circuit. Always reference to a bandgap-derived quantity.

### 6.2 MOSFET "Zener" Stacks Have Inherent TC Problems

The MOS Vth stack (5 diode-connected MOSFETs) drifts ~3mV/°C per device × 5 = 15mV/°C. Over the -40 to 150°C range: 2.85V total shift. The PTAT current compensation approach (sinking a temperature-proportional current from the gate node) reduced this, and replacing one FET with a PDK resistor (whose TC is more predictable than Vth) further improved tracking.

**Takeaway:** In processes without true Zener diodes (like SKY130), MOS clamp stacks are inherently PVT-sensitive. Budget for trimming or use a bandgap-referenced active clamp for tight onset accuracy.

### 6.3 Documentation Rot is Insidious

The design went through 10+ iterations. At each iteration, the circuit changed but the comments and READMEs didn't always follow. By the time of review, the EA header described a cascode that was removed in v5, Block 03 had a 150-line README for components that no longer existed, and the top-level README cited Cc=98pF when the actual value was 2pF.

**Takeaway:** Comments are code. Every circuit change must update every comment that references the changed element. Automated checks (grep for referenced instance names, verify they exist) would catch most of this.

### 6.4 1µF External Cap Dominates Everything

With a 1µF external cap, the dominant pole is at f = 1/(2π × Rout × 1µF) ≈ 1–10Hz. No amount of internal compensation tuning can push the UGB above ~10kHz without reducing the external cap. The 1µF cap is essential for transient performance (ΔV = Istep × dt / C) but it caps the achievable bandwidth.

**Takeaway:** Choose the external cap value as a design decision early, not as a band-aid. If you need UGB > 100kHz, use ≤100nF external cap and design the EA for higher bandwidth. If you accept UGB < 10kHz, 1µF gives bulletproof stability but sluggish response.

### 6.5 Ratio-Based Dividers Provide Free TC Cancellation

The UV/OV trip point variation was < 0.6% across PVT corners after replacing ideal resistors with PDK xhigh_po. The key: both R_top and R_bot are the same resistor type, so the divider ratio R_bot/(R_top+R_bot) is first-order TC-independent. The same principle applies to the feedback network (Block 02), which uses matched xhigh_po resistors.

**Takeaway:** Always use the same resistor type for both legs of a voltage divider. The absolute resistance may drift ±20% across temperature, but the ratio stays within ±1%.

### 6.6 Mode Control Must Be Wired to Matter

The mode control block (Block 08) was designed, verified in isolation (16/16 specs pass), and then... not connected. The ea_en was hardwired HIGH, pass_off was floating, and bypass_en had no target. This is the classic "integration gap" where individually correct blocks fail to work as a system because the glue logic is missing.

**Takeaway:** Integration verification should check that every block output is connected to something meaningful. An ERC (electrical rule check) tool would have flagged the floating nets immediately.

---

## 7. Architecture Assessment

### What Works Well

1. **BVDD-powered EA** — eliminates startup deadlock, simplifies the power-up sequence
2. **RC soft-start** — simple, robust, corner-independent (RC product is constant for matched materials)
3. **Matched xhigh_po dividers** — inherent TC cancellation for feedback and UV/OV thresholds
4. **Bandgap-referenced current limiter** — 1.28× PVT spread is approaching production quality
5. **Brick-wall current limit** — appropriate for 50mA-class regulator (foldback not needed)
6. **Separate SVDD domain for UV/OV** — comparators work regardless of PVDD state

### What Needs Architectural Rethinking

1. **Compensation strategy** — the 1µF cap + 20pF internal Miller gives stability but very low bandwidth. For a responsive LDO, either reduce external cap or move to a capless topology (class-AB output, FVF)
2. **EA output stage** — simple NFET CS + PFET load has limited gain and PSRR. A cascode or regulated-cascode would add 15–20dB
3. **Quiescent current** — 269µA is acceptable for automotive but 10× too high for portable. The 40× bias mirror is the main contributor
4. **Mode control supply domain** — PVDD-powered logic during POR is a race condition. Should be BVDD-powered

### Production Readiness Scorecard

| Criterion | Status | Notes |
|-----------|--------|-------|
| TT 27°C specs | ✅ All pass | 10/10 testable specs pass |
| PVT corners (15) | ⚠️ 88% | 7 failures across 5 corners |
| Monte Carlo | ❌ Not done | Required for tape-out |
| ESD | ❌ Not done | Need GGNMOS/SCR clamps |
| Layout | ❌ Not done | Schematic only |
| Documentation | ✅ Current | All design.cir comments match circuit |
| Testbenches | ✅ Complete | 15-corner PVT campaign automated |

---

## 8. File Manifest

### Design Files

| File | Description |
|------|-------------|
| `00_error_amp/design.cir` | Two-stage OTA, Cc=20pF/Rc=8kΩ |
| `01_pass_device/design.cir` | 10× PFET, 1mm total width |
| `02_feedback_network/design.cir` | xhigh_po divider, ratio 0.2452 |
| `03_compensation/design.cir` | Empty placeholder |
| `04_current_limiter/design.cir` | Bandgap-referenced comparator |
| `05_uv_ov_comparators/design.cir` | PDK xhigh_po resistors, SVDD domain |
| `06_level_shifter/design.cir` | Cross-coupled PMOS |
| `07_zener_clamp/design.cir` | MOS voltage clamp, PTAT-compensated |
| `08_mode_control/design.cir` | BVDD ladder, Schmitt triggers |
| `09_startup/design.cir` | Rgate=1kΩ, startup_done detector |
| `10_top_integration/design.cir` | v10, all blocks wired |

### Verification Files

| File | Description |
|------|-------------|
| `10_top_integration/pvt_results.md` | Full 15-corner PVT data |
| `10_top_integration/sky130_top.lib.spice` | Combined model library (5 corners) |
| `10_top_integration/tb_plot[1-7]_*.spice` | Plot generation testbenches |
| `10_top_integration/tb_pvt_a_*.spice` | PVT campaign testbenches |
| `10_top_integration/fix_priority.md` | Fix tracker (FIX-1 through FIX-13) |
| `10_top_integration/opinions.md` | Full design review with recommendations |

### Generated Plots

| Plot | File | Key Result |
|------|------|------------|
| Startup Transient | `plot_startup.png` | 4.984V, zero overshoot, ~10ms settling |
| Load Transient | `plot_load_transient.png` | 74mV undershoot (spec < 150mV) |
| PSRR | `plot_psrr.png` | -60.3dB DC, -51.5dB @ 1kHz |
| Bode Plot | `plot_bode.png` | Stable, ~80° PM at 10mA |
| Line Regulation | `plot_line_reg.png` | 0.9 mV/V over 5.5–10.5V |
| Current Limit | `plot_current_limit.png` | ~50mA trip, clean foldback |
