# Block 09: Startup Circuit — Design Program

---

## 1. Setup

### Purpose

The startup circuit solves the fundamental bootstrap problem of the PVDD LDO:

**The chicken-and-egg problem:**
1. The error amplifier runs from PVDD (5V).
2. PVDD is produced by the pass device, controlled by the error amplifier.
3. At power-on, PVDD = 0V, so the error amp has no supply.
4. With no error amp, the pass device gate is floating or held off — PVDD stays at 0V.
5. Deadlock: the LDO never starts.

The startup circuit forces PVDD to begin charging without the error amplifier, then hands off to the main regulation loop once PVDD is established. After handoff, the startup circuit must fully disable — any residual current or gate interference will degrade regulation.

Additional requirements: handle cold crank (BVDD drops below PVDD then recovers), work at all BVDD ramp rates from 0.1 to 12 V/µs, produce a monotonic PVDD ramp with no dips, and make a glitch-free handoff to the error amplifier.

This is the last block to be fully verified because it requires the complete regulation loop. However, the startup mechanism itself can be designed and partially tested standalone.

### Read Before Starting

Read these files to understand the full system context before touching any circuit:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `09_startup/specification.json` — this block's pass/fail criteria (numeric, machine-readable)
- `00_error_amp/results.md` — error amp enable interface, supply requirements
- `01_pass_device/results.md` — Cgs value (startup circuit must drive this gate capacitance)
- `08_mode_control/results.md` — startup/regulation mode transition interface

### Create results.md

Create `09_startup/results.md` before running any simulation. Update it after every simulation run. It must contain:

- **Startup mechanism chosen** and the reason for choosing it
- **Results table**: parameter | simulated value | spec limit | pass/fail
- **Simulation log**: what was changed, what improved or degraded, convergence issues
- **Open issues**: any ramp rate or corner not yet working

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance configured for this block only. The instance has:
- Full SkyWater SKY130A PDK installed
- ngspice installed and tested
- This block directory (`09_startup/`) as the working directory
- All other block `design.cir` files available via `.include`

### What You Can Do

You are free to choose any startup mechanism that solves the bootstrap problem. Options to consider:

- **Current-limited gate pulldown.** A weak NMOS (or NMOS + series resistor) pulls the pass device gate toward GND, partially turning on the PMOS pass device. PVDD charges through the pass device. When PVDD crosses a threshold, the pulldown disables and the error amp takes over. Simple and self-limiting.

- **Bootstrap resistor from BVDD.** A resistor from BVDD to the error amp supply provides trickle current to power the error amp directly from BVDD before PVDD is established. Simple, but wastes current permanently unless a switch disconnects it after startup.

- **Dedicated startup amplifier.** A simple, low-power amp built from HV devices that operates directly from BVDD (no PVDD needed). Provides coarse regulation during startup, then hands off to the precision error amp. Most robust but most complex.

- **Current source from BVDD.** A BVDD-powered current source that charges PVDD through the pass device or through a diode. Self-disables when PVDD reaches target.

- **Any combination** of the above.

**Key design constraint:** `vref` (1.226V from bandgap) may not be valid during the startup phase because PVDD (which often powers the bandgap) may not yet be established. The startup circuit must not depend on accurate `vref` during bootstrapping. Use BVDD-derived thresholds or Vth-based detection for the startup sensing.

**Convergence:** Startup simulations are notoriously difficult for SPICE convergence because all nodes start at zero. Use `.ic` (initial conditions) and the `uic` option. Set `.option` to aggressive tolerances. Do not give up on the real circuit because of convergence — fix it.

Modify `design.cir` freely. Add testbench files as needed. Everything in this directory is yours to change.

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria. The evaluator reads it.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md`** — this file defines the design rules.
- **Do not use behavioral startup models, ideal switches that magically bootstrap the supply, or any VerilogA components** for any internal device.

### Goal

Meet **all** pass/fail criteria in `specification.json`, verified by real ngspice simulations. The startup must work at all BVDD ramp rates (0.1 to 12 V/µs), all PVT corners, and under load (0 to 50 mA). The handoff glitch must be < 100 mV. After startup the circuit must draw < 1 µA — it must fully disable.

### Simplicity Criterion

All else being equal, simpler is better. A resistor + weak NMOS pulldown that achieves a clean startup and handoff is better than a dedicated startup amplifier with extra complexity. If a simpler mechanism works at all corners and ramp rates, use it. Add complexity only when a simpler approach demonstrably fails a spec.

---

### Optimization

Use `optimize.py` to find startup resistor and NMOS sizing that minimizes startup time while keeping PVDD undershoot at handoff within spec.

**Framework (scipy):**

```python
from scipy.optimize import differential_evolution, minimize
import subprocess, re

def cost(params):
    # Write Rstart, Wn_startup into design.cir via .param substitution
    # subprocess.run(['ngspice', '-b', 'run_block.sh'], capture_output=True)
    # Parse t_startup_us, pvdd_undershoot_mV from run.log
    # Return t_startup_us + undershoot_penalty + inrush_penalty
    pass

result = differential_evolution(cost, bounds=[(10e3, 1e6), (1e-6, 20e-6)], maxiter=100, seed=42)
result = minimize(cost, result.x, method='Nelder-Mead', options={'xatol': 100, 'fatol': 0.1})
```

**Variables:** startup bias resistor Rstart (10 kΩ–1 MΩ), startup NMOS pull-down width Wn (1–20 µm).

**Objective:** minimize startup time `t_startup_us` (time for PVDD to reach 4.9V from 0) at SS 150°C, slowest ramp rate.

**Constraints (penalty if violated):**
- Startup < 100 µs at all ramp rates (0.1, 1, 12 V/µs) and loads (0, 50 mA)
- PVDD undershoot at handoff < 50 mV
- No re-entry into startup mode after handoff (monotonic PVDD)
- Peak inrush current < 150 mA (no load), < 200 mA (50 mA load)
- Inrush duration > 100 mA < 20 µs
- Pass device Vds × Id within SOA at peak stress (cross-reference Block 01 SOA)

**Commit strategy:** commit per-block only. Keep if `t_startup_us` decreases and all constraints pass:
```bash
git add pvdd_regulator/09_startup/ && git commit -m "exp(09): <what changed>"
```
Regress → `git checkout pvdd_regulator/09_startup/design.cir`.

---

### Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Input | 0–10.5V | Battery supply (energy source for bootstrap) |
| `pvdd` | Output/Sense | 0–5V during startup | PVDD rail being bootstrapped |
| `gate` | Output | 0–BVDD | Pass device gate node |
| `gnd` | Supply | 0V | Ground |
| `vref` | Input | 1.226V | Bandgap reference (may not be valid during startup) |
| `startup_done` | Output | Digital | Startup complete flag |
| `ea_en` | Output | Digital | Error amplifier enable |

Subcircuit signature: `.subckt startup bvdd pvdd gate gnd vref startup_done ea_en`

**Connections in the LDO:**
- `gate` connects to the same node as the error amp output. During startup, the startup circuit drives the gate. After startup, the error amp takes over and the startup circuit releases.
- `pvdd` is both an output (being charged) and a sense input (monitoring the ramp).
- `startup_done` and `ea_en` connect to mode control (Block 08).

---

### Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Startup time (BVDD=7V, no load) | — | — | 100 | µs | From BVDD reaching 5.6V to PVDD within 1% |
| Startup time (BVDD=7V, 50 mA load) | — | — | 200 | µs | Worst case: heavy load |
| PVDD ramp monotonicity | Yes | — | — | — | No dips > 50 mV |
| PVDD overshoot | — | — | 200 | mV | Max overshoot above 5.0V |
| Handoff glitch | — | — | 100 | mV | PVDD disturbance at switchover |
| BVDD ramp rate tolerance | 0.1 | — | 12 | V/µs | All rates |
| Quiescent current after startup | — | — | 1 | µA | Must fully disable |
| Cold crank recovery | Yes | — | — | — | Clean re-start after BVDD dip |
| Temperature range | −40 | 27 | 150 | °C | |

---

### Operating Conditions

- **BVDD ramp profiles:**
  - Normal: 0 → 10.5V at 1 V/µs
  - Fast: 0 → 10.5V at 12 V/µs (cold-crank recovery)
  - Slow: 0 → 10.5V at 0.1 V/µs (gradual battery connect)
  - Cold crank: 10.5V → 3V → 7V (dip and recovery)
- **Load during startup:** 0 mA (best case) to 50 mA (worst case)
- **Corners:** SS/TT/FF/SF/FS at −40°C, 27°C, 150°C

---

### Known Challenges

1. **Handoff glitch.** The moment the startup circuit disables and the error amp takes over is critical. A gap (both off) or overlap (both fighting) will glitch PVDD. The handoff mechanism must be smooth.

2. **Overshoot at fast ramps.** At 12 V/µs, if the startup circuit drives the pass device gate too aggressively, PVDD will overshoot toward BVDD before the error amp can regulate. Control the drive strength.

3. **Insufficient drive at slow ramps.** At 0.1 V/µs, if the startup circuit depends on a minimum dV/dt to charge gate capacitance, it may fail. Verify startup completes at this rate.

4. **SS 150°C is the slowest startup.** Highest Vth, lowest mobility. Must complete within 200 µs.

5. **FF −40°C is the fastest.** Risk of PVDD overshoot. Lowest Vth, highest mobility — the startup pulldown may be too aggressive.

6. **Bandgap may not be available.** `vref` may be invalid during bootstrap. Do not use it for startup threshold detection.

7. **Convergence.** Use `.ic` initial conditions and `uic` option. Multiple nodes transition from zero simultaneously.

---

### Dependencies

Wave 3 — requires:
- Block 00 (`00_error_amp/design.cir`) — must hand off control to the error amp
- Block 01 (`01_pass_device/design.cir`) — drives the pass device gate (need Cgs)
- Block 02 (`02_feedback_network/design.cir`) — needed for closed-loop handoff testing
- Block 03 (`03_compensation/design.cir`) — needed for post-handoff stability
- Block 08 (`08_mode_control/design.cir`) — coordinates startup/regulation mode transition

---

### Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| Basic startup (BVDD ramp, no load) | PVDD ramp waveform, startup time |
| Startup with error amp handoff | PVDD glitch at handoff point |
| Startup with 50 mA load | Startup time under worst-case load |
| Fast BVDD ramp (12 V/µs) | PVDD overshoot |
| Slow BVDD ramp (0.1 V/µs) | Verify startup still completes |
| Cold crank recovery | BVDD dip and recovery profile |
| Startup circuit disable verification | Leakage after startup |
| Inrush current characterization | Peak pass device current during startup at BVDD=5.4V, 7V, 10.5V; at Iload=0 and 50mA |
| PVT corners | Startup at SS/FF/SF/FS, −40/27/150°C |

---

### Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Startup time (no load, BVDD=7V) | < 100 µs |
| Startup time (50 mA load, BVDD=7V) | < 200 µs |
| PVDD ramp monotonicity | No dips > 50 mV |
| PVDD overshoot | < 200 mV above 5.0V |
| Handoff glitch | < 100 mV disturbance |
| Works at 0.1 V/µs ramp | Yes |
| Works at 12 V/µs ramp | Yes |
| Cold crank recovery | Clean re-start |
| Startup circuit leakage after startup | < 1 µA |
| Works at SS 150°C | Completes within 200 µs |
| No overshoot at FF −40°C | < 200 mV |
| No latch-up or stuck states | Always reaches regulation |
| Peak inrush current (no load) | < 150 mA — device must remain in SOA |
| Peak inrush current (50 mA load) | < 200 mA absolute limit |
| Inrush duration above 100 mA | < 20 µs — limits thermal energy in pass device |

**Inrush note:** During startup, the pass device simultaneously sees high Vds (BVDD before PVDD establishes) and high Id (charging Cload plus load current). The Vds×Id product at this instant sets instantaneous power dissipation — must stay within the SOA envelope characterized in Block 01.

---

### Deliverables

1. `design.cir` — `.subckt startup bvdd pvdd gate gnd vref startup_done ea_en`
2. `tb_su_basic.spice` — basic startup at 1 V/µs, no load
3. `tb_su_handoff.spice` — PVDD disturbance at handoff
4. `tb_su_50mA.spice` — startup with 50 mA load
5. `tb_su_fast_ramp.spice` — 12 V/µs ramp, overshoot measurement
6. `tb_su_slow_ramp.spice` — 0.1 V/µs ramp, completion check
7. `tb_su_cold_crank.spice` — cold crank recovery
8. `tb_su_leakage.spice` — post-startup leakage
9. `tb_su_inrush.spice` — measure peak pass device Id and Vds×Id during startup at BVDD=5.4V, 7V, 10.5V with Iload=0 and 50mA; plot instantaneous power vs time; verify against Block 01 SOA boundary
10. `tb_su_pvt.spice` — all criteria at all PVT corners
11. `results.md` — updated after every simulation run
12. `README.md` — the visual window to this block: mechanism description, handoff details, and every plot listed below embedded inline

---

### README: Required Plots

The `README.md` is the visual window to this block. The startup waveform is the story — every reader must see PVDD going from zero to regulation cleanly.

**Mechanism:** Testbenches save data with `.wrdata`. Run `python3 plot_all.py` to generate all PNGs. Embed with `![description](filename.png)`.

**Plots required in README.md:**

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `startup_waveform.png` | `tb_su_basic` | BVDD and PVDD vs time at 1V/µs — shows monotonic ramp to 5V |
| `startup_vs_load.png` | `tb_su_50mA` | PVDD startup with no load and 50mA load overlaid — shows slower ramp under load |
| `startup_ramp_comparison.png` | `tb_su_fast_ramp`, `tb_su_slow_ramp` | PVDD for 0.1, 1, and 12 V/µs BVDD ramps overlaid |
| `handoff_detail.png` | `tb_su_handoff` | PVDD zoomed around handoff instant — shows glitch magnitude |
| `cold_crank.png` | `tb_su_cold_crank` | BVDD and PVDD vs time during 10.5V→3V→7V dip and recovery |
| `inrush_current.png` | `tb_su_inrush` | Pass device Id and instantaneous power (Vds×Id) vs time — overlaid with SOA limit line |

---

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device. No behavioral startup models or ideal switches that magically bootstrap the supply.
2. **No behavioral models.** Only testbench stimulus and supply sources may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** The startup is fundamentally a chicken-and-egg problem. It is solvable with real circuits. Convergence will fail at first — fix it with `.ic` and `.option`, not by replacing the circuit.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench must print results in this exact format:

```
startup_time_ss150_us: 78.4
startup_time_50mA_us: 143.2
pvdd_monotonic: 1
pvdd_overshoot_mV: 112.0
handoff_glitch_mV: 38.0
works_slow_ramp: 1
works_fast_ramp: 1
cold_crank_ok: 1
leakage_after_uA: 0.04
no_overshoot_ff_m40: 1
no_latch_stuck: 1
```

`startup_time_ss150_us` = time from BVDD reaching 5.6V to PVDD settling within 1% of 5.0V, at SS 150°C, no load.

### The specs.tsc File

`specs.tsc` defines all tracked metrics and pass/fail thresholds.

The **primary metric** is `startup_time_ss150_us` — worst-case startup time. Lower is better. Minimize it while maintaining monotonic ramp, < 200 mV overshoot, and clean handoff.

### Summary Printed After Each Run

```
---
startup_time_ss150_us:  78.4  us   (spec <= 100)  PASS
startup_time_50mA_us:  143.2  us   (spec <= 200)  PASS
pvdd_monotonic:          1    bool  (spec = 1)     PASS
pvdd_overshoot_mV:     112.0  mV   (spec <= 200)  PASS
handoff_glitch_mV:      38.0  mV   (spec <= 100)  PASS
leakage_after_uA:        0.04 uA   (spec <= 1)    PASS
specs_pass:             11/12
```

Extract the primary metric:

```bash
grep "^startup_time_ss150_us:" run.log
```

### Logging Results

Log to `results.tsv` (tab-separated):

```
commit	startup_time_ss150_us	specs_pass	status	description
```

Example:

```
commit	startup_time_ss150_us	specs_pass	status	description
a1b2c3d	0.000000	0/12	crash	initial stub PVDD never rises
b2c3d4e	0.000000	0/12	crash	gate pulldown too weak no charging
c3d4e5f	143.000000	10/12	discard	works but overshoot 280mV FF -40C fails
d4e5f6g	78.400000	12/12	keep	series resistor limits fast ramp overshoot
```

**Do not commit `results.tsv`.**

---

## 4. The Experiment Loop

### Branch Setup

```bash
git checkout -b autoresearch/startup-$(date +%b%d | tr '[:upper:]' '[:lower:]')
```

### LOOP FOREVER

```
1. Check git state
2. Form one idea (adjust gate pulldown strength, add current limiting resistor, tune threshold)
3. Modify design.cir
4. git commit -m "exp: <what you tried>"
5. Run: ngspice -b run_block.sh > run.log 2>&1
6. Extract: grep "^startup_time_ss150_us:\|^pvdd_monotonic:\|^pvdd_overshoot_mV:\|^handoff_glitch_mV:\|^works_fast_ramp:" run.log
7. If grep empty → crashed. tail -n 50 run.log
8. Log to results.tsv
9. If startup_time_ss150_us improved AND pvdd_monotonic=1 AND pvdd_overshoot_mV <= 200 AND specs_pass equal or better → KEEP
   Else → DISCARD: git reset --hard HEAD~1
10. Go to step 1
```

### Improvement Criterion

**Keep** if `startup_time_ss150_us` is strictly lower AND pvdd_monotonic=1 AND pvdd_overshoot_mV ≤ 200 mV AND `specs_pass` does not decrease.
**Discard** otherwise. A faster startup that overshoots or produces a non-monotonic ramp is worse, not better.

### Timeout

Startup simulations with full closed loop are slow. Allow **45 minutes** per full run. Run standalone gate pulldown test first (no error amp, 5 minutes) to verify basic operation, then add the full closed loop.

### Crashes

Startup simulations from zero initial conditions are the most convergence-difficult runs in the entire project. Use `.ic V(pvdd)=0 V(gate)=0 V(bvdd)=0` and the `uic` flag. Add `.option gmin=1e-10 abstol=1e-13`. If still failing, try a larger initial BVDD step.

### NEVER STOP

Once all 12 specs pass, try to reduce startup time further by increasing the gate pulldown strength — but watch the overshoot. Try to reduce leakage_after_uA (the circuit must fully disable). Try to eliminate the handoff glitch entirely. The smoothest possible ramp with the fastest startup and cleanest handoff is the goal. Simpler is better — fewer devices in the startup path means fewer things that can go wrong.
