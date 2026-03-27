# Block 02: Feedback Network — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** Every resistor must be an instantiated Sky130 device (`sky130_fd_pr__res_xhigh_po`, `sky130_fd_pr__res_high_po`, etc.). **No ideal resistors in the design. No R=308k behavioral elements.**
2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** The ONLY ideal components allowed are: supply sources for testbenches and testbench stimulus elements.
3. **ALL SIMULATIONS IN NGSPICE.** Fix convergence with `.option` settings — do not switch simulators.
4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.** The divider ratio must be measured in simulation, not assumed from hand calculation.
5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** Sky130 PDK resistors have non-zero TC and process variation. Characterize them; do not ignore them.

---

## Purpose

The feedback network is a resistive voltage divider that scales the PVDD output (5.0V) down to the bandgap reference level (1.226V) for comparison in the error amplifier. The divider ratio directly sets the regulated output voltage:

```
V_PVDD = V_REF * (R_TOP + R_BOT) / R_BOT = 1.226V * (1 / 0.2452) = 5.0V
```

The feedback network determines:
1. **Output voltage accuracy** — ratio errors translate directly to PVDD errors.
2. **Temperature coefficient of PVDD** — if R_TOP and R_BOT have different TCs, the ratio drifts with temperature.
3. **Quiescent current** — divider current flows from PVDD to GND continuously.
4. **Noise** — resistor thermal noise injects directly at the error amp input.
5. **Bandwidth** — parasitic capacitance at the V_FB node creates a pole that can affect loop stability.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `pvdd` | Input | 5.0V regulated | Top of divider — connected to PVDD output |
| `vfb` | Output | ~1.226V | Divider midpoint — connected to error amp negative input |
| `gnd` | Supply | 0V | Bottom of divider |

**Connections in the LDO:**
- `pvdd` connects to the PVDD output rail (drain of pass device, Block 01).
- `vfb` connects to the error amp inverting input (`vfb` on Block 00).
- The compensation network (Block 03) may also connect at or near the `vfb` node.

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Divider ratio (R_BOT / (R_TOP + R_BOT)) | 0.2440 | 0.2452 | 0.2465 | -- | Sets PVDD = 5.0V +/- 25mV from ratio alone |
| R_TOP | -- | 308 | -- | kohm | Approximate; actual value set by available R/sq |
| R_BOT | -- | 100 | -- | kohm | Approximate |
| Total divider resistance | 350 | 408 | 500 | kohm | Sets quiescent current |
| Divider current | 10 | 12.3 | 15 | uA | From PVDD to GND |
| Ratio TC (matched) | -- | -- | 50 | ppm/C | Should be near-zero with matched resistor types |
| Noise at vfb (integrated, 1Hz-1MHz) | -- | -- | 50 | uVrms | Thermal noise of divider |
| Parasitic capacitance at vfb | -- | -- | 2 | pF | Estimated; from resistor body caps |
| Temperature range | -40 | 27 | 150 | C | |

---

## Topology

**Simple two-resistor voltage divider** using matched polysilicon resistors.

```
    PVDD (5.0V)
     |
    [R_TOP  ~308 kohm]   sky130_fd_pr__res_xhigh_po
     |
    vfb (~1.226V)  -----> to error amp (-)
     |
    [R_BOT  ~100 kohm]   sky130_fd_pr__res_xhigh_po
     |
    GND
```

**Why `sky130_fd_pr__res_xhigh_po`:**
1. Extra-high-resistance polysilicon: ~2000 ohm/sq. Can implement 100 kohm in ~50 squares — manageable area.
2. Low temperature coefficient compared to diffusion resistors.
3. Matching: using the same resistor type for both R_TOP and R_BOT means the ratio TC is near-zero (TC of ratio = TC mismatch between identical resistor types, which cancels to first order).

**Implementation with unit resistors:** For best matching, build both R_TOP and R_BOT from series-connected identical unit resistors. Example: R_UNIT = 10 kohm. R_BOT = 10 units. R_TOP = 30.78 units (round to 31 units, giving ratio = 10/41 = 0.2439, PVDD = 5.027V — needs trimming or fractional unit).

Better approach: choose R_UNIT so the ratio comes out exact. With R_BOT = 10 * R_UNIT and R_TOP = 30.78 * R_UNIT, we need a fractional unit. Instead: use R_BOT = 13 * R_UNIT, R_TOP = 40 * R_UNIT. Ratio = 13/53 = 0.24528. PVDD = 1.226 / 0.24528 = 4.999V. Close enough.

**The exact ratio will be finalized during simulation** by sweeping R values and measuring V_FB at PVDD = 5.0V.

---

## Device Selection

| Component | Device | Parameters |
|-----------|--------|-----------|
| R_TOP | `sky130_fd_pr__res_xhigh_po` | W=1u, L=TBD for target resistance |
| R_BOT | `sky130_fd_pr__res_xhigh_po` | W=1u, L=TBD for target resistance |

**SPICE instantiation example:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

* Feedback divider — xhigh_po resistors
* R = rsh * L / W where rsh ~ 2000 ohm/sq for xhigh_po
* For R_TOP ~ 308 kohm: L/W = 154, so L = 154u at W = 1u
* For R_BOT ~ 100 kohm: L/W = 50, so L = 50u at W = 1u

XR_top pvdd  vfb sky130_fd_pr__res_xhigh_po W=1u L=154u
XR_bot vfb   gnd sky130_fd_pr__res_xhigh_po W=1u L=50u
```

**IMPORTANT:** The actual R/sq of `sky130_fd_pr__res_xhigh_po` must be verified from the PDK model. The value ~2000 ohm/sq is approximate. Run a single-resistor testbench to calibrate L for the desired resistance BEFORE building the full divider.

---

## Sizing Procedure

1. **Step 1: Characterize R/sq.** Instantiate `sky130_fd_pr__res_xhigh_po` with W=1u, L=10u. Apply 1V across it, measure current. Calculate R = V/I. Derive R/sq = R * W / L.

2. **Step 2: Calculate L for R_BOT.** R_BOT = 100 kohm (target). L_BOT = R_BOT * W / R_sq. Example: if R_sq = 2000 ohm/sq and W = 1u, then L_BOT = 100k * 1u / 2000 = 50u.

3. **Step 3: Calculate L for R_TOP.** For exact ratio: R_TOP = R_BOT * (V_PVDD / V_REF - 1) = 100k * (5.0/1.226 - 1) = 100k * 3.078 = 307.8 kohm. L_TOP = 307.8k * 1u / 2000 = 153.9u.

4. **Step 4: Simulate the divider.** Apply PVDD = 5.0V, measure V_FB. Adjust L_TOP or L_BOT to get V_FB = 1.226V exactly. This accounts for non-ideal effects in the PDK model (end effects, contact resistance, etc.).

5. **Step 5: Temperature sweep.** Sweep -40 to 150C. Measure V_FB at each temperature. The ratio should be nearly constant if both resistors are the same type.

6. **Step 6: Corner sweep.** Simulate at SS, FF, SF, FS. Record ratio variation.

7. **Step 7: Noise analysis.** Run `.noise` analysis at the V_FB node. The thermal noise of the divider directly adds to the error amp input noise.

---

## Testbench Requirements

| Testbench File | Measures | Key Setup |
|---------------|----------|-----------|
| `tb_fb_ratio.spice` | DC divider ratio at PVDD = 5.0V | Measure V_FB, compute ratio = V_FB / PVDD |
| `tb_fb_tc.spice` | Ratio vs temperature (-40 to 150C) | `.temp` sweep, measure V_FB at each temperature |
| `tb_fb_corners.spice` | Ratio at SS/FF/SF/FS corners | Corner sweep |
| `tb_fb_noise.spice` | Noise spectral density and integrated noise at V_FB | `.noise` analysis, 1 Hz to 10 MHz |
| `tb_fb_resistance.spice` | Absolute resistance of R_TOP and R_BOT | Separate DC measurement of each resistor |

---

## Simulation Procedure

**PDK include:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

**DC ratio measurement:**
```spice
Vpvdd pvdd gnd 5.0

XR_top pvdd vfb sky130_fd_pr__res_xhigh_po W=1u L=154u
XR_bot vfb  gnd sky130_fd_pr__res_xhigh_po W=1u L=50u

.op

.control
run
print v(vfb)
let ratio = v(vfb) / 5.0
print ratio
let vpvdd_result = 1.226 / ratio
print vpvdd_result
.endc
```

**Temperature coefficient:**
```spice
.dc temp -40 150 5

.control
run
let ratio = v(vfb) / 5.0
plot ratio vs temperature
wrdata fb_ratio_vs_temp.csv ratio
.endc
```

**Noise analysis:**
```spice
.noise v(vfb) Vpvdd dec 50 1 10meg

.control
run
setplot noise1
plot onoise_spectrum
meas ac noise_1k find onoise_spectrum at=1e3
.endc
```

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| V_FB at PVDD=5.0V, TT 27C | 1.226V +/- 1mV (adjust L until exact) |
| V_FB variation over -40 to 150C | < 5 mV (ratio TC < 50 ppm/C) |
| V_FB variation across SS/FF corners | < 10 mV |
| Divider current | 10-15 uA (not too much quiescent, not too little for noise) |
| Integrated noise at vfb (1Hz-1MHz) | < 50 uVrms |
| No model errors | All testbenches run in ngspice without errors |

---

## Dependencies

**Wave 2 block — needs Block 00 (error amp) for closed-loop verification.**

The feedback network itself has no circuit dependencies — it is just two resistors. However, it should be verified in the closed loop with Block 00 and Block 01 to confirm that the ratio produces the correct PVDD output. For standalone testing, an ideal 5V source on PVDD is sufficient.

---

## Deliverables

1. `design.cir` — Feedback divider subcircuit. Definition: `.subckt feedback_network pvdd vfb gnd`
2. `tb_fb_ratio.spice` — DC ratio testbench
3. `tb_fb_tc.spice` — Temperature coefficient testbench
4. `tb_fb_corners.spice` — Corner sweep testbench
5. `tb_fb_noise.spice` — Noise analysis testbench
6. `tb_fb_resistance.spice` — Absolute resistance measurement testbench
7. `README.md` — Design report: final R values, ratio, TC data, noise analysis, corner results
8. `*.png` — Plots: ratio vs temperature, noise spectrum
