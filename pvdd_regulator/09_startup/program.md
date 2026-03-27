# Block 09: Startup Circuit — Design Program

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device. No behavioral startup models or ideal switches that magically bootstrap the supply.
2. **No behavioral models.** Only testbench stimulus and supply sources may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** The startup is fundamentally a chicken-and-egg problem. It is solvable with real circuits.

---

## Purpose

The startup circuit solves the fundamental bootstrap problem in the PVDD LDO:

**The chicken-and-egg problem:**
1. The error amplifier runs from PVDD (5V supply domain).
2. PVDD is produced by the pass device, controlled by the error amplifier.
3. At power-on (BVDD ramping from 0V), PVDD = 0V, so the error amp has no supply.
4. With no error amp, the pass device gate is floating or pulled high (off), so PVDD stays at 0V.
5. Deadlock: the LDO never starts.

**The solution:** A startup circuit that forces PVDD to begin charging without the error amplifier, then hands off to the main regulation loop once PVDD is established.

**Additional requirements:**
- The PVDD ramp must be monotonic (no dips or oscillations).
- Must work for BVDD ramp rates from 0.1 V/us (slow battery connect) to 12 V/us (fast cold-crank recovery).
- Once regulation is established, the startup circuit must fully disable to avoid interfering with the error amp.
- Must handle cold crank: BVDD drops below PVDD and then recovers. PVDD must re-start cleanly.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Input | 0-10.5V | Battery supply (energy source for bootstrap) |
| `pvdd` | Output/Sense | 0-5V during startup | PVDD rail being bootstrapped |
| `gate` | Output | 0-BVDD | Pass device gate node |
| `gnd` | Supply | 0V | Ground |
| `vref` | Input | 1.226V | Bandgap reference (may not be available early in startup) |
| `startup_done` | Output | Digital | Startup complete flag |
| `ea_en` | Output | Digital | Error amplifier enable |

**Connections in the LDO:**
- The startup circuit connects to the same `gate` node as the error amp output. During startup, the startup circuit drives the gate. After startup, the error amp takes over and the startup circuit releases.
- `pvdd` is both an output (being charged) and a sense input (monitoring the ramp).
- `startup_done` connects to mode control (Block 08).

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Startup time (BVDD=7V, no load) | -- | -- | 100 | us | From BVDD reaching 5.6V to PVDD within 1% |
| Startup time (BVDD=7V, 50mA load) | -- | -- | 200 | us | Worst case: heavy load |
| PVDD ramp monotonicity | Yes | -- | -- | -- | No dips > 50 mV |
| PVDD overshoot during startup | -- | -- | 200 | mV | Max overshoot above 5.0V |
| BVDD ramp rate tolerance | 0.1 | -- | 12 | V/us | All rates |
| Quiescent current after startup | -- | -- | 1 | uA | Must fully disable |
| Handoff glitch | -- | -- | 100 | mV | PVDD disturbance at switchover |
| Cold crank recovery | Yes | -- | -- | -- | Clean re-start after BVDD dip |
| Temperature range | -40 | 27 | 150 | C | |

---

## Operating Conditions

- **BVDD ramp profiles:**
  - Normal: 0 to 10.5V at 1 V/us
  - Fast: 0 to 10.5V at 12 V/us (cold-crank recovery)
  - Slow: 0 to 10.5V at 0.1 V/us (gradual battery connect)
  - Cold crank: 10.5V -> 3V -> 7V (dip and recovery)
- **Load during startup:** 0 mA (best case) to 50 mA (worst case).
- **Corners:** SS/TT/FF/SF/FS at -40C, 27C, 150C.

---

## Known Challenges

1. **Handoff glitch.** The moment the startup circuit disables and the error amp takes over is critical. If there is a gap (both off) or overlap (both fighting), PVDD will glitch. The handoff mechanism must be smooth.

2. **Overshoot at fast BVDD ramps.** If the startup circuit drives the pass device gate too aggressively, PVDD will overshoot and approach BVDD before the error amp can regulate. The startup drive strength must be controlled.

3. **Insufficient drive at slow ramps.** At 0.1 V/us, BVDD rises slowly. If the startup circuit depends on a minimum dV/dt to charge gate capacitance, it may fail at slow ramps.

4. **SS 150C is the slowest startup.** Highest Vth, lowest mobility. The startup circuit may take longest to bootstrap PVDD. Must still complete within 200 us.

5. **FF -40C is the fastest startup.** Risk of PVDD overshoot. Lowest Vth, highest mobility. The startup pulldown may be too aggressive.

6. **Bandgap may not be available.** V_REF (1.226V from bandgap) may not be valid until PVDD is established. The startup circuit should not depend on V_REF being accurate during the bootstrap phase. Use BVDD-derived thresholds or simple Vth-based detection.

7. **Convergence.** Startup simulations are notoriously difficult for SPICE convergence because multiple nodes transition simultaneously from zero-energy states. Use `.ic` (initial conditions) and `uic` option.

---

## What to Explore

The agent is free to choose any startup mechanism that solves the chicken-and-egg problem. Options to consider:

- **Current-limited gate pulldown.** A weak NMOS (or NMOS + series resistor) pulls the pass device gate toward GND, partially turning on the PMOS pass device. PVDD charges through the pass device. When PVDD crosses a threshold, the pulldown disables and the error amp takes over.

- **Bootstrap resistor from BVDD.** A resistor from BVDD to the error amp supply. Provides trickle current to power the error amp directly from BVDD before PVDD is established. Simple but wastes current permanently unless a switch disconnects it.

- **Dedicated startup amplifier.** A simple, low-power amp built from HV devices that operates directly from BVDD (no PVDD needed). Provides coarse regulation during startup, then hands off to the precision error amp. Most robust but most complex.

- **Charge pump bootstrap.** A small charge pump that generates a local supply for the error amp from BVDD during startup.

- **Native device bootstrapper.** If Sky130 has native (zero-Vth) devices, they can pass current at very low Vgs, useful for bootstrapping from low BVDD.

- **Current source from BVDD.** A BVDD-powered current source that charges PVDD through the pass device or directly through a diode. Self-disables when PVDD reaches target.

**The agent decides how to solve the bootstrap problem.**

---

## Dependencies

**Wave 3 block -- requires:**
- Block 00 (error amp) -- must hand off control to the error amp
- Block 01 (pass device) -- drives the pass device gate (need Cgs value)
- Block 02 (feedback network) -- needed for closed-loop handoff testing
- Block 03 (compensation) -- needed for post-handoff stability
- Block 08 (mode control) -- coordinates startup/regulation mode transition

This is one of the last blocks to be fully verified because it requires the complete regulation loop. However, the startup mechanism itself can be designed and partially tested standalone.

---

## Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| Basic startup (BVDD ramp, no load) | PVDD ramp waveform, startup time |
| Startup with error amp handoff | PVDD glitch at handoff point |
| Startup with 50 mA load | Startup time under worst-case load |
| Fast BVDD ramp (12 V/us) | PVDD overshoot |
| Slow BVDD ramp (0.1 V/us) | Verify startup still completes |
| Cold crank recovery | BVDD dip and recovery profile |
| Startup circuit disable verification | Leakage after startup |
| PVT corners | Startup at SS/FF/SF/FS, -40/27/150C |

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Startup time (no load, BVDD=7V) | < 100 us |
| Startup time (50 mA load, BVDD=7V) | < 200 us |
| PVDD ramp monotonicity | No dips > 50 mV |
| PVDD overshoot | < 200 mV above 5.0V |
| Handoff glitch | < 100 mV disturbance |
| Works at 0.1 V/us ramp | Yes |
| Works at 12 V/us ramp | Yes |
| Cold crank recovery | Clean re-start |
| Startup circuit leakage after startup | < 1 uA |
| Works at SS 150C | Completes within 200 us |
| Works at FF -40C | No overshoot > 200 mV |
| No latch-up or stuck states | Always reaches regulation |

---

## Deliverables

1. `design.cir` -- Startup subcircuit: `.subckt startup bvdd pvdd gate gnd vref startup_done ea_en`
2. Testbench files for every measurement listed above
3. `README.md` -- Design report: startup strategy, mechanism, handoff details, ramp waveforms, timing, corner data
4. `*.png` -- Plots: PVDD ramp, gate voltage during startup, handoff zoom, cold crank waveform
