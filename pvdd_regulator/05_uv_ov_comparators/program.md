# Block 05: UV/OV Comparators — Design Program

## Absolute Rules

1. **Real Sky130 PDK only.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device. No behavioral comparators or Verilog-A thresholds.
2. **No behavioral models.** Only testbench stimulus and supply sources may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.**
5. **Push through difficulty.** Hysteresis and threshold accuracy require careful sizing. Iterate.

---

## Purpose

The UV (undervoltage) and OV (overvoltage) comparators continuously monitor the PVDD output and flag abnormal conditions:

- **UV comparator:** Asserts `uv_flag` when PVDD drops below ~4.3V. Triggers mode transitions and system resets.
- **OV comparator:** Asserts `ov_flag` when PVDD rises above ~5.5V. Flags overshoot conditions that could damage downstream circuits.

Both comparators need hysteresis to prevent chattering when PVDD hovers near a threshold. They must operate with low power (< 5 uA each) since they are always on.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `pvdd` | Input (sense) | 0-6V | PVDD output being monitored |
| `vref` | Input | 1.226V | Bandgap reference for threshold generation |
| `uv_flag` | Output | Digital (0/PVDD) | Undervoltage flag: HIGH when PVDD < UV threshold |
| `ov_flag` | Output | Digital (0/PVDD) | Overvoltage flag: HIGH when PVDD > OV threshold |
| `vdd_comp` | Supply | PVDD or BVDD | Comparator supply |
| `gnd` | Supply | 0V | Ground |
| `en` | Input | Digital | Enable signal |

**Connections in the LDO:**
- `pvdd` connects to the PVDD output rail.
- `vref` connects to the ideal V_AVBG bandgap (1.226V).
- `uv_flag` and `ov_flag` connect to mode control logic (Block 08).
- Flags may also be level-shifted (Block 06) to the SVDD domain.

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| UV threshold (falling) | 4.0 | 4.3 | 4.5 | V | PVDD level at which UV asserts |
| UV hysteresis | 50 | 100 | 150 | mV | UV de-asserts at threshold + hysteresis |
| OV threshold (rising) | 5.25 | 5.5 | 5.7 | V | PVDD level at which OV asserts |
| OV hysteresis | 50 | 100 | 150 | mV | OV de-asserts at threshold - hysteresis |
| Response time (UV) | -- | -- | 5 | us | From crossing threshold to flag change |
| Response time (OV) | -- | -- | 5 | us | From crossing threshold to flag change |
| Power per comparator | -- | -- | 5 | uA | Quiescent current from supply |
| Output levels | 0 / PVDD | -- | -- | V | Rail-to-rail digital output |
| Threshold accuracy over PVT | -- | -- | +/-10 | % | From nominal |
| Temperature range | -40 | 27 | 150 | C | |

---

## Operating Conditions

- **PVDD range:** 0 to ~6V (monitoring the full output range including overshoot).
- **Supply:** The comparators need power even when PVDD is low (for UV detection). Consider whether to run from PVDD or BVDD.
- **Corners:** SS/TT/FF/SF/FS at -40C, 27C, 150C.

---

## Known Challenges

1. **UV comparator supply chicken-and-egg.** The UV comparator must detect when PVDD is low (~4.3V), but if the comparator runs from PVDD, its own supply may be too low to function. Consider running from BVDD instead, or designing for very low supply operation.

2. **Threshold accuracy over temperature.** The threshold is set by V_REF (1.226V) and a resistive divider. The divider ratio TC and the comparator input offset both contribute to threshold error. The UV threshold must stay within 4.0-4.5V and OV within 5.25-5.7V across all PVT conditions.

3. **Hysteresis calibration.** The hysteresis mechanism must produce 50-150 mV at the PVDD level. Too little hysteresis = chattering. Too much = late detection.

4. **Low power requirement.** 5 uA per comparator means limited gm and slow response. The < 5 us response time must still be met.

---

## What to Explore

The agent is free to choose any comparator topology that meets the specs. Options to consider:

- **Differential pair with cross-coupled loads** -- the classic comparator with built-in hysteresis from positive feedback in the load.
- **Schmitt trigger** -- CMOS inverter-based threshold detector with feedback resistor for hysteresis.
- **Clocked comparator (StrongARM)** -- very low power (only consumes during comparison), but requires a clock.
- **Current-mode comparator** -- threshold set by current comparison rather than voltage. Can be very compact.
- **Two-stage comparator** -- differential pair followed by gain stage for sharper thresholds.

**Threshold generation options:**
- Resistive divider from PVDD compared to V_REF.
- Scaled current mirrors comparing PVDD-derived current to reference current.
- Direct comparison using a MOSFET threshold (Vth-referenced).

The agent decides the comparator topology, threshold generation method, and hysteresis mechanism. Two separate comparators are needed (UV and OV), but they may share the same topology or be different if the requirements warrant it.

---

## Dependencies

**Wave 1 block -- no dependencies on other blocks for standalone design.**

The comparators can be designed and tested independently. In top integration (Block 10), the UV/OV flags connect to mode control logic (Block 08).

---

## Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| UV trip point (falling and rising) | Exact threshold and hysteresis |
| OV trip point (rising and falling) | Exact threshold and hysteresis |
| Response time | From threshold crossing to flag transition |
| Power consumption | Quiescent current per comparator |
| PVT corners | Thresholds at SS/FF/SF/FS, -40/27/150C |
| Output levels | Verify rail-to-rail digital output |

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| UV threshold (falling) at TT 27C | 4.0V to 4.5V |
| UV hysteresis | 50 mV to 150 mV |
| OV threshold (rising) at TT 27C | 5.25V to 5.7V |
| OV hysteresis | 50 mV to 150 mV |
| UV threshold across all PVT | Within 4.0-4.5V range |
| OV threshold across all PVT | Within 5.25-5.7V range |
| Response time (both) | < 5 us |
| Power per comparator | < 5 uA |
| Output swings rail-to-rail | Yes |
| No oscillation at threshold | Clean switching with hysteresis |

---

## Deliverables

1. `design.cir` -- UV and OV comparator subcircuits:
   - `.subckt uv_comparator pvdd vref uv_flag vdd_comp gnd en`
   - `.subckt ov_comparator pvdd vref ov_flag vdd_comp gnd en`
2. Testbench files for every measurement listed above
3. `README.md` -- Design report: threshold values, hysteresis data, corner variation, power, response time
4. `*.png` -- Plots: PVDD ramp with flag transitions, hysteresis loop, corner threshold comparison
