import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('current_limit_data.txt')
time_s = data[:, 0]
pvdd = data[:, 1]

# Convert time to load current:
# PWL ramp: 0mA at t=20ms, 500mA at t=120ms → rate = 5 A/s
# Iload(t) = max(0, (t - 0.020)) * 5.0  [in Amps]
t_start = 0.020   # ramp starts at 20ms
ramp_rate = 5.0    # A/s

# Only use data from ramp region (t >= 20ms)
mask = time_s >= t_start
time_ramp = time_s[mask]
pvdd_ramp = pvdd[mask]
iload_a = (time_ramp - t_start) * ramp_rate
iload_ma = iload_a * 1000

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(iload_ma, pvdd_ramp, 'b-', linewidth=2)

ax.set_xlabel('Load Current (mA)', fontsize=12)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_title('Current Limit Characteristic: PVDD vs Load Current', fontsize=14)

# Find the clamp point: where PVDD drops below 4.5V (significant dropout)
clamp_idx = np.where(pvdd_ramp < 4.5)[0]
if len(clamp_idx) > 0:
    clamp_i = iload_ma[clamp_idx[0]]
    clamp_v = pvdd_ramp[clamp_idx[0]]
    ax.axvline(x=clamp_i, color='r', linestyle='--', linewidth=1, alpha=0.7)
    ax.annotate(f'Clamp ~{clamp_i:.0f} mA',
                xy=(clamp_i, clamp_v), xytext=(clamp_i + 30, clamp_v + 1.5),
                fontsize=10, arrowprops=dict(arrowstyle='->', color='red'),
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Also find where PVDD first drops below 4.9V (regulation lost)
reg_lost_idx = np.where(pvdd_ramp < 4.9)[0]
if len(reg_lost_idx) > 0:
    reg_i = iload_ma[reg_lost_idx[0]]
    ax.axvline(x=reg_i, color='orange', linestyle=':', linewidth=1, alpha=0.7)
    ax.annotate(f'Regulation lost\n~{reg_i:.0f} mA',
                xy=(reg_i, 4.9), xytext=(reg_i - 80, 3.5),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='orange'),
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax.axhline(y=5.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5, label='PVDD = 5.0V')
ax.set_xlim(-10, max(iload_ma) + 10)
ax.set_ylim(min(pvdd_ramp.min() - 0.5, -2.5), max(pvdd_ramp.max() + 0.5, 6))
ax.legend(loc='lower left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plots/plot7_current_limit.png', dpi=150)
print(f'Saved plots/plot7_current_limit.png')
print(f'Data range: Iload = {iload_ma[0]:.1f} to {iload_ma[-1]:.1f} mA')
print(f'PVDD range: {pvdd_ramp.min():.3f} to {pvdd_ramp.max():.3f} V')
if len(clamp_idx) > 0:
    print(f'Clamp point (PVDD < 4.5V): ~{clamp_i:.0f} mA')
if len(reg_lost_idx) > 0:
    print(f'Regulation lost (PVDD < 4.9V): ~{reg_i:.0f} mA')
