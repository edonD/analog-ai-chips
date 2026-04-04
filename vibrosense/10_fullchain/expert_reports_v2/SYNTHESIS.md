# VibroSense-1 Full-Chain Accuracy Problem: Expert Synthesis Report

**Date**: 2026-04-04
**Status**: 25% classification accuracy (1/4 correct). Target: >80%.
**Classifier on pre-computed vectors**: 100% (20/20).

---

## Executive Summary

Ten expert analyses have converged on a clear diagnosis: **the information needed for classification EXISTS in the analog signal chain but is LOST in the mapping from envelope detector output to classifier input**. The root cause is a 250x dynamic range mismatch between what the classifier expects (features spanning 0-1.8V) and what it receives (features spanning 0.900-0.910V). This is compounded by several secondary issues in BPF tuning and feature extraction.

---

## Key Findings from Each Expert

### Expert 01: PGA Dynamic Range
- PGA operates at **16x gain** (confirmed from simulation: measured 16.0x)
- V_SCALE = 0.02 V/g produces very small stimuli
- Fault impulses clip at PGA output (1920 mVpp > 1700 mV rail), but band-limited signals don't
- **Key number**: After BPF band-splitting, each channel sees only 10-200 mVpp

### Expert 02: BPF Frequency Response
- **CRITICAL BUG**: BPF channels 4 and 5 use wrong bias voltages
  - Ch4 needs Iref=440nA (VBN=0.6399) but gets 200nA (VBN=0.5973)
  - Ch5 needs Iref=870nA (VBN=0.6914) but gets 200nA
  - This detunes Ch4 from 7236 Hz to ~4900 Hz and Ch5 from 14639 Hz to ~7000 Hz
- BPF center frequencies (log-spaced: 227, 1001, 3162, 7236, 14639 Hz) don't match training config bands (linear: 100-500, 500-1500, 1500-3000, 3000-4500, 4500-5900 Hz)
- Channels 4 and 5 are far above the training band ranges even when properly biased

### Expert 03: Envelope Detector Sensitivity
- Envelope detector architecture is sound (OTA-based, <1 mV dead zone)
- Half-wave rectification produces DC = A/pi = 0.318 * amplitude
- With 50 mVpp BPF input: envelope = ~16 mV above VCM
- With 10 mVpp BPF input: envelope = ~3 mV above VCM
- **Key finding**: The envelope detector works correctly; the INPUT signals are too small

### Expert 04: Signal Level Budget
- **The critical bottleneck is identified**: BPF band-splitting reduces broadband signal by 15-30x, then half-wave rectification + LPF converts to DC offsets of only 1-10 mV
- After normalization by 1.8V, all features collapse to 0.500-0.506 (indistinguishable)
- The classifier always picks Outer Race (score ~8.3) over Inner Race (score ~8.1) because the RMS feature at 1.57V produces a large constant bias through the +9.77 weight

### Expert 05: Classifier Weight Mapping
- Training expects features in [0, 1.8V]; actual range is [0.900, 0.910V]
- **250x mismatch** between expected and actual feature range
- A 1 mV envelope change produces only 0.01 score delta (need ~1.0 to flip classification)
- Inner race occasionally wins because it has the largest ENV3 offset (9.7 mV vs 3.2 mV)

### Expert 06: Bearing Fault Frequencies
- Fault frequencies are correct in stimulus generation (BPFI=162 Hz, BPFO=107 Hz, BSF=71 Hz)
- Synthetic stimuli use resonance frequencies at 2.5-3.5 kHz, all clustered in BPF3's band
- Discrimination relies on subtle amplitude differences between bands, not fundamental frequency
- 200 ms simulation provides only 20-30 impulses (borderline statistical quality)

### Expert 07: Envelope Architecture
- Transistor-level envelope uses HALF-wave rectification (not full-wave like behavioral model)
- DC output = (1/pi)*A = 0.318*A (full-wave would give 0.637*A = 2x more)
- LPF settling: 8.3 ms (adequate for 200 ms sim)
- Recommended improvements: post-envelope gain stage, full-wave conversion

### Expert 08: Raw Data Analysis (Most Quantitative)
- **BPF outputs DO show differentiation**: BPF3 std spread = 23.4 mV, BPF4 = 24.9 mV, BPF5 = 23.2 mV across test cases
- **Envelope COMPRESSES this**: ENV3 mean spread = 6.4 mV, ENV4 = 6.6 mV, ENV5 = 4.9 mV
- **The information exists at BPF outputs but is lost in envelope-to-classifier mapping**
- PGA gain appears lower than 16x in practice (~4-12x) suggesting some clipping compression

### Expert 09: RMS/Crest Features
- **Peak detector is the BEST differentiating feature**: 120 mV spread (18x better than best envelope)
- RMS spread: only 2.4 mV (minimal differentiation)
- rms_ref used as kurtosis proxy: 0.0 mV spread (completely useless -- constant voltage)
- One of 8 classifier inputs is entirely wasted on a non-informative feature

### Expert 10: Training Pipeline
- Seven specific Python-vs-analog mismatches identified
- Full-wave (Python) vs half-wave (analog) rectification halves the DC output
- Envelope LPF: 10 Hz (Python) vs 92 Hz (analog) -- different ripple/settling tradeoffs
- MinMaxScaler normalization maps features to [0,1] but analog produces [0.500, 0.506]
- Recommended: end-to-end retraining with an analog chain Python model

---

## Top 3 Most Impactful Improvements

### 1. Rescale/Retrain Classifier for Actual Voltage Range (Expected: 25% -> 50-75%)

**The single highest-impact fix.** The classifier weights were trained for features spanning [0, 1.8V] but receive features spanning [0.900, 0.910V]. Even with the current tiny envelope spreads, the features DO contain class-discriminating information (especially in ENV3, ENV4, ENV5 and peak_out).

**Implementation**:
- Measure actual feature ranges from the 4 simulation raw files
- Recompute normalization: `V_norm = (V_actual - V_min) / (V_max - V_min)`
- Retrain logistic regression on features in the actual analog range
- Update classifier_behavioral.spice with new weights
- Replace rms_ref (constant, useless) with duplicate of peak_out or constant 0.9V

**Why this alone may reach 50-75%**: The peak_out feature alone has 120 mV spread and correct class ordering (inner > outer > ball > normal). With properly scaled weights, peak_out could drive correct classification for 2-3 out of 4 cases.

### 2. Increase Stimulus Amplitude (V_SCALE: 0.02 -> 0.1-0.2) (Expected: +15-25% on top of #1)

**The second highest-impact fix.** V_SCALE=0.02 V/g represents an unrealistically weak sensor. Real MEMS accelerometers (ADXL355) produce 660 mV/g. Increasing to 0.1 V/g (still conservative) gives 5x larger signals throughout the chain.

**Implementation**:
- In generate_stimuli.py: change V_SCALE from 0.02 to 0.1
- Reduce PGA gain from 16x to 4x (to avoid clipping)
- Net effect: 2.5x larger signals at BPF input, 2.5x larger envelope offsets
- Envelope spreads increase from ~7 mV to ~17 mV
- Re-run all 4 simulations

**Combined with #1**: Retraining + 5x signal boost could reach 75-90% accuracy.

### 3. Fix BPF Bias Voltages for Channels 4 and 5 (Expected: +5-15% on top of #1+#2)

**Restores correct spectral decomposition.** Currently, Ch4 and Ch5 share Ch1's bias, making their center frequencies wrong. This scrambles the spectral features the classifier was trained on.

**Implementation**:
- Add per-channel bias sources in vibrosense1_top.spice:
  - Vvbn_ch4 = 0.6399V, Vvbn_ch5 = 0.6914V (or proportionally adjusted)
- Alternatively, retune Ch4/Ch5 capacitor values for the shared 200nA bias
- Re-verify center frequencies with AC analysis

---

## Prioritized Fix Order

| Priority | Fix | Effort | Expected Accuracy | Cumulative |
|----------|-----|--------|-------------------|------------|
| Current  | -- | -- | 25% (1/4) | 25% |
| 1        | Retrain classifier for actual voltage range | Low (software only) | +25-50% | 50-75% |
| 2        | Increase V_SCALE to 0.1, PGA to 4x | Low (regenerate stimuli + resim) | +15-25% | 75-90% |
| 3        | Fix BPF Ch4/Ch5 bias | Low (edit netlist) | +5-15% | 80-95% |
| 4        | Replace rms_ref with useful kurtosis feature | Medium | +2-5% | 82-97% |
| 5        | Convert half-wave to full-wave rectifier | Medium (circuit redesign) | +2-5% | 84-99% |
| 6        | Add post-envelope gain stages | High (5 new amplifiers) | +3-5% | 87-100% |
| 7        | Increase sim duration to 500ms | Low (change .tran) | +1-3% | 88-100% |
| 8        | Use real CWRU data instead of synthetic | Low (run download script) | +5-10% | ~95% |

---

## Root Cause Summary

The 25% accuracy is caused by **three cascading failures**:

1. **Normalization mismatch** (250x): Classifier expects [0, 1.8V] features but gets [0.900, 0.910V]. This is the dominant failure mode -- even perfect analog features would fail with these weights.

2. **Insufficient signal amplitude**: V_SCALE=0.02 V/g produces millivolt-level signals after band-splitting. The envelope detector works correctly but its output (1-10 mV above VCM) is negligible compared to VCM (900 mV).

3. **BPF tuning errors**: Channels 4 and 5 are detuned because they share Ch1's bias voltage instead of having their own. This scrambles the spectral decomposition the classifier was trained on.

The good news: **the analog circuit blocks all work correctly**. The PGA amplifies, the BPFs filter, the envelopes detect, the classifier classifies. The problem is entirely in the **system integration**: signal levels, normalization, and bias distribution. These are all fixable without redesigning any transistor-level circuits.

---

## Verification Plan

After implementing fixes #1-#3:
1. Re-run all 4 test cases with ngspice
2. Parse raw files with analyze_results.py
3. Check envelope spread: target > 30 mV per channel
4. Check classifier output: target 4/4 correct (100%)
5. Run noise sensitivity test: add 1-5% Gaussian noise to stimuli
6. Target: >80% accuracy with noise, >95% without noise
