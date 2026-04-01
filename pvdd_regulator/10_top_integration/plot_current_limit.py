import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('current_limit_data.txt')
iload_a = data[:, 0]
pvdd = data[:, 1]
iload_ma = iload_a * 1000

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(iload_ma, pvdd, 'b-', linewidth=2)

ax.set_xlabel('Load Current (mA)', fontsize=12)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_title('Current Limit Characteristic: PVDD vs Load Current', fontsize=14)

# Find the clamp point: where PVDD drops below 4.5V (significant dropout)
clamp_idx = np.where(pvdd < 4.5)[0]
if len(clamp_idx) > 0:
    clamp_i = iload_ma[clamp_idx[0]]
    clamp_v = pvdd[clamp_idx[0]]
    ax.axvline(x=clamp_i, color='r', linestyle='--', linewidth=1, alpha=0.7)
    ax.annotate(f'Clamp ~{clamp_i:.0f} mA',
                xy=(clamp_i, clamp_v), xytext=(clamp_i + 10, clamp_v + 0.5),
                fontsize=10, arrowprops=dict(arrowstyle='->', color='red'),
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Also find where PVDD first drops below 5.0V (regulation lost)
reg_lost_idx = np.where(pvdd < 5.0)[0]
if len(reg_lost_idx) > 0:
    reg_i = iload_ma[reg_lost_idx[0]]
    ax.axvline(x=reg_i, color='orange', linestyle=':', linewidth=1, alpha=0.7)
    ax.annotate(f'Regulation lost\n~{reg_i:.0f} mA',
                xy=(reg_i, 5.0), xytext=(reg_i + 8, 5.5),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='orange'),
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax.axhline(y=5.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
ax.set_xlim(-2, 102)
ax.set_ylim(min(pvdd.min() - 0.5, -1), max(pvdd.max() + 0.5, 7))

plt.tight_layout()
plt.savefig('plots/plot_current_limit.png', dpi=150)
print('Saved plots/plot_current_limit.png')
