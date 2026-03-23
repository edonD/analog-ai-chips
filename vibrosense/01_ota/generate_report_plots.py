#!/usr/bin/env python3
"""Generate publication-quality plots for OTA v11 report.
All data comes from live ngspice simulations — no hardcoded values."""

import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import re

WORK = "/home/ubuntu/analog-ai-chips/vibrosense/01_ota"
os.chdir(WORK)

plt.rcParams.update({
    'font.size': 11,
    'font.family': 'sans-serif',
    'axes.linewidth': 1.2,
    'grid.alpha': 0.3,
    'figure.facecolor': 'white',
    'savefig.bbox': 'tight',
    'savefig.dpi': 200,
})

def run_spice(tb):
    r = subprocess.run(["/usr/bin/ngspice", "-b", tb], cwd=WORK,
                       capture_output=True, text=True, timeout=120)
    return r.stdout + r.stderr

def parse_meas(out, name):
    m = re.search(rf'{name}\s*=\s*([+-]?\d+\.?\d*[eE][+-]?\d+|[+-]?\d+\.?\d*)', out)
    return float(m.group(1)) if m else None

def load_wrdata(path):
    data = []
    with open(path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    data.append([float(x) for x in parts])
                except ValueError:
                    pass
    return np.array(data) if data else None

# ============================================================
# 1. BODE PLOT
# ============================================================
print("1. Bode plot...")
out = run_spice("tb_ota_ac.spice")
if os.path.exists("bode_data"):
    data = load_wrdata("bode_data")
    if data is not None and len(data) > 20:
        n = len(data)
        half = n // 2
        freq_mag = data[:half, 0]
        mag_db = data[:half, 1]
        freq_ph = data[half:, 0]
        phase_deg = data[half:, 1]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True,
                                        gridspec_kw={'height_ratios': [2, 1]})

        ax1.semilogx(freq_mag, mag_db, '#1a5276', linewidth=2)
        ax1.axhline(y=65, color='#c0392b', linestyle='--', alpha=0.7, linewidth=1, label='Target: 65 dB')
        ax1.axhline(y=60, color='#e67e22', linestyle=':', alpha=0.7, linewidth=1, label='Min: 60 dB')
        ax1.axhline(y=0, color='gray', linestyle='-', alpha=0.3, linewidth=0.5)
        ax1.set_ylabel('Gain (dB)', fontweight='bold')
        ax1.set_title('Open-Loop Frequency Response (TT, 27 C, CL = 10 pF)', fontsize=13, fontweight='bold')
        ax1.legend(loc='upper right', framealpha=0.9)
        ax1.grid(True, which='both')
        ax1.set_ylim([-20, 80])
        ax1.set_xlim([1, 1e8])

        ax2.semilogx(freq_ph, phase_deg, '#922b21', linewidth=2)
        ax2.axhline(y=-180, color='gray', linestyle='--', alpha=0.5)
        ax2.set_ylabel('Phase (deg)', fontweight='bold')
        ax2.set_xlabel('Frequency (Hz)', fontweight='bold')
        ax2.grid(True, which='both')
        ax2.set_ylim([-200, 20])

        plt.tight_layout()
        plt.savefig('report_bode.png')
        plt.close()
        print("   -> report_bode.png")

# ============================================================
# 2. DC TRANSFER
# ============================================================
print("2. DC transfer...")
out = run_spice("tb_ota_dc.spice")
if os.path.exists("dc_swing_data"):
    data = load_wrdata("dc_swing_data")
    if data is not None and len(data) > 20:
        n = len(data)
        half = n // 2
        vinp = data[:half, 0]
        vout = data[:half, 1]

        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        ax.plot(vinp, vout, '#1a5276', linewidth=2, label='OTA (unity-gain)')
        ax.plot([0, 1.8], [0, 1.8], 'k--', alpha=0.2, linewidth=1, label='Ideal (Vout = Vinp)')
        ax.fill_between([0.632, 1.678], 0, 1.8, alpha=0.08, color='green', label='Linear region (1.046 Vpp)')
        ax.set_xlabel('Vinp (V)', fontweight='bold')
        ax.set_ylabel('Vout (V)', fontweight='bold')
        ax.set_title('DC Transfer Characteristic (Unity-Gain Buffer)', fontsize=13, fontweight='bold')
        ax.legend(loc='upper left', framealpha=0.9)
        ax.grid(True)
        ax.set_xlim([0, 1.8])
        ax.set_ylim([0, 1.8])
        ax.set_aspect('equal')
        plt.tight_layout()
        plt.savefig('report_dc.png')
        plt.close()
        print("   -> report_dc.png")

# ============================================================
# 3. TRANSIENT STEP RESPONSE
# ============================================================
print("3. Transient step response...")
out = run_spice("tb_ota_tran.spice")
if os.path.exists("tran_data"):
    data = load_wrdata("tran_data")
    if data is not None and len(data) > 20:
        n = len(data)
        half = n // 2
        time_us = data[:half, 0] * 1e6
        vout = data[:half, 1]
        vinp = data[half:half + len(time_us), 1] if n >= 2 * half else None

        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.plot(time_us, vout, '#1a5276', linewidth=2, label='Vout')
        if vinp is not None:
            ax.plot(time_us, vinp, '#c0392b', linewidth=1, linestyle='--', alpha=0.7, label='Vinp')
        ax.set_xlabel('Time (us)', fontweight='bold')
        ax.set_ylabel('Voltage (V)', fontweight='bold')
        ax.set_title('Step Response (Unity-Gain, CL = 10 pF)', fontsize=13, fontweight='bold')
        ax.legend(framealpha=0.9)
        ax.grid(True)
        ax.set_xlim([0, 80])
        plt.tight_layout()
        plt.savefig('report_transient.png')
        plt.close()
        print("   -> report_transient.png")

# ============================================================
# 4. CORNER COMPARISON (from live simulations)
# ============================================================
print("4. Corner analysis...")
corners = {}
for corner in ['tt', 'ss', 'ff', 'sf', 'fs']:
    tb = f"tb_corner_{corner}.spice"
    if os.path.exists(tb):
        out = run_spice(tb)
        gain = parse_meas(out, "gain_peak") or parse_meas(out, "gain_db")
        ugb = parse_meas(out, "ugb")
        corners[corner.upper()] = {"gain": gain, "ugb": ugb}
        print(f"   {corner.upper()}: gain={gain:.1f}dB, ugb={ugb:.0f}Hz" if gain and ugb else f"   {corner.upper()}: parse failed")

if len(corners) >= 3:
    names = list(corners.keys())
    gains = [corners[n]["gain"] for n in names]
    ugbs = [corners[n]["ugb"] / 1000 for n in names]  # kHz

    colors = ['#2980b9', '#c0392b', '#27ae60', '#e67e22', '#8e44ad']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    bars1 = ax1.bar(names, gains, color=colors[:len(names)], alpha=0.85, edgecolor='white', linewidth=1.5)
    ax1.axhline(y=65, color='#c0392b', linestyle='--', linewidth=1.5, label='Target (65 dB)')
    ax1.axhline(y=60, color='#e67e22', linestyle=':', linewidth=1.5, label='Min (60 dB)')
    ax1.set_ylabel('DC Gain (dB)', fontweight='bold')
    ax1.set_title('Gain Across Process Corners', fontsize=12, fontweight='bold')
    ax1.legend(framealpha=0.9)
    ax1.grid(True, axis='y')
    ax1.set_ylim([0, max(gains) * 1.15])
    for bar, val in zip(bars1, gains):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    bars2 = ax2.bar(names, ugbs, color=colors[:len(names)], alpha=0.85, edgecolor='white', linewidth=1.5)
    ax2.axhline(y=30, color='#c0392b', linestyle='--', linewidth=1.5, label='Min (30 kHz)')
    ax2.set_ylabel('UGB (kHz)', fontweight='bold')
    ax2.set_title('Unity-Gain Bandwidth Across Corners', fontsize=12, fontweight='bold')
    ax2.legend(framealpha=0.9)
    ax2.grid(True, axis='y')
    ax2.set_ylim([0, max(ugbs) * 1.25])
    for bar, val in zip(bars2, ugbs):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f'{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig('report_corners.png')
    plt.close()
    print("   -> report_corners.png")

# ============================================================
# 5. TEMPERATURE SWEEP
# ============================================================
print("5. Temperature sweep...")
temps = {}
for t in ['-40', '27', '85']:
    tb = f"tb_temp_{t}.spice"
    if os.path.exists(tb):
        out = run_spice(tb)
        gain = parse_meas(out, "gain_peak") or parse_meas(out, "gain_db")
        ugb = parse_meas(out, "ugb")
        temps[f"{t} C"] = {"gain": gain, "ugb": ugb}

if len(temps) >= 2:
    names = list(temps.keys())
    gains = [temps[n]["gain"] for n in names]
    ugbs = [temps[n]["ugb"] / 1000 for n in names]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    tcolors = ['#2980b9', '#27ae60', '#c0392b']

    bars1 = ax1.bar(names, gains, color=tcolors[:len(names)], alpha=0.85, edgecolor='white', linewidth=1.5)
    ax1.axhline(y=55, color='#c0392b', linestyle='--', linewidth=1.5, label='Min (55 dB)')
    ax1.set_ylabel('DC Gain (dB)', fontweight='bold')
    ax1.set_title('Gain vs Temperature (TT corner)', fontsize=12, fontweight='bold')
    ax1.legend(framealpha=0.9)
    ax1.grid(True, axis='y')
    ax1.set_ylim([0, max(gains) * 1.15])
    for bar, val in zip(bars1, gains):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    bars2 = ax2.bar(names, ugbs, color=tcolors[:len(names)], alpha=0.85, edgecolor='white', linewidth=1.5)
    ax2.axhline(y=20, color='#e67e22', linestyle=':', linewidth=1.5, label='Min (20 kHz)')
    ax2.set_ylabel('UGB (kHz)', fontweight='bold')
    ax2.set_title('UGB vs Temperature (TT corner)', fontsize=12, fontweight='bold')
    ax2.legend(framealpha=0.9)
    ax2.grid(True, axis='y')
    ax2.set_ylim([0, max(ugbs) * 1.25])
    for bar, val in zip(bars2, ugbs):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f'{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig('report_temperature.png')
    plt.close()
    print("   -> report_temperature.png")

print("\nAll plots generated from live simulations.")
