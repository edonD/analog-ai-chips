#!/usr/bin/env python3
"""Generate AC analysis plots: PSRR, Bode, PSRR vs Load."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator

# ============================================================
# Plot 1: PSRR (plot_psrr.png)
# ============================================================
data = np.loadtxt('psrr_data.txt')
freq = data[:, 0]
psrr = data[:, 1]

fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogx(freq, psrr, 'b-', linewidth=1.5, label='PSRR')
ax.axhline(-40, color='gray', linestyle='--', linewidth=0.8)
ax.axhline(-20, color='gray', linestyle='--', linewidth=0.8)
ax.text(2, -39, 'Spec: -40 dB', fontsize=8, color='gray', va='bottom')
ax.text(2, -19, '-20 dB', fontsize=8, color='gray', va='bottom')
ax.set_xlabel('Frequency (Hz)', fontsize=11)
ax.set_ylabel('PSRR (dB)', fontsize=11)
ax.set_title('Power Supply Rejection Ratio \u2014 TT 27\u00b0C, 10 mA load', fontsize=12, fontweight='bold')
ax.set_xlim(1, 10e6)
ax.set_ylim(-70, 10)
ax.grid(True, which='both', alpha=0.3)
ax.legend(loc='upper right')
fig.tight_layout()
fig.savefig('plot_psrr.png', dpi=150)
plt.close(fig)
print('Saved plot_psrr.png')

# ============================================================
# Plot 2: Bode Plot (plot_bode.png)
# ============================================================
data = np.loadtxt('bode_data.txt')
freq = data[:, 0]
gain_db = data[:, 1]
# Phase is in col 3 (col 2 is freq repeated)
phase_raw = data[:, 3]
# Wrap phase to [-180, 180]
phase = phase_raw.copy()
phase = np.mod(phase + 180, 360) - 180

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

# Gain
ax1.semilogx(freq, gain_db, 'b-', linewidth=1.5, label='Gain')
ax1.set_xlabel('Frequency (Hz)', fontsize=11)
ax1.set_ylabel('Gain (dB)', fontsize=11, color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.set_xlim(1, 10e6)
ax1.set_ylim(-60, 40)
ax1.axhline(0, color='b', linestyle=':', linewidth=0.5)
ax1.grid(True, which='both', alpha=0.3)

# Phase
ax2.semilogx(freq, phase, 'r--', linewidth=1.5, label='Phase')
ax2.set_ylabel('Phase (degrees)', fontsize=11, color='r')
ax2.tick_params(axis='y', labelcolor='r')
ax2.set_ylim(-180, 180)

# Find UGB (0dB crossing)
ugb_idx = None
for i in range(len(gain_db) - 1):
    if gain_db[i] >= 0 and gain_db[i+1] < 0:
        # Interpolate
        f1, f2 = freq[i], freq[i+1]
        g1, g2 = gain_db[i], gain_db[i+1]
        ugb_freq = f1 * (f2/f1) ** (-g1 / (g2 - g1))
        pm_val = np.interp(np.log10(ugb_freq), np.log10(freq), phase)
        pm = 180 + pm_val  # phase margin = 180 + phase (phase is negative at UGB)
        ugb_idx = i
        break

if ugb_idx is not None:
    ax1.axvline(ugb_freq, color='green', linestyle='-.', linewidth=1, alpha=0.7)
    ax1.annotate(f'UGB = {ugb_freq:.0f} Hz', xy=(ugb_freq, 0),
                 xytext=(ugb_freq*3, 10), fontsize=9, color='green',
                 arrowprops=dict(arrowstyle='->', color='green', lw=0.8))
    ax1.annotate(f'PM = {pm:.1f}\u00b0', xy=(ugb_freq, pm_val),
                 xytext=(ugb_freq*5, pm_val - 20), fontsize=9, color='red',
                 arrowprops=dict(arrowstyle='->', color='red', lw=0.8))
    print(f'UGB = {ugb_freq:.0f} Hz, Phase Margin = {pm:.1f} deg')
else:
    print('WARNING: No 0dB crossing found in gain data')
    # Still annotate DC gain
    ax1.annotate(f'DC gain = {gain_db[0]:.1f} dB', xy=(freq[0], gain_db[0]),
                 xytext=(10, gain_db[0] - 5), fontsize=9, color='blue')

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower left')

ax1.set_title('Loop Gain Bode Plot \u2014 TT 27\u00b0C, 10 mA load', fontsize=12, fontweight='bold')
fig.tight_layout()
fig.savefig('plot_bode.png', dpi=150)
plt.close(fig)
print('Saved plot_bode.png')

# ============================================================
# Plot 3: PSRR vs Load (plot_psrr_vs_load.png)
# ============================================================
loads = [0, 1, 10, 50]
psrr_vals = [-5.42, -48.47, -6.30, -46.89]

fig, ax = plt.subplots(figsize=(7, 5))
colors = []
for v in psrr_vals:
    # Darker = more negative = better
    norm = min(1.0, max(0.0, (-v) / 60.0))
    colors.append(plt.cm.Blues(0.3 + 0.7 * norm))

bars = ax.bar([str(l) for l in loads], psrr_vals, color=colors, edgecolor='navy', linewidth=0.8)
ax.set_xlabel('Load Current (mA)', fontsize=11)
ax.set_ylabel('PSRR at 1 kHz (dB)', fontsize=11)
ax.set_title('PSRR at 1 kHz vs Load Current', fontsize=12, fontweight='bold')
ax.set_ylim(-70, 0)
ax.grid(True, axis='y', alpha=0.3)

# Add value labels on bars
for bar, val in zip(bars, psrr_vals):
    ax.text(bar.get_x() + bar.get_width()/2, val - 2, f'{val:.1f} dB',
            ha='center', va='top', fontsize=9, fontweight='bold', color='white')

fig.tight_layout()
fig.savefig('plot_psrr_vs_load.png', dpi=150)
plt.close(fig)
print('Saved plot_psrr_vs_load.png')
