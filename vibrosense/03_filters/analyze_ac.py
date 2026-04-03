#!/usr/bin/env python3
"""Analyze AC sweep results for all 5 BPF channels."""

import numpy as np
import sys

# Channel specifications
channels = {
    1: {'f0': 224,   'Q': 0.75, 'gm': 14.07e-9,  'gm3': 18.76e-9},
    2: {'f0': 1000,  'Q': 0.67, 'gm': 62.83e-9,  'gm3': 93.78e-9},
    3: {'f0': 3162,  'Q': 1.05, 'gm': 198.7e-9,   'gm3': 189.2e-9},
    4: {'f0': 7071,  'Q': 1.41, 'gm': 444.3e-9,   'gm3': 315.1e-9},
    5: {'f0': 14142, 'Q': 1.41, 'gm': 888.6e-9,   'gm3': 630.2e-9},
}

# Load data — wrdata format: freq1 re1 im1 freq2 re2 im2 ... (3 cols per vector)
data = np.loadtxt('ac_all_channels.txt')
freq = data[:, 0]  # All freq columns are identical

results = {}
all_pass = True

print("=" * 80)
print("Block 03: Gm-C Band-Pass Filter Bank — AC Sweep Results")
print("=" * 80)

for ch_num in range(1, 6):
    spec = channels[ch_num]
    # Each vector takes 3 columns: freq, re, im
    col_re = (ch_num - 1) * 3 + 1
    col_im = (ch_num - 1) * 3 + 2
    re = data[:, col_re]
    im = data[:, col_im]
    mag = np.sqrt(re**2 + im**2)
    mag_db = 20 * np.log10(mag + 1e-30)

    # Peak gain and frequency
    peak_idx = np.argmax(mag_db)
    f0_meas = freq[peak_idx]
    peak_db = mag_db[peak_idx]

    # Q measurement: find -3dB points
    target_db = peak_db - 3.0
    # Find lower -3dB frequency
    below_peak = np.where(freq < f0_meas)[0]
    if len(below_peak) > 0:
        crossings_low = np.where(np.diff(np.sign(mag_db[below_peak] - target_db)))[0]
        if len(crossings_low) > 0:
            idx = below_peak[crossings_low[-1]]
            # Linear interpolation
            f_low = freq[idx] + (target_db - mag_db[idx]) / (mag_db[idx+1] - mag_db[idx]) * (freq[idx+1] - freq[idx])
        else:
            f_low = freq[0]
    else:
        f_low = freq[0]

    # Find upper -3dB frequency
    above_peak = np.where(freq > f0_meas)[0]
    if len(above_peak) > 0:
        crossings_high = np.where(np.diff(np.sign(mag_db[above_peak] - target_db)))[0]
        if len(crossings_high) > 0:
            idx = above_peak[crossings_high[0]]
            f_high = freq[idx] + (target_db - mag_db[idx]) / (mag_db[idx+1] - mag_db[idx]) * (freq[idx+1] - freq[idx])
        else:
            f_high = freq[-1]
    else:
        f_high = freq[-1]

    bw_meas = f_high - f_low
    Q_meas = f0_meas / bw_meas if bw_meas > 0 else 0

    # Expected peak gain = 20*log10(Q)
    expected_gain_db = 20 * np.log10(spec['Q'])

    # Stopband: at 0.1*f0 and 10*f0
    f_low_stop = spec['f0'] * 0.1
    f_high_stop = spec['f0'] * 10
    idx_low_stop = np.argmin(np.abs(freq - f_low_stop))
    idx_high_stop = np.argmin(np.abs(freq - f_high_stop))
    stop_low_db = mag_db[idx_low_stop]
    stop_high_db = mag_db[idx_high_stop]
    rejection_low = peak_db - stop_low_db
    rejection_high = peak_db - stop_high_db

    # PASS/FAIL checks
    f0_err = abs(f0_meas - spec['f0']) / spec['f0'] * 100
    Q_err = abs(Q_meas - spec['Q']) / spec['Q'] * 100
    gain_err = abs(peak_db - expected_gain_db)

    f0_pass = f0_err < 5.0
    Q_pass = Q_err < 20.0
    gain_pass = gain_err < 1.0
    stop_low_pass = rejection_low > 15.0
    stop_high_pass = rejection_high > 15.0

    ch_pass = f0_pass and Q_pass and gain_pass and stop_low_pass and stop_high_pass
    if not ch_pass:
        all_pass = False

    results[ch_num] = {
        'f0_meas': f0_meas, 'f0_err': f0_err, 'f0_pass': f0_pass,
        'Q_meas': Q_meas, 'Q_err': Q_err, 'Q_pass': Q_pass,
        'peak_db': peak_db, 'gain_err': gain_err, 'gain_pass': gain_pass,
        'rejection_low': rejection_low, 'stop_low_pass': stop_low_pass,
        'rejection_high': rejection_high, 'stop_high_pass': stop_high_pass,
        'bw_meas': bw_meas, 'f_low': f_low, 'f_high': f_high,
        'ch_pass': ch_pass,
    }

    status = "PASS" if ch_pass else "FAIL"
    print(f"\n--- Channel {ch_num} ({spec['f0']} Hz, Q={spec['Q']}) --- [{status}]")
    print(f"  f0 measured:    {f0_meas:.1f} Hz  (error: {f0_err:.2f}%)  {'PASS' if f0_pass else 'FAIL'}")
    print(f"  Q measured:     {Q_meas:.3f}  (error: {Q_err:.1f}%)  {'PASS' if Q_pass else 'FAIL'}")
    print(f"  Peak gain:      {peak_db:.2f} dB  (expected: {expected_gain_db:.2f} dB, err: {gain_err:.2f} dB)  {'PASS' if gain_pass else 'FAIL'}")
    print(f"  -3dB BW:        {bw_meas:.1f} Hz  ({f_low:.1f} - {f_high:.1f} Hz)")
    print(f"  Stopband @0.1f0: {stop_low_db:.1f} dB  (rejection: {rejection_low:.1f} dB)  {'PASS' if stop_low_pass else 'FAIL'}")
    print(f"  Stopband @10f0:  {stop_high_db:.1f} dB  (rejection: {rejection_high:.1f} dB)  {'PASS' if stop_high_pass else 'FAIL'}")

print("\n" + "=" * 80)
print(f"OVERALL TB1 RESULT: {'ALL PASS' if all_pass else 'FAIL — see details above'}")
print("=" * 80)

# Save results for later use
np.savez('ac_results.npz', freq=freq, results=results, channels=channels)
