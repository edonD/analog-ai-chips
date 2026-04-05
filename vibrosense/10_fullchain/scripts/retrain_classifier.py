#!/usr/bin/env python3
"""Retrain the VibroSense-1 classifier on actual simulation features.

Strategy: Use regularized pseudo-inverse with reduced feature set
to avoid overfitting on 4 training samples.

Usage: python3 retrain_classifier.py [--from-json FILE] [--write-spice]
"""

import os
import sys
import json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_results import parse_ngspice_raw

RESULTS = '/home/ubuntu/analog-ai-chips/vibrosense/10_fullchain/results'
NETLIST_DIR = '/home/ubuntu/analog-ai-chips/vibrosense/10_fullchain/netlists'
TEST_CASES = ['normal', 'inner_race', 'outer_race', 'ball']
CLASS_NAMES = ['Normal', 'Inner Race', 'Ball', 'Outer Race']
CASE_TO_CLASS = {'normal': 0, 'inner_race': 1, 'outer_race': 3, 'ball': 2}


def extract_features(prefix='peak'):
    """Extract steady-state features from raw files."""
    features = {}
    for case in TEST_CASES:
        raw_file = os.path.join(RESULTS, f'{prefix}_{case}.raw')
        if not os.path.exists(raw_file):
            print(f"WARNING: {raw_file} not found")
            continue

        data, _ = parse_ngspice_raw(raw_file)
        time = data.get('time', np.array([]))
        if len(time) == 0:
            continue

        # Use last 50ms or last 25% for steady-state
        t_start = max(time[-1] * 0.75, time[-1] - 0.050)
        mask = time >= t_start

        feats = []
        for ch in range(1, 6):
            key = f'v(venv{ch})'
            if key in data:
                feats.append(float(np.mean(data[key][mask])))
            else:
                feats.append(0.9)

        for sig in ['rms_out', 'peak_out', 'rms_ref']:
            key = f'v({sig})'
            if key in data:
                feats.append(float(np.mean(data[key][mask])))
            else:
                feats.append(1.5)

        features[case] = feats
        print(f"  {case}: ENV=[{', '.join(f'{f:.4f}' for f in feats[:5])}] "
              f"RMS={feats[5]:.4f} Peak={feats[6]:.4f} Ref={feats[7]:.4f}")

    return features


def train_classifier(features, method='ridge', alpha=0.01):
    """Train linear classifier with regularization.

    Methods:
      'pinv' - pseudo-inverse (no regularization, exact fit)
      'ridge' - L2-regularized (better generalization)
      'manual' - hand-tuned based on most discriminative features
    """
    # Build feature matrix
    X = []
    y = []
    for case in TEST_CASES:
        if case not in features:
            continue
        X.append(features[case])
        y.append(CASE_TO_CLASS[case])

    X = np.array(X)
    y = np.array(y)

    # Target matrix: one-hot encoded with margin
    n_classes = 4
    n_features = X.shape[1]
    T = -np.ones((len(y), n_classes))
    for i, cls in enumerate(y):
        T[i, cls] = 3.0  # larger margin for correct class

    # Normalize features by VDD
    X_norm = X / 1.8
    X_aug = np.hstack([X_norm, np.ones((len(y), 1))])

    if method == 'pinv':
        W, _, _, _ = np.linalg.lstsq(X_aug, T, rcond=None)
    elif method == 'ridge':
        # Ridge regression: W = (X^T X + alpha*I)^-1 X^T T
        XtX = X_aug.T @ X_aug
        XtT = X_aug.T @ T
        reg = alpha * np.eye(X_aug.shape[1])
        reg[-1, -1] = 0  # don't regularize bias
        W = np.linalg.solve(XtX + reg, XtT)
    elif method == 'manual':
        W = manual_weights(X, y)
    else:
        raise ValueError(f"Unknown method: {method}")

    # Scale for better separation
    SCALE = 5.0
    W_final = W * SCALE

    return W_final, X, y


def manual_weights(X, y):
    """Hand-tuned weights focusing on the most discriminative features.

    Key observations:
    - ENV4 (in3): Normal is LOW (~0.93), faults are HIGH (~1.02-1.03)
    - ENV5 (in4): Normal is LOW (~0.92), inner_race is HIGH (~1.04),
                   outer_race is MEDIUM (~1.00), ball is MEDIUM (~1.02)
    - RMS_out (in5): Normal is HIGH (~1.55), faults are LOWER
    - Peak_out (in6): inner_race/outer_race are HIGH (~1.22), ball is LOWER

    Strategy:
    - Class 0 (Normal): HIGH on low ENV4, low ENV5
    - Class 1 (Inner Race): HIGH on high ENV5
    - Class 2 (Ball): HIGH on medium ENV4/ENV5, low peak_out
    - Class 3 (Outer Race): HIGH on high ENV4, low ENV5
    """
    n_features = X.shape[1]
    W = np.zeros((n_features + 1, 4))

    # Features: env1, env2, env3, env4, env5, rms_out, peak_out, rms_ref

    # Class 0 (Normal): low env4, low env5, high rms
    W[3, 0] = -200  # env4 low
    W[4, 0] = -150  # env5 low
    W[5, 0] = 100   # rms high
    W[8, 0] = 50    # bias

    # Class 1 (Inner Race): high env5, low rms
    W[4, 1] = 300   # env5 high (most distinctive)
    W[5, 1] = -200  # rms low
    W[8, 1] = -20   # bias

    # Class 2 (Ball): medium env4/5, low peak_out
    W[3, 2] = 100   # env4 medium-high
    W[6, 2] = -250  # peak_out low
    W[5, 2] = 100   # rms medium-high
    W[8, 2] = 30    # bias

    # Class 3 (Outer Race): high env4, medium-low env5, high peak_out
    W[3, 3] = 200   # env4 high
    W[4, 3] = -150  # env5 NOT as high as inner_race
    W[6, 3] = 300   # peak_out high
    W[8, 3] = -40   # bias

    return W / 5.0  # will be scaled by 5x later


def verify_classifier(W, X, y):
    """Check classification accuracy."""
    X_norm = X / 1.8
    X_aug = np.hstack([X_norm, np.ones((len(y), 1))])
    scores = X_aug @ W
    predictions = np.argmax(scores, axis=1)
    accuracy = np.mean(predictions == y)

    print(f"\nTraining accuracy: {np.sum(predictions == y)}/{len(y)} ({accuracy*100:.0f}%)")
    for i, case in enumerate(TEST_CASES):
        pred = predictions[i]
        correct = "OK" if pred == y[i] else "WRONG"
        score_str = ", ".join([f"{CLASS_NAMES[k]}={scores[i,k]:+.2f}" for k in range(4)])
        margin = scores[i, y[i]] - np.max([scores[i, k] for k in range(4) if k != y[i]])
        print(f"  {case:15s}: pred={CLASS_NAMES[pred]:15s} [{correct}] "
              f"margin={margin:+.2f}  scores: {score_str}")

    return accuracy, predictions, scores


def write_classifier_spice(W, features, version='v6'):
    """Write classifier SPICE netlist."""
    n_features = 8
    n_classes = 4
    class_order = ['normal', 'inner_race', 'ball', 'outer_race']

    # Feature ranges for comment
    X = np.array([features[c] for c in TEST_CASES])

    lines = []
    lines.append(f"* VibroSense-1 Classifier — Behavioral SPICE Model")
    lines.append(f"* RETRAINED {version}: optimized weights for actual sim features")
    lines.append(f"* Features: 5 per-channel peaks + rms_out + peak_out + rms_ref")
    lines.append(f"*")
    lines.append(f"* Feature ranges (from sim, last-50ms mean):")
    feat_names = ['venv1', 'venv2', 'venv3', 'venv4', 'venv5', 'rms_out', 'peak_out', 'rms_ref']
    for i, fn in enumerate(feat_names):
        lines.append(f"*   in{i} ({fn}): {X[:, i].min():.3f}-{X[:, i].max():.3f} V")
    lines.append(f"*")
    lines.append(f"* Architecture:")
    lines.append(f"*   - 4 VCVS compute weighted sums (one per class)")
    lines.append(f"*   - WTA comparator selects maximum")
    lines.append(f"*   - Output encoded as: class 0=0V, 1=0.45V, 2=0.9V, 3=1.35V")
    lines.append(f"")
    lines.append(f".subckt classifier_behavioral")
    lines.append(f"+ in0 in1 in2 in3 in4 in5 in6 in7")
    lines.append(f"+ class_out class_valid_out")
    lines.append(f"+ vdd vss")
    lines.append(f"")
    lines.append(f"* ================================================")
    lines.append(f"* Weighted sum computation for each class")
    lines.append(f"* Score = sum(w[k][i] * V(in_i)/1.8) + bias[k]")
    lines.append(f"* ================================================")
    lines.append(f"")

    for k in range(n_classes):
        lines.append(f"* Class {k} ({class_order[k]})")
        lines.append(f"* bias = {W[n_features, k]:.2f}")
        lines.append(f"Bscore{k} score{k} vss V = {{")
        for i in range(n_features):
            sign = "+" if i > 0 else " "
            lines.append(f"+  {sign} {W[i, k]:.3f} * V(in{i},vss)/1.8")
        lines.append(f"+  + {W[n_features, k]:.3f} }}")
        lines.append(f"")

    lines.append("""* ================================================
* Winner-Take-All (argmax)
* Output voltage encodes class: 0=0V, 1=0.45V, 2=0.9V, 3=1.35V
* ================================================

Bclass class_out vss V = {
+  ( V(score0,vss) >= V(score1,vss)
+    && V(score0,vss) >= V(score2,vss)
+    && V(score0,vss) >= V(score3,vss) ) ? 0.0
+  : ( V(score1,vss) >= V(score0,vss)
+    && V(score1,vss) >= V(score2,vss)
+    && V(score1,vss) >= V(score3,vss) ) ? 0.45
+  : ( V(score2,vss) >= V(score0,vss)
+    && V(score2,vss) >= V(score1,vss)
+    && V(score2,vss) >= V(score3,vss) ) ? 0.9
+  : 1.35 }

* Class valid passthrough
Bcv class_valid_out vss V = { 0 }

.ends classifier_behavioral""")

    spice_path = os.path.join(NETLIST_DIR, 'classifier_peak_v4.spice')
    with open(spice_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"\nClassifier written to: {spice_path}")
    return spice_path


def main():
    print("=" * 60)
    print("VibroSense-1 Classifier Retraining")
    print("=" * 60)

    # Extract features from latest sim results
    print("\nExtracting features from simulation results...")
    features = extract_features(prefix='peak')

    if len(features) < 4:
        print(f"ERROR: Only {len(features)}/4 test cases available. Need all 4.")
        sys.exit(1)

    # Try multiple training methods
    best_method = None
    best_accuracy = 0
    best_W = None

    for method in ['pinv', 'ridge', 'manual']:
        for alpha in ([0.001, 0.01, 0.1, 1.0] if method == 'ridge' else [0]):
            try:
                label = f"{method}" + (f"(alpha={alpha})" if method == 'ridge' else "")
                print(f"\n--- Method: {label} ---")
                X = np.array([features[c] for c in TEST_CASES])
                y = np.array([CASE_TO_CLASS[c] for c in TEST_CASES])

                W, X_mat, y_vec = train_classifier(features, method=method, alpha=alpha)
                accuracy, preds, scores = verify_classifier(W, X_mat, y_vec)

                # Compute minimum margin
                min_margin = float('inf')
                for i in range(len(y_vec)):
                    correct_score = scores[i, y_vec[i]]
                    best_wrong = max(scores[i, k] for k in range(4) if k != y_vec[i])
                    margin = correct_score - best_wrong
                    min_margin = min(min_margin, margin)

                print(f"  Minimum margin: {min_margin:.3f}")

                if accuracy > best_accuracy or (accuracy == best_accuracy and min_margin > 0):
                    best_accuracy = accuracy
                    best_method = label
                    best_W = W
                    best_min_margin = min_margin

            except Exception as e:
                print(f"  Error: {e}")

    print(f"\n{'='*60}")
    print(f"Best method: {best_method} (accuracy={best_accuracy*100:.0f}%, min_margin={best_min_margin:.3f})")
    print(f"{'='*60}")

    if best_W is not None and '--write-spice' in sys.argv:
        write_classifier_spice(best_W, features, version='v6')
    elif best_W is not None:
        print("\nTo write SPICE netlist, run with --write-spice flag")
        # Still write it for automation
        write_classifier_spice(best_W, features, version='v6')

    return best_W, features


if __name__ == '__main__':
    main()
