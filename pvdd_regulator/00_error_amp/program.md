# Block 00: Error Amplifier — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device (`sky130_fd_pr__nfet_01v8`, `sky130_fd_pr__pfet_01v8`, `sky130_fd_pr__nfet_g5v0d10v5`, `sky130_fd_pr__pfet_g5v0d10v5`, `sky130_fd_pr__res_*`, `sky130_fd_pr__cap_mim_m3_1`, etc.). **No exceptions.**
2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** The ONLY ideal components allowed are: V_AVBG (1.226V bandgap reference), I_BIAS (1uA current reference), supply sources for testbenches, and testbench stimulus/load elements.
3. **ALL SIMULATIONS IN NGSPICE.** No HSPICE, no Spectre, no Xyce. Fix convergence issues with `.option` settings — do not switch simulators or replace devices.
4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.**
5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** Iterate on the real circuit until it works.

---

## Purpose

The error amplifier is the core gain stage of the PVDD LDO regulator. It compares the feedback voltage (V_FB, scaled from PVDD) to the bandgap reference (V_REF = 1.226V) and drives the gate of the HV PMOS pass device. The error amp's gain determines regulation accuracy (load regulation, line regulation). Its bandwidth and output impedance interact with the pass device gate capacitance and the compensation network to determine loop stability.

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `vref` | Input | ~1.226V | Bandgap reference voltage (positive OTA input) |
| `vfb` | Input | ~1.226V | Feedback voltage from resistive divider (negative OTA input) |
| `vout_gate` | Output | 0 to ~PVDD | Error amp output driving pass device gate |
| `pvdd` | Supply | 5.0V regulated | Positive supply rail (regulated PVDD domain) |
| `gnd` | Supply | 0V | Ground |
| `ibias` | Input | -- | Bias current input (1uA from IREF, mirrored internally) |
| `en` | Input | 0 / PVDD | Enable signal (active high) |

**Connections in the LDO:**
- `vref` connects to the ideal V_AVBG (1.226V) bandgap reference.
- `vfb` connects to the feedback divider midpoint (Block 02).
- `vout_gate` connects to the pass device gate (Block 01) and compensation network (Block 03).
- `pvdd` connects to the regulated PVDD output rail.
- `ibias` connects to the shared IREF current mirror.

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| DC open-loop gain | 60 | 70 | -- | dB | Measured at DC, no load |
| Unity-gain bandwidth (UGB) | 200 | 500 | 1000 | kHz | With Cgs_pass load (~100pF) |
| Phase margin (open-loop, into Cgs) | 55 | 70 | -- | deg | Error amp alone, not full LDO loop |
| Input offset voltage | -- | -- | 5 | mV | Systematic offset; contributes to PVDD error |
| Input common-mode range | 0.8 | -- | 2.0 | V | Must include 1.226V |
| Output voltage swing low | -- | -- | 0.5 | V | Must pull pass gate near GND to fully turn ON |
| Output voltage swing high | PVDD-0.5 | -- | -- | V | Must approach PVDD to turn pass device OFF |
| Supply voltage (PVDD) | 4.5 | 5.0 | 5.5 | V | Regulated domain |
| Quiescent current | -- | 50 | 100 | uA | From PVDD supply |
| CMRR | 50 | 60 | -- | dB | At DC |
| PSRR (from PVDD supply) | 40 | 50 | -- | dB | At DC |
| Slew rate (positive) | 0.5 | -- | -- | V/us | Charging Cgs_pass |
| Slew rate (negative) | 0.5 | -- | -- | V/us | Discharging Cgs_pass |
| Temperature range | -40 | 27 | 150 | C | |

---

## Topology

**Folded-cascode OTA** — single-stage, high-gain, wide output swing.

**Why this topology:**
1. Single-stage means only one high-impedance node (output), simplifying compensation when embedded in the LDO loop.
2. Folded-cascode provides >60 dB gain in one stage (gm * rout_cascode).
3. Wide input common-mode range — the folded structure allows PMOS input pair (preferred here since inputs are near 1.2V, well above GND but below PVDD).
4. Wide output swing — the cascode output can swing from Vdsat_n + Vdsat_n_cascode (~0.4V) to PVDD - Vdsat_p - Vdsat_p_cascode (~PVDD - 0.4V). This is critical: the output must swing near GND to fully turn on the PMOS pass device.
5. Proven in similar LDO designs. The VibroSense SAR ADC project used a similar topology successfully.

**Architecture:**
```
                         PVDD
                          |
                   ┌──────┴──────┐
                   |             |
                 [M5p]        [M6p]   <-- PMOS cascode loads
                   |             |
                 [M3p]        [M4p]   <-- PMOS current mirror loads
                   |             |
        ┌──────────┤             ├──────────┐
        |          |             |          |
      [M7n]      [M8n]        [M9n]     [M10n]  <-- NMOS folded-cascode
        |          |             |          |
        |     vref-|  inp  inn  |-vfb      |
        |          └──┤       ├──┘         |
        |             [M1p] [M2p]          |   <-- PMOS diff pair
        |                |                 |
        |              [Mtail]             |   <-- Tail current source
        |                |                 |
        GND             GND              vout_gate
```

**Supply domain:** The error amp runs from PVDD (5V). Since Sky130 1.8V devices have Vds_max = 1.8V, we MUST use 5V thick-oxide devices (`sky130_fd_pr__nfet_05v0`, `sky130_fd_pr__pfet_05v0`) or HV devices (`sky130_fd_pr__nfet_g5v0d10v5`, `sky130_fd_pr__pfet_g5v0d10v5`) for the entire error amp. The 1.8V devices CANNOT be used directly in a 5V domain without cascode protection. **Use HV (g5v0d10v5) devices throughout.**

---

## Device Selection

| Role | Device | Why |
|------|--------|-----|
| Input diff pair (M1, M2) | `sky130_fd_pr__pfet_g5v0d10v5` | PMOS input for low-CM inputs (~1.2V). HV device for 5V supply. |
| Tail current source (Mtail) | `sky130_fd_pr__pfet_g5v0d10v5` | PMOS current source from PVDD. |
| NMOS folded-cascode (M7-M10) | `sky130_fd_pr__nfet_g5v0d10v5` | Cascode transistors, see 5V Vds. |
| PMOS cascode loads (M3-M6) | `sky130_fd_pr__pfet_g5v0d10v5` | Current mirror loads with cascode. |
| Bias mirrors | `sky130_fd_pr__nfet_g5v0d10v5` / `sky130_fd_pr__pfet_g5v0d10v5` | Mirror the 1uA IREF to desired branch currents. |

**SPICE instantiation example:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

* PMOS diff pair (input)
XM1 drain1 vref  src  pvdd sky130_fd_pr__pfet_g5v0d10v5 W=10u L=1u nf=2
XM2 drain2 vfb   src  pvdd sky130_fd_pr__pfet_g5v0d10v5 W=10u L=1u nf=2

* Tail current source
XMtail src bias_p pvdd pvdd sky130_fd_pr__pfet_g5v0d10v5 W=5u L=2u nf=1

* NMOS cascode pair
XM7  cas_n1  bn   drain1  gnd sky130_fd_pr__nfet_g5v0d10v5 W=5u L=1u nf=1
XM8  vout    bn   drain2  gnd sky130_fd_pr__nfet_g5v0d10v5 W=5u L=1u nf=1

* PMOS cascode loads
XM5 cas_n1 bp1 pvdd pvdd sky130_fd_pr__pfet_g5v0d10v5 W=5u L=1u nf=1
XM6 vout   bp2 pvdd pvdd sky130_fd_pr__pfet_g5v0d10v5 W=5u L=1u nf=1
```

---

## Sizing Procedure

1. **Set tail current (Itail):** Start with 20 uA. Each branch gets 10 uA. This gives reasonable gm for UGB target while keeping Iq low. Total EA current with mirrors: ~50 uA.

2. **Size input pair (M1, M2):** For input offset < 5 mV, want W*L > 50 um^2. Start with W=20u, L=2u (W*L = 40 um^2, marginal). Increase to W=30u, L=2u if offset is too high. Verify gm = ~100 uA/V at 10 uA bias (HV PMOS has lower mobility than standard PMOS).

3. **Calculate required gm for UGB:** UGB = gm / (2*pi * Cload). With Cgs_pass ~ 100 pF (from Block 01 characterization): gm = 2*pi * 500kHz * 100pF = 314 uA/V. At 10 uA per branch, need gm/Id ~ 31 V^-1. This is achievable in weak/moderate inversion. If not, increase Itail.

4. **Size NMOS cascode (M7-M10):** L >= 1u for output resistance. W sized for Vdsat ~ 0.2-0.3V at branch current. Start with W=5u, L=1u.

5. **Size PMOS loads (M3-M6):** Mirror ratio 1:1 from a diode-connected reference. L >= 1u. W sized for Vdsat ~ 0.2-0.3V. Start with W=5u, L=1u.

6. **Size bias mirror:** Mirror the 1 uA IREF up to 20 uA tail current (ratio 1:20). IREF mirror NMOS: W=2u, L=4u (1 uA). Tail mirror: W=40u, L=4u (20 uA).

7. **Verify all devices in saturation** at the DC operating point. Check Vds > Vdsat for every transistor.

8. **Iterate:** Simulate gain, UGB, phase margin, and adjust sizes.

---

## Testbench Requirements

| Testbench File | Measures | Key Setup |
|---------------|----------|-----------|
| `tb_ea_dc.spice` | DC operating point, all node voltages, device saturation | PVDD=5V, vref=vfb=1.226V, check Vds vs Vdsat |
| `tb_ea_ac.spice` | Open-loop gain and phase vs frequency | Break loop: AC source on vfb, measure vout_gate. Cgs_pass load on output (~100pF) |
| `tb_ea_tran.spice` | Transient step response and slew rate | Pulse on vfb (1.226V +/- 50mV), measure vout_gate settling |
| `tb_ea_cmrr.spice` | Common-mode rejection ratio | AC source on both inputs simultaneously, measure output |
| `tb_ea_psrr.spice` | Power supply rejection from PVDD | AC source on PVDD, inputs at 1.226V DC, measure output |
| `tb_ea_corners.spice` | All above at SS/FF/SF/FS corners, -40/27/150C | Parametric corner sweep |

---

## Simulation Procedure

**PDK include (use in every testbench):**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

**DC operating point:**
```spice
.op
.save all
.control
op
show all
print all
.endc
```

**AC open-loop gain/phase:**
```spice
* Break the loop: apply AC stimulus at vfb input
Vac_fb vfb_ac gnd dc 1.226 ac 1
* Load the output with estimated Cgs of pass device
Cload vout_gate gnd 100p

.ac dec 100 1 100meg
.control
run
let gain_db = db(v(vout_gate)/v(vfb_ac))
let phase = 180/PI * ph(v(vout_gate)/v(vfb_ac))
meas ac dc_gain find gain_db at=1
meas ac ugb when gain_db=0
meas ac pm find phase when gain_db=0
plot gain_db phase
wrdata ea_ac.csv gain_db phase
.endc
```

**Convergence options (if needed):**
```spice
.option reltol=1e-4
.option abstol=1e-12
.option vntol=1e-6
.option gmin=1e-12
.option method=gear
.option maxord=2
```

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| DC gain | >= 60 dB |
| UGB | 200 kHz to 1 MHz (with 100pF load) |
| Phase margin (OL into Cgs) | >= 55 deg |
| All devices in saturation | Vds > Vdsat + 50mV for every device at nominal OP |
| Output swing low | < 0.5V (to fully turn on pass device) |
| Output swing high | > PVDD - 0.5V (to fully turn off pass device) |
| Quiescent current | < 100 uA from PVDD |
| Input offset | < 5 mV |
| CMRR | > 50 dB at DC |
| PSRR | > 40 dB at DC |
| Corners: all above hold at SS, FF, SF, FS | Yes |
| Temperature: all above hold at -40, 27, 150C | Yes |

---

## Dependencies

**Wave 1 block — no dependencies on other blocks.**

However, you NEED the pass device gate capacitance (Cgs) from Block 01 characterization to set the correct load for AC simulations. If Block 01 is not yet done, use an estimated Cgs = 100 pF as placeholder and re-verify once the actual value is known.

---

## Deliverables

1. `design.cir` — Complete folded-cascode OTA subcircuit with all Sky130 devices. Subcircuit definition: `.subckt error_amp vref vfb vout_gate pvdd gnd ibias en`
2. `tb_ea_dc.spice` — DC operating point testbench
3. `tb_ea_ac.spice` — Open-loop AC gain/phase testbench
4. `tb_ea_tran.spice` — Transient step response testbench
5. `tb_ea_cmrr.spice` — CMRR testbench
6. `tb_ea_psrr.spice` — PSRR testbench
7. `tb_ea_corners.spice` — PVT corner sweep testbench
8. `README.md` — Design report with all simulation results, device table, and operating point summary
9. `*.png` — Plots: gain/phase Bode plot, transient step response, DC operating point bar chart
