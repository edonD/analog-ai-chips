#!/usr/bin/env python3
"""TB5: Corner and Temperature Sweep — untuned (DAC code=8).
Documents f0/Q/gain variation across 15 PVT conditions.
Uses analytical model (f0 scales linearly with gm for behavioral OTA)
verified by ngspice spot checks.
"""
import numpy as np
import subprocess
import json

channels = {
    1: {'f0': 224,   'Q': 0.75},
    2: {'f0': 1000,  'Q': 0.67},
    3: {'f0': 3162,  'Q': 1.05},
    4: {'f0': 7071,  'Q': 1.41},
    5: {'f0': 14142, 'Q': 1.41},
}

pvt_conditions = {
    'TT_n40': 1.0 * (300.15 / 233.15),
    'TT_27':  1.0,
    'TT_85':  1.0 * (300.15 / 358.15),
    'FF_n40': 1.25 * (300.15 / 233.15),
    'FF_27':  1.25,
    'FF_85':  1.25 * (300.15 / 358.15),
    'SS_n40': 0.75 * (300.15 / 233.15),
    'SS_27':  0.75,
    'SS_85':  0.75 * (300.15 / 358.15),
    'FS_n40': 0.90 * (300.15 / 233.15),
    'FS_27':  0.90,
    'FS_85':  0.90 * (300.15 / 358.15),
    'SF_n40': 1.10 * (300.15 / 233.15),
    'SF_27':  1.10,
    'SF_85':  1.10 * (300.15 / 358.15),
}

def run_ngspice_ac(ch, gm_scale):
    """Run AC sweep for one channel at one gm_scale."""
    spice = f"""* TB5 corner sweep: Ch{ch} gm_scale={gm_scale:.4f}
.include bpf_ch{ch}.spice
Vdd vdd 0 1.8
Vss vss 0 0
Vcm vcm 0 0.9
Vin in 0 DC 0.9 AC 1
Xbpf in bp_out vdd vss vcm bpf_ch{ch} gm_scale={gm_scale}
.control
ac dec 300 1 200k
wrdata tb5_temp.txt v(bp_out)
.endc
.end
"""
    with open('tb5_temp.spice', 'w') as f:
        f.write(spice)
    subprocess.run(['ngspice', '-b', 'tb5_temp.spice'],
                  capture_output=True, timeout=30)
    data = np.loadtxt('tb5_temp.txt')
    freq = data[:, 0]
    mag = np.sqrt(data[:, 1]**2 + data[:, 2]**2)
    mag_db = 20 * np.log10(mag + 1e-30)

    peak_idx = np.argmax(mag_db)
    f0_m = freq[peak_idx]
    peak_db = mag_db[peak_idx]

    # Q from -3dB BW
    target = peak_db - 3.0
    below = np.where(freq < f0_m)[0]
    above = np.where(freq > f0_m)[0]
    f_low, f_high = freq[0], freq[-1]
    if len(below) > 0:
        cx = np.where(np.diff(np.sign(mag_db[below] - target)))[0]
        if len(cx) > 0:
            i = below[cx[-1]]
            f_low = freq[i] + (target - mag_db[i]) / (mag_db[i+1] - mag_db[i]) * (freq[i+1] - freq[i])
    if len(above) > 0:
        cx = np.where(np.diff(np.sign(mag_db[above] - target)))[0]
        if len(cx) > 0:
            i = above[cx[0]]
            f_high = freq[i] + (target - mag_db[i]) / (mag_db[i+1] - mag_db[i]) * (freq[i+1] - freq[i])
    bw = f_high - f_low
    Q_m = f0_m / bw if bw > 0 else 0

    return f0_m, Q_m, peak_db

print("=" * 90)
print("TB5: Corner/Temperature Sweep — Untuned (DAC code=8)")
print("=" * 90)

results = {}

for ch in range(1, 6):
    spec = channels[ch]
    print(f"\n{'─'*90}")
    print(f"Channel {ch}: f0_nom={spec['f0']}Hz Q_nom={spec['Q']}")
    print(f"{'─'*90}")
    print(f"{'Corner':<12} {'f0(Hz)':>10} {'f0 shift%':>10} {'Q':>8} {'Q shift%':>10} {'Gain(dB)':>10}")

    ch_data = {}
    f0_vals = []
    Q_vals = []

    for pvt_name in sorted(pvt_conditions.keys()):
        pvt_factor = pvt_conditions[pvt_name]
        f0_m, Q_m, gain_db = run_ngspice_ac(ch, pvt_factor)
        f0_shift = (f0_m - spec['f0']) / spec['f0'] * 100
        Q_shift = (Q_m - spec['Q']) / spec['Q'] * 100
        f0_vals.append(f0_m)
        Q_vals.append(Q_m)

        ch_data[pvt_name] = {
            'f0_Hz': round(f0_m, 1),
            'f0_shift_pct': round(f0_shift, 1),
            'Q': round(Q_m, 3),
            'Q_shift_pct': round(Q_shift, 1),
            'gain_dB': round(gain_db, 2),
        }
        print(f"{pvt_name:<12} {f0_m:>10.1f} {f0_shift:>+9.1f}% {Q_m:>8.3f} "
              f"{Q_shift:>+9.1f}% {gain_db:>10.2f}")

    f0_range = (min(f0_vals), max(f0_vals))
    Q_range = (min(Q_vals), max(Q_vals))
    print(f"  f0 range: {f0_range[0]:.1f} — {f0_range[1]:.1f} Hz "
          f"({(f0_range[0]-spec['f0'])/spec['f0']*100:+.1f}% to "
          f"{(f0_range[1]-spec['f0'])/spec['f0']*100:+.1f}%)")
    print(f"  Q range:  {Q_range[0]:.3f} — {Q_range[1]:.3f}")

    results[ch] = {
        'pvt_data': ch_data,
        'f0_min': round(f0_range[0], 1),
        'f0_max': round(f0_range[1], 1),
        'Q_min': round(Q_range[0], 3),
        'Q_max': round(Q_range[1], 3),
    }

print(f"\n{'='*90}")
print("TB5 Summary: Untuned PVT variation (demonstrates need for DAC tuning)")
print(f"{'='*90}")
print(f"{'Ch':<4} {'f0_nom':>8} {'f0_min':>10} {'f0_max':>10} {'Range%':>10} "
      f"{'Q_nom':>8} {'Q_min':>8} {'Q_max':>8}")
for ch in range(1, 6):
    r = results[ch]
    s = channels[ch]
    rng = (r['f0_max'] - r['f0_min']) / s['f0'] * 100
    print(f"{ch:<4} {s['f0']:>8} {r['f0_min']:>10.1f} {r['f0_max']:>10.1f} "
          f"{rng:>9.1f}% {s['Q']:>8.2f} {r['Q_min']:>8.3f} {r['Q_max']:>8.3f}")

with open('tb5_results.json', 'w') as f:
    json.dump(results, f, indent=2)
