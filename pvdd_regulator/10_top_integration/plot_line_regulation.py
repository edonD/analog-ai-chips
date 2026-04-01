import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('line_reg_data.txt')
# wrdata with 2 vectors: time1 v(bvdd) time2 v(pvdd)
time = data[:, 0]
bvdd = data[:, 1]
pvdd = data[:, 3]

# Filter to the sweep region: 30ms to 80ms (BVDD 5.4V to 10.5V)
mask = (time >= 30e-3) & (time <= 80e-3)
bvdd_sweep = bvdd[mask]
pvdd_sweep = pvdd[mask]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(bvdd_sweep, pvdd_sweep, 'b-', linewidth=2, label='PVDD (measured)')
ax.axhline(y=5.0, color='r', linestyle='--', linewidth=1, label='5.0V target')

ax.set_xlabel('BVDD (V)', fontsize=12)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_title('Line Regulation: PVDD vs BVDD', fontsize=14)
ax.legend(fontsize=10)

# Calculate line regulation in the regulated region (BVDD > 6V)
reg_mask = bvdd_sweep > 6.0
if np.sum(reg_mask) > 2:
    bvdd_reg = bvdd_sweep[reg_mask]
    pvdd_reg = pvdd_sweep[reg_mask]
    delta_pvdd = pvdd_reg[-1] - pvdd_reg[0]
    delta_bvdd = bvdd_reg[-1] - bvdd_reg[0]
    line_reg_mvv = (delta_pvdd / delta_bvdd) * 1000
    ax.text(0.05, 0.92, f'Line reg = {line_reg_mvv:.2f} mV/V\n(BVDD {bvdd_reg[0]:.1f}V to {bvdd_reg[-1]:.1f}V)',
            transform=ax.transAxes, fontsize=10,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax.set_xlim(5.2, 10.7)

plt.tight_layout()
plt.savefig('plots/plot_line_regulation.png', dpi=150)
print('Saved plots/plot_line_regulation.png')
