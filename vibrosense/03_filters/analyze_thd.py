#!/usr/bin/env python3
"""TB3: THD measurement for all 5 BPF channels.

Note: With behavioral (linear) OTA, THD is essentially 0.
This validates the topology and measurement methodology.
Real THD requires transistor-level OTA simulation.
"""
import numpy as np
import json

channels = {
    1: {'f0': 224,   'Q': 0.75},
    2: {'f0': 1000,  'Q': 0.67},
    3: {'f0': 3162,  'Q': 1.05},
    4: {'f0': 7071,  'Q': 1.41},
    5: {'f0': 14142, 'Q': 1.41},
}

print("=" * 78)
print("TB3: THD Measurement — All Channels (200 mVpp input at f0)")
print("=" * 78)
print("\nNote: Behavioral OTA is perfectly linear → THD limited by numerical noise.")
print("Real THD requires transistor-level OTA. Results below validate methodology.\n")

results = {}
all_pass = True

for ch in range(1, 6):
    spec = channels[ch]
    f0 = spec['f0']

    data = np.loadtxt(f'thd_ch{ch}.txt')
    time = data[:, 0]
    vout = data[:, 1]  # wrdata gives real part only for transient

    # Remove DC (output sits at ~Vcm = 0.9V)
    vout_ac = vout - np.mean(vout)

    # Use last N complete cycles for FFT
    T = 1.0 / f0
    # Find how many complete cycles fit in the data
    t_total = time[-1] - time[0]
    n_cycles = int(t_total * f0)
    if n_cycles < 5:
        n_cycles = max(1, n_cycles)

    # Take exactly n_cycles worth of data from the end (steady state)
    t_start = time[-1] - n_cycles * T
    mask = time >= t_start
    t_seg = time[mask]
    v_seg = vout_ac[mask]

    # FFT
    N = len(v_seg)
    dt = np.mean(np.diff(t_seg))
    fft_vals = np.fft.rfft(v_seg * np.hanning(N))
    fft_mag = 2.0 * np.abs(fft_vals) / N
    fft_freqs = np.fft.rfftfreq(N, dt)

    # Find fundamental
    fund_idx = np.argmin(np.abs(fft_freqs - f0))
    fund_mag = fft_mag[fund_idx]

    # Find harmonics
    harmonics = {}
    for h in [2, 3, 4, 5]:
        h_idx = np.argmin(np.abs(fft_freqs - h * f0))
        h_mag = fft_mag[h_idx]
        if fund_mag > 0:
            h_db = 20 * np.log10(h_mag / fund_mag + 1e-30)
        else:
            h_db = -200
        harmonics[h] = h_db

    # THD
    hd_sum = sum([(fft_mag[np.argmin(np.abs(fft_freqs - h * f0))])**2
                   for h in [2, 3, 4, 5]])
    thd_ratio = np.sqrt(hd_sum) / (fund_mag + 1e-30)
    thd_dbc = 20 * np.log10(thd_ratio + 1e-30)

    passes = thd_dbc < -30
    if not passes:
        all_pass = False

    results[ch] = {
        'fundamental_V': round(float(fund_mag), 6),
        'HD2_dBc': round(harmonics[2], 1),
        'HD3_dBc': round(harmonics[3], 1),
        'HD4_dBc': round(harmonics[4], 1),
        'HD5_dBc': round(harmonics[5], 1),
        'THD_dBc': round(float(thd_dbc), 1),
        'pass': bool(passes),
    }

    print(f"Ch{ch} (f0={f0}Hz): Fund={fund_mag*1000:.3f}mV  "
          f"HD2={harmonics[2]:.0f}dBc HD3={harmonics[3]:.0f}dBc "
          f"THD={thd_dbc:.1f}dBc {'PASS' if passes else 'FAIL'}")

print(f"\n{'='*78}")
print(f"TB3 OVERALL: {'ALL PASS' if all_pass else 'FAIL'}")
print(f"{'='*78}")
print("\nConclusion: Behavioral OTA produces THD << -30 dBc (numerical floor).")
print("When replaced with transistor-level OTA, THD will increase due to")
print("gm nonlinearity. Expected: -40 to -50 dBc for folded-cascode OTA")
print("at 200 mVpp input (well within -30 dBc spec).")

with open('tb3_results.json', 'w') as f:
    json.dump(results, f, indent=2)
