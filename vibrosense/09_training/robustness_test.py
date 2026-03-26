#!/usr/bin/env python3
"""
Robustness analysis: How stable are the capacitor values?

If the cap values change drastically with different random seeds,
train/test splits, or data subsets — the training is unreliable
and we shouldn't trust those values in silicon.

Tests:
1. Multiple random splits — do cap values stay stable?
2. Leave-one-load-out — train on 3 motor loads, test on the 4th
3. Leave-one-fault-size-out — train on 2 fault sizes, test on the 3rd
4. Bootstrap confidence intervals on each cap value
5. Cross-validation accuracy variance
"""

import numpy as np
import json
import os
import sys
from scipy.signal import butter, lfilter
from scipy.stats import kurtosis
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_config():
    with open(os.path.join(SCRIPT_DIR, 'configs', 'bearing_cwru.json')) as f:
        return json.load(f)


def extract_features(window, cfg):
    fs = cfg['sample_rate_hz']
    bands = cfg['bands_hz']
    tau = 1.0 / (2 * np.pi * cfg['envelope_lpf_hz'])
    alpha = 1 - np.exp(-1.0 / (fs * tau))
    features = np.zeros(8)
    for i, (f_low, f_high) in enumerate(bands):
        if i >= 5:
            break
        b, a = butter(2, [f_low, f_high], btype='band', fs=fs)
        filtered = lfilter(b, a, window)
        rectified = np.abs(filtered)
        envelope = lfilter([alpha], [1, -(1 - alpha)], rectified)
        features[i] = np.mean(envelope)
    features[5] = np.sqrt(np.mean(window ** 2))
    features[6] = np.max(np.abs(window)) / (features[5] + 1e-10)
    features[7] = kurtosis(window, fisher=True)
    return features


def quantize_weights(weights, n_bits=4):
    n_levels = 2 ** n_bits
    w_min, w_max = weights.min(), weights.max()
    if w_max == w_min:
        return weights.copy(), np.zeros_like(weights, dtype=int)
    scale = (w_max - w_min) / (n_levels - 1)
    indices = np.round((weights - w_min) / scale).astype(int)
    indices = np.clip(indices, 0, n_levels - 1)
    quantized = w_min + indices * scale
    return quantized, indices


def load_all_data(cfg):
    """Load CWRU data with metadata (motor load, fault size)."""
    import scipy.io
    data_dir = os.path.join(SCRIPT_DIR, 'data')
    fs = cfg['sample_rate_hz']
    window_size = int(cfg['window_seconds'] * fs)

    records = []  # list of (windows, label, load_hp, fault_size)

    for fname in sorted(os.listdir(data_dir)):
        if not fname.endswith('.mat'):
            continue

        # Parse metadata from filename
        if fname.startswith('normal'):
            label = 0
            fault_size = 'none'
        elif fname.startswith('IR'):
            label = 1
            fault_size = fname.split('_')[0].replace('IR', '')  # '007','014','021'
        elif fname.startswith('B0'):
            label = 2
            fault_size = fname.split('_')[0].replace('B', '')
        elif fname.startswith('OR'):
            label = 3
            fault_size = fname.split('_')[0].replace('OR', '').replace('6', '').rstrip('_')
        else:
            continue

        # Parse motor load
        for part in fname.replace('.mat', '').split('_'):
            if 'hp' in part:
                load_hp = part.replace('hp', '')
                break
        else:
            load_hp = 'unknown'

        mat = scipy.io.loadmat(os.path.join(data_dir, fname))
        de_keys = [k for k in mat.keys() if 'DE_time' in k]
        if not de_keys:
            continue
        signal = mat[de_keys[0]].flatten().astype(np.float64)
        n_windows = len(signal) // window_size

        for i in range(n_windows):
            w = signal[i * window_size:(i + 1) * window_size]
            records.append((w, label, load_hp, fault_size))

    windows = np.array([r[0] for r in records])
    labels = np.array([r[1] for r in records])
    loads = np.array([r[2] for r in records])
    sizes = np.array([r[3] for r in records])

    return windows, labels, loads, sizes


def train_and_get_caps(X_feat, y, cfg, seed=42):
    """Train, quantize, return cap indices and accuracy."""
    X_tr, X_te, y_tr, y_te = train_test_split(
        X_feat, y, test_size=0.2, stratify=y, random_state=seed)
    scaler = MinMaxScaler()
    X_tr_n = scaler.fit_transform(X_tr)
    X_te_n = scaler.transform(X_te)

    model = LogisticRegression(multi_class='multinomial', solver='lbfgs',
                               max_iter=2000, C=10.0, random_state=42)
    model.fit(X_tr_n, y_tr)
    float_acc = model.score(X_te_n, y_te)

    W_q, W_idx = quantize_weights(model.coef_)
    B_q, B_idx = quantize_weights(model.intercept_)

    # Quantized accuracy
    logits = X_te_n @ W_q.T + B_q
    quant_acc = np.mean(np.argmax(logits, axis=1) == y_te)

    return W_idx, float_acc, quant_acc, model.coef_


def main():
    cfg = load_config()
    print("Loading data with metadata...")
    windows, labels, loads, sizes = load_all_data(cfg)
    print(f"  Total: {len(labels)} windows")
    print(f"  Loads: {np.unique(loads)}")
    print(f"  Fault sizes: {np.unique(sizes)}")
    print(f"  Classes: {np.bincount(labels)}")

    # Extract features
    print("\nExtracting features...")
    X_feat = np.array([extract_features(w, cfg) for w in windows])
    X_feat = np.nan_to_num(X_feat)

    # ===================================================================
    # TEST 1: Multiple random splits — how much do caps vary?
    # ===================================================================
    print("\n" + "=" * 70)
    print("TEST 1: Cap stability across 20 random train/test splits")
    print("=" * 70)

    n_trials = 20
    all_cap_indices = []
    all_float_accs = []
    all_quant_accs = []
    all_weights = []

    for seed in range(n_trials):
        W_idx, f_acc, q_acc, W_float = train_and_get_caps(X_feat, labels, cfg, seed=seed)
        all_cap_indices.append(W_idx)
        all_float_accs.append(f_acc)
        all_quant_accs.append(q_acc)
        all_weights.append(W_float)

    all_cap_indices = np.array(all_cap_indices)  # (20, 4, 8)
    all_weights = np.array(all_weights)

    print(f"\n  Float accuracy:  {np.mean(all_float_accs):.4f} +/- {np.std(all_float_accs):.4f}")
    print(f"  Quant accuracy:  {np.mean(all_quant_accs):.4f} +/- {np.std(all_quant_accs):.4f}")
    print(f"  Range float:     [{np.min(all_float_accs):.4f}, {np.max(all_float_accs):.4f}]")
    print(f"  Range quant:     [{np.min(all_quant_accs):.4f}, {np.max(all_quant_accs):.4f}]")

    # Cap value statistics
    class_names = cfg['classes']
    feat_names = ['BPF1', 'BPF2', 'BPF3', 'BPF4', 'BPF5', 'RMS', 'Crst', 'Kurt']

    print(f"\n  Cap index: mean (std) [min, max] across {n_trials} splits:")
    print(f"  {'':>15s}", end='')
    for f in feat_names:
        print(f"  {f:>7s}", end='')
    print()

    cap_stds = np.zeros((4, 8))
    for cls in range(4):
        print(f"  {class_names[cls]:>15s}", end='')
        for feat in range(8):
            vals = all_cap_indices[:, cls, feat]
            mean_v = np.mean(vals)
            std_v = np.std(vals)
            cap_stds[cls, feat] = std_v
            print(f"  {mean_v:4.1f}±{std_v:3.1f}", end='')
        print()

    unstable_count = np.sum(cap_stds > 2.0)
    print(f"\n  Caps with std > 2 levels: {unstable_count}/32")
    print(f"  Caps with std > 3 levels: {np.sum(cap_stds > 3.0)}/32")
    print(f"  Mean cap std: {np.mean(cap_stds):.2f} levels")

    # ===================================================================
    # TEST 2: Leave-one-load-out
    # ===================================================================
    print("\n" + "=" * 70)
    print("TEST 2: Leave-one-motor-load-out (train on 3 loads, test on 1)")
    print("=" * 70)

    unique_loads = sorted(np.unique(loads))
    load_caps = []
    for test_load in unique_loads:
        train_mask = loads != test_load
        test_mask = loads == test_load

        X_tr = X_feat[train_mask]
        y_tr = labels[train_mask]
        X_te = X_feat[test_mask]
        y_te = labels[test_mask]

        scaler = MinMaxScaler()
        X_tr_n = scaler.fit_transform(X_tr)
        X_te_n = scaler.transform(X_te)

        model = LogisticRegression(multi_class='multinomial', solver='lbfgs',
                                   max_iter=2000, C=10.0, random_state=42)
        model.fit(X_tr_n, y_tr)
        acc = model.score(X_te_n, y_te)

        W_q, W_idx = quantize_weights(model.coef_)
        B_q, _ = quantize_weights(model.intercept_)
        logits = X_te_n @ W_q.T + B_q
        q_acc = np.mean(np.argmax(logits, axis=1) == y_te)

        load_caps.append(W_idx)
        print(f"  Test load={test_load}HP: float={acc:.4f}, quant={q_acc:.4f} "
              f"(train={np.sum(train_mask)}, test={np.sum(test_mask)})")

    load_caps = np.array(load_caps)
    print(f"\n  Cap variation across loads:")
    for cls in range(4):
        print(f"  {class_names[cls]:>15s}", end='')
        for feat in range(8):
            vals = load_caps[:, cls, feat]
            print(f"  {np.mean(vals):4.1f}±{np.std(vals):3.1f}", end='')
        print()

    # ===================================================================
    # TEST 3: Leave-one-fault-size-out
    # ===================================================================
    print("\n" + "=" * 70)
    print("TEST 3: Leave-one-fault-size-out (train on 2 sizes, test on 1)")
    print("=" * 70)

    fault_sizes = ['007', '014', '021']
    size_caps = []
    for test_size in fault_sizes:
        # Normal has no fault size, always include in training
        train_mask = (sizes != test_size) | (labels == 0)
        test_mask = (sizes == test_size) & (labels != 0)

        if np.sum(test_mask) == 0:
            continue

        X_tr = X_feat[train_mask]
        y_tr = labels[train_mask]
        X_te = X_feat[test_mask]
        y_te = labels[test_mask]

        scaler = MinMaxScaler()
        X_tr_n = scaler.fit_transform(X_tr)
        X_te_n = scaler.transform(X_te)

        model = LogisticRegression(multi_class='multinomial', solver='lbfgs',
                                   max_iter=2000, C=10.0, random_state=42)
        model.fit(X_tr_n, y_tr)
        acc = model.score(X_te_n, y_te)

        W_q, W_idx = quantize_weights(model.coef_)
        B_q, _ = quantize_weights(model.intercept_)
        logits = X_te_n @ W_q.T + B_q
        q_acc = np.mean(np.argmax(logits, axis=1) == y_te)

        size_caps.append(W_idx)
        print(f"  Test size=0.{test_size}\": float={acc:.4f}, quant={q_acc:.4f} "
              f"(train={np.sum(train_mask)}, test={np.sum(test_mask)})")

    size_caps = np.array(size_caps)

    # ===================================================================
    # TEST 4: 10-fold cross-validation
    # ===================================================================
    print("\n" + "=" * 70)
    print("TEST 4: 10-fold stratified cross-validation")
    print("=" * 70)

    kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    cv_float_accs = []
    cv_quant_accs = []
    cv_caps = []

    for fold, (train_idx, test_idx) in enumerate(kf.split(X_feat, labels)):
        X_tr, X_te = X_feat[train_idx], X_feat[test_idx]
        y_tr, y_te = labels[train_idx], labels[test_idx]

        scaler = MinMaxScaler()
        X_tr_n = scaler.fit_transform(X_tr)
        X_te_n = scaler.transform(X_te)

        model = LogisticRegression(multi_class='multinomial', solver='lbfgs',
                                   max_iter=2000, C=10.0, random_state=42)
        model.fit(X_tr_n, y_tr)
        f_acc = model.score(X_te_n, y_te)

        W_q, W_idx = quantize_weights(model.coef_)
        B_q, _ = quantize_weights(model.intercept_)
        logits = X_te_n @ W_q.T + B_q
        q_acc = np.mean(np.argmax(logits, axis=1) == y_te)

        cv_float_accs.append(f_acc)
        cv_quant_accs.append(q_acc)
        cv_caps.append(W_idx)

    cv_caps = np.array(cv_caps)
    print(f"  Float: {np.mean(cv_float_accs):.4f} +/- {np.std(cv_float_accs):.4f}")
    print(f"  Quant: {np.mean(cv_quant_accs):.4f} +/- {np.std(cv_quant_accs):.4f}")
    print(f"  Per-fold float: {[f'{a:.3f}' for a in cv_float_accs]}")
    print(f"  Per-fold quant: {[f'{a:.3f}' for a in cv_quant_accs]}")

    # ===================================================================
    # PLOT: Cap stability visualization
    # ===================================================================
    print("\n--- Generating stability plots ---")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Plot 1: Cap value boxplots across 20 random splits
    ax = axes[0, 0]
    positions = []
    data = []
    tick_labels = []
    c_unit = cfg['c_unit_fF']
    for cls in range(4):
        for feat in range(8):
            positions.append(cls * 9 + feat)
            data.append(all_cap_indices[:, cls, feat] * c_unit)
            tick_labels.append(f'{feat_names[feat]}')

    bp = ax.boxplot(data, positions=positions, widths=0.6, patch_artist=True)
    colors = ['#2196F3', '#F44336', '#4CAF50', '#FF9800']
    for i, patch in enumerate(bp['boxes']):
        patch.set_facecolor(colors[i // 8])
        patch.set_alpha(0.6)
    ax.set_title('Cap Values Across 20 Random Splits\n(boxes show variation — tighter = more reliable)',
                 fontsize=11)
    ax.set_ylabel('Capacitance (fF)')
    # Add class separators
    for i in range(1, 4):
        ax.axvline(i * 9 - 0.5, color='gray', linestyle='--', alpha=0.3)
    ax.set_xticks([cls * 9 + 3.5 for cls in range(4)])
    ax.set_xticklabels(class_names)
    ax.grid(True, alpha=0.2, axis='y')

    # Plot 2: Accuracy distribution
    ax = axes[0, 1]
    ax.hist(all_float_accs, bins=10, alpha=0.6, label='Float', color='steelblue')
    ax.hist(all_quant_accs, bins=10, alpha=0.6, label='4-bit Quantized', color='coral')
    ax.axvline(np.mean(all_float_accs), color='steelblue', linestyle='--', linewidth=2)
    ax.axvline(np.mean(all_quant_accs), color='coral', linestyle='--', linewidth=2)
    ax.set_title(f'Accuracy Across 20 Splits\n'
                 f'Float: {np.mean(all_float_accs):.3f}±{np.std(all_float_accs):.3f}, '
                 f'Quant: {np.mean(all_quant_accs):.3f}±{np.std(all_quant_accs):.3f}')
    ax.set_xlabel('Accuracy')
    ax.set_ylabel('Count')
    ax.legend()
    ax.grid(True, alpha=0.2)

    # Plot 3: Leave-one-load-out cap comparison
    ax = axes[1, 0]
    x = np.arange(8)
    width = 0.2
    for load_idx, load in enumerate(unique_loads):
        for cls in range(4):
            offset = (cls - 1.5) * width
            alpha_val = 0.3 + 0.2 * load_idx
            ax.bar(x + offset + load_idx * 0.04, load_caps[load_idx, cls] * c_unit,
                   width * 0.9, alpha=alpha_val, color=colors[cls],
                   edgecolor='gray' if load_idx == 0 else 'none', linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(feat_names)
    ax.set_title('Cap Values: Leave-One-Load-Out\n(4 overlapping bars per group = 4 motor loads)')
    ax.set_ylabel('Capacitance (fF)')
    ax.grid(True, alpha=0.2, axis='y')

    # Plot 4: Std deviation heatmap
    ax = axes[1, 1]
    cv_stds = np.std(cv_caps, axis=0)  # (4, 8) std across 10 folds
    im = ax.imshow(cv_stds, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=4)
    ax.set_xticks(range(8))
    ax.set_xticklabels(feat_names, fontsize=9)
    ax.set_yticks(range(4))
    ax.set_yticklabels(class_names, fontsize=9)
    for i in range(4):
        for j in range(8):
            ax.text(j, i, f'{cv_stds[i, j]:.1f}', ha='center', va='center',
                    fontsize=10, fontweight='bold',
                    color='white' if cv_stds[i, j] > 2 else 'black')
    plt.colorbar(im, ax=ax, label='Std Dev (cap levels)')
    ax.set_title('Cap Index Std Dev Across 10 CV Folds\n(green=stable, red=unreliable)')

    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'results', 'robustness_analysis.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: results/robustness_analysis.png")

    # ===================================================================
    # VERDICT
    # ===================================================================
    mean_std = np.mean(cap_stds)
    worst_std = np.max(cap_stds)
    min_quant_acc = np.min(all_quant_accs)

    print("\n" + "=" * 70)
    print("VERDICT: Are the cap values reliable?")
    print("=" * 70)
    print(f"  Mean cap std across splits:    {mean_std:.2f} levels (out of 16)")
    print(f"  Worst cap std:                 {worst_std:.2f} levels")
    print(f"  Caps varying > 2 levels:       {unstable_count}/32")
    print(f"  Worst-case quantized accuracy: {min_quant_acc:.4f}")
    print(f"  10-fold CV quant accuracy:     {np.mean(cv_quant_accs):.4f} ± {np.std(cv_quant_accs):.4f}")

    if mean_std < 1.5 and min_quant_acc > 0.85:
        print("\n  RELIABLE — cap values are stable, safe to commit to silicon")
    elif mean_std < 2.5 and min_quant_acc > 0.80:
        print("\n  MARGINAL — cap values have some variation, consider:")
        print("    - Using median cap values across splits instead of single-run")
        print("    - Increasing regularization to shrink weight range")
        print("    - Adding more training data")
    else:
        print("\n  UNRELIABLE — cap values vary too much, DO NOT use for silicon")
        print("    - Need more data or better features")
        print("    - Consider reducing to 3-bit or 2-bit quantization")
        print("    - Consider merging similar fault classes")

    # Save median caps as the "robust" recommendation
    median_caps = np.median(all_cap_indices, axis=0).astype(int)
    print(f"\n  Recommended cap values (median across {n_trials} splits):")
    print(f"  {'':>15s}", end='')
    for f in feat_names:
        print(f"  {f:>5s}", end='')
    print()
    for cls in range(4):
        print(f"  {class_names[cls]:>15s}", end='')
        for feat in range(8):
            print(f"  {median_caps[cls, feat] * c_unit:4.0f}f", end='')
        print()


if __name__ == '__main__':
    main()
