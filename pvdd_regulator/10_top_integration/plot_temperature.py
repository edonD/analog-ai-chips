import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

temps = [-40, -20, 0, 27, 50, 85, 125, 150]
pvdd_vals = [5.000664, 5.000604, 5.000563, 5.000539, 5.000554, 5.000648, 5.000882, 5.001106]

temps = np.array(temps)
pvdd = np.array(pvdd_vals)

# Convert to mV deviation from 5.0V
pvdd_mv = (pvdd - 5.0) * 1000

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left: PVDD absolute
ax1.plot(temps, pvdd, 'bo-', linewidth=2, markersize=6)
ax1.axhline(y=5.0, color='r', linestyle='--', linewidth=1, alpha=0.7, label='5.0V target')
ax1.axhline(y=4.9, color='orange', linestyle=':', linewidth=1, alpha=0.7, label='Spec limits')
ax1.axhline(y=5.1, color='orange', linestyle=':', linewidth=1, alpha=0.7)
ax1.set_xlabel('Temperature (C)', fontsize=12)
ax1.set_ylabel('PVDD (V)', fontsize=12)
ax1.set_title('PVDD vs Temperature', fontsize=14)
ax1.legend(fontsize=9)
ax1.set_xlim(-50, 160)

# Right: mV deviation (zoomed in)
ax2.plot(temps, pvdd_mv, 'ro-', linewidth=2, markersize=6)
ax2.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
ax2.set_xlabel('Temperature (C)', fontsize=12)
ax2.set_ylabel('PVDD Deviation from 5.0V (mV)', fontsize=12)
ax2.set_title('Temperature Coefficient Detail', fontsize=14)
ax2.set_xlim(-50, 160)

# Annotate TC
tc = (pvdd_mv[-1] - pvdd_mv[0]) / (temps[-1] - temps[0])
ax2.text(0.05, 0.92, f'TC = {tc:.3f} mV/C\n({tc*1000/5.0:.1f} ppm/C)',
         transform=ax2.transAxes, fontsize=10,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('plots/plot_temperature.png', dpi=150)
print('Saved plots/plot_temperature.png')
