#!/usr/bin/env python3
"""Generate plots for bias_generator_full verification.

Produces:
  1. Corner x Temperature summary bar chart
  2. VDD-tracking sweep plot
"""

import subprocess
import re
import os

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("WARNING: matplotlib not available. Generating text-only reports.")

CORNERS = ['tt', 'ss', 'ff', 'sf', 'fs']
TEMPS = [-40, 27, 85]
SKY130_LIB = "/home/ubuntu/.volare/sky130A/libs.tech/combined/continuous/sky130.lib.spice"

# ===== Plot 1: Corner x Temperature Summary =====
def run_corner_sweep():
    """Run all corners and collect results."""
    NETLIST_TEMPLATE = """\
.param mc_mm_switch=0
.param mc_pr_switch=0
.option scale=1e-6
.lib "{lib}" {corner}
.include "design_full.cir"
Xbias vdd gnd iref_out vbn vbcn vbp vbcp  bias_generator_full
Vdd vdd gnd 1.8
Riref iref_out gnd 3560
.temp {temp}
.nodeset v(vbn)=0.65 v(vbp)=0.73 v(vbcn)=0.88 v(vbcp)=0.475
.control
op
let iref_nA = @Riref[i] * 1e9
echo "RESULT: $&v(vbn) $&v(vbcn) $&v(vbp) $&v(vbcp) $&iref_nA"
.endc
.end
"""
    results = {}
    for corner in CORNERS:
        results[corner] = {}
        for temp in TEMPS:
            netlist = NETLIST_TEMPLATE.format(corner=corner, temp=temp, lib=SKY130_LIB)
            tmp_file = f"/tmp/tb_plot_{corner}_{temp}.spice"
            with open(tmp_file, 'w') as f:
                f.write(netlist)
            proc = subprocess.run(['ngspice', '-b', tmp_file],
                                  capture_output=True, text=True, timeout=120)
            output = proc.stdout + proc.stderr
            match = re.search(r'RESULT:\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)', output)
            if match:
                results[corner][temp] = {
                    'vbn': float(match.group(1)),
                    'vbcn': float(match.group(2)),
                    'vbp': float(match.group(3)),
                    'vbcp': float(match.group(4)),
                    'iref': float(match.group(5))
                }
            else:
                results[corner][temp] = None
    return results


def run_vdd_sweep():
    """Run VDD sweep and return data."""
    netlist = """\
.param mc_mm_switch=0
.param mc_pr_switch=0
.option scale=1e-6
.lib "{lib}" tt
.include "design_full.cir"
Xbias vdd gnd iref_out vbn vbcn vbp vbcp  bias_generator_full
Vdd vdd gnd 1.8
Riref iref_out gnd 3560
.nodeset v(vbn)=0.65 v(vbp)=0.73 v(vbcn)=0.88 v(vbcp)=0.475
.dc Vdd 1.6 2.0 0.01
.control
run
wrdata /tmp/vdd_sweep_data v(vbn) v(vbcn) v(vbp) v(vbcp)
.endc
.end
""".format(lib=SKY130_LIB)

    with open('/tmp/tb_vdd_sweep.spice', 'w') as f:
        f.write(netlist)
    subprocess.run(['ngspice', '-b', '/tmp/tb_vdd_sweep.spice'],
                   capture_output=True, text=True, timeout=120)

    # Parse wrdata output
    data = {'vdd': [], 'vbn': [], 'vbcn': [], 'vbp': [], 'vbcp': []}
    try:
        with open('/tmp/vdd_sweep_data', 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) >= 5:
                    data['vdd'].append(float(parts[0]))
                    data['vbn'].append(float(parts[1]))
                    data['vbcn'].append(float(parts[2]))
                    data['vbp'].append(float(parts[3]))
                    data['vbcp'].append(float(parts[4]))
    except Exception:
        pass
    return data


def plot_corners(results):
    """Generate corner summary plot."""
    if not HAS_MPL:
        return

    signals = ['vbn', 'vbcn', 'vbp', 'vbcp']
    targets = {'vbn': 0.629, 'vbcn': 0.883, 'vbp': 0.739, 'vbcp': 0.474}
    tol = 0.100

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Bias Distribution: 5 Corners x 3 Temperatures', fontsize=14, fontweight='bold')

    for idx, sig in enumerate(signals):
        ax = axes[idx // 2][idx % 2]
        x_labels = []
        values = []
        colors = []

        for corner in CORNERS:
            for temp in TEMPS:
                r = results.get(corner, {}).get(temp)
                if r:
                    val = r[sig]
                    values.append(val)
                    x_labels.append(f"{corner}\n{temp}C")
                    dev = abs(val - targets[sig])
                    colors.append('green' if dev <= tol else 'red')
                else:
                    values.append(0)
                    x_labels.append(f"{corner}\n{temp}C")
                    colors.append('gray')

        x = np.arange(len(values))
        ax.bar(x, values, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
        ax.axhline(y=targets[sig], color='blue', linestyle='--', linewidth=1.5, label=f'TT 27C = {targets[sig]:.3f}V')
        ax.axhline(y=targets[sig] + tol, color='orange', linestyle=':', linewidth=1, label=f'±{tol*1000:.0f}mV')
        ax.axhline(y=targets[sig] - tol, color='orange', linestyle=':', linewidth=1)
        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, fontsize=7)
        ax.set_ylabel(f'{sig} (V)')
        ax.set_title(sig.upper())
        ax.legend(fontsize=8)
        ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig('plot_corners.png', dpi=150, bbox_inches='tight')
    print("Saved: plot_corners.png")
    plt.close()


def plot_vdd_tracking(data):
    """Generate VDD-tracking plot."""
    if not HAS_MPL or not data['vdd']:
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('VDD-Tracking Verification (TT 27C)', fontsize=14, fontweight='bold')

    vdd = np.array(data['vdd'])

    # Left: absolute voltages
    ax1.plot(vdd, data['vbn'], 'b-', label='vbn', linewidth=2)
    ax1.plot(vdd, data['vbcn'], 'g-', label='vbcn', linewidth=2)
    ax1.plot(vdd, data['vbp'], 'r-', label='vbp', linewidth=2)
    ax1.plot(vdd, data['vbcp'], 'm-', label='vbcp', linewidth=2)
    ax1.set_xlabel('VDD (V)')
    ax1.set_ylabel('Bias Voltage (V)')
    ax1.set_title('Bias Voltages vs VDD')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Right: derivatives (tracking coefficients)
    dvdd = np.diff(vdd)
    for sig, color, label in [('vbn', 'b', 'vbn'), ('vbcn', 'g', 'vbcn'),
                               ('vbp', 'r', 'vbp'), ('vbcp', 'm', 'vbcp')]:
        dv = np.diff(data[sig]) / dvdd
        ax2.plot(vdd[:-1], dv, color + '-', label=label, linewidth=2)

    ax2.axhline(y=0.85, color='red', linestyle='--', alpha=0.5, label='VDD-track min (0.85)')
    ax2.axhline(y=0.15, color='blue', linestyle='--', alpha=0.5, label='Ground-ref max (0.15)')
    ax2.set_xlabel('VDD (V)')
    ax2.set_ylabel('dV/dVDD (V/V)')
    ax2.set_title('VDD-Tracking Coefficients')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.1, 1.2)

    plt.tight_layout()
    plt.savefig('plot_vdd_tracking.png', dpi=150, bbox_inches='tight')
    print("Saved: plot_vdd_tracking.png")
    plt.close()


if __name__ == '__main__':
    print("Running corner sweep...")
    results = run_corner_sweep()

    print("\nRunning VDD sweep...")
    vdd_data = run_vdd_sweep()

    print("\nGenerating plots...")
    plot_corners(results)
    plot_vdd_tracking(vdd_data)

    # Print text summary
    print("\n=== SUMMARY ===")
    tt27 = results.get('tt', {}).get(27)
    if tt27:
        print(f"TT 27C: vbn={tt27['vbn']:.4f} vbcn={tt27['vbcn']:.4f} vbp={tt27['vbp']:.4f} vbcp={tt27['vbcp']:.4f} Iref={tt27['iref']:.1f}nA")

    # Corner deviation summary
    if tt27:
        for sig in ['vbn', 'vbcn', 'vbp', 'vbcp']:
            ref = tt27[sig]
            worst_dev = 0
            worst_cond = ""
            for c in CORNERS:
                for t in TEMPS:
                    r = results.get(c, {}).get(t)
                    if r:
                        dev = abs(r[sig] - ref)
                        if dev > worst_dev:
                            worst_dev = dev
                            worst_cond = f"{c} {t}C"
            status = "PASS" if worst_dev <= 0.100 else f"FAIL ({worst_dev*1000:.0f}mV)"
            print(f"  {sig}: worst deviation = {worst_dev*1000:.1f}mV at {worst_cond} — {status}")

    print("\nDone.")
