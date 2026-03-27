# Block 00: Error Amplifier — Design Program

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device. No exceptions.
2. **No behavioral models.** No ideal op-amps, no VCCS approximations, no VerilogA. The only ideal components allowed are: V_AVBG (1.226V bandgap), I_BIAS (1uA reference), and testbench stimulus/supply sources.
3. **ngspice only.** No HSPICE, Spectre, or Xyce. Fix convergence with `.option` settings.
4. **Every spec verified by simulation.** Hand calculations are for initial estimates only.
5. **Push through difficulty.** Iterate on the real circuit until it works.

---

## Purpose

The error amplifier is the core gain stage of the PVDD LDO regulator. It compares the feedback voltage (V_FB, ~1.226V from the resistive divider) to the bandgap reference (V_REF = 1.226V) and drives the gate of the HV pass device. The error amp's gain determines regulation accuracy. Its bandwidth and output impedance interact with the pass device gate capacitance and the compensation network to set loop stability.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `vref` | Input | ~1.226V | Bandgap reference (positive OTA input) |
| `vfb` | Input | ~1.226V | Feedback voltage from divider (negative OTA input) |
| `vout_gate` | Output | 0 to ~PVDD | Drives pass device gate |
| `pvdd` | Supply | 5.0V regulated | Positive supply rail |
| `gnd` | Supply | 0V | Ground |
| `ibias` | Input | -- | 1uA bias current input (mirrored internally) |
| `en` | Input | 0 / PVDD | Enable signal |

**Connections in the LDO:**
- `vref` connects to ideal V_AVBG (1.226V).
- `vfb` connects to the feedback divider midpoint (Block 02).
- `vout_gate` connects to the pass device gate (Block 01) and compensation network (Block 03).
- `pvdd` connects to the regulated PVDD output rail.
- `ibias` connects to the shared IREF current mirror.

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| DC open-loop gain | 60 | 70 | -- | dB | Measured at DC, no load |
| Unity-gain bandwidth (UGB) | 200 | 500 | 1000 | kHz | With Cgs_pass load (~50-200pF) |
| Phase margin (open-loop, into Cgs) | 55 | 70 | -- | deg | Error amp alone, not full LDO loop |
| Input offset voltage | -- | -- | 5 | mV | Contributes directly to PVDD error |
| Input common-mode range | 0.8 | -- | 2.0 | V | Must include 1.226V |
| Output voltage swing low | -- | -- | 0.5 | V | Must pull pass gate near GND (fully ON) |
| Output voltage swing high | PVDD-0.5 | -- | -- | V | Must approach PVDD (pass device OFF) |
| Supply voltage (PVDD) | 4.5 | 5.0 | 5.5 | V | Regulated domain |
| Quiescent current | -- | 50 | 100 | uA | From PVDD supply |
| CMRR | 50 | 60 | -- | dB | At DC |
| PSRR (from PVDD supply) | 40 | 50 | -- | dB | At DC |
| Slew rate (positive) | 0.5 | -- | -- | V/us | Charging Cgs_pass |
| Slew rate (negative) | 0.5 | -- | -- | V/us | Discharging Cgs_pass |
| Temperature range | -40 | 27 | 150 | C | |

---

## Operating Conditions

- **Supply:** PVDD = 4.5 to 5.5V (the regulated output). During startup, PVDD may not yet be established -- see Known Challenges.
- **Load:** The error amp output drives the pass device gate capacitance (50-200 pF from Block 01 characterization). This is a purely capacitive load.
- **Input levels:** Both inputs sit near 1.226V (bandgap reference level).
- **Corners:** SS/TT/FF/SF/FS at -40C, 27C, 150C.

---

## Known Challenges

1. **The error amp runs from PVDD (5V), but Sky130 1.8V devices have Vds_max = 1.8V.** You cannot use standard 1.8V transistors in a 5V domain without cascode protection. You must either use HV devices (g5v0d10v5, 5v0) or carefully stack 1.8V devices with cascode protection. This is a fundamental constraint that affects every transistor in the amplifier.

2. **High Vth in Sky130 HV devices.** The HV PMOS Vth is ~0.7-1.0V and HV NMOS Vth is ~0.6-0.9V. This eats into headroom and makes it harder to achieve wide output swing and high gain with limited supply voltage.

3. **Large capacitive load (50-200 pF).** The pass device gate capacitance is the dominant load. The error amp must have enough gm and bias current to achieve the UGB target while driving this load: UGB = gm / (2*pi*Cload).

4. **Startup chicken-and-egg.** The error amp needs PVDD to operate, but PVDD needs the error amp to regulate. The startup circuit (Block 09) solves this, but the error amp must be designed to start cleanly when PVDD first becomes available.

5. **Output swing must cover near-rail.** To fully turn the PMOS pass device ON, the gate must approach GND. To turn it OFF, the gate must approach PVDD (or BVDD). Limited output swing directly limits the regulator's dropout and shutdown behavior.

---

## What to Explore

The agent is free to choose any topology that meets the specifications above. Some topologies worth investigating as starting points:

- **Folded-cascode OTA** -- high gain (>60dB) in one stage, wide output swing, single high-impedance node.
- **Telescopic cascode OTA** -- highest gm efficiency, but limited input/output range. May not achieve the output swing requirements.
- **Two-stage OTA (e.g., with Miller compensation)** -- can achieve >80dB gain, but creates an additional pole that complicates LDO loop compensation (Block 03).
- **Recycling folded-cascode** -- improved slew rate and gm efficiency over standard folded-cascode.
- **Class-AB output stage** -- can improve slew rate dramatically for driving the large gate capacitance.
- **Current-mirror OTA** -- simple, but may not achieve sufficient gain.
- **Gain-boosted cascode** -- very high gain in one stage, but increased complexity.

Consider whether to use PMOS or NMOS input pair based on the input common-mode requirement (~1.226V). A PMOS input pair places the inputs well above GND. An NMOS input pair works if the inputs are above Vth + Vdsat_tail.

**The agent decides the topology, device types, and sizing.**

---

## Dependencies

**Wave 1 block -- no dependencies on other blocks.**

However, the pass device gate capacitance (Cgs) from Block 01 is needed to set the correct AC load. If Block 01 is not yet done, use Cgs = 100 pF as a placeholder and re-verify once the actual value is known.

---

## Testbench Requirements

The following measurements must be performed (the agent decides how to implement them):

| Measurement | What to Report |
|-------------|---------------|
| DC operating point | All node voltages, verify all devices in saturation |
| Open-loop gain and phase | Gain (dB), UGB (Hz), phase margin (deg) with Cgs load |
| Transient step response | Slew rate, settling time for a step on vfb |
| CMRR | Common-mode rejection ratio at DC and 10kHz |
| PSRR | Power supply rejection from PVDD at DC and 10kHz |
| Output swing | Verify output reaches within spec of both rails |
| PVT corners | All above at SS/FF/SF/FS and -40/27/150C |

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| DC gain | >= 60 dB |
| UGB (with Cgs_pass load) | 200 kHz to 1 MHz |
| Phase margin (OL into Cgs) | >= 55 deg |
| All devices in saturation | Vds > Vdsat + 50mV at nominal OP |
| Output swing low | < 0.5V |
| Output swing high | > PVDD - 0.5V |
| Quiescent current | < 100 uA from PVDD |
| Input offset | < 5 mV |
| CMRR | > 50 dB at DC |
| PSRR | > 40 dB at DC |
| All above hold at SS, FF, SF, FS | Yes |
| All above hold at -40, 27, 150C | Yes |

---

## Deliverables

1. `design.cir` -- Error amplifier subcircuit: `.subckt error_amp vref vfb vout_gate pvdd gnd ibias en`
2. Testbench files for every measurement listed above
3. `README.md` -- Design report with topology chosen, simulation results, device table, operating point summary
4. `*.png` -- Plots: gain/phase Bode, transient step response, corner overlays
