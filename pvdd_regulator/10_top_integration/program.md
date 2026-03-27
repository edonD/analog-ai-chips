# Block 10: Top Integration — Design Program

---

## 1. Setup

### Purpose

Block 10 connects all sub-blocks (00–09) into the complete PVDD 5V LDO regulator and runs the full 18-point verification plan. This is where the design is proven or broken. Every specification from the master `program.md` must be verified here with full Sky130 PDK simulations in ngspice.

This is not a design block — no new circuit is created here. The work is wiring, integration, and comprehensive verification. When top-level tests fail, the fix goes back into the relevant block's `design.cir`, and the top-level test re-runs.

**This block produces the final deliverable:** a complete, re-runnable SPICE netlist of the PVDD regulator that meets all 18 system-level specifications.

### Read Before Starting

Read these files before starting integration:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `10_top_integration/specification.json` — this block's 18-point verification plan
- All block `results.md` files (00–09) — understand what each block achieved and any known residual issues

**All block `design.cir` files must exist and have passed their block-level tests before starting integration.**

### Create results.md

Create `10_top_integration/results.md` before running any simulation. Update it after every test run. It must contain:

- **Integration status table**: block | design.cir present | block tests pass | integrated
- **18-point verification table**: test # | name | measured value | spec | pass/fail
- **Simulation log**: what was integrated, what failed, what was fixed in which block
- **Open issues**: any test not yet passing, with the likely root cause and plan

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance configured for this block only. The instance has:
- Full SkyWater SKY130A PDK installed
- ngspice installed and tested
- This block directory (`10_top_integration/`) as the working directory
- All block `design.cir` files available via `.include`

### What You Can Do

- Write the top-level `design.cir` that `.include`s all block subcircuits and wires them together.
- Write all 18 testbench files listed in the Verification Plan.
- When a test fails, return to the relevant block's `design.cir` and fix it there, then re-run the top-level test.
- Add intermediate testbenches or diagnostic sims at any point to isolate failures.

**Incremental integration order (recommended):**

1. **Blocks 00+01+02+03** — core regulation loop. Run Tests 1, 2, 3, 6.
2. **Add Block 04** — current limiter. Run Test 11. Re-verify Tests 1–3, 6.
3. **Add Block 05** — UV/OV comparators. Run Tests 12, 13.
4. **Add Blocks 06+08** — level shifter + mode control. Run Test 14.
5. **Add Block 07** — zener clamp. Run Test 9 (fast startup).
6. **Add Block 09** — startup. Run Tests 4, 5, 7, 8, 9.
7. **Run ALL 18 tests** on the complete regulator.
8. **Run Test 15** (PVT corners) — all specs at all corners/temperatures.

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria. The evaluator reads it.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md`** — this file defines the design rules.
- **Do not add behavioral models, ideal op-amps, or VerilogA** anywhere in the integration netlist to make a test pass. All fixes go in the block-level `design.cir` files.
- **Do not add ideal sources inside the regulator subcircuit** (only `V_AVBG`, `I_BIAS`, `V_BVDD`, `V_SVDD`, and testbench stimulus are allowed as ideal).

### Goal

All 18 tests must pass. Every spec must be met at all load points, all BVDD values, all PVT corners, and all temperatures. No exceptions. When a test fails, fix the root cause in the block that owns it — do not paper over the failure with a workaround.

### Simplicity Criterion

The top-level netlist should be as simple as possible: `.include` statements and wire connections. If the integration requires special glue circuitry beyond what the blocks provide, question whether the block interfaces were designed correctly. Minimize the number of net names and connections. A clean, readable top-level netlist is a sign of a clean design.

---

### Optimization

At the top-level, the primary optimization target is system-level phase margin under worst-case conditions. Use `optimize.py` to co-sweep Cc (compensation cap from Block 03) and the R1/R2 ratio (feedback network from Block 02) for maximum margin without individually re-optimizing blocks.

**Framework (scipy):**

```python
from scipy.optimize import differential_evolution, minimize
import subprocess, re

def cost(params):
    # Write Cc, R1, R2 into top_integration.cir via .param
    # subprocess.run(['ngspice', '-b', 'run_block.sh'], capture_output=True)
    # Parse pm_min_deg (worst-case PM across 20+ Iload points at SS 150C) from run.log
    # Parse pvdd_accuracy_mV, line_reg_mV from run.log
    # Return -pm_min_deg + accuracy_penalty + regulation_penalty
    pass

result = differential_evolution(cost, bounds=[(1e-12, 50e-12), (100e3, 1e6), (100e3, 1e6)],
                                 maxiter=200, tol=0.01, seed=42, workers=1)
result = minimize(cost, result.x, method='Nelder-Mead', options={'xatol': 1e-13, 'fatol': 0.1})
```

**Variables:** Cc (1–50 pF), R1 (100 kΩ–1 MΩ), R2 (100 kΩ–1 MΩ) — all passed as `.param` into the top-level netlist.

**Objective:** maximize minimum system PM across all 20+ Iload sweep points at SS 150°C (primary metric = `pm_min_deg` from run.log).

**Constraints (penalty if violated):**
- PVDD accuracy 4.826–5.174V at all loads and BVDD values
- Load regulation < 10 mV (0 to 50 mA)
- Line regulation < 5 mV (BVDD 5.4–10.5V)
- PM ≥ 45° at all loads, corners, Cload values
- Output noise < 100 µVrms integrated 10 Hz–100 kHz
- PSRR > 40 dB at 1 kHz
- All 32 verification tests pass

**Note:** system-level co-optimization is sensitive to parasitic interactions. Run at TT 27°C first to find the basin, then verify the solution holds at SS 150°C before committing.

**Commit strategy:** commit per-block. Each system-level improvement is one commit:
```bash
git add pvdd_regulator/10_top_integration/ && git commit -m "exp(10): <what changed>"
```
Never mix block changes in one commit. If a system-level parameter change requires fixing a sub-block, commit the sub-block first, then the integration layer.

---

### Interface (Top-Level Regulator)

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Input | 5.4–10.5V | Battery supply input |
| `pvdd` | Output | 5.0V ±3.5% | Regulated 5V output |
| `gnd` | Supply | 0V | Ground |
| `avbg` | Input | 1.226V | Bandgap reference (ideal source in testbenches) |
| `ibias` | Input | 1 µA | Bias current reference (ideal source in testbenches) |
| `svdd` | Supply | 2.2V | Low-voltage digital supply |
| `en` | Input | SVDD domain | Master enable |
| `en_ret` | Input | SVDD domain | Retention mode enable |
| `uv_flag` | Output | SVDD domain | Undervoltage flag (level-shifted) |
| `ov_flag` | Output | SVDD domain | Overvoltage flag (level-shifted) |

Subcircuit signature: `.subckt pvdd_regulator bvdd pvdd gnd avbg ibias svdd en en_ret uv_flag ov_flag`

---

### System Specifications

| # | Parameter | Min | Typ | Max | Unit | Condition |
|---|-----------|-----|-----|-----|------|-----------|
| 1 | Input voltage (BVDD) | 5.4 | 7.0 | 10.5 | V | Sky130 HV limit |
| 2 | Output voltage (PVDD) | 4.825 | 5.0 | 5.175 | V | ±3.5% over PVT and load |
| 3 | Dropout voltage | — | 400 | — | mV | BVDD=5.4V, 50 mA |
| 4 | Load current (active) | 0 | — | 50 | mA | |
| 5 | Load transient undershoot | — | — | 150 | mV | 1mA→10mA, 1µs |
| 6 | Load transient overshoot | — | — | 150 | mV | 10mA→1mA, 1µs |
| 7 | Internal load cap | — | 200 | — | pF | |
| 8 | Line regulation | — | — | 5 | mV/V | |
| 9 | Load regulation | — | — | 2 | mV/mA | |
| 10 | Quiescent current (active) | — | — | 300 | µA | |
| 11 | Quiescent current (retention) | — | — | 10 | µA | |
| 12 | UV threshold | 4.0 | 4.3 | 4.5 | V | |
| 13 | OV threshold | 5.25 | 5.5 | 5.7 | V | |
| 14 | Phase margin | 45 | — | — | deg | All conditions |
| 15 | Gain margin | 10 | — | — | dB | All conditions |
| 16 | PSRR @ DC | 40 | — | — | dB | |
| 17 | PSRR @ 10 kHz | 20 | — | — | dB | |
| 18 | Temperature range | −40 | 27 | 150 | °C | |

---

### 32-Point Verification Plan

**All 32 tests must pass. No exceptions.**

| # | Name | Setup | Measure | Pass Condition |
|---|------|-------|---------|---------------|
| 1 | DC regulation | BVDD=7V, sweep Iload 0–50 mA | VPVDD | 4.825–5.175V at all loads |
| 2 | Line regulation | Iload=10mA, sweep BVDD 5.4–10.5V | dVPVDD/dVBVDD | < 5 mV/V |
| 3 | Load regulation | BVDD=7V, sweep Iload 0–50 mA | dVPVDD/dILOAD | < 2 mV/mA |
| 4 | Load transient undershoot | 1mA→10mA in 1µs, BVDD=7V | Max undershoot | < 150 mV |
| 5 | Load transient overshoot | 10mA→1mA in 1µs, BVDD=7V | Max overshoot | < 150 mV |
| 6 | Loop stability | Break loop, AC, Iload=0/1/10/50 mA | PM and GM | PM > 45°, GM > 10 dB at ALL loads |
| 7 | PSRR (spot) | AC on BVDD, DC=7V+AC=1V | PSRR at PVDD | > 40 dB @ DC, > 20 dB @ 10 kHz |
| 8 | Startup (normal) | BVDD ramp 0→10.5V at 1 V/µs | PVDD waveform | Monotonic, no oscillation, settle < 100 µs |
| 9 | Startup (fast) | BVDD ramp 0→10.5V at 10 V/µs | Max PVDD peak | < 5.5V |
| 10 | Dropout | Iload=50mA, sweep BVDD 4.5→6V | VPVDD vs VBVDD | Regulated at BVDD=5.4V |
| 11 | Current limit | Rload=0.1Ω, BVDD=7V | Iout | < 80 mA |
| 12 | UV threshold | Sweep PVDD externally | UV flag trip | 4.0–4.6V |
| 13 | OV threshold | Sweep PVDD externally | OV flag trip | 5.3–5.7V |
| 14 | Mode transitions | BVDD ramp 0→10.5V→0 | All mode outputs + PVDD perturbation | Glitch-free; PVDD deviation < 200 mV at each transition |
| 15 | PVT corners | Tests 1–8 at SS/FF/SF/FS × −40/27/150°C | All parameters | All specs met at every condition |
| 16 | Quiescent current | BVDD=7V, no load | Total Ibvdd | < 300 µA active, < 10 µA retention |
| 17 | Retention mode | BVDD=3.5V, Iload=0.5mA | PVDD | Tracks BVDD (bypass mode) |
| 18 | Power consumption | All modes | Total power | Document — no numeric limit |
| 19 | Monte Carlo stability | 500 runs, TT 27°C, Iload=1 mA | PM distribution | mean − 2σ ≥ 45°; no single run below 35° |
| 20 | Full load transient | 0→50mA in 1µs, BVDD=7V; then 50→0mA | Max undershoot and overshoot | Undershoot < 200 mV; overshoot < 200 mV; no oscillation |
| 21 | Line transient | BVDD step +500mV and −500mV at 1V/µs, Iload=10mA | PVDD transient | PVDD deviation < 50 mV; settle < 20 µs |
| 22 | AVBG + IBIAS variation | Sweep AVBG 1.219→1.246V; IBIAS 0.947→1.033µA; all 4 extreme combos | VPVDD accuracy | PVDD within 4.825–5.175V at all combinations |
| 23 | Enable/disable sequence | Toggle en low mid-operation; re-enable; test with PVDD pre-charged | PVDD waveform | Graceful discharge on disable; clean restart on re-enable; no latch |
| 24 | PSRR full frequency | AC sweep 10 Hz–10 MHz on BVDD; at Iload=0, 1, 50 mA | PSRR vs frequency | > 40 dB at DC; > 20 dB at 10 kHz; document roll-off shape and −3 dB frequency |
| 25 | Output noise | .noise simulation on PVDD; 10 Hz–1 MHz | Integrated noise (µVrms) | < 100 µVrms integrated; report spectral density at 1 kHz and 100 kHz |
| 26 | Fine PM sweep | PM at 20+ Iload points 0→50 mA, SS 150°C | PM vs Iload curve | PM ≥ 45° at every point; no conditional stability dip |
| 27 | Cload stability | PM and transient at Cload=200pF, 500pF, 1nF, 10nF | PM and ringing | No oscillation at any Cload; PM ≥ 30° up to 500 pF |
| 28 | Cold crank (system) | BVDD profile: 10.5V→3V→7V (dip and recovery) | PVDD during dip and recovery | PVDD recovers to regulation within 500 µs; no latch |
| 29 | PVDD temperature coefficient | Sweep T −40→150°C; AVBG at nom/min/max | VPVDD vs T | TC < 200 µV/°C; stays within ±3.5% band over full range |
| 30 | Load regulation vs BVDD | Measure LDR at BVDD=5.4V, 7V, 10.5V | dVPVDD/dILOAD at each BVDD | < 2 mV/mA at all BVDD values; report worst case |
| 31 | Combined AVBG + PVT corners | 6 corners: {AVBG=min, AVBG=max} × {SS 150°C, TT 27°C, FF −40°C} | VPVDD accuracy | 4.825–5.175V at all 6 combinations |
| 32 | Pass device SOA (system level) | Full system at BVDD=10.5V, Iload=50mA, T=150°C; startup transient | Pass device Vds×Id product | Operating point inside Sky130 pfet_g5v0d10v5 SOA envelope at all times |

---

### Operating Conditions

- **BVDD:** 5.4 to 10.5V
- **PVDD:** 5.0V nominal
- **Cload:** 200 pF (on-chip, no external cap)
- **AVBG:** 1.226V ideal source
- **IBIAS:** 1 µA ideal source
- **SVDD:** 2.2V ideal source
- **Corners:** SS/TT/FF/SF/FS at −40°C, 27°C, 150°C

---

### Known Integration Challenges

1. **Loading effects invisible at block level.** The error amp, feedback divider, compensation, and pass device interact differently when connected together than in isolation. Re-verify loop stability after each block is added.

2. **Supply coupling.** Blocks sharing PVDD as a supply will couple noise. The current limiter and UV/OV comparators can inject noise through shared supply lines.

3. **Race conditions during mode transitions.** When mode control signals change, the error amp enable and bypass switch may fight briefly. This can cause PVDD glitches. Known silicon issue #m3 was caused by exactly this.

4. **Startup convergence.** Top-level startup simulations with all blocks active are the most complex simulations in the project. Use `.ic` for all supply nodes, set aggressive `.option` tolerances.

5. **Test 15 (PVT corners).** Running Tests 1–8 at 5 corners × 3 temperatures = 15 conditions minimum. This is a large simulation job — automate it with a parametric sweep or loop.

6. **Test 19 (Monte Carlo).** 500-run MC on the full closed loop is the longest simulation in this block — expect 2–4 hours. Run it last after all deterministic tests pass.

7. **Tests 24/25 (PSRR and noise).** PSRR and noise simulations can have convergence issues at low frequency in ngspice. Set `reltol=1e-5` and `abstol=1e-12` for these. Start with a coarse frequency sweep and refine if needed.

8. **Test 26 (fine PM sweep).** A conditional stability dip (PM drops below 45° at some intermediate load) will NOT show up in test 6 which only checks 4 load points. Test 26 is the catch for this failure mode.

9. **Tests 22/31 (AVBG variation).** When sweeping AVBG, also re-check load regulation and transient — a shift in VFB changes the loop's DC operating point and can affect PM through gm changes in the pass device.

---

### Dependencies

Wave 3 — requires ALL of:

| Block | Required File |
|-------|--------------|
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

---

### Testbenches

| File | Test # | Description |
|------|--------|-------------|
| `tb_top_dc_reg.spice` | 1 | DC regulation |
| `tb_top_line_reg.spice` | 2 | Line regulation |
| `tb_top_load_reg.spice` | 3 | Load regulation |
| `tb_top_load_tran.spice` | 4, 5 | Load transient (undershoot and overshoot) |
| `tb_top_lstb.spice` | 6 | Loop stability at all load points |
| `tb_top_psrr.spice` | 7 | PSRR |
| `tb_top_startup.spice` | 8 | Startup at 1 V/µs |
| `tb_top_startup_fast.spice` | 9 | Startup at 10 V/µs |
| `tb_top_dropout.spice` | 10 | Dropout at BVDD = 5.4V |
| `tb_top_ilim.spice` | 11 | Current limit |
| `tb_top_uv.spice` | 12 | UV threshold |
| `tb_top_ov.spice` | 13 | OV threshold |
| `tb_top_modes.spice` | 14 | Mode transitions |
| `tb_top_pvt.spice` | 15 | PVT corners |
| `tb_top_iq.spice` | 16 | Quiescent current |
| `tb_top_retention.spice` | 17 | Retention mode |
| `tb_top_power.spice` | 18 | Power consumption |
| `tb_top_mc.spice` | 19 | 500-run Monte Carlo — full closed-loop PM distribution |
| `tb_top_load_tran_full.spice` | 20 | Full load transient 0→50mA and 50→0mA |
| `tb_top_line_tran.spice` | 21 | Line transient — BVDD step ±500mV |
| `tb_top_avbg_sweep.spice` | 22 | AVBG and IBIAS variation across full stated range |
| `tb_top_en.spice` | 23 | Enable/disable sequence |
| `tb_top_psrr_freq.spice` | 24 | PSRR full Bode 10Hz–10MHz at 3 load points |
| `tb_top_noise.spice` | 25 | Output noise — integrated µVrms on PVDD |
| `tb_top_pm_fine.spice` | 26 | Fine PM sweep — 20+ load points, worst-case corner |
| `tb_top_cload.spice` | 27 | Cload stability — 200pF, 500pF, 1nF, 10nF |
| `tb_top_cold_crank.spice` | 28 | Cold crank system level |
| `tb_top_tc.spice` | 29 | PVDD temperature coefficient |
| `tb_top_ldr_bvdd.spice` | 30 | Load regulation vs BVDD at 3 input voltages |
| `tb_top_avbg_pvt.spice` | 31 | Combined AVBG + PVT corners |
| `tb_top_soa.spice` | 32 | Pass device SOA at system level |

---

### Pass/Fail Criteria

All 32 tests in the Verification Plan must pass. See the table above for individual pass conditions.

**MC test details (Test 19):** Run `.mc 500` on the full closed-loop netlist at TT 27°C, Iload = 1 mA. Vary all device parameters with their mismatch models. For each run, break the loop and measure phase margin. Report: mean PM, sigma, min PM across all runs. Pass condition: mean − 2σ ≥ 45°. A min below 35° in any single run is a hard fail — investigate and widen margin.

**PSRR full sweep (Test 24):** Run `.ac` with BVDD as the source. Sweep 10 Hz to 10 MHz. Run at Iload = 0, 1 mA, and 50 mA separately. Report: PSRR at DC, 1 kHz, 10 kHz, 100 kHz, 1 MHz. Document the −3 dB frequency (where PSRR rolls below 20 dB). This is the key metric for board-level noise rejection.

**Output noise (Test 25):** Run `.noise` with PVDD as the output node. Report integrated noise from 10 Hz to 1 MHz in µVrms. Report spectral density (nV/√Hz) at 1 kHz and 100 kHz. Noise floor is dominated by the feedback divider thermal noise and the error amp input noise.

---

### Deliverables

1. `design.cir` — `.subckt pvdd_regulator bvdd pvdd gnd avbg ibias svdd en en_ret uv_flag ov_flag`
2. All 32 testbench files listed above
3. `results.md` — updated after every test run
4. `README.md` — final design report: complete spec table with simulated values, pass/fail for all 32 tests, design choices summary, known limitations
5. `verification_summary.md` — machine-readable: 32 rows with test name, measured value, spec, pass/fail
6. `README.md` — the visual window to the complete regulator: full spec table with simulated values, pass/fail for all 32 tests, and every plot listed below embedded inline

---

### README: Required Plots

The `README.md` is the visual window to the complete PVDD regulator. It is the first document anyone reads to understand whether the chip works. Every critical waveform and characterization result must be embedded here. A reader who only looks at the README must be able to assess the design without running a single simulation.

**Mechanism:** Testbenches save data with `.wrdata`. Run `python3 plot_all.py` to generate all PNGs. Embed with `![description](filename.png)`.

**Plots required in README.md:**

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `dc_regulation.png` | `tb_top_dc_reg` | VPVDD vs Iload — shows regulation accuracy 0–50mA |
| `load_transient_full.png` | `tb_top_load_tran`, `tb_top_load_tran_full` | PVDD vs time — all 4 steps: 1→10mA, 10→1mA, 0→50mA, 50→0mA |
| `line_transient.png` | `tb_top_line_tran` | PVDD and BVDD vs time — BVDD step ±500mV |
| `bode_all_loads.png` | `tb_top_lstb` | Loop gain and phase at 0, 1, 10, 50mA — overlay showing PM at each load |
| `pm_vs_iload_fine.png` | `tb_top_pm_fine` | PM (°) vs Iload 20+ points, worst-case corner — conditional stability diagnostic |
| `psrr_vs_freq.png` | `tb_top_psrr_freq` | PSRR (dB) vs frequency at Iload=0, 1, 50mA — overlay 10Hz–10MHz |
| `output_noise.png` | `tb_top_noise` | PVDD noise spectral density (nV/√Hz) vs frequency |
| `startup_waveform.png` | `tb_top_startup` | BVDD and PVDD vs time at 1V/µs ramp |
| `cold_crank.png` | `tb_top_cold_crank` | BVDD and PVDD vs time — dip and recovery |
| `mode_transitions.png` | `tb_top_modes` | BVDD, PVDD, and all mode control outputs vs time |
| `mc_pm_histogram.png` | `tb_top_mc` | PM distribution from 500 MC runs — mean, ±2σ lines, 45° spec line |
| `avbg_pvdd_accuracy.png` | `tb_top_avbg_sweep`, `tb_top_avbg_pvt` | VPVDD vs AVBG — shows regulation accuracy across reference variation |
| `pvdd_tc.png` | `tb_top_tc` | VPVDD vs temperature at AVBG=min/nom/max — shows TC and worst-case accuracy |
| `pvt_summary.png` | `tb_top_pvt` | VPVDD at all 15 PVT conditions (heatmap or grouped bar) with spec window |

---

## Absolute Rules

1. **Real Sky130 PDK only.** The top-level netlist contains only `.include` references to block `design.cir` files, which contain only Sky130 PDK device instantiations. No behavioral models anywhere in the hierarchy.
2. **No behavioral models.** The only ideal components allowed are: `V_AVBG` (1.226V), `I_BIAS` (1µA), `V_BVDD`, `V_SVDD`, testbench stimulus sources, and load resistors/capacitors in testbenches.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.** Run all 32 tests. Every number must come from a re-runnable `.spice` testbench.
5. **Push through difficulty.** Top-level integration will expose problems invisible at block level. Fix them in the block designs or integration netlist — do not paper over failures with workarounds.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench must print results in this exact format. The top-level run produces one summary line per test:

```
specs_pass: 18
vpvdd_min_V: 4.971
vpvdd_max_V: 5.031
line_reg_mV_per_V: 0.8
load_reg_mV_per_mA: 0.3
undershoot_mV: 88.0
overshoot_mV: 62.0
pm_min_deg: 51.2
gm_min_dB: 14.8
psrr_dc_dB: 48.1
psrr_10k_dB: 31.4
startup_time_us: 72.3
startup_overshoot_V: 5.21
iout_limit_mA: 67.4
uv_trip_V: 4.28
ov_trip_V: 5.52
iq_active_uA: 212.0
iq_retention_uA: 4.1
pvt_all_pass: 1
```

### The specs.tsc File

`specs.tsc` defines all tracked metrics and pass/fail thresholds.

The **primary metric** is `specs_pass` — number of the 18 system tests that pass. Higher is better. Target: 18. The experiment loop advances when specs_pass increases. Once specs_pass = 18, secondary metric is pm_min_deg (higher is better).

### Summary Printed After Each Run

```
---
specs_pass:       18/18
pm_min_deg:       51.2  deg  (spec >= 45)   PASS
undershoot_mV:    88.0  mV   (spec <= 150)  PASS
iq_active_uA:    212.0  uA   (spec <= 300)  PASS
pvt_all_pass:      1    bool (spec = 1)     PASS
---
ALL 18 TESTS PASS
```

Extract the primary metric:

```bash
grep "^specs_pass:" run.log
```

### Logging Results

Log to `results.tsv` (tab-separated):

```
commit	specs_pass	pm_min_deg	status	description
```

Note: this block uses **two** numeric columns — specs_pass (primary) and pm_min_deg (secondary) — because once all 18 pass the next question is how much margin exists.

Example:

```
commit	specs_pass	pm_min_deg	status	description
a1b2c3d	0	0.0	crash	integration netlist wiring errors
b2c3d4e	12	38.2	discard	startup fails tests 8-9 and PVT test 15
c3d4e5f	16	47.1	keep	all core tests pass PVT and retention failing
d4e5f6g	18	51.2	keep	all 18 tests pass first full-system passing commit
```

**Do not commit `results.tsv`.**

---

## 4. The Experiment Loop

### Branch Setup

```bash
git checkout -b autoresearch/top-integration-$(date +%b%d | tr '[:upper:]' '[:lower:]')
```

### LOOP FOREVER

```
1. Check git state and which tests are still failing
2. Identify the root cause of the first failing test (wiring error? block-level design issue?)
3. Fix: either fix the top-level wiring OR go back to the relevant block directory and fix design.cir there
4. git commit -m "exp: fix test N — <what you changed>"
5. Run: ngspice -b run_all_tests.sh > run.log 2>&1
6. Extract: grep "^specs_pass:\|^pm_min_deg:\|^pvt_all_pass:" run.log
7. If grep empty → crashed. tail -n 50 run.log
8. Log to results.tsv
9. If specs_pass improved (more tests pass) → KEEP
   If specs_pass = 18 and pm_min_deg improved → KEEP
   Else → DISCARD: git reset --hard HEAD~1
10. Go to step 1
```

### Improvement Criterion

**Keep** if `specs_pass` is strictly higher than the previous best.
**Keep** if `specs_pass` = 18 and `pm_min_deg` is strictly higher (more margin = better).
**Discard** if specs_pass decreases or stays the same without pm_min_deg improvement.

### Integration Strategy

Work through failing tests in this order — each tier depends on the previous:

1. **Tests 1, 2, 3** (DC/line/load regulation) — core regulation loop correct
2. **Test 6** (loop stability, all loads) — compensation adequate
3. **Tests 4, 5** (transient) — loop fast enough
4. **Test 7** (PSRR) — supply rejection
5. **Tests 8, 9** (startup) — startup circuit integrated correctly
6. **Tests 10, 11** (dropout, current limit) — HV margin and protection
7. **Tests 12, 13** (UV, OV) — comparators connected correctly
8. **Test 14** (mode transitions) — mode control clean
9. **Test 15** (PVT corners) — all of the above at all corners
10. **Tests 16, 17, 18** (Iq, retention, power) — housekeeping

### Timeout

Full 18-test run including PVT corners (15 conditions) is the longest simulation job in the project. Allow **2 hours** per complete run. Run only tests 1–6 first (30 minutes) until those pass, then add tests 7–14, then add test 15 (PVT).

### Crashes

Top-level convergence failures most commonly come from:
- Floating nets (check all block port connections)
- Supply domain conflicts (wrong supply connected to a block)
- Startup state: all nodes at zero with no `.ic` statements
- Loop gain too high causing DC operating point failure

Fix each methodically. Do not add behavioral workarounds.

### NEVER STOP

Once all 18 tests pass at TT 27°C, the work is not done — PVT test 15 must also pass. Once PVT passes, optimize: increase phase margin, reduce Iq, reduce startup time. Every improvement that simplifies the integration or increases margin is worth finding. The loop runs until the human interrupts you, period.
