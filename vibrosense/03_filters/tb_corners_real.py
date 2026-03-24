#!/usr/bin/env python3
"""TB5: Corner sweep using REAL SKY130 PDK corner models.
Tests all 5 channels at tt, ss, ff, sf, fs corners at 27°C.
Also tests tt at -40°C and 85°C (3 temps × tt only, plus 5 corners × 27°C).
"""
import subprocess
import numpy as np
import json

BIAS = {'vbn': 0.565, 'vbp': 0.860, 'vbcn': 0.795, 'vbcp': 0.605}

channels = {
    1: {'f0': 224,   'Q': 0.75, 'c1': 340, 'c2': 510},
    2: {'f0': 1000,  'Q': 0.67, 'c1': 63,  'c2': 120},
    3: {'f0': 3162,  'Q': 1.05, 'c1': 33,  'c2': 25},
    4: {'f0': 7071,  'Q': 1.41, 'c1': 21,  'c2': 8},
    5: {'f0': 14142, 'Q': 1.41, 'c1': 10,  'c2': 4},
}

corners = ['tt', 'ss', 'ff', 'sf', 'fs']
temps = [27]  # Run all corners at 27°C; add -40/85 for tt only

def run_corner(ch, corner, temp):
    spec = channels[ch]
    tag = f"corner_ch{ch}_{corner}_{temp}"
    spice = f"""* Corner: {corner} Temp: {temp}C Ch{ch}
.lib "../01_ota/sky130_minimal.lib.spice" {corner}
.include "../01_ota/ota_foldcasc.spice"
.temp {temp}
Vdd vdd 0 dc 1.8
Vbn vbn 0 dc {BIAS['vbn']}
Vbcn vbcn 0 dc {BIAS['vbcn']}
Vbp vbp 0 dc {BIAS['vbp']}
Vbcp vbcp 0 dc {BIAS['vbcp']}
Vcm vcm 0 dc 0.9
Vss vss 0 dc 0
Vin in 0 dc 0.9 ac 1
Xota1 in int2 int1 vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C1 int1 0 {spec['c1']}p
Rbias1 int1 vcm 1G
Xota2 int1 vcm int2 vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C2 int2 0 {spec['c2']}p
Rbias2 int2 vcm 1G
Xota3 vcm int1 int1 vdd 0 vbn vbcn vbp vbcp ota_foldcasc
.nodeset v(int1)=0.9 v(int2)=0.9
.control
op
ac dec 200 1 200k
wrdata {tag}.txt vdb(int1)
.endc
.end
"""
    with open(f'{tag}.spice', 'w') as f:
        f.write(spice)
    result = subprocess.run(['ngspice', '-b', f'{tag}.spice'],
                          capture_output=True, text=True, timeout=120)
    try:
        data = np.loadtxt(f'{tag}.txt')
        freq = data[:, 0]; mag_db = data[:, 1]
        pi = np.argmax(mag_db); f0 = freq[pi]; pk = mag_db[pi]
        tgt = pk - 3; fl = freq[0]; fh = freq[-1]
        bl = np.where(freq < f0)[0]; ab = np.where(freq > f0)[0]
        for i in range(len(bl)-1, 0, -1):
            if mag_db[bl[i]] >= tgt and mag_db[bl[i-1]] < tgt:
                j = bl[i-1]; fl = freq[j] + (tgt-mag_db[j])/(mag_db[j+1]-mag_db[j])*(freq[j+1]-freq[j]); break
        for i in range(len(ab)-1):
            if mag_db[ab[i]] >= tgt and mag_db[ab[i+1]] < tgt:
                j = ab[i]; fh = freq[j] + (tgt-mag_db[j])/(mag_db[j+1]-mag_db[j])*(freq[j+1]-freq[j]); break
        Q = f0/(fh-fl) if fh > fl else 0
        import os
        os.remove(f'{tag}.spice')
        os.remove(f'{tag}.txt')
        return f0, Q, pk
    except Exception as e:
        return None, None, None

print("=" * 90)
print("TB5: Corner Sweep — Real SKY130 PDK Models")
print("=" * 90)

results = {}
for ch in range(1, 6):
    spec = channels[ch]
    print(f"\n--- Ch{ch} (f0={spec['f0']}Hz Q={spec['Q']}) ---")
    print(f"{'Corner':>8} {'Temp':>5} {'f0(Hz)':>10} {'shift%':>8} {'Q':>8} {'Peak(dB)':>10}")
    ch_results = {}
    for corner in corners:
        for temp in temps:
            f0, Q, pk = run_corner(ch, corner, temp)
            if f0:
                shift = (f0 - spec['f0']) / spec['f0'] * 100
                ch_results[f'{corner}_{temp}'] = {'f0': round(f0, 1), 'Q': round(Q, 3), 'pk': round(pk, 2)}
                print(f"{corner:>8} {temp:>5} {f0:>10.1f} {shift:>+7.1f}% {Q:>8.3f} {pk:>10.2f}")
            else:
                print(f"{corner:>8} {temp:>5}    FAILED")
                ch_results[f'{corner}_{temp}'] = None

    # Also run tt at -40°C and 85°C
    for temp in [-40, 85]:
        f0, Q, pk = run_corner(ch, 'tt', temp)
        if f0:
            shift = (f0 - spec['f0']) / spec['f0'] * 100
            ch_results[f'tt_{temp}'] = {'f0': round(f0, 1), 'Q': round(Q, 3), 'pk': round(pk, 2)}
            print(f"{'tt':>8} {temp:>5} {f0:>10.1f} {shift:>+7.1f}% {Q:>8.3f} {pk:>10.2f}")
        else:
            print(f"{'tt':>8} {temp:>5}    FAILED")

    results[ch] = ch_results

# Summary
print(f"\n{'='*90}")
print("Corner Summary (untuned f0 variation):")
print(f"{'='*90}")
for ch in range(1, 6):
    f0_vals = [r['f0'] for r in results[ch].values() if r is not None]
    if f0_vals:
        f0_min, f0_max = min(f0_vals), max(f0_vals)
        spec = channels[ch]
        print(f"Ch{ch}: f0_nom={spec['f0']}  f0_min={f0_min:.0f}  f0_max={f0_max:.0f}  "
              f"range: {(f0_min-spec['f0'])/spec['f0']*100:+.0f}% to {(f0_max-spec['f0'])/spec['f0']*100:+.0f}%")

with open('tb5_corners_real.json', 'w') as f:
    json.dump(results, f, indent=2)
