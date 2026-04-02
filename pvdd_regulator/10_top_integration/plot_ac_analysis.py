#!/usr/bin/env python3
"""Generate AC analysis plots: PSRR, Bode, PSRR vs Load."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

# Annotate key points
for fpt in [100, 1000, 10000]:
    idx = np.argmin(np.abs(freq - fpt))
    ax.plot(freq[idx], psrr[idx], 'ro', markersize=4)
    label = f'{fpt/1e3:.0f}kHz' if fpt >= 1000 else f'{fpt}Hz'
    ax.annotate(f'{psrr[idx]:.1f} dB\n@ {label}', xy=(freq[idx], psrr[idx]),
                xytext=(freq[idx]*2, psrr[idx]+4), fontsize=8, color='red')

ax.set_xlabel('Frequency (Hz)', fontsize=11)
ax.set_ylabel('PSRR (dB)', fontsize=11)
ax.set_title('Power Supply Rejection Ratio — TT 27°C, 10 mA load', fontsize=12, fontweight='bold')
ax.set_xlim(1, 10e6)
ax.set_ylim(-80, 10)
ax.grid(True, which='both', alpha=0.3)
ax.legend(loc='upper right')
fig.tight_layout()
fig.savefig('plot_psrr.png', dpi=150)
plt.close(fig)
print(f'Saved plot_psrr.png — DC PSRR = {psrr[0]:.1f} dB, @1kHz = {psrr[np.argmin(np.abs(freq-1000))]:.1f} dB')

# ============================================================
# Plot 2: Bode Plot (plot_bode.png)
# ============================================================
data = np.loadtxt('bode_data.txt')
freq = data[:, 0]
gain_db = data[:, 1]
phase_raw = data[:, 3]

# Truncate at 30kHz where PSRR-derived loop gain becomes unreliable
# (feedthrough assumption breaks down at HF due to output caps)
valid = freq <= 30000
freq_v = freq[valid]
gain_v = gain_db[valid]
phase_v = phase_raw[valid]
# Wrap phase to [-180, 180]
phase_v = np.mod(phase_v + 180, 360) - 180

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

# Gain
ax1.semilogx(freq_v, gain_v, 'b-', linewidth=1.5, label='Loop Gain')
ax1.set_xlabel('Frequency (Hz)', fontsize=11)
ax1.set_ylabel('Loop Gain (dB)', fontsize=11, color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.set_xlim(1, 1e5)
ax1.set_ylim(-10, 80)
ax1.axhline(0, color='b', linestyle=':', linewidth=0.5)
ax1.grid(True, which='both', alpha=0.3)

# Phase
ax2.semilogx(freq_v, phase_v, 'r--', linewidth=1.5, label='Phase')
ax2.set_ylabel('Phase (degrees)', fontsize=11, color='r')
ax2.tick_params(axis='y', labelcolor='r')
ax2.set_ylim(-180, 90)

# Annotate DC gain
ax1.annotate(f'DC gain = {gain_v[0]:.1f} dB', xy=(freq_v[0], gain_v[0]),
             xytext=(3, gain_v[0] - 5), fontsize=9, color='blue',
             arrowprops=dict(arrowstyle='->', color='blue', lw=0.8))

# Estimate UGB by extrapolation from -20 dB/dec rolloff
# Use data between 1kHz and 10kHz for slope
i1k = np.argmin(np.abs(freq_v - 1000))
i10k = np.argmin(np.abs(freq_v - 10000))
slope = (gain_v[i10k] - gain_v[i1k]) / (np.log10(freq_v[i10k]) - np.log10(freq_v[i1k]))
ugb_est = 10**(np.log10(freq_v[i10k]) - gain_v[i10k] / slope)
ax1.annotate(f'UGB (est.) ~ {ugb_est/1e3:.0f} kHz\n(extrapolated)',
             xy=(freq_v[-1], gain_v[-1]),
             xytext=(freq_v[-1]/5, 15), fontsize=8, color='green')
print(f'Estimated UGB ~ {ugb_est:.0f} Hz ({ugb_est/1e3:.1f} kHz), slope = {slope:.1f} dB/dec')

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

ax1.set_title('Loop Gain (from PSRR) — TT 27°C, 10 mA load', fontsize=12, fontweight='bold')
fig.tight_layout()
fig.savefig('plot_bode.png', dpi=150)
plt.close(fig)
print(f'Saved plot_bode.png — DC gain = {gain_v[0]:.1f} dB')

# ============================================================
# Plot 3: PSRR vs Load (plot_psrr_vs_load.png)
# ============================================================
# Read actual PSRR @ 1kHz from simulation data files
loads = [0, 1, 10, 50]
files = ['psrr_0ma.txt', 'psrr_1ma.txt', 'psrr_data.txt', 'psrr_50ma.txt']
psrr_vals = []
for f in files:
    d = np.loadtxt(f)
    idx = np.argmin(np.abs(d[:, 0] - 1000))
    psrr_vals.append(d[idx, 1])

fig, ax = plt.subplots(figsize=(7, 5))
colors = []
for v in psrr_vals:
    norm = min(1.0, max(0.0, (-v) / 60.0))
    colors.append(plt.cm.Blues(0.3 + 0.7 * norm))

bars = ax.bar([str(l) for l in loads], psrr_vals, color=colors, edgecolor='navy', linewidth=0.8)
ax.set_xlabel('Load Current (mA)', fontsize=11)
ax.set_ylabel('PSRR at 1 kHz (dB)', fontsize=11)
ax.set_title('PSRR at 1 kHz vs Load Current — TT 27°C', fontsize=12, fontweight='bold')
ax.set_ylim(-70, 0)
ax.axhline(-40, color='green', linestyle='--', linewidth=0.8, label='Spec: -40 dB')
ax.grid(True, axis='y', alpha=0.3)
ax.legend(loc='upper right')

for bar, val in zip(bars, psrr_vals):
    ax.text(bar.get_x() + bar.get_width()/2, val - 2, f'{val:.1f} dB',
            ha='center', va='top', fontsize=9, fontweight='bold', color='white')

fig.tight_layout()
fig.savefig('plot_psrr_vs_load.png', dpi=150)
plt.close(fig)
print(f'Saved plot_psrr_vs_load.png — PSRR: {", ".join(f"{v:.1f}" for v in psrr_vals)} dB')
