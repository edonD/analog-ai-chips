#!/usr/bin/env python3
"""Fix #1 (v2): Test filter at all PVT corners using generator-tracked + offset bias."""
import subprocess, numpy as np, json, os

with open('bias_corrected.json') as f:
    bias_all = json.load(f)

corners_to_test = [
    ('tt', 27), ('ss', 27), ('ff', 27), ('sf', 27), ('fs', 27),
    ('tt', -40), ('tt', 85),
]

def run_corner(corner, temp):
    key = f'{corner}_{temp}'
    b = bias_all[key]
    tag = f"fix1c_{key}"
    spice = f"""* Fix #1 corrected: Ch2 at {key}
.lib "../01_ota/sky130_minimal.lib.spice" {corner}
.include "../01_ota/ota_foldcasc.spice"
.temp {temp}
Vdd vdd 0 dc 1.8
Vbn vbn 0 dc {b['vbn']}
Vbcn vbcn 0 dc {b['vbcn']}
Vbp vbp 0 dc {b['vbp']}
Vbcp vbcp 0 dc {b['vbcp']}
Vcm vcm 0 dc 0.9
Vin in 0 dc 0.9 ac 1
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
let isup = -i(vdd)
echo "{key}: Isup=$&isup Vout=$&v(int1)"
ac dec 200 1 200k
wrdata {tag}.txt vdb(int1)
.endc
.end
"""
    with open(f'{tag}.spice', 'w') as f:
        f.write(spice)
    r = subprocess.run(['ngspice', '-b', f'{tag}.spice'], capture_output=True, text=True, timeout=120)
    info = ''
    for line in (r.stdout+r.stderr).split('\n'):
        if key+':' in line: info = line; break
    try:
        data = np.loadtxt(f'{tag}.txt'); freq=data[:,0]; m=data[:,1]
        pi=np.argmax(m); f0=freq[pi]; pk=m[pi]; tgt=pk-3
        fl,fh=freq[0],freq[-1]; bl=np.where(freq<f0)[0]; ab=np.where(freq>f0)[0]
        for i in range(len(bl)-1,0,-1):
            if m[bl[i]]>=tgt and m[bl[i-1]]<tgt: j=bl[i-1]; fl=freq[j]+(tgt-m[j])/(m[j+1]-m[j])*(freq[j+1]-freq[j]); break
        for i in range(len(ab)-1):
            if m[ab[i]]>=tgt and m[ab[i+1]]<tgt: j=ab[i]; fh=freq[j]+(tgt-m[j])/(m[j+1]-m[j])*(freq[j+1]-freq[j]); break
        Q=f0/(fh-fl) if fh>fl else 0
        os.remove(f'{tag}.spice'); os.remove(f'{tag}.txt')
        return f0, Q, pk, info
    except Exception as e:
        return None, None, None, f"FAILED: {e}"

print("="*95)
print("Fix #1: Ch2 BPF at 7 PVT corners (generator-tracked + offset bias)")
print("="*95)
print(f"{'Corner':>8} {'f0(Hz)':>10} {'shift%':>8} {'Q':>8} {'Peak(dB)':>10} {'Status':>10}")

results = {}
for corner, temp in corners_to_test:
    f0, Q, pk, info = run_corner(corner, temp)
    key = f'{corner}_{temp}'
    if f0 and f0 < 100000 and pk > -20:
        shift = (f0 - 1000) / 1000 * 100
        status = "OK" if pk > -5 else "DEGRADED"
        print(f"{key:>8} {f0:>10.1f} {shift:>+7.1f}% {Q:>8.3f} {pk:>10.2f} {status:>10}")
        results[key] = {'f0': round(f0,1), 'Q': round(Q,3), 'pk': round(pk,2), 'status': status}
    else:
        pk_str = f"{pk:.1f}" if pk else "—"
        print(f"{key:>8} {'DEAD':>10} {'—':>8} {'—':>8} {pk_str:>10} {'FAIL':>10}")
        results[key] = {'f0': None, 'status': 'DEAD'}
    if info: print(f"         {info}")

working = sum(1 for r in results.values() if r.get('status') in ('OK','DEGRADED'))
print(f"\n{working}/{len(corners_to_test)} corners functional")
with open('fix1_results.json','w') as f:
    json.dump(results, f, indent=2)
