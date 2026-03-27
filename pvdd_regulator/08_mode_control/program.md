# Block 08: Mode Control — Design Program

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor, resistor, and comparator must be an instantiated Sky130 device. No behavioral state machines, no Verilog models.
2. **No behavioral models.** Only testbench stimulus and supply sources may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** Analog state machines with multiple thresholds and hysteresis are complex. Build incrementally and test each comparator before combining.

---

## Purpose

The mode control manages the PVDD regulator's operating mode based on the BVDD input voltage. It implements five operating modes:

| # | Mode | BVDD Range | PVDD Output | Max Load | Description |
|---|------|-----------|-------------|----------|-------------|
| 1 | POR | 0 - 2.5V | OFF | -- | Everything disabled |
| 2 | Retention bypass | 2.5 - 4.2V | BVDD | 0.5 mA | Pass device fully ON, PVDD tracks BVDD |
| 3 | Retention regulate | 4.2 - 4.5V | 4.1V | 0.5 mA | Regulates to 4.1V target |
| 4 | Power-up bypass | 4.5 - 5.0V | BVDD | 10 mA | Bypass for bridge startup |
| 5 | Active regulate | > 5.6V | 5.0V | 50 mA | Full regulation |

**Mode transitions are triggered by BVDD crossing voltage thresholds.** The mode control generates output signals that configure the rest of the LDO:
- `bypass_en`: Shorts the pass device gate to GND (fully ON) for bypass modes.
- `ea_en`: Enables the error amplifier for regulation modes.
- `ref_sel`: Selects between 4.1V and 5.0V regulation targets.
- `uvov_en`: Enables UV/OV comparators (only in active mode).
- `ilim_en`: Enables current limiter.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Input (sense) | 0-10.5V | Battery supply being monitored |
| `pvdd` | Supply | 5.0V (when available) | Regulated supply |
| `svdd` | Supply | 2.2V | Low-voltage digital supply |
| `gnd` | Supply | 0V | Ground |
| `vref` | Input | 1.226V | Bandgap reference |
| `en_ret` | Input | SVDD domain | Retention mode enable |
| `bypass_en` | Output | BVDD domain | Pass device bypass control |
| `ea_en` | Output | PVDD domain | Error amplifier enable |
| `ref_sel` | Output | PVDD domain | Reference select (0=5.0V, 1=4.1V) |
| `uvov_en` | Output | PVDD domain | UV/OV comparator enable |
| `ilim_en` | Output | PVDD domain | Current limiter enable |
| `mode[1:0]` | Output | SVDD domain | Mode status |

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| BVDD threshold: POR -> retention bypass | 2.3 | 2.5 | 2.7 | V | Hysteresis: 200 mV |
| BVDD threshold: ret bypass -> ret regulate | 4.0 | 4.2 | 4.4 | V | Hysteresis: 200 mV |
| BVDD threshold: ret regulate -> PU bypass | 4.3 | 4.5 | 4.7 | V | Hysteresis: 200 mV |
| BVDD threshold: PU bypass -> active | 5.4 | 5.6 | 5.8 | V | Hysteresis: 200 mV |
| Comparator response time | -- | -- | 5 | us | Per threshold |
| Glitch-free transitions | Yes | -- | -- | -- | No glitches during mode changes |
| Quiescent current (POR mode) | -- | -- | 1 | uA | Nearly zero |
| Quiescent current (active mode) | -- | -- | 20 | uA | From BVDD |
| BVDD ramp rate tolerance | 0.1 | -- | 12 | V/us | Slow and fast ramps |
| Temperature range | -40 | 27 | 150 | C | |

---

## Operating Conditions

- **BVDD:** Ramps from 0 to 10.5V (power-up) and back to 0 (power-down).
- **Ramp rates:** 0.1 V/us to 12 V/us.
- **Temperature:** -40C to 150C.
- **Corners:** SS/TT/FF/SF/FS.

---

## Known Challenges

1. **Four thresholds must form a monotonic sequence.** As BVDD ramps up, the comparators must assert in order: POR, RET, PUP, ACT. If threshold tolerances overlap between adjacent comparators, the mode state machine can enter an invalid state.

2. **Self-powering problem.** At BVDD < 2.5V (POR mode), the mode control itself may not have enough supply to function. The design must either operate from BVDD directly (using HV devices with very low supply capability) or use a minimal bootstrap.

3. **Glitch-free transitions.** When a threshold is crossed, the output signals must change atomically. Race conditions between comparators or logic gates can produce glitches on bypass_en, ea_en, etc., which could cause PVDD spikes or dips.

4. **Hysteresis accuracy.** Each comparator needs ~200 mV hysteresis at the BVDD level. Too little causes chattering. Too much delays mode transitions.

5. **Power consumption.** Four dividers + four comparators + logic. At ~5 uA per divider and ~2 uA per comparator, total is ~28 uA. Must stay under 20 uA.

---

## What to Explore

The agent is free to choose any implementation that meets the specs. The overall structure requires BVDD threshold detection and combinational logic, but the specific circuits are up to the agent.

**Threshold detection options:**
- Four independent comparators, each with its own resistive divider comparing to V_REF.
- A single resistor ladder with multiple tap points feeding multiple comparators.
- Current-mode threshold detection (BVDD drives a resistor, compare the current to reference currents).
- Window comparator structures that inherently produce monotonic outputs.

**Logic implementation options:**
- CMOS gates built from HV devices.
- Pass-transistor logic.
- Current-steering logic (lower power).
- Simple SR latches with comparator outputs.

**Bypass switch options:**
- Large NMOS pulling the pass device gate to GND.
- Transmission gate shorting gate to source (BVDD).
- Direct connection through the mode control output.

**The truth table is fixed (see Purpose section). The implementation is up to the agent.**

---

## Dependencies

**Wave 3 block -- requires:**
- Block 06 (level shifter) -- for translating SVDD-domain enable signals to BVDD domain
- Knowledge of Block 00 (error amp) enable interface
- Knowledge of Block 01 (pass device) gate capacitance for bypass switch sizing

Can be partially designed and tested standalone (comparators and logic), but full integration requires the level shifter and downstream block enable interfaces.

---

## Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| Full mode transition sequence | BVDD ramp 0 -> 10.5V, monitor all outputs |
| Fast ramp (12 V/us) | Clean transitions, no glitches |
| Slow ramp (0.1 V/us) | Clean transitions |
| Power-down (reverse) | BVDD 10.5V -> 0, verify reverse transitions with hysteresis |
| Individual thresholds | Each comparator trip point |
| Hysteresis | Up/down thresholds for each comparator |
| PVT corners | Thresholds at SS/FF/SF/FS, -40/27/150C |
| Glitch detection | Monitor all outputs for spurious transitions |

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| POR threshold | 2.5V +/- 0.2V |
| Retention threshold | 4.2V +/- 0.2V |
| Power-up threshold | 4.5V +/- 0.2V |
| Active threshold | 5.6V +/- 0.2V |
| Hysteresis (all comparators) | 150-250 mV |
| Monotonic thermometer code | No out-of-order assertions |
| Glitch-free outputs | No intermediate states |
| Works at 12 V/us ramp | Clean transitions |
| Works at 0.1 V/us ramp | Clean transitions |
| Thresholds across PVT | Within +/-15% of nominal |
| Quiescent current (active) | < 20 uA from BVDD |
| Power-down reverse transitions | Correct with hysteresis |

---

## Deliverables

1. `design.cir` -- Mode control subcircuit: `.subckt mode_control bvdd pvdd svdd gnd vref en_ret bypass_en ea_en ref_sel uvov_en ilim_en`
2. Testbench files for every measurement listed above
3. `README.md` -- Design report: threshold values, hysteresis, transition waveforms, truth table verification, corner data
4. `*.png` -- Plots: BVDD ramp with all outputs, threshold vs corner, hysteresis loops
