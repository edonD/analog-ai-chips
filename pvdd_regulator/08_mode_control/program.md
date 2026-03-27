# Block 08: Mode Control — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device. The mode control uses HV devices (`sky130_fd_pr__nfet_g5v0d10v5`, `sky130_fd_pr__pfet_g5v0d10v5`) for BVDD-domain sensing and standard or HV devices for logic. **No exceptions. No behavioral state machines. No Verilog models.**
2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** Only testbench stimulus and supply sources may be ideal.
3. **ALL SIMULATIONS IN NGSPICE.** Fix convergence with `.option` settings — do not switch simulators.
4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.**
5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** Analog state machines with multiple thresholds and hysteresis are complex. Build incrementally and test each comparator before combining.

---

## Purpose

The mode control logic manages the PVDD regulator's operating mode based on the BVDD input voltage and enable signals. It implements the following state machine:

| # | Mode | BVDD Range | PVDD Output | What Happens |
|---|------|-----------|-------------|--------------|
| 1 | POR | 0 - 2.5V | OFF | Everything disabled. PVDD floats. |
| 2 | Retention bypass | 2.5 - 4.2V | BVDD | Pass device fully ON (gate pulled low). PVDD tracks BVDD. |
| 3 | Retention regulate | 4.2 - 4.5V | 4.1V | Error amp active, regulates to 4.1V target. Limits overshoot. |
| 4 | Power-up bypass | 4.5 - 5.0V | BVDD | Pass device fully ON for bridge driver startup. |
| 5 | Active regulate | > 5.6V | 5.0V | Full regulation. All specs guaranteed. |

**Mode transitions are triggered by BVDD crossing voltage thresholds.** The mode control generates output signals that configure the rest of the LDO:
- `bypass_en`: Shorts the pass device gate to GND (fully ON) for bypass modes.
- `ea_en`: Enables the error amplifier for regulation modes.
- `ref_sel`: Selects between 4.1V and 5.0V regulation targets.
- `uvov_en`: Enables UV/OV comparators (only in active mode).
- `ilim_en`: Enables current limiter.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Input (sense) | 0-10.5V | Battery supply being monitored |
| `pvdd` | Supply | 5.0V (when available) | Regulated supply (may not be present during startup) |
| `svdd` | Supply | 2.2V | Low-voltage digital supply |
| `gnd` | Supply | 0V | Ground |
| `en_ret` | Input | SVDD domain | Retention mode enable from system controller |
| `bypass_en` | Output | BVDD domain | Pass device bypass control (active: gate -> GND) |
| `ea_en` | Output | PVDD domain | Error amplifier enable |
| `ref_sel` | Output | PVDD domain | Reference select (0 = 5.0V target, 1 = 4.1V target) |
| `uvov_en` | Output | PVDD domain | UV/OV comparator enable |
| `ilim_en` | Output | PVDD domain | Current limiter enable |
| `mode[1:0]` | Output | SVDD domain | Mode status for digital readback |

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| BVDD threshold: POR -> retention bypass | 2.3 | 2.5 | 2.7 | V | Hysteresis: 200 mV |
| BVDD threshold: retention bypass -> regulate | 4.0 | 4.2 | 4.4 | V | Hysteresis: 200 mV |
| BVDD threshold: retention regulate -> powerup bypass | 4.3 | 4.5 | 4.7 | V | Hysteresis: 200 mV |
| BVDD threshold: powerup bypass -> active | 5.4 | 5.6 | 5.8 | V | Hysteresis: 200 mV |
| Comparator response time | -- | -- | 5 | us | For each threshold |
| Glitch-free transitions | Yes | -- | -- | -- | No output glitches during mode changes |
| Quiescent current (POR mode) | -- | -- | 1 | uA | Nearly zero in POR |
| Quiescent current (active mode) | -- | -- | 20 | uA | From BVDD |
| BVDD ramp rate tolerance | 0.1 | -- | 12 | V/us | Must handle slow and fast ramps |
| Temperature range | -40 | 27 | 150 | C | |

---

## Topology

The mode control is built from **four voltage comparators** sensing BVDD, plus **combinational logic** generating the output control signals.

### BVDD Threshold Comparators

Each comparator uses a resistive divider to scale BVDD down, then compares against a fixed reference (V_REF = 1.226V or a derived voltage). Since BVDD can be 0-10.5V, the comparators must use HV devices.

```
    BVDD ----[R_div_top]----+----[R_div_bot]---- GND
                            |
                          V_sense
                            |
                        [Comparator]  vs  V_threshold
                            |
                          output (digital)
```

**Threshold setting example (BVDD = 4.2V threshold):**
```
V_sense = BVDD * R_bot / (R_top + R_bot) = V_REF at threshold
R_bot / (R_top + R_bot) = 1.226 / 4.2 = 0.2919
```

Each comparator includes hysteresis (positive feedback) with ~200 mV hysteresis at the BVDD level.

### Four Comparators

| Comparator | BVDD Threshold | Divider Ratio | Purpose |
|-----------|---------------|---------------|---------|
| COMP_POR | 2.5V | 0.4904 | POR release |
| COMP_RET | 4.2V | 0.2919 | Retention regulate threshold |
| COMP_PUP | 4.5V | 0.2724 | Power-up bypass threshold |
| COMP_ACT | 5.6V | 0.2189 | Active regulation threshold |

### Combinational Logic

The four comparator outputs (COMP_POR, COMP_RET, COMP_PUP, COMP_ACT) form a thermometer code as BVDD ramps up. The combinational logic decodes this into the control outputs:

| COMP_POR | COMP_RET | COMP_PUP | COMP_ACT | Mode | bypass_en | ea_en | ref_sel | uvov_en |
|----------|----------|----------|----------|------|-----------|-------|---------|---------|
| 0 | 0 | 0 | 0 | POR | 0 | 0 | X | 0 |
| 1 | 0 | 0 | 0 | Ret bypass | 1 | 0 | X | 0 |
| 1 | 1 | 0 | 0 | Ret regulate | 0 | 1 | 1 (4.1V) | 0 |
| 1 | 1 | 1 | 0 | PU bypass | 1 | 0 | X | 0 |
| 1 | 1 | 1 | 1 | Active | 0 | 1 | 0 (5.0V) | 1 |

The logic is implemented using CMOS gates built from Sky130 devices. Since these signals are in the BVDD/PVDD domain, use HV devices for the gates.

---

## Device Selection

| Component | Device | Parameters |
|-----------|--------|-----------|
| Comparator diff pair (NMOS) | `sky130_fd_pr__nfet_g5v0d10v5` | W=5u, L=2u |
| Comparator loads (PMOS) | `sky130_fd_pr__pfet_g5v0d10v5` | W=2u, L=2u |
| Divider resistors | `sky130_fd_pr__res_xhigh_po` | Sized for ~5 uA per divider |
| Logic gates | `sky130_fd_pr__nfet_g5v0d10v5` / `sky130_fd_pr__pfet_g5v0d10v5` | CMOS inverters, NAND, NOR |
| Bypass switch (gate pulldown) | `sky130_fd_pr__nfet_g5v0d10v5` | W=20u, L=0.5u, pulls gate to GND |

**SPICE instantiation example (one comparator + divider):**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

* BVDD threshold comparator for 4.2V threshold
* Divider: ratio = 1.226/4.2 = 0.2919
* Total R = 250 kohm -> Idiv = BVDD/250k ~ 4-42 uA
* R_bot = 73 kohm, R_top = 177 kohm
XR_top bvdd v_sense sky130_fd_pr__res_xhigh_po W=1u L=89u
XR_bot v_sense gnd   sky130_fd_pr__res_xhigh_po W=1u L=37u

* Reference (from bandgap)
* V_comp_ref = 1.226V

* Comparator: NMOS diff pair, PMOS loads
XM1 comp_out_n v_sense comp_tail gnd sky130_fd_pr__nfet_g5v0d10v5 W=5u L=2u nf=1
XM2 comp_out_p vref    comp_tail gnd sky130_fd_pr__nfet_g5v0d10v5 W=5u L=2u nf=1
XMtail comp_tail vbn gnd gnd sky130_fd_pr__nfet_g5v0d10v5 W=2u L=4u nf=1
XM3 comp_out_n comp_out_p bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 W=2u L=2u nf=1
XM4 comp_out_p comp_out_n bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 W=3u L=2u nf=1
```

---

## Sizing Procedure

1. **Step 1: Design the four threshold dividers.** Calculate R_top and R_bot for each threshold. Use `sky130_fd_pr__res_xhigh_po`. Target ~5 uA per divider. Verify actual resistance values in simulation.

2. **Step 2: Verify thresholds.** For each comparator, sweep BVDD from 0 to 10.5V. Verify the comparator trips at the correct BVDD value (+/- 200 mV tolerance).

3. **Step 3: Add hysteresis.** Use cross-coupled loads (same as Block 05 UV/OV comparators). Size for ~200 mV hysteresis at the BVDD level (which translates to ~200 mV * divider_ratio at the comparator input).

4. **Step 4: Verify monotonic thermometer code.** As BVDD ramps from 0 to 10.5V, the comparator outputs must assert in order: POR first, then RET, PUP, ACT. No comparator should assert before one below it in the sequence. Verify with a slow BVDD ramp.

5. **Step 5: Design combinational logic.** Build CMOS AND/OR gates from HV devices to decode the comparator outputs into control signals. Verify the truth table in simulation.

6. **Step 6: Design the bypass switch.** A large NMOS pulls the pass device gate to GND when bypass_en is active. Size for fast switching (< 1 us) against the gate capacitance load.

7. **Step 7: Fast ramp test.** Ramp BVDD at 12 V/us. Verify clean transitions with no glitches or race conditions between comparators.

8. **Step 8: Slow ramp test.** Ramp BVDD at 0.1 V/us. Verify same behavior — the comparators and logic should work regardless of ramp rate.

9. **Step 9: Power-down test.** Ramp BVDD from 10.5V back down to 0. Verify reverse mode transitions with correct hysteresis.

---

## Testbench Requirements

| Testbench File | Measures | Key Setup |
|---------------|----------|-----------|
| `tb_mode_transitions.spice` | Full mode transition sequence with BVDD ramp | BVDD ramp 0 -> 10.5V at 1 V/us, monitor all outputs |
| `tb_mode_fast_ramp.spice` | Mode transitions with fast BVDD ramp | BVDD ramp at 12 V/us |
| `tb_mode_slow_ramp.spice` | Mode transitions with slow BVDD ramp | BVDD ramp at 0.1 V/us |
| `tb_mode_powerdown.spice` | Reverse transitions (power-down) | BVDD ramp 10.5V -> 0 |
| `tb_mode_thresholds.spice` | Individual comparator threshold measurement | Sweep BVDD, measure each comparator trip point |
| `tb_mode_hysteresis.spice` | Hysteresis of each comparator | BVDD triangle wave, measure up/down thresholds |
| `tb_mode_corners.spice` | Thresholds at SS/FF/SF/FS, -40/27/150C | PVT corner sweep |
| `tb_mode_glitch.spice` | Check for output glitches during transitions | Monitor all outputs for intermediate states |

---

## Simulation Procedure

**PDK include:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

**Full mode transition (BVDD ramp-up):**
```spice
* BVDD ramp from 0 to 10.5V at 1 V/us
V_BVDD bvdd gnd PWL(0 0 10.5u 10.5)
V_REF vref gnd 1.226

* Mode control circuit...

.tran 10n 12u

.control
run
plot v(bvdd) v(bypass_en) v(ea_en) v(ref_sel) v(uvov_en)
* Measure each transition point
meas tran t_por when v(bypass_en)=2.5 rise=1
meas tran bvdd_por find v(bvdd) at=t_por
meas tran t_ret when v(ea_en)=2.5 rise=1
meas tran bvdd_ret find v(bvdd) at=t_ret
print bvdd_por bvdd_ret
.endc
```

**Convergence options:**
```spice
.option reltol=1e-4
.option abstol=1e-12
.option gmin=1e-12
.option method=gear
.option itl1=500
```

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| POR threshold | 2.5V +/- 0.2V (TT 27C) |
| Retention threshold | 4.2V +/- 0.2V |
| Power-up threshold | 4.5V +/- 0.2V |
| Active threshold | 5.6V +/- 0.2V |
| Hysteresis (all comparators) | 150-250 mV |
| Monotonic thermometer code | Yes — no out-of-order assertions |
| Glitch-free outputs | No intermediate states during transitions |
| Works at 12 V/us ramp | Clean transitions |
| Works at 0.1 V/us ramp | Clean transitions |
| Thresholds across PVT | Within +/-15% of nominal |
| Quiescent current (active mode) | < 20 uA from BVDD |
| Power-down reverse transitions | Correct with hysteresis |

---

## Dependencies

**Wave 3 block — requires:**
- Block 06 (level shifter) — for translating SVDD-domain enable signals to BVDD domain
- Knowledge of Block 00 (error amp) enable mechanism
- Knowledge of Block 01 (pass device) gate capacitance for bypass switch sizing

Can be partially designed and tested standalone (the comparators and logic), but full integration testing needs the level shifter and knowledge of downstream block enable interfaces.

---

## Deliverables

1. `design.cir` — Mode control subcircuit. Definition: `.subckt mode_control bvdd pvdd svdd gnd vref en_ret bypass_en ea_en ref_sel uvov_en ilim_en`
2. `tb_mode_transitions.spice` — Full transition sequence testbench
3. `tb_mode_fast_ramp.spice` — Fast ramp testbench
4. `tb_mode_slow_ramp.spice` — Slow ramp testbench
5. `tb_mode_powerdown.spice` — Power-down testbench
6. `tb_mode_thresholds.spice` — Individual threshold testbench
7. `tb_mode_hysteresis.spice` — Hysteresis testbench
8. `tb_mode_corners.spice` — PVT corner testbench
9. `tb_mode_glitch.spice` — Glitch detection testbench
10. `README.md` — Design report: threshold values, hysteresis, transition waveforms, truth table verification, corner data
11. `*.png` — Plots: BVDD ramp with all output signals, threshold vs corner, hysteresis loops
