#!/usr/bin/env python3
"""Plot EA bias points from ngspice .meas output."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import re

# Parse ea_bias_data.txt for measured values
nodes = {}
with open('ea_bias_data.txt', 'r') as f:
    for line in f:
        # Match lines like: v_d1 = 4.12345e+00
        m = re.match(r'(\w+)\s*=\s*([0-9eE.+\-]+)', line.strip())
        if m:
            nodes[m.group(1)] = float(m.group(2))

# Expected node names from tb_plot_ea_bias.spice
labels = ['v_d1', 'v_d2', 'v_vout', 'v_pb', 'v_vref', 'v_vfb', 'v_gate', 'v_pvdd', 'v_ibias']
nice_labels = ['D1\n(diff+)', 'D2\n(diff-)', 'EA_OUT', 'PB_TAIL', 'VREF_SS', 'VFB', 'GATE', 'PVDD', 'IBIAS']

vals = []
colors = []
for lbl in labels:
    v = nodes.get(lbl, 0.0)
    vals.append(v)
    if lbl in ('v_vout', 'v_gate'):
        colors.append('red')
    elif lbl == 'v_pvdd':
        colors.append('blue')
    elif lbl in ('v_vref', 'v_vfb'):
        colors.append('green')
    else:
        colors.append('steelblue')

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(range(len(vals)), vals, color=colors, edgecolor='black', linewidth=0.5)

# Annotate each bar with its value
for i, (bar, v) in enumerate(zip(bars, vals)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f'{v:.4f}V', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_xticks(range(len(nice_labels)))
ax.set_xticklabels(nice_labels, fontsize=9)
ax.set_ylabel('Voltage (V)', fontsize=11)
ax.set_title('Error Amplifier Bias Points @ 1mA Load — TT 27°C', fontsize=12, fontweight='bold')
ax.set_ylim(0, max(vals) * 1.15)
ax.grid(axis='y', alpha=0.3)

# Highlight EA_OUT vs GATE match
ea_out = nodes.get('v_vout', 0)
gate = nodes.get('v_gate', 0)
offset_mv = (ea_out - gate) * 1000
ax.text(0.98, 0.95, f'EA_OUT - GATE = {offset_mv:.1f} mV',
        transform=ax.transAxes, ha='right', va='top', fontsize=11,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))

plt.tight_layout()
plt.savefig('plot_ea_bias.png', dpi=150, bbox_inches='tight')
print(f'Saved plot_ea_bias.png')
print(f'EA_OUT = {ea_out:.6f} V, GATE = {gate:.6f} V, offset = {offset_mv:.1f} mV')
