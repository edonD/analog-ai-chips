#!/usr/bin/env python3
"""Analyze THD and Noise for all 5 channels using real SKY130 OTA."""

import numpy as np
from datetime import datetime

# Channel parameters
channels = {
    1: {'f0': 219},
    2: {'f0': 1035},
    3: {'f0': 3131},
    4: {'f0': 6851},
    5: {'f0': 13829},
}

# Noise results from simulation (onoise_total in V_rms)
noise_results = {
    1: 7.079085e-06,
    2: 1.901791e-05,
    3: 3.599069e-05,
    4: 6.914415e-05,
    5: 3.281246e-04,
}

def load_wrdata(filename):
    """Load ngspice wrdata output (time, value pairs)."""
    t_list, v_list = [], []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('*') or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    t = float(parts[0])
                    v = float(parts[1])
                    t_list.append(t)
                    v_list.append(v)
                except ValueError:
                    continue
    return np.array(t_list), np.array(v_list)


def compute_thd(t, v, f0, n_harmonics=5):
    """Compute THD from time-domain data using FFT."""
    # Uniform resampling
    dt = np.median(np.diff(t))
    N = len(t)
    fs = 1.0 / dt

    # Remove DC
    v_ac = v - np.mean(v)

    # Window to reduce spectral leakage
    window = np.hanning(N)
    v_win = v_ac * window

    # FFT
    V = np.abs(np.fft.rfft(v_win)) * 2.0 / np.sum(window)
    freqs = np.fft.rfftfreq(N, dt)

    # Find fundamental and harmonics
    def find_peak(target_f, search_bw=None):
        if search_bw is None:
            search_bw = f0 * 0.15  # 15% bandwidth search
        mask = (freqs >= target_f - search_bw) & (freqs <= target_f + search_bw)
        if not np.any(mask):
            return 0.0
        idx = np.where(mask)[0]
        return np.max(V[idx])

    fund = find_peak(f0)
    if fund < 1e-12:
        return float('inf'), 0.0, []

    harmonics = []
    for h in range(2, n_harmonics + 1):
        hval = find_peak(h * f0)
        harmonics.append(hval)

    thd_linear = np.sqrt(np.sum(np.array(harmonics)**2)) / fund
    thd_pct = thd_linear * 100.0
    thd_db = 20 * np.log10(thd_linear) if thd_linear > 0 else -999

    return thd_pct, thd_db, harmonics


# Analyze all channels
results = []
print("=" * 70)
print("THD & Noise Analysis — All 5 Channels (Real SKY130 OTA)")
print("=" * 70)

for ch in range(1, 6):
    f0 = channels[ch]['f0']
    filename = f'thd_real_ch{ch}.txt'

    print(f"\n--- Channel {ch} (f0={f0} Hz) ---")

    try:
        t, v = load_wrdata(filename)
        print(f"  Loaded {len(t)} samples, dt={np.median(np.diff(t))*1e6:.2f} us")
        print(f"  Output: mean={np.mean(v):.4f} V, pk-pk={np.max(v)-np.min(v):.4f} V")

        thd_pct, thd_db, harmonics = compute_thd(t, v, f0)

        noise_v = noise_results[ch]
        noise_uv = noise_v * 1e6

        print(f"  THD = {thd_pct:.3f}% ({thd_db:.1f} dB)")
        for i, h in enumerate(harmonics):
            print(f"    H{i+2} = {h*1e6:.1f} uV")
        print(f"  Output noise (1-100kHz) = {noise_uv:.1f} uVrms")

        # Dynamic range: signal pk-pk / noise
        sig_rms = (np.max(v) - np.min(v)) / (2 * np.sqrt(2))
        if noise_v > 0:
            dr_db = 20 * np.log10(sig_rms / noise_v)
        else:
            dr_db = float('inf')
        print(f"  Signal RMS = {sig_rms*1e3:.2f} mV, DR = {dr_db:.1f} dB")

        results.append({
            'ch': ch, 'f0': f0,
            'thd_pct': thd_pct, 'thd_db': thd_db,
            'noise_uv': noise_uv, 'dr_db': dr_db,
            'vpkpk': np.max(v) - np.min(v),
            'status': 'OK'
        })

    except Exception as e:
        print(f"  ERROR: {e}")
        results.append({
            'ch': ch, 'f0': f0,
            'thd_pct': float('nan'), 'thd_db': float('nan'),
            'noise_uv': noise_results[ch] * 1e6, 'dr_db': float('nan'),
            'vpkpk': float('nan'),
            'status': f'ERROR: {e}'
        })

# Summary table
print("\n" + "=" * 70)
print("SUMMARY TABLE")
print("=" * 70)
header = f"{'Ch':>3} {'f0(Hz)':>8} {'THD(%)':>10} {'THD(dB)':>10} {'Noise(uV)':>10} {'DR(dB)':>8} {'Vpkpk(mV)':>10} {'Status':>8}"
print(header)
print("-" * len(header))

for r in results:
    print(f"{r['ch']:>3} {r['f0']:>8} {r['thd_pct']:>10.3f} {r['thd_db']:>10.1f} {r['noise_uv']:>10.1f} {r['dr_db']:>8.1f} {r['vpkpk']*1e3:>10.2f} {r['status']:>8}")

# Write to file
with open('thd_noise_summary.txt', 'w') as f:
    f.write(f"VibroSense THD & Noise Summary — Real SKY130 OTA\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Bias: Vbn=0.565V Vbcn=0.795V Vbp=0.860V Vbcp=0.605V Vcm=0.9V VDD=1.8V\n")
    f.write(f"Input: 200mVpp sine at each channel's measured f0\n")
    f.write(f"Noise: integrated 1Hz-100kHz (onoise_total from .noise)\n")
    f.write(f"\n")
    f.write(f"{'Ch':>3} {'f0(Hz)':>8} {'THD(%)':>10} {'THD(dB)':>10} {'Noise(uVrms)':>12} {'DR(dB)':>8} {'Vpkpk(mV)':>10}\n")
    f.write("-" * 65 + "\n")
    for r in results:
        f.write(f"{r['ch']:>3} {r['f0']:>8} {r['thd_pct']:>10.3f} {r['thd_db']:>10.1f} {r['noise_uv']:>12.1f} {r['dr_db']:>8.1f} {r['vpkpk']*1e3:>10.2f}\n")

    f.write(f"\nNotes:\n")
    f.write(f"- THD computed via FFT (Hanning window) on 20ms of transient data\n")
    f.write(f"- Harmonics 2-6 included in THD calculation\n")
    f.write(f"- DR = 20*log10(signal_rms / noise_rms)\n")
    f.write(f"- All simulations use transistor-level folded-cascode OTA (ota_foldcasc)\n")

print("\nResults written to thd_noise_summary.txt")
