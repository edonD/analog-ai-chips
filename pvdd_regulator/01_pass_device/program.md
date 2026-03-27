# Block 01: Pass Device — Design Program

---

## 1. Setup

### Purpose

The pass device is the power transistor that drops the input voltage (BVDD, 5.4–10.5V) to the regulated output (PVDD, 5.0V). All load current — zero to 50 mA — flows through this device. It is the most critical component in the LDO because:

1. Its on-resistance sets the dropout voltage (Vdo = Id × Rds_on at full gate drive).
2. Its gate capacitance (Cgs) is the dominant load for the error amplifier and sets a key pole in the feedback loop.
3. Its transconductance (gm_pass) determines the DC gain from gate to output and the output pole frequency.
4. Everything downstream — error amp sizing, compensation, startup — depends on this block's characterization.

**Characterize this block first, before designing anything else.** Its outputs (W/L, Cgs, gm, Rds_on) are required inputs to Blocks 00, 03, and 04.

This is a Wave 1 block — no dependencies on other blocks.

### Read Before Starting

Read these files to understand the full system context before touching any circuit:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues, ideal source values
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `01_pass_device/specification.json` — this block's pass/fail criteria (numeric, machine-readable)

### Create results.md

Create `01_pass_device/results.md` before running any simulation. Update it after every simulation run. It must contain:

- **Device configuration chosen** (PMOS/NMOS, device type, W/L, finger count) and the reason
- **Characterization table**: Cgs (pF), gm at 10 mA (mA/V), Rds_on (Ω), Vdo at 50 mA (mV), total W (mm)
- **Results table**: parameter | simulated value | spec limit | pass/fail
- **Simulation log**: what was changed, what improved or degraded
- **Open issues**: anything not yet meeting spec

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance configured for this block only. The instance has:
- Full SkyWater SKY130A PDK installed
- ngspice installed and tested
- This block directory (`01_pass_device/`) as the working directory

### What You Can Do

You are free to choose any pass device configuration that meets the specifications. Key decisions are yours:

- **PMOS vs NMOS:**
  - PMOS common-source (`pfet_g5v0d10v5`): low dropout (Vdo = Vds_sat), gate pulled to GND to turn fully ON. Standard LDO approach. Recommended.
  - NMOS source-follower (`nfet_g5v0d10v5`): higher dropout (Vdo = Vgs > Vth + Vdsat), gate must go above PVDD — needs charge pump. More complex, not recommended unless you have a strong reason.

- **Device type:** `pfet_g5v0d10v5` (10.5V rated) or `pfet_05v0` (5V rated). The g5v0d10v5 supports the full BVDD range.

- **W/L selection:** L = minimum for HV device (0.5µm for g5v0d10v5) gives lowest Rds_on but worst λ. Longer L improves output resistance.

- **Finger/parallel strategy:** Single device with many fingers vs. multiple parallel instances.

Modify `design.cir` freely. Add testbench files as needed. Everything in this directory is yours to change.

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria. The evaluator reads it.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md`** — this file defines the design rules.
- **Do not use behavioral MOSFET models or ideal switches** in place of real Sky130 PDK device instantiations.

### Goal

Meet **all** pass/fail criteria in `specification.json`, verified by real ngspice simulations with Sky130 PDK models. Every claimed spec must come from a `.spice` testbench that anyone can re-run. The Cgs and gm values you report here will be used directly by Blocks 00 and 03 — they must be accurate.

### Simplicity Criterion

All else being equal, simpler is better. A small improvement in Rds_on that requires doubling device count is not worth it. If a single device type with straightforward fingering meets all specs, that is the right choice. Removing complexity and getting equal or better results is a win.

---

### Optimization

Use `optimize.py` to find the minimum finger count that meets Id ≥ 50mA at dropout without exhaustive manual sweeping.

**Framework (scipy):**

```python
from scipy.optimize import differential_evolution, minimize
import subprocess, re

def cost(params):
    # Write Nf (finger count) and W/finger into design.cir via .param substitution
    # subprocess.run(['ngspice', '-b', 'run_block.sh'], capture_output=True)
    # Parse id_at_dropout_mA from run.log
    # Return Nf (minimizing finger count), large penalty if Id < 50mA or Cgs > 10pF
    pass

result = differential_evolution(cost, bounds=[(4, 64), (1e-6, 10e-6)], maxiter=50, seed=42)
result = minimize(cost, result.x, method='Nelder-Mead', options={'xatol': 1, 'fatol': 0.1})
```

**Variables:** number of fingers (Nf, integer), width per finger (W, 1–10 µm).

**Objective:** minimize Nf (smallest device that still passes — minimizes Cgs and area).

**Constraints (penalty if violated):**
- Id ≥ 50 mA at Vds = 400 mV, Vgs = −5V, TT 27°C
- Id ≥ 30 mA at SS 150°C (worst case)
- Cgs < 10 pF (limits error amp loading)
- Operating point inside Sky130 pfet_g5v0d10v5 SOA at BVDD = 10.5V, Iload = 50mA, T = 150°C

**Commit strategy:** commit per-block only. Keep if `id_at_dropout_mA` ≥ 50 and Nf decreased:
```bash
git add pvdd_regulator/01_pass_device/ && git commit -m "exp(01): <what changed>"
```
Regress → `git checkout pvdd_regulator/01_pass_device/design.cir`. Never mix block changes.

---

### Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `gate` | Input | 0 to ~BVDD | Gate drive from error amp |
| `bvdd` | Input (source) | 5.4–10.5V | Battery supply |
| `pvdd` | Output (drain) | 5.0V regulated | Regulated output |

Subcircuit signature: `.subckt pass_device gate bvdd pvdd`

Body connection is handled internally (source/bulk tied to BVDD for PMOS).

**Connections in the LDO:**
- Source/bulk = BVDD supply rail
- Drain = PVDD output rail (also connected to 200 pF Cload, feedback divider, UV/OV sense)
- Gate = error amp output (`vout_gate` from Block 00), compensation network (Block 03)

---

### Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Drain current at Vdo = 400 mV | 50 | — | — | mA | Full load, gate fully driven, TT 27°C |
| Drain current at Vdo = 400 mV | 50 | — | — | mA | SS 150°C worst case |
| Gate capacitance (Cgs) | — | TBD | — | pF | At operating point — report this value |
| Transconductance (gm) | — | TBD | — | mA/V | At Iload = 10 mA — report this value |
| Rds_on (full gate drive) | — | TBD | 20 | Ω | At max Vgs |
| Leakage current (off) | — | — | 1 | µA | Vgs = 0V |
| Total device width | — | — | 20 | mm | Must be layout-feasible |
| Max Vds | — | — | 10.5 | V | Sky130 HV device limit |
| Temperature range | −40 | 27 | 150 | °C | |

---

### Operating Conditions

- **Input:** BVDD = 5.4 to 10.5V
- **Output:** PVDD = 5.0V nominal, with 200 pF internal load cap
- **Load current:** 0 to 50 mA (active mode), 0 to 0.5 mA (retention mode)
- **Gate drive:** Error amp output, swing 0 to PVDD (or BVDD)
- **Corners:** SS/TT/FF/SF/FS at −40°C, 27°C, 150°C

---

### Known Challenges

1. **Low mobility of HV devices.** Sky130 HV PMOS has significantly lower mobility than standard PMOS. Expect total W in the multi-mm range to achieve 50 mA at 400 mV dropout. If W exceeds 20 mm the topology is impractical.

2. **Large gate capacitance.** A multi-mm device will have Cgs in the 50–200 pF range. This is the dominant load for the error amplifier and a key pole in the LDO loop. This value must be characterized accurately.

3. **SS corner at 150°C is worst case.** Highest Rds_on, lowest mobility, highest Vth. The pass device must still deliver 50 mA at 400 mV dropout under worst-case conditions.

4. **Finger count and layout.** A multi-mm device needs many fingers or multiple parallel instances. Gate resistance from long poly fingers can degrade high-frequency behavior.

---

### Dependencies

Wave 1 — no dependencies on other blocks.

This block should be designed and characterized first. Cgs and gm values must be reported in `results.md` and `README.md` before Blocks 00 and 03 can be properly sized.

---

### Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| Id vs Vds family curves | At multiple Vgs values — characterize the device |
| Id vs Vgs at dropout condition | Key sizing curve — find required W |
| Gate capacitance (Cgs) vs bias | At operating point (critical for Blocks 00/03) |
| Transconductance (gm) vs Id | At Iload = 10 mA |
| On-resistance (Rds_on) | At full gate drive |
| Leakage current | At Vgs = 0V, BVDD = 7V |
| PVT corner characterization | Id at dropout at all SS/FF/SF/FS, −40/27/150°C |
| Safe operating area (SOA) | Transient stress at max Vds and current — all operating corners |
| Power dissipation at all BVDD × Iload combinations | Verify device stays within thermal SOA; worst case is BVDD=10.5V, Iload=50mA, T=150°C → (10.5−5.0)×50mA = 275mW |

---

### Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Id at dropout, TT 27°C | ≥ 50 mA at Vds = 400 mV, full gate drive |
| Id at dropout, SS 150°C | ≥ 50 mA (worst case) |
| Total W | < 20 mm |
| Cgs at operating point | Measured and documented |
| gm at 10 mA | Measured and documented |
| Rds_on at full gate drive | < 20 Ω |
| Leakage at Vgs = 0V | < 1 µA |
| SOA at BVDD=10.5V, Iload=50mA, T=150°C | Device operating point must be inside Sky130 pfet_g5v0d10v5 rated SOA envelope |
| SOA during startup transient | Peak Vds × Id product must not exceed device rating at any instant |
| No model errors | All testbenches complete without errors |

---

### Deliverables

1. `design.cir` — `.subckt pass_device gate bvdd pvdd`
2. `tb_pass_idvds.spice` — Id vs Vds family curves
3. `tb_pass_idvgs.spice` — Id vs Vgs at dropout condition, W sizing
4. `tb_pass_cgs.spice` — Cgs vs bias at operating point
5. `tb_pass_gm.spice` — gm vs Id
6. `tb_pass_rds.spice` — Rds_on at full gate drive
7. `tb_pass_leakage.spice` — off-state leakage
8. `tb_pass_pvt.spice` — Id at dropout across all PVT corners
9. `tb_pass_soa.spice` — full SOA verification: sweep Vds from 0 to 10.5V at Id=50mA at T=150°C; plot operating point against device SOA boundary; also simulate a startup transient pulse (BVDD step 0→10.5V, Iload=50mA) to capture peak instantaneous stress
10. `results.md` — updated after every simulation run
11. `README.md` — the visual window to this block: final W/L table, Cgs value, gm value, Rds_on, and every plot listed below embedded inline

---

### README: Required Plots

The `README.md` is the visual window to this block. Any designer reading it must be able to determine whether the pass device is adequate without re-running simulations.

**Mechanism:** Testbenches save data with `.wrdata`. Run `python3 plot_all.py` to generate all PNGs. Embed with `![description](filename.png)`.

**Plots required in README.md:**

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `idvds_family.png` | `tb_pass_idvds` | Id vs Vds at multiple Vgs — full device characterization |
| `idvgs_dropout.png` | `tb_pass_idvgs` | Id vs Vgs at Vds=400mV — sizing curve, shows required W |
| `cgs_vs_vgs.png` | `tb_pass_cgs` | Cgs (pF) vs Vgs — critical for Block 00 and Block 03 sizing |
| `gm_vs_id.png` | `tb_pass_gm` | Transconductance (mA/V) vs drain current |
| `pvt_id_dropout.png` | `tb_pass_pvt` | Id at dropout across all 15 PVT corners (bar chart) — SS 150°C is the design point |
| `soa_overlay.png` | `tb_pass_soa` | Device SOA boundary with operating points plotted: nominal, max BVDD, startup transient |

---

## Absolute Rules

1. **Real Sky130 PDK only.** The pass device must be an instantiated Sky130 HV device. No behavioral MOSFET models, no ideal switches.
2. **No behavioral models.** Only testbench supply sources and stimulus elements may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.** Do not hand-calculate W/L for HV devices — simulate and find it.
5. **Push through difficulty.** The HV device may have low mobility and need very large W. That is expected. Do not replace it with an ideal switch or a behavioral model.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench (or the wrapper script that runs them) must print results in this exact format:

```
id_dropout_tt27: 58.3
id_dropout_ss150: 51.7
total_width_mm: 8.4
rds_on_ohm: 8.6
leakage_off_uA: 0.03
cgs_pF: 142.0
gm_at_10mA: 28.5
```

Use ngspice `.meas` statements to compute these values. Use a shell wrapper `run_block.sh` to invoke all testbenches and collect output into `run.log`.

### The specs.tsc File

`specs.tsc` defines the metrics to track, the grep patterns to extract them, and the pass/fail thresholds.

The **primary metric** for this block is `id_dropout_ss150_mA` — drain current at Vdo=400mV at the SS 150°C worst-case corner. Higher is better. The goal is to find a W/L and configuration that maximizes this while keeping total width < 20 mm.

### Summary Printed After Each Run

```
---
id_dropout_tt27:    58.3  mA   (spec >= 50)   PASS
id_dropout_ss150:   51.7  mA   (spec >= 50)   PASS
total_width_mm:      8.4  mm   (spec <= 20)   PASS
rds_on_ohm:          8.6  ohm  (spec <= 20)   PASS
cgs_pF:            142.0  pF   (measured)     INFO
gm_at_10mA:         28.5  mA/V (measured)     INFO
specs_pass:         7/7
```

Extract the primary metric:

```bash
grep "^id_dropout_ss150:" run.log
```

### Logging Results

Log to `results.tsv` (tab-separated). Header and columns:

```
commit	id_dropout_ss150_mA	specs_pass	status	description
```

Example:

```
commit	id_dropout_ss150_mA	specs_pass	status	description
a1b2c3d	0.000000	0/7	crash	initial stub no device
b2c3d4e	38.400000	5/7	discard	W=4mm L=0.5u not enough current
c3d4e5f	51.700000	7/7	keep	W=8.4mm L=0.5u 16 fingers meets spec
d4e5f6g	53.100000	7/7	keep	W=9mm slight improvement SS150
```

**Do not commit `results.tsv`.**

---

## 4. The Experiment Loop

### Branch Setup

```bash
git checkout -b autoresearch/pass-device-$(date +%b%d | tr '[:upper:]' '[:lower:]')
```

### LOOP FOREVER

```
1. Check git state
2. Form one experimental idea (change W, change L, change finger count, try different device type)
3. Modify design.cir
4. git commit -m "exp: <what you tried>"
5. Run: ngspice -b run_block.sh > run.log 2>&1
6. Extract: grep "^id_dropout_ss150:\|^total_width_mm:\|^cgs_pF:\|^rds_on_ohm:" run.log
7. If grep empty → crashed. tail -n 50 run.log
8. Log to results.tsv
9. If id_dropout_ss150_mA improved AND specs_pass equal or better → KEEP
   Else → DISCARD: git reset --hard HEAD~1
10. Go to step 1
```

### Improvement Criterion

**Keep** if `id_dropout_ss150_mA` is strictly higher and `specs_pass` does not decrease.
**Keep** also if `specs_pass` increases (more specs passing) even without primary metric improvement.
**Discard** otherwise.

Note: once all specs pass (7/7), optimize for maximum id_dropout_ss150_mA margin and minimum total_width_mm (smaller area for same performance is a simplification win).

### Timeout

30 minutes per full run. If exceeded, kill and treat as failure.

### Crashes

Convergence failures in Id vs Vds sweeps are common with HV devices. Add `.option gmin=1e-12` and reduce timestep. If still failing, try a different W split (more fingers of smaller width).

### NEVER STOP

Continue indefinitely until manually interrupted. If the device already meets all specs, keep trying to minimize width or explore whether a different finger configuration gives better SS corner performance. A smaller, passing design is always worth finding.
