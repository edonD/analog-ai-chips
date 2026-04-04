#!/usr/bin/env python3
"""Expert 5: Classifier Weight Mapping Analysis"""

import os
import json
import numpy as np

REPORT = os.path.join(os.path.dirname(__file__), 'expert_05_classifier_weights.md')
VIBROSENSE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS = os.path.join(VIBROSENSE, '10_fullchain/results')

def main():
    lines = []
    L = lines.append

    L("# Expert Report 05: Classifier Weight Mapping Analysis")
    L("")
    L("## 1. Classifier Architecture")
    L("")
    L("The behavioral classifier computes:")
    L("```")
    L("Score[k] = sum_i( w[k][i] * V(in_i) / 1.8 ) + bias[k]")
    L("class_out = argmax(Score[k]) encoded as voltage")
    L("```")
    L("")
    L("Key: inputs are divided by 1.8V, so the model expects features in [0, 1.8V].")
    L("")

    L("## 2. Training Pipeline Feature Normalization")
    L("")
    L("From `train.py`:")
    L("1. Raw features extracted (band envelope energies, RMS, crest, kurtosis)")
    L("2. `MinMaxScaler` normalizes features to [0, 1]")
    L("3. Logistic regression trains on [0, 1] features")
    L("4. SPICE export scales features as `voltage = feature * 1.8V`")
    L("5. SPICE classifier divides by 1.8V to recover [0, 1] features")
    L("")
    L("So: training features [0, 1] <-> SPICE voltages [0, 1.8V]")
    L("")

    # Load trained weights
    tw_path = os.path.join(VIBROSENSE, '09_training/results/trained_weights.json')
    if os.path.exists(tw_path):
        with open(tw_path) as f:
            tw = json.load(f)

        L("## 3. Trained Weight Values")
        L("")
        L("### Quantized Weights (as used in SPICE)")
        L("")
        L("| Feature | Normal | Inner Race | Ball | Outer Race |")
        L("|---------|--------|------------|------|------------|")
        feat_names = ['BPF1 env', 'BPF2 env', 'BPF3 env', 'BPF4 env', 'BPF5 env',
                      'RMS', 'Crest', 'Kurtosis']
        qw = tw['quantized_weights']
        for i in range(8):
            vals = [qw[c][i] for c in range(4)]
            L(f"| {feat_names[i]:9s} | {vals[0]:+.2f} | {vals[1]:+.2f} | {vals[2]:+.2f} | {vals[3]:+.2f} |")
        L("")
        L("### Biases")
        qb = tw['quantized_biases']
        L(f"Normal: {qb[0]:+.3f}, Inner: {qb[1]:+.3f}, Ball: {qb[2]:+.3f}, Outer: {qb[3]:+.3f}")
        L("")

    L("## 4. The Normalization Mismatch")
    L("")
    L("### What training expects (from MinMaxScaler)")
    L("")
    L("The scaler maps: `feature_norm = (feature_raw - min) / (max - min)`")
    L("Then voltage = feature_norm * 1.8V")
    L("")
    L("For the classifier to work, each feature voltage should span [0, 1.8V]")
    L("across the training dataset. Different classes should produce")
    L("DIFFERENT voltage patterns across the 8 features.")
    L("")

    L("### What the analog chain actually produces")
    L("")
    L("From full-chain simulation:")
    L("")
    L("| Feature   | Actual Range (V) | Normalized Range (V/1.8) | Training Expected |")
    L("|-----------|-----------------|-------------------------|-------------------|")

    analysis_path = os.path.join(RESULTS, 'fullchain_analysis.json')
    if os.path.exists(analysis_path):
        with open(analysis_path) as f:
            analysis = json.load(f)

        for ch in range(1, 6):
            vals = [analysis[tc][f'env{ch}_mean'] for tc in ['normal', 'inner_race', 'outer_race', 'ball']]
            vmin, vmax = min(vals), max(vals)
            nmin, nmax = vmin/1.8, vmax/1.8
            L(f"| ENV{ch}     | {vmin:.4f}-{vmax:.4f} | {nmin:.4f}-{nmax:.4f} | 0.000-1.000 |")

        # RMS
        rms_vals = [analysis[tc]['rms_out_mean'] for tc in ['normal', 'inner_race', 'outer_race', 'ball']]
        L(f"| RMS       | {min(rms_vals):.4f}-{max(rms_vals):.4f} | {min(rms_vals)/1.8:.4f}-{max(rms_vals)/1.8:.4f} | 0.000-1.000 |")

        peak_vals = [analysis[tc]['peak_out_mean'] for tc in ['normal', 'inner_race', 'outer_race', 'ball']]
        L(f"| Peak      | {min(peak_vals):.4f}-{max(peak_vals):.4f} | {min(peak_vals)/1.8:.4f}-{max(peak_vals)/1.8:.4f} | 0.000-1.000 |")
        L("")

    L("### The Gap")
    L("")
    L("- **Envelope features**: actual range ~0.501-0.505 (normalized), training expects 0.0-1.0")
    L("- **RMS feature**: actual ~0.870 (normalized), training expects 0.0-1.0")
    L("- **Peak feature**: actual ~0.563-0.630 (normalized), training expects 0.0-1.0")
    L("")
    L("The envelope features are **compressed into a ~0.004 normalized range** when")
    L("the classifier was trained for a 1.0 range. This is a **250x mismatch**.")
    L("")

    L("## 5. Score Sensitivity Analysis")
    L("")
    L("How much does a 1 mV envelope change affect classifier scores?")
    L("")
    L("A 1 mV change in input voltage -> delta_score = weight * 0.001 / 1.8")
    L("")
    L("For the most sensitive weight (outer_race, BPF5): w = 18.231")
    L("- delta_score = 18.231 * 0.001 / 1.8 = 0.0101 per mV")
    L("")
    L("To flip a classification, we typically need delta_score ~ 1.0")
    L("- Required: ~100 mV envelope change on the highest-weighted feature")
    L("- Available: ~7 mV maximum across all channels")
    L("")
    L("**The signal is 14x too small to change the classification.**")
    L("")

    L("## 6. Weight Rescaling Solution")
    L("")
    L("### Approach: Adjust weights and biases to work with actual voltage range")
    L("")
    L("Instead of: `Score = sum(w * V/1.8) + bias`")
    L("")
    L("Use: `Score = sum(w' * (V - 0.9) / 0.01) + bias'`")
    L("")
    L("This centers features at VCM (0.9V) and normalizes by ~10 mV range.")
    L("")
    L("The weight transformation:")
    L("- `w' = w * 0.01 / 1.8` (scale down by normalization factor)")
    L("- `bias' = original_bias + sum(w * 0.9/1.8)` (absorb DC offset)")
    L("")
    L("But this LOSES the training discrimination because the original weights")
    L("were trained for a different feature distribution.")
    L("")
    L("### Better Approach: Retrain with Correct Feature Range")
    L("")
    L("1. Run analog simulation for all 4 cases")
    L("2. Extract actual envelope voltages per channel")
    L("3. Use these as training features (not MinMax normalized)")
    L("4. Train classifier on actual voltage values")
    L("5. Export weights that expect inputs at ~0.9V +/- 10 mV")
    L("")
    L("The classifier weights would be ~100x larger to compensate for")
    L("the smaller input range, but the VCVS behavioral model can handle this.")
    L("")

    L("## 7. Why Inner Race Still Works")
    L("")
    L("Inner race is the ONE test case that classifies correctly. Why?")
    L("")
    L("Inner race has the largest envelope activity in channels 3-5:")
    L("- ENV3: 9.7 mV above VCM (vs 3.2 mV for normal)")
    L("- ENV4: 8.5 mV above VCM (vs 1.9 mV for normal)")
    L("- ENV5: 6.4 mV above VCM (vs 1.5 mV for normal)")
    L("")
    L("Class 1 (Inner Race) has large positive weights on ENV3 (+14.002)")
    L("and ENV2 (+5.545). The slightly larger ENV3 value tips the score.")
    L("The margin is tiny -- the classifier barely picks inner race over")
    L("outer race (0.45V output, sometimes flipping to 1.35V).")
    L("")

    L("## 8. Recommendations")
    L("")
    L("1. **Retrain classifier for actual analog feature range** (highest impact)")
    L("2. **Increase stimulus amplitude** to widen envelope spread")
    L("3. **Add post-envelope gain** to amplify mV offsets to hundreds of mV")
    L("4. **Fix BPF bias** so channels 4/5 actually separate frequencies correctly")
    L("")
    L("The weight rescaling alone (without retraining) will NOT work because")
    L("the feature DISTRIBUTION changes when you move from [0,1] normalized")
    L("to [0.900, 0.910] analog. The inter-class separations are different.")

    with open(REPORT, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Expert 05 report written to {REPORT}")

if __name__ == '__main__':
    main()
