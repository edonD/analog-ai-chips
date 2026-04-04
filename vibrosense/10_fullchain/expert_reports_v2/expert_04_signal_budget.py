#!/usr/bin/env python3
"""Expert 4: Signal Level Budget Analysis"""

import os
import json
import numpy as np

REPORT = os.path.join(os.path.dirname(__file__), 'expert_04_signal_budget.md')
VIBROSENSE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS = os.path.join(VIBROSENSE, '10_fullchain/results')

def main():
    lines = []
    L = lines.append

    L("# Expert Report 04: End-to-End Signal Level Budget")
    L("")
    L("## 1. Overview")
    L("")
    L("Signal chain: Stimulus -> PGA -> BPF -> Envelope -> Classifier")
    L("")
    L("The classifier was trained on features normalized to [0, 1], scaled to [0, 1.8V]")
    L("in the SPICE behavioral model. We trace actual signal levels through every stage")
    L("to find where the information is lost.")
    L("")

    L("## 2. Stage-by-Stage Budget (Current Design)")
    L("")
    L("### Stage 0: Stimulus Generation")
    L("")
    L("| Parameter | Normal | Inner Race | Outer Race | Ball |")
    L("|-----------|--------|------------|------------|------|")
    L("| Fault amplitude (g) | 0 | 3.0 | 2.4 | 1.8 |")
    L("| V_SCALE | 0.02 | 0.02 | 0.02 | 0.02 |")
    L("| Peak deviation from VCM | ~6 mV | ~60 mV | ~48 mV | ~36 mV |")
    L("| Broadband noise | ~12 mVpp | ~12 mVpp | ~12 mVpp | ~12 mVpp |")
    L("")

    L("### Stage 1: PGA (16x gain)")
    L("")
    L("| Parameter | Normal | Inner Race | Outer Race | Ball |")
    L("|-----------|--------|------------|------------|------|")
    L("| Input pp | ~12 mV | ~120 mV | ~96 mV | ~72 mV |")
    L("| Output pp (16x) | ~192 mV | ~1920 mV* | ~1536 mV* | ~1152 mV |")
    L("| *Clipped to rail | ~192 mV | ~1700 mV | ~1536 mV | ~1152 mV |")
    L("")
    L("*Fault impulses clip at 1.75V output limit. Continuous signal portions don't clip.")
    L("")

    L("### Stage 2: Band-Pass Filter (5 channels)")
    L("")
    L("Each BPF selects a narrow band. Signal energy SPLITS across bands.")
    L("Typical energy distribution for impulse-type faults:")
    L("- Most energy in resonance band (~3 kHz for inner race)")
    L("- Some energy in adjacent bands")
    L("- Little energy in distant bands")
    L("")

    # Load analysis data
    analysis_path = os.path.join(RESULTS, 'fullchain_analysis.json')
    if os.path.exists(analysis_path):
        with open(analysis_path) as f:
            analysis = json.load(f)

    L("Estimated BPF output (mVpp) per channel:")
    L("")
    L("| Channel | Center Hz | Normal | Inner Race | Outer Race | Ball |")
    L("|---------|-----------|--------|------------|------------|------|")
    L("| BPF1    | 227       | ~5-10  | ~5-10      | ~5-10      | ~5-10 |")
    L("| BPF2    | 1001      | ~10-20 | ~30-60     | ~30-50     | ~20-40 |")
    L("| BPF3    | 3162      | ~5-15  | ~50-100    | ~40-80     | ~30-60 |")
    L("| BPF4    | 7236*     | ~3-8   | ~30-60     | ~20-40     | ~30-50 |")
    L("| BPF5    | 14639*    | ~2-5   | ~10-30     | ~5-15      | ~10-20 |")
    L("")
    L("*BPF4 and BPF5 are detuned due to bias mismatch (see Expert 02)")
    L("")

    L("### Stage 3: Envelope Detector")
    L("")
    L("The envelope converts BPF AC amplitude to DC offset above VCM (0.9V).")
    L("")
    L("From actual simulation data (mean envelope values):")
    L("")
    if os.path.exists(analysis_path):
        L("| Channel | Normal (mV>VCM) | Inner (mV>VCM) | Outer (mV>VCM) | Ball (mV>VCM) |")
        L("|---------|-----------------|----------------|----------------|---------------|")
        for ch in range(1, 6):
            vals = []
            for tc in ['normal', 'inner_race', 'outer_race', 'ball']:
                v = (analysis[tc][f'env{ch}_mean'] - 0.9) * 1000
                vals.append(v)
            L(f"| ENV{ch}   | {vals[0]:+.2f}           | {vals[1]:+.2f}          | {vals[2]:+.2f}          | {vals[3]:+.2f}         |")
        L("")

    L("### Stage 4: Classifier Input")
    L("")
    L("The classifier behavioral model divides each input by 1.8V and multiplies by weights.")
    L("With envelope values near 0.9V (VCM), the normalized value is ~0.5 for ALL inputs.")
    L("")
    L("| Feature | Normal (norm) | Inner (norm) | Outer (norm) | Ball (norm) |")
    L("|---------|---------------|--------------|--------------|-------------|")
    if os.path.exists(analysis_path):
        for ch in range(1, 6):
            vals = []
            for tc in ['normal', 'inner_race', 'outer_race', 'ball']:
                v = analysis[tc][f'env{ch}_mean'] / 1.8
                vals.append(v)
            L(f"| ENV{ch}   | {vals[0]:.5f}       | {vals[1]:.5f}      | {vals[2]:.5f}      | {vals[3]:.5f}     |")
    L("")
    L("**All normalized features are ~0.502 +/- 0.004**")
    L("The classifier needs features distributed across [0, 1] to discriminate.")
    L("")

    L("## 3. The Gain Budget Gap")
    L("")
    L("| Stage | Input Range | Output Range | Gain | Information Loss |")
    L("|-------|-------------|-------------|------|-----------------|")
    L("| Stimulus | -- | 12-120 mVpp | -- | None |")
    L("| PGA (16x) | 12-120 mVpp | 192-1700 mVpp | 16x | Some clipping |")
    L("| BPF (band split) | 192-1700 mVpp | 5-100 mVpp | 0.03-0.06x | Energy splitting |")
    L("| Envelope | 5-100 mVpp | 0.9+1 to 0.9+10 mV | DC conversion | Small offset |")
    L("| Classifier norm | 0.901-0.910 V | 0.500-0.506 | /1.8V | **MASSIVE** |")
    L("")
    L("**The critical bottleneck**: Band-splitting reduces the signal by 15-30x,")
    L("then the envelope produces only millivolt DC offsets. These millivolt offsets")
    L("become indistinguishable when normalized to the full 0-1.8V range.")
    L("")

    L("## 4. What the Classifier Actually Sees")
    L("")
    L("Computing actual classifier scores with the real envelope values:")
    L("")

    # Compute classifier scores
    weights = [
        [5.545, 1.317, -5.026, -9.254, -11.369, -5.026, -7.140, -0.797],
        [-7.140, 5.545, 14.002, -0.797, 1.317, -2.912, 3.431, 5.545],
        [-0.797, -2.912, 5.545, 9.774, -9.254, -2.912, 3.431, -5.026],
        [3.431, -2.912, -13.483, 1.317, 18.231, 9.774, -0.797, -0.797],
    ]
    biases = [3.600, -2.798, 1.467, -2.372]

    if os.path.exists(analysis_path):
        for tc in ['normal', 'inner_race', 'outer_race', 'ball']:
            d = analysis[tc]
            features = [d[f'env{i}_mean'] for i in range(1, 6)]
            features.append(d['rms_out_mean'])
            features.append(d['peak_out_mean'])
            features.append(d.get('rms_ref_mean', d.get('rms_out_mean', 0.9)))  # rms_ref as kurtosis proxy

            L(f"### {tc}")
            L(f"Features: {[f'{v:.4f}' for v in features]}")
            scores = []
            for cls in range(4):
                s = biases[cls]
                for i in range(8):
                    s += weights[cls][i] * features[i] / 1.8
                scores.append(s)
            L(f"Scores: Normal={scores[0]:.3f}, Inner={scores[1]:.3f}, Ball={scores[2]:.3f}, Outer={scores[3]:.3f}")
            winner = np.argmax(scores)
            class_names = ['Normal', 'Inner Race', 'Ball', 'Outer Race']
            L(f"Winner: **{class_names[winner]}** (score={scores[winner]:.3f})")
            L(f"Expected: **{tc}**")
            L("")

    L("## 5. Proposed Signal Level Plan")
    L("")
    L("### Option A: Increase stimulus amplitude (easiest)")
    L("- V_SCALE: 0.02 -> 0.2 (10x)")
    L("- PGA: 16x -> 4x")
    L("- Net: 0.8 V/g vs current 0.32 V/g (2.5x increase)")
    L("- Expected envelope spread: ~15-25 mV (3x improvement)")
    L("- Still insufficient for 0-1.8V classifier range")
    L("")
    L("### Option B: Add post-envelope amplifier (medium effort)")
    L("- Add a 50-100x amplifier after each envelope LPF")
    L("- Envelope offset of 5 mV * 100 = 500 mV")
    L("- Needs DC level shifting (remove VCM before amplification)")
    L("- Would require AC-coupled gain stage or differential measurement")
    L("")
    L("### Option C: Retrain classifier for actual voltage range (best)")
    L("- The classifier was trained with MinMaxScaler mapping features to [0, 1]")
    L("- The behavioral model scales [0,1] to [0, 1.8V]")
    L("- Actual features are in range [0.900, 0.910V]")
    L("- **Retrain**: normalize to actual envelope output range, not [0, 1.8V]")
    L("- Retrain the behavioral classifier to expect inputs centered at 0.9V")
    L("  with millivolt-scale variations")
    L("- This is a WEIGHT RESCALING problem, not a hardware problem")
    L("")
    L("### Option D: Combined approach (recommended)")
    L("1. Increase V_SCALE to 0.1 V/g, keep PGA at 16x (5x signal boost)")
    L("2. Retrain classifier with features in actual analog voltage range")
    L("3. This gives envelope spreads of ~30-50 mV")
    L("4. Rescale classifier weights for the [0.88, 0.95V] feature range")
    L("5. Expected accuracy: 75-90% (envelope features become meaningful)")
    L("")

    L("## 6. Key Numbers")
    L("")
    L("| Metric | Current | Needed for 80%+ accuracy |")
    L("|--------|---------|--------------------------|")
    L("| Envelope spread (max across cases) | 6.6 mV | >50 mV |")
    L("| Feature normalized range | 0.500-0.506 | 0.0-1.0 |")
    L("| Classifier score margin | <0.1 | >1.0 |")
    L("| Signal-to-classifier-noise ratio | ~0 dB | >20 dB |")

    with open(REPORT, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Expert 04 report written to {REPORT}")

if __name__ == '__main__':
    main()
