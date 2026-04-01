#!/usr/bin/env python3
"""Generate all 7 regulator characterization plots from simulation data."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

WD = '/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration'

# Common style
plt.rcParams.update({
    'font.size': 12,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'lines.linewidth': 2,
    'figure.figsize': (8, 5),
})

# ─── Plot 1: DC Regulation ──────────────────────────────────────────────
fig, ax = plt.subplots()
# Data from ngspice echo (rload → Iload = PVDD/Rload, PVDD)
rloads = [1000000, 5000, 500, 250, 166.7, 125, 100]
pvdds  = [4.9863, 4.98475, 4.98156, 4.30976, 3.20677, 4.88323, 2.13021]
# Compute load current: I = PVDD / Rload (in mA)
iloads = [p / r * 1000 for r, p in zip(rloads, pvdds)]
# Sort by current
pairs = sorted(zip(iloads, pvdds))
iloads_s, pvdds_s = zip(*pairs)
ax.plot(iloads_s, pvdds_s, 'b-o', markersize=6)
ax.set_xlabel('Load Current (mA)')
ax.set_ylabel('PVDD (V)')
ax.set_title('Plot 1: DC Regulation — PVDD vs Load Current')
ax.set_ylim(0, 6)
ax.axhline(y=5.0, color='gray', linestyle='--', alpha=0.5, label='Target 5.0V')
ax.legend()
fig.tight_layout()
fig.savefig(f'{WD}/plot_dc_regulation.png', dpi=150)
plt.close()
print("Plot 1: plot_dc_regulation.png saved")

# ─── Plot 2: Startup Transient ──────────────────────────────────────────
fig, ax = plt.subplots()
d_pvdd = np.loadtxt(f'{WD}/plot2_pvdd.dat')
d_gate = np.loadtxt(f'{WD}/plot2_gate.dat')
d_vref = np.loadtxt(f'{WD}/plot2_vref.dat')
ax.plot(d_pvdd[:,0]*1000, d_pvdd[:,1], 'b', label='PVDD')
ax.plot(d_gate[:,0]*1000, d_gate[:,1], 'r', label='Gate')
ax.plot(d_vref[:,0]*1000, d_vref[:,1], 'g', label='Vref_ss')
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Voltage (V)')
ax.set_title('Plot 2: Startup Transient')
ax.legend()
fig.tight_layout()
fig.savefig(f'{WD}/plot_startup.png', dpi=150)
plt.close()
print("Plot 2: plot_startup.png saved")

# ─── Plot 3: Load Transient ─────────────────────────────────────────────
fig, ax = plt.subplots()
d3 = np.loadtxt(f'{WD}/plot3_pvdd.dat')
ax.plot(d3[:,0]*1e6, d3[:,1], 'b')
ax.set_xlabel('Time (us)')
ax.set_ylabel('PVDD (V)')
ax.set_title('Plot 3: Load Transient (1mA → 10mA step)')
ax.axhline(y=5.0, color='gray', linestyle='--', alpha=0.5)
# Mark step times
ax.axvline(x=50, color='r', linestyle=':', alpha=0.5, label='1→10mA')
ax.axvline(x=150, color='g', linestyle=':', alpha=0.5, label='10→1mA')
ax.legend()
fig.tight_layout()
fig.savefig(f'{WD}/plot_load_transient.png', dpi=150)
plt.close()
print("Plot 3: plot_load_transient.png saved")

# ─── Plot 4: PSRR ───────────────────────────────────────────────────────
fig, ax = plt.subplots()
d4 = np.loadtxt(f'{WD}/plot4_psrr.dat')
ax.semilogx(d4[:,0], d4[:,1], 'b')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('PSRR (dB)')
ax.set_title('Plot 4: Power Supply Rejection Ratio')
ax.axhline(y=-40, color='r', linestyle='--', alpha=0.5, label='-40 dB target')
ax.legend()
fig.tight_layout()
fig.savefig(f'{WD}/plot_psrr.png', dpi=150)
plt.close()
print("Plot 4: plot_psrr.png saved")

# ─── Plot 5: Bode Plot ──────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
d5g = np.loadtxt(f'{WD}/plot5_gain.dat')
d5p = np.loadtxt(f'{WD}/plot5_phase.dat')
ax1.semilogx(d5g[:,0], d5g[:,1], 'b')
ax1.set_ylabel('Loop Gain (dB)')
ax1.set_title('Plot 5: Loop Stability — Bode Plot')
ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='0 dB')
ax1.legend()
ax2.semilogx(d5p[:,0], d5p[:,1], 'r')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Phase (degrees)')
ax2.axhline(y=-180, color='gray', linestyle='--', alpha=0.5, label='-180 deg')
ax2.legend()
fig.tight_layout()
fig.savefig(f'{WD}/plot_bode.png', dpi=150)
plt.close()
print("Plot 5: plot_bode.png saved")

# ─── Plot 6: Line Regulation ────────────────────────────────────────────
fig, ax = plt.subplots()
d6 = np.loadtxt(f'{WD}/line_reg_data.txt')
# Columns: time, v(bvdd), time, v(pvdd)
# Filter to the sweep region (t > 20ms where line sweep begins)
mask = d6[:,0] > 0.020
bvdd = d6[mask, 1]
pvdd = d6[mask, 3]
ax.plot(bvdd, pvdd, 'b')
ax.set_xlabel('BVDD (V)')
ax.set_ylabel('PVDD (V)')
ax.set_title('Plot 6: Line Regulation — PVDD vs BVDD')
ax.axhline(y=5.0, color='gray', linestyle='--', alpha=0.5, label='Target 5.0V')
ax.legend()
fig.tight_layout()
fig.savefig(f'{WD}/plot_line_reg.png', dpi=150)
plt.close()
print("Plot 6: plot_line_reg.png saved")

# ─── Plot 7: Current Limit ──────────────────────────────────────────────
fig, ax = plt.subplots()
d7 = np.loadtxt(f'{WD}/current_limit_data.txt')
# time vs v(pvdd). Load current ramps 0→500mA from 20ms to 120ms
time = d7[:,0]
pvdd7 = d7[:,1]
# Compute load current based on PWL: 0 before 20ms, linear 0→500mA from 20ms to 120ms
iload7 = np.where(time < 0.020, 0, np.minimum((time - 0.020) / 0.100 * 500, 500))
ax.plot(iload7, pvdd7, 'b')
ax.set_xlabel('Load Current (mA)')
ax.set_ylabel('PVDD (V)')
ax.set_title('Plot 7: Current Limit — PVDD vs Iload')
ax.axhline(y=5.0, color='gray', linestyle='--', alpha=0.5, label='Target 5.0V')
ax.set_xlim(0, 200)
ax.set_ylim(0, 6)
ax.legend()
fig.tight_layout()
fig.savefig(f'{WD}/plot_current_limit.png', dpi=150)
plt.close()
print("Plot 7: plot_current_limit.png saved")

print("\nAll 7 plots generated successfully!")
