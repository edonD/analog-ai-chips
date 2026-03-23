# Block 01 Extension: PGA OTA v2 — Two-Stage Miller (500 kHz)

## 1. Why This Exists

`../ota_pga/ota_pga.spice` (v1) is a folded-cascode OTA that achieved **67.5 kHz UGB**.
It passed its own spec but that spec was wrong. The PGA (Block 02) closes a feedback loop
at gains of 1×, 4×, 16×, and 64×. Closed-loop BW = UGB / noise_gain:

| PGA gain | Noise gain | BW at 67.5 kHz UGB | Required BW |
|----------|-----------|---------------------|-------------|
| 1×       | 1         | 67.5 kHz            | >25 kHz ✓  |
| 4×       | 5         | 13.5 kHz            | >25 kHz ✗  |
| 16×      | 17        | 3.97 kHz            | >25 kHz ✗  |
| 64×      | 65        | 1.04 kHz            | >6 kHz  ✗  |

The 16× case is the binding constraint: UGB ≥ 17 × 25 kHz = **425 kHz minimum**.

**Why the folded-cascode cannot be fixed:** UGB = gm / (2π × CL). To get 6× more UGB
requires gm to increase 6× → tail current increases 36× → ~58 μA → ~105 μW. That is
350× over the power budget. The topology is fundamentally wrong for this application.

**The fix:** two-stage Miller-compensated OTA. UGB = gm1 / (2π × Cc) where Cc is a
designer-chosen cap (4 pF), independent of the 10 pF load. Same 1.5 μA stage-1 current
achieves ~477 kHz UGB.

The 9-pin subcircuit interface is **identical** to v1. Block 02 changes only the `.include`
path and subcircuit name from `ota_pga` to `ota_pga_v2`.

---

## 2. What "Done" Means

1. `ota_pga_v2.spice` exists with subcircuit:
   `.subckt ota_pga_v2 vdd gnd inp inn out vbn vbcn vbp vbcp`
   (vbcn and vbcp are declared but left unconnected inside — legal in SPICE.)
2. `verify_pga_v2.py` passes all 5 gates at TT 27°C.
3. UGB between 400 kHz and 2 MHz at TT 27°C with 10 pF load.
4. Phase margin > 60° at 10 pF load.
5. DC gain > 65 dB.
6. All transistors in saturation, Vov > 100 mV, at TT 27°C.
7. Neither `../ota_pga/ota_pga.spice` nor `../ota_foldcasc.spice` is modified.

---

## 3. Topology — Two-Stage Miller OTA

```
VDD ──┬────────────────────────┬──────────────────────────────────┐
      │                        │                                  │
     M3(diode)               M4(mirror)                        M5(CS)
      │                        │                                  │
INP──M1─┐                  ┌──M2──INN           V_s1 ─── Rz ─── Cc ─┤
         └──otail──M11(vbn)─┘                   (M4 drain)           │
                 │                                               VOUT
                GND                                              │
                                                              M7(vbn)
                                                                 │
                                                                GND
```

**Stage 1**: NMOS differential pair M1/M2 with PMOS current mirror M3/M4 active load.
Single-ended output at M4 drain (= node `v_s1`), quiescent ≈ 1.01 V.

**Stage 2**: PMOS common-source M5, gate driven by `v_s1`. NMOS current sink M7
(gate = vbn). Both drains connect to `out`.

**Compensation**: Miller cap Cc (4 pF MIM) from `out` back to `v_s1`, with nulling
resistor Rz (~18 kΩ poly) in series on the `v_s1` side. Rz eliminates the RHP zero
that Cc would otherwise create at gm5 / (2π × Cc) ≈ 2 MHz.

---

## 4. Device Sizing

All dimensions in microns. Requires `.option scale=1e-6`.

### 4.1 Stage 1

```spice
** Tail current source — ~1.5 uA at vbn=0.629V (same as ota_pga v1)
XM11  otail  vbn    gnd  gnd  sky130_fd_pr__nfet_01v8   w=11.4  l=14

** NMOS differential pair (same as ota_pga v1)
XM1   v_s1   inp    otail gnd  sky130_fd_pr__nfet_01v8  w=5     l=14
XM2   v_mir  inn    otail gnd  sky130_fd_pr__nfet_01v8  w=5     l=14

** PMOS current mirror — self-biased (diode M3, driven M4)
** Do NOT connect gates to vbp — these are self-biased
** W=2u L=2u → Vov=0.137V at 750nA → Vsg=0.787V → v_s1 = 1.013V
XM3   v_s1   v_s1   vdd  vdd  sky130_fd_pr__pfet_01v8   w=2     l=2
XM4   v_mir  v_s1   vdd  vdd  sky130_fd_pr__pfet_01v8   w=2     l=2
```

Node `v_s1` = M3/M4 gate = M3 drain = M1 drain. Quiescent ≈ 1.01 V.
Node `v_mir` = M4 drain = M2 drain (complementary half, not used further).

**Wait — single-ended output convention**: In a standard diff-pair + mirror, the
single-ended output is taken from the M4 drain (= M2 drain side), not the M3 diode
side. Correct the connections above if needed:

```spice
** Corrected: output is M4 drain = M2 drain = v_s1
XM3   v_mir  v_mir  vdd  vdd  sky130_fd_pr__pfet_01v8   w=2     l=2   ** diode side
XM4   v_s1   v_mir  vdd  vdd  sky130_fd_pr__pfet_01v8   w=2     l=2   ** output side
XM1   v_mir  inp    otail gnd  sky130_fd_pr__nfet_01v8  w=5     l=14
XM2   v_s1   inn    otail gnd  sky130_fd_pr__nfet_01v8  w=5     l=14
```

Verify in simulation: apply a small differential voltage (inp - inn = 1 mV), confirm
that v_s1 moves in the correct direction (inp↑ → v_s1↑ for NMOS input pair with
PMOS mirror load using this convention — or the opposite depending on sign; check and
adjust the stage-2 polarity if the overall loop inverts unexpectedly).

### 4.2 Miller Compensation

```spice
** Nulling resistor in series with Cc — on the v_s1 side
** Rz = 1/gm5 ≈ 18.2 kΩ
** sky130_fd_pr__res_xhigh_po: ~2 kΩ/sq, W=0.35u
** L = 18200 / 2000 * 0.35u = 3.185u → use L=3.2u
XRz   v_s1  rz_mid  gnd  sky130_fd_pr__res_xhigh_po    w=0.35  l=3.2

** Miller compensation cap — 4 pF
** sky130_fd_pr__cap_mim_m3_1: ~1 fF/um², min W=2u
** 4 pF = 4000 fF → W=64u L=63u = 4032 fF ≈ 4 pF
XCc   rz_mid  out  gnd  sky130_fd_pr__cap_mim_m3_1     w=64    l=63
```

### 4.3 Stage 2

```spice
** PMOS common-source — gate = v_s1 (≈1.013V quiescent)
** Vsg = 1.8 - 1.013 = 0.787V, |Vtp|≈0.65V, Vov≈0.137V
** W=5u L=1u → Id = (80u/2)*(5/1)*0.137^2 = 3.75 uA
** gm5 = 2*3.75u/0.137 = 54.7 uS
XM5   out  v_s1  vdd  vdd  sky130_fd_pr__pfet_01v8      w=5     l=1

** NMOS current sink — gate = vbn, sized to match Id_M5 = 3.75 uA
** At vbn=0.629V, Vov_M7 = 0.629-0.4 = 0.229V
** W/L = 2*3.75u / (270u * 0.229^2) = 7.5u / 14.15u = 0.530
** L=2u → W = 0.530 * 2 = 1.06u → use W=1.05u (above 0.84u SKY130 min)
XM7   out  vbn   gnd  gnd  sky130_fd_pr__nfet_01v8      w=1.05  l=2
```

---

## 5. Performance Analysis

### UGB
gm1 (M1/M2 at 750 nA each, W=5u L=14u):
gm1 = sqrt(2 × 270u × 5/14 × 750n) = sqrt(144.6e-12) ≈ **12 μS**

UGB = gm1 / (2π × Cc) = 12e-6 / (2π × 4e-12) = **477 kHz** ✓ (> 425 kHz required)

### Phase margin
gm5 = 54.7 μS (from sizing above)
fp2 = gm5 / (2π × CL) = 54.7e-6 / (2π × 10e-12) = **871 kHz**
PM = 90° − arctan(UGB/fp2) = 90° − arctan(477/871) = **61.3°** ✓

RHP zero (without Rz): f_z = gm5 / (2π × Cc) = 54.7e-6 / (2π × 4e-12) = 2.18 MHz
Phase loss at UGB from zero: arctan(477/2180) = 12.3°
PM without Rz: 61.3° − 12.3° = **49°** ✗ — Rz is required.
PM with Rz (zero pushed to infinity): **61.3°** ✓

### DC gain
A1 = gm1 × (ro_M2 || ro_M4)
  ro_M2 (750 nA, L=14u): λ ≈ 0.08/14 = 0.00571 V⁻¹ → ro_M2 ≈ 234 MΩ
  ro_M4 (750 nA, L=2u):  λ ≈ 0.09/2  = 0.045  V⁻¹ → ro_M4 ≈ 29.6 MΩ
  A1 = 12u × 26.2M = 315 → **49.97 dB**

A2 = gm5 × (ro_M5 || ro_M7)
  ro_M5 (3.75 uA, L=1u): λ ≈ 0.09/1 = 0.09 V⁻¹ → ro_M5 ≈ 2.96 MΩ
  ro_M7 (3.75 uA, L=2u): λ ≈ 0.08/2 = 0.04 V⁻¹ → ro_M7 ≈ 6.67 MΩ
  A2 = 54.7u × 2.03M = 111 → **40.9 dB**

Total DC gain = 49.97 + 40.9 = **90.9 dB** ✓ (>> 65 dB spec)

### Output swing
Vout_max = VDD − Vov_M5 = 1.8 − 0.137 = **1.663 V**
Vout_min = Vov_M7 = Vgs_M7 − Vtn = 0.629 − 0.4 = **0.229 V**
Swing = 1.663 − 0.229 = **1.43 Vpp** ✓

### Power
Stage 1: 1.5 μA × 1.8 V = 2.70 μW
Stage 2: 3.75 μA × 1.8 V = 6.75 μW
Mirrors/overhead: ~0.5 μA × 1.8 V ≈ 0.9 μW
Total: **~10.4 μW** (spec: <10 μW — optimize M7 to 3.3 μA if needed)

---

## 6. Expected Operating Point Table

Fill in measured values after simulation:

| Parameter            | Predicted  | Simulated (TT 27°C) |
|----------------------|------------|---------------------|
| Itail (M11)          | 1.50 μA    |                     |
| Id_stage2 (M5/M7)    | 3.75 μA    |                     |
| Total supply current | ~5.8 μA    |                     |
| Power                | ~10.4 μW   |                     |
| v_s1 quiescent       | ~1.013 V   |                     |
| Vout quiescent       | ~0.9 V     |                     |
| gm1                  | ~12 μS     |                     |
| gm5                  | ~54.7 μS   |                     |
| UGB                  | ~477 kHz   |                     |
| Phase margin         | ~61.3°     |                     |
| DC gain              | ~91 dB     |                     |
| Output swing         | ~1.43 Vpp  |                     |
| Slew rate            | ~375 mV/μs |                     |

---

## 7. Testbenches

Use the same testbench structure as `../ota_pga/tb_pga_*.spice` with two changes:
1. `ota_pga` → `ota_pga_v2` (subcircuit name)
2. All file names use `_pga_v2_` infix (e.g., `tb_pga_v2_ac.spice`)

Bias instantiation (unchanged — vbp/vbcn/vbcp go to ota_pga_v2 pins, just unconnected inside):

```spice
.include "../../00_bias/bias_distribution/design_full.cir"
Xbias vdd gnd iref_out vbn vbcn vbp vbcp  bias_generator_full
Riref iref_out gnd 3560
Xota  vdd gnd inp inn out vbn vbcn vbp vbcp  ota_pga_v2
```

AC sweep range: `.ac dec 100 1k 100Meg` — must span well above 477 kHz UGB.

---

## 8. `verify_pga_v2.py` — Updated Gate Thresholds

Copy `../ota_pga/verify_pga.py` to `verify_pga_v2.py`. Update constants:

```python
NETLIST   = "ota_pga_v2.spice"
SUBCKT    = "ota_pga_v2"
LOGFILE   = "verification_report_pga_v2.txt"

# Gate 1
ITAIL_TARGET_NA   = 1500      # M11 tail, unchanged
ID_STAGE2_MIN_NA  = 2500      # M7 current sink — new check
ID_STAGE2_MAX_NA  = 5000
VOV_MIN_MV        = 100

# Gate 2
GAIN_MIN_DB       = 65
UGB_MIN_HZ        = 400_000   # CHANGED
UGB_MAX_HZ        = 2_000_000 # CHANGED
PM_MIN_DEG        = 60

# Gate 3
SLEW_MIN_MV_US    = 50        # Id2/CL = 3.75uA/10pF = 375mV/us; gate at 50
SWING_MIN_VPP     = 1.0

# Gate 4
PSRR_MIN_DB       = 60
CMRR_MIN_DB       = 70

# Gate 5
CORNER_UGB_MIN_HZ = 250_000   # CHANGED
CORNER_PM_MIN_DEG = 55
```

---

## 9. Troubleshooting

**If PM < 60°:**
- Increase Cc to 5 pF (lowers UGB, improves fp2/UGB ratio).
- Increase M7 W by 20% to raise gm5 → raise fp2.
- Increase Rz by 20% above 1/gm5 to move the compensated zero into LHP (adds phase lead).

**If UGB < 400 kHz:**
- Reduce Cc to 3 pF.
- Confirm vbn gives Itail = 1.5 μA — measure I(XM11).

**If v_s1 quiescent is not ≈ 1.01 V:**
M3/M4 W/L controls v_s1. Increase W3=W4 → lower Vov → lower Vsg → higher v_s1.
Target: 0.8 V < v_s1 < 1.2 V.

**If M7 is in triode (Vds_M7 < Vov_M7 = 0.23V):**
Vout is below 0.23 V. Reduce W7 to lower Id2, which raises Vout.

**If M5 is in triode (Vsd_M5 < Vov_M5):**
Vout is too high (above 1.663 V). Increase W7.

**If power > 10 μW:**
Reduce M7 from W=1.05u to W=0.95u — lowers Id2 to ~3.3 μA → power ≈ 9.1 μW.
Verify PM is still >60° after the change (gm5 drops, fp2 drops).

**If PSRR fails:**
Two-stage Miller OTA has a VDD feedforward path through Cc. Add 50–100 Ω in
series with VDD supply line to M3/M4/M5 if PSRR < 60 dB at 1 kHz.

---

## 10. `specs_pga_v2.json`

Create this file with the target values. Fill in measured values after simulation.

```json
{
  "name": "VibroSense PGA OTA v2 (two-stage Miller, 477 kHz)",
  "description": "Two-stage Miller OTA replacing folded-cascode v1 (67.5kHz). Achieves 477kHz UGB for 25kHz closed-loop BW at 16x PGA gain. Same 9-pin interface.",
  "supply_v": 1.8,
  "topology": "two-stage Miller",
  "stage1_tail_ua": 1.5,
  "stage2_current_ua": 3.75,
  "miller_cap_pf": 4.0,
  "nulling_resistor_kohm": 18.2,
  "measurements": {
    "dc_gain_db":               {"target": ">65",               "weight": 15},
    "ugb_hz":                   {"target": "400000 to 2000000", "weight": 25},
    "phase_margin_deg":         {"target": ">60",               "weight": 25},
    "input_noise_nv_sqrthz_1k": {"target": "<400",              "weight": 5},
    "cmrr_db":                  {"target": ">70",               "weight": 10},
    "psrr_db":                  {"target": ">60",               "weight": 10},
    "power_uw":                 {"target": "<10",               "weight": 10}
  }
}
```

---

## 11. Files to Create in This Folder

```
ota_pga_v2.spice
specs_pga_v2.json
verify_pga_v2.py
tb_pga_v2_ac.spice
tb_pga_v2_dc.spice
tb_pga_v2_tran.spice
tb_pga_v2_psrr.spice
tb_pga_v2_cmrr.spice
tb_pga_v2_corner_tt.spice
tb_pga_v2_corner_ss.spice
tb_pga_v2_corner_ff.spice
tb_pga_v2_corner_sf.spice
tb_pga_v2_corner_fs.spice
tb_pga_v2_temp_m40.spice
tb_pga_v2_temp_27.spice
tb_pga_v2_temp_85.spice
README.md
verification_report_pga_v2.txt
```

## 12. Files Never to Touch

```
../ota_pga/          ← entire folder frozen (v1, passes its own spec)
../ota_foldcasc.spice
../verify_design.py
../specs.json
../tb_*.spice
```

---

## 13. Interface Contract (for Block 02)

```
File:    01_ota/ota_pga_v2/ota_pga_v2.spice
Subckt:  ota_pga_v2 vdd gnd inp inn out vbn vbcn vbp vbcp
UGB:     ~477 kHz at 10 pF
PM:      >60°

Used pins:   vdd, gnd, inp, inn, out, vbn
Unused pins: vbcn, vbp, vbcp (declared but unconnected inside subcircuit)

Bias:    00_bias/bias_distribution/design_full.cir → bias_generator_full
         vbp/vbcn/vbcp from bias_generator_full connect to ota_pga_v2 pins
         but are left floating inside the subcircuit — this is correct.
```
