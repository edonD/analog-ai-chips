#!/usr/bin/env python3
"""Auto-calibrate OTA bias voltages at each PVT corner.
Strategy: sweep VBP while keeping VBN from the bias generator output,
and find VBP where OTA output ≈ 0.9V (balanced). Then derive VBCN/VBCP."""
import subprocess, numpy as np, json, re

# Load generator outputs
with open('bias_corners.json') as f:
    gen = json.load(f)

corners = [('tt',27),('ss',27),('ff',27),('sf',27),('fs',27),('tt',-40),('tt',85)]

def run_ota_op(corner, temp, vbn, vbp, vbcn, vbcp):
    """Run OTA in unity-gain and measure Vout."""
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
print v(vout) -i(vdd)
.endc
.end
"""
    with open('/tmp/cal.spice','w') as f: f.write(spice)
    r = subprocess.run(['ngspice','-b','/tmp/cal.spice'], capture_output=True, text=True, timeout=30)
    out = r.stdout + r.stderr
    m = re.search(r'v\(vout\)\s*=\s*([0-9eE.+-]+)', out)
    m2 = re.search(r'-i\(vdd\)\s*=\s*([0-9eE.+-]+)', out)
    vout = float(m.group(1)) if m else None
    isup = float(m2.group(1)) if m2 else None
    return vout, isup

results = {}
print(f"{'Corner':>8} {'VBN':>7} {'VBP':>7} {'VBCN':>7} {'VBCP':>7} {'Vout':>7} {'Isup':>10}")

for corner, temp in corners:
    key = f'{corner}_{temp}'
    g = gen[key]

    # VBN from generator
    vbn = g['vbn']
    # VBCN = VBN + 0.23 (empirical from default bias)
    vbcn = vbn + 0.23
    # VBCP needs calibration — start with generator value + offset
    vbcp_start = g.get('vbcp', 0.4)

    # Sweep VBP to find balanced point (Vout≈0.9V)
    best_vbp = None
    best_err = 10
    for vbp_try_x10 in range(600, 900, 5):  # VBP from 0.60 to 0.90
        vbp = vbp_try_x10 / 1000.0
        # VBCP roughly tracks VBP: VBCP ≈ VBP - 0.255
        vbcp = vbp - 0.255
        vout, isup = run_ota_op(corner, temp, vbn, vbp, vbcn, vbcp)
        if vout is not None:
            err = abs(vout - 0.9)
            if err < best_err:
                best_err = err
                best_vbp = vbp
                best_vout = vout
                best_isup = isup
                best_vbcp = vbcp

    if best_vbp:
        # Fine-tune around best VBP
        for delta in np.arange(-0.003, 0.004, 0.001):
            vbp = best_vbp + delta
            vbcp = vbp - 0.255
            vout, isup = run_ota_op(corner, temp, vbn, vbp, vbcn, vbcp)
            if vout and abs(vout - 0.9) < best_err:
                best_err = abs(vout - 0.9)
                best_vbp = vbp
                best_vout = vout
                best_isup = isup
                best_vbcp = vbcp

        results[key] = {
            'vbn': round(vbn, 4), 'vbp': round(best_vbp, 4),
            'vbcn': round(vbcn, 4), 'vbcp': round(best_vbcp, 4),
            'vout': round(best_vout, 4), 'isup': best_isup
        }
        print(f"{key:>8} {vbn:>7.4f} {best_vbp:>7.4f} {vbcn:>7.4f} {best_vbcp:>7.4f} {best_vout:>7.4f} {best_isup:>10.3e}")
    else:
        print(f"{key:>8} CALIBRATION FAILED")
        results[key] = None

with open('bias_calibrated.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nCalibrated bias saved to bias_calibrated.json")
