# Block 05: True RMS Detector + Peak Detector + Crest Factor -- Design Report

**Project:** VibroSense-1 Analog Vibration Anomaly Detection Chip
**Process:** SkyWater SKY130A -- FULLY TRANSISTOR-LEVEL (no behavioral models)
**Supply:** 1.8V single supply
**Power:** 8.0 uW (budget: <25 uW)
**Status:** ALL 10 SPECS PASS -- including full PVT sweep (5 corners x 3 temperatures)

---

## Executive Summary

Block 05 extracts broadband RMS amplitude and peak amplitude from the PGA output, enabling crest factor computation in the MCU. The entire design uses **real SKY130 MOSFETs** -- no behavioral models, no B-sources, no ideal voltage-controlled sources.

The architecture uses a **single-pair MOSFET square-law squarer** that exploits the strong-inversion `Id = (K/2)(Vgs - Vth)^2` relationship. A signal NFET (gate = Vin) and a reference NFET (gate = Vcm) produce a differential current whose DC component after low-pass filtering is proportional to `mean(V^2) = RMS^2`. This works for **any symmetric waveform** (sine, square, triangle, noise) without waveform-specific correction factors.

The peak detector uses a 5-transistor OTA comparator with an NMOS source follower charging a 500 pF hold capacitor, with subthreshold NMOS pseudo-resistor discharge.

Total transistor count: **10 MOSFETs**, 8 resistors, 3 capacitors. Power: **8.0 uW** at 1.8V.

---

## Key Results (TT/27C)

| # | Parameter | Specification | Measured | Status |
|---|-----------|--------------|----------|--------|
| 1 | RMS accuracy (calibrated) | < 5% at 100 mVpk | **1.6%** | **PASS** |
| 2 | RMS linearity | R2 > 0.99 | **R2 = 0.99992** | **PASS** |
| 3 | RMS bandwidth | 10 Hz - 10 kHz (-3 dB) | **10 Hz - 20 kHz** | **PASS** |
| 4 | Peak accuracy (100 mVpk) | < 10% | **5.2%** | **PASS** |
| 5 | Peak hold (500 ms) | < 10% decay | **3.1%** | **PASS** |
| 6 | Crest factor (sine) | 1.414 +/- 15% | **1.363 (3.6% err)** | **PASS** |
| 7 | Crest factor (square) | 1.000 +/- 15% | **0.962 (3.8% err)** | **PASS** |
| 8 | Crest factor (triangle) | 1.732 +/- 15% | **1.655 (4.5% err)** | **PASS** |
| 9 | Total power | < 25 uW | **8.0 uW** | **PASS** |
| 10 | PVT all corners pass | All 15 corners | **YES** | **PASS** |

---

## PVT Sweep Results (5 corners x 3 temperatures)

All 15 process/temperature corners pass all specs:

| Corner | Temp | RMS Acc | CF Sine | CF Square | CF Triangle | Power |
|--------|------|---------|---------|-----------|-------------|-------|
| TT | -40C | 0.4% | 6.3% | 6.3% | 7.0% | 7.4 uW |
| TT | 27C | 1.6% | 3.6% | 3.8% | 4.5% | 8.0 uW |
| TT | 85C | 2.6% | 1.5% | 2.0% | 2.5% | 8.6 uW |
| SS | -40C | 0.3% | 6.7% | 6.7% | 7.6% | 5.7 uW |
| SS | 27C | 1.8% | 3.8% | 4.1% | 4.7% | 6.2 uW |
| SS | 85C | 2.8% | 1.6% | 2.0% | 2.6% | 6.7 uW |
| FF | -40C | 0.3% | 5.9% | 6.0% | 6.7% | 9.5 uW |
| FF | 27C | 1.2% | 3.5% | 3.5% | 4.4% | 10.2 uW |
| FF | 85C | 2.1% | 1.6% | 2.1% | 2.6% | 10.8 uW |
| SF | -40C | 0.3% | 6.5% | 6.6% | 7.3% | 10.3 uW |
| SF | 27C | 1.1% | 4.3% | 4.7% | 5.2% | 10.9 uW |
| SF | 85C | 1.9% | 2.5% | 3.0% | 3.6% | 11.4 uW |
| FS | -40C | 0.2% | 6.3% | 6.2% | 7.1% | 5.2 uW |
| FS | 27C | 1.8% | 3.3% | 3.4% | 4.2% | 5.7 uW |
| FS | 85C | 2.7% | 1.1% | 1.4% | 2.1% | 6.2 uW |

**Worst-case across all PVT:** RMS accuracy 2.8%, CF sine 6.7%, CF triangle 7.6%, Power 11.4 uW

---

## 1. Circuit Topology

### 1.1 Architecture

```
                                        +-----------------+
Vin (Vcm + V_signal) ---+-------+------|  RMS Squarer    |
                         |       |      |  Signal NFET    |--- sq_sig ---> LPF ---> rms_out
                         |       |      +-----------------+
                         |       |
                         |       |      +-----------------+
                         |       +------|  RMS Squarer    |
                         |              |  Reference NFET |--- sq_ref ---> LPF ---> rms_ref
                         |              |  (gate = Vcm)   |
                         |              +-----------------+
                         |
                         |              +-----------------+
                         +--------------|  Peak Detector  |--- peak_out
                                        |  OTA + follower |
                                        |  + 500pF hold   |
                                        +-----------------+

MCU computes: RMS = sqrt((rms_ref - rms_out) / alpha)
              CF  = peak / RMS
```

### 1.2 How the Square-Law Squarer Works

The core insight exploits the MOSFET strong-inversion square law: `Id = (K/2)(Vgs - Vth)^2`.

**Signal NFET** (gate at `inp = Vcm + V`):
```
Id_sig = (K/2)(Vov + V)^2 = (K/2)[Vov^2 + 2*Vov*V + V^2]
```

**Reference NFET** (gate at `Vcm`, matched device):
```
Id_ref = (K/2)(Vov)^2
```

**Difference current through matched load resistors:**
```
dI = Id_sig - Id_ref = (K/2)[2*Vov*V + V^2]
```

**After low-pass filtering** (for any symmetric AC signal where `mean(V) = 0`):
```
mean(dI) = (K/2) * mean(V^2) = (K/2) * RMS^2
```

The linear term `2*Vov*V` averages to zero -- no inverter circuit needed. The LPF (fc = 50 Hz) removes the ripple at the signal frequency. The MCU calibrates `alpha = K*R/2` using a known reference signal during startup.

### 1.3 Subcircuit Details

**5-Transistor OTA** (`ota5`): NMOS differential pair (W=4u, L=2u) with PMOS current mirror load (W=2u, L=2u). Tail current set by NMOS (W=2u, L=4u) biased by `vbn` from Block 00. DC gain ~50 dB, GBW ~500 kHz at 1.25 uA. Used only for the peak detector.

**RMS Squarer** (`rms_squarer`): Two matched NFETs (W=0.84u, L=6u) with 100k poly load resistors. Signal NFET gate = inp, reference NFET gate = Vcm. 1k isolation resistors to LPF. The large L=6u ensures good matching and deep strong-inversion operation at Vcm = 0.9V (Vov ~ 0.4V).

**Passive RC LPF** (`lpf_rc`): R = 3.18 Mohm, C = 1 nF. fc = 1/(2*pi*R*C) = 50 Hz. Settling to 1% in ~16 ms. The 1 nF cap is off-chip for the prototype; pad included.

**Peak Detector** (`peak_detector`): OTA5 compares `inp` to held peak voltage. NMOS source follower (W=4u, L=0.5u) charges 500 pF hold capacitor. Subthreshold NMOS discharge (W=0.42u, L=20u, Vgs~0) provides >10 Gohm impedance for slow decay. NMOS reset switch (W=1u, L=0.5u) controlled by MCU GPIO.

### 1.4 Device Count and Sizing

| Subcircuit | MOSFETs | Key Sizes |
|------------|---------|-----------|
| RMS squarer | 2 | Signal/Ref NFET: W=0.84u, L=6u |
| Peak OTA | 5 | Diff pair: 4u/2u, Mirror: 2u/2u, Tail: 2u/4u |
| Peak output | 3 | Charge: 4u/0.5u, Discharge: 0.42u/20u, Reset: 1u/0.5u |
| **Total** | **10** | + 8 resistors, 3 capacitors |

### 1.5 Power Budget

| Subcircuit | Current | Power |
|------------|---------|-------|
| RMS squarer (2 NFETs + loads) | ~2.5 uA | 4.5 uW |
| Peak OTA | 1.25 uA | 2.25 uW |
| Peak charge/discharge | ~0.1 uA avg | 0.2 uW |
| LPF leakage | ~0.5 uA | 0.9 uW |
| **Total** | **~4.4 uA** | **8.0 uW** |

---

## 2. Simulation Results

### 2.1 RMS Linearity

The squarer output `dV = V_ref - V_sig` is proportional to `V^2` with excellent linearity:

| Input (mVpk) | Squarer dV (mV) | Ideal V^2 (uV^2) | Alpha |
|--------------|-----------------|-------------------|-------|
| 10 | 0.063 | 50 | 1.258 |
| 20 | 0.250 | 200 | 1.252 |
| 50 | 1.558 | 1250 | 1.246 |
| 100 | 6.224 | 5000 | 1.245 |
| 150 | 14.01 | 11250 | 1.245 |
| 200 | 24.90 | 20000 | 1.245 |
| 300 | 55.92 | 45000 | 1.243 |

**R2 = 0.99992** -- near-perfect square-law behavior over the full 10-300 mVpk range.

![RMS Linearity](plot_rms_linearity.png)

### 2.2 RMS Frequency Response

Flat within -3 dB from 10 Hz to 20 kHz (100 mVpk sine). The squarer has no frequency-dependent gain -- bandwidth is set entirely by the input signal path.

![Frequency Response](plot_rms_freq_response.png)

### 2.3 Peak Hold Time

- Peak at 15 ms: ~94.5 mV above Vcm
- Decay at 500 ms: **3.1%** (spec: <10%)
- Decay at 1 s: ~6.3%

The subthreshold NMOS discharge transistor (W=0.42u, L=20u, Vgs~0) provides >10 Gohm impedance. Combined with 500 pF hold cap: tau >> 5 s.

![Peak Hold](plot_peak_hold.png)

### 2.4 Peak Accuracy

| Input (mVpk) | Measured Peak (mV above Vcm) | Ideal | Error |
|--------------|------------------------------|-------|-------|
| 50 | 46.5 | 50 | 7.0% |
| 100 | 94.8 | 100 | **5.2%** |
| 150 | 143.3 | 150 | 4.5% |
| 200 | 191.2 | 200 | 4.4% |
| 300 | 283.0 | 300 | 5.7% |

The ~5 mV offset comes from the NMOS source follower tracking error (limited by OTA finite gain).

![Peak Accuracy](plot_peak_accuracy.png)

### 2.5 Crest Factor

| Waveform | Ideal CF | Measured CF | Error | Status |
|----------|----------|-------------|-------|--------|
| Sine | 1.414 | 1.363 | **3.6%** | **PASS** |
| Square | 1.000 | 0.962 | **3.8%** | **PASS** |
| Triangle | 1.732 | 1.655 | **4.5%** | **PASS** |

The true-RMS squarer measures `mean(V^2)` directly, so crest factor accuracy is waveform-independent. All three test waveforms pass with <5% error -- a major improvement over the previous rectifier-based approach which required waveform-specific calibration.

![Crest Factor](plot_crest_factor.png)

### 2.6 Waveform Detail (100 mVpk, 1 kHz sine, TT/27C)

![Basic Test Waveform](plot_basic_test.png)

---

## 3. Design History

### 3.1 Previous Approach: 3-OTA Full-Wave Rectifier (REJECTED)

The initial design used a 3-OTA precision full-wave rectifier (inverting amplifier + two half-wave detectors with class-AB output stages) measuring Mean Absolute Value (MAV). This required a waveform-dependent correction factor (pi/2*sqrt(2) for sine) to approximate RMS.

**Problems:**
- MAV-to-RMS conversion is waveform-dependent -- crest factor failed for square (23.4% err) and triangle (25.9% err)
- RMS accuracy was 9.0% even after calibration
- 31 MOSFETs, 15.5 uW
- PVT failures across multiple corners

### 3.2 Current Approach: Single-Pair Square-Law Squarer

The redesign exploits MOSFET square-law physics to compute `mean(V^2)` directly:
- **Waveform-independent**: works for sine, square, triangle, noise, impulses
- **No inverter needed**: the linear term cancels by time-averaging
- **10 MOSFETs** (down from 31) -- simpler layout, better matching
- **8.0 uW** (down from 15.5 uW)
- **All PVT corners pass** with comfortable margins

---

## 4. Mismatch Sensitivity Analysis

| Source | Mechanism | Impact |
|--------|-----------|--------|
| Squarer Vth mismatch (sigma = 3.15 mV) | DC offset in squarer output | < 1% after digital offset removal |
| Load resistor mismatch (~0.5%) | Gain error: dR/R -> dRMS/RMS at ~0.25% | Negligible |
| OTA offset (~5-10 mV) | Peak detector tracking error | ~5% at 100 mVpk (within spec) |
| Temperature variation | Mobility/Vth shift changes squarer alpha | Per-temperature calibration in MCU eliminates this |

Expected yield at 3-sigma mismatch: >95% within spec after digital calibration.

---

## 5. Deliverables

| File | Description |
|------|-------------|
| `design.cir` | Complete transistor-level netlist (10 MOSFETs, SKY130) |
| `run_all.py` | Full PVT simulation suite (15 corners, 6 test categories) |
| `results_summary.txt` | PASS/FAIL summary for all 10 specs |
| `results_full.json` | Detailed numerical results for all corners |
| `plot_rms_linearity.png` | Squarer linearity (R2 = 0.99992) |
| `plot_rms_freq_response.png` | Frequency response (10 Hz - 20 kHz) |
| `plot_peak_hold.png` | Peak hold decay (3.1% at 500 ms) |
| `plot_peak_accuracy.png` | Peak detector accuracy vs amplitude |
| `plot_crest_factor.png` | Crest factor: sine/square/triangle |
| `plot_basic_test.png` | Detailed waveform plot (TT/27C) |
| `program.md` | Full design procedure and analysis |
| `new_program.md` | Fix instructions for the squarer redesign |

---

## 6. Interface to Downstream Blocks

| Pin | Direction | Range | Notes |
|-----|-----------|-------|-------|
| `inp` | Input | Vcm +/- 300 mV | From PGA (Block 02), 10 Hz - 10 kHz |
| `rms_out` | Output | ~Vcm (drops with signal) | Squarer signal path; `rms_ref - rms_out` prop RMS^2 |
| `rms_ref` | Output | ~Vcm (constant DC) | Squarer reference path |
| `peak_out` | Output | Vcm to Vcm + 300 mV | Held peak; 3.1% decay at 500 ms |
| `reset` | Input | 0 or 1.8 V | MCU GPIO; HIGH = discharge peak hold cap |
| `vbn` | Input | ~0.65 V | NMOS bias from Block 00 bias generator |
| `vcm` | Input | 0.9 V | Common-mode voltage from Block 00 |
| `vdd` | Supply | 1.8 V | |
| `vss` | Ground | 0 V | |

**MCU Computation:**
```
alpha = calibrated from known reference signal during startup
RMS   = sqrt((V_rms_ref - V_rms_out) / alpha)
CF    = V_peak / RMS
```

---

*Design verified 2025-03-24 at transistor level. SKY130, all 5 corners (TT/SS/FF/SF/FS) x 3 temperatures (-40/27/85C). 10 MOSFETs, 8.0 uW. All specs pass.*
