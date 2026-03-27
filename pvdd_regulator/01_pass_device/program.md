# Block 01: Pass Device — Design Program

## Absolute Rules

1. **Real Sky130 PDK only.** The pass device must be an instantiated Sky130 HV device. No behavioral MOSFET models, no VCCS approximations.
2. **No behavioral models.** Only testbench supply sources and stimulus elements may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.** Do not hand-calculate W/L for HV devices -- simulate and find it.
5. **Push through difficulty.** The HV device may have low mobility and need very large W. That is expected. Do not replace it with an ideal switch.

---

## Purpose

The pass device is the power transistor that drops the input voltage (BVDD, 5.4-10.5V) to the regulated output (PVDD, 5.0V). All load current (0 to 50 mA) flows through this device. It is the most critical component in the LDO because:

1. Its on-resistance sets the dropout voltage (Vdo = Id * Rds_on at full gate drive).
2. Its gate capacitance (Cgs) is the dominant load for the error amplifier and sets a key pole in the feedback loop.
3. Its transconductance (gm_pass) determines the DC gain from gate to output and the output pole frequency.
4. Its safe operating area (SOA) limits determine reliability during transients.

**Everything downstream -- error amp sizing, compensation, startup -- depends on this device's characterization. CHARACTERIZE this block FIRST before designing anything else.**

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Input (source) | 5.4-10.5V | Battery supply |
| `pvdd` | Output (drain) | 5.0V regulated | Regulated output |
| `gate` | Input (gate) | 0 to ~BVDD | Gate drive from error amp |

**Connections in the LDO:**
- Source/bulk = BVDD supply rail (for PMOS) or drain = BVDD (for NMOS source-follower)
- Drain/source = PVDD output rail, also connected to 200 pF Cload, feedback divider, UV/OV sense
- Gate = error amp output (vout_gate from Block 00), compensation network (Block 03)

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Drain current at Vdo = 400mV | 50 | -- | -- | mA | Full load, gate fully driven |
| Dropout voltage at 50 mA | -- | 400 | -- | mV | Vds at which Id = 50 mA |
| Gate capacitance (Cgs) | -- | TBD | -- | pF | At operating point; expect 50-200 pF |
| Transconductance (gm) | -- | TBD | -- | mA/V | At Iload = 10 mA operating point |
| Rds_on (full gate drive) | -- | TBD | -- | ohm | At max Vgs |
| Leakage current (off) | -- | -- | 1 | uA | Vgs = 0V |
| Max Vds | -- | -- | 10.5 | V | Sky130 HV device limit |
| Temperature range | -40 | 27 | 150 | C | |

---

## Operating Conditions

- **Input:** BVDD = 5.4 to 10.5V
- **Output:** PVDD = 5.0V nominal, with 200 pF internal load cap
- **Load current:** 0 to 50 mA (active mode), 0 to 0.5 mA (retention mode)
- **Gate drive:** From error amp output, swing 0 to PVDD (or BVDD depending on error amp supply)
- **Corners:** SS/TT/FF/SF/FS at -40C, 27C, 150C

---

## Known Challenges

1. **The only real constraint: it must be an HV device from the Sky130 PDK.** The available HV devices are `sky130_fd_pr__pfet_g5v0d10v5`, `sky130_fd_pr__nfet_g5v0d10v5`, `sky130_fd_pr__pfet_05v0`, and `sky130_fd_pr__nfet_05v0`. Vds_max = 10.5V for g5v0d10v5, 5V for 05v0 devices.

2. **Low mobility of HV devices.** Sky130 HV PMOS has significantly lower mobility than standard PMOS. Expect large total W (several mm) to achieve 50 mA at 400 mV dropout. If W exceeds 20 mm, the topology may be impractical.

3. **Large gate capacitance.** A multi-mm device will have Cgs in the range of 50-200 pF. This is the dominant load for the error amplifier and a key pole in the LDO loop. This value MUST be characterized before Block 00 or Block 03 can be properly designed.

4. **SS corner at 150C is worst case.** Highest Rds_on, lowest mobility, highest Vth. The pass device must still deliver 50 mA at 400 mV dropout under worst-case conditions.

5. **Finger count and layout.** A multi-mm device needs many fingers or multiple parallel instances. Gate resistance from long poly fingers can degrade high-frequency performance.

---

## What to Explore

The agent is free to choose any pass device configuration that meets the specs. Key decisions:

- **PMOS vs NMOS:**
  - PMOS (common-source): Low dropout (Vdo = Vds_sat), gate can be pulled to GND. Standard LDO approach. No charge pump needed.
  - NMOS (source-follower): Higher dropout (Vdo = Vgs > Vth + Vdsat), but faster response and potentially smaller device. Requires gate voltage above PVDD -- needs charge pump or bootstrap. More complex.

- **Device type:** `pfet_g5v0d10v5` (10.5V), `pfet_05v0` (5V), `nfet_g5v0d10v5`, `nfet_05v0`. The g5v0d10v5 devices support the full BVDD range.

- **W/L selection:** L = minimum for HV device (0.5u for g5v0d10v5) gives lowest Rds_on but worst channel-length modulation. Longer L improves output resistance but requires proportionally more W.

- **Finger/parallel strategy:** Single device with many fingers vs. multiple parallel instances.

**The agent decides PMOS vs NMOS, device type, W/L, and finger configuration.**

---

## Dependencies

**Wave 1 block -- no dependencies on other blocks.**

This block should be designed FIRST. Its outputs (W/L, Cgs, gm, Rds_on) are required inputs to Block 00 (error amp), Block 03 (compensation), and Block 04 (current limiter).

---

## Testbench Requirements

The following characterizations must be performed:

| Measurement | What to Report |
|-------------|---------------|
| Id vs Vds family curves | At multiple Vgs values |
| Id vs Vgs at dropout condition | The key curve for W sizing |
| Gate capacitance (Cgs) vs bias | At the operating point (critical for Blocks 00/03) |
| Transconductance (gm) vs Id | Feeds loop gain calculation |
| On-resistance (Rds_on) | At full gate drive, for bypass mode |
| PVT corner characterization | All key parameters at SS/FF/SF/FS, -40/27/150C |
| Safe operating area (SOA) | Transient stress at max Vds and current |

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Id at dropout, max gate drive | >= 50 mA at TT 27C |
| Id at dropout, SS 150C | >= 50 mA (worst case) |
| Total W | < 20 mm (otherwise impractical) |
| Cgs at operating point | Measured and documented (feeds Block 00/03) |
| gm at 10 mA | Measured and documented |
| Rds_on at full gate drive | < 20 ohm |
| No model errors or convergence failures | All testbenches run to completion |

---

## Deliverables

1. `design.cir` -- Pass device subcircuit: `.subckt pass_device gate bvdd pvdd` (body connection handled internally)
2. Testbench files for every characterization listed above
3. `README.md` -- Characterization report: final W/L, Id(Vgs) curve, Cgs value, gm value, Rds_on, corner data
4. `*.png` -- Plots: Id vs Vds family, Id vs Vgs at dropout, Cgs vs Vgs, corner comparisons
