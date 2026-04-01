import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

corners = ['tt', 'ss', 'ff', 'sf', 'fs']
colors = ['#1f77b4', '#d62728', '#2ca02c', '#9467bd', '#ff7f0e']
labels = ['TT (typical)', 'SS (slow-slow)', 'FF (fast-fast)', 'SF (slow-fast)', 'FS (fast-slow)']

fig, ax = plt.subplots(figsize=(8, 5))

for corner, color, label in zip(corners, colors, labels):
    data = np.loadtxt(f'pvt_{corner}_data.txt')
    time_s = data[:, 0]
    pvdd = data[:, 1]
    time_ms = time_s * 1000
    ax.plot(time_ms, pvdd, color=color, linewidth=1.5, label=label)

ax.axhline(y=5.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)

ax.set_xlabel('Time (ms)', fontsize=12)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_title('PVT Corner Analysis: Startup Transient', fontsize=14)
ax.legend(fontsize=9, loc='lower right')
ax.set_xlim(0, 20)
ax.set_ylim(-0.5, 6.5)

plt.tight_layout()
plt.savefig('plots/plot_pvt_corners.png', dpi=150)
print('Saved plots/plot_pvt_corners.png')
