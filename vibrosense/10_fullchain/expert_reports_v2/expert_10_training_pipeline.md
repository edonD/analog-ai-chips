# Expert Report 10: Training Pipeline Analysis

## 1. Training Pipeline Overview

File: `09_training/train.py`

### Pipeline Steps
1. Load data (CWRU .mat files or synthetic generation)
2. Segment into 0.5s windows (6000 samples at 12 kHz)
3. Extract 8 features per window:
   - Features 0-4: Band envelope energy (5 BPF bands)
   - Feature 5: Broadband RMS
   - Feature 6: Crest factor (peak/RMS)
   - Feature 7: Kurtosis
4. Normalize features with MinMaxScaler to [0, 1]
5. Train LogisticRegression with quantization-aware hyperparameter tuning
6. Quantize weights to 4-bit (16 levels)
7. Export to SPICE format

## 2. Feature Extraction Details

### Band-Pass Filtering (Python)
- 2nd-order Butterworth band-pass (scipy)
- Bands from config: [100-500], [500-1500], [1500-3000], [3000-4500], [4500-5900] Hz

### Envelope Detection (Python)
- Full-wave rectification: `np.abs(filtered)`
- 1st-order IIR LPF with alpha = 1 - exp(-1/(fs*tau))
- tau = 1/(2*pi*envelope_lpf_hz)
- envelope_lpf_hz = 10 Hz (from config)
- Feature value = mean(envelope) over 0.5s window

### Key Difference: Python vs Analog

| Aspect | Python Training | Analog Chain |
|--------|----------------|--------------|
| BPF order | 2nd-order Butterworth | 2nd-order Tow-Thomas |
| BPF bands | [100-500] etc | f0=227, 1001, 3162, 7236*, 14639* Hz |
| Rectification | Full-wave (abs) | Half-wave (OTA) |
| Envelope LPF | IIR, fc=10 Hz | Gm-C, fc=92 Hz |
| Feature | mean(envelope) | DC voltage at end of sim |
| Window | 0.5 seconds | 0.2 seconds |
| RMS | np.sqrt(mean(x^2)) | MOSFET square-law |
| Crest | max(abs(x))/RMS | Peak detector / (RMS computation) |
| Kurtosis | scipy.stats.kurtosis | rms_ref (constant!) |

*BPF4 and BPF5 are detuned in analog due to shared bias (see Expert 02)

## 3. Normalization Analysis

The training pipeline uses `MinMaxScaler`:
```python
feature_norm = (feature_raw - min) / (max - min)
```
This maps each feature independently to [0, 1].

### Normalization Parameters (from trained model)

| Feature | Min | Max | Range |
|---------|-----|-----|-------|
| BPF1 env  | 0.0142 | 0.0644 | 0.0502 |
| BPF2 env  | 0.0199 | 0.1041 | 0.0842 |
| BPF3 env  | 0.0172 | 0.2587 | 0.2415 |
| BPF4 env  | 0.0032 | 0.3578 | 0.3546 |
| BPF5 env  | 0.0017 | 0.0950 | 0.0933 |
| RMS       | 0.0631 | 0.6978 | 0.6347 |
| Crest     | 3.0247 | 17.0557 | 14.0310 |
| Kurtosis  | -0.4565 | 51.2060 | 51.6625 |

## 4. SPICE Export: Voltage Mapping

From `export_spice_vectors()` in train.py:
```python
voltage = X_test_norm[idx, feat] * 1.8  # scale to 0-1.8V
```

So a normalized feature of 0.0 -> 0.0V, and 1.0 -> 1.8V.

In the behavioral classifier:
```spice
Score = sum(w * V(in)/1.8) + bias
```

This correctly inverts the normalization: V(in)/1.8 recovers [0, 1].

**The classifier IS correct for features in [0, 1.8V].**
**The problem is that actual features are NOT in [0, 1.8V].**

## 5. The Calibration Gap

### What the classifier expects:
- Feature 0 (BPF1 env): 0.0V (normal) to 1.8V (max fault)
- Feature 1 (BPF2 env): 0.0V (normal) to 1.8V (max fault)
- ... etc

### What the analog chain produces:
- Feature 0 (BPF1 env): 0.9041V (normal) to 0.9044V (max fault)
- Feature 1 (BPF2 env): 0.9064V (normal) to 0.9088V (max fault)
- ... etc

### The mapping required:
```
V_classifier = (V_analog - VCM) / (V_max_analog - VCM) * 1.8
```
For BPF3 envelope: (0.9097 - 0.9) / (0.9097 - 0.9032) * 1.8 = 26.8V
...which exceeds the supply. The analog range is simply too compressed.

## 6. The Synthetic vs Real Data Issue

The training uses synthetic data (when CWRU .mat files unavailable):
- `generate_synthetic_data()` creates signals with class-specific spectral profiles
- Each class dominated by one BPF band (identity matrix profiles)
- This creates LARGE, CLEAN spectral differences

The full-chain stimulus also uses synthetic data:
- `generate_stimuli.py` creates bearing fault signals
- These model impulse excitation of resonances
- The spectral differences are SUBTLE (all faults excite similar resonance bands)

**Mismatch**: Training data has each class strongly exciting one specific band.
Analog data has all fault classes exciting similar frequency ranges (2.5-3.5 kHz)
with subtle modulation differences that the envelope may not capture well.

## 7. Re-Training Approach

### Option A: Simulation-in-the-Loop Training

1. Run analog simulations for many different input patterns
2. Extract actual envelope voltages from each simulation
3. Build a training dataset of (analog_features, labels)
4. Train classifier directly on analog feature space
5. Export weights for the millivolt-scale feature range

Advantages: Perfectly matched to actual hardware
Disadvantages: Requires many SPICE simulations (slow)

### Option B: Calibration Layer

1. Keep existing training on [0,1] normalized features
2. Add a calibration step between envelope and classifier:
   `V_cal = (V_env - VCM_measured) * Gain_cal + VCM_output`
3. Gain_cal = 1.8 / (expected envelope range)
4. This is essentially a per-feature PGA after the envelope

Advantages: Doesn't require retraining
Disadvantages: Requires per-channel gain stages (5 more amplifiers)

### Option C: Rescale Classifier Weights (Recommended)

1. Measure actual envelope range: [Vmin, Vmax] per channel
2. New normalization: feature_norm = (V - Vmin) / (Vmax - Vmin)
3. In SPICE: Score = sum(w' * (V(in) - Vmin) / (Vmax - Vmin)) + bias'
4. Weights stay the same, only the normalization changes

For this to work:
```
Old: Score = sum(w * V/1.8) + bias
New: Score = sum(w * (V - Vmin)/(Vmax - Vmin)) + bias

Expand: Score = sum(w/(Vmax-Vmin)) * V - sum(w*Vmin/(Vmax-Vmin)) + bias
      = sum(w_new * V) + bias_new

Where: w_new = w / (Vmax - Vmin)
       bias_new = bias - sum(w * Vmin / (Vmax - Vmin))
```

**But this requires that the analog features have the SAME relative
distribution as the training features, just linearly scaled.**
If the analog chain distorts the feature distribution (e.g., half-wave
vs full-wave rectification), the rescaling won't work.

### Option D: End-to-End Retraining (Best Long-Term)

1. Create a Python model of the analog chain:
   - PGA gain model (including clipping)
   - BPF transfer functions (actual Gm-C, not ideal Butterworth)
   - Half-wave rectifier model (not abs())
   - LPF with actual fc=92 Hz (not 10 Hz)
   - RMS squarer model
   - Peak detector model
2. Process training data through this analog model
3. Normalize the MODEL outputs (not ideal outputs)
4. Train classifier on model outputs
5. The weights will naturally account for analog non-idealities

This is the most robust solution because it creates a digital twin
of the analog chain and trains against it.

## 8. Specific Python vs Analog Mismatches to Fix

| # | Mismatch | Impact | Fix |
|---|----------|--------|-----|
| 1 | BPF bands don't match (config vs actual) | HIGH | Retune BPFs or retrain |
| 2 | Full-wave vs half-wave rectifier | 2x DC output | Use full-wave or retrain |
| 3 | Envelope LPF 10 Hz vs 92 Hz | Different ripple | Align settings |
| 4 | Feature window 0.5s vs 0.2s | Averaging quality | Increase sim time |
| 5 | Kurtosis vs rms_ref constant | Wasted feature | Add kurtosis circuit |
| 6 | MinMax to [0,1.8V] vs actual [0.90,0.91V] | CRITICAL | Rescale or retrain |
| 7 | Synthetic training data vs synthetic stimuli | Distribution mismatch | Align generation |

## 9. Priority Recommendation

**Immediate (can fix without re-simulation):**
1. Rescale classifier weights for actual voltage range (Option C)
2. This requires measuring actual envelope ranges and updating
   the behavioral classifier SPICE model

**Short-term (requires re-simulation):**
3. Increase V_SCALE to 0.1-0.2 V/g
4. Fix BPF bias voltages for channels 4-5
5. Increase sim duration to 500ms

**Medium-term (requires retraining):**
6. Build analog chain Python model (Option D)
7. Retrain with analog-aware features
8. Add real CWRU data to training pipeline