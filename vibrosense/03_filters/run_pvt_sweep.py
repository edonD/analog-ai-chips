#!/usr/bin/env python3
"""Run filter at all PVT corners using bias generator-derived voltages.
Tests Ch2 first, then all channels at worst corners."""
import subprocess
import numpy as np
import json
import os

# Load bias voltages from corners
with open('bias_corners.json') as f:
    bias_corners = json.load(f)

# Channel caps — using default bias (~2µS gm) since bias gen operates at ~500nA
# Need to retune caps for the default bias gen output
# At tt_27: VBN=0.628, VBP=0.690 — this is DIFFERENT from our LE bias (0.565/0.860)
# The bias gen's own operating point is near the OTA's designed L0 level!
# gm at this bias should be ~2µS (near default)

# For Ch2 at default bias: f0=1000Hz, need sqrt(C1*C2)≈337pF
# Q=0.67: C1≈226pF, C2≈503pF
# Pre-compensate parasitic: C1≈211pF, C2≈495pF (rough estimate)

channels = {
    2: {'f0': 1000, 'Q': 0.67, 'c1': 200, 'c2': 490},  # first guess, will iterate
}

corners_to_test = ['tt_27', 'ss_27', 'ff_27', 'sf_27', 'fs_27', 'tt_-40', 'tt_85']

def run_filter_corner(ch, corner_key, c1, c2):
    b = bias_corners[corner_key]
    parts = corner_key.split('_')
    corner = parts[0]
    temp = int(parts[1])
    tag = f"pvt_ch{ch}_{corner_key}"

    spice = f"""* PVT: Ch{ch} {corner_key}
.lib "../01_ota/sky130_minimal.lib.spice" {corner}
.include "../01_ota/ota_foldcasc.spice"
.temp {temp}
Vdd vdd 0 dc 1.8
Vbn vbn 0 dc {b['vbn']}
Vbcn vbcn 0 dc {b['vbcn']}
Vbp vbp 0 dc {b['vbp']}
Vbcp vbcp 0 dc {b['vbcp']}
Vcm vcm 0 dc 0.9
Vss vss 0 dc 0
Vin in 0 dc 0.9 ac 1
Xota1 in int2 int1 vdd vss vbn vbcn vbp vbcp ota_foldcasc
C1 int1 vss {c1}p
Rbias1 int1 vcm 1G
Xota2 int1 vcm int2 vdd vss vbn vbcn vbp vbcp ota_foldcasc
C2 int2 vss {c2}p
Rbias2 int2 vcm 1G
Xota3 vcm int1 int1 vdd vss vbn vbcn vbp vbcp ota_foldcasc
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
        os.remove(f'{tag}.spice')
        os.remove(f'{tag}.txt')
        return f0, Q, pk
    except:
        return None, None, None

# Test Ch2 at tt_27 to verify caps
print("Testing Ch2 at different C values with bias gen voltages:")
for c1, c2 in [(200, 490), (180, 480), (160, 460), (190, 470), (195, 475)]:
    f0, Q, pk = run_filter_corner(2, 'tt_27', c1, c2)
    if f0:
        print(f"  C1={c1}p C2={c2}p → f0={f0:.1f}Hz Q={Q:.3f} pk={pk:.2f}dB")

# Now run at all corners with best caps
print("\nPVT Sweep — Ch2 (will pick best C from above):")
best_c1, best_c2 = 195, 475  # adjust based on above results
for ck in corners_to_test:
    f0, Q, pk = run_filter_corner(2, ck, best_c1, best_c2)
    if f0:
        spec_f0 = 1000
        shift = (f0 - spec_f0) / spec_f0 * 100
        print(f"  {ck:>8}: f0={f0:>8.1f}Hz ({shift:>+6.1f}%) Q={Q:.3f} pk={pk:.2f}dB")
    else:
        print(f"  {ck:>8}: FAILED")
