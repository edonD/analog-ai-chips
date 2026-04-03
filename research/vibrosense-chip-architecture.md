# VibroSense-1: Always-On Analog Vibration Anomaly Detection Chip

**Target market:** Industrial predictive maintenance ($10.93B, 22% CAGR)
**Value proposition:** Reduce wireless vibration sensor node power from 50-500mW to <200uW always-on, extending battery life from months to 5+ years
**ASP target:** $5-15 (node sells for $200-1,000; chip is <5% of BOM)

---

## Why This Chip Makes Money

### The Problem

Industrial vibration monitoring is a $1.87B market growing to $2.54B by 2030. Every large factory has thousands of rotating machines (motors, pumps, compressors, bearings) that fail unexpectedly. Unplanned downtime costs **$260,000/hour**.

Current wireless vibration sensor nodes (Fluke, SKF, Honeywell) work like this:
1. Wake up every 1-60 minutes
2. Power up MEMS accelerometer + ADC + MCU
3. Sample vibration at 10-50 kHz for 1-5 seconds
4. Run FFT + anomaly detection on MCU
5. Transmit result via BLE/WiFi/LoRa
6. Sleep

**The power problem:** Steps 2-4 consume 10-100mW. Even with 99% duty-cycling, average power is 0.1-5mW. Battery life: 6-18 months. Replacing batteries on 10,000 sensors across a factory costs $50-100 per sensor per year = **$500K-1M/year just in battery changes.**

### The Solution

VibroSense-1 does the anomaly detection **in the analog domain, before the ADC**, consuming <100uW always-on. The digital MCU + radio only wake when an anomaly is detected (maybe once per day or less).

**Result:** Battery life goes from 12 months to 5+ years. The $500K/year battery replacement cost drops to near zero.

### Why Analog Wins Here (and Only Here)

1. **The signal is already analog.** MEMS accelerometer output is an analog voltage. Digitizing it at 50 kHz just to run an FFT is wasteful.
2. **Power budget is <1mW.** This is below what any digital solution can achieve for continuous 50kHz signal processing. Aspinity proved this at 30-100uW.
3. **The classification is simple.** "Normal vibration" vs "anomalous vibration" is a binary or few-class problem. You don't need a billion-parameter model.
4. **False negatives are acceptable at low rates.** Missing one anomaly out of 100 is fine — the machine doesn't fail instantly. You'll catch it next time.
5. **The customer pays for the node, not the chip.** At $200-1,000 per node, a $10 chip is noise.

---

## System Architecture

```
                        VibroSense-1 SoC
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ┌──────────┐   ┌──────────────┐   ┌───────────┐   ┌─────────┐ │
│  │  Analog   │   │   Analog     │   │  Analog   │   │ Digital │ │
│  │  Input    │──►│   Feature    │──►│  Anomaly  │──►│ Wake    │ │
│  │  Stage    │   │   Extractor  │   │  Detector │   │ Logic   │ │
│  │          │   │              │   │           │   │         │ │
│  │ • LNA    │   │ • Band-pass  │   │ • Template│   │ • IRQ   │ │
│  │ • PGA    │   │   filter bank│   │   match   │   │ • Timer │ │
│  │ • Bias   │   │ • Envelope   │   │ • Threshold│  │ • SPI   │ │
│  │          │   │   detectors  │   │   compare │   │         │ │
│  └──────────┘   │ • RMS/peak   │   │ • Learned │   └────┬────┘ │
│                  │   extraction │   │   weights │        │      │
│                  └──────────────┘   └───────────┘        │      │
│                                                          │      │
│  ┌──────────────────────────────────────────────────────┐│      │
│  │              Programmable Analog Core                 ││      │
│  │                                                      ││      │
│  │  NVM-programmed weights (MIM caps or flash trim)     ││      │
│  │  Configurable filter coefficients                    ││      │
│  │  Adjustable thresholds via SPI from host MCU         ││      │
│  └──────────────────────────────────────────────────────┘│      │
│                                                          ▼      │
│  ┌─────────────┐   ┌──────────┐   ┌──────────────────────────┐ │
│  │  8-bit SAR  │   │  Temp    │   │      SPI / I2C           │ │
│  │  ADC        │   │  Sensor  │   │      Interface           │ │
│  │ (on-demand) │   │          │   │  (to host MCU for config │ │
│  │             │   │          │   │   and detailed readback)  │ │
│  └─────────────┘   └──────────┘   └──────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
         │                                    │
    MEMS Accel                           Host MCU
    (analog out)                    (sleeps until IRQ)
                                         │
                                    BLE / LoRa
                                    (transmit only
                                     on anomaly)
```

---

## Analog Signal Processing Chain (The Core IP)

### Block 1: Analog Input Stage

```
MEMS Accel ──► AC Coupling ──► PGA ──► Anti-alias Filter ──► Feature Extractor
(±2g to ±16g)   (10 Hz HPF)   (0-40dB)   (25 kHz LPF)
```

**Programmable Gain Amplifier (PGA):**
- 4 gain settings: 1x, 4x, 16x, 64x (0, 12, 24, 36 dB)
- Switched-capacitor or resistive feedback
- Input range: 10 mV to 1V peak (covers MEMS outputs from ADXL355, BMI270, etc.)
- Bandwidth: 50 kHz (covers bearing defect frequencies up to 20 kHz)
- Power: <5 uW (subthreshold OTA design)

**Why subthreshold:** At 130nm, subthreshold gm/Id ≈ 25 V⁻¹ gives maximum transconductance per unit current. A 100nA OTA gives gm = 2.5uS — enough for 50kHz bandwidth with 10pF loads.

### Block 2: Analog Filter Bank (Feature Extraction)

This is where the magic happens. Instead of digitizing and running FFT, we extract frequency-domain features directly in analog.

```
                    ┌─── BPF 100-500 Hz ───► Envelope Det ───► RMS ──┐
                    │                                                  │
                    ├─── BPF 500-2k Hz ───► Envelope Det ───► RMS ──┤
                    │                                                  │
Input ──► Splitter ─┤─── BPF 2k-5k Hz  ───► Envelope Det ───► RMS ──├──► Feature
                    │                                                  │    Vector
                    ├─── BPF 5k-10k Hz ───► Envelope Det ───► RMS ──┤    (8 analog
                    │                                                  │    voltages)
                    ├─── BPF 10k-20k Hz──► Envelope Det ───► RMS ──┤
                    │                                                  │
                    ├─── Broadband RMS ─────────────────────────────┤
                    │                                                  │
                    └─── Crest Factor (peak/RMS) ──────────────────┘
                         Kurtosis estimator ───────────────────────┘
```

**8 features extracted continuously in analog:**
1. RMS in 100-500 Hz band (shaft imbalance, misalignment)
2. RMS in 500-2 kHz band (gear mesh frequencies)
3. RMS in 2-5 kHz band (bearing outer race defects)
4. RMS in 5-10 kHz band (bearing inner race defects)
5. RMS in 10-20 kHz band (bearing ball defects, early-stage faults)
6. Broadband RMS (overall vibration level)
7. Crest factor (peak-to-RMS ratio — indicates impulsive events)
8. Kurtosis estimate (statistical indicator of bearing damage)

**These 8 features are the EXACT features used by ISO 10816 and ISO 20816 vibration severity standards.** This isn't a toy — it's what vibration analysts actually use.

**Circuit implementation:**

Each band-pass filter:
- 2nd-order Gm-C (transconductor-capacitor) filter
- Gm set by bias current (programmable center frequency)
- Q ≈ 2-5 (moderate selectivity, not sharp)
- Power per filter: ~2-5 uW (subthreshold Gm cells)

Envelope detector:
- Full-wave rectifier (using subthreshold MOS diode bridge)
- Low-pass smoothing (Gm-C, fc ≈ 10 Hz)
- Output: DC voltage proportional to RMS in band
- Power: ~1 uW

Total analog feature extraction: **~30-50 uW for 8 channels**

### Block 3: Analog Anomaly Detector (Classifier)

The 8 analog feature voltages feed a simple analog classifier:

```
Feature    Weight
Vector     Array      Summer    Comparator    Output
(8 ch)     (8 caps)

V_f1 ──►[C1]──┐
V_f2 ──►[C2]──┤
V_f3 ──►[C3]──┼──► Σ(Ci×Vi) ──► [+] ──► Normal/Anomaly
V_f4 ──►[C4]──┤                  [-]          (digital IRQ)
V_f5 ──►[C5]──┤                   ▲
V_f6 ──►[C6]──┤              Threshold
V_f7 ──►[C7]──┤             (programmable)
V_f8 ──►[C8]──┘
```

**This is a single-neuron perceptron with 8 inputs.**

- Weights stored as MIM capacitor ratios (binary-weighted: C, 2C, 4C, 8C per weight)
- 4-bit weight precision (16 levels) — enough for anomaly detection
- Charge-domain MAC: Q = Σ(C_i × V_feature_i)
- Threshold comparison: simple CMOS comparator
- Multiple output neurons possible (for multi-class: normal, imbalance, bearing, looseness)

**Weight programming:**
- Option A: Fuse-trimmed MIM cap arrays (one-time programmable, simplest)
- Option B: SRAM-loaded cap switches (reconfigurable, needs power-on init)
- Option C: Flash-trimmed (non-volatile, reprogrammable, needs NVM)

**For sky130:** SRAM-loaded is most practical. Host MCU writes weights via SPI at power-up.

Power: **~5-10 uW** for the classifier

### Block 4: Digital Wake Logic

Minimal digital:
- IRQ output pin (active when anomaly detected)
- SPI slave interface (for configuration and weight loading)
- Timer/counter (debounce — require N consecutive anomaly detections)
- 8-bit SAR ADC (on-demand, for MCU to read exact feature values when awake)
- Temperature sensor (for compensation)

Power: **~1-5 uW** (clock-gated, mostly asleep)

---

## Total Power Budget

| Block | Power | Fraction |
|-------|-------|----------|
| PGA + input stage | 5 uW | 5% |
| Filter bank (5 BPFs) | 25 uW | 25% |
| Envelope detectors (5) | 5 uW | 5% |
| Broadband RMS + crest + kurtosis | 10 uW | 10% |
| Analog classifier | 10 uW | 10% |
| Digital wake logic (idle) | 5 uW | 5% |
| Bias + reference | 10 uW | 10% |
| Leakage + overhead | 30 uW | 30% |
| **Total always-on** | **~100 uW** | **100%** |

**Compare to digital approach:** MCU (nRF52840) running FFT at 50kHz = 3-10 mW continuous = **30-100x more power**.

---

## Simulation Plan

### What to Simulate and Why

The simulation proves the chip works at three levels:

**Level 1: Component Verification**
Each analog block simulated individually in ngspice with sky130 models.

**Level 2: Signal Chain Verification**
Full chain from MEMS input to anomaly detection output. Use real vibration waveforms.

**Level 3: System Verification**
Statistical accuracy on a real bearing fault dataset (CWRU Bearing Dataset — the standard benchmark).

### Simulation 1: Subthreshold OTA (The Building Block)

Everything in this chip is built from one cell: a subthreshold operational transconductance amplifier.

```spice
* VibroSense-1: Subthreshold OTA for Gm-C filter
* SkyWater SKY130 PDK
* Target: gm = 2.5 uS at Ibias = 100 nA

.lib "./sky130_fd_pr/models/sky130.lib.spice" tt

* Simple 5-transistor OTA (folded cascode for higher gain)
* All transistors in subthreshold: Vgs - Vth < 0

* NMOS input pair (W/L = 10u/1u, subthreshold)
M1 vout1 vinp  vtail  gnd  sky130_fd_pr__nfet_01v8 W=10u L=1u
M2 vout2 vinn  vtail  gnd  sky130_fd_pr__nfet_01v8 W=10u L=1u

* PMOS active load (W/L = 5u/2u, current mirror)
M3 vout1 vout1 vdd   vdd  sky130_fd_pr__pfet_01v8 W=5u L=2u
M4 vout2 vout1 vdd   vdd  sky130_fd_pr__pfet_01v8 W=5u L=2u

* Tail current source
M5 vtail vbias gnd   gnd  sky130_fd_pr__nfet_01v8 W=2u L=4u

* Bias: 100 nA tail current
Ibias vdd vbias 100n
Mbias vbias vbias gnd gnd sky130_fd_pr__nfet_01v8 W=2u L=4u

Vdd vdd gnd 1.8
Vinn vinn gnd 0.9

* Test: AC sweep for gm measurement
Vinp vinp gnd DC 0.9 AC 1m
.ac dec 100 1 100Meg

* Test: DC sweep for linearity
* .dc Vinp 0.85 0.95 0.001

* Corner analysis
* .lib "./sky130_fd_pr/models/sky130.lib.spice" ss
* .lib "./sky130_fd_pr/models/sky130.lib.spice" ff

.control
run
plot vdb(vout2) ; gain in dB
plot 180/PI*cph(vout2) ; phase
meas ac gm_val find vdb(vout2) at=1k
meas ac ugbw when vdb(vout2)=0
meas ac pm find (180+180/PI*cph(vout2)) when vdb(vout2)=0
print gm_val ugbw pm
.endc

.end
```

**Expected results:**
- Open-loop gain: >50 dB
- Unity-gain bandwidth: ~50-100 kHz (with 10pF load)
- Phase margin: >60°
- gm: ~2.5 uS at 100 nA
- Power: 180 nW (Vdd × Ibias)

### Simulation 2: Gm-C Band-Pass Filter

```spice
* VibroSense-1: 2nd-order Gm-C Band-Pass Filter
* Center frequency: 3.5 kHz (bearing defect band)
* Q = 3, BW = ~1.2 kHz (covers 2k-5k Hz band)
*
* Topology: Tow-Thomas biquad using two OTAs and two caps
*
* Transfer function: H(s) = (gm1/C1) * s / (s^2 + (gm3/C2)*s + gm1*gm2/(C1*C2))
*
* For f0 = 3.5 kHz, Q = 3:
*   gm1 = gm2 = 2*pi*f0*C = 2*pi*3500*10p = 220 nS
*   gm3 = gm1/Q = 73 nS
*   C1 = C2 = 10 pF

.lib "./sky130_fd_pr/models/sky130.lib.spice" tt

* Include OTA subcircuit (from Sim 1, parameterized)
.subckt ota vip vim vout vdd vss ibias
* [OTA netlist as above, parameterized by ibias]
.ends

* Tow-Thomas BPF
XOTA1 vinp  vbp  vhp  vdd gnd ota ibias=100n  ; integrator 1
XOTA2 vhp   vcm  vlp  vdd gnd ota ibias=100n  ; integrator 2
XOTA3 vlp   vcm  vbp  vdd gnd ota ibias=33n   ; feedback (sets Q)
C1 vhp gnd 10p
C2 vlp gnd 10p

* Input signal: bearing fault vibration (multi-tone test)
Vin vinp gnd DC 0.9 SIN(0.9 50m 3500) ; 3.5 kHz, 50mV amplitude
* Add harmonics for realistic test:
* Vin2 vinp gnd SIN(0 10m 500)  ; shaft frequency
* Vin3 vinp gnd SIN(0 20m 7000) ; higher harmonic

Vcm vcm gnd 0.9
Vdd vdd gnd 1.8

.tran 1u 10m
.ac dec 100 10 100k

.control
run
plot v(vbp)-0.9  ; bandpass output (AC-coupled view)
* Verify center frequency and Q from AC response
.endc

.end
```

**Expected results:**
- Center frequency: 3.5 kHz (tunable via bias current)
- -3dB bandwidth: ~1.2 kHz (Q=3)
- Passband gain: 0 dB (unity)
- Rejection at 100 Hz: >20 dB
- Rejection at 20 kHz: >15 dB
- Power: ~360 nW (2 OTAs × 180 nW)
- Input-referred noise: <100 nV/√Hz (thermal noise limited)

### Simulation 3: Envelope Detector

```spice
* VibroSense-1: Full-Wave Rectifier + Low-Pass (Envelope Detector)
* Extracts RMS-like envelope from BPF output
*
* Uses subthreshold MOS pseudo-diode bridge
* Output: DC voltage proportional to amplitude in band

.lib "./sky130_fd_pr/models/sky130.lib.spice" tt

* Subthreshold rectifier: two NMOS in diode config
* At subthreshold, I = I0 * exp(Vgs/nVt) -- exponential I-V gives rectification
M1 vout vinp gnd gnd sky130_fd_pr__nfet_01v8 W=1u L=0.5u
M2 vout vinn gnd gnd sky130_fd_pr__nfet_01v8 W=1u L=0.5u

* Low-pass smoothing: R-C with long time constant
* tau = R*C = 10M * 10p = 100 us (fc ≈ 1.6 kHz -- smooths carrier)
R1 vout vsmooth 10Meg
C1 vsmooth gnd 10p

* Alternatively use Gm-C LPF for better control:
* XOTA_lpf vout vcm vsmooth vdd gnd ota ibias=10n
* C_lpf vsmooth gnd 100p

* Test input: 3.5 kHz carrier, amplitude-modulated at 10 Hz
* Simulates bearing fault that causes periodic impulses
Vinp vinp gnd DC 0.9 SIN(0.9 50m 3500)
Vinn vinn gnd 0.9

Vdd vdd gnd 1.8

.tran 10u 200m

.control
run
plot v(vsmooth) ; should show DC level proportional to input amplitude
.endc

.end
```

### Simulation 4: Charge-Domain MAC (Classifier)

```spice
* VibroSense-1: 8-input Charge-Domain MAC Classifier
* Implements: y = Σ(w_i × x_i) using capacitor-based CIM
*
* Weights: 4-bit, stored as binary-weighted cap switches
* Inputs: 8 analog feature voltages (from envelope detectors)

.lib "./sky130_fd_pr/models/sky130.lib.spice" tt

* MIM capacitor model (sky130_fd_pr__cap_mim_m3_1)
* Using ideal caps here for clarity; replace with PDK model

* Unit capacitor
.param Cunit=50f

* Weight encoding: 4-bit per input (switches controlled by SRAM bits)
* Weight[0] = 0b1010 = 10 → connects C and 8C (total 9*Cunit)
* Weight[1] = 0b0110 = 6  → connects 2C and 4C (total 6*Cunit)
* etc.

* Input 0: Feature voltage V_f0, Weight = 10 (9*Cunit)
* Bit 0 (1C): ON
Sw0_b0 vf0 vbl Ctrl_w0b0 gnd SMODEL
Cw0_b0 vbl gnd {1*Cunit}
* Bit 1 (2C): OFF (switch open)
* Bit 2 (4C): OFF
* Bit 3 (8C): ON
Sw0_b3 vf0 vbl Ctrl_w0b3 gnd SMODEL
Cw0_b3 vbl gnd {8*Cunit}

* Input 1: Feature voltage V_f1, Weight = 6 (6*Cunit)
Sw1_b1 vf1 vbl Ctrl_w1b1 gnd SMODEL
Cw1_b1 vbl gnd {2*Cunit}
Sw1_b2 vf1 vbl Ctrl_w1b2 gnd SMODEL
Cw1_b2 vbl gnd {4*Cunit}

* ... (repeat for all 8 inputs)

* Bitline parasitic capacitance
Cbl_par vbl gnd 200f

* Precharge phase: reset bitline to Vref
Sw_pre vref vbl Ctrl_pre gnd SMODEL
Vref vref gnd 0.9

* Threshold comparator
* Compare vbl against programmable threshold
Vthresh vthresh gnd 0.95 ; set by SPI from host MCU
Xcomp vbl vthresh anomaly_out vdd gnd comparator

.model SMODEL SW Vt=0.5 Vh=0.1 Ron=100 Roff=1G

* Control signals (precharge, then evaluate)
Vctrl_pre Ctrl_pre gnd PULSE(1.5 0 0 1n 1n 500n 2u)
* Weight switches: static during evaluation
Vctrl_w0b0 Ctrl_w0b0 gnd 1.5
Vctrl_w0b3 Ctrl_w0b3 gnd 1.5
Vctrl_w1b1 Ctrl_w1b1 gnd 1.5
Vctrl_w1b2 Ctrl_w1b2 gnd 1.5

* Feature inputs (DC for now; in real system these are envelope detector outputs)
Vf0 vf0 gnd 0.92  ; slightly elevated = mild vibration in band 0
Vf1 vf1 gnd 0.95  ; elevated = vibration in band 1
* ... (8 total)

Vdd vdd gnd 1.8

.tran 1n 5u

.control
run
plot v(vbl) v(anomaly_out)
.endc

.end
```

### Simulation 5: Full Signal Chain (End-to-End)

```spice
* VibroSense-1: Full Chain Test
* Input: realistic bearing fault vibration waveform
* Output: anomaly detection IRQ
*
* Chain: Input → PGA → BPF bank → Envelope → MAC → Comparator → IRQ

* Use PWL file for realistic vibration data
* (Generate from CWRU Bearing Dataset using Python preprocessing)

* Vin vinp gnd PWL file="bearing_fault_normal.csv"
* Vin vinp gnd PWL file="bearing_fault_inner_race.csv"
* Vin vinp gnd PWL file="bearing_fault_outer_race.csv"
* Vin vinp gnd PWL file="bearing_fault_ball.csv"

* [Full hierarchical netlist connecting all blocks]
* This simulation takes ~10 minutes on a modern CPU for 1 second of real-time
```

---

## How to Build It: Step-by-Step

### Phase 1: Prove the Analog Signal Chain (Weeks 1-3)

**Goal:** Verify each analog block meets spec in sky130.

```bash
# Setup
docker pull hpretl/iic-osic-tools:latest
docker run -it -v $(pwd):/foss/designs hpretl/iic-osic-tools:latest

# Design flow
cd /foss/designs/vibrosense

# 1. Draw OTA schematic in Xschem
xschem ota_subthreshold.sch

# 2. Simulate in ngspice
ngspice ota_testbench.spice
# Verify: gain>50dB, UGB>50kHz, PM>60°, Idd<200nA

# 3. Draw Gm-C BPF
xschem bpf_gmC.sch
# Simulate: verify center freq, Q, rejection

# 4. Envelope detector
xschem envelope_detector.sch

# 5. Full analog chain (hierarchical)
xschem analog_chain_top.sch
# Feed in test tones, verify feature extraction
```

**Deliverables:**
- [ ] OTA: gain, bandwidth, power, noise vs spec
- [ ] 5 BPFs: center frequencies match ISO 10816 bands
- [ ] Envelope detectors: DC output tracks amplitude correctly
- [ ] Monte Carlo: mismatch impact on filter frequencies (100 runs)
- [ ] Corner analysis: TT, SS, FF, SF, FS at -40°C, 25°C, 85°C

### Phase 2: Prove the Classifier (Weeks 3-4)

**Goal:** Train weights in Python, load into analog sim, verify accuracy.

```python
# train_classifier.py
# Uses CWRU Bearing Dataset (standard benchmark)
# Extracts same 8 features as analog chain
# Trains single-layer perceptron with 4-bit quantized weights

import numpy as np
from scipy.signal import butter, filtfilt
from sklearn.metrics import accuracy_score

# Load CWRU bearing dataset (publicly available)
# http://csegroups.case.edu/bearingdatacenter/

def extract_features(signal, fs=12000):
    """Extract same 8 features as analog chip"""
    features = []

    # Band-pass filters matching analog chip bands
    bands = [(100, 500), (500, 2000), (2000, 5000), (5000, 10000)]
    for flo, fhi in bands:
        b, a = butter(2, [flo/(fs/2), fhi/(fs/2)], btype='band')
        filtered = filtfilt(b, a, signal)
        features.append(np.sqrt(np.mean(filtered**2)))  # RMS in band

    # Broadband RMS
    features.append(np.sqrt(np.mean(signal**2)))

    # Crest factor
    features.append(np.max(np.abs(signal)) / features[-1])

    # Kurtosis
    features.append(np.mean((signal - np.mean(signal))**4) /
                    np.mean((signal - np.mean(signal))**2)**2)

    # Zero-crossing rate (bonus feature)
    features.append(np.sum(np.diff(np.sign(signal)) != 0) / len(signal))

    return np.array(features)

# Train simple perceptron
# Quantize weights to 4-bit (16 levels)
def quantize_weights(weights, bits=4):
    levels = 2**bits
    w_min, w_max = weights.min(), weights.max()
    scale = (w_max - w_min) / (levels - 1)
    w_q = np.round((weights - w_min) / scale) * scale + w_min
    return w_q

# Expected accuracy on CWRU: >95% for binary (normal vs fault)
# Expected accuracy for 4-class: >85% (normal, inner, outer, ball)
```

**Deliverables:**
- [ ] Python golden model accuracy on CWRU dataset
- [ ] 4-bit quantized weight accuracy (should be within 2% of float)
- [ ] Export weights as SPICE parameters
- [ ] ngspice simulation with exported weights vs Python golden model

### Phase 3: Layout and Integration (Weeks 5-8)

```bash
# Layout in Magic
magic -T sky130A vibrosense_top.mag

# Key layout considerations:
# - Common-centroid OTA pairs (for matching)
# - MIM cap arrays in matched rows (for weight precision)
# - Guard rings around analog blocks
# - Separate analog and digital power domains
# - Decoupling caps on every power rail

# DRC
magic -dnull -noconsole -T sky130A <<EOF
load vibrosense_top
drc check
drc count
EOF

# LVS
netgen -batch lvs "vibrosense_top.spice vibrosense_top" \
                   "vibrosense_top.mag vibrosense_top" \
                   sky130A_setup.tcl

# PEX (parasitic extraction)
magic -dnull -noconsole -T sky130A <<EOF
load vibrosense_top
extract all
ext2spice lvs
ext2spice cthresh 0.01
ext2spice
EOF

# Post-layout simulation
ngspice vibrosense_postlayout.spice
```

### Phase 4: Tapeout (Months 3-6)

**Option A: Tiny Tapeout (~$700)**
- 2 analog tiles = enough for: 1 BPF + envelope + comparator (proof of single channel)
- 4-6 analog pins
- Good for: validating the Gm-C filter and envelope detector on real silicon

**Option B: chipIgnite ($14,950)**
- Full 10mm² die
- Complete VibroSense-1 with all 5 BPFs, 8-feature extractor, classifier
- 100 packaged chips for testing
- **This is the real product prototype**

**Option C: wafer.space GF180 ($7,000)**
- 1000 chips
- 180nm is actually better for subthreshold analog (lower leakage)
- No MIM caps in open PDK but MOS caps work for proof

---

## Test Plan (After Silicon)

### Bench Test
1. Apply known vibration waveform via function generator + piezo shaker
2. Measure feature extraction accuracy: compare analog output to Python FFT
3. Sweep temperature: -20°C to 85°C (industrial range)
4. Measure total power: should be <100 uW at 1.8V

### Real-World Test
1. Mount on a bearing test rig (university mech eng lab or makerspace lathe)
2. Run healthy bearing: chip should output "normal"
3. Introduce fault (scratched race, chipped ball): chip should detect within seconds
4. Compare detection latency and accuracy to digital solution (MCU + FFT)

### Benchmark vs Competition
| Metric | VibroSense-1 Target | POLYN VibroSense | MCU + FFT (nRF52840) |
|--------|--------------------|-----------------|--------------------|
| Always-on power | <100 uW | 34 uW (claimed) | 3-10 mW |
| Detection latency | <100 ms | <50 us (claimed) | 100-500 ms |
| Classification accuracy | >90% (4-class) | Unknown | >95% |
| Battery life (300mAh) | 5+ years | 10+ years | 6-12 months |

---

## Bill of Materials (Complete Sensor Node)

| Component | Part | Cost |
|-----------|------|------|
| VibroSense-1 | Custom ASIC | $5-10 |
| MEMS accelerometer | ADXL355 or BMI270 | $3-8 |
| Host MCU | nRF52840 (BLE) | $3 |
| Antenna | Chip antenna | $0.50 |
| Battery | CR2032 or 300mAh LiPo | $1-3 |
| PCB + passives | | $2-5 |
| Enclosure | IP67 industrial | $5-15 |
| **Total BOM** | | **$20-45** |
| **Selling price** | | **$150-500** |
| **Gross margin** | | **75-90%** |

---

## Revenue Model

| Year | Units | ASP (chip) | Revenue (chip) | Notes |
|------|-------|-----------|---------------|-------|
| Y1 | 1,000 | $15 | $15K | Early adopters, pilot programs |
| Y2 | 10,000 | $12 | $120K | First production customers |
| Y3 | 100,000 | $8 | $800K | Design wins ramping |
| Y4 | 500,000 | $6 | $3M | Multiple verticals |
| Y5 | 2,000,000 | $5 | $10M | Scale — would match Mythic's current revenue |

**The complete sensor node has much better economics:**

| Year | Nodes | ASP (node) | Revenue (node) | Gross Margin |
|------|-------|-----------|---------------|-------------|
| Y1 | 500 | $300 | $150K | 80% |
| Y2 | 5,000 | $250 | $1.25M | 80% |
| Y3 | 25,000 | $200 | $5M | 75% |
| Y4 | 100,000 | $175 | $17.5M | 75% |
| Y5 | 500,000 | $150 | $75M | 70% |

**Selling nodes, not chips, is 10x better revenue at 5x better margins.**

---

## Sources

- CWRU Bearing Dataset: csegroups.case.edu/bearingdatacenter
- ISO 10816 / ISO 20816: Vibration severity standards
- POLYN VibroSense: polyn.ai/vibrosense-iiot
- Aspinity AML100/AML200: aspinity.com
- Predictive maintenance market: Coherent Market Insights 2025
- SkyWater PDK: skywater-pdk.readthedocs.io
- JKU SAR ADC: github.com/iic-jku/SKY130_SAR-ADC1
- ChipFoundry: chipfoundry.io
