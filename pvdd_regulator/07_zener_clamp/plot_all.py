#!/usr/bin/env python3
"""plot_all.py — Block 07: Zener Clamp — Generate all plots."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob

def load_wrdata(path):
    """Load ngspice .wrdata file (2-column: x y)."""
    data = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('*') or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    data.append((float(parts[0]), float(parts[1])))
                except ValueError:
                    continue
    if not data:
        return np.array([]), np.array([])
    d = np.array(data)
    return d[:, 0], d[:, 1]


def plot_iv_characteristic():
    """Plot I-V characteristic from tb_zc_iv data."""
    if not os.path.exists('iv_data.txt'):
        print("iv_data.txt not found, skipping IV plot")
        return
    v, i = load_wrdata('iv_data.txt')
    if len(v) == 0:
        print("No data in iv_data.txt")
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Linear scale
    ax1.plot(v, i * 1e3, 'b-', linewidth=1.5)
    ax1.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='1 mA onset')
    ax1.axhline(y=10.0, color='orange', linestyle='--', alpha=0.5, label='10 mA')
    ax1.axvline(x=5.0, color='green', linestyle=':', alpha=0.5, label='PVDD = 5.0V')
    ax1.axvline(x=5.5, color='gray', linestyle=':', alpha=0.3)
    ax1.axvline(x=6.2, color='gray', linestyle=':', alpha=0.3)
    ax1.set_xlabel('PVDD (V)')
    ax1.set_ylabel('Clamp Current (mA)')
    ax1.set_title('Zener Clamp I-V (Linear)')
    ax1.set_xlim(4, 8)
    ax1.set_ylim(-1, 50)
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    # Log scale
    i_pos = np.clip(i, 1e-12, None)
    ax2.semilogy(v, i_pos * 1e9, 'b-', linewidth=1.5)
    ax2.axhline(y=1000, color='r', linestyle='--', alpha=0.5, label='1 µA spec')
    ax2.axhline(y=5000, color='orange', linestyle='--', alpha=0.5, label='5 µA spec')
    ax2.axvline(x=5.0, color='green', linestyle=':', alpha=0.5, label='PVDD = 5.0V')
    ax2.axvline(x=5.17, color='purple', linestyle=':', alpha=0.5, label='PVDD = 5.17V')
    ax2.set_xlabel('PVDD (V)')
    ax2.set_ylabel('Clamp Current (nA)')
    ax2.set_title('Zener Clamp I-V (Log)')
    ax2.set_xlim(3, 8)
    ax2.set_ylim(0.01, 1e8)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('iv_characteristic.png', dpi=150)
    plt.close()
    print("Saved iv_characteristic.png")


def plot_iv_vs_temperature():
    """Plot I-V curves at multiple temperatures."""
    temps = [-40, 27, 85, 150]
    fnames = ['iv_temp_m40.txt', 'iv_temp_27.txt', 'iv_temp_85.txt', 'iv_temp_150.txt']
    colors = ['blue', 'green', 'orange', 'red']

    fig, ax = plt.subplots(figsize=(8, 5))

    found_any = False
    for temp, fname, color in zip(temps, fnames, colors):
        if not os.path.exists(fname):
            continue
        v, i = load_wrdata(fname)
        if len(v) == 0:
            continue
        found_any = True
        ax.semilogy(v, np.clip(i, 1e-12, None) * 1e3, color=color,
                     linewidth=1.5, label=f'{temp}°C')

    if not found_any:
        print("No temperature data found, skipping temp plot")
        return

    ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='1 mA')
    ax.axvline(x=5.0, color='gray', linestyle=':', alpha=0.3)
    ax.set_xlabel('PVDD (V)')
    ax.set_ylabel('Clamp Current (mA)')
    ax.set_title('Zener Clamp I-V vs Temperature')
    ax.set_xlim(3, 8)
    ax.set_ylim(1e-7, 1e3)
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('iv_vs_temperature.png', dpi=150)
    plt.close()
    print("Saved iv_vs_temperature.png")


def plot_transient():
    """Plot transient clamping waveform."""
    if not os.path.exists('transient_data.txt'):
        print("transient_data.txt not found, skipping transient plot")
        return
    t, v = load_wrdata('transient_data.txt')
    if len(t) == 0:
        print("No data in transient_data.txt")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t * 1e6, v, 'b-', linewidth=1.5)
    ax.axhline(y=6.5, color='r', linestyle='--', alpha=0.5, label='6.5V spec limit')
    ax.axhline(y=5.0, color='green', linestyle=':', alpha=0.5, label='5.0V nominal')
    ax.set_xlabel('Time (µs)')
    ax.set_ylabel('PVDD (V)')
    ax.set_title('Transient Clamping (10 V/µs ramp, 200 pF Cload)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.5, 8)

    plt.tight_layout()
    plt.savefig('transient_clamping.png', dpi=150)
    plt.close()
    print("Saved transient_clamping.png")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    plot_iv_characteristic()
    plot_iv_vs_temperature()
    plot_transient()
    print("All plots generated.")
