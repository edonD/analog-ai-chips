# Block 04: Current Limiter — Design Program

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device. No behavioral current limiters or ideal comparators.
2. **No behavioral models.** Only testbench stimulus and load elements may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** Short-circuit simulations stress convergence. Fix with `.option` settings and initial conditions, not by replacing the circuit.

---

## Purpose

The current limiter protects the HV pass device from destruction during output short-circuit or overload conditions. Without it, a shorted PVDD output would force the error amp to drive the pass device to maximum current, potentially exceeding SOA limits and causing thermal runaway or oxide breakdown.

The current limiter senses the output current and, when it exceeds a threshold (60-80 mA), limits the gate drive to cap the maximum output current regardless of load impedance.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Supply | 5.4-10.5V | Battery supply |
| `pvdd` | Sense | 5.0V regulated | Output node (for current monitoring) |
| `gate` | In/Out | 0 to ~PVDD | Error amp output / pass device gate (clamped when limit hit) |
| `gnd` | Supply | 0V | Ground |
| `ilim_flag` | Output | Digital | Current limit active flag (optional) |

**Connections in the LDO:**
- The current limiter senses the pass device current and acts on the `gate` node.
- Under normal operation (0-50 mA), the limiter must be completely transparent.
- When current exceeds the threshold, the limiter overrides the error amp's gate drive.

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Current limit threshold | 60 | 70 | 80 | mA | 20-60% above 50 mA max load |
| Threshold accuracy over PVT | -- | -- | +/-20 | % | Acceptable for protection |
| Response time | -- | -- | 10 | us | From overcurrent to clamping |
| Sense element area overhead | -- | -- | 5 | % | Fraction of main pass device area |
| Quiescent current overhead | -- | -- | 10 | uA | Under normal (non-limiting) operation |
| Voltage headroom consumed | -- | -- | 50 | mV | Additional dropout from sense element |
| Temperature range | -40 | 27 | 150 | C | |

---

## Operating Conditions

- **Normal mode:** Iload = 0 to 50 mA. Limiter must be completely inactive.
- **Limiting mode:** Iload tries to exceed 60-80 mA. Limiter activates.
- **Short-circuit:** Rload approaches 0. Limiter must protect the pass device.
- **BVDD range:** 5.4 to 10.5V during limiting.
- **Corners:** SS/TT/FF/SF/FS at -40C, 27C, 150C.

---

## Known Challenges

1. **The limit threshold must stay above 50 mA at all PVT corners.** If the limiter trips below 50 mA at any corner, it interferes with normal operation. This means the SS 150C threshold (lowest, due to reduced mobility and shifted Vth) must still be above 50 mA.

2. **The limit threshold must stay below ~100 mA at all corners.** If it drifts too high at FF -40C, the protection is ineffective.

3. **No interference with normal regulation.** At 50 mA load, the limiter must add negligible voltage drop, noise, or phase shift to the main regulation loop.

4. **Short-circuit convergence.** Simulating a hard short (Rload ~ 0) with a current limiter active is notoriously difficult for SPICE convergence. Expect to need aggressive `.option` settings.

5. **Power dissipation during sustained shorts.** With Vout = 0V and Ilim = 70 mA, the pass device dissipates P = BVDD * 70 mA = 0.7W at BVDD = 10.5V. A fold-back characteristic (reducing Ilim as Vout drops) mitigates this.

---

## What to Explore

The agent is free to choose any current limiting topology that meets the specs. Options to consider:

- **Sense mirror (scaled replica).** A small replica of the pass device (W_sense = W_pass / N) carries a proportional current. When the sense current exceeds a reference, the limiter activates. Classic approach. Mirror ratio accuracy depends on Vds matching.

- **Sense resistor in series.** A small resistor in the main current path. Voltage across it is compared to a threshold. Simple but adds dropout voltage. May be acceptable if the resistor is small enough (< 1 ohm = 50 mV at 50 mA).

- **Brick-wall limiter.** Hard clamp at the threshold -- no fold-back. Simpler to design, but higher power dissipation during sustained shorts.

- **Foldback current limiter.** Reduces the current limit as Vout drops. Limits pass device power during shorts. More complex but safer thermally.

- **Hybrid.** Brick-wall for fast response, then transition to foldback for thermal protection during sustained events.

- **Digital/threshold approach.** Comparator monitoring a sense voltage, driving a clamp switch.

**The agent decides the sensing method, clamping mechanism, and whether to include foldback.**

---

## Dependencies

**Wave 2 block -- requires:**
- Block 01 (pass device) -- the sense element must match the pass device (same type, same L if using a mirror)
- Block 00 (error amp) -- needed for closed-loop current limiting behavior
- Block 02 (feedback network) -- needed for closed-loop testing
- Block 03 (compensation) -- needed for stability verification with limiter in circuit

---

## Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| Output I-V curve showing limiting | Iout vs Vout with Rload swept to near 0 |
| Current limit trip point | Exact threshold at TT 27C |
| Transient short-circuit response | Time from short to current clamping |
| Normal operation impact | PVDD with and without limiter at 0-50 mA |
| Loop stability with limiter | PM must still be > 45 deg at normal loads |
| PVT corner threshold | Limit threshold at SS/FF/SF/FS, -40/27/150C |

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Current limit at TT 27C | 60-80 mA |
| Current limit at SS 150C | >= 50 mA (must not limit below max load) |
| Current limit at FF -40C | <= 100 mA (must actually limit) |
| Response time to short | < 10 us |
| Impact on PVDD at Iload = 50 mA | < 10 mV difference vs no-limiter |
| Sense element quiescent current | < 10 uA at Iload = 0 |
| No oscillation during limiting | Clean transient, no ringing |
| Loop stability unaffected | PM > 45 deg with limiter at normal loads |

---

## Deliverables

1. `design.cir` -- Current limiter subcircuit: `.subckt current_limiter gate bvdd pvdd gnd ilim_flag`
2. Testbench files for every measurement listed above
3. `README.md` -- Design report: topology, mirror ratio or sense method, limit threshold, I-V curve, transient response, corner data
4. `*.png` -- Plots: I-V limit curve, transient short-circuit response, corner comparison
