# Block 01: Pass Device — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** Every transistor must be an instantiated Sky130 device. The pass device is `sky130_fd_pr__pfet_g5v0d10v5`. **No exceptions. No behavioral MOSFET models. No VCCS approximations.**
2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** The ONLY ideal components allowed are supply sources (V_BVDD, V_SVDD) and testbench stimulus/load elements.
3. **ALL SIMULATIONS IN NGSPICE.** Fix convergence with `.option` settings — do not switch simulators.
4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.**
5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** The HV PMOS may have low mobility and need very large W. That is expected. Do not replace it with an ideal switch.

---

## Purpose

The pass device is the power transistor that drops the input voltage (BVDD, 5.4-10.5V) to the regulated output (PVDD, 5.0V). All load current (0 to 50 mA) flows through this device. It is configured as a common-source PMOS: source tied to BVDD, drain to PVDD, gate driven by the error amplifier. The pass device is the most critical component in the LDO because:

1. Its on-resistance sets the dropout voltage (Vdo = Id * Rds_on at full gate drive).
2. Its gate capacitance (Cgs) is the dominant load for the error amplifier and sets a key pole in the feedback loop.
3. Its transconductance (gm_pass) sets the DC gain from gate to output and the output pole frequency.
4. Its safe operating area (SOA) limits determine reliability during transients.

**Everything downstream — error amp sizing, compensation, startup — depends on this device's characterization. Design this block FIRST.**

---

## Interface

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Input (source) | 5.4-10.5V | Battery supply — pass device source terminal |
| `pvdd` | Output (drain) | 5.0V regulated | Regulated output — pass device drain terminal |
| `gate` | Input (gate) | 0 to ~BVDD | Gate drive from error amp output |
| `bvdd` | Bulk | same as source | Body tied to source (BVDD) for PMOS |

**Connections in the LDO:**
- Source = BVDD supply rail
- Drain = PVDD output rail, also connected to 200 pF Cload, feedback divider, UV/OV sense
- Gate = error amp output (vout_gate from Block 00), compensation network (Block 03)
- Bulk = BVDD (standard PMOS body connection)

---

## Target Specifications

| Parameter | Min | Typ | Max | Unit | Notes |
|-----------|-----|-----|-----|------|-------|
| Drain current at Vds=0.4V | 50 | -- | -- | mA | Full load, gate fully driven |
| Dropout voltage at 50 mA | -- | 400 | -- | mV | Vds at which Id = 50 mA with Vgs = max |
| Gate capacitance (Cgs) | -- | TBD | -- | pF | At operating point; expect 50-200 pF |
| Transconductance (gm) | -- | TBD | -- | mA/V | At Iload = 10 mA operating point |
| Rds_on (full gate drive) | -- | TBD | -- | ohm | Vgs = -5V (gate at GND, source at 5V) |
| Leakage current (off) | -- | -- | 1 | uA | Vgs = 0V, Vds = 5V |
| Max Vds | -- | -- | 10.5 | V | Sky130 HV device limit |
| Max Vgs | -- | -- | 5.0 | V | Gate driven from PVDD domain |
| Temperature range | -40 | 27 | 150 | C | |

---

## Topology

**Single HV PMOS transistor** — `sky130_fd_pr__pfet_g5v0d10v5` — configured as a common-source amplifier in the LDO loop.

```
    BVDD (5.4-10.5V)
     |
     S (source + bulk)
    [sky130_fd_pr__pfet_g5v0d10v5]
     G ---- gate (from error amp)
     D
     |
    PVDD (5.0V output)
     |
    [Cload 200pF]  [Rload]  [feedback divider]
     |               |          |
    GND             GND        GND
```

**Why PMOS:**
- Low dropout: Vdo = Vds_sat (just the saturation voltage, ~200-400 mV for large W)
- Gate can be pulled to GND (fully ON) or to BVDD (fully OFF) using a single supply domain
- Matches the original GF130BCD PDMOS topology
- No charge pump needed (unlike NMOS source-follower LDO)

**Finger sizing:** The device will be large (several mm total W). Use multi-finger instantiation with `nf` parameter or multiple parallel instances to manage layout and gate resistance.

---

## Device Selection

| Component | Device | Parameters |
|-----------|--------|-----------|
| Pass transistor | `sky130_fd_pr__pfet_g5v0d10v5` | W=TBD (several mm), L=0.5u (min for HV), nf=multiple |

**SPICE instantiation example:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

* Pass device — PMOS, source=BVDD, drain=PVDD, bulk=BVDD
* Start with W=1000u (1mm) to characterize, then scale
XMpass pvdd gate bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 W=1000u L=0.5u nf=20

* For larger W, use multiple instances in parallel:
* XMpass1 pvdd gate bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 W=1000u L=0.5u nf=20
* XMpass2 pvdd gate bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 W=1000u L=0.5u nf=20
* ... (total 5-10 instances for 5-10mm total W)
```

**Note on L:** The minimum L for `sky130_fd_pr__pfet_g5v0d10v5` is 0.5 um. Using L=0.5u gives minimum Rds_on. If channel-length modulation is excessive (poor output resistance), increase to L=1u — but this doubles the required W for the same current.

---

## Sizing Procedure

This is a characterization-driven process. You do NOT hand-calculate W/L for HV devices — you simulate and find it.

1. **Step 1: Characterize a unit device.** Instantiate `sky130_fd_pr__pfet_g5v0d10v5` with W=100u, L=0.5u. Sweep Vgs from 0 to -5V at Vds = -0.4V (dropout condition). Record Id vs Vgs.

2. **Step 2: Find Id per unit width.** From the sweep, find the Vgs at which Id = some reference current per um of W. For example, if W=100u gives Id=1mA at Vgs=-3V, Vds=-0.4V, then Id/W = 10 uA/um.

3. **Step 3: Calculate total W for 50 mA.** Required W = 50 mA / (Id/W). If Id/W = 10 uA/um at the operating point, then W = 5000u = 5 mm.

4. **Step 4: Verify.** Instantiate the full-size device. Apply Vgs corresponding to error amp output at regulation (typically Vgs ~ -2 to -4V), Vds = -0.4V. Confirm Id >= 50 mA.

5. **Step 5: Characterize Cgs.** Use AC analysis or charge-based measurement. At the operating point (Vgs ~ -3V, Vds ~ -0.4V, Id ~ 10-50 mA), extract Cgs. This is CRITICAL — it determines the error amp load and a key pole.

6. **Step 6: Characterize gm.** Measure dId/dVgs at the operating point. This determines the LDO loop gain from gate to output: A_pass = gm_pass * Rload || rds_pass.

7. **Step 7: Corner characterization.** Repeat Steps 1-6 at SS, FF corners and -40C, 150C. The SS corner at 150C is worst case for Rds_on (highest dropout). FF corner at -40C gives highest gm (affects stability).

8. **Step 8: Rds_on for bypass mode.** With Vgs = -5V (gate at GND, source at PVDD=5V), measure Rds_on. This is used in bypass/retention mode where the pass device is fully ON.

---

## Testbench Requirements

| Testbench File | Measures | Key Setup |
|---------------|----------|-----------|
| `tb_pass_iv.spice` | Id vs Vds family curves | Sweep Vds 0 to -5V, Vgs = 0 to -5V in steps of 0.5V |
| `tb_pass_dropout.spice` | Id vs Vgs at Vds = -0.4V (dropout) | Sweep Vgs 0 to -5V, fixed Vds = -0.4V. Find W for 50 mA. |
| `tb_pass_cgs.spice` | Gate capacitance vs bias point | AC analysis: small-signal AC on gate, measure Ig/freq to get Cgs |
| `tb_pass_gm.spice` | Transconductance vs Id | Sweep Vgs, compute dId/dVgs numerically |
| `tb_pass_rdson.spice` | On-resistance vs Vgs | Vgs = -5V, sweep Vds near 0, measure slope |
| `tb_pass_corners.spice` | Repeat key measurements at SS/FF/SF/FS, -40/27/150C | Parametric corner sweep |
| `tb_pass_soa.spice` | Safe operating area check | Transient: Vds ramp to 10.5V at 50 mA, verify no breakdown |

---

## Simulation Procedure

**PDK include:**
```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

**Id vs Vgs at Vds = -0.4V (the key characterization):**
```spice
* Pass device characterization — find W for 50 mA at dropout
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

XMpass drain gate source source sky130_fd_pr__pfet_g5v0d10v5 W=100u L=0.5u nf=4

Vds drain source -0.4
Vgs gate source 0

.dc Vgs 0 -5 -0.01

.control
run
plot -i(Vds) vs v(gate,source)
meas dc id_at_3v find -i(Vds) at=-3.0
print id_at_3v
wrdata pass_id_vgs.csv -i(Vds)
.endc
```

**Gate capacitance measurement:**
```spice
* Bias at operating point, apply small AC to gate
Vgs gate source dc -3.0 ac 1
Vds drain source dc -0.4

.ac dec 50 1k 1g

.control
run
* Cgs = Im(Ig) / (2*pi*freq)
let cgs = imag(i(Vgs)) / (2 * PI * frequency)
plot cgs vs frequency
meas ac cgs_1mhz find cgs at=1e6
.endc
```

**Convergence options:**
```spice
.option reltol=1e-3
.option abstol=1e-12
.option gmin=1e-12
.option method=gear
```

---

## Pass/Fail Criteria

| Parameter | Pass Condition |
|-----------|---------------|
| Id at Vds=-0.4V, max Vgs drive | >= 50 mA (at TT 27C) |
| Id at Vds=-0.4V, max Vgs drive, SS 150C | >= 50 mA (worst case) |
| Total W | < 20 mm (if larger, topology is impractical) |
| Cgs at operating point | Measured and documented (any value — this feeds Block 00/03) |
| gm at 10 mA | Measured and documented (feeds loop gain calculation) |
| Rds_on at full gate drive | < 20 ohm (for bypass mode voltage drop) |
| No model errors or convergence failures | All testbenches run to completion |

---

## Dependencies

**Wave 1 block — no dependencies on other blocks.**

This block should be designed FIRST. Its outputs (W/L, Cgs, gm, Rds_on) are inputs to Block 00 (error amp), Block 03 (compensation), and Block 04 (current limiter).

---

## Deliverables

1. `design.cir` — Pass device subcircuit. Subcircuit definition: `.subckt pass_device gate bvdd pvdd` (with body tied to bvdd internally)
2. `tb_pass_iv.spice` — Id-Vds family curve testbench
3. `tb_pass_dropout.spice` — Id vs Vgs at dropout testbench (the critical one)
4. `tb_pass_cgs.spice` — Gate capacitance characterization testbench
5. `tb_pass_gm.spice` — Transconductance characterization testbench
6. `tb_pass_rdson.spice` — On-resistance testbench
7. `tb_pass_corners.spice` — PVT corner sweep testbench
8. `tb_pass_soa.spice` — Safe operating area testbench
9. `README.md` — Characterization report: final W/L, Id(Vgs) curve, Cgs value, gm value, Rds_on, corner data, all backed by simulation plots
10. `*.png` — Plots: Id vs Vds family, Id vs Vgs at dropout, Cgs vs Vgs, corner comparison
