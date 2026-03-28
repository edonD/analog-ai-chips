#!/usr/bin/env python3
"""plot_all.py — Generate all required plots for Block 06: Level Shifter."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def load_wrdata(filename, ncols_per_signal=2):
    """Load ngspice wrdata file. Returns list of (time, values) tuples."""
    data = np.loadtxt(filename)
    signals = []
    for i in range(0, data.shape[1], ncols_per_signal):
        t = data[:, i]
        v = data[:, i + 1]
        signals.append((t, v))
    return signals


def plot_switching_waveforms():
    """Plot input/output waveforms for both shifters."""
    if not os.path.exists('waveform_logic.dat'):
        print("WARNING: waveform_logic.dat not found, skipping switching plot")
        return

    signals = load_wrdata('waveform_logic.dat')
    if len(signals) < 4:
        print("WARNING: insufficient signals in waveform_logic.dat")
        return

    t_in_up, v_in_up = signals[0]
    t_out_up, v_out_up = signals[1]
    t_in_dn, v_in_dn = signals[2]
    t_out_dn, v_out_dn = signals[3]

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Low-to-High shifter
    ax = axes[0]
    ax.plot(t_in_up * 1e9, v_in_up, 'b-', linewidth=1.5, label='Input (0–2.2V)')
    ax.plot(t_out_up * 1e9, v_out_up, 'r-', linewidth=1.5, label='Output (0–BVDD)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title('Level Shifter UP: SVDD (2.2V) → BVDD (7V)')
    ax.legend(loc='right')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.5, 8)

    # High-to-Low shifter
    ax = axes[1]
    ax.plot(t_in_dn * 1e9, v_in_dn, 'b-', linewidth=1.5, label='Input (0–5V)')
    ax.plot(t_out_dn * 1e9, v_out_dn, 'r-', linewidth=1.5, label='Output (0–2.2V)')
    ax.set_ylabel('Voltage (V)')
    ax.set_xlabel('Time (ns)')
    ax.set_title('Level Shifter DOWN: PVDD (5V) → SVDD (2.2V)')
    ax.legend(loc='right')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.5, 6)

    plt.tight_layout()
    plt.savefig('switching_waveforms.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: switching_waveforms.png")


def plot_delay_vs_bvdd():
    """Plot delay vs BVDD from run.log data."""
    if not os.path.exists('run.log'):
        print("WARNING: run.log not found, skipping delay_vs_bvdd plot")
        return

    with open('run.log') as f:
        log = f.read()

    # Extract BVDD sweep delays from the bvdd_sweep testbench
    bvdd_vals = [5.4, 7.0, 10.5]
    suffixes = ['54', '70', '105']
    delays = []

    for sfx in suffixes:
        # Parse tplh and tphl, take the max as the delay for this BVDD
        tplh_m = re.search(rf'tplh_up_{sfx}_ns:\s+(\S+)', log)
        tphl_m = re.search(rf'tphl_up_{sfx}_ns:\s+(\S+)', log)
        if tplh_m and tphl_m:
            tplh = float(tplh_m.group(1))
            tphl = float(tphl_m.group(1))
            delays.append(max(tplh, tphl))
        else:
            delays.append(None)

    if any(d is None for d in delays):
        print("ERROR: Could not parse BVDD sweep delays from run.log — skipping delay_vs_bvdd plot")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([str(v) for v in bvdd_vals], delays, color=['#e74c3c', '#3498db', '#2ecc71'],
           width=0.5, edgecolor='black')
    ax.set_xlabel('BVDD (V)')
    ax.set_ylabel('Propagation Delay (ns)')
    ax.set_title('Propagation Delay vs BVDD (TT 27°C)')
    ax.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='Spec limit (100 ns)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    for i, d in enumerate(delays):
        ax.text(i, d + 1, f'{d:.1f} ns', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('delay_vs_bvdd.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: delay_vs_bvdd.png")


def plot_delay_pvt():
    """Plot delay at PVT corners from run.log data."""
    if not os.path.exists('run.log'):
        print("WARNING: run.log not found, skipping delay_pvt plot")
        return

    with open('run.log') as f:
        log = f.read()

    # Extract the key delay metrics
    # The PVT testbench runs SS 150C BVDD=5.4V (worst case)
    # The delay testbench runs TT 27C BVDD=7V (nominal)
    corners = ['TT 27°C\nBVDD=7V', 'SS 150°C\nBVDD=5.4V']
    delays = []

    # TT nominal delay
    m = re.search(r'delay_max_ns_tt:\s+(\S+)', log)
    if m:
        delays.append(float(m.group(1)))
    else:
        delays.append(None)

    # SS worst case (last delay_max_ns from PVT sweep)
    m = re.findall(r'^delay_max_ns:\s+(\S+)', log, re.MULTILINE)
    if m:
        delays.append(float(m[-1]))
    else:
        delays.append(None)

    if any(d is None for d in delays):
        print("ERROR: Could not parse PVT delays from run.log — skipping delay_pvt plot")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#3498db', '#e74c3c']
    bars = ax.bar(corners, delays, color=colors, width=0.5, edgecolor='black')
    ax.set_ylabel('Max Propagation Delay (ns)')
    ax.set_title('Worst-Case Delay at PVT Corners')
    ax.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='Spec limit (100 ns)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    for i, d in enumerate(delays):
        ax.text(i, d + 1.5, f'{d:.1f} ns', ha='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('delay_pvt.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: delay_pvt.png")


if __name__ == '__main__':
    plot_switching_waveforms()
    plot_delay_vs_bvdd()
    plot_delay_pvt()
    print("All plots generated.")
