#!/usr/bin/env python3
"""plot_all.py — Generate all required plots for Block 09: Startup Circuit"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def load_wrdata(filename, ncols=None):
    """Load ngspice .wrdata output. Returns dict of arrays."""
    if not os.path.exists(filename):
        print(f"WARNING: {filename} not found")
        return None
    data = np.loadtxt(filename, skiprows=1)
    return data

def plot_startup_waveform():
    """Plot BVDD and PVDD vs time at 1V/µs"""
    data = load_wrdata('tb_su_basic_data.txt')
    if data is None:
        return
    # Columns: time,bvdd, time,pvdd, time,gate, time,startup_done, time,ea_en
    t = data[:, 0] * 1e6  # µs
    bvdd = data[:, 1]
    pvdd = data[:, 3]
    gate = data[:, 5]
    ea_en = data[:, 9]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    ax1.plot(t, bvdd, 'b-', label='BVDD', linewidth=1.5)
    ax1.plot(t, pvdd, 'r-', label='PVDD', linewidth=1.5)
    ax1.axhline(y=5.0, color='g', linestyle='--', alpha=0.5, label='5V target')
    ax1.set_ylabel('Voltage (V)')
    ax1.set_title('Startup Waveform — 1 V/µs BVDD Ramp, No Load')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-0.5, 8)

    ax2.plot(t, gate, 'purple', label='Gate', linewidth=1.5)
    ax2.plot(t, ea_en, 'orange', label='ea_en', linewidth=1.5, alpha=0.7)
    ax2.set_ylabel('Voltage (V)')
    ax2.set_xlabel('Time (µs)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('startup_waveform.png', dpi=150)
    plt.close()
    print("Generated startup_waveform.png")

def plot_startup_vs_load():
    """Plot PVDD startup with no load and 50mA load overlaid"""
    data_basic = load_wrdata('tb_su_basic_data.txt')
    data_50mA = load_wrdata('tb_su_50mA_data.txt')
    if data_basic is None or data_50mA is None:
        return

    t1 = data_basic[:, 0] * 1e6
    pvdd1 = data_basic[:, 3]
    t2 = data_50mA[:, 0] * 1e6
    pvdd2 = data_50mA[:, 3]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t1, pvdd1, 'r-', label='No load', linewidth=1.5)
    ax.plot(t2, pvdd2, 'b-', label='50 mA load', linewidth=1.5)
    ax.axhline(y=5.0, color='g', linestyle='--', alpha=0.5, label='5V target')
    ax.set_xlabel('Time (µs)')
    ax.set_ylabel('PVDD (V)')
    ax.set_title('Startup: No Load vs 50 mA Load')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.5, 8)
    plt.tight_layout()
    plt.savefig('startup_vs_load.png', dpi=150)
    plt.close()
    print("Generated startup_vs_load.png")

def plot_ramp_comparison():
    """Plot PVDD for different BVDD ramp rates"""
    data_fast = load_wrdata('tb_su_fast_data.txt')
    data_slow = load_wrdata('tb_su_slow_data.txt')
    data_normal = load_wrdata('tb_su_basic_data.txt')

    fig, ax = plt.subplots(figsize=(10, 5))
    if data_normal is not None:
        t = data_normal[:, 0] * 1e6
        ax.plot(t, data_normal[:, 3], 'b-', label='1 V/µs (normal)', linewidth=1.5)
    if data_fast is not None:
        t = data_fast[:, 0] * 1e6
        ax.plot(t, data_fast[:, 3], 'r-', label='12 V/µs (fast)', linewidth=1.5)
    if data_slow is not None:
        t = data_slow[:, 0] * 1e6
        ax.plot(t, data_slow[:, 3], 'g-', label='0.1 V/µs (slow)', linewidth=1.5)

    ax.axhline(y=5.0, color='k', linestyle='--', alpha=0.3, label='5V target')
    ax.set_xlabel('Time (µs)')
    ax.set_ylabel('PVDD (V)')
    ax.set_title('PVDD Startup at Different BVDD Ramp Rates')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 200)
    plt.tight_layout()
    plt.savefig('startup_ramp_comparison.png', dpi=150)
    plt.close()
    print("Generated startup_ramp_comparison.png")

def plot_handoff_detail():
    """Plot PVDD zoomed around handoff instant"""
    data = load_wrdata('tb_su_handoff_data.txt')
    if data is None:
        return

    t = data[:, 0] * 1e6
    pvdd = data[:, 3]
    ea_en = data[:, 7]

    # Find handoff region (ea_en transitions)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    ax1.plot(t, pvdd, 'r-', linewidth=1.5, label='PVDD')
    ax1.set_ylabel('PVDD (V)')
    ax1.set_title('Handoff Detail — PVDD at Startup-to-Regulation Transition')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(t, ea_en, 'orange', linewidth=1.5, label='ea_en')
    ax2.set_ylabel('ea_en (V)')
    ax2.set_xlabel('Time (µs)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('handoff_detail.png', dpi=150)
    plt.close()
    print("Generated handoff_detail.png")

def plot_cold_crank():
    """Plot BVDD and PVDD during cold crank"""
    data = load_wrdata('tb_su_cold_crank_data.txt')
    if data is None:
        return

    t = data[:, 0] * 1e6
    bvdd = data[:, 1]
    pvdd = data[:, 3]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, bvdd, 'b-', label='BVDD', linewidth=1.5)
    ax.plot(t, pvdd, 'r-', label='PVDD', linewidth=1.5)
    ax.axhline(y=5.0, color='g', linestyle='--', alpha=0.5, label='5V target')
    ax.set_xlabel('Time (µs)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title('Cold Crank Recovery — BVDD 10.5V → 3V → 7V')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('cold_crank.png', dpi=150)
    plt.close()
    print("Generated cold_crank.png")

def plot_inrush():
    """Plot pass device current and power during startup"""
    data = load_wrdata('tb_su_inrush_data.txt')
    if data is None:
        return

    t = data[:, 0] * 1e6
    id_pass = data[:, 1] * 1000  # mA
    vds = data[:, 3]
    p_inst = data[:, 5] * 1000  # mW

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    ax1.plot(t, id_pass, 'r-', linewidth=1.5)
    ax1.axhline(y=150, color='k', linestyle='--', alpha=0.5, label='150 mA limit')
    ax1.set_ylabel('Pass Device Id (mA)')
    ax1.set_title('Inrush Current During Startup')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(t, p_inst, 'b-', linewidth=1.5)
    ax2.set_ylabel('Instantaneous Power (mW)')
    ax2.set_xlabel('Time (µs)')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('inrush_current.png', dpi=150)
    plt.close()
    print("Generated inrush_current.png")

if __name__ == '__main__':
    plot_startup_waveform()
    plot_startup_vs_load()
    plot_ramp_comparison()
    plot_handoff_detail()
    plot_cold_crank()
    plot_inrush()
    print("\nAll plots generated.")
