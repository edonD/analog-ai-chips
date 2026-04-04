# Expert Report 05: Classifier Weight Mapping Analysis

## 1. Classifier Architecture

The behavioral classifier computes:
```
Score[k] = sum_i( w[k][i] * V(in_i) / 1.8 ) + bias[k]
class_out = argmax(Score[k]) encoded as voltage
```

Key: inputs are divided by 1.8V, so the model expects features in [0, 1.8V].

## 2. Training Pipeline Feature Normalization

From `train.py`:
1. Raw features extracted (band envelope energies, RMS, crest, kurtosis)
2. `MinMaxScaler` normalizes features to [0, 1]
3. Logistic regression trains on [0, 1] features
4. SPICE export scales features as `voltage = feature * 1.8V`
5. SPICE classifier divides by 1.8V to recover [0, 1] features

So: training features [0, 1] <-> SPICE voltages [0, 1.8V]

## 3. Trained Weight Values

### Quantized Weights (as used in SPICE)

| Feature | Normal | Inner Race | Ball | Outer Race |
|---------|--------|------------|------|------------|
| BPF1 env  | +5.55 | -7.14 | -0.80 | +3.43 |
| BPF2 env  | +1.32 | +5.55 | -2.91 | -2.91 |
| BPF3 env  | -5.03 | +14.00 | +5.55 | -13.48 |
| BPF4 env  | -9.25 | -0.80 | +9.77 | +1.32 |
| BPF5 env  | -11.37 | +1.32 | -9.25 | +18.23 |
| RMS       | -5.03 | -2.91 | -2.91 | +9.77 |
| Crest     | -7.14 | +3.43 | +3.43 | -0.80 |
| Kurtosis  | -0.80 | +5.55 | -5.03 | -0.80 |

### Biases
Normal: +3.600, Inner: -2.798, Ball: +1.467, Outer: -2.372

## 4. The Normalization Mismatch

### What training expects (from MinMaxScaler)

The scaler maps: `feature_norm = (feature_raw - min) / (max - min)`
Then voltage = feature_norm * 1.8V

For the classifier to work, each feature voltage should span [0, 1.8V]
across the training dataset. Different classes should produce
DIFFERENT voltage patterns across the 8 features.

### What the analog chain actually produces

From full-chain simulation:

| Feature   | Actual Range (V) | Normalized Range (V/1.8) | Training Expected |
|-----------|-----------------|-------------------------|-------------------|
| ENV1     | 0.9041-0.9044 | 0.5023-0.5025 | 0.000-1.000 |
| ENV2     | 0.9064-0.9088 | 0.5036-0.5049 | 0.000-1.000 |
| ENV3     | 0.9032-0.9097 | 0.5018-0.5054 | 0.000-1.000 |
| ENV4     | 0.9019-0.9085 | 0.5011-0.5047 | 0.000-1.000 |
| ENV5     | 0.9015-0.9064 | 0.5008-0.5035 | 0.000-1.000 |
| RMS       | 1.5653-1.5678 | 0.8696-0.8710 | 0.000-1.000 |
| Peak      | 1.0133-1.1336 | 0.5630-0.6298 | 0.000-1.000 |

### The Gap

- **Envelope features**: actual range ~0.501-0.505 (normalized), training expects 0.0-1.0
- **RMS feature**: actual ~0.870 (normalized), training expects 0.0-1.0
- **Peak feature**: actual ~0.563-0.630 (normalized), training expects 0.0-1.0

The envelope features are **compressed into a ~0.004 normalized range** when
the classifier was trained for a 1.0 range. This is a **250x mismatch**.

## 5. Score Sensitivity Analysis

How much does a 1 mV envelope change affect classifier scores?

A 1 mV change in input voltage -> delta_score = weight * 0.001 / 1.8

For the most sensitive weight (outer_race, BPF5): w = 18.231
- delta_score = 18.231 * 0.001 / 1.8 = 0.0101 per mV

To flip a classification, we typically need delta_score ~ 1.0
- Required: ~100 mV envelope change on the highest-weighted feature
- Available: ~7 mV maximum across all channels

**The signal is 14x too small to change the classification.**

## 6. Weight Rescaling Solution

### Approach: Adjust weights and biases to work with actual voltage range

Instead of: `Score = sum(w * V/1.8) + bias`

Use: `Score = sum(w' * (V - 0.9) / 0.01) + bias'`

This centers features at VCM (0.9V) and normalizes by ~10 mV range.

The weight transformation:
- `w' = w * 0.01 / 1.8` (scale down by normalization factor)
- `bias' = original_bias + sum(w * 0.9/1.8)` (absorb DC offset)

But this LOSES the training discrimination because the original weights
were trained for a different feature distribution.

### Better Approach: Retrain with Correct Feature Range

1. Run analog simulation for all 4 cases
2. Extract actual envelope voltages per channel
3. Use these as training features (not MinMax normalized)
4. Train classifier on actual voltage values
5. Export weights that expect inputs at ~0.9V +/- 10 mV

The classifier weights would be ~100x larger to compensate for
the smaller input range, but the VCVS behavioral model can handle this.

## 7. Why Inner Race Still Works

Inner race is the ONE test case that classifies correctly. Why?

Inner race has the largest envelope activity in channels 3-5:
- ENV3: 9.7 mV above VCM (vs 3.2 mV for normal)
- ENV4: 8.5 mV above VCM (vs 1.9 mV for normal)
- ENV5: 6.4 mV above VCM (vs 1.5 mV for normal)

Class 1 (Inner Race) has large positive weights on ENV3 (+14.002)
and ENV2 (+5.545). The slightly larger ENV3 value tips the score.
The margin is tiny -- the classifier barely picks inner race over
outer race (0.45V output, sometimes flipping to 1.35V).

## 8. Recommendations

1. **Retrain classifier for actual analog feature range** (highest impact)
2. **Increase stimulus amplitude** to widen envelope spread
3. **Add post-envelope gain** to amplify mV offsets to hundreds of mV
4. **Fix BPF bias** so channels 4/5 actually separate frequencies correctly

The weight rescaling alone (without retraining) will NOT work because
the feature DISTRIBUTION changes when you move from [0,1] normalized
to [0.900, 0.910] analog. The inter-class separations are different.