# Block 05: UV/OV Comparators — Design Program

---

## 1. Setup

### Purpose

The UV (undervoltage) and OV (overvoltage) comparators continuously monitor the PVDD output and flag abnormal conditions:

- **UV comparator:** Asserts `uv_flag` when PVDD drops below ~4.3V. This triggers mode transitions and system resets in the mode control logic (Block 08).
- **OV comparator:** Asserts `ov_flag` when PVDD rises above ~5.5V. This flags overshoot conditions that could damage downstream circuits.

Both comparators need hysteresis to prevent chattering when PVDD hovers near a threshold. They must operate with low power (< 5 µA each) because they are always on — even during retention mode and low-BVDD conditions.

This is a Wave 1 block — no dependencies on other blocks for standalone design and testing.

### Read Before Starting

Read these files to understand the full system context before touching any circuit:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `05_uv_ov_comparators/specification.json` — this block's pass/fail criteria (numeric, machine-readable)

### Create results.md

Create `05_uv_ov_comparators/results.md` before running any simulation. Update it after every simulation run. It must contain:

- **Topology chosen** for each comparator and the reason
- **Results table**: parameter | simulated value | spec limit | pass/fail
- **Simulation log**: what was changed, what improved or degraded
- **Open issues**: any threshold or corner not yet in spec

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance configured for this block only. The instance has:
- Full SkyWater SKY130A PDK installed
- ngspice installed and tested
- This block directory (`05_uv_ov_comparators/`) as the working directory

### What You Can Do

You are free to choose any comparator topology for each of the UV and OV comparators. They may use the same topology or different ones if requirements warrant:

- **Differential pair with cross-coupled loads** — classic comparator with built-in hysteresis from positive feedback.
- **Schmitt trigger** — CMOS inverter-based threshold detector with feedback resistor for hysteresis. Very simple.
- **Two-stage comparator** — differential pair followed by a gain stage for sharper switching.
- **Current-mode comparator** — threshold set by current comparison. Very compact.
- **Any other topology** that meets the power, accuracy, and hysteresis requirements.

**Threshold generation:** The threshold is set by comparing a PVDD-derived signal to V_REF (1.226V). You may use a resistive divider from PVDD compared to V_REF, scaled current mirrors, or any other approach.

**Hysteresis:** Must produce 50–150 mV at the PVDD level. Too little = chattering. Too much = late detection.

**Supply consideration:** The UV comparator must detect PVDD as low as 4.0V. If the comparator runs from PVDD, its supply may be marginal at this voltage. Consider running from BVDD instead, or verify operation down to 4.0V.

Modify `design.cir` freely. Add testbench files as needed. Everything in this directory is yours to change.

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria. The evaluator reads it.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md`** — this file defines the design rules.
- **Do not use behavioral comparators, Verilog-A thresholds, or ideal switches** for any internal device.

### Goal

Meet **all** pass/fail criteria in `specification.json`, verified by real ngspice simulations with Sky130 PDK models. Both comparators must meet their threshold windows across all PVT corners and all temperatures. The power limit (< 5 µA per comparator) and response time (< 5 µs) must both be met simultaneously.

### Simplicity Criterion

All else being equal, simpler is better. A Schmitt trigger that meets the spec is better than a two-stage comparator that adds complexity without improving performance. Both UV and OV comparators can share the same topology if one design meets both sets of requirements — do not build two different circuits when one will do.

---

### Optimization

Use `optimize.py` to find resistor divider values that center UV and OV thresholds with minimum PVT spread and maximum hysteresis margin.

**Framework (scipy):**

```python
from scipy.optimize import differential_evolution, minimize
import subprocess, re

def cost(params):
    # Write Ruv_top, Ruv_bot, Rov_top, Rov_bot into design.cir via .param substitution
    # subprocess.run(['ngspice', '-b', 'run_block.sh'], capture_output=True)
    # Parse uv_threshold_V, ov_threshold_V, hysteresis_mV from run.log
    # cost = (uv_err**2 + ov_err**2) + pvt_spread_penalty + hysteresis_penalty
    pass

result = differential_evolution(cost, bounds=[(10e3, 1e6)]*4, maxiter=150, seed=42)
result = minimize(cost, result.x, method='Nelder-Mead', options={'xatol': 100, 'fatol': 1e-4})
```

**Variables:** UV divider (Ruv_top, Ruv_bot), OV divider (Rov_top, Rov_bot); each 10 kΩ–1 MΩ.

**Objective:** minimize |UV_threshold − 4.5V| + |OV_threshold − 5.5V| at TT 27°C (centering within spec band).

**Constraints (penalty if violated):**
- UV trip point 4.3–4.7V at all 15 PVT corners
- OV trip point 5.3–5.7V at all 15 PVT corners
- Hysteresis 50–200 mV (both comparators)
- Propagation delay < 2 µs
- 3σ MC spread < 50 mV per threshold
- Static current per comparator < 5 µA

**Commit strategy:** commit per-block only. Keep if threshold accuracy improves and all constraints pass:
```bash
git add pvdd_regulator/05_uv_ov_comparators/ && git commit -m "exp(05): <what changed>"
```
Regress → `git checkout pvdd_regulator/05_uv_ov_comparators/design.cir`.

---

### Interface

**UV comparator:**

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `pvdd` | Input (sense) | 0–6V | PVDD output being monitored |
| `vref` | Input | 1.226V | Bandgap reference for threshold generation |
| `uv_flag` | Output | Digital (0/vdd_comp) | HIGH when PVDD < UV threshold |
| `vdd_comp` | Supply | PVDD or BVDD | Comparator supply |
| `gnd` | Supply | 0V | Ground |
| `en` | Input | Digital | Enable signal |

**OV comparator:**

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `pvdd` | Input (sense) | 0–6V | PVDD output being monitored |
| `vref` | Input | 1.226V | Bandgap reference for threshold generation |
| `ov_flag` | Output | Digital (0/vdd_comp) | HIGH when PVDD > OV threshold |
| `vdd_comp` | Supply | PVDD or BVDD | Comparator supply |
| `gnd` | Supply | 0V | Ground |
| `en` | Input | Digital | Enable signal |

Subcircuit signatures:
- `.subckt uv_comparator pvdd vref uv_flag vdd_comp gnd en`
- `.subckt ov_comparator pvdd vref ov_flag vdd_comp gnd en`

**Connections in the LDO:**
- `pvdd` ← PVDD output rail
- `vref` ← ideal V_AVBG (1.226V)
- `uv_flag`, `ov_flag` → mode control logic (Block 08), optionally level-shifted (Block 06) to SVDD domain

---

### Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| UV threshold (falling) | 4.0 | 4.3 | 4.5 | V | PVDD level at which UV asserts |
| UV hysteresis | 50 | 100 | 150 | mV | UV de-asserts at threshold + hysteresis |
| OV threshold (rising) | 5.25 | 5.5 | 5.7 | V | PVDD level at which OV asserts |
| OV hysteresis | 50 | 100 | 150 | mV | OV de-asserts at threshold − hysteresis |
| Response time (UV) | — | — | 5 | µs | From threshold crossing to flag change |
| Response time (OV) | — | — | 5 | µs | From threshold crossing to flag change |
| Power per comparator | — | — | 5 | µA | Quiescent current from supply |
| Output levels | 0 / vdd_comp | — | — | V | Rail-to-rail digital output |
| Threshold accuracy over PVT | — | — | ±10 | % | From nominal |
| Temperature range | −40 | 27 | 150 | °C | |

---

### Operating Conditions

- **PVDD range:** 0 to ~6V (monitoring the full output range including overshoot).
- **Supply:** PVDD or BVDD — designer choice (UV must work when PVDD is low).
- **Corners:** SS/TT/FF/SF/FS at −40°C, 27°C, 150°C.

---

### Known Challenges

1. **UV comparator supply chicken-and-egg.** The UV comparator must detect when PVDD is low (~4.0V), but if it runs from PVDD its own supply may be insufficient. Consider running from BVDD, or verify operation is correct down to 4.0V supply.

2. **Threshold accuracy over temperature.** The threshold is set by V_REF (1.226V) and a resistive divider. The divider ratio TC and comparator input offset both contribute to threshold error across −40 to 150°C.

3. **Hysteresis calibration.** Too little hysteresis = chattering when PVDD is near the threshold. Too much = late detection of actual fault conditions.

4. **Low power and fast response are in tension.** 5 µA per comparator limits gm and slows the comparator. The < 5 µs response time must still be met at this bias level.

---

### Dependencies

Wave 1 — no dependencies on other blocks.

In top integration (Block 10), UV/OV flags connect to mode control logic (Block 08) and may be level-shifted (Block 06) to the SVDD domain.

---

### Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| UV trip point (falling and rising) | Exact threshold and hysteresis |
| OV trip point (rising and falling) | Exact threshold and hysteresis |
| Response time | From threshold crossing to flag transition |
| Power consumption | Quiescent current per comparator |
| PVT corners | Thresholds at SS/FF/SF/FS, −40/27/150°C |
| Output levels | Verify rail-to-rail digital output |
| Monte Carlo offset distribution | 200 runs each — UV and OV threshold sigma from transistor mismatch |

---

### Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| UV threshold (falling) at TT 27°C | 4.0V to 4.5V |
| UV hysteresis | 50 mV to 150 mV |
| OV threshold (rising) at TT 27°C | 5.25V to 5.7V |
| OV hysteresis | 50 mV to 150 mV |
| UV threshold across all PVT | Within 4.0–4.5V range |
| OV threshold across all PVT | Within 5.25–5.7V range |
| Response time (both) | < 5 µs |
| Power per comparator | < 5 µA |
| Output swings rail-to-rail | Yes |
| No oscillation at threshold | Clean switching with hysteresis |
| UV threshold MC sigma (200 runs) | 3σ < 50 mV — threshold stays inside 4.0–4.5V window |
| OV threshold MC sigma (200 runs) | 3σ < 50 mV — threshold stays inside 5.25–5.7V window |

---

### Deliverables

1. `design.cir` — both subcircuits: `.subckt uv_comparator ...` and `.subckt ov_comparator ...`
2. `tb_uv_trip.spice` — UV threshold and hysteresis
3. `tb_ov_trip.spice` — OV threshold and hysteresis
4. `tb_comp_response.spice` — response time for both
5. `tb_comp_power.spice` — quiescent current per comparator
6. `tb_comp_output_swing.spice` — rail-to-rail output verification
7. `tb_comp_pvt.spice` — threshold variation at all PVT corners
8. `tb_uvov_mc.spice` — 200-run Monte Carlo on both comparators; measure UV and OV trip thresholds per run; report mean, sigma, min, max for each; pass if 3σ band fits within allowed window
9. `results.md` — updated after every simulation run
10. `README.md` — the visual window to this block: threshold values, hysteresis, and every plot listed below embedded inline

---

### README: Required Plots

The `README.md` is the visual window to this block. Threshold accuracy and hysteresis behavior must be immediately visible.

**Mechanism:** Testbenches save data with `.wrdata`. Run `python3 plot_all.py` to generate all PNGs. Embed with `![description](filename.png)`.

**Plots required in README.md:**

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `uv_trip_hysteresis.png` | `tb_uv_trip` | UV flag vs PVDD — rising and falling sweep showing hysteresis loop |
| `ov_trip_hysteresis.png` | `tb_ov_trip` | OV flag vs PVDD — same for OV |
| `response_time.png` | `tb_comp_response` | Input voltage and flag output vs time — shows propagation delay |
| `uv_pvt_threshold.png` | `tb_comp_pvt` | UV threshold at all 15 PVT corners (bar) with spec window |
| `ov_pvt_threshold.png` | `tb_comp_pvt` | OV threshold at all 15 PVT corners (bar) with spec window |
| `mc_uv_histogram.png` | `tb_uvov_mc` | UV threshold distribution from 200 MC runs |
| `mc_ov_histogram.png` | `tb_uvov_mc` | OV threshold distribution from 200 MC runs |

---

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device. No behavioral comparators or Verilog-A thresholds.
2. **No behavioral models.** Only testbench stimulus and supply sources may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** Hysteresis and threshold accuracy require careful sizing across PVT. Iterate.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench must print results in this exact format:

```
threshold_error_mV: 45.0
uv_thresh_falling_V: 4.255
uv_hysteresis_mV: 87.0
ov_thresh_rising_V: 5.545
ov_hysteresis_mV: 92.0
response_time_us: 2.1
power_per_comp_uA: 3.8
uv_pvt_in_window: 1
ov_pvt_in_window: 1
```

`threshold_error_mV` = max(|UV_actual − 4.3|, |OV_actual − 5.5|) × 1000. This is what you are minimizing.

### The specs.tsc File

`specs.tsc` defines all tracked metrics and pass/fail thresholds.

The **primary metric** is `threshold_error_mV` — the maximum absolute threshold deviation from nominal. Lower is better. The experiment loop advances when this strictly decreases.

### Summary Printed After Each Run

```
---
threshold_error_mV:   45.0  mV   (spec <= 200)  PASS
uv_thresh_falling_V:  4.255 V    (spec 4.0-4.5) PASS
ov_thresh_rising_V:   5.545 V    (spec 5.25-5.7)PASS
uv_hysteresis_mV:     87.0  mV   (spec 50-150)  PASS
ov_hysteresis_mV:     92.0  mV   (spec 50-150)  PASS
response_time_us:      2.1  us   (spec <= 5)    PASS
power_per_comp_uA:     3.8  uA   (spec <= 5)    PASS
specs_pass:           13/13
```

Extract the primary metric:

```bash
grep "^threshold_error_mV:" run.log
```

### Logging Results

Log to `results.tsv` (tab-separated):

```
commit	threshold_error_mV	specs_pass	status	description
```

Example:

```
commit	threshold_error_mV	specs_pass	status	description
a1b2c3d	0.000000	0/13	crash	initial stub
b2c3d4e	320.000000	7/13	discard	divider ratio wrong UV out of window at PVT
c3d4e5f	87.000000	13/13	keep	diff pair with cross-coupled load TT passes
d4e5f6g	45.000000	13/13	keep	tuned divider ratio reduces threshold error
```

**Do not commit `results.tsv`.**

---

## 4. The Experiment Loop

### Branch Setup

```bash
git checkout -b autoresearch/uvov-$(date +%b%d | tr '[:upper:]' '[:lower:]')
```

### LOOP FOREVER

```
1. Check git state
2. Form one idea (adjust divider ratio, adjust hysteresis element, change bias current)
3. Modify design.cir
4. git commit -m "exp: <what you tried>"
5. Run: ngspice -b run_block.sh > run.log 2>&1
6. Extract: grep "^threshold_error_mV:\|^uv_thresh_falling_V:\|^ov_thresh_rising_V:\|^power_per_comp_uA:" run.log
7. If grep empty → crashed. tail -n 50 run.log
8. Log to results.tsv
9. If threshold_error_mV improved AND specs_pass equal or better → KEEP
   Else → DISCARD: git reset --hard HEAD~1
10. Go to step 1
```

### Improvement Criterion

**Keep** if `threshold_error_mV` is strictly lower and `specs_pass` does not decrease and both thresholds remain within their windows across all PVT corners.
**Discard** otherwise.

### Timeout

15 minutes per full run (comparators simulate quickly). PVT sweep adds time — run TT first, add corners once TT passes.

### NEVER STOP

Once thresholds are accurate and all specs pass, try to reduce `power_per_comp_uA` further — less always-on current is better. Try to simplify the hysteresis mechanism. If both UV and OV use the same topology, verify they truly share the same circuit — one subcircuit parameterized by threshold is cleaner than two separate circuits.
