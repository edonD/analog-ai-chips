import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('line_reg_data.txt')
bvdd = data[:, 0]
pvdd = data[:, 1]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(bvdd, pvdd, 'b-', linewidth=2, label='PVDD (measured)')
ax.axhline(y=5.0, color='r', linestyle='--', linewidth=1, label='5.0V target')

ax.set_xlabel('BVDD (V)', fontsize=12)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_title('Line Regulation: PVDD vs BVDD', fontsize=14)
ax.legend(fontsize=10)

# Calculate line regulation
delta_pvdd = pvdd[-1] - pvdd[0]
delta_bvdd = bvdd[-1] - bvdd[0]
line_reg_mvv = (delta_pvdd / delta_bvdd) * 1000
ax.text(0.05, 0.92, f'Line reg = {line_reg_mvv:.2f} mV/V',
        transform=ax.transAxes, fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax.set_xlim(5.2, 10.7)
ax.set_ylim(pvdd.min() - 0.001, pvdd.max() + 0.001)

plt.tight_layout()
plt.savefig('plots/plot_line_regulation.png', dpi=150)
print('Saved plots/plot_line_regulation.png')
