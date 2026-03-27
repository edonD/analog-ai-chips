# Block 07: Zener Clamp — Design Program

## Absolute Rules

1. **Real Sky130 PDK only.** Every diode and transistor must be an instantiated Sky130 device. No ideal Zener diodes or behavioral clamp models.
2. **No behavioral models.** Only testbench stimulus and supply sources may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** Sky130 does not have true Zener diodes. You must build the clamp from available devices. This requires creative circuit design.

---

## Purpose

The Zener clamp protects the PVDD output from voltage transients and overshoot conditions. In an automotive environment, events such as load dump (BVDD spike), fast BVDD ramps, and inductive switching can cause PVDD to overshoot beyond 5.5V. The clamp limits the maximum PVDD voltage by shunting excess current to ground when the voltage exceeds the clamp threshold.

**Protection scenarios:**
1. **Load dump transient:** BVDD spikes, error amp cannot respond fast enough, PVDD overshoots.
2. **Startup overshoot:** Error amp may be slow to respond during power-up.
3. **ESD event:** External pulse coupled to PVDD pin.
4. **Pass device gate stuck low:** Error amp fails, pass device fully ON, PVDD = BVDD.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `pvdd` | Input/Output | 5-6V | PVDD output node being clamped |
| `gnd` | Supply | 0V | Ground (clamp current sink) |

**Connections in the LDO:**
- `pvdd` connects directly to the PVDD output rail.
- The clamp sits in parallel with the load capacitor and feedback divider.
- It is passive -- draws zero current under normal conditions (PVDD < clamp threshold).

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Clamp voltage (onset, 1mA) | 5.5 | 5.8 | 6.2 | V | Voltage at which significant current starts |
| Clamp voltage at 10 mA | -- | 6.0 | 6.5 | V | Must not exceed this |
| Leakage at PVDD = 5.0V | -- | -- | 1 | uA | Must not affect quiescent budget |
| Leakage at PVDD = 5.17V | -- | -- | 5 | uA | Must not interfere with regulation |
| Peak current capability | 100 | -- | -- | mA | During transient (pulse, not DC) |
| Clamp impedance above threshold | -- | -- | 50 | ohm | Low impedance for effective clamping |
| Area | -- | -- | 5000 | um^2 | Compact |
| Temperature range | -40 | 27 | 150 | C | |

---

## Operating Conditions

- **Normal operation:** PVDD = 4.8 to 5.17V. Clamp draws < 1 uA.
- **Overshoot event:** PVDD exceeds 5.5V. Clamp activates and shunts current.
- **Transient pulse:** Fast voltage ramp (up to 10V/us) on PVDD through low impedance.
- **Corners:** SS/TT/FF/SF/FS at -40C, 27C, 150C.

---

## Known Challenges

1. **Sky130 has no true Zener diodes.** There are no dedicated Zener or avalanche diode devices in the PDK. The clamp must be built from available devices: PN junction diodes, MOSFETs, or combinations thereof.

2. **Temperature coefficient of diode stacks.** Forward-biased diode stacks have a negative TC (~-2 mV/C per junction). A 9-diode stack shifts by 9 * 2 mV * 190C = 3.4V across the -40 to 150C range. At 150C, the clamp could drop to ~5.1V -- dangerously close to the normal PVDD. At -40C, it rises to ~6.3V -- potentially too high for protection. This is a fundamental problem with the diode stack approach.

3. **Leakage at normal PVDD.** The clamp must not draw significant current at PVDD = 5.0V or 5.17V. For diode stacks, the voltage per junction (5.17V / 9 = 0.574V) must be safely below the diode turn-on knee.

4. **Clamp vs. LDO loop interaction.** During an OV event, if the clamp activates while the LDO loop is regulating, the clamp's low impedance appears in parallel with the load. This could affect loop stability. Verify that the clamp does not cause oscillation.

5. **Breakdown voltage uncertainty.** The `05v5` suffix on Sky130 diodes refers to the maximum rated voltage, not the breakdown voltage. The actual reverse breakdown may differ and must be characterized in simulation.

---

## What to Explore

The agent is free to choose any clamping approach that meets the specs. **Sky130 has no Zener -- the agent must find a way.**

- **Forward-biased diode stack.** Stack N junctions in series using `sky130_fd_pr__diode_pw2nd_05v5` or `sky130_fd_pr__diode_pd2nw_05v5`. Clamp voltage = N * Vf (~0.65V each at 27C). Simple and predictable, but has severe TC problems (see Known Challenges).

- **MOSFET voltage clamp.** An NMOS with gate biased by a resistive divider from PVDD. When PVDD exceeds the divider threshold + Vth, the MOSFET turns on and shunts current. Tunable threshold, sharper turn-on, better TC than diode stack. But draws static current through the divider.

- **Reverse-biased diode (avalanche).** Use PDK diodes in reverse bias near their breakdown voltage. Must characterize the actual breakdown voltage in simulation -- it may or may not be at a useful level.

- **Diode-connected MOSFET stack.** Stack diode-connected HV MOSFETs. Each drops Vth (~0.7-0.9V). TC of Vth is ~-1 mV/C, better than PN junction TC. Fewer devices needed.

- **Hybrid approach.** Combine a MOSFET active clamp for precision with a diode stack for fast transient response.

- **TC compensation.** Mix device types with opposite TC to stabilize the clamp voltage over temperature.

**The agent must find an approach that provides adequate clamping across the full -40 to 150C temperature range.**

---

## Dependencies

**Wave 3 block -- can be designed in parallel with other protection blocks.**

No circuit-level dependencies. The clamp is passive, connected in parallel with PVDD. When integrated (Block 10), verify that clamp leakage does not affect regulation and that the clamp does not cause oscillation during OV events.

---

## Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| DC I-V characteristic | Full I-V curve from 0 to 7V |
| Clamp voltage at 1mA and 10mA | Onset and clamping voltages |
| Leakage at PVDD = 5.0V and 5.17V | Current draw at normal operating voltage |
| Temperature sweep | I-V curve at -40, 27, 85, 150C |
| Transient clamping | Peak voltage during fast ramp (10V/us) |
| Process corners | Clamp voltage at SS/FF/SF/FS |

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Clamp onset at TT 27C | 5.5V to 6.2V (at 1 mA) |
| Clamp voltage at 10 mA, TT 27C | < 6.5V |
| Leakage at PVDD = 5.0V, TT 27C | < 1 uA |
| Leakage at PVDD = 5.17V, TT 27C | < 5 uA |
| Clamp onset at 150C | > 5.0V (must not drag down normal PVDD) |
| Clamp onset at -40C | < 7.0V (must still provide protection) |
| Transient peak (10V/us ramp) | < 6.5V with 200pF Cload |
| Peak current at 7V | > 100 mA (pulse rating) |

---

## Deliverables

1. `design.cir` -- Zener clamp subcircuit: `.subckt zener_clamp pvdd gnd`
2. Testbench files for every measurement listed above
3. `README.md` -- Design report: topology chosen, clamp voltage, I-V curve, TC data, leakage data
4. `*.png` -- Plots: I-V curve, I-V at multiple temperatures, transient clamping waveform
