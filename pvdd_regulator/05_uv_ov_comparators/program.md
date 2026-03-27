# Block 05: UV/OV Comparators — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device (`sky130_fd_pr__nfet_g5v0d10v5`, `sky130_fd_pr__pfet_g5v0d10v5`, `sky130_fd_pr__res_xhigh_po`, etc.). **No exceptions. No behavioral comparators. No Verilog-A thresholds.**
2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** Only testbench stimulus and supply sources may be ideal.
3. **ALL SIMULATIONS IN NGSPICE.** Fix convergence with `.option` settings — do not switch simulators.
4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.**
5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** Comparator hysteresis and threshold accuracy require careful sizing. Iterate until it works.

---

## Purpose

The UV (undervoltage) and OV (overvoltage) comparators continuously monitor the PVDD output and flag abnormal conditions:

- **UV comparator:** Asserts `uv_flag` when PVDD drops below ~4.3V. This triggers mode transitions (e.g., switching from active regulation to bypass mode) and system-level resets.
- **OV comparator:** Asserts `ov_flag` when PVDD rises above ~5.5V. This flags abnormal overshoot conditions that could damage downstream circuits.

Both comparators need hysteresis to avoid chattering when PVDD hovers near a threshold. They must operate with low power (< 5 uA each) since they are always on.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `pvdd` | Input (sense) | 0-6V | PVDD output being monitored |
| `vref` | Input | 1.226V | Bandgap reference for threshold generation |
| `uv_flag` | Output | Digital (0/PVDD) | Undervoltage flag: HIGH when PVDD < UV threshold |
| `ov_flag` | Output | Digital (0/PVDD) | Overvoltage flag: HIGH when PVDD > OV threshold |
| `vdd_comp` | Supply | PVDD or BVDD | Comparator supply (must work even when PVDD is low) |
| `gnd` | Supply | 0V | Ground |
| `en` | Input | Digital | Enable signal (can be disabled in POR mode) |

**Connections in the LDO:**
- `pvdd` connects to the PVDD output rail.
- `vref` connects to the ideal V_AVBG bandgap (1.226V).
- `uv_flag` and `ov_flag` connect to mode control logic (Block 08).
- Flags may also be level-shifted (Block 06) to the SVDD domain for digital readout.

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
| Temperature range | -40 | 27 | 150 | C | |
| Threshold accuracy over PVT | -- | -- | +/-10 | % | From nominal |

---

## Topology

**Continuous-time comparator with built-in Schmitt trigger hysteresis.** Two separate comparators share the same architecture.

### Threshold Generation

The comparators do not monitor PVDD directly against a fixed reference. Instead, PVDD is scaled down via a resistive divider to the reference level, and compared to V_REF:

**UV comparator:**
```
PVDD ---[R_uv_top]---+---[R_uv_bot]--- GND
                      |
                    V_uv_sense (~1.226V when PVDD = 4.3V)
                      |
                  [Comparator] (+) = V_uv_sense
                               (-) = V_REF (1.226V)
```

Divider ratio: R_bot / (R_top + R_bot) = V_REF / V_UV_threshold = 1.226 / 4.3 = 0.2851

**OV comparator:**
```
PVDD ---[R_ov_top]---+---[R_ov_bot]--- GND
                      |
                    V_ov_sense (~1.226V when PVDD = 5.5V)
                      |
                  [Comparator] (+) = V_REF (1.226V)
                               (-) = V_ov_sense
```

Divider ratio: R_bot / (R_top + R_bot) = V_REF / V_OV_threshold = 1.226 / 5.5 = 0.2229

### Comparator Core

A simple differential pair with positive feedback for hysteresis:

```
              VDD_comp
               |
         ┌─────┴─────┐
       [M3p]       [M4p]     PMOS loads (cross-coupled for hysteresis)
         |           |
    in+ ─┤           ├─ in-
       [M1n]       [M2n]     NMOS differential pair
         └─────┬─────┘
             [Mtail]          Tail current
               |
              GND
```

**Hysteresis mechanism:** Cross-couple M3 and M4 with a sizing imbalance. When the comparator switches, the positive feedback from the cross-coupled pair shifts the effective threshold by the hysteresis amount. The hysteresis voltage is set by the ratio of the cross-coupled pair W/L to the input pair W/L.

Alternatively, use a simpler approach: **Schmitt trigger inverter** on the comparator output, feeding back a small current to the input divider through a switched resistor. When the output flips, the feedback resistor shifts the threshold.

---

## Device Selection

| Component | Device | Parameters |
|-----------|--------|-----------|
| Comparator diff pair (NMOS) | `sky130_fd_pr__nfet_g5v0d10v5` | W=5u, L=2u |
| Comparator loads (PMOS) | `sky130_fd_pr__pfet_g5v0d10v5` | W=2u, L=2u (with cross-coupling) |
| Tail current source | `sky130_fd_pr__nfet_g5v0d10v5` | W=2u, L=4u, biased for 2 uA |
| Threshold divider resistors | `sky130_fd_pr__res_xhigh_po` | Sized for ~5 uA divider current |
| Hysteresis feedback resistor | `sky130_fd_pr__res_xhigh_po` | Large value (>1 Mohm) |
| Output inverter | `sky130_fd_pr__nfet_g5v0d10v5` / `sky130_fd_pr__pfet_g5v0d10v5` | Standard CMOS inverter |

**SPICE instantiation example:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

* UV threshold divider
* Ratio = 0.2851, total R ~ 250 kohm for ~5 uA current
* R_bot = 71.3 kohm, R_top = 178.7 kohm
XR_uv_top pvdd v_uv_sense sky130_fd_pr__res_xhigh_po W=1u L=89u
XR_uv_bot v_uv_sense gnd  sky130_fd_pr__res_xhigh_po W=1u L=36u

* UV comparator differential pair
XM1 out_n v_uv_sense tail gnd sky130_fd_pr__nfet_g5v0d10v5 W=5u L=2u nf=1
XM2 out_p vref       tail gnd sky130_fd_pr__nfet_g5v0d10v5 W=5u L=2u nf=1

* Tail current source (2 uA)
XMtail tail vbn gnd gnd sky130_fd_pr__nfet_g5v0d10v5 W=2u L=4u nf=1

* Cross-coupled PMOS loads (for hysteresis)
XM3 out_n out_p pvdd pvdd sky130_fd_pr__pfet_g5v0d10v5 W=2u L=2u nf=1
XM4 out_p out_n pvdd pvdd sky130_fd_pr__pfet_g5v0d10v5 W=3u L=2u nf=1
```

---

## Sizing Procedure

1. **Step 1: Design the threshold dividers.** Calculate R_top and R_bot for each comparator using the target thresholds and V_REF = 1.226V. Use `sky130_fd_pr__res_xhigh_po`. Verify the actual resistance in simulation (R/sq may differ from estimate).

2. **Step 2: Verify divider accuracy.** Apply PVDD = threshold voltage. Measure V_sense. It should equal V_REF (1.226V). Adjust resistor L values until exact.

3. **Step 3: Design comparator core.** Size the differential pair for offset < threshold_accuracy / divider_gain. At the divider ratio of ~0.25, a 25 mV offset at the comparator input translates to ~100 mV threshold error. Want offset < 10 mV, so W*L > 20 um^2 for each input device.

4. **Step 4: Set tail current.** 2-4 uA for low power. This gives gm ~ 30-60 uA/V, adequate for the < 5 us response time target.

5. **Step 5: Size cross-coupled loads for hysteresis.** The hysteresis voltage (referred to the input) depends on the ratio of the cross-coupled pair size imbalance. Start with M3:M4 width ratio of 1:1.5. Simulate: sweep PVDD up and down, measure the difference between rising and falling thresholds. Adjust the ratio until hysteresis = 50-100 mV at PVDD.

6. **Step 6: Add output buffer.** The comparator output may not be rail-to-rail. Add a CMOS inverter (HV devices) to produce clean 0/PVDD logic levels.

7. **Step 7: PVT sweep.** Verify thresholds and hysteresis across SS/FF/SF/FS and -40/27/150C. The UV threshold variation should stay within 4.0-4.5V; OV within 5.25-5.7V.

---

## Testbench Requirements

| Testbench File | Measures | Key Setup |
|---------------|----------|-----------|
| `tb_uv_threshold.spice` | UV trip point (PVDD falling and rising) | Slow PVDD ramp down and back up, measure flag transitions |
| `tb_ov_threshold.spice` | OV trip point (PVDD rising and falling) | Slow PVDD ramp up and back down, measure flag transitions |
| `tb_uvov_hyst.spice` | Hysteresis measurement for both comparators | PVDD triangle wave, measure both trip points |
| `tb_uvov_delay.spice` | Response time from threshold crossing to flag | Fast PVDD step through threshold, measure delay |
| `tb_uvov_corners.spice` | Thresholds at SS/FF/SF/FS, -40/27/150C | Parametric PVT sweep |
| `tb_uvov_power.spice` | Quiescent current of both comparators | DC measurement at PVDD = 5V |

---

## Simulation Procedure

**PDK include:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

**UV threshold measurement (slow ramp):**
```spice
* Ramp PVDD from 5.5V down to 3.5V and back up
Vpvdd pvdd gnd PWL(0 5.5 100u 3.5 200u 5.5)
Vref vref gnd 1.226

* UV comparator circuit here...

.tran 0.1u 200u

.control
run
plot v(pvdd) v(uv_flag)
* Find threshold: where uv_flag crosses 50% of PVDD
meas tran uv_fall_time when v(uv_flag)=2.5 rise=1
meas tran uv_rise_time when v(uv_flag)=2.5 fall=1
meas tran uv_fall_v find v(pvdd) at=uv_fall_time
meas tran uv_rise_v find v(pvdd) at=uv_rise_time
let hysteresis = uv_rise_v - uv_fall_v
print uv_fall_v uv_rise_v hysteresis
.endc
```

**Convergence options:**
```spice
.option reltol=1e-4
.option abstol=1e-12
.option gmin=1e-12
.option method=gear
```

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
| Output swings to 0 and PVDD (rail-to-rail) | Yes |
| No oscillation or metastability at threshold | Clean switching with hysteresis |

---

## Dependencies

**Wave 1 block — no dependencies on other blocks for standalone design.**

The comparators can be designed and tested independently. In top integration (Block 10), the UV/OV flags connect to the mode control logic (Block 08).

---

## Deliverables

1. `design.cir` — UV and OV comparator subcircuits. Definitions:
   - `.subckt uv_comparator pvdd vref uv_flag vdd_comp gnd en`
   - `.subckt ov_comparator pvdd vref ov_flag vdd_comp gnd en`
2. `tb_uv_threshold.spice` — UV threshold testbench
3. `tb_ov_threshold.spice` — OV threshold testbench
4. `tb_uvov_hyst.spice` — Hysteresis testbench
5. `tb_uvov_delay.spice` — Response time testbench
6. `tb_uvov_corners.spice` — PVT corner sweep testbench
7. `tb_uvov_power.spice` — Power consumption testbench
8. `README.md` — Design report: threshold values, hysteresis data, corner variation, power, response time
9. `*.png` — Plots: PVDD ramp with flag transitions, hysteresis loop, corner threshold comparison
