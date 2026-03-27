# Block 06: Level Shifter — Design Program

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor must be an instantiated Sky130 device. No behavioral level shifters or ideal switches.
2. **No behavioral models.** Only testbench stimulus and supply sources may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** Level shifters across wide voltage ratios (2.2V to 10.5V) are tricky. Iterate.

---

## Purpose

The level shifter translates digital control signals between two voltage domains:

- **SVDD domain (2.2V):** Where digital mode control, enable signals, and configuration bits originate.
- **BVDD/PVDD domain (5-10.5V):** Where the error amplifier, pass device, and protection circuits operate.

Without level shifters, SVDD-domain signals (0/2.2V) cannot reliably drive HV-domain gates, and HV-domain outputs (0/5-10.5V) would overstress SVDD-domain inputs.

**Signals requiring level shifting:**

| Signal | Direction | From | To |
|--------|-----------|------|-----|
| `en` (enable) | SVDD -> BVDD | 0/2.2V | 0/BVDD |
| `mode[1:0]` | SVDD -> BVDD | 0/2.2V | 0/BVDD |
| `bypass_en` | SVDD -> BVDD | 0/2.2V | 0/BVDD |
| `uv_flag` | PVDD -> SVDD | 0/PVDD | 0/2.2V |
| `ov_flag` | PVDD -> SVDD | 0/PVDD | 0/2.2V |

---

## Interface

### Low-to-High (SVDD -> BVDD)

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `in` | Input | 0/SVDD (2.2V) | Input signal |
| `out` | Output | 0/BVDD | Level-shifted output |
| `svdd` | Supply | 2.2V | Low-voltage supply |
| `bvdd` | Supply | 5.4-10.5V | High-voltage supply |
| `gnd` | Supply | 0V | Ground |

### High-to-Low (PVDD -> SVDD)

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `in` | Input | 0/PVDD (~5V) | Input signal |
| `out` | Output | 0/SVDD (2.2V) | Level-shifted output |
| `pvdd` | Supply | 5.0V | High-voltage supply |
| `svdd` | Supply | 2.2V | Low-voltage supply |
| `gnd` | Supply | 0V | Ground |

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Output swing (low-to-high) | 0/BVDD | -- | -- | V | Must reach full BVDD rail |
| Output swing (high-to-low) | 0/SVDD | -- | -- | V | Must reach full SVDD rail |
| Propagation delay (rising) | -- | -- | 100 | ns | |
| Propagation delay (falling) | -- | -- | 100 | ns | |
| BVDD operating range | 5.4 | -- | 10.5 | V | Must work across full range |
| Static power per shifter | -- | -- | 5 | uA | No static current in steady state |
| Duty cycle distortion | -- | -- | 5 | % | Symmetric delays |
| Temperature range | -40 | 27 | 150 | C | |

---

## Operating Conditions

- **SVDD:** Fixed 2.2V.
- **BVDD:** 5.4 to 10.5V (the level shifter must work across this entire range).
- **PVDD:** ~5.0V (for high-to-low shifter).
- **Input signals:** Digital, 0 to SVDD or 0 to PVDD.
- **Load:** Typical gate capacitance of downstream logic (~0.5-2 pF).
- **Corners:** SS/TT/FF/SF/FS at -40C, 27C, 150C.

---

## Known Challenges

1. **SVDD = 2.2V must drive HV NMOS devices.** The HV NMOS Vth is ~0.6-0.9V. At Vgs = 2.2V, the device is in moderate inversion with limited drive strength. At SS corner 150C, Vth can approach 0.9V, leaving only ~1.3V of overdrive. The level shifter must be sized to overcome cross-coupled latch pull-up current even at this worst case.

2. **Wide BVDD range.** At BVDD = 5.4V, the PMOS cross-coupled pair is weak (small Vsg). At BVDD = 10.5V, the PMOS is strong and there may be excessive crowbar current during switching. The design must handle both extremes.

3. **1.8V device protection.** If using 1.8V devices in the SVDD domain, their gate-oxide cannot tolerate more than 1.8V. Any signal from the BVDD/PVDD domain must be clamped or level-shifted before reaching a 1.8V device gate.

4. **Static power.** A poorly designed level shifter can have a permanent DC current path through the cross-coupled pair during an intermediate state. The design must ensure zero (or near-zero) static current in both stable states.

---

## What to Explore

The agent is free to choose any level shifter topology that meets the specs. Options to consider:

**Low-to-high (SVDD -> BVDD):**
- **Cross-coupled PMOS** -- the classic approach. Two HV PMOS cross-coupled from BVDD, two HV NMOS pull-downs driven by SVDD-level inputs.
- **Current-mirror level shifter** -- uses a current mirror to transfer the signal. More robust at low Vgs but uses more current.
- **Wilson-mirror level shifter** -- improved current mirror with better switching characteristics.
- **Differential cascode** -- cascoded input stage for improved isolation.
- **Resistor-load level shifter** -- replace cross-coupled PMOS with resistors. Simpler but slower and draws static current.

**High-to-low (PVDD -> SVDD):**
- **Voltage-clamped inverter** -- HV NMOS input, 1.8V or HV PMOS load, output clamped to SVDD.
- **Resistive divider** -- simple but slow and draws DC current.
- **Cascode clamp** -- stack devices to limit voltage seen by SVDD-domain transistors.
- **Current-mirror approach** -- sense current from HV domain, mirror to SVDD domain.

**The agent decides the topology for both directions.**

---

## Dependencies

**Wave 1 block -- no dependencies on other blocks for standalone design.**

The level shifter is a utility block used by Block 08 (mode control) and Block 10 (top integration). It can be designed and tested independently.

---

## Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| Logic function verification | Both up and down shifters, both input states |
| Propagation delay (tpLH, tpHL) | At nominal conditions |
| Functionality across BVDD range | BVDD = 5.4, 7, 10.5V |
| Static power | Current in both stable states |
| PVT corners | Delay and function at SS/FF/SF/FS, -40/27/150C |
| Output levels | Verify output reaches within 0.2V of both rails |

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Low-to-high output reaches BVDD | Output HIGH > BVDD - 0.2V |
| Low-to-high output reaches GND | Output LOW < 0.2V |
| High-to-low output reaches SVDD | Output HIGH > SVDD - 0.2V |
| High-to-low output reaches GND | Output LOW < 0.2V |
| Propagation delay | < 100 ns at all conditions |
| Works at BVDD = 5.4V | Reliable switching at minimum supply |
| Works at BVDD = 10.5V | Reliable switching, no breakdown |
| Static power | < 5 uA per shifter |
| Works at SS 150C | Reliable switching (worst case) |
| No metastable states | Output always resolves to rail |

---

## Deliverables

1. `design.cir` -- Level shifter subcircuits:
   - `.subckt level_shifter_up in out bvdd svdd gnd`
   - `.subckt level_shifter_down in out pvdd svdd gnd`
2. Testbench files for every measurement listed above
3. `README.md` -- Design report: topology, device sizes, delay measurements, BVDD range validation, corner data
4. `*.png` -- Plots: input/output waveforms, delay vs BVDD, corner comparison
