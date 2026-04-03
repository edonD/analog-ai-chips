#!/usr/bin/env python3
"""VibroSense-1 Full-Chain Result Analysis.

Parses ngspice raw files, extracts waveforms, computes metrics.
"""

import os
import sys
import json
import struct
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
FULLCHAIN = os.path.dirname(BASE)
RESULTS = os.path.join(FULLCHAIN, 'results')


def parse_ngspice_raw(filename):
    """Parse ngspice binary raw file.

    Returns dict of variable_name -> numpy array.
    """
    with open(filename, 'rb') as f:
        raw = f.read()

    # Parse header (ASCII until 'Binary:\n')
    header_end = raw.find(b'Binary:\n')
    if header_end < 0:
        raise ValueError("Not a binary raw file")

    header = raw[:header_end].decode('ascii', errors='replace')
    binary_data = raw[header_end + len(b'Binary:\n'):]

    # Extract metadata from header
    n_vars = 0
    n_points = 0
    var_names = []
    var_types = []
    is_complex = False

    for line in header.split('\n'):
        line = line.strip()
        if line.startswith('No. Variables:'):
            n_vars = int(line.split(':')[1].strip())
        elif line.startswith('No. Points:'):
            n_points = int(line.split(':')[1].strip())
        elif line.startswith('Flags:') and 'complex' in line.lower():
            is_complex = True
        elif '\t' in line and len(var_names) < n_vars:
            parts = line.split('\t')
            if len(parts) >= 3 and parts[0].strip().isdigit():
                var_names.append(parts[1].strip())
                var_types.append(parts[2].strip())

    if n_vars == 0:
        raise ValueError(f"Could not parse header: n_vars={n_vars}")

    # Parse binary data (double precision, column-major)
    bytes_per_point = n_vars * 8  # 8 bytes per double
    if is_complex:
        bytes_per_point = n_vars * 16

    # If n_points is 0 (ngspice writes 0 during streaming), infer from data size
    if n_points == 0:
        n_points = len(binary_data) // bytes_per_point

    data = {}
    if not is_complex:
        usable = n_points * bytes_per_point
        all_data = np.frombuffer(binary_data[:usable],
                                 dtype=np.float64)
        all_data = all_data.reshape(n_points, n_vars)
        for i, name in enumerate(var_names):
            data[name] = all_data[:, i]

    return data, var_names


def analyze_quick_test():
    """Analyze the quick 25ms test (default sine stimulus)."""
    raw_file = os.path.join(RESULTS, 'fullchain_quick.raw')
    if not os.path.exists(raw_file):
        print("No quick test raw file found.")
        return

    print("=" * 60)
    print("QUICK TEST ANALYSIS (25ms, 1kHz sine input)")
    print("=" * 60)

    data, var_names = parse_ngspice_raw(raw_file)
    time = data.get('time', data.get('v-sweep', np.array([])))

    print(f"\nRaw file: {raw_file}")
    print(f"Variables: {len(var_names)}")
    print(f"Time points: {len(time)}")
    if len(time) > 0:
        print(f"Time range: {time[0]*1e3:.3f} ms to {time[-1]*1e3:.3f} ms")

    # Print all variable names
    print(f"\nAvailable signals:")
    for name in var_names:
        if name in data:
            d = data[name]
            print(f"  {name:40s}: min={d.min():+.4f}, max={d.max():+.4f}, "
                  f"mean={d.mean():+.4f}")

    # Key signal analysis
    results = {}

    # Input
    if 'v(vin)' in data:
        vin = data['v(vin)']
        results['vin_pp'] = float(vin.max() - vin.min())
        results['vin_mean'] = float(vin.mean())
        print(f"\n--- Input ---")
        print(f"  Vin: {results['vin_mean']:.3f} V (mean), "
              f"{results['vin_pp']*1e3:.1f} mVpp")

    # PGA output
    if 'v(vout_pga)' in data:
        vpga = data['v(vout_pga)']
        results['vpga_pp'] = float(vpga.max() - vpga.min())
        results['vpga_mean'] = float(vpga.mean())
        if 'vin_pp' in results and results['vin_pp'] > 0:
            results['pga_gain'] = results['vpga_pp'] / results['vin_pp']
        print(f"\n--- PGA Output ---")
        print(f"  Vpga: {results['vpga_mean']:.3f} V (mean), "
              f"{results['vpga_pp']*1e3:.1f} mVpp")
        if 'pga_gain' in results:
            print(f"  PGA gain: {results['pga_gain']:.1f}x")

    # Filter outputs
    for ch in range(1, 6):
        key = f'v(vbpf{ch}p)'
        if key in data:
            d = data[key]
            results[f'bpf{ch}_pp'] = float(d.max() - d.min())
            results[f'bpf{ch}_mean'] = float(d.mean())

    if any(f'bpf{ch}_pp' in results for ch in range(1, 6)):
        print(f"\n--- Filter Outputs (Vpp) ---")
        for ch in range(1, 6):
            if f'bpf{ch}_pp' in results:
                print(f"  BPF{ch}: {results[f'bpf{ch}_pp']*1e3:.2f} mVpp, "
                      f"mean={results[f'bpf{ch}_mean']:.3f} V")

    # Envelope outputs
    for ch in range(1, 6):
        key = f'v(venv{ch})'
        if key in data:
            d = data[key]
            results[f'env{ch}_final'] = float(d[-1])
            results[f'env{ch}_mean'] = float(d[len(d)//2:].mean())

    if any(f'env{ch}_final' in results for ch in range(1, 6)):
        print(f"\n--- Envelope Outputs (final value) ---")
        for ch in range(1, 6):
            if f'env{ch}_final' in results:
                print(f"  ENV{ch}: {results[f'env{ch}_final']:.4f} V")

    # RMS and Peak
    for key in ['v(rms_out)', 'v(rms_ref)', 'v(peak_out)']:
        if key in data:
            d = data[key]
            name = key.replace('v(', '').replace(')', '')
            results[f'{name}_final'] = float(d[-1])
            print(f"\n  {name}: {d[-1]:.4f} V")

    # Classifier output
    if 'v(class_out)' in data:
        cout = data['v(class_out)']
        # Get stable value (last portion)
        stable = cout[len(cout)//2:]
        results['class_voltage'] = float(np.median(stable))
        # Decode class
        v = results['class_voltage']
        if v < 0.225:
            results['detected_class'] = 0
        elif v < 0.675:
            results['detected_class'] = 1
        elif v < 1.125:
            results['detected_class'] = 2
        else:
            results['detected_class'] = 3

        class_names = ['Normal', 'Inner Race', 'Ball', 'Outer Race']
        print(f"\n--- Classifier Output ---")
        print(f"  Voltage: {results['class_voltage']:.3f} V")
        print(f"  Detected class: {results['detected_class']} "
              f"({class_names[results['detected_class']]})")

    # Scores
    for i in range(4):
        key = f'v(score{i})'  # internal to classifier subcircuit
        alt_key = f'xclass.score{i}'
        for k in [key, alt_key]:
            if k in data:
                results[f'score{i}'] = float(data[k][-1])

    if any(f'score{i}' in results for i in range(4)):
        print(f"\n--- Classifier Scores ---")
        for i in range(4):
            if f'score{i}' in results:
                print(f"  Class {i}: {results[f'score{i}']:.3f}")

    # Power measurement
    print(f"\n--- Power Consumption ---")
    total_power = 0
    power_blocks = {}
    for name in var_names:
        if name.startswith('i(') or name.startswith('@') or '#branch' in name:
            if 'v_vdd_' in name.lower() or 'vdd#branch' in name.lower():
                current = data[name]
                # Average current (use second half for settled values)
                avg_i = -np.mean(current[len(current)//2:])  # negative = into supply
                power = 1.8 * avg_i
                block_name = name.replace('i(', '').replace(')', '').replace('#branch', '')
                if abs(power) > 1e-12:  # skip zero-current blocks
                    power_blocks[block_name] = power
                    total_power += power

    if power_blocks:
        for name, power in sorted(power_blocks.items()):
            print(f"  {name:30s}: {power*1e6:>10.2f} uW")
        print(f"  {'TOTAL':30s}: {total_power*1e6:>10.2f} uW")
        results['power_uw'] = float(total_power * 1e6)
        results['power_blocks'] = {k: float(v*1e6) for k, v in power_blocks.items()}
    else:
        print("  No power data found in raw file")

    # Save results
    results_file = os.path.join(RESULTS, 'quick_test_results.json')
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {results_file}")

    return results


def analyze_fullchain_test(test_case):
    """Analyze a full-chain test case."""
    raw_file = os.path.join(RESULTS, f'fullchain_{test_case}.raw')
    if not os.path.exists(raw_file):
        print(f"No raw file for {test_case}")
        return None

    data, var_names = parse_ngspice_raw(raw_file)
    time = data.get('time', np.array([]))

    print(f"\n{'='*60}")
    print(f"ANALYSIS: {test_case}")
    print(f"{'='*60}")
    print(f"Time points: {len(time)}, range: {time[0]*1e3:.1f} - {time[-1]*1e3:.1f} ms")

    results = {'test_case': test_case, 'n_points': len(time)}

    # Classifier output over time
    if 'v(class_out)' in data:
        cout = data['v(class_out)']
        # Sample at regular intervals (every 1ms)
        dt = 1e-3
        classifications = []
        for t_sample in np.arange(dt, time[-1], dt):
            idx = np.searchsorted(time, t_sample)
            if idx < len(cout):
                v = cout[idx]
                if v < 0.225:
                    cls = 0
                elif v < 0.675:
                    cls = 1
                elif v < 1.125:
                    cls = 2
                else:
                    cls = 3
                classifications.append((float(t_sample), cls))

        results['classifications'] = classifications
        if classifications:
            # Majority vote (second half)
            second_half = [c for t, c in classifications if t > time[-1]/2]
            if second_half:
                from collections import Counter
                majority = Counter(second_half).most_common(1)[0]
                results['majority_class'] = majority[0]
                results['majority_pct'] = majority[1] / len(second_half) * 100

    return results


def main():
    os.makedirs(RESULTS, exist_ok=True)

    # Analyze quick test
    results = analyze_quick_test()

    # Analyze any full-chain tests that exist
    for tc in ['normal', 'inner_race', 'outer_race', 'ball']:
        raw = os.path.join(RESULTS, f'fullchain_{tc}.raw')
        if os.path.exists(raw):
            analyze_fullchain_test(tc)


if __name__ == '__main__':
    main()
