# Block 03: Compensation Network — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** Every capacitor and resistor in the compensation network must be an instantiated Sky130 device (`sky130_fd_pr__cap_mim_m3_1`, `sky130_fd_pr__res_xhigh_po`, MOS caps, etc.). **No ideal capacitors. No ideal resistors. No behavioral elements.**
2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** Only testbench stimulus sources and load elements may be ideal.
3. **ALL SIMULATIONS IN NGSPICE.** Fix convergence with `.option` settings — do not switch simulators.
4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.** Phase margin must be measured from AC simulation, not estimated from hand analysis.
5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** This is the hardest block in the LDO. The output pole moves 1000x with load. You will need to iterate many times. Do not give up and use a behavioral model.

---

## Purpose

The compensation network ensures the PVDD LDO feedback loop is stable (phase margin > 45 degrees, gain margin > 10 dB) across ALL operating conditions:
- Load current: 0 mA (no load) to 50 mA (full load)
- Temperature: -40C to 150C
- Process corners: SS, TT, FF, SF, FS
- Input voltage: BVDD = 5.4V to 10.5V

**Why this is the hardest block:**

The LDO output pole is at: f_out = 1 / (2*pi * Rload * Cload)

| Load Current | Effective Rload | Output Pole Frequency |
|-------------|----------------|----------------------|
| 0 mA (no load) | ~infinity (leakage) | < 1 kHz |
| 100 uA | 50 kohm | ~16 kHz |
| 1 mA | 5 kohm | ~160 kHz |
| 10 mA | 500 ohm | ~1.6 MHz |
| 50 mA | 100 ohm | ~8 MHz |

The output pole moves by a factor of 1000x from no-load to full-load. A compensation scheme that works at one load point may be completely unstable at another. **The compensation must stabilize the loop at ALL load points simultaneously.**

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `vout_gate` | Connection | 0 to ~PVDD | Error amp output / pass device gate node |
| `pvdd` | Connection | 5.0V | PVDD output node |
| `gnd` | Supply | 0V | Ground |
| `vfb` | Connection | ~1.226V | Feedback node (optional, for lead compensation) |

**Connections in the LDO:**
- The compensation network connects between the error amp output (`vout_gate` from Block 00) and other nodes (PVDD, GND, or vfb) depending on the topology chosen.
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

## Topology

**Miller compensation (Type I)** is the recommended starting point. If insufficient, escalate to Type II or Type III.

### Strategy 1: Miller Compensation (Start Here)

Connect a capacitor (Cc) from the error amp output (`vout_gate`) to the PVDD output node. This creates a Miller effect that:
1. Pushes the dominant pole (gate pole) to lower frequency.
2. Pushes the output pole to higher frequency (pole splitting).

```
    Error Amp Output (vout_gate)
         |
        [Cc]  (Miller cap, ~5-50 pF)
         |
    PVDD output node
```

**Optional: series resistor for zero.** Add Rz in series with Cc to create a left-half-plane zero that boosts phase margin:

```
    vout_gate ---[Rz]---[Cc]--- pvdd
```

The zero is at: fz = 1 / (2*pi * Rz * Cc)

Place fz near the output pole at mid-load to help at both extremes.

### Strategy 2: Dominant-Pole Compensation (Backup)

If Miller compensation cannot stabilize across all loads, add a large capacitor at the error amp output to make the gate pole absolutely dominant:

```
    vout_gate ---[Cg]--- gnd    (Cg >> Cgs_pass)
```

This is simple but severely limits bandwidth and transient response.

### Strategy 3: Adaptive Bias (Advanced)

Sense the load current and increase the error amp bias at high loads. This moves the error amp pole out, tracking the output pole as it moves with load. This is how the best capless LDOs work, but adds complexity.

**Start with Strategy 1 (Miller + Rz). Only escalate if it fails across the full load range.**

---

## Device Selection

| Component | Device | Parameters |
|-----------|--------|-----------|
| Miller cap (Cc) | `sky130_fd_pr__cap_mim_m3_1` | W, L sized for 5-50 pF (~2 fF/um^2) |
| Series resistor (Rz) | `sky130_fd_pr__res_xhigh_po` | Value TBD (1-100 kohm range) |
| Extra gate cap (if needed) | MOS cap: `sky130_fd_pr__nfet_g5v0d10v5` as cap | Gate to source/drain/bulk shorted |

**SPICE instantiation example:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

* Miller compensation cap: 20 pF
* Area = C / density = 20pF / 2fF/um^2 = 10000 um^2
* W = 100u, L = 100u gives 10000 um^2 = 20 pF
XCc vout_gate_rz pvdd sky130_fd_pr__cap_mim_m3_1 W=100u L=100u

* Series zero resistor: 10 kohm
XRz vout_gate vout_gate_rz sky130_fd_pr__res_xhigh_po W=1u L=5u

* Alternative: MOS cap at gate (if dominant-pole approach needed)
* XCg vout_gate vout_gate gnd gnd sky130_fd_pr__nfet_g5v0d10v5 W=50u L=50u nf=1
```

**MIM cap sizing reference:**
| Target Capacitance | Area (um^2) | Example W x L |
|-------|------|------|
| 5 pF | 2,500 | 50u x 50u |
| 10 pF | 5,000 | 71u x 71u |
| 20 pF | 10,000 | 100u x 100u |
| 50 pF | 25,000 | 158u x 158u |

---

## Sizing Procedure

**IMPORTANT: This procedure requires completed Block 00 (error amp), Block 01 (pass device), and Block 02 (feedback network). You cannot size compensation without the full loop.**

1. **Step 1: Build the uncompensated loop.** Connect error amp + pass device + feedback divider + 200pF Cload. Apply V_REF = 1.226V. Set BVDD = 7V. NO compensation yet.

2. **Step 2: Measure uncompensated loop.** Break the loop at the feedback node (vfb). Inject AC stimulus. Run `.ac dec 100 1 100meg`. Measure loop gain and phase at Iload = 0, 1mA, 10mA, 50mA. Record pole locations and crossover frequency. **It WILL be unstable at some or all loads.**

3. **Step 3: Identify the poles.**
   - Gate pole: f_gate = 1 / (2*pi * Rout_EA * (Cgs_pass + Cc))
   - Output pole: f_out = gm_pass / (2*pi * Cload) at light load, or 1/(2*pi * Rload * Cload)
   - The problem: at no-load, output pole is slow (~kHz) and gate pole is fast. At full-load, output pole is fast (~MHz) and may collide with UGB.

4. **Step 4: Choose Cc.** Start with Cc = 10 pF. The Miller effect multiplies Cc by the pass device gain (gm_pass * Rload), creating a dominant pole at the gate. Simulate loop stability at all loads. Increase Cc if PM < 45 deg at light load. Decrease if bandwidth is too low.

5. **Step 5: Add Rz for zero.** If PM < 45 deg at some load (typically mid-load where poles are closest), add Rz in series with Cc. Choose Rz to place the zero near the problematic pole: fz = 1/(2*pi * Rz * Cc). Start with Rz = 1/(gm_pass) ~ 1/gm of pass device at mid-load. Simulate.

6. **Step 6: Sweep all loads.** Parametric sweep Rload from 100 ohm (50mA) to 100 kohm (50uA). Phase margin must be > 45 deg at EVERY point.

7. **Step 7: Corner/temperature sweep.** Run at SS/FF/SF/FS and -40/27/150C. The worst case is typically SS corner at 150C (lowest gm, slowest loop) or FF at -40C (highest gm, risk of ringing).

8. **Step 8: Transient verification.** Run load step (1mA to 10mA in 1us). Confirm no oscillation, undershoot < 150 mV, settling < 10 us. The AC analysis tells you PM; the transient tells you if the AC analysis was right.

9. **Step 9: Iterate.** If any condition fails, adjust Cc and Rz. If Miller compensation alone cannot stabilize all loads, consider:
   - Adding a second compensation path
   - Adding a feed-forward capacitor from vfb to vout_gate
   - Implementing adaptive biasing in the error amp
   - Using a cascode-compensated topology

---

## Testbench Requirements

| Testbench File | Measures | Key Setup |
|---------------|----------|-----------|
| `tb_comp_lstb.spice` | Loop gain and phase margin (LSTB method) | Break loop at vfb, AC sweep, measure T(s) = loop gain |
| `tb_comp_load_sweep.spice` | PM and GM vs load current | Parametric: Rload = 100, 500, 1k, 5k, 10k, 50k, 100k ohm |
| `tb_comp_pvt.spice` | PM at all 5 corners and 3 temperatures | 15 simulation runs minimum |
| `tb_comp_transient.spice` | Load step response (time domain) | 1mA -> 10mA and 10mA -> 1mA steps, 1us edge |
| `tb_comp_bode.spice` | Full Bode plot of open-loop transfer function | For design visualization and debugging |
| `tb_comp_bvdd_sweep.spice` | PM vs BVDD (5.4 to 10.5V) | Verify stability across input range |

**Critical: Loop-breaking technique for ngspice.** Use a large inductor (1GH) in series with vfb to break the DC loop while passing AC:

```spice
* Loop stability testbench (Middlebrook method simplified)
* Break the loop at the feedback node
Lbreak vfb_int vfb 1G
Cbreak vfb_int gnd 1G

* AC injection
Vac_inj vfb_int vfb_sense dc 0 ac 1

* The feedback divider connects pvdd to vfb_sense
* The error amp sees vfb
```

---

## Simulation Procedure

**PDK include:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

**Loop stability measurement (simplified break-loop):**
```spice
.include "../00_error_amp/design.cir"
.include "../01_pass_device/design.cir"
.include "../02_feedback_network/design.cir"

* Supplies
V_BVDD bvdd gnd 7.0
V_REF  vref gnd 1.226
I_BIAS pvdd ibias 1u

* Instantiate blocks
Xea  vref vfb vout_gate pvdd gnd ibias en error_amp
Xpass vout_gate bvdd pvdd pass_device

* Compensation (the block under test)
XCc vout_gate_rz pvdd sky130_fd_pr__cap_mim_m3_1 W=100u L=100u
XRz vout_gate vout_gate_rz sky130_fd_pr__res_xhigh_po W=1u L=5u

* Output load
Cload pvdd gnd 200p
Rload pvdd gnd 1k         * 5 mA operating point

* Feedback with loop break
Xfb pvdd vfb_sense gnd feedback_network
Lbreak vfb vfb_sense 1G
Vac vfb_sense vfb_ac dc 0 ac 1

* Enable
Ven en gnd 5.0

.ac dec 100 1 100meg

.control
run
let loop_gain_db = db(v(vfb_ac))
let loop_phase = 180/PI * ph(v(vfb_ac))
plot loop_gain_db loop_phase
meas ac pm find loop_phase when loop_gain_db=0
meas ac gm_cross find loop_gain_db when loop_phase=-180
let gm_db = -gm_cross
print pm gm_db
.endc
```

**Convergence options:**
```spice
.option reltol=1e-4
.option abstol=1e-12
.option vntol=1e-6
.option gmin=1e-12
.option method=gear
.option itl1=500
.option itl4=200
```

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
| Load transient undershoot (1mA -> 10mA) | < 150 mV |
| Load transient overshoot (10mA -> 1mA) | < 150 mV |
| Settling time | < 10 us to within 1% |
| No oscillation at any condition | Zero sustained ringing in any transient |

**If any single condition fails, the compensation is NOT done. Iterate.**

---

## Dependencies

**Wave 2 block — requires ALL of the following:**
- Block 00 (error amp) — `design.cir` must exist and simulate correctly
- Block 01 (pass device) — `design.cir` must exist with characterized Cgs, gm
- Block 02 (feedback network) — `design.cir` must exist with correct ratio

The compensation network cannot be designed in isolation. It is meaningless without the full loop.

---

## Deliverables

1. `design.cir` — Compensation network subcircuit. Definition: `.subckt compensation vout_gate pvdd gnd` (or `.subckt compensation vout_gate pvdd vfb gnd` if lead compensation is used)
2. `tb_comp_lstb.spice` — Loop stability testbench
3. `tb_comp_load_sweep.spice` — PM vs load parametric sweep
4. `tb_comp_pvt.spice` — PVT corner sweep
5. `tb_comp_transient.spice` — Load step transient testbench
6. `tb_comp_bode.spice` — Full Bode plot testbench
7. `tb_comp_bvdd_sweep.spice` — PM vs BVDD testbench
8. `README.md` — Design report: compensation topology chosen, Cc and Rz values, PM at every load/corner/temp data point, Bode plots, transient waveforms, explanation of why it works
9. `*.png` — Plots: Bode plot (gain + phase), PM vs load current graph, transient step responses, corner overlay plots
