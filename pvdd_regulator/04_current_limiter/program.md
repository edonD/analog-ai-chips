# Block 04: Current Limiter — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device (`sky130_fd_pr__pfet_g5v0d10v5`, `sky130_fd_pr__nfet_g5v0d10v5`, `sky130_fd_pr__res_*`, etc.). **No exceptions. No behavioral current limiters. No ideal comparators.**
2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** Only testbench stimulus and load elements may be ideal.
3. **ALL SIMULATIONS IN NGSPICE.** Fix convergence with `.option` settings — do not switch simulators.
4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.**
5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** Short-circuit simulations will stress convergence. Fix with `.option` settings and initial conditions, not by replacing the circuit.

---

## Purpose

The current limiter protects the HV PMOS pass device from destruction during output short-circuit or overload conditions. Without it, a shorted PVDD output would force the error amp to pull the pass device gate to GND (maximum drive), passing potentially hundreds of mA through the device and exceeding its safe operating area (SOA), causing thermal runaway or oxide breakdown.

The current limiter senses the output current flowing through the pass device and, when it exceeds a threshold (60-80 mA), clamps the error amp output to limit the gate drive. This caps the maximum output current regardless of load impedance.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Supply | 5.4-10.5V | Battery supply (same as pass device source) |
| `pvdd` | Sense | 5.0V regulated | Output node — monitors current indirectly |
| `gate` | In/Out | 0 to ~PVDD | Error amp output / pass device gate — clamped when limit hit |
| `gnd` | Supply | 0V | Ground |
| `ilim_flag` | Output | Digital | Current limit active flag (optional, for mode control) |

**Connections in the LDO:**
- The sense transistor source connects to BVDD (same as pass device source).
- The sense transistor gate connects to the same gate node as the pass device.
- The sense transistor drain connects to a sense resistor or mirror that detects the current.
- The clamp circuit acts on the `gate` node, preventing it from going below a threshold.

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Current limit threshold | 60 | 70 | 80 | mA | 20-60% above 50 mA max load |
| Threshold accuracy over PVT | -- | -- | +/-20 | % | Acceptable for protection function |
| Response time | -- | -- | 10 | us | From overcurrent event to clamping |
| Sense transistor area overhead | -- | -- | 5 | % | Fraction of main pass device W |
| Quiescent current overhead | -- | -- | 10 | uA | Under normal (non-limiting) operation |
| Voltage headroom consumed | -- | -- | 50 | mV | Additional dropout from sense element |
| Fold-back ratio (optional) | -- | 0.5 | -- | -- | Ilim at Vout=0 / Ilim at Vout=5V |
| Temperature range | -40 | 27 | 150 | C | |

---

## Topology

**Sense transistor mirror with threshold comparator.**

The current limiter uses a scaled replica of the pass device to sense the output current without inserting a resistor in the main current path (which would increase dropout voltage).

```
    BVDD
     |                    |
     S                    S
    [Mpass]              [Msense]     (W_sense = W_pass / N, same L)
     G----+----G          G----+
     D    |               D    |
     |    |               |    |
    PVDD  gate           [Rsense]
                          |
                         [Comparator] ---> clamp gate node
                          |
                         GND
```

**How it works:**
1. `Msense` is a replica of `Mpass` with W scaled down by factor N (e.g., N = 100). Same gate voltage, same Vgs, same Vds (approximately).
2. `Isense = Ipass / N` (by current mirror ratio).
3. `Rsense` converts Isense to a voltage: Vsense = Isense * Rsense.
4. When Vsense exceeds a threshold (set by a reference or a diode-connected device), the comparator activates the clamp.
5. The clamp pulls the gate node toward BVDD (turning off the PMOS pass device), limiting the current.

**Mirror ratio N = 100:** For Ipass = 70 mA (limit), Isense = 0.7 mA. With Rsense = 1 kohm, Vsense = 0.7V — detectable with a simple threshold (Vth of a diode-connected NMOS).

**Optional fold-back:** Add Vout-dependent offset to the threshold so the limit decreases as Vout drops. This reduces power dissipation in the pass device during sustained shorts (Pdiss = (BVDD - Vout) * Ilim — worst at Vout = 0 with high Ilim).

---

## Device Selection

| Component | Device | Parameters |
|-----------|--------|-----------|
| Sense transistor | `sky130_fd_pr__pfet_g5v0d10v5` | W = W_pass / N, same L as pass device |
| Sense resistor | `sky130_fd_pr__res_xhigh_po` | ~1-5 kohm |
| Threshold reference (diode-connected) | `sky130_fd_pr__nfet_g5v0d10v5` | Sized for Vth ~ 0.7V at Isense |
| Clamp transistor | `sky130_fd_pr__pfet_g5v0d10v5` | Pulls gate toward BVDD when limit activated |
| Comparator devices | `sky130_fd_pr__nfet_g5v0d10v5` / `sky130_fd_pr__pfet_g5v0d10v5` | Simple differential pair or inverter |

**SPICE instantiation example:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

* Sense transistor — 1/100th of pass device
* If Mpass is W=5000u L=0.5u, then Msense is W=50u L=0.5u
XMsense sense_drain gate bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 W=50u L=0.5u nf=2

* Sense resistor — converts sense current to voltage
XRsense sense_drain sense_node sky130_fd_pr__res_xhigh_po W=2u L=2u

* Threshold device — diode-connected NMOS as voltage reference
XMref sense_node sense_node gnd gnd sky130_fd_pr__nfet_g5v0d10v5 W=5u L=1u nf=1

* Clamp PMOS — activated when Vsense > Vth_ref
XMclamp gate clamp_ctrl bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 W=10u L=1u nf=1
```

---

## Sizing Procedure

1. **Step 1: Determine pass device W.** From Block 01, get the final pass device W/L. Example: W_pass = 5000u, L = 0.5u.

2. **Step 2: Choose mirror ratio N.** N = 100 is a good starting point. Msense: W = 50u, L = 0.5u. Verify that Isense tracks Ipass accurately at the operating point (both devices in saturation, similar Vds).

3. **Step 3: Verify current mirroring.** Simulate: sweep Ipass from 0 to 100 mA (by sweeping gate voltage). Plot Isense vs Ipass. The ratio should be close to 1:N. Note any deviation at high current (Msense may enter triode if Vds differs).

4. **Step 4: Choose Rsense.** At the limit current (70 mA), Isense = 0.7 mA. Want Vsense = Vth of threshold device (~0.7V for HV NMOS). So Rsense = 0.7V / 0.7mA = 1 kohm.

5. **Step 5: Design the threshold and clamp.** A simple approach: when Vsense > Vth of a diode-connected NMOS, the NMOS turns on and activates the clamp path. For more precision, use a differential comparator referencing a current from IREF.

6. **Step 6: Simulate the I-V limit curve.** Sweep Vout from 5V to 0V with a controlled current source as load. Measure the output I-V characteristic. Verify the current clamps at the target (60-80 mA).

7. **Step 7: Short-circuit transient.** Apply a step from Rload = 100 ohm (50 mA) to Rload = 0.1 ohm (near short). Verify the current limiter activates within 10 us and clamps the current.

8. **Step 8: Verify no interference at normal loads.** At Iload = 0 to 50 mA, the current limiter must be completely inactive. It should add negligible voltage drop or noise to the output. Check that Vsense stays well below the threshold at 50 mA.

9. **Step 9: PVT sweep.** The current limit threshold will vary with process (Vth variation) and temperature (mobility variation). Verify 60-80 mA limit holds across corners. +/-20% is acceptable for protection.

---

## Testbench Requirements

| Testbench File | Measures | Key Setup |
|---------------|----------|-----------|
| `tb_ilim_dc.spice` | Output I-V curve showing current limiting | Sweep Rload from high to ~0, plot Iout vs Vout |
| `tb_ilim_mirror.spice` | Sense mirror accuracy (Isense vs Ipass) | Sweep gate voltage, measure both currents |
| `tb_ilim_short.spice` | Transient response to output short-circuit | Step Rload from 100 ohm to 0.1 ohm, measure Iout vs time |
| `tb_ilim_threshold.spice` | Exact current limit trip point | Fine sweep near trip point |
| `tb_ilim_corners.spice` | Limit threshold across PVT | SS/FF/SF/FS at -40/27/150C |
| `tb_ilim_normal.spice` | Verify no impact on normal operation (0-50 mA) | Loop closed, load from 0 to 50 mA, compare PVDD with/without limiter |

---

## Simulation Procedure

**PDK include:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

**Current limit I-V curve:**
```spice
.include "../00_error_amp/design.cir"
.include "../01_pass_device/design.cir"
.include "../02_feedback_network/design.cir"
.include "../03_compensation/design.cir"

* Full LDO loop with current limiter
V_BVDD bvdd gnd 7.0
V_REF  vref gnd 1.226
I_BIAS pvdd ibias 1u

Xea   vref vfb gate pvdd gnd ibias en error_amp
Xpass gate bvdd pvdd pass_device
Xfb   pvdd vfb gnd feedback_network
Xcomp gate pvdd gnd compensation

* Current limiter under test
XMsense sd gate bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 W=50u L=0.5u nf=2
XRsense sd gnd sky130_fd_pr__res_xhigh_po W=2u L=2u

Cload pvdd gnd 200p
Ven en gnd 5.0

* Sweep load current
Iload gnd pvdd 0

.dc Iload 0 120m 0.5m

.control
run
plot v(pvdd) vs -i(Iload)
plot -i(V_BVDD) vs -i(Iload)
wrdata ilim_iv.csv v(pvdd) -i(V_BVDD)
.endc
```

**Convergence options (short-circuit sims need help):**
```spice
.option reltol=1e-3
.option abstol=1e-10
.option vntol=1e-4
.option gmin=1e-10
.option method=gear
.option itl1=1000
.option itl4=500
```

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Current limit clamps at | 60-80 mA at TT 27C |
| Current limit at SS 150C (worst) | >= 50 mA (must not limit below max load) |
| Current limit at FF -40C (best) | <= 100 mA (must actually limit) |
| Response time to short | < 10 us |
| Impact on PVDD at Iload = 50 mA | < 10 mV difference vs no-limiter |
| Sense transistor quiescent current | < 10 uA at Iload = 0 |
| No oscillation during current limiting | Transient is clean, no ringing |
| Loop stability unaffected | PM still > 45 deg with limiter in circuit (at normal loads) |

---

## Dependencies

**Wave 2 block — requires:**
- Block 00 (error amp) — needed for closed-loop current limiting behavior
- Block 01 (pass device) — the sense transistor must match the pass device (same type, same L)
- Block 02 (feedback network) — needed for closed-loop testing
- Block 03 (compensation) — needed for stability verification with limiter

The sense transistor sizing directly depends on the pass device W/L from Block 01.

---

## Deliverables

1. `design.cir` — Current limiter subcircuit. Definition: `.subckt current_limiter gate bvdd pvdd gnd ilim_flag`
2. `tb_ilim_dc.spice` — Output I-V curve testbench
3. `tb_ilim_mirror.spice` — Sense mirror accuracy testbench
4. `tb_ilim_short.spice` — Short-circuit transient testbench
5. `tb_ilim_threshold.spice` — Trip point measurement testbench
6. `tb_ilim_corners.spice` — PVT corner sweep testbench
7. `tb_ilim_normal.spice` — Normal operation impact testbench
8. `README.md` — Design report: mirror ratio, limit threshold, I-V curve, transient response, corner data
9. `*.png` — Plots: I-V limit curve, transient short-circuit response, corner comparison
