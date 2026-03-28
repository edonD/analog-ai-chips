#!/usr/bin/env python3
"""plot_all.py — Generate all required plots for Block 04 Current Limiter"""

import subprocess
import sys

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("matplotlib/numpy not available — skipping plots")
    sys.exit(0)

# ===== PVT Threshold Bar Chart =====
corners = ['FF\n-40C', 'TT\n27C', 'SS\n150C']
thresholds = [58.9, 77.8, 110.3]  # mA

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(corners, thresholds, color=['#2196F3', '#4CAF50', '#FF9800'], width=0.5)
ax.axhline(y=50, color='red', linestyle='--', linewidth=2, label='Min spec (50 mA)')
ax.axhline(y=100, color='red', linestyle='--', linewidth=2, label='Max spec (100 mA)')
ax.axhline(y=75, color='gray', linestyle=':', linewidth=1, label='Target (75 mA)')
ax.set_ylabel('Current Limit Threshold (mA)')
ax.set_title('Block 04: Current Limit vs PVT Corner')
ax.set_ylim(0, 130)
ax.legend()
for bar, val in zip(bars, thresholds):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{val:.1f}', ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('ilim_pvt_threshold.png', dpi=150)
print("Saved ilim_pvt_threshold.png")

print("Plot generation complete")
