# Block 07: Zener Clamp — Design Program

---

## 1. Setup

### Purpose

The Zener clamp protects the PVDD output from voltage transients and overshoot conditions. In an automotive environment, events such as load dump (BVDD spike), fast BVDD ramps, and inductive switching can cause PVDD to overshoot beyond 5.5V. The clamp limits the maximum PVDD voltage by shunting excess current to ground when the voltage exceeds the clamp threshold.

This block is purely passive — it draws zero current under normal conditions (PVDD < clamp threshold) and activates only during overvoltage events. It sits in parallel with the load capacitor and feedback divider, connected directly to the PVDD output rail.

**Sky130 has no true Zener diode.** You must build the clamp entirely from available PDK devices. This requires creative circuit design.

This is a Wave 3 block. It can be designed in parallel with other blocks — it has no circuit-level dependencies. When integrated (Block 10), verify that clamp leakage does not affect regulation.

### Read Before Starting

Read these files to understand the full system context before touching any circuit:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `07_zener_clamp/specification.json` — this block's pass/fail criteria (numeric, machine-readable)

### Create results.md

Create `07_zener_clamp/results.md` before running any simulation. Update it after every simulation run. It must contain:

- **Approach chosen** (diode stack, MOSFET clamp, hybrid, etc.) and the reason
- **Results table**: parameter | simulated value | spec limit | pass/fail
- **Simulation log**: what was changed, what improved or degraded
- **Open issues**: any temperature or corner where the clamp threshold is out of range

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance configured for this block only. The instance has:
- Full SkyWater SKY130A PDK installed
- ngspice installed and tested
- This block directory (`07_zener_clamp/`) as the working directory

### What You Can Do

You are free to choose any clamping approach. Sky130 has no Zener — you must find a way. Options to consider:

- **Forward-biased diode stack.** Stack N junctions in series using `sky130_fd_pr__diode_pw2nd_05v5` or `sky130_fd_pr__diode_pd2nw_05v5`. Clamp voltage = N × Vf (~0.65V each at 27°C). Simple and predictable, but has severe TC problems: ~−2 mV/°C per junction × N junctions × 190°C temperature range. Characterize this carefully.

- **Diode-connected MOSFET stack.** Stack diode-connected HV MOSFETs. Each drops Vth (~0.7–0.9V). TC of Vth is ~−1 mV/°C, better than PN junction TC. Fewer devices needed.

- **MOSFET voltage clamp.** An NMOS with gate biased by a resistive divider from PVDD. When PVDD exceeds the divider threshold + Vth, the MOSFET turns on and shunts current. Tunable threshold, sharper turn-on, better TC. But draws static current through the divider — must stay < 1 µA at PVDD = 5.0V.

- **Reverse-biased diode (avalanche).** Use PDK diodes in reverse bias near breakdown. Must characterize actual breakdown voltage in simulation — it may or may not be at a useful level.

- **Hybrid approach.** Combine a MOSFET active clamp for precision with a diode stack for fast transient response.

- **TC compensation.** Mix device types with opposite TC to stabilize the clamp voltage over temperature.

The most difficult constraint is the −40 to 150°C temperature range. Any approach with a large TC will either drag down normal PVDD at 150°C (too low) or fail to protect at −40°C (too high). Characterize the TC of your chosen approach thoroughly before calling it done.

Modify `design.cir` freely. Add testbench files as needed. Everything in this directory is yours to change.

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria. The evaluator reads it.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md`** — this file defines the design rules.
- **Do not use ideal Zener diode models or behavioral clamp sources** for any internal device.

### Goal

Meet **all** pass/fail criteria in `specification.json`, verified by real ngspice simulations. The clamp must work across the full −40 to 150°C range without dragging down normal PVDD (leakage < 1 µA at 5.0V, clamp onset > 5.0V at 150°C) and without being too slow to protect against fast transients.

### Simplicity Criterion

All else being equal, simpler is better. A plain diode stack that meets all specs (including temperature) is better than a complex hybrid that barely meets them. If you can solve the TC problem with an extra device rather than a completely different topology, do that. Removing a device and maintaining the same clamping behavior is a win.

---

### Optimization

Use `optimize.py` to sweep device count and TC compensation sizing to minimize leakage while keeping clamp onset > 5.0V at 150°C.

**Framework (scipy):**

```python
from scipy.optimize import differential_evolution, minimize
import subprocess, re

def cost(params):
    # Write N_diodes (or N_mosfets), Wcomp (TC compensation device width) into design.cir
    # subprocess.run(['ngspice', '-b', 'run_block.sh'], capture_output=True)
    # Parse leakage_at_5v_nA, clamp_onset_150c_V from run.log
    # Return leakage_at_5v_nA, large penalty if clamp_onset_150c_V < 5.0 or onset_27c outside 5.5-6.2V
    pass

result = differential_evolution(cost, bounds=[(3, 12), (1e-6, 20e-6)], maxiter=100, seed=42)
result = minimize(cost, result.x, method='Nelder-Mead', options={'xatol': 0.5, 'fatol': 1})
```

**Variables:** number of stack devices N (3–12, integer), TC compensation device width Wcomp (1–20 µm, if hybrid approach).

**Objective:** minimize `leakage_at_5v_nA` — lowest leakage at normal PVDD while keeping clamp onset within window (primary metric from run.log).

**Constraints (penalty if violated):**
- Clamp onset 5.5–6.2V at TT 27°C (at 1 mA)
- Clamp onset > 5.0V at 150°C (must not drag down PVDD)
- Clamp onset < 7.0V at −40°C (must still provide protection)
- Leakage at PVDD = 5.17V < 5 µA
- Clamp voltage at 10 mA < 6.5V
- Transient peak < 6.5V at 10 V/µs ramp

**Note:** N_diodes is an integer — `differential_evolution` will find near-integer values; round before writing to design.cir.

**Commit strategy:** commit per-block only. Keep if `leakage_at_5v_nA` strictly decreases and `clamp_onset_150c_V` ≥ 5.0V:
```bash
git add pvdd_regulator/07_zener_clamp/ && git commit -m "exp(07): <what changed>"
```
Regress → `git checkout pvdd_regulator/07_zener_clamp/design.cir`.

---

### Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `pvdd` | Input/Output | 5–6V | PVDD output node being clamped |
| `gnd` | Supply | 0V | Ground (clamp current sink) |

Subcircuit signature: `.subckt zener_clamp pvdd gnd`

**Connections in the LDO:**
- Sits in parallel with the 200 pF Cload and the feedback divider
- Passive — draws zero current under normal conditions (PVDD < clamp threshold)
- No enable signal — always active

---

### Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Clamp voltage (onset, 1 mA) | 5.5 | 5.8 | 6.2 | V | At TT 27°C |
| Clamp voltage at 10 mA | — | 6.0 | 6.5 | V | At TT 27°C |
| Leakage at PVDD = 5.0V | — | — | 1 | µA | TT 27°C |
| Leakage at PVDD = 5.17V | — | — | 5 | µA | TT 27°C |
| Peak current capability | 100 | — | — | mA | During transient pulse, not DC |
| Clamp impedance above threshold | — | — | 50 | Ω | Low impedance for effective clamping |
| Clamp onset at 150°C | > 5.0 | — | — | V | Must not drag down normal PVDD |
| Clamp onset at −40°C | — | — | 7.0 | V | Must still provide protection |
| Temperature range | −40 | 27 | 150 | °C | |

---

### Operating Conditions

- **Normal operation:** PVDD = 4.8 to 5.17V. Clamp draws < 1 µA.
- **Overshoot event:** PVDD exceeds 5.5V. Clamp activates and shunts current.
- **Transient pulse:** Fast voltage ramp (up to 10V/µs) on PVDD through low impedance.
- **Corners:** SS/TT/FF/SF/FS at −40°C, 27°C, 150°C.

---

### Known Challenges

1. **Sky130 has no true Zener.** There are no dedicated Zener or avalanche diode devices. Build from PN junction diodes, MOSFETs, or combinations.

2. **Temperature coefficient of diode stacks.** Vf ≈ −2 mV/°C per junction. A 9-diode stack (9 × 0.65V = 5.85V at 27°C) shifts by 9 × 2 mV × 190°C = 3.4V over the temperature range. At 150°C the clamp drops to ~2.45V — completely unusable. This is a fundamental problem requiring a different approach or TC compensation.

3. **Leakage at normal PVDD.** The clamp must not draw significant current at PVDD = 5.0V or 5.17V. The clamp voltage must stay safely above the normal operating range even at 150°C.

4. **Clamp vs. LDO loop interaction.** During an OV event, if the clamp activates while the LDO loop is regulating, the clamp's low impedance appears in parallel with the load. Verify that the clamp does not cause oscillation.

5. **Breakdown voltage uncertainty.** The `05v5` suffix on Sky130 diodes refers to the maximum rated voltage, not the breakdown voltage. Characterize actual breakdown in simulation.

---

### Dependencies

Wave 3 — no circuit-level dependencies.

When integrated (Block 10), verify clamp leakage does not affect regulation and clamp activation does not cause loop oscillation.

---

### Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| DC I–V characteristic | Full I–V curve from 0 to 7V |
| Clamp voltage at 1 mA and 10 mA | Onset and clamping voltages at TT 27°C |
| Leakage at PVDD = 5.0V and 5.17V | Current draw at normal operating voltage |
| Temperature sweep | I–V curve at −40°C, 27°C, 85°C, 150°C |
| Transient clamping | Peak voltage during fast ramp (10V/µs) |
| Process corners | Clamp voltage at SS/FF/SF/FS |

---

### Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Clamp onset at TT 27°C | 5.5V to 6.2V (at 1 mA) |
| Clamp voltage at 10 mA, TT 27°C | < 6.5V |
| Leakage at PVDD = 5.0V, TT 27°C | < 1 µA |
| Leakage at PVDD = 5.17V, TT 27°C | < 5 µA |
| Clamp onset at 150°C | > 5.0V |
| Clamp onset at −40°C | < 7.0V |
| Transient peak (10V/µs ramp) | < 6.5V with 200 pF Cload |
| Peak current at 7V | > 100 mA (pulse rating) |

---

### Deliverables

1. `design.cir` — `.subckt zener_clamp pvdd gnd`
2. `tb_zc_iv.spice` — DC I–V curve, clamp onset, leakage
3. `tb_zc_temp.spice` — I–V at −40°C, 27°C, 85°C, 150°C
4. `tb_zc_transient.spice` — transient clamping during fast ramp
5. `tb_zc_corners.spice` — clamp voltage at all process corners
6. `results.md` — updated after every simulation run
7. `README.md` — the visual window to this block: topology, device stack count, and every plot listed below embedded inline

---

### README: Required Plots

The `README.md` is the visual window to this block. The I–V characteristic and temperature behavior of the clamp must be visible at a glance.

**Mechanism:** Testbenches save data with `.wrdata`. Run `python3 plot_all.py` to generate all PNGs. Embed with `![description](filename.png)`.

**Plots required in README.md:**

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `iv_characteristic.png` | `tb_zc_iv` | Iclamp vs VPVDD — leakage region, onset knee, and clamping region |
| `iv_vs_temperature.png` | `tb_zc_temp` | I–V curves overlaid at −40°C, 27°C, 85°C, 150°C — shows TC of clamp voltage |
| `transient_clamping.png` | `tb_zc_transient` | VPVDD vs time during a 10V/µs ramp — shows clamp activating and peak voltage |

---

## Absolute Rules

1. **Real Sky130 PDK only.** Every diode and transistor must be an instantiated Sky130 device. No ideal Zener diodes or behavioral clamp models.
2. **No behavioral models.** Only testbench stimulus and supply sources may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** Sky130 does not have true Zener diodes. You must build the clamp from available devices. This requires creative circuit design — iterate until it works.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench must print results in this exact format:

```
leakage_at_5v_nA: 12.4
clamp_onset_1mA_V: 5.82
clamp_at_10mA_V: 6.01
leakage_at_5p17v_nA: 48.0
clamp_onset_150c_V: 5.21
clamp_onset_m40c_V: 6.44
transient_peak_V: 6.18
peak_current_mA: 145.0
```

`leakage_at_5v_nA` = clamp current at PVDD = 5.0V in nanoamps. This must stay below 1000 nA (1 µA).

### The specs.tsc File

`specs.tsc` defines all tracked metrics and pass/fail thresholds.

The **primary metric** is `leakage_at_5v_nA` — leakage at normal PVDD. Lower is better. Minimize this while keeping the clamp onset above 5.5V at TT and above 5.0V at 150°C.

### Summary Printed After Each Run

```
---
leakage_at_5v_nA:      12.4  nA   (spec <= 1000)  PASS
clamp_onset_1mA_V:      5.82 V    (spec 5.5-6.2)  PASS
clamp_at_10mA_V:        6.01 V    (spec <= 6.5)   PASS
clamp_onset_150c_V:     5.21 V    (spec >= 5.0)   PASS
clamp_onset_m40c_V:     6.44 V    (spec <= 7.0)   PASS
transient_peak_V:       6.18 V    (spec <= 6.5)   PASS
specs_pass:             9/9
```

Extract the primary metric:

```bash
grep "^leakage_at_5v_nA:" run.log
```

### Logging Results

Log to `results.tsv` (tab-separated):

```
commit	leakage_at_5v_nA	specs_pass	status	description
```

Example:

```
commit	leakage_at_5v_nA	specs_pass	status	description
a1b2c3d	0.000000	0/9	crash	initial stub
b2c3d4e	0.000000	2/9	discard	9-diode stack 150C clamp drops to 4.8V fails
c3d4e5f	250.000000	6/9	discard	MOSFET clamp 150C OK but leakage too high
d4e5f6g	12.400000	9/9	keep	diode-connected HV NMOS stack 6 devices
```

**Do not commit `results.tsv`.**

---

## 4. The Experiment Loop

### Branch Setup

```bash
git checkout -b autoresearch/zener-clamp-$(date +%b%d | tr '[:upper:]' '[:lower:]')
```

### LOOP FOREVER

```
1. Check git state
2. Form one idea (add/remove device from stack, try MOSFET vs diode, try TC compensation)
3. Modify design.cir
4. git commit -m "exp: <what you tried>"
5. Run: ngspice -b run_block.sh > run.log 2>&1
6. Extract: grep "^leakage_at_5v_nA:\|^clamp_onset_1mA_V:\|^clamp_onset_150c_V:\|^clamp_onset_m40c_V:" run.log
7. If grep empty → crashed. tail -n 50 run.log
8. Log to results.tsv
9. If leakage_at_5v_nA improved AND clamp_onset_150c_V >= 5.0 AND specs_pass equal or better → KEEP
   Else → DISCARD: git reset --hard HEAD~1
10. Go to step 1
```

### Improvement Criterion

**Keep** if `leakage_at_5v_nA` is strictly lower AND clamp_onset_150c_V ≥ 5.0V AND `specs_pass` does not decrease.
**Discard** otherwise. You cannot trade away the 150°C lower bound to get lower leakage — both must be satisfied simultaneously.

### Timeout

I–V sweeps and temperature sweeps are fast. 10–15 minutes per full run. Timeout at 25 minutes.

### NEVER STOP

The TC problem is hard. If a pure diode stack fails at 150°C, try a MOSFET-based clamp. If that has too much leakage, try TC compensation. Try every combination. Each attempt teaches you something about the trade-off space. Keep the simplest circuit that passes all corners — fewer devices, better.
