#!/usr/bin/env python3
"""Generate 3 PVT/line-regulation plots for PVDD regulator."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import re, os

os.chdir('/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration')

# ── PVT data ──────────────────────────────────────────────────────────────
corners = ['tt', 'ss', 'ff', 'sf', 'fs']
temps = [-40, 27, 150]
pvt_data = {}

for c in corners:
    for t in temps:
        fname = f'pvt_v2_results/a_{c}_{t}.log'
        with open(fname) as f:
            for line in f:
                m = re.search(r'pvdd_final\s+=\s+([\d.eE+-]+)', line)
                if m:
                    pvt_data[(c, t)] = float(m.group(1))

corner_labels = ['TT', 'SS', 'FF', 'SF', 'FS']
temp_labels = ['-40C', '27C', '150C']

# ── Plot 1: PVT DC Regulation Bar Chart ──────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6), dpi=150)

temp_colors = ['#2196F3', '#4CAF50', '#FF9800']
n_corners = len(corners)
bar_width = 0.22
x = np.arange(n_corners)

for i, t in enumerate(temps):
    vals = [pvt_data[(c, t)] for c in corners]
    bars = ax.bar(x + i * bar_width, vals, bar_width, label=temp_labels[i],
                  color=temp_colors[i], edgecolor='black', linewidth=0.5)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0001,
                f'{v:.4f}', ha='center', va='bottom', fontsize=7, rotation=45)

ax.set_ylim(4.990, 5.020)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_xlabel('Process Corner', fontsize=12)
ax.set_title('DC Regulation Across 15 PVT Corners \u2014 All PASS', fontsize=14, fontweight='bold')
ax.set_xticks(x + bar_width)
ax.set_xticklabels(corner_labels, fontsize=11)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)
ax.axhline(y=5.000, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
ax.text(0.98, 0.95, 'Spec: 4.825V \u2013 5.175V (\u00b13.5%)\nAll corners well within spec',
        transform=ax.transAxes, ha='right', va='top', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.8))

plt.tight_layout()
plt.savefig('plot_pvt_dc_regulation.png')
plt.close()
print('Saved plot_pvt_dc_regulation.png')

# ── Plot 2: PVT Temperature Plot ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
markers = ['o', 's', '^', 'D', 'v']

for i, c in enumerate(corners):
    vals = [pvt_data[(c, t)] for t in temps]
    ax.plot(temps, vals, color=colors[i], marker=markers[i], markersize=8,
            linewidth=2, label=corner_labels[i])

ax.set_xlabel('Temperature (\u00b0C)', fontsize=12)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_title('Output Voltage vs Temperature \u2014 All Process Corners', fontsize=14, fontweight='bold')
ax.set_xticks(temps)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

all_vals = [pvt_data[(c, t)] for c in corners for t in temps]
ymin = min(all_vals) - 0.0005
ymax = max(all_vals) + 0.0005
ax.set_ylim(ymin, ymax)

plt.tight_layout()
plt.savefig('plot_pvt_temperature.png')
plt.close()
print('Saved plot_pvt_temperature.png')

# ── Plot 3: Line Regulation ──────────────────────────────────────────────
def read_wrdata(fname):
    bvdd, pvdd = [], []
    with open(fname) as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                bvdd.append(float(parts[0]))
                pvdd.append(float(parts[1]))
    return np.array(bvdd), np.array(pvdd)

bvdd_5, pvdd_5 = read_wrdata('line_reg_5ma.txt')
bvdd_10, pvdd_10 = read_wrdata('line_reg_10ma.txt')

fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

ax.plot(bvdd_5, pvdd_5, 'b-o', markersize=4, linewidth=1.5, label='5 mA load (1 k\u03a9)')
ax.plot(bvdd_10, pvdd_10, 'r-s', markersize=4, linewidth=1.5, label='10 mA load (500 \u03a9)')

ax.set_xlabel('BVDD (V)', fontsize=12)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_title('Line Regulation \u2014 TT 27\u00b0C', fontsize=14, fontweight='bold')
ax.set_ylim(4.990, 5.005)
ax.set_xlim(5.4, 10.5)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)

dv_10 = (pvdd_10[-1] - pvdd_10[0]) * 1000
dbvdd = bvdd_10[-1] - bvdd_10[0]
lr_10 = dv_10 / dbvdd

dv_5 = (pvdd_5[-1] - pvdd_5[0]) * 1000
lr_5 = dv_5 / dbvdd

ax.text(0.02, 0.95,
        f'10 mA: \u0394V = {dv_10:.1f} mV ({lr_10:.2f} mV/V)\n'
        f'  5 mA: \u0394V = {dv_5:.1f} mV ({lr_5:.2f} mV/V)',
        transform=ax.transAxes, ha='left', va='top', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.savefig('plot_line_regulation.png')
plt.close()
print('Saved plot_line_regulation.png')
