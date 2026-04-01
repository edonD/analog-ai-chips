#!/usr/bin/env python3
"""Plot 5: Loop Stability — Bode Plot (Gain + Phase)"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

gain_data = np.loadtxt('plot5_gain.dat')
phase_data = np.loadtxt('plot5_phase.dat')

freq = gain_data[:, 0]
gain_db = gain_data[:, 1]
phase_deg = phase_data[:, 1]

# Find UGB (0dB crossing)
ugb_idx = None
for i in range(1, len(gain_db)):
    if gain_db[i - 1] > 0 and gain_db[i] <= 0:
        ugb_idx = i
        break

ugb_hz = freq[ugb_idx] if ugb_idx else 0
# Phase already has +180 offset from spice (accounts for loop inversion)
# So PM is simply the phase value at UGB
pm_deg = phase_deg[ugb_idx] if ugb_idx else 0

# Find gain margin (phase = -180 crossing)
gm_idx = None
for i in range(1, len(phase_deg)):
    if phase_deg[i - 1] > -180 and phase_deg[i] <= -180:
        gm_idx = i
        break

gm_db = -gain_db[gm_idx] if gm_idx else float('inf')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# Gain plot
ax1.semilogx(freq, gain_db, 'b-', linewidth=2)
ax1.axhline(y=0, color='r', linestyle='--', linewidth=1, alpha=0.7, label='0 dB')
if ugb_idx:
    ax1.plot(ugb_hz, 0, 'ro', markersize=8)
    ax1.annotate(f'UGB = {ugb_hz/1e3:.1f} kHz',
                 xy=(ugb_hz, 0), xytext=(ugb_hz * 3, 15),
                 fontsize=9, color='red',
                 arrowprops=dict(arrowstyle='->', color='red', lw=1.2))
ax1.set_ylabel('Loop Gain (dB)', fontsize=11)
ax1.set_title('Loop Stability: Bode Plot (Rload=5k\u03a9, 1mA)', fontsize=12, fontweight='bold')
ax1.set_ylim(-40, 100)
ax1.legend(fontsize=9, loc='upper right')
ax1.tick_params(axis='both', which='major', labelsize=10)

# Phase plot
ax2.semilogx(freq, phase_deg, 'b-', linewidth=2)
ax2.axhline(y=-180, color='r', linestyle='--', linewidth=1, alpha=0.7, label='-180\u00b0')
if ugb_idx:
    ax2.plot(ugb_hz, phase_deg[ugb_idx], 'ro', markersize=8)
    ax2.annotate(f'PM = {pm_deg:.1f}\u00b0',
                 xy=(ugb_hz, phase_deg[ugb_idx]),
                 xytext=(ugb_hz * 3, phase_deg[ugb_idx] - 30),
                 fontsize=9, color='red',
                 arrowprops=dict(arrowstyle='->', color='red', lw=1.2))
ax2.set_xlabel('Frequency (Hz)', fontsize=11)
ax2.set_ylabel('Phase (degrees)', fontsize=11)
ax2.set_xlim(1, 1e8)
ax2.set_ylim(-270, 90)
ax2.legend(fontsize=9, loc='upper right')
ax2.tick_params(axis='both', which='major', labelsize=10)

plt.tight_layout()
plt.savefig('plot_bode.png', dpi=150, bbox_inches='tight')
print(f'Saved plot_bode.png  (UGB={ugb_hz/1e3:.1f}kHz, PM={pm_deg:.1f}deg, GM={gm_db:.1f}dB)')
