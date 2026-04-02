#!/usr/bin/env python3
"""Plot 1: DC Regulation — PVDD vs Load Current"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Data from fresh ngspice simulation — post FIX-19 through FIX-23
rload_vals = [1000000, 5000, 500, 250, 166.7, 125, 100]
pvdd_vals  = [5.0011, 5.00107, 5.001, 5.00096, 5.00093, 5.00091, 5.00089]

# Compute load currents: I = V/R (in mA)
iload_ma = [v / r * 1000 for v, r in zip(pvdd_vals, rload_vals)]

fig, ax = plt.subplots(figsize=(7, 4.5))

ax.plot(iload_ma, pvdd_vals, 'b-o', linewidth=2, markersize=6, label='PVDD')

# Spec limits
ax.axhline(y=5.175, color='r', linestyle='--', linewidth=1, alpha=0.7, label='Upper spec (5.175 V)')
ax.axhline(y=4.825, color='r', linestyle='--', linewidth=1, alpha=0.7, label='Lower spec (4.825 V)')
ax.axhline(y=5.0, color='gray', linestyle=':', linewidth=0.8, alpha=0.5, label='Nominal (5.0 V)')

ax.set_xlabel('Load Current (mA)', fontsize=11)
ax.set_ylabel('PVDD (V)', fontsize=11)
ax.set_title('DC Regulation: PVDD vs Load Current', fontsize=12, fontweight='bold')
ax.set_xlim(-1, 65)
ax.set_ylim(4.7, 5.3)
ax.legend(fontsize=9, loc='lower left')

ax.tick_params(axis='both', which='major', labelsize=10)
plt.tight_layout()
plt.savefig('plot_dc_regulation.png', dpi=150, bbox_inches='tight')
print('Saved plot_dc_regulation.png')
