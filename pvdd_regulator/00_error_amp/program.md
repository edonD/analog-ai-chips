# Block 00: Error Amplifier — Design Program

---

## 1. Setup

### Purpose

The error amplifier is the heart of the PVDD LDO feedback loop. It compares the feedback voltage (V_FB ≈ 1.226V from the resistive divider) to the bandgap reference (V_REF = 1.226V) and drives the gate of the HV pass device. Its DC gain sets regulation accuracy. Its bandwidth and output impedance, combined with the pass device gate capacitance and the compensation network, determine loop stability and transient response.

This is a Wave 1 block — it has no dependencies on other blocks and can be designed immediately.

### Read Before Starting

Read these files to understand the full system context before touching any circuit:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues, ideal source values
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `00_error_amp/specification.json` — this block's pass/fail criteria (numeric, machine-readable)

### Create results.md

Create `00_error_amp/results.md` before running any simulation. Update it after every simulation run. It must contain:

- **Topology chosen** and the reason for choosing it
- **Results table**: parameter | simulated value | spec limit | pass/fail
- **Simulation log**: what was changed, what improved or degraded, any convergence issues encountered
- **Open issues**: anything not yet meeting spec

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance configured for this block only. The instance has:
- Full SkyWater SKY130A PDK installed
- ngspice installed and tested
- This block directory (`00_error_amp/`) as the working directory

### What You Can Do

You are free to choose any error amplifier topology that meets the specifications. The design space is wide:

- **Folded-cascode OTA** — high gain in one stage, wide output swing, single high-impedance node. Good starting point.
- **Telescopic cascode OTA** — highest gm efficiency, but limited output range. May not achieve the required swing.
- **Two-stage OTA with Miller compensation** — can achieve >80 dB gain but adds a pole that complicates Block 03.
- **Recycling folded-cascode** — improved slew rate and gm efficiency.
- **Class-AB output stage** — better slew rate for driving the large pass device gate capacitance.
- **Current-mirror OTA** — simple but may not achieve sufficient gain.
- **Any combination or variant** you think is appropriate.

Consider whether to use a PMOS or NMOS input pair based on the common-mode input level (~1.226V). A PMOS input pair sits well above GND. An NMOS input pair works if the inputs are above Vth + Vdsat_tail.

Because the error amp runs from PVDD (5V), any 1.8V Sky130 device must be cascoded or otherwise protected. HV devices (`sky130_fd_pr__pfet_g5v0d10v5`, `sky130_fd_pr__nfet_g5v0d10v5`) are the safer choice for this supply domain.

Modify `design.cir` freely. Add testbench files as needed. Everything in this directory is yours to change.

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria. The evaluator reads it.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md`** — this file defines the design rules.
- **Do not use behavioral models, ideal op-amps, VCCS sources, or VerilogA** for any internal device. The only ideal components allowed are: `V_AVBG` (1.226V bandgap), `I_BIAS` (1µA reference), and testbench stimulus/supply sources.

### Goal

Meet **all** pass/fail criteria in `specification.json`, verified by real ngspice simulations with Sky130 PDK models. Every claimed spec must come from a `.spice` testbench that anyone can re-run. Hand calculations are for initial sizing only — simulation is the only truth.

Run every testbench listed in the Testbench Requirements section. Do not skip any.

### Simplicity Criterion

All else being equal, simpler is better. A small performance improvement that adds ugly complexity is not worth it. Conversely, removing a device or stage and achieving equal or better results is a great outcome — that is a simplification win. When two topologies meet the spec equally, choose the simpler one.

---

### Optimization

Use `optimize.py` to sweep device parameters without manual trial-and-error. The optimizer calls ngspice in batch mode, parses the primary metric, and searches the design space efficiently.

**Framework (scipy):**

```python
from scipy.optimize import differential_evolution, minimize
import subprocess, re

def cost(params):
    # Write W/L values into design.cir via .param substitution
    # subprocess.run(['ngspice', '-b', 'run_block.sh'], capture_output=True)
    # Parse primary metric from run.log
    # Return -metric (maximizing gain×PM product), large penalty if constraints violated
    pass

# Phase 1 — global search (gradient-free, handles non-convex SPICE landscape)
result = differential_evolution(cost, bounds=[...], maxiter=100, tol=0.01, seed=42, workers=1)
# Phase 2 — local refinement
result = minimize(cost, result.x, method='Nelder-Mead', options={'xatol': 0.01, 'fatol': 0.001})
```

**Variables:** input pair W/L (Min), tail mirror W/L (Mtail), load mirror W/L (Mload), output stage W/L (Mout), bias current (Ibias).

**Objective:** maximize DC gain × GBW product (primary metric = `gain_dB` from run.log).

**Constraints (penalty if violated):**
- GBW ≥ 5 MHz
- Phase margin ≥ 60°
- Output swing: 0.5V to PVDD − 0.3V
- Input offset < 2 mV at TT 27°C
- CMRR > 60 dB, PSRR > 60 dB

**Commit strategy:** commit per-block only. Keep a result if `gain_dB` improves and all constraints pass:
```bash
git add pvdd_regulator/00_error_amp/ && git commit -m "exp(00): <what changed>"
```
If the run fails or regresses → `git checkout pvdd_regulator/00_error_amp/design.cir`. Never mix block changes in one commit.

---

### Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `vref` | Input | ~1.226V | Bandgap reference (positive OTA input) |
| `vfb` | Input | ~1.226V | Feedback voltage from divider (negative OTA input) |
| `vout_gate` | Output | 0 to ~PVDD | Drives pass device gate |
| `pvdd` | Supply | 5.0V regulated | Positive supply rail |
| `gnd` | Supply | 0V | Ground |
| `ibias` | Input | — | 1µA bias current input (mirrored internally) |
| `en` | Input | 0 / PVDD | Enable signal |

Subcircuit signature: `.subckt error_amp vref vfb vout_gate pvdd gnd ibias en`

**Connections in the LDO:**
- `vref` ← ideal V_AVBG (1.226V)
- `vfb` ← feedback divider midpoint (Block 02)
- `vout_gate` → pass device gate (Block 01) and compensation network (Block 03)
- `pvdd` ← regulated PVDD output rail
- `ibias` ← shared IREF current mirror

---

### Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| DC open-loop gain | 60 | 70 | — | dB | At DC, no load |
| Unity-gain bandwidth (UGB) | 200 | 500 | 1000 | kHz | With Cgs_pass load (~100 pF placeholder) |
| Phase margin (open-loop, into Cgs) | 55 | 70 | — | deg | Error amp alone, not full LDO loop |
| Input offset voltage | — | — | 5 | mV | Contributes directly to PVDD error |
| Input common-mode range | 0.8 | — | 2.0 | V | Must include 1.226V |
| Output voltage swing low | — | — | 0.5 | V | Must pull pass gate near GND (fully ON) |
| Output voltage swing high | PVDD−0.5 | — | — | V | Error amp max output; full pass device shutoff requires BVDD-domain gate pull-up (Block 08) |
| Supply voltage (PVDD) | 4.5 | 5.0 | 5.5 | V | Regulated domain |
| Quiescent current | — | 50 | 100 | µA | From PVDD supply |
| CMRR | 50 | 60 | — | dB | At DC |
| PSRR (from PVDD) | 40 | 50 | — | dB | At DC |
| Slew rate (positive) | 0.5 | — | — | V/µs | Charging Cgs_pass |
| Slew rate (negative) | 0.5 | — | — | V/µs | Discharging Cgs_pass |
| Temperature range | −40 | 27 | 150 | °C | |

---

### Operating Conditions

- **Supply:** PVDD = 4.5 to 5.5V. During startup PVDD may not be established — see Known Challenges.
- **Load:** The error amp output drives the pass device gate capacitance (50–200 pF from Block 01 characterization). Purely capacitive load. Use 100 pF as placeholder until Block 01 is complete.
- **Input levels:** Both inputs near 1.226V.
- **Corners:** SS/TT/FF/SF/FS at −40°C, 27°C, 150°C.

---

### Known Challenges

1. **The error amp runs from PVDD (5V), but Sky130 1.8V devices have Vds_max = 1.8V.** You cannot use standard 1.8V transistors in a 5V domain without cascode protection. You must use HV devices (`sky130_fd_pr__pfet_g5v0d10v5`, `sky130_fd_pr__nfet_g5v0d10v5`) or carefully stacked 1.8V devices with cascode protection. This applies to every transistor in the amplifier.

2. **High Vth in Sky130 HV devices.** HV PMOS Vth ≈ 0.7–1.0V, HV NMOS Vth ≈ 0.6–0.9V. This eats into headroom and makes it harder to achieve wide output swing and high gain with limited supply.

3. **Large capacitive load (50–200 pF).** The pass device gate capacitance is the dominant load. UGB = gm / (2π·Cload). Size the tail current accordingly.

4. **Startup chicken-and-egg.** The error amp needs PVDD to operate but PVDD needs the error amp. The startup circuit (Block 09) solves this, but the error amp must be designed to start cleanly when PVDD first becomes available.

5. **Output swing is limited by PVDD supply.** To fully turn the PMOS pass device ON, the gate must approach GND — achievable. To turn it fully OFF at BVDD = 10.5V, the gate must reach ≥ 9.7V (BVDD − |Vth| ≈ 9.7V) — this is unreachable from a 5V supply. **The error amp cannot shut off the pass device at high BVDD.** Full shutoff is handled exclusively by Block 08 (mode control), which drives a dedicated BVDD-domain HV NMOS to pull the gate to BVDD. The error amp's job is regulation in the linear region, not rail-to-rail shutoff.

---

### Dependencies

Wave 1 — no dependencies on other blocks.

Use Cgs = 100 pF as a placeholder for the pass device gate capacitance. Re-verify once Block 01 is complete and the actual Cgs value is known.

---

### Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| DC operating point | All node voltages, verify all devices in saturation |
| Open-loop gain and phase | Gain (dB), UGB (Hz), phase margin (deg) with Cgs load |
| Output swing | Verify output reaches within spec of both rails |
| CMRR | Common-mode rejection ratio at DC |
| PSRR | Power supply rejection from PVDD at DC |
| Quiescent current | Total Iq from PVDD with en=PVDD |
| PVT corners | All above at SS/FF/SF/FS and −40/27/150°C |
| Output noise | Voltage noise spectral density at vout_gate (V/√Hz) and at vfb input-referred; integrated noise 10 Hz–1 MHz |

---

### Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| DC gain | ≥ 60 dB |
| UGB (with Cgs_pass load) | 200 kHz to 1 MHz |
| Phase margin (OL into Cgs) | ≥ 55 deg |
| All devices in saturation | Vds > Vdsat + 50 mV at nominal OP |
| Output swing low | < 0.5V |
| Output swing high | > PVDD − 0.5V (note: full shutoff at BVDD > 5.5V requires Block 08 gate pull-up) |
| Quiescent current | < 100 µA from PVDD |
| Input offset | < 5 mV |
| CMRR | > 50 dB at DC |
| PSRR | > 40 dB at DC |
| Input-referred noise (integrated 10 Hz–1 MHz) | < 20 µVrms — sets floor for PVDD output noise |
| All above at SS, FF, SF, FS | Yes |
| All above at −40, 27, 150°C | Yes |

---

### Deliverables

1. `design.cir` — `.subckt error_amp vref vfb vout_gate pvdd gnd ibias en`
2. `tb_ea_dc.spice` — DC operating point, saturation check, Iq
3. `tb_ea_ac.spice` — open-loop gain and phase, UGB, phase margin
4. `tb_ea_swing.spice` — output swing verification
5. `tb_ea_cmrr.spice` — CMRR
6. `tb_ea_psrr.spice` — PSRR at DC and full frequency sweep 10 Hz–10 MHz
7. `tb_ea_noise.spice` — output noise spectral density and integrated noise; use `.noise` analysis; report V/√Hz at 1 kHz and 10 kHz, and integrated µVrms from 10 Hz–1 MHz
8. `tb_ea_pvt.spice` — all above at all PVT corners
9. `results.md` — updated after every simulation run
10. `README.md` — the visual window to this block: topology diagram, device table, operating point summary, and every plot listed below embedded inline

---

### README: Required Plots

The `README.md` is the visual window to this block. Every reader must be able to understand the amplifier's behavior by reading the README alone — no simulation re-runs required. Every significant result appears as an embedded plot.

**Mechanism:** Each testbench saves output data with `.wrdata filename.dat`. A `plot_all.py` script reads the `.dat` files and writes PNG plots using matplotlib. Run `python3 plot_all.py` after all testbenches. Embed in README with `![description](filename.png)`.

**Plots required in README.md:**

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `bode_gain_phase.png` | `tb_ea_ac` | Open-loop gain (dB) and phase (°) vs frequency — overlay TT/SS/FF corners |
| `output_swing.png` | `tb_ea_swing` | Vout vs differential input — shows near-rail swing limits |
| `noise_spectral.png` | `tb_ea_noise` | Input-referred noise (nV/√Hz) vs frequency 10 Hz–10 MHz |
| `psrr_vs_freq.png` | `tb_ea_psrr` | PSRR (dB) vs frequency 10 Hz–10 MHz |
| `pvt_gain.png` | `tb_ea_pvt` | DC gain at all 15 PVT conditions (bar or scatter) |
| `pvt_pm.png` | `tb_ea_pvt` | Phase margin at all 15 PVT conditions |

---

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device. No exceptions.
2. **No behavioral models.** No ideal op-amps, no VCCS approximations, no VerilogA. The only ideal components allowed are: `V_AVBG` (1.226V bandgap), `I_BIAS` (1µA reference), and testbench stimulus/supply sources.
3. **ngspice only.** No HSPICE, Spectre, or Xyce. Fix convergence with `.option` settings (reltol, abstol, gmin, etc.).
4. **Every spec verified by simulation.** Hand calculations are for initial sizing only. The final claimed performance must come from a re-runnable ngspice testbench.
5. **Push through difficulty.** The HV device headroom will be tight. The output swing will be hard to achieve. Convergence will fail. None of these are reasons to simplify the circuit by replacing devices with behavioral models or skipping verification. Iterate on the real circuit until it works.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench (or the wrapper script that runs them) must print results in this exact format so that `grep` can extract them:

```
phase_margin: 67.3
dc_gain_dB: 72.4
ugb_kHz: 450.2
output_swing_low_V: 0.31
output_swing_high_V: 4.72
iq_uA: 48.1
input_offset_mV: 1.8
cmrr_dB: 63.0
psrr_dB: 52.1
devices_in_sat: 1
pvt_all_pass: 1
```

Use ngspice `.meas` statements to compute these values inside the simulation. Use a shell wrapper (e.g. `run_block.sh`) to invoke all testbenches and collect their output into a single `run.log`. Every metric listed in `specs.tsc` must appear in `run.log` exactly once per run.

### The specs.tsc File

`specs.tsc` defines the metrics to track, the grep patterns to extract them, and the pass/fail thresholds. Do not modify it. Read it to understand what the experiment loop is measuring.

The **primary metric** for this block is `phase_margin_deg` — the open-loop phase margin with the Cgs_pass load. Higher is better. The experiment loop uses this as the headline number.

### Summary Printed After Each Run

After each run, the wrapper script (or you manually) prints a summary of the key metrics extracted from `run.log`:

```
---
phase_margin:     67.3  deg   (spec >= 55)    PASS
dc_gain_dB:       72.4  dB    (spec >= 60)    PASS
ugb_kHz:         450.2  kHz   (spec 200-1000) PASS
iq_uA:            48.1  uA    (spec <= 100)   PASS
input_offset_mV:   1.8  mV    (spec <= 5)     PASS
cmrr_dB:          63.0  dB    (spec >= 50)    PASS
psrr_dB:          52.1  dB    (spec >= 40)    PASS
specs_pass:       12/12
```

Extract the primary metric from the log:

```bash
grep "^phase_margin:" run.log
```

### Logging Results

When an experiment is done, log it to `results.tsv` (tab-separated — do NOT use commas). The TSV has a header row and 5 columns:

```
commit	phase_margin_deg	specs_pass	status	description
```

- **commit** — git commit hash, short (7 chars), from `git rev-parse --short HEAD`
- **phase_margin_deg** — primary metric value (e.g. `67.300000`). Use `0.000000` for crashes.
- **specs_pass** — fraction of specs passing (e.g. `12/12`). Use `0/12` for crashes.
- **status** — `keep`, `discard`, or `crash`
- **description** — short text describing what this experiment tried (no commas, no tabs)

Example:

```
commit	phase_margin_deg	specs_pass	status	description
a1b2c3d	0.000000	0/12	crash	initial empty subckt
b2c3d4e	55.200000	10/12	keep	folded cascode PMOS input first pass
c3d4e5f	67.300000	12/12	keep	increased tail current to 20uA
d4e5f6g	61.000000	11/12	discard	switched to telescopic cascode loses swing
```

**Do not commit `results.tsv`** — leave it untracked by git. It is your personal experiment log on this instance.

---

## 4. The Experiment Loop

### Branch Setup

Work on a dedicated branch for this block:

```bash
git checkout -b autoresearch/error-amp-$(date +%b%d | tr '[:upper:]' '[:lower:]')
# e.g.: autoresearch/error-amp-mar27
```

### LOOP FOREVER

```
1. Check git state: current branch and commit
2. Form one experimental idea (topology change, sizing tweak, bias adjustment)
3. Modify design.cir directly — hack the circuit
4. git commit -m "exp: <what you tried>"
5. Run: ngspice -b run_block.sh > run.log 2>&1
6. Extract: grep "^phase_margin:\|^dc_gain_dB:\|^ugb_kHz:\|^iq_uA:\|^pvt_all_pass:" run.log
7. If grep is empty → crashed. Run: tail -n 50 run.log to read the error.
8. Log the result to results.tsv
9. If phase_margin_deg improved AND specs_pass is equal or better → KEEP (advance)
   Else → DISCARD: git reset --hard HEAD~1
10. Go to step 1
```

### Improvement Criterion

An experiment is a **keep** if:
- `phase_margin_deg` is strictly higher than the previous best, AND
- `specs_pass` does not decrease, AND
- No previously passing spec now fails.

An experiment is a **discard** if phase_margin_deg is equal or lower, or if any previously passing spec now fails.

If `specs_pass` increases (more specs now pass than before) even without primary metric improvement, that is also a **keep** — getting closer to full spec compliance is progress.

### Timeout

Each run of the full testbench suite should complete within **30 minutes**. If a run exceeds 30 minutes, kill it (`Ctrl-C` or `kill`) and treat it as a failure — discard and revert. The phase margin sweep across multiple load/corner conditions can be slow; if it is taking too long, split the PVT sweep into a separate testbench that only runs when the TT 27°C passes.

### Crashes

- **Easy fix (typo, missing `.include`, wrong net name):** Fix it, re-run. Do not log the broken attempt.
- **Convergence failure:** Tighten `.option` settings (lower `reltol`, add `gmin`). Try `.ic` initial conditions. If still failing after 3 attempts, the topology may be unworkable — discard.
- **Fundamental failure (wrong topology, circuit cannot meet spec):** Log as `crash`, revert, move on to a different idea.

### NEVER STOP

Once the experiment loop has begun, do **not** pause to ask whether to continue. Do not say "should I keep going?" The human may be asleep. Continue working indefinitely until manually interrupted.

If you run out of obvious ideas:
- Re-read `program.md` Known Challenges and think harder
- Try a completely different topology from the What to Explore list
- Try combining two approaches that each partially worked
- Try more aggressive sizing (larger W, higher bias current, longer L for better matching)
- Look at what specs are still failing and think about what circuit change directly addresses them

The loop runs until the human interrupts you, period.
