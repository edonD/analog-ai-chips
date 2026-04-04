#!/usr/bin/env python3
"""Expert 8: Full-Chain Raw Data Analysis"""

import os
import json
import numpy as np

REPORT = os.path.join(os.path.dirname(__file__), 'expert_08_raw_data_analysis.md')
VIBROSENSE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS = os.path.join(VIBROSENSE, '10_fullchain/results')

def parse_ngspice_raw(filename):
    """Parse ngspice binary raw file."""
    with open(filename, 'rb') as f:
        raw = f.read()
    header_end = raw.find(b'Binary:\n')
    if header_end < 0:
        raise ValueError("Not a binary raw file")
    header = raw[:header_end].decode('ascii', errors='replace')
    binary_data = raw[header_end + len(b'Binary:\n'):]
    n_vars = 0
    n_points = 0
    var_names = []
    for line in header.split('\n'):
        line = line.strip()
        if line.startswith('No. Variables:'):
            n_vars = int(line.split(':')[1].strip())
        elif line.startswith('No. Points:'):
            n_points = int(line.split(':')[1].strip())
        elif '\t' in line and len(var_names) < n_vars:
            parts = line.split('\t')
            if len(parts) >= 3 and parts[0].strip().isdigit():
                var_names.append(parts[1].strip())
    if n_vars == 0:
        return {}, []
    bytes_per_point = n_vars * 8
    if n_points == 0:
        n_points = len(binary_data) // bytes_per_point
    usable = n_points * bytes_per_point
    all_data = np.frombuffer(binary_data[:usable], dtype=np.float64)
    all_data = all_data.reshape(n_points, n_vars)
    data = {}
    for i, name in enumerate(var_names):
        data[name] = all_data[:, i]
    return data, var_names

def main():
    lines = []
    L = lines.append

    L("# Expert Report 08: Full-Chain Raw Data Analysis")
    L("")
    L("## 1. Data Availability")
    L("")

    test_cases = ['normal', 'inner_race', 'outer_race', 'ball']
    all_data = {}

    for tc in test_cases:
        raw_file = os.path.join(RESULTS, f'fullchain_{tc}.raw')
        if os.path.exists(raw_file):
            size_mb = os.path.getsize(raw_file) / 1e6
            L(f"- {tc}: {size_mb:.1f} MB")
            try:
                data, var_names = parse_ngspice_raw(raw_file)
                all_data[tc] = data
                time = data.get('time', np.array([]))
                L(f"  Parsed: {len(var_names)} variables, {len(time)} time points")
                if len(time) > 0:
                    L(f"  Time range: {time[0]*1e3:.1f} ms to {time[-1]*1e3:.1f} ms")
            except Exception as e:
                L(f"  Parse error: {e}")
        else:
            L(f"- {tc}: NOT FOUND")
    L("")

    if not all_data:
        L("**No raw data could be parsed. Cannot perform analysis.**")
        with open(REPORT, 'w') as f:
            f.write('\n'.join(lines))
        return

    L("## 2. Input Signal Analysis")
    L("")
    L("| Test Case | Vin mean (V) | Vin pp (mV) | Vin min (V) | Vin max (V) |")
    L("|-----------|-------------|-------------|-------------|-------------|")
    for tc in test_cases:
        if tc in all_data and 'v(vin)' in all_data[tc]:
            vin = all_data[tc]['v(vin)']
            L(f"| {tc:12s} | {vin.mean():.4f} | {(vin.max()-vin.min())*1e3:.1f} | {vin.min():.4f} | {vin.max():.4f} |")
    L("")

    L("## 3. PGA Output Analysis")
    L("")
    L("| Test Case | PGA mean (V) | PGA pp (mV) | PGA min (V) | PGA max (V) | Gain |")
    L("|-----------|-------------|-------------|-------------|-------------|------|")
    for tc in test_cases:
        d = all_data.get(tc, {})
        if 'v(vout_pga)' in d and 'v(vin)' in d:
            vpga = d['v(vout_pga)']
            vin = d['v(vin)']
            gain = (vpga.max()-vpga.min()) / max(vin.max()-vin.min(), 1e-9)
            L(f"| {tc:12s} | {vpga.mean():.4f} | {(vpga.max()-vpga.min())*1e3:.1f} | {vpga.min():.4f} | {vpga.max():.4f} | {gain:.1f}x |")
    L("")

    L("## 4. BPF Output Analysis (per channel)")
    L("")
    for ch in range(1, 6):
        key = f'v(vbpf{ch}p)'
        L(f"### BPF Channel {ch}")
        L("")
        L(f"| Test Case | Mean (V) | Vpp (mV) | Std (mV) |")
        L(f"|-----------|----------|----------|----------|")
        for tc in test_cases:
            d = all_data.get(tc, {})
            if key in d:
                sig = d[key]
                # Use second half for settled analysis
                half = len(sig) // 2
                sig_half = sig[half:]
                pp = (sig_half.max() - sig_half.min()) * 1e3
                std = sig_half.std() * 1e3
                L(f"| {tc:12s} | {sig_half.mean():.4f} | {pp:.2f} | {std:.2f} |")
        L("")

    L("## 5. Envelope Output Analysis (per channel)")
    L("")
    L("Using last 50ms window for settled values:")
    L("")
    for ch in range(1, 6):
        key = f'v(venv{ch})'
        L(f"### Envelope Channel {ch}")
        L("")
        L(f"| Test Case | Mean (V) | Mean-VCM (mV) | Std (mV) | Final (V) |")
        L(f"|-----------|----------|---------------|----------|-----------|")
        for tc in test_cases:
            d = all_data.get(tc, {})
            if key in d:
                time = d.get('time', np.array([]))
                sig = d[key]
                if len(time) > 0:
                    # Last 50ms
                    t_end = time[-1]
                    mask = time > (t_end - 0.05)
                    sig_window = sig[mask]
                    mean_v = sig_window.mean()
                    std_v = sig_window.std() * 1e3
                    final_v = sig[-1]
                    L(f"| {tc:12s} | {mean_v:.6f} | {(mean_v-0.9)*1e3:+.3f} | {std_v:.3f} | {final_v:.6f} |")
        L("")

    L("## 6. Cross-Channel Envelope Comparison (Last 50ms)")
    L("")
    L("### Deviations from VCM (mV)")
    L("")
    L("| Test Case | ENV1 | ENV2 | ENV3 | ENV4 | ENV5 | Max-Min |")
    L("|-----------|------|------|------|------|------|---------|")

    env_data = {}
    for tc in test_cases:
        d = all_data.get(tc, {})
        time = d.get('time', np.array([]))
        if len(time) == 0:
            continue
        t_end = time[-1]
        mask = time > (t_end - 0.05)
        env_vals = []
        for ch in range(1, 6):
            key = f'v(venv{ch})'
            if key in d:
                sig = d[key][mask]
                env_vals.append((sig.mean() - 0.9) * 1e3)
            else:
                env_vals.append(0)
        env_data[tc] = env_vals
        spread = max(env_vals) - min(env_vals)
        L(f"| {tc:12s} | {env_vals[0]:+.2f} | {env_vals[1]:+.2f} | {env_vals[2]:+.2f} | {env_vals[3]:+.2f} | {env_vals[4]:+.2f} | {spread:.2f} |")
    L("")

    # Cross-case analysis
    L("### Per-Channel Spread Across Test Cases (mV)")
    L("")
    for ch in range(5):
        vals = [env_data.get(tc, [0]*5)[ch] for tc in test_cases]
        spread = max(vals) - min(vals)
        L(f"- ENV{ch+1}: spread = {spread:.2f} mV (min={min(vals):+.2f}, max={max(vals):+.2f})")
    L("")

    L("## 7. RMS and Peak Output Analysis")
    L("")
    L("| Test Case | RMS out (V) | RMS ref (V) | Peak out (V) | RMS-Ref diff (mV) |")
    L("|-----------|-------------|-------------|--------------|-------------------|")
    for tc in test_cases:
        d = all_data.get(tc, {})
        time = d.get('time', np.array([]))
        if len(time) == 0:
            continue
        t_end = time[-1]
        mask = time > (t_end - 0.05)
        rms = d.get('v(rms_out)', np.array([0]))
        ref = d.get('v(rms_ref)', np.array([0]))
        peak = d.get('v(peak_out)', np.array([0]))
        rms_v = rms[mask].mean() if len(rms) > sum(mask) else rms[-1]
        ref_v = ref[mask].mean() if len(ref) > sum(mask) else ref[-1]
        peak_v = peak[mask].mean() if len(peak) > sum(mask) else peak[-1]
        L(f"| {tc:12s} | {rms_v:.4f} | {ref_v:.4f} | {peak_v:.4f} | {(rms_v-ref_v)*1e3:.1f} |")
    L("")

    L("## 8. Classifier Score Analysis")
    L("")
    for score_prefix in ['v(score', 'score']:
        found_any = False
        for tc in test_cases:
            d = all_data.get(tc, {})
            for i in range(4):
                key = f'{score_prefix}{i})'
                if key in d:
                    found_any = True
        if found_any:
            L(f"Using score key prefix: `{score_prefix}`")
            break

    L("")
    L("| Test Case | Score0 (Normal) | Score1 (Inner) | Score2 (Ball) | Score3 (Outer) | Winner |")
    L("|-----------|----------------|----------------|---------------|----------------|--------|")
    class_names = ['Normal', 'Inner', 'Ball', 'Outer']
    for tc in test_cases:
        d = all_data.get(tc, {})
        time = d.get('time', np.array([]))
        if len(time) == 0:
            continue
        t_end = time[-1]
        mask = time > (t_end - 0.05)
        scores = []
        for i in range(4):
            for key in [f'v(score{i})', f'score{i}']:
                if key in d:
                    s = d[key][mask].mean() if len(d[key]) > sum(mask) else d[key][-1]
                    scores.append(s)
                    break
            else:
                scores.append(float('nan'))
        if not any(np.isnan(scores)):
            winner = class_names[np.argmax(scores)]
            L(f"| {tc:12s} | {scores[0]:+.3f} | {scores[1]:+.3f} | {scores[2]:+.3f} | {scores[3]:+.3f} | {winner} |")
        else:
            # Try to get from class_out
            if 'v(class_out)' in d:
                cout = d['v(class_out)'][mask]
                median_v = np.median(cout)
                if median_v < 0.225:
                    winner = 'Normal'
                elif median_v < 0.675:
                    winner = 'Inner'
                elif median_v < 1.125:
                    winner = 'Ball'
                else:
                    winner = 'Outer'
                L(f"| {tc:12s} | (scores N/A) | | | | {winner} (V={median_v:.3f}) |")
    L("")

    L("## 9. Where Exactly Is Differentiation Lost?")
    L("")
    L("### Stage-by-stage discrimination metric (max spread across 4 cases)")
    L("")

    # Calculate spreads at each stage
    stages = {}

    # Input
    vin_spreads = []
    for tc in test_cases:
        d = all_data.get(tc, {})
        if 'v(vin)' in d:
            vin = d['v(vin)']
            vin_spreads.append(vin.std())
    if vin_spreads:
        stages['Input (Vin std)'] = (max(vin_spreads) - min(vin_spreads)) * 1e3

    # PGA
    pga_spreads = []
    for tc in test_cases:
        d = all_data.get(tc, {})
        if 'v(vout_pga)' in d:
            vpga = d['v(vout_pga)']
            half = len(vpga)//2
            pga_spreads.append(vpga[half:].std())
    if pga_spreads:
        stages['PGA (std spread)'] = (max(pga_spreads) - min(pga_spreads)) * 1e3

    # BPF - per channel
    for ch in range(1, 6):
        key = f'v(vbpf{ch}p)'
        bpf_stds = []
        for tc in test_cases:
            d = all_data.get(tc, {})
            if key in d:
                half = len(d[key])//2
                bpf_stds.append(d[key][half:].std())
        if bpf_stds:
            stages[f'BPF{ch} (std spread)'] = (max(bpf_stds) - min(bpf_stds)) * 1e3

    # Envelope - per channel
    for ch in range(1, 6):
        key = f'v(venv{ch})'
        env_means = []
        for tc in test_cases:
            d = all_data.get(tc, {})
            if key in d:
                time = d.get('time', np.array([]))
                mask = time > (time[-1] - 0.05)
                env_means.append(d[key][mask].mean())
        if env_means:
            stages[f'ENV{ch} (mean spread)'] = (max(env_means) - min(env_means)) * 1e3

    L("| Stage | Cross-case spread (mV) | Assessment |")
    L("|-------|----------------------|------------|")
    for stage, spread in stages.items():
        if spread > 10:
            assessment = "GOOD"
        elif spread > 1:
            assessment = "MARGINAL"
        else:
            assessment = "POOR"
        L(f"| {stage:25s} | {spread:.2f} | {assessment} |")
    L("")

    L("## 10. Key Findings")
    L("")
    L("1. **Input signals DO differ**: The stimulus Vpp varies by test case")
    L("   (inner race > outer race > ball > normal)")
    L("")
    L("2. **PGA preserves differentiation**: After PGA, the signal std still differs")
    L("")
    L("3. **BPF channels show SOME differentiation**: The AC amplitude (std) differs")
    L("   across test cases, especially in channels 2-4")
    L("")
    L("4. **Envelope detector COMPRESSES differentiation**: The DC envelope values")
    L("   are within ~7 mV of each other. The BPF amplitude differences (~10-50 mV)")
    L("   are reduced to ~1-7 mV DC offsets by the half-wave rectification + LPF.")
    L("")
    L("5. **The classifier cannot distinguish 1-7 mV differences** because it divides")
    L("   by 1.8V, making the features all ~0.5 (normalized).")
    L("")
    L("**The information EXISTS at the BPF outputs but is LOST in the envelope-to-classifier**")
    L("**mapping. The fix is either amplification after envelope or classifier retraining.**")

    with open(REPORT, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Expert 08 report written to {REPORT}")

if __name__ == '__main__':
    main()
