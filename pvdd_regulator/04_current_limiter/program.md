# Block 04: Current Limiter — Design Program

---

## 1. Setup

### Purpose

The current limiter protects the HV pass device from destruction during output short-circuit or overload conditions. Without it, a shorted PVDD output would force the error amp to drive the pass device to maximum current, potentially exceeding safe operating area limits and causing thermal runaway or oxide breakdown.

The current limiter senses the output current and, when it exceeds the threshold (60–80 mA), limits the gate drive to cap the maximum output current regardless of load impedance. Under normal operation (0–50 mA) the limiter must be completely transparent — it must not affect regulation, loop stability, or quiescent current in any observable way.

This is a Wave 2 block. It requires Blocks 00, 01, 02, and 03 to be complete before full closed-loop verification.

### Read Before Starting

Read these files to understand the full system context before touching any circuit:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `04_current_limiter/specification.json` — this block's pass/fail criteria (numeric, machine-readable)
- `01_pass_device/results.md` — pass device W/L (sense element must match)
- `03_compensation/results.md` — loop stability baseline (must remain stable with limiter in circuit)

### Create results.md

Create `04_current_limiter/results.md` before running any simulation. Update it after every simulation run. It must contain:

- **Topology chosen** (sense mirror, sense resistor, foldback, etc.) and the reason
- **Results table**: parameter | simulated value | spec limit | pass/fail
- **Simulation log**: what was changed, what improved or degraded, convergence issues
- **Open issues**: anything not yet meeting spec

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance configured for this block only. The instance has:
- Full SkyWater SKY130A PDK installed
- ngspice installed and tested
- This block directory (`04_current_limiter/`) as the working directory
- Blocks 00–03 `design.cir` files available via `.include`

### What You Can Do

You are free to choose any current limiting topology. Options to consider:

- **Sense mirror (scaled replica).** A small replica of the pass device (W_sense = W_pass / N) carries a proportional current. When sense current exceeds a reference, the limiter activates. Classic approach, but mirror ratio accuracy depends on Vds matching.
- **Sense resistor in series.** A small resistor in the main current path. Voltage across it is compared to a threshold. Simple but adds dropout voltage (must be < 50 mV at 50 mA → resistor < 1 Ω).
- **Brick-wall limiter.** Hard clamp at the threshold. Simpler to design but higher power dissipation during sustained shorts.
- **Foldback current limiter.** Reduces the current limit as Vout drops — limits pass device power during shorts. More complex but thermally safer.
- **Hybrid.** Brick-wall for fast response, then foldback for thermal protection during sustained events.

The sense element must use the same Sky130 HV device type and same L as the main pass device (Block 01). Use N = W_pass / W_sense as the mirror ratio.

Modify `design.cir` freely. Add testbench files as needed. Everything in this directory is yours to change.

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria. The evaluator reads it.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md`** — this file defines the design rules.
- **Do not use behavioral current limiters, ideal comparators, or ideal switches** for any internal device.

### Goal

Meet **all** pass/fail criteria in `specification.json`, verified by real ngspice simulations. The limiter threshold must stay above 50 mA at SS 150°C (worst case — do not interfere with normal operation) and below 100 mA at FF −40°C (must actually protect). The loop must remain stable with the limiter in circuit at all normal load points.

Short-circuit simulations stress convergence. Fix convergence problems with `.option` settings and initial conditions (`.ic`), not by replacing the circuit.

### Simplicity Criterion

All else being equal, simpler is better. A brick-wall sense mirror that meets all specs is better than a foldback with extra complexity that marginally reduces peak power. Add foldback only if the brick-wall design creates a real reliability problem that cannot otherwise be addressed.

---

### Optimization

Use `optimize.py` to center the current limit threshold at 75 mA (midpoint of 50–100 mA spec) with minimum PVT spread.

**Framework (scipy):**

```python
from scipy.optimize import differential_evolution, minimize
import subprocess, re

def cost(params):
    # Write mirror ratio N and Rsense into design.cir via .param substitution
    # subprocess.run(['ngspice', '-b', 'run_block.sh'], capture_output=True)
    # Parse ilim_threshold_mA from run.log
    # Return (ilim_threshold_mA - 75)**2 + pvt_spread_penalty
    pass

result = differential_evolution(cost, bounds=[(1, 20), (0.1, 10)], maxiter=100, seed=42)
result = minimize(cost, result.x, method='Nelder-Mead', options={'xatol': 0.1, 'fatol': 0.01})
```

**Variables:** sense mirror ratio N (1–20), sense resistor Rsense (0.1–10 Ω), NMOS pull-down W/L.

**Objective:** minimize |Ilim − 75 mA| at TT 27°C (centering within 50–100 mA band gives maximum PVT margin).

**Constraints (penalty if violated):**
- Ilim threshold 50–100 mA at all 15 PVT corners
- 3σ MC spread stays within 50–110 mA
- Response time < 1 µs (sense node bandwidth)
- Leakage through sense path < 10 µA at normal operation (Iout = 0)

**Commit strategy:** commit per-block only. Keep if `ilim_threshold_mA` moves closer to 75 mA and all constraints pass:
```bash
git add pvdd_regulator/04_current_limiter/ && git commit -m "exp(04): <what changed>"
```
Regress → `git checkout pvdd_regulator/04_current_limiter/design.cir`.

---

### Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `gate` | In/Out | 0 to ~PVDD | Error amp output / pass device gate (clamped when limit hit) |
| `bvdd` | Supply | 5.4–10.5V | Battery supply |
| `pvdd` | Sense | 5.0V regulated | Output node (for current monitoring) |
| `gnd` | Supply | 0V | Ground |
| `ilim_flag` | Output | Digital | Current limit active flag (optional) |

Subcircuit signature: `.subckt current_limiter gate bvdd pvdd gnd ilim_flag`

**Connections in the LDO:**
- Under normal operation (0–50 mA), the limiter is completely transparent
- When current exceeds the threshold, the limiter overrides the error amp's gate drive
- `ilim_flag` connects to mode control (Block 08) if implemented

---

### Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Current limit threshold | 60 | 70 | 80 | mA | 20–60% above 50 mA max load |
| Threshold accuracy over PVT | — | — | ±20 | % | Acceptable for protection |
| Response time | — | — | 10 | µs | From overcurrent to clamping |
| Sense element area overhead | — | — | 5 | % | Fraction of main pass device area |
| Quiescent current overhead | — | — | 10 | µA | Under normal (non-limiting) operation |
| Voltage headroom consumed | — | — | 50 | mV | Additional dropout from sense element |
| Temperature range | −40 | 27 | 150 | °C | |

---

### Operating Conditions

- **Normal mode:** Iload = 0 to 50 mA. Limiter must be completely inactive.
- **Limiting mode:** Iload tries to exceed 60–80 mA. Limiter activates.
- **Short-circuit:** Rload approaches 0 Ω. Limiter must protect the pass device.
- **BVDD range:** 5.4 to 10.5V during limiting.
- **Corners:** SS/TT/FF/SF/FS at −40°C, 27°C, 150°C.

---

### Known Challenges

1. **Threshold must stay above 50 mA at SS 150°C.** If the limiter trips below 50 mA at any corner, it interferes with normal operation. Worst case is SS 150°C — highest Vth, lowest mobility.

2. **Threshold must stay below 100 mA at FF −40°C.** If it drifts too high at the fast corner, the protection is ineffective.

3. **No interference with normal regulation.** At 50 mA load, the limiter must add negligible voltage drop, noise, or phase shift to the main regulation loop.

4. **Short-circuit convergence.** Simulating a hard short (Rload ≈ 0) with a current limiter active is notoriously difficult for SPICE convergence. Expect to use aggressive `.option` settings.

5. **Power dissipation during sustained shorts.** At Vout = 0V and Ilim = 70 mA, the pass device dissipates P = BVDD × 70 mA = 0.74W at BVDD = 10.5V. Foldback mitigates this.

---

### Dependencies

Wave 2 — requires:
- Block 01 (`01_pass_device/design.cir`) — sense element must match pass device
- Block 00 (`00_error_amp/design.cir`) — needed for closed-loop current limiting
- Block 02 (`02_feedback_network/design.cir`) — needed for closed-loop testing
- Block 03 (`03_compensation/design.cir`) — stability must be verified with limiter in circuit

---

### Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| Output I–V curve showing limiting | Iout vs Vout with Rload swept to near 0 |
| Current limit trip point | Exact threshold at TT 27°C |
| Transient short-circuit response | Time from short to current clamping |
| Normal operation impact | PVDD with and without limiter at 0–50 mA |
| Loop stability with limiter | PM must still be > 45° at normal loads |
| PVT corner threshold | Limit threshold at SS/FF/SF/FS, −40/27/150°C |
| Monte Carlo threshold distribution | 200 runs, TT 27°C — report threshold mean and sigma |

---

### Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Current limit at TT 27°C | 60–80 mA |
| Current limit at SS 150°C | ≥ 50 mA (must not limit below max load) |
| Current limit at FF −40°C | ≤ 100 mA (must actually limit) |
| Response time to short | < 10 µs |
| Impact on PVDD at Iload = 50 mA | < 10 mV difference vs no-limiter |
| Sense element quiescent current | < 10 µA at Iload = 0 |
| No oscillation during limiting | Clean transient, no ringing |
| Loop stability unaffected | PM > 45° with limiter at normal loads |
| MC threshold (200 runs): mean − 3σ | ≥ 50 mA — no run must clip below rated load |
| MC threshold (200 runs): mean + 3σ | ≤ 110 mA — protection must remain effective |

---

### Deliverables

1. `design.cir` — `.subckt current_limiter gate bvdd pvdd gnd ilim_flag`
2. `tb_ilim_iv.spice` — I–V curve with limiting
3. `tb_ilim_trip.spice` — limit threshold at TT/SS/FF corners
4. `tb_ilim_transient.spice` — transient short-circuit response
5. `tb_ilim_normal.spice` — PVDD with and without limiter at 0–50 mA
6. `tb_ilim_lstb.spice` — loop stability with limiter in circuit
7. `tb_ilim_pvt.spice` — threshold at all PVT corners
8. `tb_ilim_mc.spice` — 200-run Monte Carlo on sense mirror mismatch; measure trip threshold at each run; report mean, sigma, min, max; pass if 3σ band stays within 50–110 mA
9. `results.md` — updated after every simulation run
10. `README.md` — the visual window to this block: topology, mirror ratio, and every plot listed below embedded inline

---

### README: Required Plots

The `README.md` is the visual window to this block. The current limit threshold and its variation tell the whole story — every reader must see it.

**Mechanism:** Testbenches save data with `.wrdata`. Run `python3 plot_all.py` to generate all PNGs. Embed with `![description](filename.png)`.

**Plots required in README.md:**

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `ilim_iv_curve.png` | `tb_ilim_iv` | Iout vs Vout — shows linear region, limiting knee, clamped region |
| `ilim_transient.png` | `tb_ilim_transient` | Iout and PVDD vs time during short-circuit event |
| `ilim_pvt_threshold.png` | `tb_ilim_pvt` | Trip threshold at all 15 PVT corners (bar chart) with 50mA and 100mA spec lines |
| `mc_threshold_histogram.png` | `tb_ilim_mc` | Threshold distribution from 200 MC runs — show mean, ±3σ, spec window |

---

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device. No behavioral current limiters or ideal comparators.
2. **No behavioral models.** Only testbench stimulus and load elements may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** Short-circuit simulations stress convergence. Fix with `.option` settings and initial conditions, not by replacing the circuit.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench must print results in this exact format:

```
ilim_ss150_mA: 52.4
ilim_tt27_mA: 68.3
ilim_ff_m40_mA: 87.1
response_time_us: 3.2
pvdd_impact_mV: 2.1
sense_quiescent_uA: 0.8
loop_pm_with_limiter_deg: 48.2
no_oscillation: 1
```

### The specs.tsc File

`specs.tsc` defines all tracked metrics and pass/fail thresholds.

The **primary metric** is `ilim_ss150_mA` — current limit threshold at SS 150°C. Higher is better (keep it as far above 50 mA as possible without pushing the FF −40°C threshold above 100 mA).

### Summary Printed After Each Run

```
---
ilim_ss150_mA:            52.4  mA   (spec >= 50)    PASS
ilim_tt27_mA:             68.3  mA   (spec 60-80)    PASS
ilim_ff_m40_mA:           87.1  mA   (spec <= 100)   PASS
response_time_us:          3.2  us   (spec <= 10)    PASS
loop_pm_with_limiter_deg: 48.2  deg  (spec >= 45)    PASS
specs_pass:               9/9
```

Extract the primary metric:

```bash
grep "^ilim_ss150_mA:" run.log
```

### Logging Results

Log to `results.tsv` (tab-separated):

```
commit	ilim_ss150_mA	specs_pass	status	description
```

Example:

```
commit	ilim_ss150_mA	specs_pass	status	description
a1b2c3d	0.000000	0/9	crash	initial stub
b2c3d4e	44.200000	5/9	discard	mirror ratio too aggressive trips below 50mA
c3d4e5f	52.400000	9/9	keep	W_sense = W_pass/50 meets all corners
d4e5f6g	53.800000	9/9	keep	W_sense = W_pass/55 better SS margin
```

**Do not commit `results.tsv`.**

---

## 4. The Experiment Loop

### Branch Setup

```bash
git checkout -b autoresearch/ilim-$(date +%b%d | tr '[:upper:]' '[:lower:]')
```

### LOOP FOREVER

```
1. Check git state
2. Form one idea (adjust mirror ratio, change sense element size, try foldback vs brick-wall)
3. Modify design.cir
4. git commit -m "exp: <what you tried>"
5. Run: ngspice -b run_block.sh > run.log 2>&1
6. Extract: grep "^ilim_ss150_mA:\|^ilim_tt27_mA:\|^ilim_ff_m40_mA:\|^loop_pm:" run.log
7. If grep empty → crashed. tail -n 50 run.log
8. Log to results.tsv
9. If ilim_ss150_mA improved AND specs_pass equal or better → KEEP
   Else → DISCARD: git reset --hard HEAD~1
10. Go to step 1
```

### Improvement Criterion

**Keep** if `ilim_ss150_mA` is strictly higher and `specs_pass` does not decrease and `ilim_ff_m40_mA` stays ≤ 100 mA.
**Discard** otherwise. The FF −40°C constraint is a hard ceiling — if the SS margin improved but FF now exceeds 100 mA, that is still a discard.

### Timeout

Short-circuit simulations are slow. Allow **30 minutes** per full run. Run only the trip-point testbench first (fast), add the full closed-loop testbench once the threshold looks promising.

### Crashes

Short-circuit (Rload → 0) simulations are notoriously convergence-difficult. Use `.option gmin=1e-10`, `reltol=1e-4`, and `.ic` initial conditions. If it still crashes after 3 attempts, try a higher minimum Rload (0.5 Ω instead of 0.1 Ω) and note the limitation.

### NEVER STOP

Once all specs pass, try to reduce sense_quiescent_uA (less Iq overhead = better). Try to reduce the sense element area fraction. Simplest limiter that passes all corners is the goal.
