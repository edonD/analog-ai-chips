#!/usr/bin/env python3
"""
VibroSense-1 Training Pipeline
===============================
Trains a linear classifier on vibration data, quantizes weights to 4-bit,
and exports capacitor values for the analog MAC array (Block 06).

The pipeline is config-driven: swap configs/bearing_cwru.json for
configs/gearbox.json and the same hardware classifies gearbox faults
with different cap values and filter tuning.

Usage:
    python train.py                           # default: CWRU bearing
    python train.py --config configs/gearbox.json --data-dir data/gearbox/
    python train.py --config configs/pump_cavitation.json --synthetic
"""

import argparse
import json
import os
import sys
import warnings

import numpy as np
from scipy.signal import butter, lfilter
from scipy.stats import kurtosis
from scipy.ndimage import maximum_filter1d
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore', category=FutureWarning)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_config(config_path):
    with open(config_path) as f:
        cfg = json.load(f)
    print(f"Config: {cfg['name']} — {cfg['description']}")
    print(f"  Classes: {cfg['classes']}")
    print(f"  Bands:   {cfg['bands_hz']}")
    print(f"  Fs={cfg['sample_rate_hz']} Hz, window={cfg['window_seconds']}s, "
          f"Q={cfg['quantization_bits']}-bit")
    return cfg


# ---------------------------------------------------------------------------
# Data loading — CWRU .mat files
# ---------------------------------------------------------------------------

def load_cwru_data(data_dir, cfg):
    """Load CWRU .mat files, segment into windows, return (windows, labels)."""
    import scipy.io

    fs = cfg['sample_rate_hz']
    window_size = int(cfg['window_seconds'] * fs)

    # Map filename prefixes to class labels
    label_map = {
        'normal': 0,
        'IR': 1,
        'B0': 2,   # B007, B014, B021
        'OR': 3,
    }

    def classify_filename(fname):
        for prefix, label in label_map.items():
            if fname.startswith(prefix):
                return label
        return None

    windows = []
    labels = []
    file_counts = {c: 0 for c in range(cfg['n_classes'])}

    mat_files = sorted(f for f in os.listdir(data_dir) if f.endswith('.mat'))
    if not mat_files:
        print(f"ERROR: No .mat files found in {data_dir}")
        sys.exit(1)

    for fname in mat_files:
        label = classify_filename(fname)
        if label is None:
            continue

        mat = scipy.io.loadmat(os.path.join(data_dir, fname))
        de_keys = [k for k in mat.keys() if 'DE_time' in k]
        if not de_keys:
            continue

        signal = mat[de_keys[0]].flatten().astype(np.float64)
        n_windows = len(signal) // window_size

        for i in range(n_windows):
            w = signal[i * window_size : (i + 1) * window_size]
            windows.append(w)
            labels.append(label)

        file_counts[label] += 1

    X = np.array(windows)
    y = np.array(labels)

    print(f"\nData loaded from {data_dir}:")
    print(f"  Files per class: {file_counts}")
    print(f"  Total windows:   {len(y)}")
    print(f"  Window size:     {window_size} samples ({cfg['window_seconds']}s)")
    for c in range(cfg['n_classes']):
        print(f"  Class {c} ({cfg['classes'][c]:>15s}): {np.sum(y == c)} windows")

    return X, y


def generate_synthetic_data(cfg, n_per_class=200):
    """Generate synthetic vibration data for use cases without real datasets.

    Creates signals with class-specific spectral signatures matching
    the configured band structure, so the trained weights are physically
    meaningful even before real data is collected.
    """
    fs = cfg['sample_rate_hz']
    window_size = int(cfg['window_seconds'] * fs)
    bands = cfg['bands_hz']
    rng = np.random.RandomState(42)

    # Each class has a characteristic spectral profile
    # Profile[i] = relative energy in band i (higher = more energy)
    n_classes = cfg['n_classes']
    profiles = np.eye(n_classes, len(bands)) * 3.0 + 1.0  # each class dominated by one band
    # Add some cross-band energy and noise
    profiles += rng.uniform(0.2, 0.8, profiles.shape)
    # Class 0 (normal) has low flat energy across all bands
    profiles[0, :] = 0.5 + rng.uniform(0, 0.3, len(bands))

    windows = []
    labels = []
    t = np.arange(window_size) / fs

    for cls in range(n_classes):
        for _ in range(n_per_class):
            signal = np.zeros(window_size)
            for band_idx, (f_lo, f_hi) in enumerate(bands):
                # Sinusoid at band center + noise shaped to band
                f_center = np.sqrt(f_lo * f_hi)  # geometric mean
                amp = profiles[cls, band_idx] * rng.uniform(0.8, 1.2)
                phase = rng.uniform(0, 2 * np.pi)
                signal += amp * np.sin(2 * np.pi * f_center * t + phase)
                # Add narrowband noise
                bw_noise = rng.normal(0, amp * 0.3, window_size)
                try:
                    b, a = butter(2, [f_lo, f_hi], btype='band', fs=fs)
                    signal += lfilter(b, a, bw_noise)
                except ValueError:
                    pass

            # Add broadband noise floor
            signal += rng.normal(0, 0.2, window_size)

            # Class-specific kurtosis (impulsive faults)
            if cls > 0:
                n_impulses = rng.randint(3, 15)
                impulse_locs = rng.choice(window_size, n_impulses, replace=False)
                signal[impulse_locs] += rng.normal(0, profiles[cls].max() * 2, n_impulses)

            windows.append(signal)
            labels.append(cls)

    X = np.array(windows)
    y = np.array(labels)

    print(f"\nSynthetic data generated:")
    print(f"  {n_per_class} windows per class x {n_classes} classes = {len(y)} total")
    print(f"  Window size: {window_size} samples ({cfg['window_seconds']}s)")
    return X, y


# ---------------------------------------------------------------------------
# Feature extraction — matches analog Blocks 03-05
# ---------------------------------------------------------------------------

def extract_features(window, cfg):
    """Extract 8 features from one signal window.

    CRITICAL: This must match the analog signal chain exactly.
    - 5 band-pass filters: 2nd-order Butterworth (matches Gm-C Tow-Thomas)
    - 5 envelope detectors: abs() + 1st-order IIR LPF (matches analog rectifier + RC)
    - 1 broadband RMS
    - 1 crest factor
    - 1 kurtosis
    """
    fs = cfg['sample_rate_hz']
    bands = cfg['bands_hz']
    envelope_lpf_hz = cfg['envelope_lpf_hz']
    rms_window_ms = cfg['rms_window_ms']

    features = np.zeros(8)

    # --- Band envelope features (0-4) ---
    # IIR LPF coefficient matching analog envelope detector
    tau = 1.0 / (2 * np.pi * envelope_lpf_hz)
    alpha = 1 - np.exp(-1.0 / (fs * tau))

    for i, (f_low, f_high) in enumerate(bands):
        if i >= 5:
            break
        # 2nd-order Butterworth band-pass (matches Block 03 Tow-Thomas)
        try:
            b, a = butter(2, [f_low, f_high], btype='band', fs=fs)
            filtered = lfilter(b, a, window)
        except ValueError:
            filtered = window  # fallback if band is invalid

        # Full-wave rectification (matches Block 04 rectifier)
        rectified = np.abs(filtered)

        # 1st-order IIR low-pass (matches Block 04 RC filter)
        envelope = lfilter([alpha], [1, -(1 - alpha)], rectified)

        # Average envelope energy
        features[i] = np.mean(envelope)

    # --- Broadband RMS (feature 5) — matches Block 05 RMS-to-DC ---
    features[5] = np.sqrt(np.mean(window ** 2))

    # --- Crest factor (feature 6) — matches Block 05 peak/RMS ---
    rms_val = features[5]
    features[6] = np.max(np.abs(window)) / (rms_val + 1e-10)

    # --- Kurtosis (feature 7) — matches Block 05 analog approximation ---
    features[7] = kurtosis(window, fisher=True)

    return features


def extract_all_features(X_windows, cfg):
    """Extract features from all windows."""
    n = len(X_windows)
    X_feat = np.zeros((n, 8))
    for i in range(n):
        X_feat[i] = extract_features(X_windows[i], cfg)
        if (i + 1) % 500 == 0:
            print(f"  Feature extraction: {i+1}/{n}")
    print(f"  Feature extraction complete: {n} windows -> (n, 8) matrix")
    return X_feat


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train_and_evaluate(X_train, y_train, X_val, y_val, X_test, y_test, cfg):
    """Train LogisticRegression with quantization-aware hyperparameter tuning.

    Key insight: we tune C to maximize *quantized* accuracy, not float accuracy.
    Strong regularization (low C) keeps weights small and well-distributed,
    which quantizes much better — even if float accuracy is slightly lower.
    This is the right tradeoff for analog hardware.
    """
    class_names = cfg['classes']
    C_grid = cfg['regularization_C_grid']
    n_bits = cfg['quantization_bits']

    # --- Quantization-aware hyperparameter search ---
    print("\nHyperparameter tuning (quantization-aware):")
    print(f"  {'C':>8s} {'float_val':>10s} {'quant_val':>10s} {'w_range':>12s}")
    print("  " + "-" * 44)
    best_C = 1.0
    best_quant_val_acc = 0
    for C in C_grid:
        m = LogisticRegression(multi_class='multinomial', solver='lbfgs',
                               max_iter=2000, C=C, random_state=42)
        m.fit(X_train, y_train)
        float_acc = m.score(X_val, y_val)

        # Evaluate with quantized weights on validation set
        W_q, _, _, _, _ = quantize_weights(m.coef_, n_bits)
        B_q, _, _, _, _ = quantize_weights(m.intercept_, n_bits)
        quant_acc, _ = evaluate_quantized(X_val, y_val, W_q, B_q, cfg)

        w_range = m.coef_.max() - m.coef_.min()
        print(f"  {C:8.2f} {float_acc:10.4f} {quant_acc:10.4f} {w_range:12.2f}")

        if quant_acc > best_quant_val_acc or (
                quant_acc == best_quant_val_acc and float_acc > best_quant_val_acc):
            best_quant_val_acc = quant_acc
            best_C = C

    print(f"  -> Best C={best_C}, quant_val_acc={best_quant_val_acc:.4f}")

    # --- Final training ---
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs',
                               max_iter=2000, C=best_C, random_state=42)
    model.fit(X_train, y_train)

    train_acc = model.score(X_train, y_train)
    val_acc = model.score(X_val, y_val)
    test_acc = model.score(X_test, y_test)

    print(f"\nFloat model results:")
    print(f"  Train accuracy: {train_acc:.4f}")
    print(f"  Val accuracy:   {val_acc:.4f}")
    print(f"  Test accuracy:  {test_acc:.4f}")

    # Weight matrix shape
    W = model.coef_      # (n_classes, 8)
    B = model.intercept_  # (n_classes,)
    print(f"  Weight matrix:  {W.shape} ({W.size} weights)")
    print(f"  Bias vector:    {B.shape} ({B.size} biases)")
    print(f"  Total params:   {W.size + B.size}")

    return model, train_acc, val_acc, test_acc


# ---------------------------------------------------------------------------
# Quantization
# ---------------------------------------------------------------------------

def quantize_weights(weights, n_bits=4):
    """Quantize float weights to n_bits uniform levels.

    Maps to capacitor values: cap = index * C_unit.
    16 levels (4-bit) with ~0.1% matching at 130nm = reliable discrimination.
    """
    n_levels = 2 ** n_bits
    w_min = weights.min()
    w_max = weights.max()

    if w_max == w_min:
        return weights.copy(), np.zeros_like(weights, dtype=int), w_min, w_max, 1.0

    scale = (w_max - w_min) / (n_levels - 1)
    indices = np.round((weights - w_min) / scale).astype(int)
    indices = np.clip(indices, 0, n_levels - 1)
    quantized = w_min + indices * scale

    return quantized, indices, float(w_min), float(w_max), float(scale)


def predict_quantized(X, W_quant, B_quant):
    """Predict using quantized weights (pure linear model)."""
    logits = X @ W_quant.T + B_quant
    return np.argmax(logits, axis=1)


def evaluate_quantized(X_test, y_test, W_quant, B_quant, cfg):
    """Evaluate quantized model."""
    y_pred = predict_quantized(X_test, W_quant, B_quant)
    acc = np.mean(y_pred == y_test)
    return acc, y_pred


def evaluate_with_noise(X, y, W, B, sigma_frac, n_trials=100):
    """Evaluate accuracy with Gaussian noise on features (analog noise model)."""
    rng = np.random.RandomState(42)
    accuracies = []
    for _ in range(n_trials):
        noise = rng.normal(0, sigma_frac, size=X.shape)
        X_noisy = np.clip(X + noise, 0, 1)
        y_pred = predict_quantized(X_noisy, W, B)
        accuracies.append(np.mean(y_pred == y))
    return np.mean(accuracies), np.std(accuracies)


# ---------------------------------------------------------------------------
# SPICE export — capacitor values for Block 06
# ---------------------------------------------------------------------------

def export_spice_weights(W_indices, B_indices, w_min, w_max, w_scale,
                         b_min, b_max, b_scale, cfg, accuracies,
                         norm_params, filename):
    """Export weights as SPICE .param file for Block 06 MAC array.

    Each weight maps to a MIM capacitor: C = index * C_unit.
    The hardware SPI (Block 08) can load these at runtime, so swapping
    from bearing detection to gearbox monitoring = new cap values via SPI.
    """
    c_unit = cfg['c_unit_fF']

    with open(filename, 'w') as f:
        f.write(f"* VibroSense-1 Classifier Weights — {cfg['name']}\n")
        f.write(f"* {cfg['description']}\n")
        f.write(f"* Generated by Block 09 training pipeline\n")
        f.write(f"* Float accuracy:     {accuracies['test_float']:.4f}\n")
        f.write(f"* Quantized accuracy: {accuracies['test_quantized']:.4f}\n")
        f.write(f"* Weight range: [{w_min:.6f}, {w_max:.6f}]\n")
        f.write(f"* Quantization step: {w_scale:.6f}\n")
        f.write(f"* C_unit = {c_unit}fF, max capacitor = {15 * c_unit}fF\n")
        f.write(f"*\n")
        f.write(f"* Filter band tuning for this use case:\n")
        for i, (f_lo, f_hi) in enumerate(cfg['bands_hz']):
            f.write(f"*   BPF{i+1}: {f_lo}-{f_hi} Hz — {cfg['band_labels'][i]}\n")
        f.write(f"*\n")
        f.write(f"* PGA gain: {cfg['pga_gain']}\n\n")

        # Weight capacitors
        f.write("* ========== Weight Capacitors (class x feature) ==========\n")
        f.write("* C_wXY = weight[class X][feature Y] * C_unit\n")
        f.write("* 32 capacitors total for 4-class x 8-feature MAC\n\n")
        for cls in range(cfg['n_classes']):
            f.write(f"* --- Class {cls}: {cfg['classes'][cls]} ---\n")
            for feat in range(8):
                idx = W_indices[cls, feat]
                cap_fF = idx * c_unit
                f.write(f".param C_w{cls}{feat} = {cap_fF}f "
                        f"  $ idx={idx:2d}  feat={feat}\n")
            f.write("\n")

        # Bias current sources
        f.write("* ========== Bias Current Sources ==========\n")
        f.write("* I_bX = bias[class X] mapped to current\n\n")
        for cls in range(cfg['n_classes']):
            idx = B_indices[cls]
            f.write(f".param I_b{cls} = {idx * 100}n  "
                    f"$ {cfg['classes'][cls]}, idx={idx}\n")

        # Normalization parameters (inform analog gain design)
        f.write("\n* ========== Normalization Parameters ==========\n")
        f.write("* These inform PGA gain and filter tuning in Blocks 02-05\n")
        f.write("* so analog outputs map to [0, 1.8V] without digital normalization\n\n")
        for i in range(8):
            feat_name = ['band1_env', 'band2_env', 'band3_env', 'band4_env',
                         'band5_env', 'broadband_rms', 'crest_factor', 'kurtosis'][i]
            f.write(f".param norm_min{i} = {norm_params['min'][i]:.6f}  $ {feat_name}\n")
            f.write(f".param norm_max{i} = {norm_params['max'][i]:.6f}\n")

        # SPI register values (Block 08 WEIGHT0-3 registers)
        f.write("\n* ========== SPI Register Values (Block 08) ==========\n")
        f.write("* WEIGHT0-3 registers pack 8 x 4-bit indices per class\n")
        f.write("* Format: [feat7:feat6:feat5:feat4:feat3:feat2:feat1:feat0]\n\n")
        for cls in range(cfg['n_classes']):
            reg_val = 0
            for feat in range(8):
                reg_val |= (int(W_indices[cls, feat]) & 0xF) << (feat * 4)
            f.write(f".param WEIGHT{cls}_reg = 32'h{reg_val:08X}  "
                    f"$ {cfg['classes'][cls]}\n")

    print(f"  SPICE weights exported: {filename}")


def export_spice_vectors(X_test_norm, y_test, cfg, filename,
                         n_per_class=5, hold_time=1e-3):
    """Export test feature vectors as SPICE PWL sources for Block 10."""
    class_names = cfg['classes']
    rng = np.random.RandomState(42)

    with open(filename, 'w') as f:
        f.write(f"* VibroSense-1 Test Feature Vectors — {cfg['name']}\n")
        f.write(f"* Generated by Block 09 training pipeline\n")
        f.write(f"* {n_per_class} vectors per class, {hold_time*1e3:.1f}ms hold\n\n")

        # Select representative vectors
        selected = []
        selected_labels = []
        for cls in range(cfg['n_classes']):
            cls_indices = np.where(y_test == cls)[0]
            n_avail = min(n_per_class, len(cls_indices))
            chosen = rng.choice(cls_indices, size=n_avail, replace=False)
            selected.extend(chosen)
            selected_labels.extend([cls] * n_avail)

        total_vectors = len(selected)
        total_time = total_vectors * hold_time

        # One PWL source per feature
        feat_names = ['band1_env', 'band2_env', 'band3_env', 'band4_env',
                      'band5_env', 'rms', 'crest', 'kurtosis']
        for feat in range(8):
            f.write(f"* Feature {feat}: {feat_names[feat]}\n")
            f.write(f"V_feat{feat} feat{feat} gnd PWL(\n")
            for i, idx in enumerate(selected):
                t_start = i * hold_time
                t_end = (i + 1) * hold_time - 1e-9
                voltage = X_test_norm[idx, feat] * 1.8  # scale to 0-1.8V
                f.write(f"+  {t_start:.9f} {voltage:.6f}\n")
                f.write(f"+  {t_end:.9f} {voltage:.6f}\n")
            f.write(f"+  {total_time:.9f} 0.0)\n\n")

        # Expected labels
        f.write("* ========== Expected Labels ==========\n")
        for i, idx in enumerate(selected):
            f.write(f"* Vector {i:3d}: class={y_test[idx]} "
                    f"({class_names[y_test[idx]]})\n")

    print(f"  SPICE vectors exported: {filename}")


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------

def export_json(model, W_float, B_float, W_quant, W_indices, B_quant, B_indices,
                w_min, w_max, w_scale, b_min, b_max, b_scale,
                norm_params, accuracies, cfg, filename):
    """Export everything to JSON for Block 06/08/10 consumption."""
    results = {
        'config': cfg['name'],
        'description': cfg['description'],
        'model': 'LogisticRegression',
        'n_features': 8,
        'n_classes': cfg['n_classes'],
        'class_names': cfg['classes'],
        'feature_names': [
            'band1_env', 'band2_env', 'band3_env', 'band4_env', 'band5_env',
            'broadband_rms', 'crest_factor', 'kurtosis'
        ],
        'feature_bands_hz': cfg['bands_hz'],
        'float_weights': W_float.tolist(),
        'float_biases': B_float.tolist(),
        'quantized_weights': W_quant.tolist(),
        'quantized_biases': B_quant.tolist(),
        'quantized_indices': W_indices.tolist(),
        'bias_indices': B_indices.tolist(),
        'quantization': {
            'n_bits': cfg['quantization_bits'],
            'w_min': w_min,
            'w_max': w_max,
            'w_scale': w_scale,
            'b_min': b_min,
            'b_max': b_max,
            'b_scale': b_scale,
            'c_unit_fF': cfg['c_unit_fF'],
        },
        'normalization': norm_params,
        'accuracy': accuracies,
        'hardware_mapping': {
            'pga_gain': cfg['pga_gain'],
            'filter_bands_hz': cfg['bands_hz'],
            'envelope_lpf_hz': cfg['envelope_lpf_hz'],
            'n_capacitors': W_float.size,
            'max_cap_fF': 15 * cfg['c_unit_fF'],
            'total_cap_area_um2_est': W_float.size * 15 * cfg['c_unit_fF'] * 0.001,
        },
    }

    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  JSON exported: {filename}")


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def plot_confusion_matrices(y_test, y_pred_float, y_pred_quant, y_pred_noisy,
                            cfg, filename):
    class_names = cfg['classes']

    cm_float = confusion_matrix(y_test, y_pred_float)
    cm_quant = confusion_matrix(y_test, y_pred_quant)
    cm_noisy = confusion_matrix(y_test, y_pred_noisy)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, cm, title in zip(axes,
            [cm_float, cm_quant, cm_noisy],
            ['Float Weights', '4-bit Quantized', 'Quantized + 2% Noise']):
        im = ax.imshow(cm, cmap='Blues')
        ax.set_title(f'{title}\n({cfg["name"]})', fontsize=11)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('True')
        ax.set_xticks(range(cfg['n_classes']))
        ax.set_yticks(range(cfg['n_classes']))
        ax.set_xticklabels(class_names, rotation=45, ha='right', fontsize=9)
        ax.set_yticklabels(class_names, fontsize=9)
        for i in range(cfg['n_classes']):
            for j in range(cfg['n_classes']):
                ax.text(j, i, str(cm[i, j]), ha='center', va='center',
                        color='white' if cm[i, j] > cm.max() / 2 else 'black')

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"  Confusion matrix plot: {filename}")


def plot_weight_histogram(W_float, W_indices, cfg, filename):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].hist(W_float.flatten(), bins=30, alpha=0.7, color='steelblue')
    axes[0].set_title(f'Float Weights — {cfg["name"]}')
    axes[0].set_xlabel('Weight Value')
    axes[0].set_ylabel('Count')
    axes[0].axvline(0, color='red', linestyle='--', alpha=0.5)

    n_bits = cfg['quantization_bits']
    n_levels = 2 ** n_bits
    axes[1].hist(W_indices.flatten(), bins=np.arange(-0.5, n_levels + 0.5, 1),
                 alpha=0.7, color='coral', rwidth=0.8)
    axes[1].set_title(f'Quantized Weight Indices ({n_bits}-bit)')
    axes[1].set_xlabel(f'Quantization Level (0-{n_levels-1})')
    axes[1].set_ylabel('Count')

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"  Weight histogram: {filename}")


def plot_noise_sensitivity(noise_results, cfg, filename):
    sigmas = [r[0] for r in noise_results]
    means = [r[1] for r in noise_results]
    stds = [r[2] for r in noise_results]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(sigmas, means, yerr=stds, marker='o', capsize=5,
                color='steelblue', linewidth=2)
    ax.axhline(cfg['targets']['noisy_accuracy_pct_2sigma'] / 100,
               color='red', linestyle='--', label=f"Target @ 2% noise")
    ax.set_xlabel('Noise Sigma (fraction of feature range)')
    ax.set_ylabel('Accuracy')
    ax.set_title(f'Noise Sensitivity — {cfg["name"]}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0.4, 1.05)

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"  Noise sensitivity plot: {filename}")


def plot_feature_importance(W_float, cfg, filename):
    """Show which features matter most per class — guides hardware tuning."""
    feat_names = ['BPF1\nenv', 'BPF2\nenv', 'BPF3\nenv', 'BPF4\nenv',
                  'BPF5\nenv', 'RMS', 'Crest', 'Kurt']

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(8)
    width = 0.8 / cfg['n_classes']
    colors = ['#2196F3', '#F44336', '#4CAF50', '#FF9800']

    for cls in range(cfg['n_classes']):
        offset = (cls - cfg['n_classes'] / 2 + 0.5) * width
        ax.bar(x + offset, np.abs(W_float[cls]), width, label=cfg['classes'][cls],
               color=colors[cls % len(colors)], alpha=0.8)

    ax.set_xticks(x)
    ax.set_xticklabels(feat_names, fontsize=9)
    ax.set_ylabel('|Weight|')
    ax.set_title(f'Feature Importance by Class — {cfg["name"]}\n'
                 f'(guides which filter bands need highest precision)')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"  Feature importance plot: {filename}")


def plot_capacitor_map(W_indices, cfg, filename):
    """Visual map of the 32 capacitor values — what gets programmed into silicon."""
    fig, ax = plt.subplots(figsize=(10, 4))
    c_unit = cfg['c_unit_fF']
    cap_values = W_indices * c_unit

    im = ax.imshow(cap_values, cmap='YlOrRd', aspect='auto')
    ax.set_xticks(range(8))
    ax.set_xticklabels(['BPF1', 'BPF2', 'BPF3', 'BPF4', 'BPF5',
                         'RMS', 'Crest', 'Kurt'], fontsize=9)
    ax.set_yticks(range(cfg['n_classes']))
    ax.set_yticklabels(cfg['classes'], fontsize=9)
    ax.set_xlabel('Feature (input)')
    ax.set_ylabel('Class (neuron)')
    ax.set_title(f'Capacitor Map (fF) — {cfg["name"]}\n'
                 f'C_unit={c_unit}fF, {cfg["quantization_bits"]}-bit, '
                 f'{W_indices.size} caps total')

    for i in range(cfg['n_classes']):
        for j in range(8):
            val = cap_values[i, j]
            ax.text(j, i, f'{val:.0f}', ha='center', va='center',
                    fontsize=8, fontweight='bold',
                    color='white' if val > cap_values.max() * 0.6 else 'black')

    cbar = plt.colorbar(im, ax=ax, label='Capacitance (fF)')
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"  Capacitor map: {filename}")


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def generate_report(y_test, y_pred_float, y_pred_quant, y_pred_noisy,
                    accuracies, noise_results, cfg, filename):
    class_names = cfg['classes']

    with open(filename, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write(f"CLASSIFICATION REPORT — VibroSense-1 Training Pipeline\n")
        f.write(f"Config: {cfg['name']} — {cfg['description']}\n")
        f.write("=" * 70 + "\n\n")

        f.write("--- Float Weights ---\n")
        f.write(classification_report(y_test, y_pred_float,
                target_names=class_names, digits=4) + "\n\n")

        f.write("--- 4-bit Quantized Weights ---\n")
        f.write(classification_report(y_test, y_pred_quant,
                target_names=class_names, digits=4) + "\n\n")

        f.write("--- Quantized + 2% Analog Noise ---\n")
        f.write(classification_report(y_test, y_pred_noisy,
                target_names=class_names, digits=4) + "\n\n")

        f.write("--- Summary ---\n")
        for k, v in accuracies.items():
            f.write(f"  {k:30s}: {v:.4f}\n")

        f.write("\n--- Noise Sensitivity ---\n")
        f.write(f"{'Sigma':>8s} {'Mean Acc':>10s} {'Std':>8s}\n")
        f.write("-" * 28 + "\n")
        for sigma, mean_acc, std_acc in noise_results:
            f.write(f"{sigma:8.3f} {mean_acc:10.4f} {std_acc:8.4f}\n")

        # PASS/FAIL
        targets = cfg['targets']
        f.write("\n--- PASS/FAIL Criteria ---\n")
        checks = [
            ('Float accuracy >= {:.0f}%'.format(targets['float_accuracy_pct']),
             accuracies['test_float'] * 100 >= targets['float_accuracy_pct']),
            ('Quantized accuracy >= {:.0f}%'.format(targets['quantized_accuracy_pct']),
             accuracies['test_quantized'] * 100 >= targets['quantized_accuracy_pct']),
            ('Quantization loss < {:.0f}pp'.format(targets['max_quantization_loss_pp']),
             accuracies['quantization_loss'] * 100 < targets['max_quantization_loss_pp']),
            ('Noisy accuracy (2%) >= {:.0f}%'.format(targets['noisy_accuracy_pct_2sigma']),
             accuracies.get('test_noisy_2pct', 0) * 100 >= targets['noisy_accuracy_pct_2sigma']),
        ]
        for desc, passed in checks:
            f.write(f"  {'PASS' if passed else 'FAIL'}: {desc}\n")

        # Hardware tuning recommendations
        f.write("\n--- Hardware Tuning Notes ---\n")
        f.write(f"  PGA gain setting: {cfg['pga_gain']}\n")
        f.write(f"  Filter bands (program into Block 03 via bias currents):\n")
        for i, (f_lo, f_hi) in enumerate(cfg['bands_hz']):
            f.write(f"    BPF{i+1}: {f_lo:5d} - {f_hi:5d} Hz\n")
        f.write(f"  Envelope LPF cutoff: {cfg['envelope_lpf_hz']} Hz\n")
        f.write(f"  Load weights via SPI WEIGHT0-3 registers (Block 08)\n")

    print(f"  Report: {filename}")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='VibroSense-1 Training Pipeline')
    parser.add_argument('--config', default=os.path.join(SCRIPT_DIR, 'configs', 'bearing_cwru.json'),
                        help='Use case config JSON')
    parser.add_argument('--data-dir', default=os.path.join(SCRIPT_DIR, 'data'),
                        help='Directory with .mat data files')
    parser.add_argument('--output-dir', default=os.path.join(SCRIPT_DIR, 'results'),
                        help='Output directory for results')
    parser.add_argument('--synthetic', action='store_true',
                        help='Generate synthetic data (for use cases without real datasets)')
    parser.add_argument('--n-synthetic', type=int, default=300,
                        help='Windows per class for synthetic data')
    args = parser.parse_args()

    print("=" * 70)
    print("VibroSense-1 Training Pipeline")
    print("=" * 70)

    # 1. Load config
    cfg = load_config(args.config)
    os.makedirs(args.output_dir, exist_ok=True)

    # 2. Load or generate data
    if args.synthetic:
        print("\n--- Generating synthetic data ---")
        X_windows, y = generate_synthetic_data(cfg, n_per_class=args.n_synthetic)
    else:
        print("\n--- Loading data ---")
        if not os.path.isdir(args.data_dir) or not any(
                f.endswith('.mat') for f in os.listdir(args.data_dir)):
            print(f"No .mat files in {args.data_dir}")
            print("Run: python download_cwru.py")
            print("Or use --synthetic for synthetic data")
            sys.exit(1)
        X_windows, y = load_cwru_data(args.data_dir, cfg)

    # 3. Feature extraction
    print("\n--- Feature extraction ---")
    X_features = extract_all_features(X_windows, cfg)

    # Check for NaN/Inf
    n_bad = np.sum(~np.isfinite(X_features))
    if n_bad > 0:
        print(f"  WARNING: {n_bad} non-finite values, replacing with 0")
        X_features = np.nan_to_num(X_features, nan=0.0, posinf=0.0, neginf=0.0)

    # 4. Train/val/test split
    print("\n--- Data split ---")
    X_train, X_temp, y_train, y_temp = train_test_split(
        X_features, y, test_size=0.30, stratify=y, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42)
    print(f"  Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    for c in range(cfg['n_classes']):
        print(f"  Class {c} ({cfg['classes'][c]:>15s}): "
              f"train={np.sum(y_train==c)}, val={np.sum(y_val==c)}, "
              f"test={np.sum(y_test==c)}")

    # 5. Normalize to [0,1]
    print("\n--- Normalization ---")
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_train_norm = scaler.fit_transform(X_train)
    X_val_norm = scaler.transform(X_val)
    X_test_norm = scaler.transform(X_test)
    norm_params = {
        'min': scaler.data_min_.tolist(),
        'max': scaler.data_max_.tolist(),
        'scale': scaler.scale_.tolist(),
    }
    print(f"  Feature ranges (train):")
    feat_names = ['BPF1_env', 'BPF2_env', 'BPF3_env', 'BPF4_env',
                  'BPF5_env', 'RMS', 'Crest', 'Kurt']
    for i in range(8):
        print(f"    {feat_names[i]:>10s}: [{scaler.data_min_[i]:.4f}, "
              f"{scaler.data_max_[i]:.4f}]")

    # 6. Train
    print("\n--- Training ---")
    model, train_acc, val_acc, test_acc = train_and_evaluate(
        X_train_norm, y_train, X_val_norm, y_val, X_test_norm, y_test, cfg)

    W_float = model.coef_
    B_float = model.intercept_
    y_pred_float = model.predict(X_test_norm)

    # 7. Quantize
    print("\n--- Quantization ---")
    n_bits = cfg['quantization_bits']
    W_quant, W_indices, w_min, w_max, w_scale = quantize_weights(W_float, n_bits)
    B_quant, B_indices, b_min, b_max, b_scale = quantize_weights(B_float, n_bits)

    quant_acc, y_pred_quant = evaluate_quantized(
        X_test_norm, y_test, W_quant, B_quant, cfg)

    print(f"  Weight MSE:       {np.mean((W_float - W_quant)**2):.6f}")
    print(f"  Max weight error: {np.max(np.abs(W_float - W_quant)):.6f}")
    print(f"  Quant step:       {w_scale:.6f}")
    print(f"  Weight range:     [{w_min:.4f}, {w_max:.4f}]")
    print(f"  Quantized acc:    {quant_acc:.4f}")
    print(f"  Accuracy loss:    {test_acc - quant_acc:.4f} "
          f"({(test_acc - quant_acc)*100:.1f} pp)")

    # 8. Noise sensitivity
    print("\n--- Noise sensitivity ---")
    noise_levels = [0.0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.10]
    noise_results = []
    print(f"  {'Sigma':>8s} {'Mean Acc':>10s} {'Std':>8s}")
    print("  " + "-" * 28)
    for sigma in noise_levels:
        mean_acc, std_acc = evaluate_with_noise(
            X_test_norm, y_test, W_quant, B_quant, sigma)
        noise_results.append((sigma, mean_acc, std_acc))
        print(f"  {sigma:8.3f} {mean_acc:10.4f} {std_acc:8.4f}")

    # Get noisy prediction for confusion matrix (single trial at 2%)
    rng = np.random.RandomState(99)
    noise_2pct = rng.normal(0, 0.02, size=X_test_norm.shape)
    X_noisy = np.clip(X_test_norm + noise_2pct, 0, 1)
    y_pred_noisy = predict_quantized(X_noisy, W_quant, B_quant)
    noisy_acc = np.mean(y_pred_noisy == y_test)

    # Collect accuracies
    accuracies = {
        'train_float': float(train_acc),
        'val_float': float(val_acc),
        'test_float': float(test_acc),
        'test_quantized': float(quant_acc),
        'quantization_loss': float(test_acc - quant_acc),
        'test_noisy_2pct': float(noisy_acc),
    }

    # 9. Export
    print("\n--- Exporting ---")
    export_spice_weights(W_indices, B_indices, w_min, w_max, w_scale,
                         b_min, b_max, b_scale, cfg, accuracies, norm_params,
                         os.path.join(args.output_dir, 'weights_spice.txt'))

    export_spice_vectors(X_test_norm, y_test, cfg,
                         os.path.join(args.output_dir, 'feature_vectors_spice.txt'))

    export_json(model, W_float, B_float, W_quant, W_indices, B_quant, B_indices,
                w_min, w_max, w_scale, b_min, b_max, b_scale,
                norm_params, accuracies, cfg,
                os.path.join(args.output_dir, 'trained_weights.json'))

    # 10. Plots
    print("\n--- Generating plots ---")
    plot_confusion_matrices(y_test, y_pred_float, y_pred_quant, y_pred_noisy,
                            cfg, os.path.join(args.output_dir, 'confusion_matrix.png'))
    plot_weight_histogram(W_float, W_indices, cfg,
                          os.path.join(args.output_dir, 'weight_histogram.png'))
    plot_noise_sensitivity(noise_results, cfg,
                           os.path.join(args.output_dir, 'noise_sensitivity.png'))
    plot_feature_importance(W_float, cfg,
                            os.path.join(args.output_dir, 'feature_importance.png'))
    plot_capacitor_map(W_indices, cfg,
                       os.path.join(args.output_dir, 'capacitor_map.png'))

    # 11. Report
    print("\n--- Generating report ---")
    generate_report(y_test, y_pred_float, y_pred_quant, y_pred_noisy,
                    accuracies, noise_results, cfg,
                    os.path.join(args.output_dir, 'classification_report.txt'))

    # 12. Summary
    targets = cfg['targets']
    print("\n" + "=" * 70)
    print(f"RESULTS SUMMARY — {cfg['name']}")
    print("=" * 70)
    print(f"  Float accuracy:      {test_acc*100:6.2f}%  "
          f"(target >= {targets['float_accuracy_pct']}%)")
    print(f"  Quantized accuracy:  {quant_acc*100:6.2f}%  "
          f"(target >= {targets['quantized_accuracy_pct']}%)")
    print(f"  Quantization loss:   {(test_acc-quant_acc)*100:6.2f} pp  "
          f"(target < {targets['max_quantization_loss_pp']} pp)")
    print(f"  Noisy acc (2%):      {noisy_acc*100:6.2f}%  "
          f"(target >= {targets['noisy_accuracy_pct_2sigma']}%)")
    print(f"  Capacitors:          {W_indices.size} x {cfg['c_unit_fF']}fF "
          f"(max {15*cfg['c_unit_fF']}fF)")
    print()

    # PASS/FAIL
    all_pass = True
    checks = [
        ('Float accuracy', test_acc * 100 >= targets['float_accuracy_pct']),
        ('Quantized accuracy', quant_acc * 100 >= targets['quantized_accuracy_pct']),
        ('Quantization loss', (test_acc - quant_acc) * 100 < targets['max_quantization_loss_pp']),
        ('Noisy accuracy (2%)', noisy_acc * 100 >= targets['noisy_accuracy_pct_2sigma']),
    ]
    for name, passed in checks:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  [{status}] {name}")

    print()
    if all_pass:
        print("  >>> ALL CHECKS PASSED <<<")
    else:
        print("  >>> SOME CHECKS FAILED — review results <<<")

    print(f"\n  Output: {args.output_dir}/")
    print("=" * 70)

    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main())
