# Block 09 — Training Pipeline: Program

## Overview

Python training pipeline that produces quantized weights for the VibroSense-1
analog classifier (Block 06). The pipeline extracts features that exactly match
the analog signal chain (Blocks 03-05), trains a linear classifier, quantizes
weights to 4-bit precision, and exports everything needed for SPICE simulation.

This is the bridge between the digital/software world and the analog hardware.
If the feature extraction here does not match the analog chain, the trained
weights will not work on the chip.

---

## SOTA Context and Honest Expectations

### CWRU Bearing Dataset Benchmarks

The CWRU bearing dataset is the most widely used benchmark for vibration-based
fault detection. Published results:

| Method | Accuracy | Notes |
|--------|----------|-------|
| Deep CNN (2020+) | 99.0-99.8% | Large model, GPU inference |
| 1D-CNN | 97-99% | Moderate model, edge-deployable |
| SVM + handcrafted features | 95-98% | Classic ML approach |
| Random Forest + FFT features | 94-97% | Ensemble method |
| Simple perceptron (float) | 88-95% | Single-layer, depends on features |
| KNN | 90-96% | Non-parametric |
| **Our target (float)** | **88-93%** | Linear classifier, 8 features |
| **Our target (4-bit quantized)** | **85-90%** | Same, with quantization loss |
| **Our target (with analog noise)** | **82-88%** | Quantized + 2% Gaussian noise |

### Why Intentionally Simple?

Our classifier is a single-layer linear model with 8 inputs and 4 outputs
(normal + 3 fault classes). This maps to exactly 32 multiply-accumulate
operations, implemented as 32 capacitors in the analog domain (Block 06).

A CNN that achieves 99% would require:
- Thousands of MACs per inference
- Weight storage in SRAM (thousands of bytes)
- ADCs with 8+ bit precision
- A digital accelerator or CPU
- 10-100x more power

Our 88-93% with 32 capacitors and <50 uW total power is the correct
engineering tradeoff for an always-on vibration monitor. The MCU that reads
our IRQ output can run a more sophisticated algorithm if confirmation is needed.

---

## Feature Extraction Specification

### Critical Requirement: Match the Analog Chain

The Python feature extraction MUST produce identical results (within analog
tolerances) to the analog signal chain in Blocks 03-05. This means:

1. **Filters must match Gm-C Tow-Thomas topology response** — use 2nd-order
   Butterworth as the design target (the Tow-Thomas circuit is configured
   for Butterworth response in Block 03).

2. **Envelope detection must match full-wave rectifier + LPF** — use
   `abs()` for rectification and a 1st-order IIR for the LPF.

3. **RMS and crest factor must match analog RMS-to-DC converter** — use
   the same time constant (10 ms window).

### Feature List (8 features)

| # | Feature | Analog Block | Python Implementation |
|---|---------|-------------|----------------------|
| 0 | Band 1 envelope | BPF1 (100-500 Hz) + envelope | Butterworth BP + abs() + LPF |
| 1 | Band 2 envelope | BPF2 (500-2000 Hz) + envelope | Butterworth BP + abs() + LPF |
| 2 | Band 3 envelope | BPF3 (2000-5000 Hz) + envelope | Butterworth BP + abs() + LPF |
| 3 | Band 4 envelope | BPF4 (5000-10k Hz) + envelope | Butterworth BP + abs() + LPF |
| 4 | Band 5 envelope | BPF5 (10k-Nyquist Hz) + envelope | Butterworth BP + abs() + LPF |
| 5 | Broadband RMS | RMS-to-DC converter | sqrt(mean(x^2)) over window |
| 6 | Crest factor | Peak detector / RMS | max(abs(x)) / RMS |
| 7 | Kurtosis | Analog approximation | scipy.stats.kurtosis |

### Band-Pass Filter Specifications

Each band-pass filter is a 2nd-order Butterworth implemented with
`scipy.signal.butter(N=2, Wn=[f_low, f_high], btype='band', fs=12000)`.

| Filter | f_low (Hz) | f_high (Hz) | Center (Hz) | Q |
|--------|-----------|------------|-------------|---|
| BPF1 | 100 | 500 | 224 | 0.56 |
| BPF2 | 500 | 2000 | 1000 | 0.67 |
| BPF3 | 2000 | 5000 | 3162 | 1.05 |
| BPF4 | 5000 | 10000 | 7071 | 1.41 |
| BPF5 | 10000 | Nyquist* | — | — |

*Nyquist = 6000 Hz for 12 kHz sample rate. BPF5 upper limit is capped at
5990 Hz to avoid instability at Nyquist.

**Note on BPF5:** At 12 kHz sample rate, the 10000-Nyquist band is extremely
narrow (10000-5999 Hz wraps — actually this band is not physically meaningful
at 12 kHz sampling). **Decision: for 12 kHz data, BPF5 uses (4000, 5990) Hz
instead.** For higher sample rates (48 kHz), the original (10000, Nyquist)
applies.

Actually, let's reconsider: at fs=12 kHz, Nyquist = 6 kHz. A band from
10000-Nyquist is impossible since 10000 > Nyquist. **Revised BPF5: (4000, 5900) Hz
for 12 kHz data.** This captures the highest representable frequencies.

### Envelope Detection

For each filtered band signal:

```python
# Full-wave rectification (matches analog full-wave rectifier)
rectified = np.abs(filtered_signal)

# 1st-order IIR low-pass filter at 10 Hz (matches analog LPF)
# Time constant tau = 1/(2*pi*10) = 15.9 ms
# For discrete: alpha = 1 - exp(-1/(fs*tau))
tau = 1.0 / (2 * np.pi * 10)  # 10 Hz cutoff
alpha = 1 - np.exp(-1.0 / (fs * tau))
envelope = np.zeros_like(rectified)
envelope[0] = rectified[0]
for i in range(1, len(rectified)):
    envelope[i] = alpha * rectified[i] + (1 - alpha) * envelope[i-1]
```

The envelope represents the energy in each frequency band over time. This
is what the analog envelope detector (Block 04) produces.

### RMS Calculation

```python
# Window-based RMS matching analog RMS-to-DC converter
# Window = 10 ms = 120 samples at 12 kHz
window = int(0.010 * fs)  # 120 samples
rms = np.sqrt(np.convolve(signal**2, np.ones(window)/window, mode='same'))
```

### Crest Factor

```python
# Peak / RMS over the same window
# Use rolling maximum for peak
from scipy.ndimage import maximum_filter1d
peak = maximum_filter1d(np.abs(signal), size=window)
crest = peak / (rms + 1e-10)  # avoid division by zero
```

### Kurtosis

```python
from scipy.stats import kurtosis
# Compute kurtosis over the feature extraction window
kurt = kurtosis(signal_window, fisher=True)  # excess kurtosis
# Normal distribution: kurt=0. Impulsive faults: kurt >> 0
```

### Feature Extraction Per Window

For a 0.5-second window (6000 samples at 12 kHz):

```python
def extract_features(window, fs=12000):
    features = np.zeros(8)

    # Band-pass filter + envelope for 5 bands
    bands = [(100, 500), (500, 2000), (2000, 4000), (4000, 5900)]
    # Note: only 4 bands feasible at 12 kHz. 5th band = (4000, 5900)
    # Adjust: use 5 bands with modified frequencies for 12 kHz
    bands = [(100, 500), (500, 1500), (1500, 3000), (3000, 4500), (4500, 5900)]

    for i, (f_low, f_high) in enumerate(bands):
        b, a = butter(2, [f_low, f_high], btype='band', fs=fs)
        filtered = lfilter(b, a, window)
        rectified = np.abs(filtered)
        # Envelope via LPF
        tau = 1.0 / (2 * np.pi * 10)
        alpha = 1 - np.exp(-1.0 / (fs * tau))
        env = lfilter([alpha], [1, -(1-alpha)], rectified)
        features[i] = np.mean(env)  # average envelope energy

    # Broadband RMS
    features[5] = np.sqrt(np.mean(window**2))

    # Crest factor
    features[6] = np.max(np.abs(window)) / (features[5] + 1e-10)

    # Kurtosis
    features[7] = kurtosis(window, fisher=True)

    return features
```

**Important frequency band revision for 12 kHz sampling:**

The original specification assumed a higher sample rate. At 12 kHz (Nyquist
= 6 kHz), we cannot have a band above 6 kHz. Revised bands:

| Filter | f_low (Hz) | f_high (Hz) | Physical meaning |
|--------|-----------|------------|-----------------|
| BPF1 | 100 | 500 | Low-frequency structural resonance |
| BPF2 | 500 | 1500 | Mid-frequency bearing tones |
| BPF3 | 1500 | 3000 | High-frequency bearing defect frequencies |
| BPF4 | 3000 | 4500 | Very high frequency, early fault detection |
| BPF5 | 4500 | 5900 | Near-Nyquist, impulse energy |

These bands must also be updated in the analog filter design (Block 03) to
match. The SPICE models and the Python feature extraction MUST use the same
frequencies.

---

## Data Loading and Preprocessing

### CWRU Dataset Structure

The CWRU bearing data center provides MATLAB .mat files. Each file contains
accelerometer data at 12 kHz (drive-end) or 48 kHz (fan-end). We use the
12 kHz drive-end data exclusively.

**Files to load (12 kHz drive-end, all motor loads):**

| Class | Fault Size | MATLAB Variable Pattern | Label |
|-------|-----------|------------------------|-------|
| Normal | N/A | `X097_DE_time`, `X098_DE_time`, etc. | 0 |
| Inner Race | 0.007" | `X105_DE_time`, `X106_DE_time`, etc. | 1 |
| Inner Race | 0.014" | `X169_DE_time`, `X170_DE_time`, etc. | 1 |
| Inner Race | 0.021" | `X209_DE_time`, `X210_DE_time`, etc. | 1 |
| Ball | 0.007" | `X118_DE_time`, `X119_DE_time`, etc. | 2 |
| Ball | 0.014" | `X185_DE_time`, `X186_DE_time`, etc. | 2 |
| Ball | 0.021" | `X222_DE_time`, `X223_DE_time`, etc. | 2 |
| Outer Race | 0.007" | `X130_DE_time`, `X131_DE_time`, etc. | 3 |
| Outer Race | 0.014" | `X197_DE_time`, `X198_DE_time`, etc. | 3 |
| Outer Race | 0.021" | `X234_DE_time`, `X235_DE_time`, etc. | 3 |

**Note:** Outer race faults have three sub-positions (centered @6:00, orthogonal
@3:00, opposite @12:00). For simplicity, we combine all outer race positions
into class 3. A more sophisticated classifier could distinguish them, but
our 4-class system (normal + 3 fault types) is the right granularity for
an always-on alarm.

### Loading Code

```python
import scipy.io
import numpy as np
import os

def load_cwru_data(data_dir, fs=12000):
    """Load all CWRU .mat files and return segmented windows with labels."""
    windows = []
    labels = []

    # Define file-to-label mapping
    # (filename_pattern, label, description)
    file_map = {
        'normal': 0,
        'IR': 1,      # inner race
        'B': 2,       # ball
        'OR': 3,      # outer race
    }

    for fname in sorted(os.listdir(data_dir)):
        if not fname.endswith('.mat'):
            continue
        mat = scipy.io.loadmat(os.path.join(data_dir, fname))
        # Find the DE_time variable
        de_key = [k for k in mat.keys() if 'DE_time' in k]
        if not de_key:
            continue
        signal = mat[de_key[0]].flatten()
        label = classify_filename(fname)  # map filename to class label

        # Segment into 0.5-second windows (6000 samples)
        window_size = int(0.5 * fs)  # 6000 samples
        n_windows = len(signal) // window_size
        for i in range(n_windows):
            w = signal[i * window_size : (i + 1) * window_size]
            windows.append(w)
            labels.append(label)

    return np.array(windows), np.array(labels)
```

### Data Split

```python
from sklearn.model_selection import train_test_split

X_windows, y = load_cwru_data('data/')

# Extract features for all windows
X_features = np.array([extract_features(w) for w in X_windows])

# Stratified split: 70% train, 15% validation, 15% test
X_train, X_temp, y_train, y_temp = train_test_split(
    X_features, y, test_size=0.30, stratify=y, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42
)

print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
print(f"Class distribution (train): {np.bincount(y_train)}")
```

---

## Normalization

### Min-Max Normalization to [0,1]

```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
X_train_norm = scaler.fit_transform(X_train)
X_val_norm = scaler.transform(X_val)
X_test_norm = scaler.transform(X_test)

# Save normalization parameters for deployment
norm_params = {
    'min': scaler.data_min_.tolist(),
    'max': scaler.data_max_.tolist(),
    'scale': scaler.scale_.tolist(),
}
```

**Why [0,1]?** The analog classifier uses capacitors to store weights. The
input features are represented as voltages between 0 and VDD. Normalizing
to [0,1] maps directly to [0V, 1.8V] in the analog domain.

**Deployment note:** The normalization parameters must be stored somewhere
accessible. Options:
1. Fixed in analog design (adjust PGA gains and filter tuning to produce
   pre-normalized outputs) — preferred, zero overhead
2. Stored as additional register values — adds complexity
3. Performed by external MCU — defeats always-on purpose

For VibroSense-1, we choose option 1: the analog chain gain stages are
designed so that typical vibration signals produce features already in the
[0, 1.8V] range. The normalization parameters from training inform the
analog gain design in Blocks 02-05.

---

## Training

### Model: Logistic Regression (Linear Classifier)

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(
    multi_class='multinomial',
    solver='lbfgs',
    max_iter=1000,
    C=1.0,           # regularization (tune on validation set)
    random_state=42,
)

model.fit(X_train_norm, y_train)

# Float accuracy
train_acc = model.score(X_train_norm, y_train)
val_acc = model.score(X_val_norm, y_val)
test_acc = model.score(X_test_norm, y_test)

print(f"Train accuracy: {train_acc:.4f}")
print(f"Val accuracy:   {val_acc:.4f}")
print(f"Test accuracy:  {test_acc:.4f}")
```

### Hyperparameter Tuning

Tune regularization strength C on validation set:

```python
best_C = 1.0
best_val_acc = 0
for C in [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0]:
    m = LogisticRegression(multi_class='multinomial', solver='lbfgs',
                           max_iter=1000, C=C, random_state=42)
    m.fit(X_train_norm, y_train)
    acc = m.score(X_val_norm, y_val)
    print(f"C={C:6.2f}  val_acc={acc:.4f}")
    if acc > best_val_acc:
        best_val_acc = acc
        best_C = C
```

### Weight Matrix

After training, the model has:
- `model.coef_`: shape (4, 8) — 4 classes x 8 features = 32 weights
- `model.intercept_`: shape (4,) — 4 bias terms

Total: 32 weights + 4 biases = 36 parameters.

In the analog domain, the 32 weights map to 32 capacitors. The 4 biases
map to 4 fixed current sources. See Block 06 for details.

---

## Weight Quantization

### 4-Bit Uniform Quantization

The analog classifier stores weights as capacitor values. With practical
capacitor matching (~0.1% at 130nm for 50fF+ caps), we can reliably
distinguish 16 levels (4 bits).

```python
def quantize_weights(weights, n_bits=4):
    """Quantize float weights to n_bits uniform levels."""
    n_levels = 2**n_bits  # 16 levels
    w_min = weights.min()
    w_max = weights.max()

    # Uniform quantization
    scale = (w_max - w_min) / (n_levels - 1)
    quantized_indices = np.round((weights - w_min) / scale).astype(int)
    quantized_indices = np.clip(quantized_indices, 0, n_levels - 1)

    # Reconstruct quantized values
    quantized_weights = w_min + quantized_indices * scale

    return quantized_weights, quantized_indices, w_min, w_max, scale

# Quantize
W_float = model.coef_  # (4, 8)
W_quant, W_indices, w_min, w_max, w_scale = quantize_weights(W_float)

# Also quantize biases (same scheme or separate)
B_float = model.intercept_  # (4,)
B_quant, B_indices, b_min, b_max, b_scale = quantize_weights(B_float)
```

### Quantization Error Analysis

```python
# Weight-level error
mse_weight = np.mean((W_float - W_quant)**2)
max_weight_error = np.max(np.abs(W_float - W_quant))
print(f"Weight MSE: {mse_weight:.6f}")
print(f"Max weight error: {max_weight_error:.6f}")
print(f"Quantization step: {w_scale:.6f}")
print(f"Weight range: [{w_min:.4f}, {w_max:.4f}]")

# Accuracy with quantized weights
def predict_quantized(X, W_quant, B_quant):
    """Predict using quantized weights (linear model)."""
    logits = X @ W_quant.T + B_quant
    return np.argmax(logits, axis=1)

y_pred_quant = predict_quantized(X_test_norm, W_quant, B_quant)
quant_acc = np.mean(y_pred_quant == y_test)
print(f"Quantized accuracy: {quant_acc:.4f}")
print(f"Accuracy loss from quantization: {test_acc - quant_acc:.4f}")
```

### Quantization Histogram

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Float weight distribution
axes[0].hist(W_float.flatten(), bins=30, alpha=0.7, color='blue')
axes[0].set_title('Float Weights Distribution')
axes[0].set_xlabel('Weight Value')
axes[0].set_ylabel('Count')

# Quantized weight distribution
axes[1].hist(W_indices.flatten(), bins=np.arange(-0.5, 16.5, 1),
             alpha=0.7, color='red', rwidth=0.8)
axes[1].set_title('Quantized Weight Indices (4-bit)')
axes[1].set_xlabel('Quantization Level (0-15)')
axes[1].set_ylabel('Count')

plt.tight_layout()
plt.savefig('results/weight_histogram.png', dpi=150)
plt.close()
```

**What to look for in the histogram:**

- If all weights cluster in 2-3 levels: 4 bits is overkill, but fine
- If weights concentrate at extremes: possible saturation issue
- If distribution is roughly uniform: good utilization of 4-bit range
- If one level has >50% of weights: model may be under-trained or features
  are redundant

---

## Analog Noise Simulation

### Purpose

The analog signal chain introduces noise: thermal noise from OTAs, mismatch
in capacitors, supply noise, etc. We simulate this by adding Gaussian noise
to the normalized features during inference.

### Noise Model

```python
def evaluate_with_noise(X, y, W, B, sigma_frac, n_trials=100):
    """Evaluate accuracy with additive Gaussian noise on features.

    sigma_frac: noise std as fraction of feature range (0.02 = 2%)
    """
    accuracies = []
    for trial in range(n_trials):
        noise = np.random.normal(0, sigma_frac, size=X.shape)
        X_noisy = np.clip(X + noise, 0, 1)  # clip to valid range
        y_pred = predict_quantized(X_noisy, W, B)
        acc = np.mean(y_pred == y)
        accuracies.append(acc)

    return np.mean(accuracies), np.std(accuracies)

# Evaluate at multiple noise levels
noise_levels = [0.0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.10]
print("\nNoise Sensitivity Analysis:")
print(f"{'Sigma':>8s} {'Mean Acc':>10s} {'Std':>8s}")
print("-" * 28)
for sigma in noise_levels:
    mean_acc, std_acc = evaluate_with_noise(
        X_test_norm, y_test, W_quant, B_quant, sigma
    )
    print(f"{sigma:8.3f} {mean_acc:10.4f} {std_acc:8.4f}")
```

**Expected results:**

| Noise sigma | Expected accuracy | Notes |
|-------------|------------------|-------|
| 0.00 | 85-90% | Quantized, no noise (baseline) |
| 0.005 | 85-90% | Negligible degradation |
| 0.01 | 84-89% | Slight degradation |
| 0.02 | 82-88% | **Target noise level** |
| 0.03 | 80-86% | Marginal |
| 0.05 | 75-82% | Significant degradation |
| 0.10 | 60-75% | Approaching random |

The 2% noise level corresponds to realistic analog circuit noise in the
VibroSense-1 signal chain (estimated from SPICE noise analysis of individual
blocks). If accuracy drops below 82% at 2% noise, we need to either:
1. Improve analog noise performance (bigger transistors, more current)
2. Add more features (more hardware)
3. Accept lower accuracy

---

## Evaluation and Reporting

### Confusion Matrix

```python
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import numpy as np

class_names = ['Normal', 'Inner Race', 'Ball', 'Outer Race']

# Float model confusion matrix
y_pred_float = model.predict(X_test_norm)
cm_float = confusion_matrix(y_test, y_pred_float)

# Quantized model confusion matrix
y_pred_quant = predict_quantized(X_test_norm, W_quant, B_quant)
cm_quant = confusion_matrix(y_test, y_pred_quant)

# Noisy quantized confusion matrix (single trial at sigma=0.02)
noise = np.random.normal(0, 0.02, size=X_test_norm.shape)
X_noisy = np.clip(X_test_norm + noise, 0, 1)
y_pred_noisy = predict_quantized(X_noisy, W_quant, B_quant)
cm_noisy = confusion_matrix(y_test, y_pred_noisy)

# Plot all three
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, cm, title in zip(axes,
    [cm_float, cm_quant, cm_noisy],
    ['Float Weights', '4-bit Quantized', 'Quantized + 2% Noise']):
    im = ax.imshow(cm, cmap='Blues')
    ax.set_title(title)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')
    ax.set_xticks(range(4))
    ax.set_yticks(range(4))
    ax.set_xticklabels(class_names, rotation=45, ha='right')
    ax.set_yticklabels(class_names)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, str(cm[i, j]), ha='center', va='center',
                    color='white' if cm[i, j] > cm.max()/2 else 'black')

plt.tight_layout()
plt.savefig('results/confusion_matrix.png', dpi=150)
plt.close()
```

### Classification Report

```python
report_float = classification_report(y_test, y_pred_float,
    target_names=class_names, digits=4)
report_quant = classification_report(y_test, y_pred_quant,
    target_names=class_names, digits=4)
report_noisy = classification_report(y_test, y_pred_noisy,
    target_names=class_names, digits=4)

with open('results/classification_report.txt', 'w') as f:
    f.write("=" * 60 + "\n")
    f.write("CLASSIFICATION REPORT — VibroSense-1 Training Pipeline\n")
    f.write("=" * 60 + "\n\n")

    f.write("--- Float Weights ---\n")
    f.write(report_float + "\n\n")

    f.write("--- 4-bit Quantized Weights ---\n")
    f.write(report_quant + "\n\n")

    f.write("--- Quantized + 2% Analog Noise ---\n")
    f.write(report_noisy + "\n\n")

    f.write(f"Float accuracy:     {test_acc:.4f}\n")
    f.write(f"Quantized accuracy: {quant_acc:.4f}\n")
    f.write(f"Accuracy loss:      {test_acc - quant_acc:.4f}\n")
    f.write(f"Noisy accuracy:     {np.mean(y_pred_noisy == y_test):.4f}\n")
```

---

## SPICE Export

### Weight Export for Block 06

The analog classifier (Block 06) needs weights as capacitor values. The
mapping is: capacitor value = W_index * C_unit, where C_unit is the unit
capacitance (e.g., 10 fF).

```python
def export_weights_spice(W_indices, B_indices, w_min, w_max, w_scale,
                         b_min, b_max, b_scale, filename):
    """Export weights as SPICE .param file for Block 06."""
    with open(filename, 'w') as f:
        f.write("* VibroSense-1 Classifier Weights\n")
        f.write("* Generated by Block 09 training pipeline\n")
        f.write(f"* Float accuracy: {test_acc:.4f}\n")
        f.write(f"* Quantized accuracy: {quant_acc:.4f}\n")
        f.write(f"* Weight range: [{w_min:.6f}, {w_max:.6f}]\n")
        f.write(f"* Quantization step: {w_scale:.6f}\n")
        f.write(f"* C_unit = 10fF, max capacitor = 150fF\n\n")

        # Weight capacitors: C_wXY = W_indices[X][Y] * C_unit
        f.write("* Weight capacitors (class x feature)\n")
        for cls in range(4):
            for feat in range(8):
                idx = W_indices[cls, feat]
                cap_fF = idx * 10  # 10 fF per level
                f.write(f".param C_w{cls}{feat} = {cap_fF}f\n")

        f.write("\n* Bias current sources\n")
        for cls in range(4):
            idx = B_indices[cls]
            # Bias maps to a current: I_bias = idx * I_unit
            f.write(f".param I_b{cls} = {idx * 100}n\n")  # 100nA per level

        f.write("\n* Normalization parameters (for analog gain setting)\n")
        for i in range(8):
            f.write(f".param norm_min{i} = {norm_params['min'][i]:.6f}\n")
            f.write(f".param norm_max{i} = {norm_params['max'][i]:.6f}\n")

export_weights_spice(W_indices, B_indices, w_min, w_max, w_scale,
                     b_min, b_max, b_scale, 'results/weights_spice.txt')
```

### Feature Vector Export for Block 10

Block 10 (full-chain integration) needs test vectors as time-domain analog
waveforms. We export representative feature vectors as SPICE PWL (piecewise
linear) sources.

```python
def export_feature_vectors_spice(X_test_norm, y_test, filename,
                                 n_per_class=5, hold_time=1e-3):
    """Export feature vectors as SPICE PWL stimuli.

    Each feature is a voltage source that steps through test vectors.
    hold_time: how long each vector is held (1ms = 1 classifier cycle)
    """
    with open(filename, 'w') as f:
        f.write("* VibroSense-1 Test Feature Vectors\n")
        f.write("* Generated by Block 09 training pipeline\n")
        f.write(f"* {n_per_class} vectors per class, {hold_time*1e3:.1f}ms hold\n\n")

        # Select n_per_class representative vectors per class
        selected = []
        for cls in range(4):
            cls_indices = np.where(y_test == cls)[0]
            chosen = np.random.choice(cls_indices, size=n_per_class, replace=False)
            selected.extend(chosen)

        total_vectors = len(selected)
        total_time = total_vectors * hold_time

        # One PWL source per feature
        for feat in range(8):
            f.write(f"* Feature {feat} stimulus\n")
            f.write(f"V_feat{feat} feat{feat} gnd PWL(\n")
            for i, idx in enumerate(selected):
                t_start = i * hold_time
                t_end = (i + 1) * hold_time - 1e-9  # small gap for transition
                voltage = X_test_norm[idx, feat] * 1.8  # scale to 0-1.8V
                f.write(f"+  {t_start:.9f} {voltage:.6f}\n")
                f.write(f"+  {t_end:.9f} {voltage:.6f}\n")
            f.write(f"+  {total_time:.9f} 0.0)\n\n")

        # Also write expected labels for verification
        f.write("* Expected labels (for verification):\n")
        for i, idx in enumerate(selected):
            f.write(f"* Vector {i}: class={y_test[idx]} "
                    f"({class_names[y_test[idx]]})\n")

export_feature_vectors_spice(X_test_norm, y_test,
                             'results/feature_vectors_spice.txt')
```

---

## JSON Export

```python
import json

results = {
    'model': 'LogisticRegression',
    'n_features': 8,
    'n_classes': 4,
    'class_names': class_names,
    'float_weights': W_float.tolist(),
    'float_biases': B_float.tolist(),
    'quantized_indices': W_indices.tolist(),
    'quantized_weights': W_quant.tolist(),
    'quantized_biases': B_quant.tolist(),
    'bias_indices': B_indices.tolist(),
    'quantization': {
        'n_bits': 4,
        'w_min': float(w_min),
        'w_max': float(w_max),
        'w_scale': float(w_scale),
        'b_min': float(b_min),
        'b_max': float(b_max),
        'b_scale': float(b_scale),
    },
    'normalization': norm_params,
    'accuracy': {
        'train_float': float(train_acc),
        'val_float': float(val_acc),
        'test_float': float(test_acc),
        'test_quantized': float(quant_acc),
        'quantization_loss': float(test_acc - quant_acc),
    },
    'feature_bands_hz': bands,
    'feature_names': [
        'band1_env', 'band2_env', 'band3_env', 'band4_env', 'band5_env',
        'broadband_rms', 'crest_factor', 'kurtosis'
    ],
}

with open('results/trained_weights.json', 'w') as f:
    json.dump(results, f, indent=2)
```

---

## Complete Pipeline Script Structure

```
train.py:
  main():
    1. load_cwru_data()          — load .mat files, segment windows
    2. extract_all_features()    — apply feature extraction to all windows
    3. split_data()              — train/val/test split
    4. normalize()               — MinMaxScaler fit on train
    5. tune_hyperparams()        — grid search C on validation set
    6. train_model()             — fit LogisticRegression with best C
    7. evaluate_float()          — accuracy, confusion matrix, report
    8. quantize_weights()        — 4-bit uniform quantization
    9. evaluate_quantized()      — accuracy with quantized weights
   10. evaluate_noisy()          — accuracy with analog noise simulation
   11. export_json()             — trained_weights.json
   12. export_spice_weights()    — weights_spice.txt
   13. export_spice_vectors()    — feature_vectors_spice.txt
   14. generate_plots()          — confusion_matrix.png, weight_histogram.png
   15. generate_report()         — classification_report.txt
   16. print_summary()           — console output of all results
```

---

## PASS/FAIL Criteria

| Criterion | Target | Hard Fail |
|-----------|--------|-----------|
| Float test accuracy | >= 88% | < 85% |
| Quantized test accuracy | >= 85% | < 80% |
| Quantization accuracy loss | < 5 pp | >= 8 pp |
| Per-class recall (float) | >= 80% each | any class < 70% |
| Per-class recall (quantized) | >= 75% each | any class < 60% |
| Noisy accuracy (sigma=2%) | >= 82% | < 75% |
| Noisy accuracy (sigma=5%) | report only | — |
| Weight histogram | reasonable distribution | all weights same level |
| Confusion matrix | generated | missing |
| SPICE weight export | valid .param syntax | parse errors |
| SPICE vector export | valid PWL syntax | parse errors |
| JSON export | valid JSON, all fields | missing fields |
| Feature extraction | matches analog chain | different filter specs |

---

## Known Risks and Mitigations

**Risk 1: CWRU dataset is too easy.**
The CWRU dataset uses accelerometers directly on the bearing housing with
artificially seeded faults. Real-world performance will be worse. Mitigation:
the noise injection test simulates some degradation. For real deployment,
field calibration is required.

**Risk 2: 12 kHz sample rate limits frequency bands.**
At 12 kHz, we only have 6 kHz of bandwidth. Many bearing fault signatures
are above 6 kHz (ball pass frequency outer race harmonics). Mitigation:
the 48 kHz fan-end data could be used, but our ADC (Block 07) is designed
for ~100 kHz bandwidth, so this is not a hardware limitation — it is a
dataset limitation. Use 48 kHz data if available and re-derive filter bands.

**Risk 3: Linear classifier may confuse ball and outer race faults.**
These fault types produce similar frequency signatures (both excite the
ball-pass frequencies). The distinguishing feature is the modulation pattern,
which our envelope detector captures. If per-class recall for ball faults
drops below 70%, consider: (a) adding a 6th feature (envelope modulation
depth), or (b) merging ball and outer race into one "fault" class.

**Risk 4: Quantization may disproportionately affect one class.**
If the decision boundary for one class is defined by small weight differences,
4-bit quantization may destroy it. Mitigation: check per-class accuracy
before and after quantization. If one class drops >10 pp, consider
quantization-aware training (re-train with quantized weights in the loop).

---

## Execution

```bash
cd vibrosense/09_training
python train.py --data-dir data/ --output-dir results/
```

Expected runtime: < 60 seconds on any modern laptop. The dataset is small
(~100 MB) and the model is trivial. Feature extraction is the slow part
(scipy filtering), but still under 30 seconds for all windows.
