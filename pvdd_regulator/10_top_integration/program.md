# Block 10: Top Integration — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** The top-level design contains ONLY `.include` references to the block-level `design.cir` files, which contain ONLY Sky130 PDK device instantiations. **No exceptions. No behavioral models anywhere in the hierarchy. No ideal components except the allowed external references.**
2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** The ONLY ideal components allowed in the TOP-LEVEL netlist are:
   - `V_AVBG` (bandgap reference, 1.226V DC source) — external chip block
   - `I_BIAS` (current reference, 1uA DC source) — external chip block
   - `V_BVDD` (battery supply source for testbenches)
   - `V_SVDD` (2.2V supply for testbenches)
   - Testbench stimulus sources (pulse, sine, PWL for transient tests)
   - Load resistors/capacitors in testbenches
3. **ALL SIMULATIONS IN NGSPICE.** No HSPICE, no Spectre, no Xyce. Fix convergence with `.option` settings — do not switch simulators.
4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.** Run all 18 verification tests. Every number in the final report must come from a re-runnable `.spice` testbench.
5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** Top-level integration will expose problems invisible at block level: loading effects, supply coupling, race conditions, convergence failures. Fix them in the block designs or the integration netlist. Do not simplify.

---

## Purpose

Block 10 connects all sub-blocks (00-09) into the complete PVDD 5V LDO regulator and runs the full verification plan. This is where the design is proven or broken. Every specification from the master `program.md` must be verified here with full Sky130 PDK simulations in ngspice.

**This block produces the final deliverable:** a complete, re-runnable SPICE netlist of the PVDD regulator that meets all specifications.

---

## Interface (Top-Level Regulator)

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Input | 5.4-10.5V | Battery supply input |
| `pvdd` | Output | 5.0V +/-3.5% | Regulated 5V output |
| `gnd` | Supply | 0V | Ground |
| `avbg` | Input | 1.226V | Bandgap reference (ideal source) |
| `ibias` | Input | 1uA | Bias current reference (ideal source) |
| `svdd` | Supply | 2.2V | Low-voltage digital supply |
| `en` | Input | SVDD domain | Master enable |
| `en_ret` | Input | SVDD domain | Retention mode enable |
| `uv_flag` | Output | SVDD domain | Undervoltage flag (level-shifted) |
| `ov_flag` | Output | SVDD domain | Overvoltage flag (level-shifted) |
| `mode[1:0]` | Output | SVDD domain | Operating mode status |

---

## Target Specifications (Full Regulator)

These are the master specs from `program.md`. Every row must be verified.

| # | Parameter | Min | Typ | Max | Unit | Notes |
|---|-----------|-----|-----|-----|------|-------|
| 1 | Input voltage (BVDD) | 5.4 | 7.0 | 10.5 | V | |
| 2 | Output voltage (PVDD) | 4.8 | 5.0 | 5.17 | V | +/-3.5% over PVT and load |
| 3 | Dropout voltage | -- | 400 | -- | mV | At BVDD=5.4V, 50 mA |
| 4 | Load current (active) | 0 | -- | 50 | mA | |
| 5 | Load transient undershoot | -- | -- | 150 | mV | 1mA -> 10mA step, 1us |
| 6 | Load transient overshoot | -- | -- | 150 | mV | 10mA -> 1mA step, 1us |
| 7 | Internal load cap | -- | 200 | -- | pF | |
| 8 | Line regulation | -- | -- | 5 | mV/V | |
| 9 | Load regulation | -- | -- | 2 | mV/mA | |
| 10 | Quiescent current (active) | -- | -- | 300 | uA | |
| 11 | Quiescent current (retention) | -- | -- | 10 | uA | |
| 12 | UV threshold | 4.0 | 4.3 | 4.5 | V | |
| 13 | OV threshold | 5.25 | 5.5 | 5.7 | V | |
| 14 | Phase margin | 45 | -- | -- | deg | All conditions |
| 15 | Gain margin | 10 | -- | -- | dB | All conditions |
| 16 | PSRR @ DC | 40 | -- | -- | dB | |
| 17 | PSRR @ 10kHz | 20 | -- | -- | dB | |
| 18 | Temperature range | -40 | 27 | 150 | C | |

---

## Topology (Integration Architecture)

The top-level netlist connects all blocks following the master architecture:

```
    V_BVDD (5.4-10.5V)
      |
      +--------[Block 07: Zener Clamp]--------+
      |                                        |
      +--------[Block 09: Startup]-------+     |
      |                                  |     |
      +--S [Block 01: Pass Device] D-----+-----+--- PVDD (5.0V)
      |        |G                        |         |
      |        |                    [Block 04:   [200pF Cload]
      |        |                   Current Lim]    |
      |   [Block 03:                               GND
      |   Compensation]                   |
      |        |                    [Block 02: Feedback]
      |   [Block 00:                      |
      |   Error Amp] <---vfb------[R_top]--+--[R_bot]--GND
      |        |                              |
      |   V_REF (1.226V)                    V_FB
      |        |
      |   [Block 05: UV/OV]
      |        |
      +---[Block 06: Level Shifter]
      |        |
      +---[Block 08: Mode Control]
               |
          SVDD domain signals (en, en_ret, uv_flag, ov_flag, mode)
```

### Top-Level Netlist Structure

```spice
* PVDD 5V LDO Regulator — Top Integration
* Sky130 PDK, ngspice

.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

* Include all block subcircuits
.include "../00_error_amp/design.cir"
.include "../01_pass_device/design.cir"
.include "../02_feedback_network/design.cir"
.include "../03_compensation/design.cir"
.include "../04_current_limiter/design.cir"
.include "../05_uv_ov_comparators/design.cir"
.include "../06_level_shifter/design.cir"
.include "../07_zener_clamp/design.cir"
.include "../08_mode_control/design.cir"
.include "../09_startup/design.cir"

* Top-level subcircuit
.subckt pvdd_regulator bvdd pvdd gnd avbg ibias svdd en en_ret uv_flag_out ov_flag_out

* Block 01: Pass device
Xpass gate bvdd pvdd pass_device

* Block 00: Error amplifier
Xea avbg vfb gate pvdd gnd ibias ea_en error_amp

* Block 02: Feedback network
Xfb pvdd vfb gnd feedback_network

* Block 03: Compensation
Xcomp gate pvdd gnd compensation

* Block 04: Current limiter
Xilim gate bvdd pvdd gnd ilim_flag current_limiter

* Block 05: UV/OV comparators
Xuv pvdd avbg uv_flag pvdd gnd uvov_en uv_comparator
Xov pvdd avbg ov_flag pvdd gnd uvov_en ov_comparator

* Block 06: Level shifters
Xls_en  en_bvdd en     bvdd svdd gnd level_shifter_up
Xls_uv  uv_flag uv_flag_out pvdd svdd gnd level_shifter_down
Xls_ov  ov_flag ov_flag_out pvdd svdd gnd level_shifter_down

* Block 07: Zener clamp
Xzener pvdd gnd zener_clamp

* Block 08: Mode control
Xmode bvdd pvdd svdd gnd avbg en_ret bypass_en ea_en ref_sel uvov_en ilim_en mode_control

* Block 09: Startup
Xstart bvdd pvdd gate gnd avbg startup_done ea_en startup

* Internal load capacitor
Cload pvdd gnd 200p

.ends pvdd_regulator
```

---

## Verification Plan (18-Point)

This is the complete verification plan from the master `program.md`. **Every test must pass. No exceptions.**

### Test 1: DC Regulation
| Item | Detail |
|------|--------|
| Testbench | `tb_top_dc_reg.spice` |
| Setup | BVDD=7V, sweep Iload 0 to 50mA |
| Measure | VPVDD at each load point |
| Pass | VPVDD = 5.0V +/-3.5% (4.825V to 5.175V) at all loads |

### Test 2: Line Regulation
| Item | Detail |
|------|--------|
| Testbench | `tb_top_line_reg.spice` |
| Setup | Iload=10mA, sweep BVDD 5.4 to 10.5V |
| Measure | dVPVDD / dVBVDD |
| Pass | Line regulation < 5 mV/V |

### Test 3: Load Regulation
| Item | Detail |
|------|--------|
| Testbench | `tb_top_load_reg.spice` |
| Setup | BVDD=7V, sweep Iload 0 to 50mA |
| Measure | dVPVDD / dILOAD |
| Pass | Load regulation < 2 mV/mA |

### Test 4: Load Transient (Undershoot)
| Item | Detail |
|------|--------|
| Testbench | `tb_top_load_tran.spice` |
| Setup | 1mA -> 10mA step in 1us, BVDD=7V |
| Measure | Max undershoot on PVDD |
| Pass | Undershoot < 150 mV |

### Test 5: Load Transient (Overshoot)
| Item | Detail |
|------|--------|
| Testbench | `tb_top_load_tran.spice` |
| Setup | 10mA -> 1mA step in 1us, BVDD=7V |
| Measure | Max overshoot on PVDD |
| Pass | Overshoot < 150 mV |

### Test 6: Loop Stability
| Item | Detail |
|------|--------|
| Testbench | `tb_top_lstb.spice` |
| Setup | Break loop at vfb, AC sweep, at Iload = 0, 1mA, 10mA, 50mA |
| Measure | Phase margin and gain margin |
| Pass | PM > 45 deg, GM > 10 dB at ALL load points |

### Test 7: PSRR
| Item | Detail |
|------|--------|
| Testbench | `tb_top_psrr.spice` |
| Setup | AC source on BVDD (DC=7V + AC=1), measure at PVDD |
| Measure | PSRR = 20*log10(Vac_pvdd / Vac_bvdd) |
| Pass | PSRR > 40 dB @ DC, > 20 dB @ 10 kHz |

### Test 8: Startup (Normal)
| Item | Detail |
|------|--------|
| Testbench | `tb_top_startup.spice` |
| Setup | BVDD ramp 0 -> 10.5V at 1 V/us |
| Measure | PVDD waveform: monotonicity, settling, overshoot |
| Pass | Monotonic, no oscillation, settle < 100 us |

### Test 9: Startup (Fast)
| Item | Detail |
|------|--------|
| Testbench | `tb_top_startup_fast.spice` |
| Setup | BVDD ramp 0 -> 10.5V at 10 V/us |
| Measure | Max PVDD overshoot |
| Pass | No overshoot > 5.5V |

### Test 10: Dropout
| Item | Detail |
|------|--------|
| Testbench | `tb_top_dropout.spice` |
| Setup | Iload=50mA, sweep BVDD 4.5 -> 6V |
| Measure | VPVDD vs VBVDD |
| Pass | VPVDD within 100 mV of BVDD until regulation starts; regulated at BVDD > 5.4V |

### Test 11: Current Limit
| Item | Detail |
|------|--------|
| Testbench | `tb_top_ilim.spice` |
| Setup | Rload=0.1 ohm (near short), BVDD=7V |
| Measure | Output current |
| Pass | Iout clamped < 80 mA |

### Test 12: UV Threshold
| Item | Detail |
|------|--------|
| Testbench | `tb_top_uv.spice` |
| Setup | Sweep PVDD externally (disconnect regulator, force PVDD) |
| Measure | UV flag trip point |
| Pass | Trip at 4.3V +/-0.3V |

### Test 13: OV Threshold
| Item | Detail |
|------|--------|
| Testbench | `tb_top_ov.spice` |
| Setup | Sweep PVDD externally (disconnect regulator, force PVDD) |
| Measure | OV flag trip point |
| Pass | Trip at 5.5V +/-0.2V |

### Test 14: Mode Transitions
| Item | Detail |
|------|--------|
| Testbench | `tb_top_modes.spice` |
| Setup | BVDD ramp through all thresholds (0 -> 10.5V -> 0) |
| Measure | All mode output signals |
| Pass | Clean transitions, no glitches, correct sequence |

### Test 15: PVT Corners
| Item | Detail |
|------|--------|
| Testbench | `tb_top_pvt.spice` |
| Setup | Tests 1-8 at SS/FF/SF/FS corners and -40/27/150C |
| Measure | All parameters from tests 1-8 |
| Pass | All specs met at every corner/temperature combination |

### Test 16: Quiescent Current
| Item | Detail |
|------|--------|
| Testbench | `tb_top_iq.spice` |
| Setup | BVDD=7V, no load (Iload=0) |
| Measure | Total current from BVDD |
| Pass | Iq < 300 uA (active), < 10 uA (retention) |

### Test 17: Retention Mode
| Item | Detail |
|------|--------|
| Testbench | `tb_top_retention.spice` |
| Setup | BVDD=3.5V, Iload=0.5mA |
| Measure | PVDD voltage |
| Pass | PVDD tracks BVDD (bypass mode, PVDD ~ BVDD) |

### Test 18: Power Consumption
| Item | Detail |
|------|--------|
| Testbench | `tb_top_power.spice` |
| Setup | All operating modes |
| Measure | Total power from BVDD in each mode |
| Pass | Report total. No specific limit, but document. |

---

## Device Selection

No new devices. Block 10 uses only the subcircuits from Blocks 00-09, which contain all the Sky130 devices. The only direct instantiation is the 200 pF load capacitor:

```spice
* Internal load capacitor (200 pF MIM cap)
* Area = 200pF / 2fF/um^2 = 100,000 um^2
* W = 316u, L = 316u (or multiple smaller caps in parallel)
XCload1 pvdd gnd sky130_fd_pr__cap_mim_m3_1 W=316u L=158u
XCload2 pvdd gnd sky130_fd_pr__cap_mim_m3_1 W=316u L=158u
* Total: 2 * 316u * 158u * 2fF/um^2 = 2 * 99,856fF ~ 200pF
```

Or use an ideal 200pF cap in the testbench if the MIM cap causes convergence issues (the load cap is not part of the regulator design — it is an external chip component).

---

## Sizing Procedure

There is no new sizing in Block 10. The integration procedure is:

1. **Step 1: Verify all block `design.cir` files exist and simulate.** Run a smoke test: include all files, run `.op`, confirm no errors.

2. **Step 2: Connect all blocks.** Wire the top-level netlist following the architecture diagram. Pay careful attention to:
   - Net names match across block interfaces
   - Supply domains are correct (which blocks run from PVDD, which from BVDD)
   - Enable signals are properly connected
   - No floating nodes

3. **Step 3: Run the DC operating point.** This is the first real test. If it converges, you are on the right track. If not, debug: check for floating gates, uninitialized nodes, incorrect polarities.

4. **Step 4: Run Test 1 (DC regulation).** This confirms the basic loop works. If PVDD != 5.0V, debug the error amp, feedback ratio, or pass device sizing.

5. **Step 5: Run all 18 tests in sequence.** Fix failures by going back to the relevant block and modifying its design, then re-running the top-level test.

6. **Step 6: PVT corners.** Run the critical tests (1, 4-6, 8) at all corners. This is where most designs fail. Iterate.

---

## Testbench Requirements

| Testbench File | Verification Test # | Measures |
|---------------|-------|----------|
| `tb_top_dc_reg.spice` | 1 | DC regulation vs load |
| `tb_top_line_reg.spice` | 2 | Line regulation vs BVDD |
| `tb_top_load_reg.spice` | 3 | Load regulation vs Iload |
| `tb_top_load_tran.spice` | 4, 5 | Load transient under/overshoot |
| `tb_top_lstb.spice` | 6 | Loop stability (PM, GM) |
| `tb_top_psrr.spice` | 7 | PSRR vs frequency |
| `tb_top_startup.spice` | 8 | Startup (normal ramp) |
| `tb_top_startup_fast.spice` | 9 | Startup (fast ramp) |
| `tb_top_dropout.spice` | 10 | Dropout voltage |
| `tb_top_ilim.spice` | 11 | Current limiting |
| `tb_top_uv.spice` | 12 | UV threshold |
| `tb_top_ov.spice` | 13 | OV threshold |
| `tb_top_modes.spice` | 14 | Mode transitions |
| `tb_top_pvt.spice` | 15 | PVT corner sweep (critical tests) |
| `tb_top_iq.spice` | 16 | Quiescent current |
| `tb_top_retention.spice` | 17 | Retention mode |
| `tb_top_power.spice` | 18 | Power consumption |

---

## Simulation Procedure

**PDK include (in every testbench):**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

**Example: Test 1 — DC Regulation:**
```spice
.include "design.cir"

* External ideal sources
V_BVDD bvdd gnd 7.0
V_AVBG avbg gnd 1.226
V_SVDD svdd gnd 2.2
I_BIAS pvdd ibias 1u

* Instantiate top-level regulator
Xreg bvdd pvdd gnd avbg ibias svdd en en_ret uv_flag ov_flag pvdd_regulator

* Enable
Ven en gnd 2.2
Ven_ret en_ret gnd 0

* Load current sweep
Iload gnd pvdd 0

.dc Iload 0 50m 0.5m

.control
run
plot v(pvdd) vs -i(Iload)
meas dc vpvdd_0mA find v(pvdd) at=0
meas dc vpvdd_50mA find v(pvdd) at=50m
let load_reg = (vpvdd_0mA - vpvdd_50mA) / 50m
print vpvdd_0mA vpvdd_50mA load_reg
wrdata top_dc_reg.csv v(pvdd)
.endc
```

**Example: Test 6 — Loop Stability:**
```spice
.include "design.cir"

V_BVDD bvdd gnd 7.0
V_AVBG avbg gnd 1.226
V_SVDD svdd gnd 2.2
I_BIAS pvdd ibias 1u

* Need to break the loop at vfb inside the regulator
* This requires either:
* 1. Exposing the vfb node in the top subcircuit (add a pin)
* 2. Or running the stability test at the block level (Block 03 testbench)
* Recommended: add vfb as a test pin in the top subcircuit

Xreg bvdd pvdd gnd avbg ibias svdd en en_ret uv_flag ov_flag pvdd_regulator

* Loop break at vfb (requires modification of top subcircuit to expose vfb)
Lbreak vfb_int vfb 1G
Vac vfb_int vfb_sense dc 0 ac 1

Rload pvdd gnd 500    * 10 mA load

.ac dec 100 1 100meg

.control
run
let gain = db(v(vfb_sense))
let phase = 180/PI * ph(v(vfb_sense))
meas ac pm find phase when gain=0
meas ac gm_cross find gain when phase=-180
print pm gm_cross
plot gain phase
.endc
```

**Convergence options for top-level sims:**
```spice
.option reltol=1e-3
.option abstol=1e-10
.option vntol=1e-4
.option gmin=1e-10
.option method=gear
.option maxord=2
.option itl1=1000
.option itl4=500
.option itl6=200
```

---

## Pass/Fail Criteria

**ALL 18 tests must pass. This is the master checklist.**

| Test # | Parameter | Pass Condition |
|--------|-----------|---------------|
| 1 | DC regulation | VPVDD = 5.0V +/-3.5% at 0-50 mA |
| 2 | Line regulation | < 5 mV/V (BVDD 5.4-10.5V) |
| 3 | Load regulation | < 2 mV/mA (0-50 mA) |
| 4 | Load transient undershoot | < 150 mV (1->10 mA step) |
| 5 | Load transient overshoot | < 150 mV (10->1 mA step) |
| 6 | Phase margin | > 45 deg at all loads |
| 6 | Gain margin | > 10 dB at all loads |
| 7 | PSRR @ DC | > 40 dB |
| 7 | PSRR @ 10 kHz | > 20 dB |
| 8 | Startup (1 V/us) | Monotonic, settle < 100 us |
| 9 | Startup (10 V/us) | No overshoot > 5.5V |
| 10 | Dropout | PVDD regulated at BVDD=5.4V, 50mA |
| 11 | Current limit | Iout clamped < 80 mA at short |
| 12 | UV threshold | Trip at 4.3V +/-0.3V |
| 13 | OV threshold | Trip at 5.5V +/-0.2V |
| 14 | Mode transitions | Clean, glitch-free, correct sequence |
| 15 | PVT corners | All above pass at SS/FF/SF/FS, -40/27/150C |
| 16 | Quiescent current | < 300 uA (active), < 10 uA (retention) |
| 17 | Retention mode | PVDD tracks BVDD at 3.5V |
| 18 | Power consumption | Documented for all modes |

---

## Dependencies

**Wave 3 block — requires ALL other blocks (00-09) to be complete.**

| Block | Required Deliverable |
|-------|---------------------|
| Block 00 | `00_error_amp/design.cir` |
| Block 01 | `01_pass_device/design.cir` |
| Block 02 | `02_feedback_network/design.cir` |
| Block 03 | `03_compensation/design.cir` |
| Block 04 | `04_current_limiter/design.cir` |
| Block 05 | `05_uv_ov_comparators/design.cir` |
| Block 06 | `06_level_shifter/design.cir` |
| Block 07 | `07_zener_clamp/design.cir` |
| Block 08 | `08_mode_control/design.cir` |
| Block 09 | `09_startup/design.cir` |

**Integration order (recommended):**
1. First: connect Block 00 + Block 01 + Block 02 + Block 03 (core regulation loop). Run Tests 1-6. Fix any issues.
2. Second: add Block 04 (current limiter). Run Test 11. Verify Tests 1-6 still pass.
3. Third: add Block 05 (UV/OV). Run Tests 12-13.
4. Fourth: add Block 06 + Block 08 (level shifter + mode control). Run Test 14.
5. Fifth: add Block 07 (zener clamp). Run Test 9.
6. Sixth: add Block 09 (startup). Run Tests 8-9.
7. Final: run ALL 18 tests on the complete regulator. Then run Test 15 (PVT corners).

---

## Deliverables

1. `design.cir` — Complete PVDD regulator top-level subcircuit (`.subckt pvdd_regulator ...`), containing only `.include` references and subcircuit instantiations. **This is the primary deliverable of the entire project.**
2. `tb_top_dc_reg.spice` — Test 1: DC regulation
3. `tb_top_line_reg.spice` — Test 2: Line regulation
4. `tb_top_load_reg.spice` — Test 3: Load regulation
5. `tb_top_load_tran.spice` — Tests 4-5: Load transient
6. `tb_top_lstb.spice` — Test 6: Loop stability
7. `tb_top_psrr.spice` — Test 7: PSRR
8. `tb_top_startup.spice` — Test 8: Startup (normal)
9. `tb_top_startup_fast.spice` — Test 9: Startup (fast)
10. `tb_top_dropout.spice` — Test 10: Dropout
11. `tb_top_ilim.spice` — Test 11: Current limit
12. `tb_top_uv.spice` — Test 12: UV threshold
13. `tb_top_ov.spice` — Test 13: OV threshold
14. `tb_top_modes.spice` — Test 14: Mode transitions
15. `tb_top_pvt.spice` — Test 15: PVT corners
16. `tb_top_iq.spice` — Test 16: Quiescent current
17. `tb_top_retention.spice` — Test 17: Retention mode
18. `tb_top_power.spice` — Test 18: Power consumption
19. `README.md` — Final design report: complete specification table with simulated values, pass/fail status for all 18 tests, summary of design choices, known limitations, block-by-block parameter summary
20. `*.png` — Plots for every test: regulation curves, Bode plots, transient waveforms, I-V curves, threshold measurements, mode transition diagrams, PVT corner overlays
21. `verification_summary.md` — Machine-readable summary: 18 rows, each with test name, measured value, spec, pass/fail
