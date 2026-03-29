#!/usr/bin/env python3
"""plot_all.py — Generate all required plots for Block 04 Current Limiter"""
import sys
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("matplotlib/numpy not available — skipping plots")
    sys.exit(0)

# ===== I-V Curve =====
try:
    data = np.loadtxt('ilim_iv_data')
    vgate = data[:, 0]  # Gate drive voltage
    iload = data[:, 1] * 1000  # Current in mA

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(vgate, iload, 'b-', linewidth=2)
    ax.axhline(y=79, color='red', linestyle='--', alpha=0.7, label='Limit ~79 mA')
    ax.set_xlabel('Gate Drive Voltage (V)')
    ax.set_ylabel('Load Current (mA)')
    ax.set_title('Block 04: I-V Curve — Current Limiting')
    ax.set_xlim(7, 0)
    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('ilim_iv_curve.png', dpi=150)
    print("Saved ilim_iv_curve.png")
except Exception as e:
    print(f"I-V plot skipped: {e}")

# ===== PVT Threshold Bar Chart =====
corners = ['FF -40C', 'TT 27C', 'SS 150C']
thresholds = [43.4, 79.0, 135.7]

fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#2196F3', '#4CAF50', '#FF9800']
bars = ax.bar(corners, thresholds, color=colors, width=0.5)
ax.axhline(y=50, color='red', linestyle='--', linewidth=2, label='Min spec (50 mA)')
ax.axhline(y=100, color='red', linestyle='--', linewidth=2, label='Max spec (100 mA)')
ax.axhline(y=75, color='gray', linestyle=':', linewidth=1, label='Target (75 mA)')
ax.set_ylabel('Current Limit Threshold (mA)')
ax.set_title('Block 04: Current Limit vs PVT Corner')
ax.set_ylim(0, 160)
ax.legend()
for bar, val in zip(bars, thresholds):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
            f'{val:.1f}', ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('ilim_pvt_threshold.png', dpi=150)
print("Saved ilim_pvt_threshold.png")

print("All plots generated")
