# Block 08: Mode Control — Design Program

---

## 1. Setup

### Purpose

The mode control manages the PVDD regulator's operating mode based on the BVDD input voltage. It implements five operating modes with clean, glitch-free transitions:

| # | Mode | BVDD Range | PVDD Output | Max Load |
|---|------|-----------|-------------|----------|
| 1 | POR | 0 – 2.5V | OFF | — |
| 2 | Retention bypass | 2.5 – 4.2V | BVDD | 0.5 mA |
| 3 | Retention regulate | 4.2 – 4.5V | 4.1V | 0.5 mA |
| 4 | Power-up bypass | 4.5 – 5.0V | BVDD | 10 mA |
| 5 | Active regulate | > 5.6V | 5.0V | 50 mA |

Mode transitions are triggered by BVDD crossing voltage thresholds. The mode control generates output signals that configure the rest of the LDO: `bypass_en`, `ea_en`, `ref_sel`, `uvov_en`, `ilim_en`. These signals must change atomically — race conditions that cause glitches on these outputs can produce PVDD spikes or dips.

This is a Wave 3 block. It requires Block 06 (level shifter) for translating SVDD-domain enable signals into the BVDD domain.

### Read Before Starting

Read these files to understand the full system context before touching any circuit:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues (especially #m3: PVDD oscillation during mode transitions)
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `08_mode_control/specification.json` — this block's pass/fail criteria (numeric, machine-readable)
- `06_level_shifter/results.md` — level shifter interface for domain crossing

### Create results.md

Create `08_mode_control/results.md` before running any simulation. Update it after every simulation run. It must contain:

- **Implementation approach chosen** (threshold detection, logic, bypass switch) and the reason
- **Threshold table**: comparator | nominal threshold | simulated value | pass/fail
- **Results table**: parameter | simulated value | spec limit | pass/fail
- **Simulation log**: what was changed, what improved or degraded
- **Open issues**: any threshold or transition not yet meeting spec

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance configured for this block only. The instance has:
- Full SkyWater SKY130A PDK installed
- ngspice installed and tested
- This block directory (`08_mode_control/`) as the working directory
- Block 06 `design.cir` available via `.include`

### What You Can Do

The truth table (five modes, four thresholds) is fixed. The implementation is entirely up to you:

**Threshold detection:**
- Four independent comparators, each with its own resistive divider comparing to V_REF.
- A single resistor ladder with multiple tap points feeding multiple comparators (saves area and ensures monotonicity).
- Current-mode threshold detection.
- Window comparator structures that inherently produce monotonic outputs.

**Logic implementation:**
- CMOS gates built from HV devices.
- Pass-transistor logic.
- Simple SR latches with comparator outputs.
- Current-steering logic (lower power).

**Bypass switch (for bypass modes):**
- Large NMOS pulling the pass device gate to GND.
- Transmission gate.
- Direct connection through the mode control output.

**Key constraint:** Four thresholds must form a strict monotonic sequence. If threshold tolerances overlap between adjacent comparators, the mode state machine can enter an invalid state. A shared resistor ladder with matched taps inherently prevents this problem.

Modify `design.cir` freely. Add testbench files as needed. Everything in this directory is yours to change.

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria. The evaluator reads it.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md`** — this file defines the design rules.
- **Do not use behavioral state machines, Verilog models, or ideal switches** for any internal device. No Verilog-A, no `switch` elements, no behavioral gates.

### Goal

Meet **all** pass/fail criteria in `specification.json`, verified by real ngspice simulations. All four thresholds must be correct, all outputs must be glitch-free during transitions, and the system must work at ramp rates from 0.1 V/µs to 12 V/µs. The silicon known issue #m3 (PVDD oscillation after mode transitions) is a direct consequence of glitchy mode control outputs — design for clean transitions from the start.

### Simplicity Criterion

All else being equal, simpler is better. A single resistor ladder feeding four comparators is simpler than four independent dividers — use the ladder. SR latches for hysteresis are simpler than cross-coupled comparators — use the latches if they work. Build incrementally: get one comparator working perfectly before adding the next.

---

### Optimization

Use `optimize.py` to find resistor ladder values that minimize threshold TC variation and maximize monotonicity margin across PVT.

**Framework (scipy):**

```python
from scipy.optimize import differential_evolution, minimize
import subprocess, re

def cost(params):
    # Write R1..R5 ladder values into design.cir via .param substitution
    # subprocess.run(['ngspice', '-b', 'run_block.sh'], capture_output=True)
    # Parse th1_V..th4_V at TT/SS/FF 27C/150C/-40C from run.log
    # cost = sum of threshold TC errors + monotonicity_inversion_penalty
    pass

result = differential_evolution(cost, bounds=[(10e3, 500e3)]*5, maxiter=150, seed=42)
result = minimize(cost, result.x, method='Nelder-Mead', options={'xatol': 100, 'fatol': 1e-4})
```

**Variables:** R1–R5 resistor ladder values (10 kΩ–500 kΩ each), setting the four BVDD comparator trip points.

**Objective:** minimize maximum threshold deviation from nominal across −40 to 150°C (minimizes TC drift of all four thresholds simultaneously).

**Constraints (penalty if violated):**
- Threshold ordering th1 < th2 < th3 < th4 maintained at all 15 PVT corners (monotonicity)
- th1 (POR exit) = 2.5V ± 5%
- th2 (retention/regulate boundary) = 4.2V ± 5%
- th3 (bypass/regulate handoff) = 4.5V ± 5%
- th4 (active regulate entry) = 5.6V ± 5%
- Static current through ladder < 10 µA at BVDD = 5.4V
- 200-run MC: zero threshold ordering inversions

**Commit strategy:** commit per-block only. Keep if threshold TC deviation decreases and monotonicity holds at all corners:
```bash
git add pvdd_regulator/08_mode_control/ && git commit -m "exp(08): <what changed>"
```
Regress → `git checkout pvdd_regulator/08_mode_control/design.cir`.

---

### Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Input (sense) | 0–10.5V | Battery supply being monitored |
| `pvdd` | Supply | 5.0V (when available) | Regulated supply |
| `svdd` | Supply | 2.2V | Low-voltage digital supply |
| `gnd` | Supply | 0V | Ground |
| `vref` | Input | 1.226V | Bandgap reference |
| `en_ret` | Input | SVDD domain | Retention mode enable |
| `bypass_en` | Output | BVDD domain | Pass device bypass control |
| `ea_en` | Output | PVDD domain | Error amplifier enable |
| `ref_sel` | Output | PVDD domain | Reference select (0=5.0V target, 1=4.1V target) |
| `uvov_en` | Output | PVDD domain | UV/OV comparator enable |
| `ilim_en` | Output | PVDD domain | Current limiter enable |
| `pass_off` | Output | BVDD domain | Pass device hard shutoff — drives HV gate pull-up to BVDD during POR |

Subcircuit signature: `.subckt mode_control bvdd pvdd svdd gnd vref en_ret bypass_en ea_en ref_sel uvov_en ilim_en pass_off`

**Note on `pass_off` architecture:** The error amplifier (Block 00) runs from PVDD (5V) and cannot drive the pass device gate above 5V. At BVDD = 10.5V, the PMOS gate must reach ≥ 9.7V to turn the device fully off (Vgs ≈ 0). This is unreachable from a 5V supply. The `pass_off` signal must therefore drive a dedicated BVDD-domain HV switch — a large NMOS (sky130_fd_pr__nfet_g5v0d10v5) pulling the gate node to BVDD — that operates independently of the error amp. This switch is active during POR (BVDD < 2.5V entry threshold) to ensure the pass device is off before the regulator loop is active.

---

### Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| BVDD threshold: POR → ret bypass | 2.3 | 2.5 | 2.7 | V | Hysteresis: 200 mV |
| BVDD threshold: ret bypass → ret reg | 4.0 | 4.2 | 4.4 | V | Hysteresis: 200 mV |
| BVDD threshold: ret reg → PU bypass | 4.3 | 4.5 | 4.7 | V | Hysteresis: 200 mV |
| BVDD threshold: PU bypass → active | 5.4 | 5.6 | 5.8 | V | Hysteresis: 200 mV |
| Comparator response time | — | — | 5 | µs | Per threshold |
| Glitch-free transitions | Yes | — | — | — | No glitches during mode changes |
| Quiescent current (active mode) | — | — | 20 | µA | From BVDD |
| BVDD ramp rate tolerance | 0.1 | — | 12 | V/µs | Slow and fast ramps |
| Temperature range | −40 | 27 | 150 | °C | |

---

### Operating Conditions

- **BVDD:** Ramps from 0 to 10.5V (power-up) and back to 0 (power-down).
- **Ramp rates:** 0.1 V/µs to 12 V/µs.
- **Temperature:** −40°C to 150°C.
- **Corners:** SS/TT/FF/SF/FS.

---

### Known Challenges

1. **Monotonic threshold sequence.** Four thresholds must form a strict sequence. Process variation can shift adjacent comparators into overlap. A shared resistor ladder with matched taps is the best defense.

2. **Self-powering at low BVDD.** At BVDD < 2.5V (POR mode), the mode control has no established supply. It must either operate from BVDD directly using HV devices, or use a minimal bootstrap.

3. **Glitch-free transitions.** When a threshold is crossed, all output signals must change atomically. Race conditions between comparators or logic gates can produce glitches that cause PVDD spikes or dips (known issue #m3 in silicon).

4. **Hysteresis accuracy.** Each comparator needs ~200 mV hysteresis at the BVDD level. Too little = chattering on slow ramps. Too much = delayed mode transitions.

5. **Power budget.** Four dividers + four comparators + logic. Must stay under 20 µA total from BVDD.

---

### Dependencies

Wave 3 — requires:
- Block 06 (`06_level_shifter/design.cir`) — for domain crossing of enable signals

Can be partially designed and tested standalone (comparators and logic). Full integration requires Block 06 and the downstream block enable interfaces.

---

### Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| Full mode transition sequence | BVDD ramp 0 → 10.5V, monitor all outputs |
| Fast ramp (12 V/µs) | Clean transitions, no glitches |
| Slow ramp (0.1 V/µs) | Clean transitions, no chattering |
| Power-down (reverse) | BVDD 10.5V → 0, verify reverse transitions with hysteresis |
| Individual thresholds | Each comparator trip point at TT 27°C |
| Hysteresis | Up/down thresholds for each comparator |
| PVT corners | Thresholds at SS/FF/SF/FS, −40/27/150°C |
| Glitch detection | Monitor all outputs for spurious transitions |
| Monte Carlo threshold monotonicity | 200 runs — verify all 4 thresholds maintain strict ordering in every run |

---

### Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| POR threshold | 2.5V ± 0.2V |
| Retention threshold | 4.2V ± 0.2V |
| Power-up threshold | 4.5V ± 0.2V |
| Active threshold | 5.6V ± 0.2V |
| Hysteresis (all comparators) | 150–250 mV |
| Monotonic thermometer code | No out-of-order assertions |
| Glitch-free outputs | No intermediate states on any output |
| Works at 12 V/µs ramp | Clean transitions |
| Works at 0.1 V/µs ramp | Clean transitions, no chattering |
| Thresholds across PVT | Within ±15% of nominal |
| Quiescent current (active) | < 20 µA from BVDD |
| Power-down reverse transitions | Correct with hysteresis |
| MC monotonicity (200 runs) | Zero inversions in all 200 runs — TH1 < TH2 < TH3 < TH4 must hold in every run |

**Monotonicity note:** A shared resistor ladder guarantees ratio accuracy between taps but mismatch in the comparator input pairs can shift apparent thresholds. MC catches the tail cases where comparator offset flips adjacent thresholds.

---

### Deliverables

1. `design.cir` — `.subckt mode_control bvdd pvdd svdd gnd vref en_ret bypass_en ea_en ref_sel uvov_en ilim_en pass_off`
2. `tb_mc_ramp_normal.spice` — full mode sequence, 1 V/µs ramp
3. `tb_mc_fast_ramp.spice` — 12 V/µs ramp
4. `tb_mc_slow_ramp.spice` — 0.1 V/µs ramp
5. `tb_mc_power_down.spice` — power-down reverse transitions
6. `tb_mc_hysteresis.spice` — up/down thresholds for each comparator
7. `tb_mc_iq.spice` — quiescent current in active mode
8. `tb_mc_pvt.spice` — all thresholds at all PVT corners
9. `tb_mc_monotonic.spice` — 200-run Monte Carlo; measure all 4 trip thresholds per run; report ordering violations; pass condition: zero inversions in 200 runs
10. `results.md` — updated after every simulation run
11. `README.md` — the visual window to this block: threshold table, state machine diagram, and every plot listed below embedded inline

---

### README: Required Plots

The `README.md` is the visual window to this block. The mode transition timing diagram is the single most important waveform in this block — it must appear first and be easy to read.

**Mechanism:** Testbenches save data with `.wrdata`. Run `python3 plot_all.py` to generate all PNGs. Embed with `![description](filename.png)`.

**Plots required in README.md:**

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `mode_transition_full.png` | `tb_mc_ramp_normal` | BVDD + all output signals vs time — the full state machine timing diagram at 1V/µs |
| `mode_transition_fast.png` | `tb_mc_fast_ramp` | Same at 12V/µs — verify clean transitions on fast automotive ramp |
| `threshold_pvt.png` | `tb_mc_pvt` | All 4 thresholds at all 15 PVT corners (grouped bar) with ±15% spec lines |
| `mc_monotonicity.png` | `tb_mc_monotonic` | All 4 threshold values per MC run (scatter, 200 runs) — visually confirms no inversions |

---

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor, resistor, and comparator must be an instantiated Sky130 device. No behavioral state machines, no Verilog models.
2. **No behavioral models.** Only testbench stimulus and supply sources may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** Analog state machines with multiple thresholds and hysteresis are complex. Build incrementally and test each comparator before combining.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench must print results in this exact format:

```
thresh_max_error_pct: 4.2
thresh_por_V: 2.51
thresh_ret_V: 4.19
thresh_pup_V: 4.48
thresh_act_V: 5.58
hysteresis_min_mV: 183.0
hysteresis_max_mV: 217.0
monotonic: 1
glitch_free: 1
works_fast_ramp: 1
works_slow_ramp: 1
iq_active_uA: 14.2
```

`thresh_max_error_pct` = max over all 4 thresholds of |actual − nominal| / nominal × 100. Nominals: 2.5V, 4.2V, 4.5V, 5.6V.

### The specs.tsc File

`specs.tsc` defines all tracked metrics and pass/fail thresholds.

The **primary metric** is `thresh_max_error_pct` — worst threshold deviation across all PVT conditions. Lower is better. The experiment loop advances when this strictly decreases.

### Summary Printed After Each Run

```
---
thresh_max_error_pct:  4.2  %     (spec <= 15)   PASS
monotonic:             1    bool  (spec = 1)      PASS
glitch_free:           1    bool  (spec = 1)      PASS
works_fast_ramp:       1    bool  (spec = 1)      PASS
works_slow_ramp:       1    bool  (spec = 1)      PASS
iq_active_uA:         14.2  uA   (spec <= 20)    PASS
specs_pass:           16/16
```

Extract the primary metric:

```bash
grep "^thresh_max_error_pct:" run.log
```

### Logging Results

Log to `results.tsv` (tab-separated):

```
commit	thresh_max_error_pct	specs_pass	status	description
```

Example:

```
commit	thresh_max_error_pct	specs_pass	status	description
a1b2c3d	0.000000	0/16	crash	initial stub
b2c3d4e	18.500000	12/16	discard	independent dividers thresholds overlap at PVT
c3d4e5f	7.800000	14/16	keep	shared resistor ladder eliminates overlap
d4e5f6g	4.200000	16/16	keep	tuned ladder ratios reduces PVT error
```

**Do not commit `results.tsv`.**

---

## 4. The Experiment Loop

### Branch Setup

```bash
git checkout -b autoresearch/mode-ctrl-$(date +%b%d | tr '[:upper:]' '[:lower:]')
```

### LOOP FOREVER

```
1. Check git state
2. Form one idea (adjust ladder ratios, tune comparator bias, fix glitch in transition logic)
3. Modify design.cir
4. git commit -m "exp: <what you tried>"
5. Run: ngspice -b run_block.sh > run.log 2>&1
6. Extract: grep "^thresh_max_error_pct:\|^monotonic:\|^glitch_free:\|^works_fast_ramp:" run.log
7. If grep empty → crashed. tail -n 50 run.log
8. Log to results.tsv
9. If thresh_max_error_pct improved AND monotonic=1 AND glitch_free=1 AND specs_pass equal or better → KEEP
   Else → DISCARD: git reset --hard HEAD~1
10. Go to step 1
```

### Improvement Criterion

**Keep** if `thresh_max_error_pct` is strictly lower AND monotonic=1 AND glitch_free=1 AND `specs_pass` does not decrease.
**Discard** otherwise. Monotonicity and glitch-free transitions are non-negotiable — they directly cause silicon known issue #m3.

### Timeout

Mode control simulations with slow/fast ramps take 20–30 minutes for the full suite. Allow **45 minutes** per run. Run only the TT ramp test first (2 minutes), add PVT after.

### Crashes

If the output oscillates during a ramp (PVDD chatters), the hysteresis is insufficient or there is a race condition. Increase hysteresis first. If still chattering, review the logic for metastability between comparators.

### NEVER STOP

Once all 16 specs pass, try to reduce iq_active_uA. Try to simplify the resistor ladder (fewer taps). Try to simplify the logic. A simpler state machine with the same threshold accuracy and glitch-free transitions is always the better design.
