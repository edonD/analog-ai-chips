# Block 07: Zener Clamp — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** Every diode and transistor must be an instantiated Sky130 device (`sky130_fd_pr__diode_pw2nd_05v5`, `sky130_fd_pr__diode_pd2nw_05v5`, `sky130_fd_pr__nfet_g5v0d10v5`, etc.). **No exceptions. No ideal Zener diodes. No behavioral clamp models.**
2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** Only testbench stimulus and supply sources may be ideal.
3. **ALL SIMULATIONS IN NGSPICE.** Fix convergence with `.option` settings — do not switch simulators.
4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.**
5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** Sky130 does not have true Zener diodes. You must build the clamp from available devices. This requires creative circuit design.

---

## Purpose

The Zener clamp protects the PVDD output from voltage transients and overshoot conditions. In an automotive environment, events such as load dump (BVDD spike to 40V+), fast BVDD ramps, and inductive switching can cause PVDD to overshoot beyond 5.5V. The clamp limits the maximum voltage on PVDD by shunting excess current to ground when the voltage exceeds the clamp threshold.

**Protection scenarios:**
1. **Load dump transient:** BVDD spikes, error amp cannot respond fast enough, PVDD overshoots.
2. **Startup overshoot:** During power-up, the error amp may be slow to respond, allowing PVDD to overshoot.
3. **ESD event:** External ESD pulse coupled to PVDD pin.
4. **Pass device gate stuck low:** If the error amp fails, pass device is fully ON, PVDD = BVDD.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `pvdd` | Input/Output | 5-6V | PVDD output node — the node being clamped |
| `gnd` | Supply | 0V | Ground — clamp current sink |

**Connections in the LDO:**
- `pvdd` connects directly to the PVDD output rail.
- The clamp sits in parallel with the load capacitor and feedback divider.
- It is passive — draws zero current under normal conditions (PVDD < clamp threshold).

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Clamp voltage (onset) | 5.5 | 5.8 | 6.2 | V | Voltage at which significant current starts flowing |
| Clamp voltage at 10 mA | -- | 6.0 | 6.5 | V | Should not exceed this at 10 mA clamp current |
| Leakage at PVDD = 5.0V | -- | -- | 1 | uA | Must not affect quiescent current budget |
| Leakage at PVDD = 5.17V (max regulated) | -- | -- | 5 | uA | Must not interfere with regulation |
| Peak current capability | 100 | -- | -- | mA | During transient event (pulse, not DC) |
| Clamp impedance above threshold | -- | -- | 50 | ohm | Low impedance for effective clamping |
| Area | -- | -- | 5000 | um^2 | Compact; original was 4096 um^2 |
| Temperature range | -40 | 27 | 150 | C | |

---

## Topology

Sky130 does not have dedicated Zener diodes. Three approaches are available:

### Option A: Diode Stack (Recommended Starting Point)

Stack multiple forward-biased diodes in series between PVDD and GND. Each PN junction drops ~0.6-0.7V. For a clamp at ~5.8V, stack 9 diodes: 9 * 0.65V = 5.85V.

```
    PVDD
     |
    [D1] (forward biased at clamp)
     |
    [D2]
     |
    [D3]
     |
    ... (9 diodes total)
     |
    [D9]
     |
    GND
```

**Pros:** Simple, predictable, symmetric I-V.
**Cons:** Vf has negative TC (~-2 mV/C per diode). At 150C, clamp drops to ~5.1V (9 * 0.57V) — too close to PVDD nominal. At -40C, clamp rises to ~6.3V (9 * 0.70V).

**TC mitigation:** Mix diode types or add a series resistor. Or reduce to 8 diodes and accept a slightly lower clamp threshold.

### Option B: MOSFET Clamp (Thick-Oxide NMOS)

Use a thick-oxide NMOS with gate connected through a resistive divider from PVDD:

```
    PVDD ---[R1]---+---[R2]--- GND
                   |
                  gate
                   |
                  [Mclamp]   sky130_fd_pr__nfet_g5v0d10v5
                  drain=PVDD, source=GND
```

When PVDD exceeds the divider threshold + Vth, Mclamp turns on and shunts current. The clamp voltage is set by: V_clamp = Vth * (R1 + R2) / R2.

**Pros:** Tunable threshold, sharper turn-on than diode stack.
**Cons:** Consumes static current through the divider. Active device — may interact with the LDO loop if not careful.

### Option C: Reverse-Biased Diode (Avalanche)

Use `sky130_fd_pr__diode_pw2nd_05v5` in reverse bias. The breakdown voltage of Sky130 5.5V diodes is specified at ~5.5V. Stack or use single diode.

**Caution:** The breakdown voltage of PDK diodes must be verified in simulation. The "05v5" in the device name refers to the maximum rated voltage, not the breakdown voltage. The actual breakdown may be higher.

**Start with Option A (diode stack). Fall back to Option B if temperature variation is unacceptable.**

---

## Device Selection

| Component | Device | Parameters |
|-----------|--------|-----------|
| Forward diode (Option A) | `sky130_fd_pr__diode_pw2nd_05v5` | Area sized for current capability |
| Forward diode (Option A alt) | `sky130_fd_pr__diode_pd2nw_05v5` | P-diff to N-well junction |
| Clamp NMOS (Option B) | `sky130_fd_pr__nfet_g5v0d10v5` | W=20u, L=0.5u for low Rds_on |
| Divider resistors (Option B) | `sky130_fd_pr__res_xhigh_po` | For threshold setting |

**SPICE instantiation example (diode stack):**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

* 9-diode stack from PVDD to GND
* sky130_fd_pr__diode_pw2nd_05v5: anode = P-well, cathode = N-diffusion
* Forward bias: anode = high, cathode = low
XD1 pvdd  n1 sky130_fd_pr__diode_pw2nd_05v5 area=32e-12 pj=32e-6
XD2 n1    n2 sky130_fd_pr__diode_pw2nd_05v5 area=32e-12 pj=32e-6
XD3 n2    n3 sky130_fd_pr__diode_pw2nd_05v5 area=32e-12 pj=32e-6
XD4 n3    n4 sky130_fd_pr__diode_pw2nd_05v5 area=32e-12 pj=32e-6
XD5 n4    n5 sky130_fd_pr__diode_pw2nd_05v5 area=32e-12 pj=32e-6
XD6 n5    n6 sky130_fd_pr__diode_pw2nd_05v5 area=32e-12 pj=32e-6
XD7 n6    n7 sky130_fd_pr__diode_pw2nd_05v5 area=32e-12 pj=32e-6
XD8 n7    n8 sky130_fd_pr__diode_pw2nd_05v5 area=32e-12 pj=32e-6
XD9 n8   gnd sky130_fd_pr__diode_pw2nd_05v5 area=32e-12 pj=32e-6
```

**Note:** The `area` and `pj` (perimeter) parameters set the diode size and current capability. `area=32e-12` corresponds to a 32 um^2 diode (e.g., 5.6u x 5.6u). Larger area = lower series resistance = higher current capability.

---

## Sizing Procedure

1. **Step 1: Characterize a single diode.** Instantiate one `sky130_fd_pr__diode_pw2nd_05v5` with area=32e-12. Sweep forward voltage from 0 to 1V, measure current. Record Vf at 1 mA, 10 mA, and the temperature coefficient.

2. **Step 2: Determine the number of diodes.** At the target clamp voltage (5.8V) and the forward drop per diode from Step 1, calculate N = V_clamp / Vf. Round to integer.

3. **Step 3: Simulate the full stack.** Instantiate N diodes in series. Sweep voltage across the stack from 0 to 7V. Plot I-V curve. Verify onset at the target voltage.

4. **Step 4: Temperature sweep.** Run the I-V curve at -40C, 27C, and 150C. The Vf drop per diode decreases ~2 mV/C. For 9 diodes over 190C range: shift = 9 * 2 mV * 190 = 3.4V total range. This is enormous — the diode stack may NOT work across the full temperature range without mitigation.

5. **Step 5: If TC is unacceptable, switch to Option B (MOSFET clamp).** Design the resistive divider and NMOS clamp. The MOSFET Vth has lower TC (~-1 mV/C) and the divider ratio is temperature-independent if matched resistors are used. Total TC may be manageable.

6. **Step 6: Verify leakage at normal PVDD.** At PVDD = 5.0V and 5.17V, the clamp must draw < 5 uA. For the diode stack, this means the voltage per diode (5.17V / 9 = 0.574V) must be below the diode turn-on voltage. Verify in simulation.

7. **Step 7: Transient test.** Apply a fast voltage ramp (10V/us) to PVDD through a low impedance. Verify the clamp limits the peak voltage.

8. **Step 8: Peak current test.** Apply PVDD = 7V through a current-limiting resistor. Measure clamp current. Verify the diodes can handle it without excessive heating (check power dissipation vs pulse width).

---

## Testbench Requirements

| Testbench File | Measures | Key Setup |
|---------------|----------|-----------|
| `tb_zener_iv.spice` | DC I-V characteristic of the clamp | Sweep voltage 0 to 7V, measure current |
| `tb_zener_diode_char.spice` | Single diode characterization (Vf, TC) | Sweep V, measure I at multiple temperatures |
| `tb_zener_transient.spice` | Clamping behavior during voltage spike | Fast ramp on PVDD, measure peak voltage |
| `tb_zener_leakage.spice` | Leakage at PVDD = 5.0V and 5.17V | DC measurement at normal operating voltage |
| `tb_zener_tc.spice` | Clamp voltage vs temperature | I-V curve at -40, 27, 85, 150C |
| `tb_zener_corners.spice` | Clamp voltage at SS/FF/SF/FS corners | Corner sweep |

---

## Simulation Procedure

**PDK include:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

**DC I-V curve:**
```spice
* Sweep voltage across the clamp stack
Vclamp pvdd gnd 0

.dc Vclamp 0 7 0.01

.control
run
plot -i(Vclamp) vs v(pvdd)
meas dc v_at_1mA find v(pvdd) when -i(Vclamp)=1m
meas dc v_at_10mA find v(pvdd) when -i(Vclamp)=10m
print v_at_1mA v_at_10mA
wrdata zener_iv.csv -i(Vclamp)
.endc
```

**Temperature sweep:**
```spice
.control
foreach temp_val -40 0 27 85 125 150
  set temp = $temp_val
  op
  dc Vclamp 0 7 0.01
  plot -i(Vclamp) vs v(pvdd)
  reset
end
.endc
```

**Convergence options:**
```spice
.option reltol=1e-3
.option abstol=1e-12
.option gmin=1e-12
```

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Clamp onset voltage at TT 27C | 5.5V to 6.2V (1 mA threshold) |
| Clamp voltage at 10 mA, TT 27C | < 6.5V |
| Leakage at PVDD = 5.0V, TT 27C | < 1 uA |
| Leakage at PVDD = 5.17V, TT 27C | < 5 uA |
| Clamp onset at 150C | > 5.0V (must not drag down normal PVDD) |
| Clamp onset at -40C | < 7.0V (must still provide protection) |
| Transient peak (10V/us ramp) | < 6.5V with 200pF Cload |
| Peak current at 7V | > 100 mA (pulse rating) |

---

## Dependencies

**Wave 3 block — can be designed in parallel with other protection blocks.**

No circuit-level dependencies. The clamp is a passive element connected in parallel with the PVDD output. However, when integrated into the full LDO (Block 10), verify that:
- The clamp leakage does not affect load regulation.
- The clamp does not oscillate with the LDO loop during OV events.

---

## Deliverables

1. `design.cir` — Zener clamp subcircuit. Definition: `.subckt zener_clamp pvdd gnd`
2. `tb_zener_iv.spice` — DC I-V characteristic testbench
3. `tb_zener_diode_char.spice` — Single diode characterization testbench
4. `tb_zener_transient.spice` — Transient clamping testbench
5. `tb_zener_leakage.spice` — Leakage measurement testbench
6. `tb_zener_tc.spice` — Temperature sweep testbench
7. `tb_zener_corners.spice` — Corner sweep testbench
8. `README.md` — Design report: topology chosen (diode stack vs MOSFET), clamp voltage, I-V curve, TC data, leakage data
9. `*.png` — Plots: I-V curve, I-V at multiple temperatures, transient clamping waveform
