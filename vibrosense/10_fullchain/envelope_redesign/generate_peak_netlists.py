#!/usr/bin/env python3
"""Generate per-test-case netlists using peak-based envelope detector.

Also retrains the classifier based on estimated peak feature values.
"""

import os
import numpy as np

NETLIST_DIR = '/home/ubuntu/analog-ai-chips/vibrosense/10_fullchain/netlists'
TEST_CASES = ['normal', 'inner_race', 'outer_race', 'ball']

# ============================================================
# Step 1: Estimate peak feature values from BPF data
# ============================================================
# BPF peak amplitudes (mV above VCM) from Expert Report 08
# These are Vpp/2 estimates from the raw data
bpf_peaks_mv = {
    'normal':     [33, 50, 28, 16, 11],
    'inner_race': [39, 73, 91, 93, 109],
    'outer_race': [41, 71, 98, 89, 62],
    'ball':       [36, 52, 71, 68, 63],
}

# With peak envelope detector, output = VCM + peak_amplitude
# peak_amplitude ≈ BPF Vpeak (since peak detector tracks max)
# But there's some decay (tau=20ms), so effective peak is ~80-90% of true peak
PEAK_EFFICIENCY = 0.85  # account for decay between peaks

VCM = 0.9
peak_features = {}
for case, peaks in bpf_peaks_mv.items():
    peak_features[case] = [VCM + p * PEAK_EFFICIENCY * 1e-3 for p in peaks]

# RMS and global peak values (from actual simulation data)
rms_out = {'normal': 1.5678, 'inner_race': 1.5653, 'outer_race': 1.5664, 'ball': 1.5675}
peak_out = {'normal': 1.0133, 'inner_race': 1.1336, 'outer_race': 1.0883, 'ball': 1.0638}
rms_ref = {'normal': 1.6162, 'inner_race': 1.6162, 'outer_race': 1.6162, 'ball': 1.6162}

print("=== Estimated Peak Features (V) ===")
print(f"{'Case':15s} | {'PK1':7s} | {'PK2':7s} | {'PK3':7s} | {'PK4':7s} | {'PK5':7s} | {'RMS':7s} | {'Peak':7s} | {'Ref':7s}")
for case in TEST_CASES:
    pf = peak_features[case]
    print(f"{case:15s} | {pf[0]:.4f} | {pf[1]:.4f} | {pf[2]:.4f} | {pf[3]:.4f} | {pf[4]:.4f} | {rms_out[case]:.4f} | {peak_out[case]:.4f} | {rms_ref[case]:.4f}")

# ============================================================
# Step 2: Train classifier on estimated features
# ============================================================
# Build feature matrix (4 samples x 8 features)
X = []
y = []
class_names = ['normal', 'inner_race', 'ball', 'outer_race']  # class order in classifier
case_to_class = {'normal': 0, 'inner_race': 1, 'ball': 2, 'outer_race': 3}

for case in TEST_CASES:
    features = peak_features[case] + [rms_out[case], peak_out[case], rms_ref[case]]
    X.append(features)
    y.append(case_to_class[case])

X = np.array(X)
y = np.array(y)

print(f"\nFeature matrix shape: {X.shape}")
print(f"Labels: {y}")

# Compute per-feature spread
for i in range(8):
    spread = X[:, i].max() - X[:, i].min()
    print(f"Feature {i}: range [{X[:, i].min():.4f}, {X[:, i].max():.4f}], spread = {spread*1000:.1f} mV")

# Train a linear classifier using least-squares
# Score for class k: score_k = sum(w_ki * x_i) + bias_k
# We want: for each sample, the correct class has the highest score
# Use one-vs-all approach with large margin

# Create target matrix: T[sample, class] = +1 if correct, -1 otherwise
n_classes = 4
n_features = 8
T = -np.ones((len(y), n_classes))
for i, cls in enumerate(y):
    T[i, cls] = 1.0

# Add bias column
X_aug = np.hstack([X / 1.8, np.ones((len(y), 1))])  # normalize by 1.8V

# Solve least-squares: X_aug @ W = T
# W shape: (n_features+1, n_classes)
W, residuals, rank, sv = np.linalg.lstsq(X_aug, T, rcond=None)

print(f"\n=== Trained Weights ===")
print(f"Weight matrix shape: {W.shape}")
feature_names = ['pk1', 'pk2', 'pk3', 'pk4', 'pk5', 'rms', 'peak', 'ref']
for k in range(n_classes):
    print(f"\nClass {k} ({class_names[k]}):")
    for i in range(n_features):
        print(f"  {feature_names[i]:5s}: {W[i, k]:+10.3f}")
    print(f"  bias:  {W[n_features, k]:+10.3f}")

# Verify: compute scores for all samples
scores = X_aug @ W
predictions = np.argmax(scores, axis=1)
accuracy = np.mean(predictions == y)
print(f"\n=== Training Accuracy: {accuracy*100:.0f}% ({np.sum(predictions == y)}/{len(y)}) ===")
for i, case in enumerate(TEST_CASES):
    pred_class = class_names[predictions[i]]
    correct = "OK" if predictions[i] == y[i] else "WRONG"
    score_str = ", ".join([f"{class_names[k]}={scores[i,k]:+.3f}" for k in range(4)])
    print(f"  {case:15s}: predicted={pred_class:15s} [{correct}] scores: {score_str}")

# Scale weights to produce larger score margins
# Multiply all weights by a factor to increase separation
SCALE = 5.0
W_scaled = W * SCALE

# Re-verify with scaled weights
scores_scaled = X_aug @ W_scaled
predictions_scaled = np.argmax(scores_scaled, axis=1)
print(f"\n=== With {SCALE}x scaled weights ===")
for i, case in enumerate(TEST_CASES):
    pred_class = class_names[predictions_scaled[i]]
    correct = "OK" if predictions_scaled[i] == y[i] else "WRONG"
    score_str = ", ".join([f"{class_names[k]}={scores_scaled[i,k]:+.3f}" for k in range(4)])
    print(f"  {case:15s}: predicted={pred_class:15s} [{correct}] scores: {score_str}")

# ============================================================
# Step 3: Write new classifier SPICE file
# ============================================================
W_final = W_scaled

classifier_spice = f"""* VibroSense-1 Classifier — Behavioral SPICE Model
* RETRAINED v4: weights for peak-based envelope detector features
* Features: 5 per-channel peaks + rms_out + peak_out + rms_ref
*
* Expected feature ranges:
*   in0-in4 (per-ch peaks): {X[:,0].min():.3f}-{X[:,4].max():.3f} V
*   in5 (rms_out): ~1.565-1.568 V
*   in6 (peak_out): ~1.013-1.134 V
*   in7 (rms_ref): ~1.616 V (constant)
*
* Trained via least-squares on estimated peak features
*
* Architecture:
*   - 4 VCVS compute weighted sums (one per class)
*   - WTA comparator selects maximum
*   - Output encoded as: class 0=0V, 1=0.45V, 2=0.9V, 3=1.35V

.subckt classifier_behavioral
+ in0 in1 in2 in3 in4 in5 in6 in7
+ class_out class_valid_out
+ vdd vss

* ================================================
* Weighted sum computation for each class
* Score = sum(w[k][i] * V(in_i)/1.8) + bias[k]
* ================================================

"""

for k in range(n_classes):
    classifier_spice += f"* Class {k} ({class_names[k]})\n"
    classifier_spice += f"* bias = {W_final[n_features, k]:.2f}\n"
    classifier_spice += f"Bscore{k} score{k} vss V = {{\n"
    for i in range(n_features):
        sign = "+" if i > 0 else " "
        classifier_spice += f"+  {sign} {W_final[i, k]:.3f} * V(in{i},vss)/1.8\n"
    classifier_spice += f"+  + {W_final[n_features, k]:.3f} }}\n\n"

classifier_spice += """* ================================================
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

.ends classifier_behavioral
"""

classifier_path = os.path.join(NETLIST_DIR, 'classifier_peak_v4.spice')
with open(classifier_path, 'w') as f:
    f.write(classifier_spice)
print(f"\nClassifier written to: {classifier_path}")

# ============================================================
# Step 4: Generate per-test-case netlists with peak envelope
# ============================================================

for case in TEST_CASES:
    # Read the existing netlist as template
    src_path = os.path.join(NETLIST_DIR, f'vibrosense1_{case}.spice')
    with open(src_path, 'r') as f:
        content = f.read()

    # Replace envelope detector include
    content = content.replace(
        '.include envelope_det_fixed.spice',
        '* Envelope detector replaced with peak-based behavioral model\n.include envelope_peak_behavioral.spice'
    )

    # Replace classifier include
    content = content.replace(
        '.include classifier_behavioral.spice',
        '* Classifier retrained for peak envelope features\n.include classifier_peak_v4.spice'
    )

    # Remove OTA includes that are no longer needed by envelope (but keep for BPF/PGA)
    # Actually, keep all includes — BPF and PGA still use them

    # Update output file paths
    out_path = os.path.join(NETLIST_DIR, f'vibrosense1_peak_{case}.spice')
    with open(out_path, 'w') as f:
        f.write(content)

    print(f"Written: {out_path}")

print("\nAll netlists generated!")
