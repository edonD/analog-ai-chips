import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('uvov_data.txt')
# wrdata with 3 vectors: time1 v(pvdd) time2 v(uv_flag) time3 v(ov_flag)
pvdd = data[:, 1]
uv_flag = data[:, 3]
ov_flag = data[:, 5]

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(pvdd, uv_flag, 'b-', linewidth=1.5, label='UV Flag')
ax.plot(pvdd, ov_flag, 'r-', linewidth=1.5, label='OV Flag')

ax.set_xlabel('PVDD (V)', fontsize=12)
ax.set_ylabel('Flag Voltage (V)', fontsize=12)
ax.set_title('UV/OV Comparator Thresholds vs PVDD', fontsize=14)
ax.legend(fontsize=10)

# Find UV trip point: where uv_flag crosses 1.1V (falling)
uv_cross = None
for i in range(1, len(pvdd)):
    if uv_flag[i-1] > 1.1 and uv_flag[i] <= 1.1:
        # Linear interpolation
        frac = (1.1 - uv_flag[i]) / (uv_flag[i-1] - uv_flag[i])
        uv_cross = pvdd[i] + frac * (pvdd[i-1] - pvdd[i])
        break

# Find OV trip point: where ov_flag crosses 1.1V (rising)
ov_cross = None
for i in range(1, len(pvdd)):
    if ov_flag[i-1] < 1.1 and ov_flag[i] >= 1.1:
        frac = (1.1 - ov_flag[i-1]) / (ov_flag[i] - ov_flag[i-1])
        ov_cross = pvdd[i-1] + frac * (pvdd[i] - pvdd[i-1])
        break

if uv_cross is not None:
    ax.axvline(x=uv_cross, color='b', linestyle=':', linewidth=1, alpha=0.5)
    ax.annotate(f'UV trip\n{uv_cross:.2f} V',
                xy=(uv_cross, 1.1), xytext=(uv_cross - 1.2, 1.5),
                fontsize=10, arrowprops=dict(arrowstyle='->', color='blue'),
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

if ov_cross is not None:
    ax.axvline(x=ov_cross, color='r', linestyle=':', linewidth=1, alpha=0.5)
    ax.annotate(f'OV trip\n{ov_cross:.2f} V',
                xy=(ov_cross, 1.1), xytext=(ov_cross + 0.3, 1.5),
                fontsize=10, arrowprops=dict(arrowstyle='->', color='red'),
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Mark normal operating range
ax.axvline(x=5.0, color='green', linestyle='--', linewidth=1, alpha=0.4, label='PVDD=5.0V target')
ax.legend(fontsize=9, loc='center right')

ax.set_xlim(0, 7)
ax.set_ylim(-0.1, 2.4)

plt.tight_layout()
plt.savefig('plots/plot_uvov.png', dpi=150)
print('Saved plots/plot_uvov.png')
print(f'UV trip: {uv_cross:.3f} V' if uv_cross else 'UV trip not found')
print(f'OV trip: {ov_cross:.3f} V' if ov_cross else 'OV trip not found')
