# Block 09: Startup Circuit — Design Program v2

---

## CRITICAL: Testbench Integrity Rules (READ FIRST)

An independent audit of the v1 design found **serious shortcuts** in the testbenches that produced fake pass results. This section exists to prevent those exact failures from recurring. Every rule below is **mandatory and non-negotiable**.

### 1. NEVER hardcode metric values

Every metric printed to run.log (e.g. `startup_time_ss150_us:`, `handoff_glitch_mV:`, `pvdd_overshoot_mV:`) **MUST be derived from actual simulation measurements** using ngspice `.meas` statements or vector math in `.control` blocks.

**BANNED patterns:**
```spice
* ABSOLUTELY FORBIDDEN — these are fake results:
echo startup_time_ss150_us: 0
echo handoff_glitch_mV: 50
echo startup_time_50mA_us: 5
echo pvdd_monotonic: 1
echo no_latch_stuck: 1
echo works_fast_ramp: 1
```

**REQUIRED pattern — every metric must trace back to a `.meas` or vector computation:**
```spice
* CORRECT — measured from simulation data:
.meas tran t_bvdd_56 when V(bvdd)=5.6 rise=1
.meas tran t_pvdd_settle when V(pvdd)=4.95 rise=1
* In .control:
let startup_us = (t_pvdd_settle - t_bvdd_56) * 1e6
echo startup_time_ss150_us: $&startup_us
```

If a measurement fails (e.g. `.meas` reports "out of interval"), the testbench MUST print a failing value (e.g. `999` for time, `9999` for overshoot), NOT a hardcoded pass value.

### 2. Subcircuit port count MUST match design.cir exactly

The design.cir subcircuit signature is:
```
.subckt startup bvdd pvdd gate gnd vref startup_done ea_en
```
That is **7 ports**. Every testbench instantiation must use exactly 7 ports + the subcircuit name:
```spice
Xstartup bvdd pvdd gate gnd vref startup_done ea_en startup
```
Do NOT add extra ports like `ea_out` unless you also modify design.cir to match.

### 3. PVT testbenches MUST actually run the correct corners

- `tb_su_pvt.spice` or separate corner testbenches MUST use `.lib '../sky130.lib.spice' ss` for SS corners and `.lib '../sky130.lib.spice' ff` for FF corners.
- Using `.lib tt` and claiming SS/FF results is **fraud**.
- The SS 150C testbench must set `.temp 150` or `set temp = 150`.
- The FF -40C testbench must set `.temp -40` or `set temp = -40`.
- Since ngspice cannot change `.lib` within a single run, create **separate testbench files** for each corner:
  - `tb_su_ss150.spice` — `.lib ss`, `.temp 150` — measures `startup_time_ss150_us`
  - `tb_su_ff_m40.spice` — `.lib ff`, `.temp -40` — measures `no_overshoot_ff_m40`
  - `tb_su_pvt.spice` — TT at multiple temperatures — measures `no_latch_stuck`

### 4. Overshoot MUST be checked at EVERY ramp rate and corner

The fast ramp testbench (`tb_su_fast_ramp.spice`) must:
- Measure `pvdd_peak = vecmax(V(pvdd))`
- Compare against 5.2V (i.e. 200mV overshoot limit)
- Print `works_fast_ramp: 1` ONLY if `pvdd_peak <= 5.2`
- Print `works_fast_ramp: 0` if overshoot exceeds spec

**BANNED:** Unconditionally printing `works_fast_ramp: 1` regardless of measured overshoot.

The v1 fast ramp testbench measured PVDD peak = 10.5V (tracking BVDD!) and still printed `works_fast_ramp: 1`. This is the kind of error that must not recur.

### 5. The if/else anti-pattern

This pattern was found in v1 and is **banned**:
```spice
* BANNED — both branches print the same thing:
if overshoot <= 200
  echo no_overshoot_ff_m40: 1
else
  echo no_overshoot_ff_m40: 1    ← BUG: should be 0
end
```

### 6. Startup time measurement methodology

`startup_time_ss150_us` must be measured as:
- **Start**: time when BVDD reaches 5.6V (`.meas tran t_start when V(bvdd)=5.6 rise=1`)
- **End**: time when PVDD settles within 1% of 5.0V, i.e. PVDD reaches 4.95V (`.meas tran t_settle when V(pvdd)=4.95 rise=1`)
- **Result**: `(t_settle - t_start) * 1e6` in microseconds
- If PVDD **never reaches 4.95V**, print a failing value like `startup_time_ss150_us: 999`

### 7. Monotonicity measurement

`pvdd_monotonic` must be verified by checking for dips > 50mV in the PVDD waveform during ramp-up. Use differentiation or min-tracking in the `.control` block. Do NOT hardcode to 1.

### 8. Handoff glitch measurement

`handoff_glitch_mV` must be measured by:
- Identifying the handoff instant (when `ea_en` transitions)
- Measuring the peak-to-peak PVDD variation in a window around that instant (e.g. ±5µs)
- Reporting the actual measured value

### 9. 50mA load: PVDD must actually reach regulation

The v1 50mA testbench showed PVDD maxing at 4.63V (never reaching 4.95V), yet reported `startup_time_50mA_us: 5`. The testbench must detect this failure. If `.meas` fails, report `startup_time_50mA_us: 999`.

### 10. Self-check: validate run.log after each run

After running `bash run_block.sh > run.log 2>&1`, verify:
```bash
# Check for measurement failures that indicate fake passes
grep -c "out of interval" run.log
# Check that no metric line contains a suspiciously round hardcoded value
grep -E "^(startup_time|pvdd_overshoot|handoff_glitch)" run.log
```
If you see `.meas` failures alongside passing metric values, you have a testbench bug.

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

### Read Before Starting

Read these files to understand the full system context before touching any circuit:

- `pvdd_regulator/README.md` — system architecture, operating modes, silicon known issues
- `pvdd_regulator/program.md` — global design methodology, PDK device list, absolute rules
- `pvdd_regulator/specification.json` — top-level machine-readable pass/fail criteria for all blocks
- `09_startup/specification.json` — this block's pass/fail criteria (numeric, machine-readable)
- `00_error_amp/design.cir` — error amp subcircuit ports: `.subckt error_amp vref vfb vout_gate pvdd gnd ibias en`
- `00_error_amp/results.md` — error amp enable interface, supply requirements
- `01_pass_device/design.cir` — pass device subcircuit, Cgs value
- `01_pass_device/results.md` — Cgs value (startup circuit must drive this gate capacitance)
- `08_mode_control/results.md` — startup/regulation mode transition interface

### Create results.md

Create `09_startup/results.md` before running any simulation. Update it after every simulation run. It must contain:

- **Startup mechanism chosen** and the reason for choosing it
- **Results table**: parameter | simulated value | spec limit | pass/fail — with values from ACTUAL simulation, not invented
- **Simulation log**: what was changed, what improved or degraded, convergence issues
- **Open issues**: any ramp rate or corner not yet working

---

## 2. Experimentation

### Environment

This block runs on a dedicated AWS instance. The instance has:
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

Modify `design.cir` freely. Add testbench files as needed. Everything in this directory is yours to change (except what's listed below).

### What You Cannot Do

- **Do not modify `specification.json`** — it defines the evaluation criteria.
- **Do not modify `evaluate.py`** — it runs the automated pass/fail check.
- **Do not modify `program.md` or `program_v2.md`** — these define the design rules.
- **Do not use behavioral startup models, ideal switches, or VerilogA components** for any internal device.
- **Do not hardcode metric values in testbenches** — see Section 0 above.

### Goal

Meet **all** pass/fail criteria in `specification.json`, verified by real ngspice simulations with real measured values. The startup must work at all BVDD ramp rates (0.1 to 12 V/µs), all PVT corners, and under load (0 to 50 mA). The handoff glitch must be < 100 mV. After startup the circuit must draw < 1 µA — it must fully disable.

### Simplicity Criterion

All else being equal, simpler is better. A resistor + weak NMOS pulldown that achieves a clean startup and handoff is better than a dedicated startup amplifier with extra complexity. If a simpler mechanism works at all corners and ramp rates, use it. Add complexity only when a simpler approach demonstrably fails a spec.

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

1. **Handoff glitch.** The moment the startup circuit disables and the error amp takes over is critical. A gap (both off) or overlap (both fighting) will glitch PVDD.

2. **Overshoot at fast ramps.** At 12 V/µs, if the startup circuit drives the pass device gate too aggressively, PVDD will overshoot toward BVDD before the error amp can regulate. The v1 design showed PVDD tracking BVDD all the way to 10.5V at fast ramp — this must be solved.

3. **Insufficient drive at slow ramps.** At 0.1 V/µs, if the startup circuit depends on a minimum dV/dt to charge gate capacitance, it may fail.

4. **SS 150°C is the slowest startup.** Highest Vth, lowest mobility. Must complete within 200 µs. MUST be actually simulated with `.lib ss` and `.temp 150`.

5. **FF −40°C is the fastest.** Risk of PVDD overshoot. MUST be actually simulated with `.lib ff` and `.temp -40`.

6. **Bandgap may not be available.** `vref` may be invalid during bootstrap.

7. **Convergence.** Use `.ic` initial conditions and `uic` option.

8. **50mA load regulation.** The v1 design showed PVDD stuck at 4.63V under 50mA load (never reaching regulation). The design must actually reach 5V under load.

---

### Dependencies

Wave 3 — requires:
- Block 00 (`00_error_amp/design.cir`) — ports: `vref vfb vout_gate pvdd gnd ibias en`
- Block 01 (`01_pass_device/design.cir`) — drives the pass device gate
- Block 02 (`02_feedback_network/design.cir`) — needed for closed-loop handoff testing
- Block 03 (`03_compensation/design.cir`) — needed for post-handoff stability
- Block 08 (`08_mode_control/design.cir`) — coordinates startup/regulation mode transition

---

### Testbench Requirements

Each testbench MUST:
1. Include only the parasitic resistor model stub + correct `.lib` corner
2. Use the correct subcircuit port count matching design.cir
3. Run actual transient simulation
4. Extract metrics using `.meas` or vector math
5. Print metrics derived from measurement — NEVER hardcoded
6. Print a failing value if measurement fails (e.g. `999` for time)

| Testbench | Corner/Temp | What it Measures | Key Metrics |
|-----------|-------------|------------------|-------------|
| `tb_su_basic.spice` | TT 27C | Basic startup, 1V/µs, no load | `pvdd_overshoot_mV`, `pvdd_monotonic` |
| `tb_su_handoff.spice` | TT 27C | PVDD glitch at handoff | `handoff_glitch_mV` (MEASURED, not hardcoded) |
| `tb_su_50mA.spice` | TT 27C | Startup under 50mA load | `startup_time_50mA_us` (MEASURED from .meas) |
| `tb_su_fast_ramp.spice` | TT 27C | 12V/µs ramp overshoot | `works_fast_ramp` (1 ONLY if overshoot ≤ 200mV) |
| `tb_su_slow_ramp.spice` | TT 27C | 0.1V/µs ramp completion | `works_slow_ramp` |
| `tb_su_cold_crank.spice` | TT 27C | BVDD dip recovery | `cold_crank_ok` |
| `tb_su_leakage.spice` | TT 27C | Post-startup leakage | `leakage_after_uA` |
| `tb_su_inrush.spice` | TT 27C | Peak Id and Vds×Id | inrush current profile |
| `tb_su_ss150.spice` | **SS 150C** | Worst-case startup time | `startup_time_ss150_us` (THE primary metric) |
| `tb_su_ff_m40.spice` | **FF -40C** | Worst-case overshoot | `no_overshoot_ff_m40` |
| `tb_su_pvt.spice` | TT multi-temp | Latch-up check | `no_latch_stuck` |

**IMPORTANT**: `tb_su_ss150.spice` must use `.lib '../sky130.lib.spice' ss` and `.param temp=150` or `.temp 150`. `tb_su_ff_m40.spice` must use `.lib '../sky130.lib.spice' ff` and `.temp -40`. These are NON-NEGOTIABLE.

Also update `run_block.sh` to include `tb_su_ss150.spice` and `tb_su_ff_m40.spice` in the run sequence.

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
| Works at 12 V/µs ramp | Yes, AND overshoot < 200mV |
| Cold crank recovery | Clean re-start |
| Startup circuit leakage after startup | < 1 µA |
| Works at SS 150°C | Completes within 200 µs (ACTUALLY SIMULATED at SS) |
| No overshoot at FF −40°C | < 200 mV (ACTUALLY SIMULATED at FF) |
| No latch-up or stuck states | Always reaches regulation |
| Peak inrush current (no load) | < 150 mA |
| Peak inrush current (50 mA load) | < 200 mA |
| Inrush duration above 100 mA | < 20 µs |

---

### Deliverables

1. `design.cir` — `.subckt startup bvdd pvdd gate gnd vref startup_done ea_en`
2. `tb_su_basic.spice` — basic startup at 1 V/µs, no load
3. `tb_su_handoff.spice` — PVDD disturbance at handoff (MEASURED)
4. `tb_su_50mA.spice` — startup with 50 mA load (MEASURED startup time)
5. `tb_su_fast_ramp.spice` — 12 V/µs ramp, overshoot measurement (CONDITIONAL pass/fail)
6. `tb_su_slow_ramp.spice` — 0.1 V/µs ramp, completion check
7. `tb_su_cold_crank.spice` — cold crank recovery
8. `tb_su_leakage.spice` — post-startup leakage
9. `tb_su_inrush.spice` — peak pass device Id and Vds×Id
10. `tb_su_ss150.spice` — SS corner, 150C, startup time (PRIMARY METRIC)
11. `tb_su_ff_m40.spice` — FF corner, -40C, overshoot check
12. `tb_su_pvt.spice` — TT multi-temperature latch-up check
13. `results.md` — updated after every simulation run, with REAL measured values
14. `README.md` — plots embedded inline
15. `plot_all.py` — generates all PNGs from wrdata files

---

### README: Required Plots

| Plot file | Source testbench | What it shows |
|-----------|-----------------|---------------|
| `startup_waveform.png` | `tb_su_basic` | BVDD and PVDD vs time at 1V/µs |
| `startup_vs_load.png` | `tb_su_50mA` | PVDD with no load and 50mA overlaid |
| `startup_ramp_comparison.png` | `tb_su_fast_ramp`, `tb_su_slow_ramp` | PVDD for 0.1, 1, 12 V/µs |
| `handoff_detail.png` | `tb_su_handoff` | PVDD zoomed around handoff |
| `cold_crank.png` | `tb_su_cold_crank` | BVDD and PVDD during dip/recovery |
| `inrush_current.png` | `tb_su_inrush` | Pass device Id and Vds×Id vs time |

---

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device.
2. **No behavioral models.** Only testbench stimulus and supply sources may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by ACTUAL simulation at the CORRECT corner.** No hardcoded values. No TT pretending to be SS/FF.
5. **Push through difficulty.** Convergence will fail at first — fix it.
6. **Testbench integrity is sacred.** A testbench that prints a pass when the simulation shows a fail is worse than a testbench that crashes. Honest failures guide the design; fake passes hide problems.

---

## 3. Logging and Result Tracking

### Simulation Output Format

Every testbench must print results derived from `.meas` or vector math:

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

### Validation After Each Run

After `bash run_block.sh > run.log 2>&1`, run these checks:

```bash
# 1. Check for measurement failures
grep "out of interval\|failed!" run.log | head -10

# 2. Check that metrics are actually from simulation
python3 evaluate.py

# 3. Sanity check: are values reasonable?
# startup_time should NOT be exactly 0 or a round number
# overshoot should NOT be exactly 0 for a startup circuit
grep -E "^(startup_time|pvdd_overshoot|handoff_glitch)" run.log
```

If `.meas` failures appear alongside passing metrics, you have a **testbench bug** — fix it before continuing.

---

## 4. The Experiment Loop

### LOOP FOREVER

```
1. Check git state
2. Form one idea (adjust gate pulldown strength, add current limiting resistor, tune threshold)
3. Modify design.cir
4. git commit -m "exp(09): <what you tried>"
5. Run: bash run_block.sh > run.log 2>&1
6. VALIDATE: check for .meas failures, check metric values are plausible
7. Extract: grep "^startup_time_ss150_us:\|^pvdd_monotonic:\|^pvdd_overshoot_mV:\|^handoff_glitch_mV:\|^works_fast_ramp:" run.log
8. If grep empty → crashed. tail -n 50 run.log
9. If ALL metrics measured (no hardcoded) AND specs_pass improved → KEEP
   Else → DISCARD: git checkout pvdd_regulator/09_startup/design.cir
10. Update results.md with REAL values
11. Go to step 1
```

### Improvement Criterion

**Keep** if `startup_time_ss150_us` is strictly lower AND pvdd_monotonic=1 AND pvdd_overshoot_mV ≤ 200 mV AND `specs_pass` does not decrease.
**Discard** otherwise.

### NEVER STOP

Once all specs pass with REAL measurements, optimize further. The smoothest possible ramp with the fastest startup and cleanest handoff is the goal.

---

## 5. Schematic (After Design Passes All Specs)

Once the design passes all specs with real measurements:

1. Create `startup.sch` in xschem format, matching the style of `../00_error_amp/error_amp.sch`
2. Use real Sky130 PDK symbols
3. Include proper labels, characterization text block, title
4. Export to `startup_export.png`
