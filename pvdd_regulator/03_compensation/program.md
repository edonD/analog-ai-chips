# Block 03: Compensation Network — Design Program

## Absolute Rules

1. **Real Sky130 PDK only.** Every capacitor and resistor in the compensation network must be an instantiated Sky130 device. No ideal capacitors or resistors.
2. **No behavioral models.** Only testbench stimulus sources and load elements may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.** Phase margin must be measured from AC simulation, not estimated from hand analysis.
5. **Push through difficulty.** This is the hardest block. The output pole moves 1000x with load. You will iterate many times. Do not give up.

---

## Purpose

The compensation network ensures the PVDD LDO feedback loop is stable (PM > 45 deg, GM > 10 dB) across ALL operating conditions:
- Load current: 0 mA to 50 mA
- Temperature: -40C to 150C
- Process corners: SS, TT, FF, SF, FS
- Input voltage: BVDD = 5.4V to 10.5V

---

## Why This Is the Hardest Block

The LDO output pole is at: `f_out = 1 / (2*pi * Rload * Cload)`

| Load Current | Effective Rload | Output Pole Frequency |
|-------------|----------------|----------------------|
| 0 mA | ~infinity | < 1 kHz |
| 100 uA | 50 kohm | ~16 kHz |
| 1 mA | 5 kohm | ~160 kHz |
| 10 mA | 500 ohm | ~1.6 MHz |
| 50 mA | 100 ohm | ~8 MHz |

The output pole moves by 1000x from no-load to full-load. A compensation scheme that works at one load may be completely unstable at another. **The compensation must stabilize the loop at ALL load points simultaneously.**

In addition, the gate pole (set by error amp output impedance and pass device Cgs) creates a second critical pole. The interaction between these two load-dependent poles is what makes LDO compensation fundamentally different from -- and harder than -- standard two-stage op-amp compensation.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `vout_gate` | Connection | 0 to ~PVDD | Error amp output / pass device gate node |
| `pvdd` | Connection | 5.0V | PVDD output node |
| `gnd` | Supply | 0V | Ground |
| `vfb` | Connection | ~1.226V | Feedback node (if needed for lead compensation) |

**Connections in the LDO:**
- The compensation network connects between the error amp output (`vout_gate`) and other nodes (PVDD, GND, or vfb) depending on the topology chosen.
- It physically sits between Block 00 (error amp) and Block 01 (pass device).

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Phase margin (all loads) | 45 | 55 | -- | deg | At Iload = 0, 0.1, 1, 10, 50 mA |
| Gain margin (all loads) | 10 | 15 | -- | dB | At all load points |
| Phase margin (all corners) | 45 | -- | -- | deg | SS, FF, SF, FS at 27C |
| Phase margin (all temps) | 45 | -- | -- | deg | -40, 27, 150C at TT |
| Unity-gain bandwidth | 100 | 300 | 1000 | kHz | At nominal load (10 mA) |
| DC loop gain | 40 | 60 | -- | dB | For load/line regulation |
| Settling time (load step) | -- | -- | 10 | us | 1mA to 10mA step, settle to 1% |
| Compensation cap area | -- | -- | 50000 | um^2 | Keep area reasonable |

---

## Operating Conditions

- **Full loop includes:** Error amp (Block 00) + pass device (Block 01) + feedback divider (Block 02) + 200 pF Cload + compensation network.
- **Load range:** Rload from ~100 ohm (50 mA) to open circuit (no load, just leakage).
- **BVDD:** 5.4 to 10.5V.
- **Corners:** SS/TT/FF/SF/FS at -40C, 27C, 150C.

---

## Known Challenges

1. **The output pole moves 1000x with load.** At no-load, the output pole is at ~1 kHz. At 50 mA, it is at ~8 MHz. Any fixed compensation must handle this entire range.

2. **The gate pole also moves.** The error amp output impedance varies with operating point, so the gate pole (Rout_EA * Cgs_pass) is not fixed either.

3. **No ESR zero to help.** This is an internal-cap-only LDO (200 pF on-chip). There is no external cap with ESR to provide a stabilizing zero.

4. **Worst-case load points.** Light load (no-load) tends to have the worst PM because the output pole is slowest and closest to the crossover frequency. But mid-load can also be problematic if the two poles collide near UGB.

5. **Area budget.** Large compensation caps consume die area. A 50 pF MIM cap is 25,000 um^2. The total compensation area should stay under 50,000 um^2.

6. **Transient vs. AC.** A design with 45 deg PM in AC analysis may still ring in transient if the poles move during the transient. Verify with both AC and transient simulations.

---

## What to Explore

The agent is free to choose any compensation strategy that achieves PM > 45 deg at all loads. **Do not limit yourself to Miller compensation.** Some approaches worth investigating:

- **Miller compensation (Cc from gate to output)** -- the classic approach. Creates pole-splitting. Optionally add a series resistor (Rz) for a left-half-plane zero. Simple but may not stabilize all loads.
- **Miller with nulling resistor** -- Rz in series with Cc to place a zero that tracks the non-dominant pole.
- **Dominant-pole at gate** -- add large cap at error amp output to make gate pole absolutely dominant. Simple but kills bandwidth.
- **Adaptive biasing** -- sense load current and increase error amp bias at high loads. Moves the gate pole out to track the output pole. How the best capless LDOs work.
- **Multi-loop compensation** -- separate fast inner loop and slow outer loop.
- **Pole-zero tracking** -- compensation that automatically adjusts with load.
- **Nested Miller** -- if using a two-stage error amp.
- **Feed-forward capacitor** -- from vfb to vout_gate for phase lead.
- **Cascode compensation** -- separate the Miller cap feedback path through a cascode node for better pole-splitting.

**The agent should explore topologies that achieve PM > 45 deg across the full 0-50 mA load range. The topology that works is the right topology.**

---

## Dependencies

**Wave 2 block -- requires ALL of the following:**
- Block 00 (error amp) -- `design.cir` must exist and simulate
- Block 01 (pass device) -- `design.cir` must exist with characterized Cgs, gm
- Block 02 (feedback network) -- `design.cir` must exist with correct ratio

The compensation network cannot be designed in isolation. It is meaningless without the full loop.

---

## Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| Loop gain and phase margin (LSTB) | PM and GM at each load point |
| PM vs load current sweep | Parametric: Iload = 0, 0.1, 1, 10, 50 mA |
| PM at all PVT corners | 5 corners x 3 temperatures = 15 conditions minimum |
| PM vs BVDD | Sweep BVDD 5.4 to 10.5V |
| Load step transient | 1mA to 10mA and 10mA to 1mA, 1us edge |
| Full Bode plot | Open-loop gain and phase for visualization |

**Note on loop-breaking:** In ngspice, use a large inductor (1GH) in series at the feedback node to break the DC loop while passing AC. The agent may use any valid loop-breaking technique.

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Phase margin at Iload = 0 mA | >= 45 deg |
| Phase margin at Iload = 100 uA | >= 45 deg |
| Phase margin at Iload = 1 mA | >= 45 deg |
| Phase margin at Iload = 10 mA | >= 45 deg |
| Phase margin at Iload = 50 mA | >= 45 deg |
| Gain margin at ALL loads | >= 10 dB |
| PM at SS/FF/SF/FS corners, all loads | >= 45 deg |
| PM at -40C and 150C, all loads | >= 45 deg |
| Load transient undershoot (1->10 mA) | < 150 mV |
| Load transient overshoot (10->1 mA) | < 150 mV |
| Settling time | < 10 us to within 1% |
| No oscillation at any condition | Zero sustained ringing in any transient |

**If any single condition fails, the compensation is NOT done. Iterate.**

---

## Deliverables

1. `design.cir` -- Compensation network subcircuit: `.subckt compensation vout_gate pvdd gnd` (add `vfb` pin if lead compensation is used)
2. Testbench files for every measurement listed above
3. `README.md` -- Design report: topology chosen, component values, PM at every load/corner/temp, Bode plots, transient waveforms, explanation of why the chosen approach works
4. `*.png` -- Plots: Bode (gain + phase), PM vs load current, transient step responses, corner overlays
