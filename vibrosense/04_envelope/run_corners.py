#!/usr/bin/env python3
"""Corner analysis for transistor-level LPF OTA."""

import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import re

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
CORNERS = ['tt', 'ss', 'ff', 'sf', 'fs']
VPP = 0.100
VPEAK = VPP / 2.0
FREQ = 3162
VCM = 0.9
EXPECTED_DC = (2.0/np.pi) * VPEAK  # 31.83 mV


def run_corner(corner):
    """Run simulation at given process corner."""
    spice = f"""* Corner analysis: {corner.upper()}
.title Envelope Detector Corner {corner.upper()}

.include "../01_ota/models/sky130_fd_pr__nfet_01v8__{corner}_standalone.spice"
.include "../01_ota/models/sky130_fd_pr__pfet_01v8__{corner}_standalone.spice"
.include "envelope_det_tran.spice"

Vdd vdd 0 1.8
Vss vss 0 0
Vcm vcm 0 {VCM}
Vbn_lpf vbn_lpf 0 0.58

Vin vin vcm sin(0 {VPEAK} {FREQ})

Xenv vin vcm vout vdd vss vbn_lpf envelope_det_tran

.tran 1u 500m uic

.control
run
meas tran vout_avg avg v(vout) from=400m to=500m
meas tran vout_pp pp v(vout) from=400m to=500m
echo "MEAS vout_avg=$&vout_avg vout_pp=$&vout_pp"

* Operating point
echo "OP_TAIL @m.xenv.xlpf.mtail[id]"
print @m.xenv.xlpf.mtail[id]
echo "OP_GM @m.xenv.xlpf.m1[gm]"
print @m.xenv.xlpf.m1[gm]
echo "OP_M1VGS @m.xenv.xlpf.m1[vgs]"
print @m.xenv.xlpf.m1[vgs]
echo "OP_M1VTH @m.xenv.xlpf.m1[vth]"
print @m.xenv.xlpf.m1[vth]
echo "OP_M3VGS @m.xenv.xlpf.m3[vgs]"
print @m.xenv.xlpf.m3[vgs]
echo "OP_M3VTH @m.xenv.xlpf.m3[vth]"
print @m.xenv.xlpf.m3[vth]
quit
.endc

.end
"""
    fname = f'tb_corner_{corner}.spice'
    with open(os.path.join(WORK_DIR, fname), 'w') as f:
        f.write(spice)

    proc = subprocess.run(['ngspice', '-b', fname], capture_output=True,
                          text=True, timeout=300, cwd=WORK_DIR)
    output = proc.stdout + proc.stderr

    result = {'corner': corner.upper()}

    # Parse measurements
    for line in output.split('\n'):
        m = re.search(r'vout_avg\s*=\s*([\d.eE+-]+)', line)
        if m:
            result['vout_avg'] = float(m.group(1))
        m = re.search(r'vout_pp\s*=\s*([\d.eE+-]+)', line)
        if m:
            result['vout_pp'] = float(m.group(1))
        # Operating point
        for key in ['mtail', 'm1']:
            m = re.search(rf'@m\.xenv\.xlpf\.{key}\[id\]\s*=\s*([\d.eE+-]+)', line)
            if m:
                result[f'{key}_id'] = float(m.group(1))
        m = re.search(r'@m\.xenv\.xlpf\.m1\[gm\]\s*=\s*([\d.eE+-]+)', line)
        if m:
            result['m1_gm'] = float(m.group(1))
        m = re.search(r'@m\.xenv\.xlpf\.m1\[vgs\]\s*=\s*([\d.eE+-]+)', line)
        if m:
            result['m1_vgs'] = float(m.group(1))
        m = re.search(r'@m\.xenv\.xlpf\.m1\[vth\]\s*=\s*([\d.eE+-]+)', line)
        if m:
            result['m1_vth'] = float(m.group(1))
        m = re.search(r'@m\.xenv\.xlpf\.m3\[vgs\]\s*=\s*([\d.eE+-]+)', line)
        if m:
            result['m3_vgs'] = float(m.group(1))
        m = re.search(r'@m\.xenv\.xlpf\.m3\[vth\]\s*=\s*([\d.eE+-]+)', line)
        if m:
            result['m3_vth'] = float(m.group(1))

    return result


def main():
    print("=" * 60)
    print("CORNER ANALYSIS — Transistor-Level LPF OTA")
    print("=" * 60)

    results = []
    for corner in CORNERS:
        print(f"\n  Running {corner.upper()}...", end=' ', flush=True)
        r = run_corner(corner)
        results.append(r)

        if 'vout_avg' in r:
            dc_env = r['vout_avg'] - VCM
            err = (dc_env - EXPECTED_DC) / EXPECTED_DC * 100
            ripple = r.get('vout_pp', 0) / dc_env * 100 if dc_env > 0 else 0
            gm = r.get('m1_gm', 0)
            fc = gm / (2 * np.pi * 10e-9) if gm > 0 else 0

            r['dc_envelope'] = dc_env
            r['error_pct'] = err
            r['ripple_pct'] = ripple
            r['fc_hz'] = fc

            m1_vov = (r.get('m1_vgs', 0) - r.get('m1_vth', 0)) * 1000
            m3_vov = (r.get('m3_vgs', 0) - r.get('m3_vth', 0)) * 1000

            print(f"DC={dc_env*1000:.2f}mV  Err={err:+.1f}%  "
                  f"gm={gm*1e9:.0f}nS  fc={fc:.1f}Hz  "
                  f"Tail={r.get('mtail_id', 0)*1e9:.1f}nA  "
                  f"M1_Vov={m1_vov:.0f}mV  M3_Vov={m3_vov:.0f}mV")
        else:
            print("FAILED")

    # Summary table
    print("\n" + "=" * 60)
    print("CORNER SUMMARY")
    print("=" * 60)
    print(f"{'Corner':<8} {'DC(mV)':<10} {'Error(%)':<10} {'fc(Hz)':<10} {'Ripple(%)':<10} {'Tail(nA)':<10}")
    print("-" * 58)
    for r in results:
        if 'dc_envelope' in r:
            print(f"{r['corner']:<8} {r['dc_envelope']*1000:<10.2f} {r['error_pct']:<+10.1f} "
                  f"{r['fc_hz']:<10.1f} {r['ripple_pct']:<10.3f} {r.get('mtail_id', 0)*1e9:<10.1f}")

    # Plot corner comparison
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    corners_label = [r['corner'] for r in results if 'dc_envelope' in r]
    dc_vals = [r['dc_envelope']*1000 for r in results if 'dc_envelope' in r]
    fc_vals = [r['fc_hz'] for r in results if 'dc_envelope' in r]
    err_vals = [abs(r['error_pct']) for r in results if 'dc_envelope' in r]

    # DC output
    colors_dc = ['green' if abs(e) < 5 else 'orange' if abs(e) < 15 else 'red'
                 for e in [r['error_pct'] for r in results if 'dc_envelope' in r]]
    axes[0].bar(corners_label, dc_vals, color=colors_dc, edgecolor='black')
    axes[0].axhline(y=EXPECTED_DC*1000, color='blue', linestyle='--', label=f'Ideal ({EXPECTED_DC*1000:.1f} mV)')
    axes[0].set_ylabel('DC Envelope (mV)')
    axes[0].set_title('DC Output Across Corners')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y')

    # fc
    colors_fc = ['green' if 5 <= fc <= 20 else 'red' for fc in fc_vals]
    axes[1].bar(corners_label, fc_vals, color=colors_fc, edgecolor='black')
    axes[1].axhline(y=5, color='red', linestyle='--')
    axes[1].axhline(y=20, color='red', linestyle='--')
    axes[1].axhline(y=10, color='blue', linestyle='--', label='Target 10 Hz')
    axes[1].set_ylabel('LPF Cutoff (Hz)')
    axes[1].set_title('LPF fc Across Corners')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, axis='y')

    # Error
    colors_err = ['green' if e < 5 else 'red' for e in err_vals]
    axes[2].bar(corners_label, err_vals, color=colors_err, edgecolor='black')
    axes[2].axhline(y=5, color='red', linestyle='--', label='5% spec limit')
    axes[2].set_ylabel('Rectification Error (%)')
    axes[2].set_title('Error Across Corners')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3, axis='y')

    plt.suptitle('VibroSense Block 04: Envelope Detector — 5-Corner Analysis (100 mVpp, 3162 Hz)',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(WORK_DIR, 'plot_corners.png'), dpi=150)
    plt.close()
    print("\n  Saved plot_corners.png")


if __name__ == '__main__':
    main()
