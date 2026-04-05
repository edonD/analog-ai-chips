#!/usr/bin/env python3
"""Analyze peak-detector simulation results for VibroSense-1.

Parses all 4 peak_*.raw files, extracts features, checks classification,
and produces detailed reports.
"""

import os
import sys
import json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_results import parse_ngspice_raw

RESULTS = '/home/ubuntu/analog-ai-chips/vibrosense/10_fullchain/results'
TEST_CASES = ['normal', 'inner_race', 'outer_race', 'ball']
CLASS_NAMES = ['Normal', 'Inner Race', 'Ball', 'Outer Race']
CASE_TO_CLASS = {'normal': 0, 'inner_race': 1, 'outer_race': 3, 'ball': 2}

def analyze_one(case):
    """Analyze a single test case."""
    raw_file = os.path.join(RESULTS, f'peak_{case}.raw')
    if not os.path.exists(raw_file):
        print(f"  {case}: raw file not found")
        return None

    data, var_names = parse_ngspice_raw(raw_file)
    time = data.get('time', np.array([]))
    if len(time) == 0:
        print(f"  {case}: no time data")
        return None

    result = {
        'test_case': case,
        'n_points': len(time),
        'sim_time_ms': float(time[-1] * 1e3),
    }

    # Use last 50ms for steady-state analysis (or last 25% if sim is short)
    t_start = max(time[-1] * 0.75, time[-1] - 0.050)
    mask = time >= t_start

    print(f"\n{'='*60}")
    print(f"TEST CASE: {case} (expected class {CASE_TO_CLASS[case]} = {CLASS_NAMES[CASE_TO_CLASS[case]]})")
    print(f"{'='*60}")
    print(f"  Time points: {len(time)}, range: {time[0]*1e3:.1f} - {time[-1]*1e3:.1f} ms")
    print(f"  Analysis window: {t_start*1e3:.1f} - {time[-1]*1e3:.1f} ms ({mask.sum()} points)")

    # Envelope features
    print(f"\n  Envelope features (steady-state):")
    for ch in range(1, 6):
        key = f'v(venv{ch})'
        if key in data:
            d = data[key][mask]
            result[f'env{ch}_mean'] = float(d.mean())
            result[f'env{ch}_median'] = float(np.median(d))
            result[f'env{ch}_min'] = float(d.min())
            result[f'env{ch}_max'] = float(d.max())
            result[f'env{ch}_std'] = float(d.std())
            print(f"    ENV{ch}: mean={d.mean():.4f} V, range=[{d.min():.4f}, {d.max():.4f}], std={d.std()*1e3:.2f} mV")

    # RMS/Peak features
    for sig in ['rms_out', 'rms_ref', 'peak_out']:
        key = f'v({sig})'
        if key in data:
            d = data[key][mask]
            result[f'{sig}_mean'] = float(d.mean())
            result[f'{sig}_median'] = float(np.median(d))
            print(f"    {sig}: mean={d.mean():.4f} V, median={np.median(d):.4f} V")

    # Classification output
    key = 'v(class_out)'
    if key in data:
        cout = data[key][mask]
        # Sample at 1ms intervals for voting
        all_cout = data[key]
        dt = 1e-3
        votes = {0: 0, 1: 0, 2: 0, 3: 0}
        for t_sample in np.arange(t_start, time[-1], dt):
            idx = np.searchsorted(time, t_sample)
            if idx < len(all_cout):
                v = all_cout[idx]
                if v < 0.225:
                    cls = 0
                elif v < 0.675:
                    cls = 1
                elif v < 1.125:
                    cls = 2
                else:
                    cls = 3
                votes[cls] += 1

        total_votes = sum(votes.values())
        if total_votes > 0:
            majority_class = max(votes, key=votes.get)
            majority_pct = votes[majority_class] / total_votes * 100
        else:
            majority_class = -1
            majority_pct = 0

        result['class_voltage_median'] = float(np.median(cout))
        result['class_voltage_final'] = float(cout[-1])
        result['detected_class'] = majority_class
        result['detected_name'] = CLASS_NAMES[majority_class] if majority_class >= 0 else 'Unknown'
        result['expected_class'] = CASE_TO_CLASS[case]
        result['expected_name'] = CLASS_NAMES[CASE_TO_CLASS[case]]
        result['correct'] = majority_class == CASE_TO_CLASS[case]
        result['votes'] = {CLASS_NAMES[k]: f"{v}/{total_votes} ({v/total_votes*100:.0f}%)" for k, v in votes.items() if v > 0}
        result['majority_pct'] = majority_pct

        print(f"\n  Classification:")
        print(f"    class_out median: {np.median(cout):.3f} V, final: {cout[-1]:.3f} V")
        print(f"    Majority vote: class {majority_class} ({CLASS_NAMES[majority_class]}) at {majority_pct:.0f}%")
        print(f"    Expected: class {CASE_TO_CLASS[case]} ({CLASS_NAMES[CASE_TO_CLASS[case]]})")
        print(f"    {'CORRECT' if result['correct'] else 'WRONG'}")
        if total_votes > 0:
            for cls in range(4):
                if votes[cls] > 0:
                    print(f"      class {cls} ({CLASS_NAMES[cls]}): {votes[cls]}/{total_votes} ({votes[cls]/total_votes*100:.0f}%)")

    # Power measurement
    total_power = 0.0
    power_blocks = {}
    for vn in var_names:
        if 'v_vdd_' in vn.lower() or vn == 'i(vdd)':
            if vn in data:
                current = data[vn][mask]
                avg_i = -np.mean(current)  # negative convention
                power = 1.8 * avg_i
                block = vn.replace('i(', '').replace(')', '')
                if abs(power) > 1e-12:
                    power_blocks[block] = float(power * 1e6)
                    if block != 'vdd':
                        total_power += power

    result['power_blocks_uw'] = power_blocks
    result['total_power_uw'] = float(total_power * 1e6)

    if power_blocks:
        print(f"\n  Power consumption:")
        for name, puw in sorted(power_blocks.items()):
            if name != 'vdd':
                print(f"    {name:20s}: {puw:>8.2f} uW")
        print(f"    {'TOTAL':20s}: {total_power*1e6:>8.2f} uW")

    return result


def main():
    print("VibroSense-1 Peak Detector Results Analysis")
    print("=" * 60)

    all_results = {}
    n_correct = 0
    n_total = 0

    for case in TEST_CASES:
        result = analyze_one(case)
        if result is not None:
            all_results[case] = result
            n_total += 1
            if result.get('correct', False):
                n_correct += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    accuracy = n_correct / n_total * 100 if n_total > 0 else 0
    print(f"Accuracy: {n_correct}/{n_total} ({accuracy:.0f}%)")
    for case in TEST_CASES:
        if case in all_results:
            r = all_results[case]
            status = "OK" if r.get('correct') else "WRONG"
            detected = r.get('detected_name', '?')
            expected = r.get('expected_name', '?')
            print(f"  {case:15s}: detected={detected:15s} expected={expected:15s} [{status}]")

    # Feature comparison table
    print(f"\n--- Feature Comparison (steady-state medians) ---")
    header = f"{'Case':15s}"
    for ch in range(1, 6):
        header += f" | {'ENV'+str(ch):7s}"
    header += f" | {'RMS':7s} | {'Peak':7s} | {'Ref':7s}"
    print(header)
    for case in TEST_CASES:
        if case in all_results:
            r = all_results[case]
            row = f"{case:15s}"
            for ch in range(1, 6):
                val = r.get(f'env{ch}_mean', 0)
                row += f" | {val:.4f} "
            row += f" | {r.get('rms_out_mean', 0):.4f} | {r.get('peak_out_mean', 0):.4f} | {r.get('rms_ref_mean', 0):.4f}"
            print(row)

    # Save results
    results_file = os.path.join(RESULTS, 'peak_detector_results_v2.json')
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults saved to {results_file}")

    return all_results, n_correct, n_total


if __name__ == '__main__':
    results, correct, total = main()
