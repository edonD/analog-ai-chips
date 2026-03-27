# Block 06: Level Shifter — Design Program

---

## 1. Setup

### Purpose

The level shifter translates digital control signals between two voltage domains:

- **SVDD domain (2.2V):** Where digital mode control, enable signals, and configuration bits originate.
- **BVDD/PVDD domain (5–10.5V):** Where the error amplifier, pass device, and protection circuits operate.

Without level shifters, SVDD-domain signals (0/2.2V) cannot reliably drive HV-domain gates, and HV-domain outputs (0/5–10.5V) would overstress SVDD-domain inputs.

Two direction variants are needed:
- **Low-to-high (SVDD → BVDD):** For enable and mode signals going from the digital controller into the HV domain.
- **High-to-low (PVDD → SVDD):** For status flags (UV, OV) coming from the HV domain back to the digital controller.

This is a Wave 1 block — no dependencies on other blocks for standalone design.

### Read Before Starting

Read these files to understand the full system context before touching any circuit:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `06_level_shifter/specification.json` — this block's pass/fail criteria (numeric, machine-readable)

### Create results.md

Create `06_level_shifter/results.md` before running any simulation. Update it after every simulation run. It must contain:

- **Topology chosen** for each direction and the reason
- **Results table**: parameter | simulated value | spec limit | pass/fail
- **Simulation log**: what was changed, what improved or degraded
- **Open issues**: any corner or BVDD value not yet reliable

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance configured for this block only. The instance has:
- Full SkyWater SKY130A PDK installed
- ngspice installed and tested
- This block directory (`06_level_shifter/`) as the working directory

### What You Can Do

You are free to choose any level shifter topology for each direction. They may share a topology or differ:

**Low-to-high (SVDD → BVDD):**
- **Cross-coupled PMOS** — the classic approach. Two HV PMOS cross-coupled from BVDD, two HV NMOS pull-downs driven by SVDD-level inputs. Recommended starting point.
- **Current-mirror level shifter** — more robust at low Vgs but uses more current.
- **Resistor-load level shifter** — simpler but draws static current and is slower.

**High-to-low (PVDD → SVDD):**
- **Voltage-clamped inverter** — HV NMOS input, PMOS load, output clamped to SVDD.
- **Cascode clamp** — stack devices to limit voltage seen by SVDD-domain transistors.
- **Current-mirror approach** — sense current from HV domain, mirror to SVDD domain.

The level shifter must work across the full BVDD range of 5.4–10.5V. At BVDD = 5.4V the PMOS pull-up is weak; at BVDD = 10.5V there may be excessive crowbar current during switching. Verify both extremes.

Protect all SVDD-domain devices (1.8V oxide limit) from seeing more than 1.8V at any terminal.

Modify `design.cir` freely. Add testbench files as needed. Everything in this directory is yours to change.

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria. The evaluator reads it.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md`** — this file defines the design rules.
- **Do not use behavioral level shifters or ideal switches** for any internal device.

### Goal

Meet **all** pass/fail criteria in `specification.json`, verified by real ngspice simulations. Both directions must work reliably from BVDD = 5.4V to 10.5V, at SS 150°C (hardest case: SVDD only provides ~1.3V overdrive on HV NMOS), and with no static crowbar current in either steady state.

### Simplicity Criterion

All else being equal, simpler is better. A classic cross-coupled PMOS shifter (4 transistors) that meets all specs is better than a 10-transistor variant with marginal improvement. If the UV/OV flags and enable signals all have the same requirements, one shared topology is better than two different ones.

---

### Optimization

Use `optimize.py` to find NMOS/PMOS sizing that minimizes worst-case propagation delay at SS 150°C, BVDD = 5.4V without exhaustive manual sweeping.

**Framework (scipy):**

```python
from scipy.optimize import differential_evolution, minimize
import subprocess, re

def cost(params):
    # Write Wn, Wp into design.cir via .param substitution (NMOS pull-down, PMOS cross-coupled)
    # subprocess.run(['ngspice', '-b', 'run_block.sh'], capture_output=True)
    # Parse delay_max_ns from run.log (worst-case corner: SS 150C, BVDD=5.4V)
    # Return delay_max_ns, large penalty if output swing fails or static power > 5uA
    pass

result = differential_evolution(cost, bounds=[(1e-6, 20e-6), (1e-6, 20e-6)], maxiter=100, seed=42)
result = minimize(cost, result.x, method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 0.1})
```

**Variables:** NMOS pull-down width Wn (1–20 µm), PMOS cross-coupled width Wp (1–20 µm).

**Objective:** minimize `delay_max_ns` at worst-case corner (SS 150°C, BVDD = 5.4V) — primary metric from run.log.

**Constraints (penalty if violated):**
- Output HIGH within 0.2V of BVDD (low-to-high) and SVDD (high-to-low) at all corners
- Output LOW < 0.2V at all corners
- Delay < 100 ns at all 15 PVT conditions and BVDD = 5.4V, 7V, 10.5V
- Static power < 5 µA per shifter in both stable states
- No metastable state at any corner

**Commit strategy:** commit per-block only. Keep if `delay_max_ns` strictly decreases and all constraints pass:
```bash
git add pvdd_regulator/06_level_shifter/ && git commit -m "exp(06): <what changed>"
```
Regress → `git checkout pvdd_regulator/06_level_shifter/design.cir`.

---

### Interface

**Low-to-high shifter:**

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `in` | Input | 0/SVDD (2.2V) | Input signal |
| `out` | Output | 0/BVDD | Level-shifted output |
| `bvdd` | Supply | 5.4–10.5V | High-voltage supply |
| `svdd` | Supply | 2.2V | Low-voltage supply |
| `gnd` | Supply | 0V | Ground |

**High-to-low shifter:**

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `in` | Input | 0/PVDD (~5V) | Input signal |
| `out` | Output | 0/SVDD (2.2V) | Level-shifted output |
| `pvdd` | Supply | 5.0V | High-voltage supply |
| `svdd` | Supply | 2.2V | Low-voltage supply |
| `gnd` | Supply | 0V | Ground |

Subcircuit signatures:
- `.subckt level_shifter_up in out bvdd svdd gnd`
- `.subckt level_shifter_down in out pvdd svdd gnd`

**Signals requiring shifting:**

| Signal | Direction | From → To |
|--------|-----------|-----------|
| `en` (enable) | SVDD → BVDD | 0/2.2V → 0/BVDD |
| `mode[1:0]` | SVDD → BVDD | 0/2.2V → 0/BVDD |
| `bypass_en` | SVDD → BVDD | 0/2.2V → 0/BVDD |
| `uv_flag` | PVDD → SVDD | 0/PVDD → 0/2.2V |
| `ov_flag` | PVDD → SVDD | 0/PVDD → 0/2.2V |

---

### Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Output swing (low-to-high) | 0/BVDD | — | — | V | Must reach full BVDD rail |
| Output swing (high-to-low) | 0/SVDD | — | — | V | Must reach full SVDD rail |
| Propagation delay (rising) | — | — | 100 | ns | |
| Propagation delay (falling) | — | — | 100 | ns | |
| BVDD operating range | 5.4 | — | 10.5 | V | Must work across full range |
| Static power per shifter | — | — | 5 | µA | No static current in steady state |
| Temperature range | −40 | 27 | 150 | °C | |

---

### Operating Conditions

- **SVDD:** Fixed 2.2V
- **BVDD:** 5.4 to 10.5V
- **PVDD:** ~5.0V (for high-to-low shifter)
- **Load:** Gate capacitance of downstream logic (~0.5–2 pF)
- **Corners:** SS/TT/FF/SF/FS at −40°C, 27°C, 150°C

---

### Known Challenges

1. **SVDD = 2.2V must drive HV NMOS.** HV NMOS Vth ≈ 0.6–0.9V. At SS 150°C, Vth can approach 0.9V, leaving only ~1.3V overdrive. The pull-down must overcome the cross-coupled PMOS at this worst case.

2. **Wide BVDD range.** At BVDD = 5.4V the PMOS cross-coupled pair is weak. At BVDD = 10.5V there may be excessive crowbar current during switching. Verify both extremes.

3. **1.8V device protection.** Any signal from the BVDD/PVDD domain must be clamped or level-shifted before reaching a 1.8V device gate. Never apply > 1.8V to a standard-device gate or drain.

4. **Static power.** A poorly designed level shifter can have a permanent DC current path through the cross-coupled pair during an intermediate state. Verify zero (or near-zero) static current in both stable states.

---

### Dependencies

Wave 1 — no dependencies on other blocks.

Used by Block 08 (mode control) and Block 10 (top integration).

---

### Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| Logic function | Both shifters, both input states |
| Propagation delay (tpLH, tpHL) | At nominal BVDD and corners |
| Functionality across BVDD range | BVDD = 5.4V, 7V, 10.5V |
| Static power | Current in both stable states |
| PVT corners | Delay and function at SS/FF/SF/FS, −40/27/150°C |
| Output levels | Verify output reaches within 0.2V of both rails |

---

### Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Low-to-high output HIGH | > BVDD − 0.2V |
| Low-to-high output LOW | < 0.2V |
| High-to-low output HIGH | > SVDD − 0.2V |
| High-to-low output LOW | < 0.2V |
| Propagation delay | < 100 ns at all conditions |
| Works at BVDD = 5.4V | Reliable switching |
| Works at BVDD = 10.5V | Reliable switching, no breakdown |
| Static power | < 5 µA per shifter |
| Works at SS 150°C | Reliable switching (worst case) |
| No metastable states | Output always resolves to rail |

---

### Deliverables

1. `design.cir` — both subcircuits: `.subckt level_shifter_up ...` and `.subckt level_shifter_down ...`
2. `tb_ls_logic.spice` — logic function, output levels, metastability check
3. `tb_ls_delay.spice` — propagation delay
4. `tb_ls_bvdd_sweep.spice` — function at BVDD = 5.4V, 7V, 10.5V
5. `tb_ls_power.spice` — static power in both stable states
6. `tb_ls_pvt.spice` — all criteria at all PVT corners
7. `results.md` — updated after every simulation run
8. `README.md` — the visual window to this block: topology, device sizes, and every plot listed below embedded inline

---

### README: Required Plots

The `README.md` is the visual window to this block. Switching waveforms and delay data must be immediately visible.

**Mechanism:** Testbenches save data with `.wrdata`. Run `python3 plot_all.py` to generate all PNGs. Embed with `![description](filename.png)`.

**Plots required in README.md:**

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `switching_waveforms.png` | `tb_ls_logic` | Input and output waveforms for both shifters — low-to-high and high-to-low |
| `delay_vs_bvdd.png` | `tb_ls_bvdd_sweep` | Propagation delay (ns) vs BVDD at 5.4V, 7V, 10.5V |
| `delay_pvt.png` | `tb_ls_pvt` | Delay at all 15 PVT corners (bar chart) — SS 150°C BVDD=5.4V is worst case |

---

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor must be an instantiated Sky130 device. No behavioral level shifters or ideal switches.
2. **No behavioral models.** Only testbench stimulus and supply sources may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** Level shifters across wide voltage ratios (2.2V to 10.5V) are tricky. Iterate.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench must print results in this exact format:

```
delay_max_ns: 38.2
lth_out_high_margin_V: 0.41
lth_out_low_V: 0.08
htl_out_high_margin_V: 0.35
htl_out_low_V: 0.06
static_power_uA: 0.3
works_bvdd_min: 1
works_bvdd_max: 1
works_ss_150c: 1
no_metastable: 1
```

`delay_max_ns` = max propagation delay across both edges and both directions at the worst-case corner (SS 150°C, BVDD = 5.4V).

### The specs.tsc File

`specs.tsc` defines all tracked metrics and pass/fail thresholds.

The **primary metric** is `delay_max_ns` — worst-case propagation delay. Lower is better. The experiment loop advances when this strictly decreases while all reliability checks remain passing.

### Summary Printed After Each Run

```
---
delay_max_ns:              38.2  ns   (spec <= 100)  PASS
lth_out_high_margin_V:      0.41 V    (spec >= 0.2)  PASS
htl_out_high_margin_V:      0.35 V    (spec >= 0.2)  PASS
static_power_uA:             0.3 uA   (spec <= 5)    PASS
works_bvdd_min:              1   bool  (spec = 1)     PASS
works_ss_150c:               1   bool  (spec = 1)     PASS
specs_pass:                 10/10
```

Extract the primary metric:

```bash
grep "^delay_max_ns:" run.log
```

### Logging Results

Log to `results.tsv` (tab-separated):

```
commit	delay_max_ns	specs_pass	status	description
```

Example:

```
commit	delay_max_ns	specs_pass	status	description
a1b2c3d	0.000000	0/10	crash	initial stub
b2c3d4e	0.000000	0/10	crash	cross-coupled PMOS does not switch at BVDD=5.4V SS
c3d4e5f	82.300000	9/10	discard	works but metastable at one corner
d4e5f6g	38.200000	10/10	keep	wider NMOS pull-down fixes SS 150C switching
```

**Do not commit `results.tsv`.**

---

## 4. The Experiment Loop

### Branch Setup

```bash
git checkout -b autoresearch/level-shifter-$(date +%b%d | tr '[:upper:]' '[:lower:]')
```

### LOOP FOREVER

```
1. Check git state
2. Form one idea (widen NMOS pull-down, adjust PMOS cross-coupled sizing, try different topology)
3. Modify design.cir
4. git commit -m "exp: <what you tried>"
5. Run: ngspice -b run_block.sh > run.log 2>&1
6. Extract: grep "^delay_max_ns:\|^works_bvdd_min:\|^works_ss_150c:\|^static_power_uA:" run.log
7. If grep empty → crashed. tail -n 50 run.log
8. Log to results.tsv
9. If delay_max_ns improved AND works_bvdd_min=1 AND works_ss_150c=1 AND no_metastable=1 → KEEP
   Else → DISCARD: git reset --hard HEAD~1
10. Go to step 1
```

### Improvement Criterion

**Keep** if `delay_max_ns` is strictly lower AND all boolean reliability checks (works_bvdd_min, works_bvdd_max, works_ss_150c, no_metastable) remain 1 AND `specs_pass` does not decrease.
**Discard** otherwise. A faster shifter that fails at any corner is useless.

### Timeout

Level shifter simulations are fast — 5–10 minutes for a full run. Timeout at 20 minutes.

### NEVER STOP

Once all specs pass, try to reduce static_power_uA further. Try fewer transistors — a simpler shifter that meets spec is always better. If both low-to-high and high-to-low can use the same topology with different parameters, unify them into one parameterized subcircuit — that is a simplification win.
