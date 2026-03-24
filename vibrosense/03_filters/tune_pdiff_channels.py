#!/usr/bin/env python3
"""Tune pseudo-differential channel cap values by iterating in ngspice.
Uses ota_bias_dist v8 with per-channel Iref."""
import subprocess, numpy as np, json, os

channels = {
    1: {'f0': 224,   'Q': 0.75, 'iref': 50,  'c1_init': 77,  'c2_init': 137},
    2: {'f0': 1000,  'Q': 0.67, 'iref': 70,  'c1_init': 39,  'c2_init': 86},
    3: {'f0': 3162,  'Q': 1.05, 'iref': 150, 'c1_init': 23,  'c2_init': 21},
    4: {'f0': 7071,  'Q': 1.41, 'iref': 440, 'c1_init': 20,  'c2_init': 10},
    5: {'f0': 14142, 'Q': 1.41, 'iref': 870, 'c1_init': 10,  'c2_init': 5},
}

def run_pdiff_ac(ch, c1, c2, iref):
    """Run pseudo-diff filter AC sweep, return f0, Q, peak."""
    tag = f"ptune_{ch}"
    spice = f""".lib "../01_ota/sky130_minimal.lib.spice" tt
.include "../01_ota/ota_foldcasc.spice"
.include "pseudo_res.spice"
.include "ota_bias_dist.spice"
Vdd vdd 0 dc 1.8
Iref vdd iref {iref}n
Xbdist iref vdd 0 vbn vbcn vbp vbcp ota_bias_dist
Vcm vcm 0 dc 0.9
Vinp inp 0 dc 0.9 ac 0.5
Vinn inn 0 dc 0.9 ac -0.5
* Positive path
Xota1p inp int2p int1p vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C1p int1p 0 {c1}p
Xpr1p int1p vcm pseudo_res
Xota2p int1p vcm int2p vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C2p int2p 0 {c2}p
Xpr2p int2p vcm pseudo_res
Xota3p vcm int1p int1p vdd 0 vbn vbcn vbp vbcp ota_foldcasc
* Negative path
Xota1n inn int2n int1n vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C1n int1n 0 {c1}p
Xpr1n int1n vcm pseudo_res
Xota2n int1n vcm int2n vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C2n int2n 0 {c2}p
Xpr2n int2n vcm pseudo_res
Xota3n vcm int1n int1n vdd 0 vbn vbcn vbp vbcp ota_foldcasc
.nodeset v(int1p)=0.9 v(int2p)=0.9 v(int1n)=0.9 v(int2n)=0.9
.control
op
ac dec 200 1 200k
wrdata {tag}.txt vdb(int1p,int1n)
.endc
.end
"""
    with open(f'{tag}.spice','w') as f: f.write(spice)
    subprocess.run(['ngspice','-b',f'{tag}.spice'], capture_output=True, text=True, timeout=120)
    try:
        data = np.loadtxt(f'{tag}.txt'); freq=data[:,0]; m=data[:,1]
        pi=np.argmax(m); f0=freq[pi]; pk=m[pi]; tgt=pk-3
        fl,fh=freq[0],freq[-1]; bl=np.where(freq<f0)[0]; ab=np.where(freq>f0)[0]
        for i in range(len(bl)-1,0,-1):
            if m[bl[i]]>=tgt and m[bl[i-1]]<tgt: j=bl[i-1]; fl=freq[j]+(tgt-m[j])/(m[j+1]-m[j])*(freq[j+1]-freq[j]); break
        for i in range(len(ab)-1):
            if m[ab[i]]>=tgt and m[ab[i+1]]<tgt: j=ab[i]; fh=freq[j]+(tgt-m[j])/(m[j+1]-m[j])*(freq[j+1]-freq[j]); break
        Q = f0/(fh-fl) if fh>fl else 0
        os.remove(f'{tag}.spice'); os.remove(f'{tag}.txt')
        return f0, Q, pk
    except:
        return None, None, None

print("="*80)
print("Tuning pseudo-differential channels with ota_bias_dist")
print("="*80)

results = {}
for ch, spec in channels.items():
    f0_tgt = spec['f0']; Q_tgt = spec['Q']; iref = spec['iref']
    c1 = spec['c1_init']; c2 = spec['c2_init']

    print(f"\n--- Ch{ch} (f0={f0_tgt}Hz Q={Q_tgt} Iref={iref}nA) ---")

    for iteration in range(10):
        f0, Q, pk = run_pdiff_ac(ch, c1, c2, iref)
        if f0 is None or f0 > 100000 or pk < -30:
            print(f"  iter{iteration}: C1={c1:.1f}p C2={c2:.1f}p → DEAD")
            # Try scaling caps up (filter too unstable at small C)
            c1 *= 1.5; c2 *= 1.5
            continue

        f0_err = (f0 - f0_tgt) / f0_tgt
        Q_err = (Q - Q_tgt) / Q_tgt
        print(f"  iter{iteration}: C1={c1:.1f}p C2={c2:.1f}p → f0={f0:.1f}Hz ({f0_err*100:+.1f}%) Q={Q:.3f} ({Q_err*100:+.1f}%) pk={pk:.2f}dB")

        if abs(f0_err) < 0.08 and abs(Q_err) < 0.15:
            results[ch] = {'c1': round(c1,1), 'c2': round(c2,1), 'f0': round(f0,1), 'Q': round(Q,3), 'pk': round(pk,2)}
            print(f"  CONVERGED")
            break

        # Adjust f0: scale both C by (f0/f0_tgt)²
        if abs(f0_err) > 0.05:
            scale = (f0/f0_tgt)**2
            c1 *= scale; c2 *= scale

        # Adjust Q: change C1/C2 ratio
        if abs(Q_err) > 0.10:
            q_scale = (Q_tgt/Q)**0.3
            geo = np.sqrt(c1*c2)
            c1 *= q_scale; c2 /= q_scale
            geo_new = np.sqrt(c1*c2)
            c1 *= geo/geo_new; c2 *= geo/geo_new
    else:
        results[ch] = {'c1': round(c1,1), 'c2': round(c2,1), 'f0': round(f0,1) if f0 else None,
                       'Q': round(Q,3) if Q else None, 'pk': round(pk,2) if pk else None}
        print(f"  NOT CONVERGED")

print("\n" + "="*80)
print("FINAL TUNED PARAMETERS:")
print("="*80)
print(f"{'Ch':>3} {'f0_tgt':>7} {'f0_meas':>8} {'err%':>6} {'Q_tgt':>6} {'Q_meas':>7} {'C1(pF)':>7} {'C2(pF)':>7} {'Peak':>6}")
for ch in sorted(results.keys()):
    r = results[ch]; s = channels[ch]
    if r.get('f0'):
        fe = abs(r['f0']-s['f0'])/s['f0']*100
        qe = abs(r['Q']-s['Q'])/s['Q']*100
        print(f"{ch:>3} {s['f0']:>7} {r['f0']:>8.1f} {fe:>5.1f}% {s['Q']:>5.2f} {r['Q']:>7.3f} {r['c1']:>7.1f} {r['c2']:>7.1f} {r['pk']:>6.2f}")
    else:
        print(f"{ch:>3} {s['f0']:>7} {'FAIL':>8}")

with open('pdiff_tuned.json','w') as f:
    json.dump(results, f, indent=2)
