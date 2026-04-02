#!/usr/bin/env python3
"""Plot current limit characteristic from .OP steady-state measurements."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Read data
data = []
with open('/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration/ilim_dc_data.txt') as f:
    for line in f:
        if line.startswith('#') or line.strip() == '':
            continue
        parts = line.strip().split()
        if len(parts) >= 2:
            try:
                iload_ma = float(parts[0])
                pvdd = float(parts[1])
                if pvdd < 0:
                    pvdd = 0.0
                data.append((iload_ma, pvdd))
            except:
                continue

data.sort(key=lambda x: x[0])
iload = np.array([d[0] for d in data])
pvdd = np.array([d[1] for d in data])

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(iload, pvdd, 'b-o', linewidth=2, markersize=4, label='PVDD (DC operating point)')
ax.axhline(y=5.0, color='gray', linestyle='--', alpha=0.5, label='5.0V target')
ax.axvline(x=50, color='red', linestyle='--', alpha=0.7, label='50mA short-circuit limit')

ax.set_xlabel('Load Current (mA)', fontsize=12)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_title('Current Limit Characteristic — DC Operating Point (TT 27°C)', fontsize=13)
ax.set_xlim(0, 55)
ax.set_ylim(-0.2, 6.5)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right', fontsize=10)

# Annotate regulation region
ax.annotate('Regulation\n(PVDD ≈ 5.0V)', xy=(12, 4.98), xytext=(8, 3.8),
            fontsize=10, ha='center', arrowprops=dict(arrowstyle='->', color='blue'),
            color='blue')

# Annotate foldback region
ax.annotate('Foldback: PVDD drops,\ncurrent clamped 17→50mA',
            xy=(30, 1.6), xytext=(35, 2.8),
            fontsize=9, ha='center', arrowprops=dict(arrowstyle='->', color='red'),
            color='red')

# Annotate short-circuit current
ax.annotate('Isc = 49.9mA', xy=(49.9, 0.0), xytext=(42, 0.6),
            fontsize=10, ha='center', arrowprops=dict(arrowstyle='->', color='darkred'),
            color='darkred')

# Shade regulation region
ax.axvspan(0, 15, alpha=0.05, color='green')
ax.text(7.5, 6.1, 'Regulation', ha='center', fontsize=9, color='green', style='italic')

# Shade foldback region
ax.axvspan(15, 50, alpha=0.05, color='red')
ax.text(32.5, 6.1, 'Current Limit (Foldback)', ha='center', fontsize=9, color='red', style='italic')

plt.tight_layout()
plt.savefig('/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration/plot_current_limit.png', dpi=150)
print("Plot saved to plot_current_limit.png")

# Print summary
print("\nData points:")
for i_ma, v in zip(iload, pvdd):
    print(f"  {i_ma:7.2f} mA -> {v:.4f} V")
