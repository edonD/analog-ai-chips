# Block 03: Compensation Network — Design Program

---

## 1. Setup

### Purpose

The compensation network ensures the PVDD LDO feedback loop is stable across all operating conditions. This is the hardest block in the entire design. The fundamental difficulty is that the LDO output pole moves by a factor of 1000× as load current varies from 0 mA to 50 mA:

| Load Current | Effective Rload | Output Pole |
|-------------|----------------|-------------|
| 0 mA | ~∞ | < 1 kHz |
| 100 µA | 50 kΩ | ~16 kHz |
| 1 mA | 5 kΩ | ~160 kHz |
| 10 mA | 500 Ω | ~1.6 MHz |
| 50 mA | 100 Ω | ~8 MHz |

A compensation scheme that stabilizes at one load point may be completely unstable at another. The compensation must achieve PM > 45° and GM > 10 dB simultaneously at **all** load points, all PVT corners, and all temperatures.

This is a Wave 2 block. It requires all of Blocks 00, 01, and 02 to be complete before it can be properly designed — the compensation is meaningless without the full loop.

### Read Before Starting

Read these files to understand the full system context before touching any circuit:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `03_compensation/specification.json` — this block's pass/fail criteria (numeric, machine-readable)
- `00_error_amp/results.md` — error amp Rout, UGB, topology (sets the gate pole)
- `01_pass_device/results.md` — Cgs value (dominant load), gm (sets output pole gain)
- `02_feedback_network/results.md` — feedback node capacitance

### Create results.md

Create `03_compensation/results.md` before running any simulation. Update it after every simulation run. It must contain:

- **Topology chosen** and the reason for choosing it
- **Component values table**: all compensation element values
- **PM table**: phase margin at each load point (0 / 100µA / 1mA / 10mA / 50mA)
- **Simulation log**: what was changed, what improved or degraded
- **Open issues**: any load point or corner where PM < 45°

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance configured for this block only. The instance has:
- Full SkyWater SKY130A PDK installed
- ngspice installed and tested
- This block directory (`03_compensation/`) as the working directory
- Block 00, 01, and 02 `design.cir` files available via `.include`

### What You Can Do

You are free to choose any compensation strategy. Do not limit yourself to Miller compensation — it is one option among many. The topology that achieves PM > 45° across the full 0–50 mA load range is the right topology:

- **Miller compensation** (Cc from gate to output) — classic pole-splitting. Add Rz in series for a left-half-plane zero. Simple but may not stabilize at all loads.
- **Miller with nulling resistor** — Rz to place a zero that tracks the non-dominant pole.
- **Dominant-pole at gate** — large cap at error amp output to make the gate pole absolutely dominant. Simple but kills bandwidth.
- **Adaptive biasing** — sense load current and increase error amp bias at high loads. Moves the gate pole out to track the output pole. This is how the best capless LDOs work.
- **Feed-forward capacitor** — from vfb to vout_gate for phase lead.
- **Cascode compensation** — separate the Miller cap feedback path through a cascode node.
- **Nested Miller** — if using a two-stage error amp.
- **Any other approach** that works.

The full loop for AC simulation includes: Block 00 (error amp) + Block 01 (pass device) + Block 02 (feedback divider) + 200 pF Cload + your compensation network.

Modify `design.cir` freely. Add testbench files as needed. Everything in this directory is yours to change.

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria. The evaluator reads it.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md`** — this file defines the design rules.
- **Do not use ideal capacitors or resistors** in `design.cir`. Every compensation element must be an instantiated Sky130 PDK device (`sky130_fd_pr__cap_mim_m3_1`, `sky130_fd_pr__res_xhigh_po`, etc.).

### Goal

Meet **all** pass/fail criteria in `specification.json`, verified by real ngspice simulations with Sky130 PDK models. Every load point must be tested. Every claimed PM value must come from a `.spice` testbench that anyone can re-run.

If **any single condition fails**, the compensation is not done. Iterate.

### Simplicity Criterion

All else being equal, simpler is better. A one-cap Miller compensation that achieves PM > 45° at all loads beats a complex multi-element network that barely passes. If you find yourself adding a third or fourth compensation element, ask whether the underlying topology choice is wrong. Conversely, if removing a compensation element and replacing it with a simpler alternative gives the same or better PM, that is a win.

---

### Optimization

Use `optimize.py` to find the Cc/Rz combination that maximizes worst-case PM over all load currents without manual sweeping.

**Framework (scipy):**

```python
from scipy.optimize import differential_evolution, minimize
import subprocess, re

def cost(params):
    # Write Cc, Rz into design.cir via .param substitution
    # subprocess.run(['ngspice', '-b', 'run_block.sh'], capture_output=True)
    # Parse pm_min_deg (minimum PM across all 20 load sweep points) from run.log
    # Return -pm_min_deg, large penalty if pm_min_deg < 45 at any corner or Iload
    pass

result = differential_evolution(cost, bounds=[(1e-12, 50e-12), (0, 5000)], maxiter=150, seed=42)
result = minimize(cost, result.x, method='Nelder-Mead', options={'xatol': 1e-13, 'fatol': 0.1})
```

**Variables:** Cc (Miller capacitor, 1–50 pF), Rz (zero resistor, 0–5 kΩ).

**Objective:** maximize minimum PM across all 20 Iload sweep points at worst-case corner SS 150°C (primary metric = `pm_min_deg` from run.log).

**Constraints (penalty if violated):**
- PM ≥ 45° at every Iload from 0 to 50 mA (fine sweep, 20+ points)
- PM ≥ 45° at all 15 PVT corners
- GBW ≤ 10 MHz (prevent interaction with error amp poles)
- PVDD load step undershoot < 200 mV (checked via `tb_comp_load_step.spice`)
- MC distribution: mean − 2σ ≥ 45° (checked separately, not in optimizer loop)

**Commit strategy:** commit per-block only. Keep if `pm_min_deg` strictly increases and all constraints pass:
```bash
git add pvdd_regulator/03_compensation/ && git commit -m "exp(03): <what changed>"
```
Regress → `git checkout pvdd_regulator/03_compensation/design.cir`.

---

### Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `vout_gate` | Connection | 0 to ~PVDD | Error amp output / pass device gate node |
| `pvdd` | Connection | 5.0V | PVDD output node |
| `gnd` | Supply | 0V | Ground |
| `vfb` | Connection (optional) | ~1.226V | Feedback node (if lead compensation is used) |

Subcircuit signature: `.subckt compensation vout_gate pvdd gnd` (add `vfb` pin if needed)

**Connections in the LDO:**
- Sits between Block 00 (error amp output) and Block 01 (pass device gate)
- May also connect to Block 02 (vfb node) if lead compensation is used

---

### Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Phase margin (all loads) | 45 | 55 | — | deg | At Iload = 0, 0.1, 1, 10, 50 mA |
| Gain margin (all loads) | 10 | 15 | — | dB | At all load points |
| Phase margin (all corners) | 45 | — | — | deg | SS, FF, SF, FS at 27°C |
| Phase margin (all temps) | 45 | — | — | deg | −40°C, 27°C, 150°C at TT |
| Unity-gain bandwidth | 100 | 300 | 1000 | kHz | At nominal load (10 mA) |
| DC loop gain | 40 | 60 | — | dB | For load/line regulation |
| Settling time (load step) | — | — | 10 | µs | 1mA to 10mA step, settle to 1% |
| Compensation cap area | — | — | 50000 | µm² | Keep area reasonable |

---

### Operating Conditions

- **Full loop:** Block 00 + Block 01 + Block 02 + 200 pF Cload + compensation
- **Load range:** Rload from ~100 Ω (50 mA) to open circuit (no load)
- **BVDD:** 5.4 to 10.5V
- **Corners:** SS/TT/FF/SF/FS at −40°C, 27°C, 150°C

---

### Known Challenges

1. **Output pole moves 1000×.** At no-load the output pole is at ~1 kHz. At 50 mA it is at ~8 MHz. Any fixed compensation must handle this entire range simultaneously.

2. **No ESR zero.** This is an internal-cap-only LDO (200 pF on-chip, no external cap). There is no ESR zero from an external capacitor to help stabilize the loop.

3. **Worst-case is often light load.** At no-load the output pole is slowest, nearest the crossover frequency. But mid-load can also be problematic if the two poles collide near UGB.

4. **Area budget.** A 50 pF MIM cap is ~25,000 µm². Keep total compensation area under 50,000 µm².

5. **Transient vs. AC.** A design with 45° PM in AC may still ring in transient if poles move during the transient. Verify with both AC and transient simulations.

---

### Dependencies

Wave 2 — requires ALL of:
- Block 00 (`00_error_amp/design.cir`) — must exist and simulate
- Block 01 (`01_pass_device/design.cir`) — must exist with characterized Cgs and gm
- Block 02 (`02_feedback_network/design.cir`) — must exist with correct ratio

---

### Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| Loop gain and phase margin (LSTB) | PM and GM at each load point |
| PM vs load current sweep | Parametric: Iload = 0, 0.1, 1, 10, 50 mA |
| PM at all PVT corners | 5 corners × 3 temperatures = 15 conditions minimum |
| PM vs BVDD | Sweep BVDD 5.4 to 10.5V |
| Load step transient | 1mA→10mA and 10mA→1mA, 1µs edge |
| Full Bode plot | Open-loop gain and phase for visualization |
| Monte Carlo PM distribution | 500 runs at Iload = 1 mA, TT 27°C — report mean PM, sigma, worst case |
| Fine PM sweep (conditional stability check) | PM at 20+ load points: 0, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50 mA — verify no dip below threshold at any intermediate load |
| Capacitive load stability | PM at Cload = 200 pF (nominal), 500 pF, 1 nF, 10 nF — board bypass caps must not cause oscillation |

**Loop breaking:** Use a large inductor (1 GH) in series at the feedback node to break the DC loop while passing AC. Any valid loop-breaking technique is acceptable.

---

### Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Phase margin at Iload = 0 mA | ≥ 45° |
| Phase margin at Iload = 100 µA | ≥ 45° |
| Phase margin at Iload = 1 mA | ≥ 45° |
| Phase margin at Iload = 10 mA | ≥ 45° |
| Phase margin at Iload = 50 mA | ≥ 45° |
| Gain margin at ALL loads | ≥ 10 dB |
| PM at SS/FF/SF/FS, all loads | ≥ 45° |
| PM at −40°C and 150°C, all loads | ≥ 45° |
| Load transient undershoot (1→10 mA) | < 150 mV |
| Load transient overshoot (10→1 mA) | < 150 mV |
| Settling time | < 10 µs to within 1% |
| No oscillation at any condition | Zero sustained ringing in any transient |
| MC PM (500 runs): mean − 2σ | ≥ 45° — design must have margin above the deterministic pass condition |
| Fine PM sweep — no dip below 45° | PM ≥ 45° at every one of the 20+ load points; no conditional stability |
| Cload = 500 pF | PM ≥ 30° (reduced spec — must not oscillate) |
| Cload = 1 nF | PM ≥ 20° or ringing < 3 cycles in transient — document safe limit |
| Cload = 10 nF | Document behavior — hard fail if any oscillation |

**If any single condition fails, the compensation is not done. Iterate.**

---

### Deliverables

1. `design.cir` — `.subckt compensation vout_gate pvdd gnd` (add `vfb` if needed)
2. `tb_comp_lstb.spice` — loop gain, PM, GM at each load point
3. `tb_comp_pm_vs_load.spice` — parametric PM sweep over Iload
4. `tb_comp_pvt.spice` — PM at all corners and temperatures
5. `tb_comp_bvdd_sweep.spice` — PM vs BVDD
6. `tb_comp_load_step.spice` — load step transient
7. `tb_comp_mc.spice` — 500-run Monte Carlo; `.mc 500`; measure loop PM at Iload = 1 mA for each run; report mean, sigma, min; pass if mean − 2σ ≥ 45°
8. `tb_comp_pm_fine.spice` — PM at 20+ evenly-spaced Iload values from 0 to 50 mA using `.step` parametric; plot PM vs Iload; catch any dip (conditional stability) not visible at the 5 standard points
9. `tb_comp_cload.spice` — PM at Cload = 200 pF, 500 pF, 1 nF, 10 nF; use `.param cload=200p` with `.step`; report PM at each; document maximum safe external capacitance
10. `results.md` — updated after every simulation run
11. `README.md` — the visual window to this block: topology, component values, and every plot listed below embedded inline

---

### README: Required Plots

The `README.md` is the visual window to this block. Stability is the most critical system property — every reader must see the full PM picture across load, corners, and mismatch.

**Mechanism:** Testbenches save data with `.wrdata`. Run `python3 plot_all.py` to generate all PNGs. Embed with `![description](filename.png)`.

**Plots required in README.md:**

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `bode_all_loads.png` | `tb_comp_lstb` | Loop gain (dB) and phase (°) vs frequency — overlay at Iload=0/1/10/50mA |
| `pm_vs_iload_fine.png` | `tb_comp_pm_fine` | PM (°) vs Iload — 20+ points 0→50mA — the key conditional stability diagnostic |
| `pm_pvt_heatmap.png` | `tb_comp_pvt` | PM at all 15 PVT conditions (5 corners × 3 temps) as heatmap or grouped bar |
| `load_step_transient.png` | `tb_comp_load_step` | PVDD vs time for 1→10mA and 10→1mA steps |
| `mc_pm_histogram.png` | `tb_comp_mc` | PM distribution from 500 MC runs — show mean, mean−2σ line, spec line at 45° |
| `pm_vs_cload.png` | `tb_comp_cload` | PM vs external Cload — marks safe region and danger zone |

---

## Absolute Rules

1. **Real Sky130 PDK only.** Every capacitor and resistor in the compensation network must be an instantiated Sky130 device. No ideal capacitors or resistors.
2. **No behavioral models.** Only testbench stimulus sources and load elements may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.** Phase margin must be measured from AC simulation, not estimated from hand analysis.
5. **Push through difficulty.** This is the hardest block. The output pole moves 1000× with load. You will iterate many times. Do not give up.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench must print results in this exact format:

```
pm_min_deg: 47.2
pm_0mA_deg: 47.2
pm_100uA_deg: 53.1
pm_1mA_deg: 61.4
pm_10mA_deg: 68.3
pm_50mA_deg: 72.1
gm_min_dB: 14.2
transient_undershoot_mV: 88.0
transient_overshoot_mV: 61.0
settling_time_us: 4.2
no_oscillation: 1
pm_pvt_min_deg: 46.1
```

`pm_min_deg` = minimum of all phase margin values across all load points and all PVT corners. This is the headline number.

### The specs.tsc File

`specs.tsc` defines all tracked metrics and pass/fail thresholds.

The **primary metric** is `pm_min_deg` — the worst-case phase margin across the entire load range and all PVT conditions. Higher is better. The experiment loop advances the branch when pm_min_deg strictly increases.

### Summary Printed After Each Run

```
---
pm_min_deg:              47.2  deg  (spec >= 45)   PASS
pm_0mA_deg:              47.2  deg  (spec >= 45)   PASS
pm_50mA_deg:             72.1  deg  (spec >= 45)   PASS
gm_min_dB:               14.2  dB   (spec >= 10)   PASS
transient_undershoot_mV: 88.0  mV   (spec <= 150)  PASS
settling_time_us:         4.2  us   (spec <= 10)   PASS
specs_pass:              12/12
```

Extract the primary metric:

```bash
grep "^pm_min_deg:" run.log
```

### Logging Results

Log to `results.tsv` (tab-separated):

```
commit	pm_min_deg	specs_pass	status	description
```

Example:

```
commit	pm_min_deg	specs_pass	status	description
a1b2c3d	0.000000	0/12	crash	no compensation element yet
b2c3d4e	22.300000	4/12	discard	bare Miller cap 10pF not enough
c3d4e5f	47.200000	12/12	keep	Miller 20pF + Rz 5k passes all loads
d4e5f6g	51.800000	12/12	keep	increased Rz to 8k improves no-load PM
```

**Do not commit `results.tsv`.**

---

## 4. The Experiment Loop

### Branch Setup

```bash
git checkout -b autoresearch/compensation-$(date +%b%d | tr '[:upper:]' '[:lower:]')
```

### LOOP FOREVER

```
1. Check git state
2. Form one idea (change Cc value, change Rz, add feed-forward cap, try adaptive biasing)
3. Modify design.cir
4. git commit -m "exp: <what you tried>"
5. Run: ngspice -b run_block.sh > run.log 2>&1
6. Extract: grep "^pm_min_deg:\|^pm_0mA_deg:\|^pm_50mA_deg:\|^gm_min_dB:\|^no_oscillation:" run.log
7. If grep empty → crashed. tail -n 50 run.log
8. Log to results.tsv
9. If pm_min_deg improved AND specs_pass equal or better → KEEP
   Else → DISCARD: git reset --hard HEAD~1
10. Go to step 1
```

### Improvement Criterion

**Keep** if `pm_min_deg` is strictly higher and `specs_pass` does not decrease.
**Keep** also if `specs_pass` increases (especially if no-load PM was the failing condition — getting that to pass is major progress).
**Discard** otherwise.

The hardest condition is no-load (pm_0mA_deg). If that is failing and everything else passes, focus all experiments on improving it — that is the binding constraint.

### Timeout

This block runs the most simulations (15+ conditions for the full PVT sweep). Allow **45 minutes** per full run. For initial topology exploration, run only TT 27°C first (5 minutes), then add PVT sweep only once TT passes.

### Crashes

Phase margin simulations can fail to converge near the unity-gain frequency. Add `.option` `reltol=1e-5` and increase the AC simulation frequency resolution. If the loop simulation itself diverges, check that the loop-breaking inductor (1 GH) is placed correctly.

### NEVER STOP

If all specs pass and pm_min_deg > 55°, try to reduce compensation capacitor area without losing PM margin. Smaller cap = smaller die area = simplification win. Or try removing a compensation element entirely to see if the circuit still passes — that is the ultimate simplification win.
