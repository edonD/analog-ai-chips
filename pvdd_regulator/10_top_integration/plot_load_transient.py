#!/usr/bin/env python3
"""Plot 3: Load Transient — PVDD vs time with 1→10mA step"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('plot3_pvdd.dat')
time_us = data[:, 0] * 1e6  # s -> us
pvdd = data[:, 1]

# Find undershoot (min after step-up at 50us) and overshoot (max after step-down at 150us)
mask_under = (time_us >= 50) & (time_us <= 100)
mask_over = (time_us >= 150) & (time_us <= 200)
mask_ss = (time_us >= 30) & (time_us <= 49)

pvdd_ss = np.mean(pvdd[mask_ss])
pvdd_min = np.min(pvdd[mask_under])
pvdd_max = np.max(pvdd[mask_over])
idx_min = np.argmin(pvdd[mask_under]) + np.argmax(mask_under)
idx_max = np.argmax(pvdd[mask_over]) + np.argmax(mask_over)

undershoot_mv = (pvdd_ss - pvdd_min) * 1000
overshoot_mv = (pvdd_max - pvdd_ss) * 1000

fig, ax = plt.subplots(figsize=(8, 4.5))

ax.plot(time_us, pvdd, 'b-', linewidth=1.5)

# Annotate undershoot
ax.annotate(f'Undershoot: {undershoot_mv:.1f} mV',
            xy=(time_us[idx_min], pvdd_min),
            xytext=(80, pvdd_min - 0.03),
            fontsize=9, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.2))

# Annotate overshoot
ax.annotate(f'Overshoot: {overshoot_mv:.1f} mV',
            xy=(time_us[idx_max], pvdd_max),
            xytext=(180, pvdd_max + 0.03),
            fontsize=9, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.2))

# Step indicators
ax.axvline(x=50, color='gray', linestyle=':', linewidth=0.8, alpha=0.6)
ax.axvline(x=150, color='gray', linestyle=':', linewidth=0.8, alpha=0.6)
ax.text(50, ax.get_ylim()[0] + 0.002, '1\u219210mA', fontsize=8, ha='center', color='gray')
ax.text(150, ax.get_ylim()[0] + 0.002, '10\u21921mA', fontsize=8, ha='center', color='gray')

ax.set_xlabel('Time (\u00b5s)', fontsize=11)
ax.set_ylabel('PVDD (V)', fontsize=11)
ax.set_title('Load Transient: 1mA \u2192 10mA Step Response', fontsize=12, fontweight='bold')
ax.set_xlim(0, 250)
ax.tick_params(axis='both', which='major', labelsize=10)

plt.tight_layout()
plt.savefig('plot_load_transient.png', dpi=150, bbox_inches='tight')
print(f'Saved plot_load_transient.png  (undershoot={undershoot_mv:.1f}mV, overshoot={overshoot_mv:.1f}mV)')
