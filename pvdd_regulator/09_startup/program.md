# Block 09: Startup Circuit — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device (`sky130_fd_pr__nfet_g5v0d10v5`, `sky130_fd_pr__pfet_g5v0d10v5`, `sky130_fd_pr__res_xhigh_po`, etc.). **No exceptions. No behavioral startup models. No ideal switches that magically bootstrap the supply.**
2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** Only testbench stimulus and supply sources may be ideal.
3. **ALL SIMULATIONS IN NGSPICE.** Fix convergence with `.option` settings — do not switch simulators.
4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.**
5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** The startup circuit is fundamentally a chicken-and-egg problem. The error amp needs PVDD to operate, but PVDD needs the error amp to regulate. This is solvable with real circuits. Do not replace any part with a behavioral model.

---

## Purpose

The startup circuit solves the fundamental bootstrap problem in the PVDD LDO:

**The chicken-and-egg problem:**
1. The error amplifier runs from PVDD (5V supply domain).
2. PVDD is produced by the pass device, controlled by the error amplifier.
3. At power-on (BVDD ramping from 0V), PVDD = 0V, so the error amp has no supply.
4. With no error amp, the pass device gate is floating or pulled to BVDD (off), so PVDD stays at 0V.
5. Deadlock: the LDO never starts.

**The solution:** A startup circuit that forces PVDD to charge up from BVDD without the error amplifier, then hands off to the main regulation loop once PVDD is established.

**Additional startup challenges:**
- The PVDD ramp must be monotonic (no dips or oscillations).
- Startup must work for BVDD ramp rates from 0.1 V/us (slow battery connect) to 12 V/us (fast cold-crank recovery).
- Once regulation is established, the startup circuit must fully disable to avoid interfering with the error amp's control of the pass device.
- The startup circuit must handle the case where BVDD drops below PVDD (cold crank) and then recovers.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Input | 0-10.5V | Battery supply (the energy source for bootstrap) |
| `pvdd` | Output/Sense | 0-5V (during startup) | The PVDD rail being bootstrapped |
| `gate` | Output | 0-BVDD | Pass device gate node — startup circuit drives this |
| `gnd` | Supply | 0V | Ground |
| `startup_done` | Output | Digital | Flag indicating startup is complete, handoff to error amp |
| `ea_en` | Output | Digital | Error amplifier enable (asserted when PVDD is high enough) |

**Connections in the LDO:**
- The startup circuit connects to the same `gate` node as the error amp output. During startup, the startup circuit controls the gate. After startup, the error amp takes over and the startup circuit releases.
- `pvdd` is both an output (being charged) and a sense input (monitoring the ramp).
- `startup_done` connects to the mode control (Block 08) to coordinate the transition from startup to regulation.

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Startup time (BVDD = 7V, no load) | -- | -- | 100 | us | Time from BVDD reaching 5.6V to PVDD within 1% of target |
| Startup time (BVDD = 7V, 50 mA load) | -- | -- | 200 | us | Worst case: heavy load during startup |
| PVDD ramp monotonicity | Yes | -- | -- | -- | No dips > 50 mV during ramp |
| PVDD overshoot during startup | -- | -- | 200 | mV | Max overshoot above 5.0V target |
| BVDD ramp rate tolerance | 0.1 | -- | 12 | V/us | Must work at all rates |
| Quiescent current (after startup) | -- | -- | 1 | uA | Startup circuit must fully disable |
| Handoff glitch | -- | -- | 100 | mV | PVDD disturbance when switching from startup to EA control |
| Cold crank recovery | Yes | -- | -- | -- | BVDD drops to 3V and recovers; PVDD must re-start cleanly |
| Temperature range | -40 | 27 | 150 | C | |

---

## Topology

### Strategy 1: Current-Limited Gate Pulldown (Recommended)

A weak pulldown on the pass device gate that turns the pass device partially ON, allowing PVDD to charge up through the pass device. Once PVDD is established, the pulldown is disabled and the error amp takes over.

```
    BVDD
     |
     S
    [Mpass]  (main pass device)
     G ----+---- (to error amp, normally)
     D     |
     |     |
    PVDD   [Mstartup_pd]   Weak NMOS pulldown
           |                (gate controlled by startup logic)
          GND

    PVDD ---[Comparator]--- threshold (~4V)
                |
             [Startup Logic]
                |
            Mstartup_pd gate control
```

**How it works:**
1. At power-on, startup logic detects PVDD < threshold.
2. Activates Mstartup_pd, which pulls the pass device gate weakly toward GND.
3. Pass device turns ON partially, charging PVDD through the 200pF Cload.
4. As PVDD rises past the threshold (~4V), the startup logic deactivates Mstartup_pd.
5. Simultaneously, ea_en is asserted, enabling the error amplifier.
6. The error amp takes over gate control and regulates PVDD to 5.0V.

**The pulldown must be weak** (small W or large series resistance) to limit the inrush current and prevent PVDD from overshooting. If Mstartup_pd is too strong, the gate goes to 0V immediately, pass device is fully ON, PVDD = BVDD = overshoot.

### Strategy 2: Bootstrap Resistor from BVDD

A resistor from BVDD to the error amp supply rail, providing a trickle current to power the error amp directly from BVDD before PVDD is established.

```
    BVDD ---[Rboot]--- EA_supply
                          |
                       [Error Amp]
                          |
                         PVDD (once EA is powered, it can regulate)
```

**Pros:** Simple, no switching logic needed.
**Cons:** The bootstrap resistor wastes current continuously (BVDD - PVDD) / Rboot. At BVDD = 10.5V, PVDD = 5V, Rboot = 100k: Iwaste = 55 uA. This adds to quiescent current permanently unless a switch disconnects it after startup.

### Strategy 3: Dedicated Startup Amplifier

A simple, low-power amplifier built from HV devices that operates directly from BVDD (no need for PVDD). It provides coarse regulation during startup, then hands off to the precision error amp.

**This is the most robust approach but the most complex.** Use if Strategy 1 has handoff glitch problems.

**Start with Strategy 1 (current-limited gate pulldown). It is the simplest and most commonly used.**

---

## Device Selection

| Component | Device | Parameters |
|-----------|--------|-----------|
| Startup pulldown NMOS | `sky130_fd_pr__nfet_g5v0d10v5` | W=2u, L=2u (weak, intentionally) |
| Pulldown series resistor (optional) | `sky130_fd_pr__res_xhigh_po` | 10-100 kohm (limits pulldown current) |
| PVDD threshold comparator NMOS | `sky130_fd_pr__nfet_g5v0d10v5` | W=5u, L=2u |
| PVDD threshold comparator PMOS | `sky130_fd_pr__pfet_g5v0d10v5` | W=2u, L=2u |
| Threshold divider resistors | `sky130_fd_pr__res_xhigh_po` | For scaling PVDD to reference level |
| Startup disable switch | `sky130_fd_pr__pfet_g5v0d10v5` | Disconnects pulldown after startup |
| Bootstrap resistor (Strategy 2) | `sky130_fd_pr__res_xhigh_po` | 50-200 kohm |

**SPICE instantiation example (Strategy 1):**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

* Startup pulldown — weak NMOS pulling pass device gate toward GND
* Series resistor limits current to ~10 uA (enough to charge Cgs slowly)
XRstart gate start_mid sky130_fd_pr__res_xhigh_po W=1u L=50u
XMstart start_mid start_en gnd gnd sky130_fd_pr__nfet_g5v0d10v5 W=2u L=2u nf=1

* PVDD threshold detector (comparator)
* Divider scales PVDD: 4.0V -> 1.226V
* Ratio = 1.226/4.0 = 0.3065
XR_st_top pvdd v_start_sense sky130_fd_pr__res_xhigh_po W=1u L=70u
XR_st_bot v_start_sense gnd sky130_fd_pr__res_xhigh_po W=1u L=31u

* Simple comparator: when v_start_sense > vref, startup_done = 1
XMcomp_n1 comp_out v_start_sense tail_s gnd sky130_fd_pr__nfet_g5v0d10v5 W=5u L=2u nf=1
XMcomp_n2 comp_ref vref        tail_s gnd sky130_fd_pr__nfet_g5v0d10v5 W=5u L=2u nf=1
XMtail_s tail_s vbn gnd gnd sky130_fd_pr__nfet_g5v0d10v5 W=2u L=4u nf=1

* startup_en = NOT(startup_done)
* When PVDD < 4V: startup_done = 0, start_en = 1, pulldown active
* When PVDD > 4V: startup_done = 1, start_en = 0, pulldown off, EA takes over
```

---

## Sizing Procedure

1. **Step 1: Determine the pulldown strength.** The pulldown must charge the pass device gate capacitance (Cgs, from Block 01) slowly enough to avoid PVDD overshoot, but fast enough to meet the 100 us startup time target. With Cgs ~ 100 pF and 100 kohm series resistance: tau = 100 pF * 100 kohm = 10 us. Gate reaches ~63% in 10 us, PVDD starts rising. This is reasonable.

2. **Step 2: Simulate PVDD ramp with pulldown only (no error amp).** Apply BVDD step from 0 to 7V. Activate pulldown. Monitor PVDD. It should ramp up through the pass device. Check: does PVDD overshoot? If yes, increase the pulldown resistance or decrease Mstartup W.

3. **Step 3: Determine the handoff threshold.** Choose the PVDD level at which the startup circuit disables and the error amp enables. This should be well below the regulation target (5.0V) to give the error amp time to take over before PVDD reaches target. 4.0V is a good choice.

4. **Step 4: Design the threshold comparator.** Resistive divider from PVDD + simple comparator vs V_REF. Same topology as UV/OV comparators (Block 05). Add hysteresis to prevent chattering during handoff.

5. **Step 5: Simulate the full handoff.** Connect the startup circuit with the error amp (initially disabled). When PVDD crosses the threshold, disable the pulldown and enable the error amp simultaneously. Monitor PVDD for glitches during the handoff. The glitch should be < 100 mV.

6. **Step 6: Test with load.** Apply 50 mA load from t=0 (worst case). PVDD will ramp slower because the load current must also come through the partially-on pass device. Verify startup completes within 200 us.

7. **Step 7: Test all BVDD ramp rates.** PWL source: 0.1 V/us, 1 V/us, 12 V/us. Verify monotonic PVDD ramp and clean handoff at each rate.

8. **Step 8: Cold crank test.** BVDD ramps to 10.5V, then drops to 3V (PVDD loses regulation and drops), then recovers to 7V. Verify the startup circuit re-engages and PVDD recovers cleanly.

9. **Step 9: PVT corners.** The startup timing varies with process (gm, Vth of pulldown) and temperature. Verify startup works at SS 150C (slowest) and FF -40C (fastest, risk of overshoot).

---

## Testbench Requirements

| Testbench File | Measures | Key Setup |
|---------------|----------|-----------|
| `tb_startup_ramp.spice` | PVDD ramp during startup | BVDD ramp 0 -> 7V at 1 V/us, no load, monitor PVDD |
| `tb_startup_handoff.spice` | Handoff from startup to error amp | Full LDO with startup circuit, monitor PVDD glitch at handoff |
| `tb_startup_loaded.spice` | Startup with 50 mA load | BVDD ramp with heavy load from t=0 |
| `tb_startup_fast.spice` | Fast BVDD ramp (12 V/us) | Check overshoot with fast ramp |
| `tb_startup_slow.spice` | Slow BVDD ramp (0.1 V/us) | Check that startup still works at slow ramp |
| `tb_startup_coldcrank.spice` | Cold crank recovery | BVDD: 0 -> 10.5V -> 3V -> 7V, verify recovery |
| `tb_startup_pvt.spice` | Startup at SS/FF/SF/FS, -40/27/150C | PVT corner sweep |
| `tb_startup_disable.spice` | Verify startup circuit is fully off after startup | Measure leakage current from startup circuit during steady-state regulation |

---

## Simulation Procedure

**PDK include:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

**Basic startup ramp:**
```spice
.include "../00_error_amp/design.cir"
.include "../01_pass_device/design.cir"
.include "../02_feedback_network/design.cir"
.include "../03_compensation/design.cir"

* BVDD ramp from 0 to 7V at 1 V/us
V_BVDD bvdd gnd PWL(0 0 7u 7 100u 7)
V_REF vref gnd 1.226
I_BIAS pvdd ibias 1u

* Pass device
Xpass gate bvdd pvdd pass_device

* Error amp (initially disabled, enabled by startup circuit)
Xea vref vfb gate pvdd gnd ibias ea_en error_amp

* Feedback and compensation
Xfb pvdd vfb gnd feedback_network
Xcomp gate pvdd gnd compensation

* Load
Cload pvdd gnd 200p

* STARTUP CIRCUIT UNDER TEST
* (instantiate startup subcircuit here)

.tran 10n 100u uic

.control
run
plot v(bvdd) v(pvdd) v(gate) v(ea_en)
meas tran startup_time when v(pvdd)=4.95 rise=1
meas tran pvdd_overshoot max v(pvdd)
print startup_time pvdd_overshoot
.endc
```

**Convergence options (startup sims are notoriously difficult):**
```spice
.option reltol=1e-3
.option abstol=1e-10
.option vntol=1e-4
.option gmin=1e-10
.option method=gear
.option itl1=1000
.option itl4=500
.option itl6=200
* Use uic (use initial conditions) to start from zero-energy state
.ic v(pvdd)=0 v(gate)=0
```

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Startup time (no load, BVDD=7V) | < 100 us |
| Startup time (50 mA load, BVDD=7V) | < 200 us |
| PVDD ramp monotonicity | No dips > 50 mV |
| PVDD overshoot | < 200 mV above 5.0V target |
| Handoff glitch | < 100 mV disturbance on PVDD |
| Works at BVDD ramp 0.1 V/us | Yes |
| Works at BVDD ramp 12 V/us | Yes |
| Cold crank recovery | Clean re-start after BVDD dip |
| Startup circuit leakage after startup | < 1 uA |
| Works at SS 150C (slowest) | Startup completes within 200 us |
| Works at FF -40C (fastest) | No overshoot > 200 mV |
| No latch-up or stuck states | PVDD always reaches regulation from any BVDD profile |

---

## Dependencies

**Wave 3 block — requires:**
- Block 00 (error amp) — the startup circuit must hand off control to the error amp
- Block 01 (pass device) — the startup circuit drives the pass device gate (need Cgs value)
- Block 02 (feedback network) — needed for closed-loop handoff testing
- Block 03 (compensation) — needed for post-handoff stability
- Block 08 (mode control) — coordinates the startup/regulation mode transition

This is one of the last blocks to be fully verified because it requires the complete regulation loop to test the handoff. However, the startup pulldown circuit itself can be designed and partially tested standalone.

---

## Deliverables

1. `design.cir` — Startup circuit subcircuit. Definition: `.subckt startup bvdd pvdd gate gnd vref startup_done ea_en`
2. `tb_startup_ramp.spice` — Basic startup ramp testbench
3. `tb_startup_handoff.spice` — Handoff to error amp testbench
4. `tb_startup_loaded.spice` — Startup with load testbench
5. `tb_startup_fast.spice` — Fast BVDD ramp testbench
6. `tb_startup_slow.spice` — Slow BVDD ramp testbench
7. `tb_startup_coldcrank.spice` — Cold crank recovery testbench
8. `tb_startup_pvt.spice` — PVT corner testbench
9. `tb_startup_disable.spice` — Post-startup disable verification testbench
10. `README.md` — Design report: startup strategy, pulldown sizing, handoff mechanism, ramp waveforms, timing data, corner results
11. `*.png` — Plots: PVDD ramp waveform, gate voltage during startup, handoff zoom, cold crank waveform
