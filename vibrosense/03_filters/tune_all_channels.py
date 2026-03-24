#!/usr/bin/env python3
"""
Iteratively tune C1/C2 for each channel to hit target f0 and Q
using the real transistor-level OTA at LE bias.

Strategy: binary search on C scale factor to hit f0,
then adjust C1/C2 ratio to hit Q.
"""

import subprocess
import numpy as np
import os

# All channels use LE bias
BIAS = {'vbn': 0.565, 'vbp': 0.860, 'vbcn': 0.795, 'vbcp': 0.605}

channels = {
    1: {'f0': 224,   'Q': 0.75, 'c1_init': 335, 'c2_init': 596},
    2: {'f0': 1000,  'Q': 0.67, 'c1_init': 63,  'c2_init': 120},  # already tuned
    3: {'f0': 3162,  'Q': 1.05, 'c1_init': 33,  'c2_init': 30},
    4: {'f0': 7071,  'Q': 1.41, 'c1_init': 20,  'c2_init': 10},
    5: {'f0': 14142, 'Q': 1.41, 'c1_init': 10,  'c2_init': 5},
}


def run_ac_sim(c1_pf, c2_pf, tag):
    """Run AC sim and return (f0_measured, Q_measured, peak_gain_dB)."""
    spice = f"""* Auto-tune: C1={c1_pf}p C2={c2_pf}p
.lib "../01_ota/sky130_minimal.lib.spice" tt
.include "../01_ota/ota_foldcasc.spice"
Vdd vdd 0 dc 1.8
Vbn vbn 0 dc {BIAS['vbn']}
Vbcn vbcn 0 dc {BIAS['vbcn']}
Vbp vbp 0 dc {BIAS['vbp']}
Vbcp vbcp 0 dc {BIAS['vbcp']}
Vcm vcm 0 dc 0.9
Vin in 0 dc 0.9 ac 1
Xota1 in int2 int1 vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C1 int1 0 {c1_pf}p
Rbias1 int1 vcm 1G
Xota2 int1 vcm int2 vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C2 int2 0 {c2_pf}p
Rbias2 int2 vcm 1G
Xota3 vcm int1 int1 vdd 0 vbn vbcn vbp vbcp ota_foldcasc
.nodeset v(int1)=0.9 v(int2)=0.9
.control
op
ac dec 200 1 200k
wrdata tune_{tag}.txt vdb(int1)
.endc
.end
"""
    fname = f'tune_{tag}.spice'
    with open(fname, 'w') as f:
        f.write(spice)

    result = subprocess.run(['ngspice', '-b', fname],
                          capture_output=True, text=True, timeout=60)

    data = np.loadtxt(f'tune_{tag}.txt')
    freq = data[:, 0]
    mag_db = data[:, 1]

    peak_idx = np.argmax(mag_db)
    f0 = freq[peak_idx]
    peak = mag_db[peak_idx]

    # Q from -3dB BW
    target = peak - 3
    f_low, f_high = freq[0], freq[-1]
    below = np.where(freq < f0)[0]
    above = np.where(freq > f0)[0]
    for i in range(len(below)-1, 0, -1):
        if mag_db[below[i]] >= target and mag_db[below[i-1]] < target:
            j = below[i-1]
            f_low = freq[j] + (target-mag_db[j])/(mag_db[j+1]-mag_db[j])*(freq[j+1]-freq[j])
            break
    for i in range(len(above)-1):
        if mag_db[above[i]] >= target and mag_db[above[i+1]] < target:
            j = above[i]
            f_high = freq[j] + (target-mag_db[j])/(mag_db[j+1]-mag_db[j])*(freq[j+1]-freq[j])
            break
    bw = f_high - f_low
    Q = f0 / bw if bw > 0 else 0

    # Stopband
    idx_lo = np.argmin(abs(freq - f0*0.1))
    idx_hi = np.argmin(abs(freq - min(f0*10, freq[-1]*0.95)))
    rej_lo = peak - mag_db[idx_lo]
    rej_hi = peak - mag_db[idx_hi]

    # Clean up
    os.remove(fname)
    os.remove(f'tune_{tag}.txt')

    return f0, Q, peak, rej_lo, rej_hi


print("=" * 80)
print("Channel Auto-Tuning with Real SKY130 OTA")
print("=" * 80)

results = {}

for ch_num, spec in channels.items():
    if ch_num == 2:
        # Already tuned
        results[ch_num] = {'c1': 63, 'c2': 120, 'f0': 1035, 'Q': 0.659,
                          'peak': -1.67, 'rej_lo': 16.8, 'rej_hi': 16.0}
        print(f"\nCh{ch_num}: ALREADY TUNED — C1=63p C2=120p f0=1035 Q=0.659")
        continue

    print(f"\n--- Tuning Ch{ch_num} (f0={spec['f0']}Hz Q={spec['Q']}) ---")

    c1 = spec['c1_init']
    c2 = spec['c2_init']
    f0_target = spec['f0']
    Q_target = spec['Q']

    # Step 1: Coarse f0 tuning (scale both C proportionally)
    for iteration in range(8):
        f0_m, Q_m, pk, rl, rh = run_ac_sim(c1, c2, f'ch{ch_num}_i{iteration}')
        print(f"  iter{iteration}: C1={c1:.1f}p C2={c2:.1f}p → f0={f0_m:.1f}Hz Q={Q_m:.3f} pk={pk:.2f}dB")

        f0_err = (f0_m - f0_target) / f0_target
        Q_err = (Q_m - Q_target) / Q_target

        if abs(f0_err) < 0.05 and abs(Q_err) < 0.15:
            print(f"  CONVERGED: f0 err={f0_err*100:.1f}%, Q err={Q_err*100:.1f}%")
            results[ch_num] = {'c1': round(c1, 1), 'c2': round(c2, 1),
                              'f0': round(f0_m, 1), 'Q': round(Q_m, 3),
                              'peak': round(pk, 2), 'rej_lo': round(rl, 1),
                              'rej_hi': round(rh, 1)}
            break

        # Adjust f0: f0 ∝ 1/sqrt(C1*C2), so to increase f0, decrease C
        if abs(f0_err) > 0.03:
            # f0_m/f0_target = sqrt(C_needed/C_actual)
            # C_new = C_old × (f0_m/f0_target)² → decreases C when f0 too low
            scale2 = (f0_m / f0_target) ** 2
            c1 = c1 * scale2
            c2 = c2 * scale2

        # Adjust Q: change C1/C2 ratio
        if abs(Q_err) > 0.10:
            # Q = sqrt(C1_eff/C2_eff), increase C1/C2 to increase Q
            q_scale = (Q_target / Q_m) ** 0.5  # partial correction
            c1_new = c1 * q_scale
            c2_new = c2 / q_scale
            # Keep geometric mean constant (preserve f0)
            geo = np.sqrt(c1 * c2)
            geo_new = np.sqrt(c1_new * c2_new)
            c1 = c1_new * geo / geo_new
            c2 = c2_new * geo / geo_new
    else:
        # Didn't converge, save last result
        results[ch_num] = {'c1': round(c1, 1), 'c2': round(c2, 1),
                          'f0': round(f0_m, 1), 'Q': round(Q_m, 3),
                          'peak': round(pk, 2), 'rej_lo': round(rl, 1),
                          'rej_hi': round(rh, 1)}
        print(f"  NOT CONVERGED after 8 iterations")

print("\n" + "=" * 80)
print("FINAL TUNED PARAMETERS:")
print("=" * 80)
print(f"{'Ch':>3} {'f0_tgt':>7} {'f0_meas':>8} {'err%':>6} {'Q_tgt':>6} {'Q_meas':>7} {'C1(pF)':>7} {'C2(pF)':>7} {'Peak':>6} {'R_lo':>5} {'R_hi':>5}")
for ch_num in sorted(results.keys()):
    r = results[ch_num]
    spec = channels[ch_num]
    f0_err = abs(r['f0'] - spec['f0']) / spec['f0'] * 100
    Q_err = abs(r['Q'] - spec['Q']) / spec['Q'] * 100
    pf = 'P' if f0_err < 5 else 'F'
    pq = 'P' if Q_err < 20 else 'F'
    print(f"{ch_num:>3} {spec['f0']:>7} {r['f0']:>8.1f} {f0_err:>5.1f}%[{pf}] {spec['Q']:>5.2f} {r['Q']:>7.3f}[{pq}] {r['c1']:>7.1f} {r['c2']:>7.1f} {r['peak']:>6.2f} {r['rej_lo']:>5.1f} {r['rej_hi']:>5.1f}")

import json
with open('tuned_channels.json', 'w') as f:
    json.dump(results, f, indent=2)
