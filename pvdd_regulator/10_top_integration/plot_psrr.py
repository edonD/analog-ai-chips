#!/usr/bin/env python3
"""Plot 4: PSRR — Magnitude in dB vs Frequency"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('plot4_psrr.dat')
freq = data[:, 0]
psrr_db = data[:, 1]

fig, ax = plt.subplots(figsize=(8, 4.5))

ax.semilogx(freq, psrr_db, 'b-', linewidth=2)

# Spec lines
ax.axhline(y=-20, color='r', linestyle='--', linewidth=1, alpha=0.7, label='-20 dB spec')
ax.axhline(y=-40, color='orange', linestyle='--', linewidth=1, alpha=0.7, label='-40 dB spec')

# Key frequency annotations
for f_target, label in [(100, '100Hz'), (1e3, '1kHz'), (10e3, '10kHz'), (100e3, '100kHz'), (1e6, '1MHz')]:
    idx = np.argmin(np.abs(freq - f_target))
    ax.plot(freq[idx], psrr_db[idx], 'ko', markersize=4)
    ax.annotate(f'{label}\n{psrr_db[idx]:.1f}dB', xy=(freq[idx], psrr_db[idx]),
                xytext=(0, 10), textcoords='offset points', fontsize=7, ha='center')

ax.set_xlabel('Frequency (Hz)', fontsize=11)
ax.set_ylabel('PSRR (dB)', fontsize=11)
ax.set_title('Power Supply Rejection Ratio (Rload=500\u03a9, 10mA)', fontsize=12, fontweight='bold')
ax.set_xlim(1, 1e7)
ax.legend(fontsize=9, loc='upper right')
ax.tick_params(axis='both', which='major', labelsize=10)

plt.tight_layout()
plt.savefig('plot_psrr.png', dpi=150, bbox_inches='tight')
print(f'Saved plot_psrr.png  (PSRR_DC={psrr_db[0]:.1f}dB)')
