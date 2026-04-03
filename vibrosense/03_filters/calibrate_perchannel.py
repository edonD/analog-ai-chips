#!/usr/bin/env python3
"""Calibrate per-channel bias using Iref-driven VBN diode.
The VBN diode (matched to OTA tail) generates PVT-tracking VBN.
VBP is found by sweeping for OTA balance. VBCN/VBCP from empirical offsets."""
import subprocess, numpy as np, json, re, os

# For Ch2: Iref=218nA (from measured supply current at LE bias)
IREF = 218e-9

corners = [('tt',27),('ss',27),('ff',27),('sf',27),('fs',27),('tt',-40),('tt',85)]

def get_vbn_from_diode(corner, temp, iref):
    """Sim: Iref through diode NMOS (W=3.8u L=14u) → VBN."""
    spice = f""".lib "../01_ota/sky130_minimal.lib.spice" {corner}
.temp {temp}
Vdd vdd 0 dc 1.8
Iref vdd vbn {iref}
XMbn vbn vbn 0 0 sky130_fd_pr__nfet_01v8 W=3.8u L=14u nf=1
.control
op
print v(vbn)
.endc
.end
"""
    with open('/tmp/diode.spice','w') as f: f.write(spice)
    r = subprocess.run(['ngspice','-b','/tmp/diode.spice'], capture_output=True, text=True, timeout=15)
    m = re.search(r'v\(vbn\)\s*=\s*([0-9eE.+-]+)', r.stdout+r.stderr)
    return float(m.group(1)) if m else None

def test_ota_balance(corner, temp, vbn, vbp):
    """Test OTA in unity gain, return Vout."""
    vbcn = vbn + 0.23
    vbcp = vbp - 0.255
    spice = f""".lib "../01_ota/sky130_minimal.lib.spice" {corner}
.include "../01_ota/ota_foldcasc.spice"
.temp {temp}
Vdd vdd 0 dc 1.8
Vbn vbn 0 dc {vbn}
Vbcn vbcn 0 dc {vbcn}
Vbp vbp 0 dc {vbp}
Vbcp vbcp 0 dc {vbcp}
Vin vinp 0 dc 0.9
Xota vinp vout vout vdd 0 vbn vbcn vbp vbcp ota_foldcasc
.control
op
print v(vout)
.endc
.end
"""
    with open('/tmp/bal.spice','w') as f: f.write(spice)
    r = subprocess.run(['ngspice','-b','/tmp/bal.spice'], capture_output=True, text=True, timeout=15)
    m = re.search(r'v\(vout\)\s*=\s*([0-9eE.+-]+)', r.stdout+r.stderr)
    return float(m.group(1)) if m else None

print("Auto-calibrating per-channel bias (Iref=218nA VBN diode)")
print(f"{'Corner':>8} {'VBN':>7} {'VBP':>7} {'VBCN':>7} {'VBCP':>7} {'Vout':>7}")

results = {}
for corner, temp in corners:
    key = f'{corner}_{temp}'
    vbn = get_vbn_from_diode(corner, temp, IREF)
    if vbn is None:
        print(f"{key:>8} VBN DIODE FAILED"); continue

    # Sweep VBP (coarse)
    best_vbp, best_err = None, 10
    for vbp_x1000 in range(600, 950, 10):
        vbp = vbp_x1000/1000.0
        vout = test_ota_balance(corner, temp, vbn, vbp)
        if vout and abs(vout - 0.9) < best_err:
            best_err = abs(vout - 0.9)
            best_vbp = vbp
            best_vout = vout

    if best_vbp:
        # Fine sweep
        for delta in np.arange(-0.008, 0.009, 0.002):
            vbp = best_vbp + delta
            vout = test_ota_balance(corner, temp, vbn, vbp)
            if vout and abs(vout - 0.9) < best_err:
                best_err = abs(vout - 0.9)
                best_vbp = vbp
                best_vout = vout

        vbcn = vbn + 0.23
        vbcp = best_vbp - 0.255
        results[key] = {'vbn':round(vbn,4),'vbp':round(best_vbp,4),
                        'vbcn':round(vbcn,4),'vbcp':round(vbcp,4)}
        print(f"{key:>8} {vbn:>7.4f} {best_vbp:>7.4f} {vbcn:>7.4f} {vbcp:>7.4f} {best_vout:>7.4f}")
    else:
        print(f"{key:>8} VBN={vbn:.4f} — VBP CALIBRATION FAILED")

with open('bias_perchannel_cal.json','w') as f:
    json.dump(results, f, indent=2)
