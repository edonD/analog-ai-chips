#!/usr/bin/env python3
"""plot_all.py — Generate all plots for Block 05: UV/OV Comparators."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load_wrdata(filename):
    """Load ngspice .wrdata output file. Returns dict of column_name -> array."""
    data = []
    headers = None
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('*'):
                continue
            parts = line.split()
            if headers is None:
                # Check if first line is headers (non-numeric first field)
                try:
                    float(parts[0])
                    # Numeric — no headers
                    data.append([float(x) for x in parts])
                except ValueError:
                    headers = parts
                continue
            try:
                data.append([float(x) for x in parts])
            except ValueError:
                continue
    arr = np.array(data)
    if headers and len(headers) == arr.shape[1]:
        return {h: arr[:, i] for i, h in enumerate(headers)}
    return arr


def plot_uv_trip():
    """UV flag vs PVDD — hysteresis loop."""
    try:
        d = load_wrdata('uv_trip_data.txt')
    except Exception:
        print("Cannot load uv_trip_data.txt")
        return

    if isinstance(d, dict):
        pvdd = d.get('v(pvdd)', d.get('pvdd', None))
        flag = d.get('v(uv_flag)', d.get('uv_flag', None))
        if pvdd is None:
            pvdd = list(d.values())[0]
            flag = list(d.values())[1]
    else:
        pvdd = d[:, 0]
        flag = d[:, 1]

    n = len(pvdd)
    mid = n // 2

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(pvdd[:mid], flag[:mid], 'b-', label='PVDD rising', linewidth=1.5)
    ax.plot(pvdd[mid:], flag[mid:], 'r-', label='PVDD falling', linewidth=1.5)
    ax.axvspan(4.0, 4.5, alpha=0.1, color='green', label='UV spec window')
    ax.set_xlabel('PVDD (V)')
    ax.set_ylabel('UV Flag (V)')
    ax.set_title('UV Comparator — Trip Point & Hysteresis')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(3.5, 5.0)
    fig.tight_layout()
    fig.savefig('uv_trip_hysteresis.png', dpi=150)
    plt.close()
    print("Saved uv_trip_hysteresis.png")


def plot_ov_trip():
    """OV flag vs PVDD — hysteresis loop."""
    try:
        d = load_wrdata('ov_trip_data.txt')
    except Exception:
        print("Cannot load ov_trip_data.txt")
        return

    if isinstance(d, dict):
        pvdd = d.get('v(pvdd)', d.get('pvdd', None))
        flag = d.get('v(ov_flag)', d.get('ov_flag', None))
        if pvdd is None:
            pvdd = list(d.values())[0]
            flag = list(d.values())[1]
    else:
        pvdd = d[:, 0]
        flag = d[:, 1]

    n = len(pvdd)
    mid = n // 2

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(pvdd[:mid], flag[:mid], 'b-', label='PVDD rising', linewidth=1.5)
    ax.plot(pvdd[mid:], flag[mid:], 'r-', label='PVDD falling', linewidth=1.5)
    ax.axvspan(5.25, 5.7, alpha=0.1, color='green', label='OV spec window')
    ax.set_xlabel('PVDD (V)')
    ax.set_ylabel('OV Flag (V)')
    ax.set_title('OV Comparator — Trip Point & Hysteresis')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(4.5, 6.0)
    fig.tight_layout()
    fig.savefig('ov_trip_hysteresis.png', dpi=150)
    plt.close()
    print("Saved ov_trip_hysteresis.png")


def plot_response():
    """Input and flag vs time — propagation delay."""
    try:
        d = load_wrdata('response_data.txt')
    except Exception:
        print("Cannot load response_data.txt")
        return

    if isinstance(d, dict):
        keys = list(d.keys())
        pvdd_uv = d[keys[0]]
        uv_flag = d[keys[1]]
        pvdd_ov = d[keys[2]]
        ov_flag = d[keys[3]]
    else:
        pvdd_uv = d[:, 0]
        uv_flag = d[:, 1]
        pvdd_ov = d[:, 2]
        ov_flag = d[:, 3]

    # Generate time axis from data length
    t = np.linspace(0, 100e-6, len(pvdd_uv))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(t*1e6, pvdd_uv, 'b-', label='PVDD (UV test)')
    ax1.plot(t*1e6, uv_flag, 'r-', label='UV flag')
    ax1.axvline(50, color='gray', linestyle='--', alpha=0.5, label='Step @ 50µs')
    ax1.set_ylabel('Voltage (V)')
    ax1.set_title('UV Response Time')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(t*1e6, pvdd_ov, 'b-', label='PVDD (OV test)')
    ax2.plot(t*1e6, ov_flag, 'r-', label='OV flag')
    ax2.axvline(50, color='gray', linestyle='--', alpha=0.5, label='Step @ 50µs')
    ax2.set_xlabel('Time (µs)')
    ax2.set_ylabel('Voltage (V)')
    ax2.set_title('OV Response Time')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig('response_time.png', dpi=150)
    plt.close()
    print("Saved response_time.png")


if __name__ == '__main__':
    plot_uv_trip()
    plot_ov_trip()
    plot_response()
    print("All plots generated.")
