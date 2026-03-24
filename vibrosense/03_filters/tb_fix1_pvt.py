#!/usr/bin/env python3
"""Fix #1: Verify PVT corners with bias distribution network driving the filter.
Instantiates ota_bias_dist + bpf_ch2_real at all 7 corners.
Uses real SKY130 corner models from the minimal lib."""

import subprocess
import numpy as np
import json

corners_to_test = [
    ('tt', 27), ('ss', 27), ('ff', 27), ('sf', 27), ('fs', 27),
    ('tt', -40), ('tt', 85),
]

def run_corner(corner, temp):
    tag = f"fix1_{corner}_{temp}"
    spice = f"""* Fix #1: Ch2 BPF with bias_dist at {corner}/{temp}C
.lib "../01_ota/sky130_minimal.lib.spice" {corner}
.include "../01_ota/ota_foldcasc.spice"
.include "ota_bias_dist.spice"
.temp {temp}

Vdd vdd 0 dc 1.8
Iref vdd iref 500n

* Bias distribution generates VBN/VBP/VBCN/VBCP automatically
Xbdist iref vdd 0 vbn vbcn vbp vbcp ota_bias_dist

Vcm vcm 0 dc 0.9
Vin in 0 dc 0.9 ac 1

* Ch2 BPF using bias_dist outputs (C1=63p, C2=120p as tuned)
Xota1 in int2 int1 vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C1 int1 0 63p
Rbias1 int1 vcm 1G
Xota2 int1 vcm int2 vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C2 int2 0 120p
Rbias2 int2 vcm 1G
Xota3 vcm int1 int1 vdd 0 vbn vbcn vbp vbcp ota_foldcasc

.nodeset v(int1)=0.9 v(int2)=0.9

.control
op
let vbn_v = v(vbn)
let vbcn_v = v(vbcn)
let vbp_v = v(vbp)
let vbcp_v = v(vbcp)
let vout_dc = v(int1)
let isup = -i(vdd)
echo "{corner}_{temp}: VBN=$&vbn_v VBCN=$&vbcn_v VBP=$&vbp_v VBCP=$&vbcp_v Vout=$&vout_dc Isup=$&isup"

ac dec 200 1 200k
wrdata {tag}.txt vdb(int1)
.endc
.end
"""
    with open(f'{tag}.spice', 'w') as f:
        f.write(spice)

    result = subprocess.run(['ngspice', '-b', f'{tag}.spice'],
                          capture_output=True, text=True, timeout=120)

    # Extract bias voltages from output
    bias_line = ''
    for line in (result.stdout + result.stderr).split('\n'):
        if f'{corner}_{temp}:' in line:
            bias_line = line
            break

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
        return f0, Q, pk, bias_line
    except Exception as e:
        return None, None, None, f"FAILED: {e}"


print("=" * 95)
print("Fix #1: Ch2 BPF with ota_bias_dist at ALL 7 PVT corners")
print("=" * 95)
print(f"{'Corner':>8} {'f0(Hz)':>10} {'shift%':>8} {'Q':>8} {'Peak(dB)':>10} {'Status':>8}")
print("-" * 95)

results = {}
for corner, temp in corners_to_test:
    f0, Q, pk, bias_info = run_corner(corner, temp)
    key = f'{corner}_{temp}'
    if f0 and f0 < 100000 and pk > -50:
        shift = (f0 - 1000) / 1000 * 100
        functional = "OK" if pk > -10 else "DEGRADED"
        print(f"{key:>8} {f0:>10.1f} {shift:>+7.1f}% {Q:>8.3f} {pk:>10.2f} {functional:>8}")
        results[key] = {'f0': round(f0, 1), 'Q': round(Q, 3), 'pk': round(pk, 2),
                       'status': functional}
    else:
        print(f"{key:>8} {'DEAD':>10} {'—':>8} {'—':>8} {pk if pk else '—':>10} {'FAIL':>8}")
        results[key] = {'f0': None, 'status': 'DEAD'}
    if bias_info:
        print(f"         {bias_info}")

with open('fix1_pvt_results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Summary
working = sum(1 for r in results.values() if r.get('status') in ('OK', 'DEGRADED'))
print(f"\n{working}/{len(corners_to_test)} corners functional")
