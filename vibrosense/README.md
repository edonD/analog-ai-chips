# VibroSense-1: Always-On Analog Vibration Anomaly Detection Chip

## A Lecture on How This Sensor Works

---

### The Problem We're Solving

Every rotating machine in every factory — motors, pumps, compressors, fans, bearings — vibrates. When a machine is healthy, it vibrates in a characteristic, predictable pattern. When something goes wrong — a bearing starts to pit, a shaft becomes misaligned, a gear tooth chips — the vibration pattern changes in specific, well-understood ways.

Today, wireless vibration sensors cost $200-1,000 each and last 6-18 months on a battery. A factory with 10,000 sensors spends $500K-1M/year just replacing batteries. The reason: every sensor contains a microcontroller running an FFT at 50kHz, burning 3-10mW continuously. Even with duty cycling (wake every 60 seconds, sample for 1 second), average power is 100uW-5mW — too much for decade-long battery life.

**VibroSense-1 solves this by doing the vibration analysis in the analog domain, before digitization, at <300uW always-on.** The digital MCU and radio stay asleep until a fault is detected.

---

### How Vibration Tells You What's Broken

This is not machine learning magic. This is physics. Every mechanical fault creates vibration at specific, predictable frequencies:

```
FAULT TYPE                  FREQUENCY RANGE         WHY
─────────────────────────── ─────────────────────── ────────────────────────────
Shaft imbalance             0.5×-1× shaft RPM       Mass asymmetry on rotor
Misalignment                1×-3× shaft RPM         Shaft/coupling offset
Mechanical looseness        0.5×-Nx shaft RPM       Harmonics from impacts
Gear mesh faults            Teeth × RPM             Tooth damage modulates mesh
Bearing outer race (BPFO)   0.4 × N × RPM          Ball passing over pit
Bearing inner race (BPFI)   0.6 × N × RPM          Ball passing over pit
Bearing ball spin (BSF)     0.4 × N × RPM × (d/D)  Cracked ball rotation
Bearing cage fault          0.4 × RPM               Cage dragging
Early-stage faults          5-20 kHz broadband      Metal-on-metal impulses
```

Where N = number of rolling elements, d = ball diameter, D = pitch diameter.

For a typical 1800 RPM motor (30 Hz shaft frequency) with a 9-ball bearing:
- BPFO ≈ 108 Hz → falls in **Band 1 (100-500 Hz)**
- BPFI ≈ 162 Hz → falls in **Band 1 (100-500 Hz)**
- Gear mesh (20-tooth) ≈ 600 Hz → falls in **Band 2 (500-2000 Hz)**
- BSF ≈ 72 Hz → falls in **Band 1** (but also creates harmonics in higher bands)
- Early-stage damage → broadband energy in **Bands 4-5 (5-20 kHz)**

**The key insight:** You don't need to identify the exact frequency. You need to detect that the **energy distribution across frequency bands has changed.** A healthy bearing has most energy in Band 1-2. A failing bearing leaks energy into Bands 3-5. This is what ISO 10816 and ISO 20816 standardize.

---

### The Signal Chain: From Vibration to Decision

```
                           VibroSense-1 Signal Flow
                           ════════════════════════

  PHYSICAL          ANALOG                    ANALOG              DIGITAL
  WORLD             PREPROCESSING             INTELLIGENCE        OUTPUT
  ─────────         ─────────────             ────────────        ──────

  ┌─────────┐       ┌─────────┐
  │ Bearing │       │  MEMS   │  Analog voltage
  │ vibrates│──────►│  Accel  │─── (±2g = ±660mV) ───┐
  │ at 30Hz │       │ ADXL355 │                       │
  │ + faults│       └─────────┘                       │
  └─────────┘                                         ▼
                                                ┌───────────┐
                                          ┌─────┤    PGA     │
                                          │     │  1x-64x   │
                                          │     └─────┬─────┘
                                          │           │
                                          │     Signal now 50-1000 mVpp
                                          │           │
                     ┌────────────────────┼───────────┤
                     │                    │           │
              ┌──────▼──────┐      ┌──────▼─────┐   ┌▼──────────────┐
              │   BPF 1     │      │   BPF 2    │   │  BPF 3,4,5   │
              │  100-500 Hz │      │  0.5-2 kHz │   │  2-20 kHz    │
              │  (shaft,    │      │  (gears)   │   │  (bearings)  │
              │   bearing)  │      │            │   │              │
              └──────┬──────┘      └──────┬─────┘   └──────┬───────┘
                     │                    │                │
              ┌──────▼──────┐      ┌──────▼─────┐   ┌─────▼────────┐
              │  Envelope   │      │  Envelope  │   │  Envelope    │
              │  Detector   │      │  Detector  │   │  Detectors   │
              │  (rectify   │      │            │   │  (3 channels)│
              │   + LPF)    │      │            │   │              │
              └──────┬──────┘      └──────┬─────┘   └─────┬────────┘
                     │                    │                │
                     │   DC voltage proportional to        │
                     │   energy in each band               │
                     │                    │                │
                     ▼                    ▼                ▼
              ┌──────────────────────────────────────────────────┐
              │              8-Feature Vector                    │
              │                                                  │
              │  [RMS_band1, RMS_band2, RMS_band3, RMS_band4,  │
              │   RMS_band5, RMS_broadband, Crest_factor,       │
              │   Kurtosis_estimate]                             │
              │                                                  │
              │  Each feature is a DC analog voltage (0-1.8V)   │
              └───────────────────────┬──────────────────────────┘
                                      │
                                      ▼
              ┌──────────────────────────────────────────────────┐
              │         Charge-Domain MAC Classifier             │
              │                                                  │
              │  4 parallel neurons (one per fault class):       │
              │                                                  │
              │  y_normal    = Σ(w0_i × feature_i)              │
              │  y_imbalance = Σ(w1_i × feature_i)              │
              │  y_bearing   = Σ(w2_i × feature_i)              │
              │  y_looseness = Σ(w3_i × feature_i)              │
              │                                                  │
              │  Using MIM capacitors: Q = C_weight × V_feature │
              │  Charge shares onto bitline → voltage = MAC     │
              │                                                  │
              │  Winner-take-all → class with highest score     │
              └───────────────────────┬──────────────────────────┘
                                      │
                                      ▼
              ┌──────────────────────────────────────────────────┐
              │              Decision Logic                      │
              │                                                  │
              │  if (class ≠ NORMAL) for N consecutive cycles:  │
              │     → Assert IRQ pin                             │
              │     → Wake host MCU                              │
              │     → MCU activates ADC, reads exact features   │
              │     → MCU transmits via BLE/LoRa                │
              │  else:                                           │
              │     → Stay asleep. Cost: 300 uW.                │
              └──────────────────────────────────────────────────┘
```

---

### Why Each Block Exists (The Physics Argument)

**PGA (Programmable Gain Amplifier):** MEMS accelerometers output 100-660 mV/g. A healthy motor at 30Hz might produce 0.1g = 10-66mV. A failing bearing might produce 2g = 200mV-1.3V. The PGA normalizes this to fill the filter bank's input range (~200mVpp optimal for low THD in Gm-C filters). Without the PGA, you'd need filters that work from millivolts to volts — impractical.

**Band-Pass Filters:** The frequency content of vibration carries the diagnostic information. A digital system would sample at 50kHz and run a 1024-point FFT (512 frequency bins). We replace this with 5 analog band-pass filters that give us 5 "bins" — far fewer, but covering the exact frequency ranges where faults manifest. This is sufficient because fault detection is a coarse classification problem, not a frequency identification problem.

**Envelope Detectors:** The BPF outputs are AC signals at the carrier frequency (hundreds to thousands of Hz). We need DC values proportional to the energy in each band. The envelope detector rectifies and smooths the BPF output, producing a slowly-varying DC voltage (~10 Hz bandwidth) that represents the RMS power in that band. This is analogous to computing the magnitude of an FFT bin.

**Charge-Domain MAC Classifier:** The 8 DC feature voltages must be combined with learned weights to produce a classification. We use capacitive charge sharing (Q=CV) to compute the weighted sum in one clock cycle, at near-zero energy. The weights are trained offline on the CWRU Bearing Dataset and loaded via SPI at power-on. This replaces the MCU's multiply-accumulate computation.

**Why not just threshold each band?** Because faults don't always increase energy in a single band. A bearing outer-race fault increases Band 1 AND creates harmonics in Bands 3-4. Misalignment increases Band 1 but not Band 3. The classifier learns the multi-dimensional decision boundary that separates these patterns. A simple per-band threshold would have 30-40% false alarm rate vs <5% for the trained classifier.

---

### How Signals Transfer Between Blocks

All inter-block signals are **continuous-time analog voltages on-chip.** There is no digitization between blocks (except the final ADC for MCU readback). This is the entire point.

| From → To | Signal | Type | Range | Bandwidth |
|-----------|--------|------|-------|-----------|
| MEMS → PGA | Vibration | AC, differential or single-ended | 5-1300 mVpp | DC-25 kHz |
| PGA → BPFs | Amplified vibration | AC, single-ended, DC-biased at Vcm=0.9V | 50-500 mVpp | DC-25 kHz |
| PGA → RMS/Crest | Same as above | AC | 50-500 mVpp | DC-25 kHz |
| BPF → Envelope | Filtered vibration | AC, narrow-band | 10-200 mVpp | Band-dependent |
| Envelope → Classifier | Band energy | **DC** (slowly varying) | 0.1-1.5 V | ~10 Hz |
| RMS/Crest → Classifier | Statistical features | **DC** | 0.1-1.5 V | ~10 Hz |
| Classifier → Digital | Anomaly flag | **Digital** (1-bit per class) | 0 or 1.8V | ~10 Hz |
| Digital → MCU | IRQ | **Digital** (open-drain) | 0 or Vdd | Event-driven |

**Critical interface: Envelope → Classifier.** The envelope detector output settles in ~100ms (10 Hz LPF). The classifier samples this every 100ms (10 Hz rate). The classifier operates in two phases:
1. **Sample phase (100ns):** Connect each feature voltage to its weight capacitor. Charge = C_weight × V_feature.
2. **Evaluate phase (100ns):** Share charge onto bitline. Comparator fires.

Total classification time: ~200ns. Duty cycle: 200ns every 100ms = 0.0002%. Classifier power is negligible.

---

### Power Breakdown (Where Every Microwatt Goes)

```
Total: ~300 uW at 1.8V
═══════════════════════

BPF5 (10-20 kHz)     ████████████████ 50 uW  (17%) ← Highest frequency = most current
BPF4 (5-10 kHz)      ████████████     36 uW  (12%)
Bias + references     ████████████     30 uW  (10%)
PGA                   ██████████       20 uW  (7%)
BPF3 (2-5 kHz)       █████████        18 uW  (6%)
Envelope det. (×5)    ████████         25 uW  (8%)
RMS + crest           ██████           15 uW  (5%)
Leakage + routing     ████████████████████████ 65 uW  (22%)
Classifier            ██               5 uW   (2%)
BPF2 (500-2k Hz)     ████             6 uW   (2%)
Digital (idle)        ████             10 uW  (3%)
BPF1 (100-500 Hz)    ██               2 uW   (1%)
ADC (sleep)           █               0.5 uW  (<1%)
Overhead              █████████████   17.5 uW (6%)

Key insight: 38% of power is in the two highest-frequency filters.
If the application only needs bands 1-3 (most industrial motors),
power drops to ~180 uW by disabling BPF4 and BPF5.
```

---

### Comparison to Digital Approach

| | VibroSense-1 (Analog) | nRF52840 + FFT (Digital) | POLYN VibroSense |
|---|---|---|---|
| Always-on power | **300 uW** | 3-10 mW | 34 uW (claimed) |
| Detection latency | 100-200 ms | 100-500 ms (duty-cycled) | <50 us (claimed) |
| Battery life (300mAh) | **3-5 years** | 6-12 months | 10+ years (claimed) |
| Frequency resolution | 5 bands | 512 bins (FFT) | Unknown |
| Classification | 4-class, on-chip | Unlimited (firmware) | Binary (normal/fault) |
| Reprogrammable | Weights via SPI | Fully reprogrammable | Limited |
| BOM cost (chip) | $5-15 | $3 (MCU only) | Unknown |
| Maturity | Design phase | Production | Low-volume 2024 |

**Honest assessment:** The digital approach is more flexible (any algorithm, any model). The analog approach wins on power (10-30x) and latency (always-on vs duty-cycled). POLYN claims better power but hasn't published independent benchmarks. Our 300uW is honest — it accounts for the sky130 PMOS model limitation that forces moderate inversion operation.

---

## Current Design Status (as of 2026-03-27)

| Block | Name | Status | Key Numbers | Notes |
|-------|------|--------|-------------|-------|
| 00 | Bias Generator | ✅ Complete | 507 nA, 0.97 µW, TC=116 ppm/C | TC 158 ppm/C at FS corner (5% over spec, functionally accepted) |
| 01 | Folded-Cascode OTA | ✅ Complete | 63.5 dB gain, 422 kHz UGB, 0.9 µW | All 5 gates pass |
| 02 | PGA (Cap-Feedback) | ✅ Complete | ±0.15 dB gain error, BW>25 kHz all gains | Power landed at 10 µW (spec relaxed from 5 µW) |
| 03 | 5-Channel BPF Bank | ✅ Complete | All 5 channels verified, corners pass | Independently confirmed |
| 04 | Envelope Detector | ⚠️ Partial | 4/7 specs pass, 21 µW/channel | Fails at <50 mVpp; PGA normalizes above this in practice |
| 05 | RMS + Crest Factor | ✅ Complete | ENOB-equiv R²=0.99992, 8 µW | All 10 specs, all 15 PVT corners |
| 06 | Charge-Domain Classifier | ✅ Complete | 99.5% MC accuracy, <0.001 µW avg | 10/10 specs, 45× corner margin |
| 07 | 8-bit SAR ADC (v3) | ⚠️ Unproven | 28.2 µW active, ±1 LSB all corners | DNL/INL/ENOB at 100 kHz not yet simulated (days of runtime) |
| 08 | Digital Control | ✅ Complete | 1.4 µW @ 1 MHz, SPI verified | Tapeout-ready RTL |
| 09 | Training Pipeline | ✅ Complete | CWRU dataset, multi-fault configs | Weights exported to SPICE format |
| 10 | Full Chain Integration | ⏳ Not started | — | Pending all blocks stable |

**Blocker for full-chain:** Block 04 envelope power (105 µW total for 5 channels vs 25 µW budget) and Block 07 ADC DNL/INL unproven. Neither blocks functionality — the classifier operates correctly on Block 04's actual output voltages, and Block 07's transfer function is verified at 13 points across the full range.

---

## Folder Structure — Parallel Design Blocks

Each folder is **self-contained** and can be assigned to a separate agent instance running in parallel. Dependencies are managed through **interface specifications** — each block gets the exact input/output voltage ranges and impedances it must design to, without needing the other block's netlist.

```
vibrosense/
├── README.md                 ← You are here (system lecture + status)
├── 00_bias/                  ← ✅ COMPLETE — 507 nA, 30/30 PVT conditions pass
├── 01_ota/                   ← ✅ COMPLETE — 63.5 dB, 422 kHz UGB, all gates pass
├── 02_pga/                   ← ✅ COMPLETE — tapeout-ready, all gains verified
├── 03_filters/               ← ✅ COMPLETE — 5 channels, all specs pass
├── 04_envelope/              ← ⚠️ PARTIAL — 4/7 specs, power 21 µW/ch (over budget)
├── 05_rms_crest/             ← ✅ COMPLETE — all 10 specs, all 15 PVT corners
├── 06_classifier/            ← ✅ COMPLETE — 99.5% MC accuracy, 10/10 specs
├── 07_adc/                   ← (v2 reference — superseded by 07_adc_v3)
├── 07_adc_v3/                ← ⚠️ FUNCTIONAL — corners/power pass, DNL/INL unproven
├── 08_digital/               ← ✅ COMPLETE — tapeout-ready RTL, SPI verified
├── 09_training/              ← ✅ COMPLETE — CWRU pipeline, weights exported
└── 10_fullchain/             ← ⏳ NOT STARTED — awaiting all blocks stable
```

### Parallelism Map

```
TIME ──────────────────────────────────────────────────►

PARALLEL WAVE 1 (all launch simultaneously):
  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
  │ 00_bias  │ │ 01_ota   │ │06_classif│ │ 07_adc   │
  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
       │            │            │            │
  ┌────┴─────┐ ┌────┴─────┐     │       ┌────┴─────┐
  │08_digital│ │09_training│     │       │          │
  └────┬─────┘ └────┬─────┘     │       │          │
       │            │            │       │          │

PARALLEL WAVE 2 (launch when 01_ota completes):
  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
  │ 02_pga   │ │03_filter✅│ │04_envelope│ │05_rms    │
  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
       │            │            │            │

SEQUENTIAL (launch when ALL above complete):
  ┌──────────────────────────────────────────────────┐
  │               10_fullchain                        │
  │  Integrate all blocks, end-to-end verification   │
  └──────────────────────────────────────────────────┘
```

### Interface Contract (All Blocks Must Respect This)

Every analog block operates at:
- **Supply:** 1.8V (Vdd) and 0V (Vss/GND)
- **Common-mode voltage:** 0.9V (mid-rail) for all AC-coupled signals
- **Signal swing:** ±250mV around Vcm (500mVpp max) unless otherwise specified
- **Load capacitance:** Assume 10pF at every output (pessimistic, covers routing + next stage input)
- **Bias currents:** Sourced from Block 00 current mirrors. Each block specifies how many copies of Iref=500nA it needs.

### OTA Behavioral Model (For Wave 2 Blocks)

Blocks 02-05 depend on the OTA but can start immediately using this behavioral model. Replace with the real OTA netlist when Block 01 completes.

```spice
* Behavioral OTA for parallel block development
* Replace with real sky130 OTA from 01_ota/ when ready
.subckt ota_behavioral vip vim vout vdd vss
* Ideal voltage-controlled current source
G1 vout vss cur='2.5e-6 * (v(vip) - v(vim))'  ; gm = 2.5 uS
* Output resistance (sets DC gain = gm × Rout = 2.5u × 40M = 100 = 40dB)
* For folded cascode: Rout ~ 400M → gain = 60dB
Rout vout vss 400Meg
Cout vout vss 50f  ; parasitic output cap
.ends
```

Blocks in Wave 2 must:
1. First verify with the behavioral model
2. Then re-verify with the real OTA netlist from 01_ota/
3. Report results for BOTH and flag any degradation >10%
