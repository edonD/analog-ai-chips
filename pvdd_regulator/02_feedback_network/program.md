# Block 02: Feedback Network — Design Program

---

## 1. Setup

### Purpose

The feedback network is a voltage divider that scales PVDD (5.0V) down to the bandgap reference level (1.226V) for comparison in the error amplifier. The divider ratio directly sets the regulated output voltage:

```
V_PVDD = V_REF / ratio = 1.226V / 0.2452 = 5.0V
```

The feedback network determines output voltage accuracy, temperature coefficient of PVDD, quiescent current from the divider, noise injected at the error amp input, and the bandwidth of the feedback path. Getting the ratio exactly right is critical — every millivolt of error here appears directly on PVDD.

This is a Wave 2 block. It can be designed and tested standalone using an ideal 5V source on PVDD, but must be re-verified in the closed loop with Blocks 00 and 01.

### Read Before Starting

Read these files to understand the full system context before touching any circuit:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues, ideal source values
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `02_feedback_network/specification.json` — this block's pass/fail criteria (numeric, machine-readable)

### Create results.md

Create `02_feedback_network/results.md` before running any simulation. Update it after every simulation run. It must contain:

- **Topology and resistor type chosen** and the reason
- **Results table**: parameter | simulated value | spec limit | pass/fail
- **Simulation log**: what was changed, what improved or degraded
- **Open issues**: anything not yet meeting spec

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance configured for this block only. The instance has:
- Full SkyWater SKY130A PDK installed
- ngspice installed and tested
- This block directory (`02_feedback_network/`) as the working directory

### What You Can Do

You are free to choose any resistor topology and type that meets the specifications. Options to consider:

- **Simple two-resistor divider** — R_TOP ≈ 308 kΩ, R_BOT ≈ 100 kΩ. Standard approach.
- **Unit-resistor ladder** — build both R_TOP and R_BOT from identical unit resistors in series for best process matching and TC cancellation.
- **Trimming taps** — include intermediate taps for post-fabrication output voltage adjustment.

Sky130 resistor types available:
- `sky130_fd_pr__res_xhigh_po` — extra-high R polysilicon (~2 kΩ/sq, low TC). Best choice for high-value resistors in small area.
- `sky130_fd_pr__res_high_po` — medium-R polysilicon.
- `sky130_fd_pr__res_generic_nd` — N-diffusion resistor.
- `sky130_fd_pr__res_generic_pd` — P-diffusion resistor.

Using the same resistor type for both R_TOP and R_BOT cancels TC to first order. Using unit resistors improves matching further.

Modify `design.cir` freely. Add testbench files as needed. Everything in this directory is yours to change.

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria. The evaluator reads it.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md`** — this file defines the design rules.
- **Do not use ideal resistors** (`R value`) for any device in the `design.cir` subcircuit. Only instantiated Sky130 PDK resistor devices are allowed.

### Goal

Meet **all** pass/fail criteria in `specification.json`, verified by real ngspice simulations with Sky130 PDK models. The V_FB value at PVDD = 5.0V must be measured in simulation — PDK resistors have end effects, contact resistance, and non-ideal R/sq values that make the hand-calculated value wrong. Adjust the device sizing until the simulated V_FB is exactly right.

### Simplicity Criterion

All else being equal, simpler is better. A two-resistor divider that meets the ratio and TC specs is better than a complex ladder with trimming taps. Do not add trimming taps unless a simpler approach fails to meet the spec.

---

### Optimization

Use `optimize.py` to find R1/R2 values that minimize VFB temperature coefficient without manual ratio sweeping.

**Framework (scipy):**

```python
from scipy.optimize import differential_evolution, minimize
import subprocess, re

def cost(params):
    # Write R1, R2 into design.cir via .param substitution
    # subprocess.run(['ngspice', '-b', 'run_block.sh'], capture_output=True)
    # Parse vfb_27c_V, vfb_m40c_V, vfb_150c_V from run.log
    # cost = max(|vfb_T - 1.226|) across temperatures + penalty if ratio wrong
    pass

result = differential_evolution(cost, bounds=[(50e3, 500e3), (50e3, 500e3)], maxiter=100, seed=42)
result = minimize(cost, result.x, method='Nelder-Mead', options={'xatol': 100, 'fatol': 1e-4})
```

**Variables:** R1 (top resistor, 50 kΩ–500 kΩ), R2 (bottom resistor, 50 kΩ–500 kΩ).

**Objective:** minimize peak VFB deviation from 1.226V across −40 to 150°C (primary metric = `vfb_tc_max_mV` from run.log).

**Constraints (penalty if violated):**
- VFB = 1.226V ± 5 mV at TT 27°C (ratio R2/(R1+R2) = Vref/Vout = 1.226/5.0)
- Divider current ≤ 1 µA (R1+R2 ≥ 5 MΩ) — or use Sky130 poly resistors with matched TC
- 3σ VFB spread < 10 mV (verified by MC testbench, not optimizer — but optimizer tunes nominal)
- TC < 200 µV/°C integrated −40 to 150°C

**Commit strategy:** commit per-block only. Keep if `vfb_tc_max_mV` decreases and all constraints pass:
```bash
git add pvdd_regulator/02_feedback_network/ && git commit -m "exp(02): <what changed>"
```
Regress → `git checkout pvdd_regulator/02_feedback_network/design.cir`.

---

### Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `pvdd` | Input | 5.0V regulated | Top of divider |
| `vfb` | Output | ~1.226V | Divider midpoint → error amp negative input |
| `gnd` | Supply | 0V | Bottom of divider |

Subcircuit signature: `.subckt feedback_network pvdd vfb gnd`

**Connections in the LDO:**
- `pvdd` ← PVDD output rail (drain of pass device, Block 01)
- `vfb` → error amp inverting input (Block 00)
- The compensation network (Block 03) may also connect at or near the `vfb` node

---

### Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Divider ratio (Vfb/Vpvdd) | 0.2440 | 0.2452 | 0.2465 | — | Sets PVDD = 5.0V ±25 mV from ratio alone |
| Total divider resistance | 350 | 408 | 500 | kΩ | Sets quiescent current |
| Divider current | 10 | 12.3 | 15 | µA | From PVDD to GND |
| Ratio TC (matched) | — | — | 50 | ppm/°C | Near-zero with matched resistor types |
| Noise at vfb (integrated, 1 Hz–1 MHz) | — | — | 50 | µVrms | Thermal noise of divider |
| Parasitic capacitance at vfb | — | — | 2 | pF | From resistor body caps |
| Temperature range | −40 | 27 | 150 | °C | |

---

### Operating Conditions

- **Input:** PVDD = 4.8 to 5.17V
- **Output:** V_FB = ~1.226V at PVDD = 5.0V
- **Corners:** SS/TT/FF/SF/FS at −40°C, 27°C, 150°C

---

### Known Challenges

1. **Ratio accuracy vs. area.** PDK resistors have end effects, contact resistance, and non-ideal R/sq values. Calibrate the ratio in simulation before finalizing sizing — do not trust hand calculations.

2. **Temperature coefficient.** Even with matched resistor types there can be residual TC mismatch. The ratio TC determines how much PVDD drifts with temperature beyond the bandgap TC.

3. **Quiescent current budget.** Lower resistance = higher current = lower noise but worse Iq. Higher resistance = lower current = higher noise and more susceptibility to leakage. Target: 10–15 µA.

4. **Parasitic capacitance at V_FB.** High-value poly resistors have significant body capacitance. This creates a pole at the feedback node that can affect loop stability, especially with high-resistance dividers.

---

### Dependencies

Wave 2 — can be tested standalone. Full verification requires the closed loop with Blocks 00 and 01.

---

### Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| DC divider ratio at PVDD = 5.0V | V_FB value, computed ratio |
| Ratio vs temperature (−40 to 150°C) | Ratio TC in ppm/°C |
| Ratio at process corners | Variation across SS/FF/SF/FS |
| Absolute resistance values | R_TOP and R_BOT individually |
| Noise at V_FB node | Spectral density and integrated noise (1 Hz–1 MHz) |
| Monte Carlo resistor mismatch | VFB distribution over 200 runs — report mean and sigma |

---

### Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| V_FB at PVDD = 5.0V, TT 27°C | 1.226V ± 1 mV (adjust sizing until exact) |
| V_FB variation over −40 to 150°C | < 5 mV |
| V_FB variation across SS/FF | < 10 mV |
| Divider current | 10–15 µA |
| Integrated noise at vfb (1 Hz–1 MHz) | < 50 µVrms |
| VFB MC sigma (200 runs, TT 27°C) | 3σ < 10 mV — keeps PVDD within ±30 mV (0.6%) |
| No model errors | All testbenches run without errors |

---

### Deliverables

1. `design.cir` — `.subckt feedback_network pvdd vfb gnd`
2. `tb_fb_dc_ratio.spice` — DC ratio at PVDD = 5.0V, divider current
3. `tb_fb_temp.spice` — ratio vs temperature, TC
4. `tb_fb_corners.spice` — ratio at SS/FF/SF/FS corners
5. `tb_fb_noise.spice` — noise spectrum and integrated noise at vfb
6. `tb_fb_mc.spice` — 200-run Monte Carlo on R1/R2 mismatch; `.mc 200` with resistor mismatch models; measure VFB at each run; report mean, sigma, min, max
7. `results.md` — updated after every simulation run
8. `README.md` — the visual window to this block: final R values, ratio, and every plot listed below embedded inline

---

### README: Required Plots

The `README.md` is the visual window to this block. The feedback ratio directly sets PVDD accuracy — every reader must see the full distribution of VFB.

**Mechanism:** Testbenches save data with `.wrdata`. Run `python3 plot_all.py` to generate all PNGs. Embed with `![description](filename.png)`.

**Plots required in README.md:**

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `vfb_vs_temp.png` | `tb_fb_temp` | VFB (V) vs temperature −40 to 150°C — shows TC contribution to PVDD error |
| `vfb_corners.png` | `tb_fb_corners` | VFB at all 15 PVT corners (bar chart) with ±1% spec band marked |
| `noise_vfb.png` | `tb_fb_noise` | Noise spectral density at vfb (nV/√Hz) vs frequency |
| `mc_vfb_histogram.png` | `tb_fb_mc` | VFB distribution histogram from 200 MC runs — show mean, ±1σ, ±3σ lines |

---

## Absolute Rules

1. **Real Sky130 PDK only.** Every resistor must be an instantiated Sky130 device. No ideal `R=308k` behavioral elements.
2. **No behavioral models.** Only testbench supply sources and stimulus may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.** The divider ratio must be measured in simulation, not assumed from hand calculation.
5. **Push through difficulty.** Sky130 PDK resistors have non-zero TC and process variation. Characterize them; do not ignore them.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench must print results in this exact format:

```
vfb_error_mV: 0.312
vfb_temp_drift_mV: 2.1
vfb_corner_drift_mV: 6.4
divider_current_uA: 12.3
noise_vfb_uVrms: 31.2
```

`vfb_error_mV` = |V_FB − 1.226| × 1000 at PVDD=5.0V TT 27°C. This is what you are minimizing.

### The specs.tsc File

`specs.tsc` defines all tracked metrics and pass/fail thresholds.

The **primary metric** is `vfb_error_mV` — how far V_FB is from the 1.226V target. Lower is better. The goal is to size the divider so this is as close to zero as possible, while keeping divider current in the 10–15 µA window and ratio TC < 50 ppm/°C.

### Summary Printed After Each Run

```
---
vfb_error_mV:          0.312  mV    (spec <= 1)    PASS
vfb_temp_drift_mV:     2.100  mV    (spec <= 5)    PASS
vfb_corner_drift_mV:   6.400  mV    (spec <= 10)   PASS
divider_current_uA:   12.300  uA    (spec 10-15)   PASS
noise_vfb_uVrms:      31.200  uVrms (spec <= 50)   PASS
specs_pass:            6/6
```

Extract the primary metric:

```bash
grep "^vfb_error_mV:" run.log
```

### Logging Results

Log to `results.tsv` (tab-separated):

```
commit	vfb_error_mV	specs_pass	status	description
```

Example:

```
commit	vfb_error_mV	specs_pass	status	description
a1b2c3d	0.000000	0/6	crash	initial stub
b2c3d4e	8.500000	3/6	discard	hand-calc R values not accurate enough
c3d4e5f	1.200000	5/6	keep	adjusted R_BOT unit count
d4e5f6g	0.312000	6/6	keep	fine-tuned R_TOP by 1 unit segment
```

**Do not commit `results.tsv`.**

---

## 4. The Experiment Loop

### Branch Setup

```bash
git checkout -b autoresearch/feedback-net-$(date +%b%d | tr '[:upper:]' '[:lower:]')
```

### LOOP FOREVER

```
1. Check git state
2. Form one idea (adjust number of unit resistors in R_TOP or R_BOT, try different resistor type)
3. Modify design.cir
4. git commit -m "exp: <what you tried>"
5. Run: ngspice -b run_block.sh > run.log 2>&1
6. Extract: grep "^vfb_error_mV:\|^vfb_temp_drift_mV:\|^divider_current_uA:" run.log
7. If grep empty → crashed. tail -n 50 run.log
8. Log to results.tsv
9. If vfb_error_mV improved (lower) AND specs_pass equal or better → KEEP
   Else → DISCARD: git reset --hard HEAD~1
10. Go to step 1
```

### Improvement Criterion

**Keep** if `vfb_error_mV` is strictly lower and `specs_pass` does not decrease.
**Keep** also if `specs_pass` increases (more specs passing).
**Discard** otherwise.

Once vfb_error_mV < 0.1 mV and all 6 specs pass, try to also minimize divider_current_uA (lower Iq is a bonus) without breaking the ratio.

### Timeout

This block runs fast — typically 2–5 minutes per full run. Timeout at 15 minutes.

### NEVER STOP

If ratio is already perfect, try to reduce TC further by exploring matched unit resistor arrays. Try to reduce noise. Try to reduce total resistor area. Small improvements that simplify the design are always worth finding.
