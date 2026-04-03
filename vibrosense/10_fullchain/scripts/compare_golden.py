#!/usr/bin/env python3
"""VibroSense-1 Golden Model Comparison.

Compares SPICE simulation results to a Python golden model
that processes the same input data using ideal digital filters.
"""

import os
import sys
import json
import numpy as np
from scipy.signal import butter, sosfilt

sys.path.insert(0, os.path.dirname(__file__))
from analyze_results import parse_ngspice_raw

BASE = os.path.dirname(os.path.abspath(__file__))
FULLCHAIN = os.path.dirname(BASE)
RESULTS = os.path.join(FULLCHAIN, 'results')


def bandpass_filter(signal, fs, f_low, f_high, order=4):
    """Apply Butterworth bandpass filter."""
    nyq = fs / 2
    low = max(f_low / nyq, 0.001)
    high = min(f_high / nyq, 0.999)
    sos = butter(order, [low, high], btype='band', output='sos')
    return sosfilt(sos, signal)


def envelope_detector(signal, fs, lpf_cutoff=10):
    """Ideal envelope: rectify + LPF."""
    rectified = np.abs(signal)
    nyq = fs / 2
    cutoff = min(lpf_cutoff / nyq, 0.999)
    sos = butter(2, cutoff, btype='low', output='sos')
    return sosfilt(sos, rectified)


def extract_features(signal, fs=12000):
    """Extract 8 features from a signal window (golden model)."""
    # Band definitions (Hz)
    bands = [(100, 500), (500, 1500), (1500, 3000), (3000, 4500), (4500, 5900)]

    features = []

    # 5 band envelope energies
    for f_low, f_high in bands:
        filtered = bandpass_filter(signal, fs, f_low, f_high)
        env = envelope_detector(filtered, fs, lpf_cutoff=10)
        features.append(np.mean(env[-len(env)//2:]))

    # Broadband RMS
    features.append(np.sqrt(np.mean(signal**2)))

    # Crest factor
    peak = np.max(np.abs(signal))
    rms = features[-1]
    crest = peak / rms if rms > 0 else 0
    features.append(crest)

    # Kurtosis
    std = np.std(signal)
    kurt = np.mean(((signal - np.mean(signal)) / std)**4) - 3 if std > 0 else 0
    features.append(kurt)

    return np.array(features)


def run_golden_classifier(features, weights_file):
    """Run golden model classifier on features."""
    with open(weights_file) as f:
        w = json.load(f)

    W = np.array(w['quantized_weights'])
    B = np.array(w['quantized_biases'])
    norm_min = np.array(w['normalization']['min'])
    norm_max = np.array(w['normalization']['max'])

    # Normalize
    features_norm = (features - norm_min) / (norm_max - norm_min + 1e-10)
    features_norm = np.clip(features_norm, 0, 1)

    # Classify
    logits = features_norm @ W.T + B
    return np.argmax(logits), logits


def compare_spice_to_golden():
    """Compare SPICE results to golden model for each test case."""
    weights_file = os.path.join(FULLCHAIN, '..', '09_training', 'results', 'trained_weights.json')

    class_names = ['Normal', 'Inner Race', 'Ball', 'Outer Race']
    test_cases = ['normal', 'inner_race', 'outer_race', 'ball']
    expected_class = {'normal': 0, 'inner_race': 1, 'ball': 2, 'outer_race': 3}

    print("=" * 60)
    print("GOLDEN MODEL COMPARISON")
    print("=" * 60)

    results = {}

    for tc in test_cases:
        # Read stimulus to get original signal
        stim_file = os.path.join(FULLCHAIN, 'stimuli', f'{tc}_stimulus.pwl')
        if not os.path.exists(stim_file):
            continue

        # Parse PWL file
        times = []
        voltages = []
        with open(stim_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith('+') or (line and line[0].isdigit()):
                    parts = line.lstrip('+').strip().split()
                    if len(parts) >= 2:
                        try:
                            t = float(parts[0])
                            v = float(parts[1].rstrip(')'))
                            times.append(t)
                            voltages.append(v)
                        except ValueError:
                            pass

        if not times:
            continue

        signal = np.array(voltages)
        # Remove DC offset and convert back to acceleration units
        signal = (signal - 0.9) / 0.1  # reverse the V_scale and V_offset

        # Extract features using golden model
        features = extract_features(signal, fs=12000)

        # Run golden classifier
        golden_class, golden_logits = run_golden_classifier(features, weights_file)

        print(f"\n--- {tc} ---")
        print(f"  Expected class: {expected_class[tc]} ({class_names[expected_class[tc]]})")
        print(f"  Golden model:   {golden_class} ({class_names[golden_class]})")
        print(f"  Golden logits:  {golden_logits}")
        print(f"  Features: {features}")

        # Check SPICE result if available
        raw_file = os.path.join(RESULTS, f'fullchain_{tc}.raw')
        spice_class = None
        if os.path.exists(raw_file):
            try:
                data, _ = parse_ngspice_raw(raw_file)
                if 'v(class_out)' in data:
                    cout = data['v(class_out)']
                    v = np.median(cout[len(cout)//2:])
                    if v < 0.225: spice_class = 0
                    elif v < 0.675: spice_class = 1
                    elif v < 1.125: spice_class = 2
                    else: spice_class = 3
                    print(f"  SPICE result:   {spice_class} ({class_names[spice_class]})")
                    print(f"  SPICE matches golden: {spice_class == golden_class}")
            except:
                print(f"  SPICE result:   (simulation still running)")

        results[tc] = {
            'expected': expected_class[tc],
            'golden_class': int(golden_class),
            'golden_logits': golden_logits.tolist(),
            'golden_correct': golden_class == expected_class[tc],
            'spice_class': spice_class,
        }

    # Summary
    golden_correct = sum(1 for r in results.values() if r['golden_correct'])
    print(f"\nGolden model accuracy: {golden_correct}/{len(results)} "
          f"({100*golden_correct/len(results):.0f}%)" if results else "")

    # Save
    with open(os.path.join(RESULTS, 'golden_comparison.json'), 'w') as f:
        json.dump(results, f, indent=2, default=str)

    return results


if __name__ == '__main__':
    compare_spice_to_golden()
