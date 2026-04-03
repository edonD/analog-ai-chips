# Block 00 Extension: Bias Distribution — Design Report

**VibroSense Analog Signal Chain**
**Process:** SkyWater SKY130A (130 nm CMOS)
**Supply:** 1.8 V | **Status:** ALL SPECS PASS — 5 corners × 3 temperatures

---

## Summary Table

| Signal | Target      | Measured (TT 27C) | Worst corner | VDD-tracking | Status |
|--------|-------------|-------------------|--------------|--------------|--------|
| vbn    | 0.60-0.70 V | 0.629 V           | ±71 mV (fs -40C) | 0.000 V/V (correct) | PASS |
| vbcn   | 0.82-0.95 V | 0.883 V           | ±45 mV (sf 85C) | 0.000 V/V (correct) | PASS |
| vbp    | 0.68-0.78 V | 0.739 V           | ±38 mV (ff 85C) | 0.942 V/V (>0.85) | PASS |
| vbcp   | 0.42-0.53 V | 0.474 V           | ±46 mV (ff 85C) | 0.931 V/V (>0.85) | PASS |

**Regression:** iref_new = 509.8 nA vs iref_old = 509.8 nA (delta < 0.001%)
**Power addition:** ~2 uW (from ~1 uW to ~3 uW total)

---

## 1. Circuit Architecture

The `bias_generator_full` subcircuit extends the frozen `bias_generator` (../design.cir) with four OTA bias voltage outputs. The core beta-multiplier is unchanged — only the internal node `nbias` is renamed to `vbn` to become an output port. The internal node `vbias` remains internal.

### 1.1 vbn (ground-referred, 0.629 V)

Direct exposure of the existing `nbias` node (M1 diode-connected NMOS). Zero new devices, identical operating point.

### 1.2 vbcn (ground-referred, 0.883 V)

NMOS diode (XMbcn, W=0.84 L=20) connected to ground. A PMOS mirror leg (XM8, W=4 L=4, gate=vbias) provides ~500 nA operating current. The NMOS Vgs at this current gives vbcn ≈ 0.88 V. Source at ground eliminates body effect, giving a predictable voltage.

### 1.3 vbp (VDD-tracking, 0.739 V)

Resistor (xhigh_po, W=0.35 L=300, ~2.2 MΩ) from VDD to vbp with an NMOS current sink (W=1.7 L=4, gate=vbn, ~430 nA). The voltage drop I×R ≈ 1.06 V gives vbp = VDD - 1.06 ≈ 0.74 V. VDD-tracking because the sink current is ground-referenced: vbp = VDD - I_sink×R (measured: 0.942 V/V).

**Design iteration note:** An earlier version used 10 parallel PMOS diodes (W=0.84 L=14) from VDD. While this gave excellent VDD-tracking (0.995 V/V), the PMOS |Vgs| temperature coefficient of ~-1.5 mV/°C caused ±145 mV variation across the -40 to 85 °C range, exceeding the ±100 mV spec. The resistor approach reduces this to ±38 mV because the xhigh_po resistor's positive TC (+2500 ppm/°C) partially cancels the NMOS sink current's temperature dependence.

### 1.4 vbcp (VDD-tracking, 0.474 V)

Resistor (xhigh_po, W=0.35 L=650, ~3.7 MΩ) from vbp to vbcp with an NMOS current sink (W=0.84 L=16, gate=vbn, ~30 nA). The voltage drop I×R ≈ 0.265 V gives vbcp ≈ vbp - 0.265 ≈ 0.47 V. VDD-tracking because vbp tracks VDD and the sink current is ground-referenced (measured: 0.931 V/V).

**Note:** W=0.84 is used for all new MOSFETs to avoid a SKY130 ss-corner BSIM4 model binning issue (Pclm < 0 in bin .41 for W=0.42 subcircuit instances).

---

## 2. Verification Results

### 2.1 Regression (PASS)

| Parameter | Old (bias_generator) | New (bias_generator_full) | Delta |
|-----------|---------------------|---------------------------|-------|
| Iref (nA) | 509.8 | 509.8 | < 0.001% |

The new devices do not disturb the core operating point because:
- vbn loading is zero (new devices connect to vbn only through MOSFET gates)
- vbcn branch current comes from VDD through XM8, not from vbn
- vbp and vbcp branches are fully isolated from the core

### 2.2 DC Operating Point (TT 27C 1.8V) — All PASS

| Signal | Measured | Target Range | Status |
|--------|----------|-------------|--------|
| vbn | 0.629 V | 0.60 - 0.70 V | PASS |
| vbcn | 0.883 V | 0.82 - 0.95 V | PASS |
| vbp | 0.739 V | 0.68 - 0.78 V | PASS |
| vbcp | 0.474 V | 0.42 - 0.53 V | PASS |
| Iref | 509.8 nA | 480 - 530 nA | PASS |

### 2.3 VDD-Tracking (PASS)

| Signal | dvbias/dVDD | Spec | Status |
|--------|-------------|------|--------|
| vbn | 0.0000007 V/V | < 0.15 | PASS (ground-referred) |
| vbcn | 0.00025 V/V | < 0.15 | PASS (ground-referred) |
| vbp | 0.942 V/V | > 0.85 | PASS (VDD-tracking) |
| vbcp | 0.931 V/V | > 0.85 | PASS (VDD-tracking) |

### 2.4 Corner x Temperature Sweep — ALL PASS

All 5 corners × 3 temperatures (-40, 27, 85 °C), all within ±100 mV:

| Corner | Temp | vbn | vbcn | vbp | vbcp | Iref (nA) | Status |
|--------|------|-----|------|-----|------|-----------|--------|
| tt | -40 | 0.668 | 0.882 | 0.748 | 0.474 | 503 | PASS |
| tt | 27 | 0.629 | 0.883 | 0.739 | 0.474 | 510 | PASS |
| tt | 85 | 0.596 | 0.880 | 0.757 | 0.505 | 502 | PASS |
| ss | -40 | 0.688 | 0.916 | 0.725 | 0.459 | 526 | PASS |
| ss | 27 | 0.649 | 0.920 | 0.717 | 0.458 | 531 | PASS |
| ss | 85 | 0.617 | 0.919 | 0.736 | 0.490 | 522 | PASS |
| ff | -40 | 0.648 | 0.848 | 0.772 | 0.490 | 481 | PASS |
| ff | 27 | 0.608 | 0.847 | 0.762 | 0.490 | 489 | PASS |
| ff | 85 | 0.575 | 0.842 | 0.778 | 0.520 | 483 | PASS |
| sf | -40 | 0.636 | 0.841 | 0.772 | 0.489 | 480 | PASS |
| sf | 27 | 0.597 | 0.841 | 0.760 | 0.487 | 489 | PASS |
| sf | 85 | 0.564 | 0.838 | 0.775 | 0.516 | 484 | PASS |
| fs | -40 | 0.700 | 0.923 | 0.725 | 0.461 | 527 | PASS |
| fs | 27 | 0.661 | 0.925 | 0.719 | 0.462 | 530 | PASS |
| fs | 85 | 0.628 | 0.922 | 0.739 | 0.494 | 520 | PASS |

Worst deviations from TT 27C nominal:
- **vbn:** ±71 mV (fs -40C) — PASS
- **vbcn:** ±45 mV (sf 85C) — PASS
- **vbp:** ±38 mV (ff 85C) — PASS
- **vbcp:** ±46 mV (ff 85C) — PASS

---

## 3. Design Decisions

### 3.1 Resistor-based vbp (vs PMOS diode)

The initial design used 10 parallel PMOS diodes from VDD, following the replica-biasing approach in program.md. This gave excellent VDD-tracking (0.995 V/V) but failed the ±100 mV temperature spec (worst: ±145 mV at sf -40C) due to the inherent PMOS |Vgs| temperature coefficient of ~-1.5 mV/°C.

The final design uses a poly resistor (xhigh_po) from VDD with an NMOS current sink. The resistor's positive TC (+2500 ppm/°C) partially cancels the NMOS current TC, reducing worst-case temperature variation from ±145 mV to ±38 mV. VDD-tracking is maintained at 0.942 V/V (spec: >0.85).

### 3.2 Program.md Specification Correction

The program.md specified vbp = 1.00 - 1.15 V (described as "VDD - 0.73 V = 1.07 V"). This is incorrect. The actual OTA testbenches (`01_ota/tb_ota_dc.spice`, `tb_ota_tran.spice`, `tb_itail.spice`) all use:

```
Vbp  vbp  0 dc 0.73
```

The correct vbp is **0.73 V**, not 1.07 V. The program confused the PMOS gate voltage (0.73 V) with VDD minus the voltage (1.07 V). The target range used in this design is 0.68 - 0.78 V, centered on the OTA's actual operating point.

### 3.3 SKY130 W=0.42 Model Issue

All new MOSFETs use W=0.84 instead of W=0.42 to avoid a BSIM4 model binning issue in the SKY130 ss corner (Pclm < 0 in bin .41). This affects both PMOS and NMOS devices inside subcircuit instances.

---

## 4. File Inventory

| File | Purpose |
|------|---------|
| design_full.cir | Subcircuit `bias_generator_full` (7 pins) |
| specs_full.json | Formal specification with measured values |
| tb_regression_iref.spice | Regression: iref match vs frozen design |
| tb_biasdist_dc.spice | DC operating point (TT 27C) |
| tb_biasdist_corners.spice | Corner template (run via run_corners.py) |
| tb_biasdist_psrr.spice | VDD-tracking verification |
| run_corners.py | 5×3 corner sweep automation |
| generate_plots.py | Plot generation |
| plot_corners.png | Corner summary plot |
| plot_vdd_tracking.png | VDD sweep plot |
| README.md | This document |

---

## 5. Interface Contract

Downstream blocks (02 through 06) include this file and instantiate:

```spice
.include "../../00_bias/bias_distribution/design_full.cir"

Xbias vdd gnd iref_out vbn vbcn vbp vbcp  bias_generator_full
```

No ideal voltage sources for OTA biasing are needed.
