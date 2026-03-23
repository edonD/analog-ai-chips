#!/usr/bin/env python3
"""TB1 Analysis: AC sweep results for all 5 BPF channels (4th-order cascaded)."""
import numpy as np
import json

# 4th-order design: Q_eff = 1.554 * Qs, peak gain = Qs^2
channels = {
    1: {'f0': 224,   'Qs': 0.778, 'Q_eff': 1.209, 'peak_gain_db': -4.36},
    2: {'f0': 1000,  'Qs': 1.160, 'Q_eff': 1.803, 'peak_gain_db': 2.57},
    3: {'f0': 3162,  'Qs': 1.845, 'Q_eff': 2.867, 'peak_gain_db': 10.64},
    4: {'f0': 7071,  'Qs': 2.200, 'Q_eff': 3.419, 'peak_gain_db': 13.70},
    5: {'f0': 14142, 'Qs': 2.200, 'Q_eff': 3.419, 'peak_gain_db': 13.70},
}

results = {}
all_pass = True

print("=" * 78)
print("TB1: AC Sweep — 4th-Order Cascaded BPF Verification")
print("=" * 78)

for ch in range(1, 6):
    spec = channels[ch]
    data = np.loadtxt(f'ac_ch{ch}.txt')
    freq = data[:, 0]
    re = data[:, 1]
    im = data[:, 2]
    mag = np.sqrt(re**2 + im**2)
    mag_db = 20 * np.log10(mag + 1e-30)

    peak_idx = np.argmax(mag_db)
    f0_m = freq[peak_idx]
    peak_db = mag_db[peak_idx]
    expected_gain = spec['peak_gain_db']

    # Q from -3dB bandwidth
    target = peak_db - 3.0
    below = np.where(freq < f0_m)[0]
    above = np.where(freq > f0_m)[0]
    f_low = freq[0]
    if len(below) > 0:
        cx = np.where(np.diff(np.sign(mag_db[below] - target)))[0]
        if len(cx) > 0:
            i = below[cx[-1]]
            f_low = freq[i] + (target - mag_db[i]) / (mag_db[i+1] - mag_db[i]) * (freq[i+1] - freq[i])
    f_high = freq[-1]
    if len(above) > 0:
        cx = np.where(np.diff(np.sign(mag_db[above] - target)))[0]
        if len(cx) > 0:
            i = above[cx[0]]
            f_high = freq[i] + (target - mag_db[i]) / (mag_db[i+1] - mag_db[i]) * (freq[i+1] - freq[i])
    bw = f_high - f_low
    Q_m = f0_m / bw if bw > 0 else 0

    # Stopband
    idx_lo = np.argmin(np.abs(freq - spec['f0'] * 0.1))
    idx_hi = np.argmin(np.abs(freq - min(spec['f0'] * 10, freq[-1]*0.95)))
    rej_lo = peak_db - mag_db[idx_lo]
    rej_hi = peak_db - mag_db[idx_hi]

    # PASS/FAIL
    f0_err = abs(f0_m - spec['f0']) / spec['f0'] * 100
    Q_err = abs(Q_m - spec['Q_eff']) / spec['Q_eff'] * 100
    g_err = abs(peak_db - expected_gain)

    p = {
        'f0': f0_err < 5, 'Q': Q_err < 20, 'gain': g_err < 1,
        'stop_lo': rej_lo > 15, 'stop_hi': rej_hi > 15
    }
    ch_pass = all(p.values())
    if not ch_pass: all_pass = False

    results[ch] = {
        'f0_meas': round(f0_m, 1), 'f0_err_pct': round(f0_err, 2),
        'Q_meas': round(Q_m, 3), 'Q_err_pct': round(Q_err, 1),
        'peak_gain_dB': round(peak_db, 2), 'gain_err_dB': round(g_err, 2),
        'rejection_low_dB': round(rej_lo, 1), 'rejection_high_dB': round(rej_hi, 1),
        'bw_Hz': round(bw, 1), 'pass': ch_pass
    }

    s = "PASS" if ch_pass else "FAIL"
    print(f"\nCh{ch} (f0={spec['f0']}Hz Qs={spec['Qs']} Q_eff={spec['Q_eff']:.2f}) [{s}]")
    print(f"  f0={f0_m:.1f}Hz ({f0_err:.2f}%) Q_eff={Q_m:.3f} ({Q_err:.1f}%)"
          f" Gain={peak_db:.2f}dB (exp:{expected_gain:.2f}dB err:{g_err:.2f}dB)")
    print(f"  BW={bw:.1f}Hz  Stop: {rej_lo:.1f}dB/{rej_hi:.1f}dB")

print(f"\n{'='*78}")
print(f"TB1 OVERALL: {'ALL PASS' if all_pass else 'FAIL'}")
print(f"{'='*78}")

with open('tb1_results.json', 'w') as f:
    json.dump(results, f, indent=2)
