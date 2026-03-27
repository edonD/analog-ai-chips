# Block 06: Level Shifter — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** Every transistor must be an instantiated Sky130 device (`sky130_fd_pr__nfet_01v8`, `sky130_fd_pr__pfet_01v8`, `sky130_fd_pr__nfet_g5v0d10v5`, `sky130_fd_pr__pfet_g5v0d10v5`). **No exceptions. No behavioral level shifters. No ideal switches.**
2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** Only testbench stimulus and supply sources may be ideal.
3. **ALL SIMULATIONS IN NGSPICE.** Fix convergence with `.option` settings — do not switch simulators.
4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.**
5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** Level shifters across wide voltage ratios (2.2V to 10.5V) are tricky. The cross-coupled pair may not flip at low BVDD. Iterate.

---

## Purpose

The level shifter translates digital control signals between the SVDD domain (2.2V) and the BVDD/PVDD domain (5-10.5V). This is necessary because:

1. The error amplifier and pass device operate in the BVDD/PVDD domain (5-10.5V).
2. The digital mode control, enable signals, and configuration bits originate in the SVDD domain (2.2V).
3. The UV/OV flags generated in the PVDD domain must be read by SVDD-domain logic.

Without level shifters, the SVDD-domain signals (0/2.2V) cannot reliably drive HV-domain gates, and HV-domain outputs (0/5-10.5V) would overstress SVDD-domain inputs.

**Signals requiring level shifting:**

| Signal | Direction | From | To |
|--------|-----------|------|-----|
| `en` (enable) | SVDD -> BVDD | 0/2.2V | 0/BVDD |
| `mode[1:0]` (mode control) | SVDD -> BVDD | 0/2.2V | 0/BVDD |
| `bypass_en` | SVDD -> BVDD | 0/2.2V | 0/BVDD |
| `uv_flag` | PVDD -> SVDD | 0/PVDD | 0/2.2V |
| `ov_flag` | PVDD -> SVDD | 0/PVDD | 0/2.2V |

---

## Interface

### Low-to-High Level Shifter (SVDD -> BVDD)

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `in` | Input | 0/SVDD (2.2V) | Input signal from SVDD domain |
| `in_b` | Input | 0/SVDD (2.2V) | Complementary input (optional, can generate internally) |
| `out` | Output | 0/BVDD | Level-shifted output in BVDD domain |
| `out_b` | Output | 0/BVDD | Complementary output (optional) |
| `svdd` | Supply | 2.2V | Low-voltage supply |
| `bvdd` | Supply | 5.4-10.5V | High-voltage supply |
| `gnd` | Supply | 0V | Ground |

### High-to-Low Level Shifter (PVDD -> SVDD)

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `in` | Input | 0/PVDD (~5V) | Input signal from PVDD domain |
| `out` | Output | 0/SVDD (2.2V) | Level-shifted output in SVDD domain |
| `pvdd` | Supply | 5.0V | High-voltage input supply |
| `svdd` | Supply | 2.2V | Low-voltage output supply |
| `gnd` | Supply | 0V | Ground |

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Input voltage swing (low-to-high) | 0/2.2 | -- | -- | V | SVDD domain |
| Output voltage swing (low-to-high) | 0/BVDD | -- | -- | V | Must reach full BVDD rail |
| Input voltage swing (high-to-low) | 0/PVDD | -- | -- | V | PVDD domain |
| Output voltage swing (high-to-low) | 0/2.2 | -- | -- | V | Must reach full SVDD rail |
| Propagation delay (rising) | -- | -- | 100 | ns | From input edge to output edge |
| Propagation delay (falling) | -- | -- | 100 | ns | |
| BVDD operating range | 5.4 | -- | 10.5 | V | Must work across full BVDD range |
| Static power per shifter | -- | -- | 5 | uA | No static current path in steady state |
| Maximum duty cycle distortion | -- | -- | 5 | % | Symmetric rise/fall delays |
| Temperature range | -40 | 27 | 150 | C | |

---

## Topology

### Low-to-High: Cross-Coupled PMOS Level Shifter

The standard and proven topology for voltage up-shifting:

```
                    BVDD
                     |
              ┌──────┴──────┐
            [M3p]         [M4p]      HV PMOS (cross-coupled)
              |             |
         out_b|        out  |
              |             |
            [M1n]         [M2n]      HV NMOS (driven by SVDD-level inputs)
              |             |
             GND           GND

     in ──> gate of M2n (through buffer if needed)
    in_b ──> gate of M1n
```

**How it works:**
1. When `in` = SVDD (2.2V), M2n turns ON, pulling `out` low. This turns M3p ON (cross-coupled), pulling `out_b` to BVDD. M4p is OFF.
2. When `in` = 0V, M1n turns ON (via `in_b`), pulling `out_b` low. This turns M4p ON, pulling `out` to BVDD. M3p is OFF.

**Key concern:** M1n and M2n are HV NMOS devices driven by only 2.2V on the gate. The Vth of `sky130_fd_pr__nfet_g5v0d10v5` is ~0.6-0.9V. With Vgs = 2.2V, the NMOS devices are in moderate inversion and have limited drive strength compared to the HV PMOS loads. The NMOS must be sized wider than the PMOS to ensure reliable switching, especially at SS corner and high temperature.

**If Vgs = 2.2V does not reliably overcome the PMOS cross-coupling** (risk at SS corner with Vth ~ 0.9V), add a PMOS header or weaken the cross-coupled PMOS by increasing their L or decreasing their W.

### High-to-Low: Voltage Clamped Inverter

For PVDD (5V) to SVDD (2.2V) down-shifting:

```
    SVDD (2.2V)
      |
    [M5p]    PMOS (1.8V device, since output is SVDD domain)
      |
     out ──> SVDD-domain output
      |
    [M6n]    HV NMOS (gate tolerant to PVDD)
      |
     GND

    in (0/PVDD) ──> gate of M6n (through resistive divider or cascode clamp)
```

**Caution:** The 1.8V PMOS gate cannot see more than 1.8V. If the input swings to PVDD (5V), use a cascode or resistive divider to protect the 1.8V device. Alternatively, use all HV devices and clamp the output to SVDD with a diode.

---

## Device Selection

| Component | Device | Parameters |
|-----------|--------|-----------|
| Cross-coupled PMOS (M3, M4) | `sky130_fd_pr__pfet_g5v0d10v5` | W=2u, L=0.5u |
| Input NMOS (M1, M2) | `sky130_fd_pr__nfet_g5v0d10v5` | W=5u, L=0.5u (wider for drive strength at Vgs=2.2V) |
| Down-shifter NMOS | `sky130_fd_pr__nfet_g5v0d10v5` | W=2u, L=0.5u |
| Down-shifter PMOS | `sky130_fd_pr__pfet_g5v0d10v5` | W=2u, L=0.5u (or 1.8V device with protection) |
| Inverter buffer (SVDD domain) | `sky130_fd_pr__nfet_01v8` / `sky130_fd_pr__pfet_01v8` | Standard 1.8V inverter |

**SPICE instantiation example (low-to-high):**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

* Cross-coupled PMOS level shifter (SVDD -> BVDD)
* Cross-coupled pair
XM3 out_b out   bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 W=2u L=0.5u nf=1
XM4 out   out_b bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 W=2u L=0.5u nf=1

* Input pull-down NMOS (driven by SVDD-level signals)
XM1 out_b in_b gnd gnd sky130_fd_pr__nfet_g5v0d10v5 W=5u L=0.5u nf=1
XM2 out   in   gnd gnd sky130_fd_pr__nfet_g5v0d10v5 W=5u L=0.5u nf=1

* Generate complementary input from single-ended
* Use SVDD-domain inverter
XMinv_n in_buf in   gnd  gnd  sky130_fd_pr__nfet_01v8 W=1u L=0.15u nf=1
XMinv_p in_buf in   svdd svdd sky130_fd_pr__pfet_01v8 W=2u L=0.15u nf=1
* in_b = in_buf (inverted)
```

---

## Sizing Procedure

1. **Step 1: Determine HV NMOS drive strength at Vgs = 2.2V.** Instantiate `sky130_fd_pr__nfet_g5v0d10v5` with W=1u, L=0.5u. Apply Vgs=2.2V, sweep Vds. Measure Id_sat. This tells you the current available per um of width at the SVDD drive voltage.

2. **Step 2: Determine HV PMOS strength.** Similarly characterize `sky130_fd_pr__pfet_g5v0d10v5` at full Vgs (BVDD). This is the current the NMOS must overcome to flip the cross-coupled latch.

3. **Step 3: Size for reliable switching.** The NMOS pull-down current at Vgs=2.2V must exceed the PMOS cross-coupled current. Rule of thumb: make NMOS W at least 2-3x the PMOS W. Verify at SS corner, 150C (worst: NMOS Vth highest, mobility lowest).

4. **Step 4: Simulate switching.** Apply a 2.2V pulse on `in`. Verify `out` switches from 0 to BVDD (and back). Measure propagation delay.

5. **Step 5: Sweep BVDD.** The level shifter must work from BVDD = 5.4V to 10.5V. At low BVDD, the PMOS Vth is a larger fraction of the supply — verify switching still works. At high BVDD, verify no excessive crowbar current during transition.

6. **Step 6: Static power.** In steady state (in = constant), there should be no DC current path. Verify Idd < 1 uA in both states.

7. **Step 7: Design the down-shifter (PVDD -> SVDD).** Use an HV NMOS as the input device (gate can handle 5V). Use resistor or cascode to limit the output swing to SVDD. Verify output is clean 0/2.2V.

8. **Step 8: PVT corners.** Verify all delays and functionality at SS/FF/SF/FS and -40/27/150C.

---

## Testbench Requirements

| Testbench File | Measures | Key Setup |
|---------------|----------|-----------|
| `tb_ls_function.spice` | Logic function verification (up and down shifters) | Apply pulse on input, verify output levels |
| `tb_ls_delay.spice` | Propagation delay (tpLH, tpHL) | Fast pulse input, measure 50% to 50% delay |
| `tb_ls_supply.spice` | Functionality across BVDD = 5.4 to 10.5V | Parametric BVDD sweep |
| `tb_ls_power.spice` | Static and dynamic power consumption | DC measurement in both states, measure at 1 MHz toggle |
| `tb_ls_corners.spice` | Functionality and delay at SS/FF/SF/FS, -40/27/150C | PVT corner sweep |
| `tb_ls_drive.spice` | NMOS drive current at Vgs = 2.2V characterization | For sizing verification |

---

## Simulation Procedure

**PDK include:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

**Functional test (low-to-high):**
```spice
V_BVDD bvdd gnd 7.0
V_SVDD svdd gnd 2.2

* Input pulse: 0 to 2.2V, 100ns period
Vin in gnd PULSE(0 2.2 10n 1n 1n 48n 100n)

* Level shifter circuit...
* (instantiate cross-coupled pair, NMOS, inverter)

* Load cap (typical gate load)
Cout out gnd 0.5p

.tran 0.1n 500n

.control
run
plot v(in) v(out) v(out_b)
meas tran tphl trig v(in) val=1.1 rise=1 targ v(out) val=3.5 fall=1
meas tran tplh trig v(in) val=1.1 fall=1 targ v(out) val=3.5 rise=1
print tphl tplh
.endc
```

**BVDD sweep test:**
```spice
.param bvdd_val = 7.0
V_BVDD bvdd gnd {bvdd_val}

* Run transient at each BVDD point
.control
foreach bv 5.4 6.0 7.0 8.0 9.0 10.0 10.5
  alter V_BVDD = $bv
  tran 0.1n 500n
  meas tran tplh trig v(in) val=1.1 fall=1 targ v(out) val='$bv/2' rise=1
  print tplh
  reset
end
.endc
```

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Low-to-high: output reaches BVDD | Output HIGH > BVDD - 0.2V |
| Low-to-high: output reaches GND | Output LOW < 0.2V |
| High-to-low: output reaches SVDD | Output HIGH > SVDD - 0.2V |
| High-to-low: output reaches GND | Output LOW < 0.2V |
| Propagation delay | < 100 ns at all conditions |
| Works at BVDD = 5.4V (minimum) | Reliable switching confirmed |
| Works at BVDD = 10.5V (maximum) | Reliable switching, no breakdown |
| Static power | < 5 uA per shifter in steady state |
| Works at SS corner, 150C | Reliable switching (worst case for NMOS drive) |
| No metastable states | Output always resolves to rail |

---

## Dependencies

**Wave 1 block — no dependencies on other blocks for standalone design.**

The level shifter is a utility block used by Block 08 (mode control) and Block 10 (top integration). It can be designed and tested independently using ideal supply sources.

---

## Deliverables

1. `design.cir` — Level shifter subcircuits:
   - `.subckt level_shifter_up in out bvdd svdd gnd` (SVDD -> BVDD)
   - `.subckt level_shifter_down in out pvdd svdd gnd` (PVDD -> SVDD)
2. `tb_ls_function.spice` — Functional verification testbench
3. `tb_ls_delay.spice` — Propagation delay testbench
4. `tb_ls_supply.spice` — BVDD sweep testbench
5. `tb_ls_power.spice` — Power consumption testbench
6. `tb_ls_corners.spice` — PVT corner testbench
7. `tb_ls_drive.spice` — Drive strength characterization testbench
8. `README.md` — Design report: topology, device sizes, delay measurements, BVDD range validation, corner data
9. `*.png` — Plots: input/output waveforms, delay vs BVDD, corner comparison
