# Block 02: Feedback Network — Design Program

## Absolute Rules

1. **Real Sky130 PDK only.** Every resistor must be an instantiated Sky130 device. No ideal R=308k behavioral elements.
2. **No behavioral models.** Only testbench supply sources and stimulus may be ideal.
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.** The divider ratio must be measured in simulation, not assumed from hand calculation.
5. **Push through difficulty.** Sky130 PDK resistors have non-zero TC and process variation. Characterize them; do not ignore them.

---

## Purpose

The feedback network is a voltage divider that scales PVDD (5.0V) down to the bandgap reference level (1.226V) for comparison in the error amplifier. The divider ratio directly sets the regulated output voltage:

```
V_PVDD = V_REF / ratio = 1.226V / 0.2452 = 5.0V
```

The feedback network determines:
1. **Output voltage accuracy** -- ratio errors translate directly to PVDD errors.
2. **Temperature coefficient of PVDD** -- mismatched TCs between top and bottom resistors cause ratio drift.
3. **Quiescent current** -- divider current flows continuously from PVDD to GND.
4. **Noise** -- resistor thermal noise injects directly at the error amp input.
5. **Bandwidth** -- parasitic capacitance at V_FB creates a pole that can affect loop stability.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `pvdd` | Input | 5.0V regulated | Top of divider |
| `vfb` | Output | ~1.226V | Divider midpoint, to error amp negative input |
| `gnd` | Supply | 0V | Bottom of divider |

**Connections in the LDO:**
- `pvdd` connects to the PVDD output rail (drain of pass device, Block 01).
- `vfb` connects to the error amp inverting input (Block 00).
- The compensation network (Block 03) may also connect at or near the `vfb` node.

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Divider ratio (Vfb/Vpvdd) | 0.2440 | 0.2452 | 0.2465 | -- | Sets PVDD = 5.0V +/- 25mV from ratio alone |
| Total divider resistance | 350 | 408 | 500 | kohm | Sets quiescent current |
| Divider current | 10 | 12.3 | 15 | uA | From PVDD to GND |
| Ratio TC (matched) | -- | -- | 50 | ppm/C | Near-zero with matched resistor types |
| Noise at vfb (integrated, 1Hz-1MHz) | -- | -- | 50 | uVrms | Thermal noise of divider |
| Parasitic capacitance at vfb | -- | -- | 2 | pF | From resistor body caps |
| Temperature range | -40 | 27 | 150 | C | |

---

## Operating Conditions

- **Input:** PVDD = 4.8 to 5.17V (regulated output range)
- **Output:** V_FB = ~1.226V at PVDD = 5.0V
- **Corners:** SS/TT/FF/SF/FS at -40C, 27C, 150C

---

## Known Challenges

1. **Ratio accuracy vs. area.** The divider ratio must produce V_FB = 1.226V at PVDD = 5.0V. PDK resistors have end effects, contact resistance, and non-ideal R/sq values that must be calibrated in simulation before finalizing the design.

2. **Temperature coefficient.** Even with matched resistor types, there can be residual TC mismatch. The ratio TC determines how much PVDD drifts with temperature beyond the bandgap TC.

3. **Quiescent current budget.** Lower resistance = higher current = lower noise but worse Iq. Higher resistance = lower current = higher noise and more susceptibility to leakage currents. The total divider current should be 10-15 uA.

4. **Parasitic capacitance at V_FB.** High-value poly resistors have significant body capacitance. This creates a pole at the feedback node that can affect loop stability, especially with high-resistance dividers.

---

## What to Explore

The agent is free to choose any topology and resistor type that meets the specs. Options to consider:

- **Simple two-resistor divider** -- the standard approach. R_TOP ~ 308 kohm, R_BOT ~ 100 kohm.
- **Unit-resistor ladder** -- build both R_TOP and R_BOT from identical unit resistors in series for best matching.
- **Kelvin connection** -- separate sense and force paths for highest accuracy (likely overkill here).
- **Buffered divider** -- add a unity-gain buffer at the V_FB node to isolate the divider from the error amp input capacitance.
- **Trimming taps** -- include intermediate taps on the resistor string for post-fabrication adjustment.

**Resistor type choices in Sky130:**
- `sky130_fd_pr__res_xhigh_po` -- extra-high R polysilicon (~2 kohm/sq, low TC). Good for high-value resistors in small area.
- `sky130_fd_pr__res_high_po` -- medium-R polysilicon.
- `sky130_fd_pr__res_generic_nd` -- N-diffusion resistor.
- `sky130_fd_pr__res_generic_pd` -- P-diffusion resistor.

Using the same resistor type for both R_TOP and R_BOT cancels the TC to first order.

**The agent decides the resistor type, topology, exact values, and layout strategy.**

---

## Dependencies

**Wave 2 block -- needs Block 00 (error amp) for closed-loop verification.**

The feedback network itself has no circuit dependencies -- it is just resistors. However, it should be verified in the closed loop with Blocks 00 and 01 to confirm the correct PVDD output. For standalone testing, an ideal 5V source on PVDD is sufficient.

---

## Testbench Requirements

| Measurement | What to Report |
|-------------|---------------|
| DC divider ratio at PVDD = 5.0V | V_FB value, computed ratio |
| Ratio vs temperature (-40 to 150C) | Ratio TC in ppm/C |
| Ratio at process corners | Variation across SS/FF/SF/FS |
| Absolute resistance values | R_TOP and R_BOT individually |
| Noise at V_FB node | Spectral density and integrated noise (1Hz-1MHz) |

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| V_FB at PVDD=5.0V, TT 27C | 1.226V +/- 1mV (adjust sizing until exact) |
| V_FB variation over -40 to 150C | < 5 mV (ratio TC < 50 ppm/C) |
| V_FB variation across SS/FF | < 10 mV |
| Divider current | 10-15 uA |
| Integrated noise at vfb (1Hz-1MHz) | < 50 uVrms |
| No model errors | All testbenches run without errors |

---

## Deliverables

1. `design.cir` -- Feedback divider subcircuit: `.subckt feedback_network pvdd vfb gnd`
2. Testbench files for every measurement listed above
3. `README.md` -- Design report: final R values, ratio, TC data, noise analysis, corner results
4. `*.png` -- Plots: ratio vs temperature, noise spectrum
