#!/usr/bin/env python3
"""Draw a block-level schematic of the two-stage Miller OTA error amplifier."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(1, 1, figsize=(20, 14))
ax.set_xlim(-1, 21)
ax.set_ylim(-1, 15)
ax.set_aspect('equal')
ax.axis('off')

# Colors
C_PMOS = '#4a90d9'
C_NMOS = '#d94a4a'
C_PASSIVE = '#6b8e23'
C_WIRE = '#333333'
C_LABEL = '#000000'
C_NET = '#0066cc'
C_SUPPLY = '#cc6600'
C_SECTION = '#888888'

def mos_box(ax, x, y, name, typ, w, l, m, color):
    """Draw a MOSFET as a labeled box."""
    rect = FancyBboxPatch((x-0.6, y-0.4), 1.2, 0.8,
                           boxstyle="round,pad=0.05",
                           facecolor=color, alpha=0.25, edgecolor=color, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x, y+0.1, name, ha='center', va='center', fontsize=7, fontweight='bold', color=C_LABEL)
    ax.text(x, y-0.15, f'{typ}', ha='center', va='center', fontsize=5.5, color=color)
    ax.text(x, y-0.55, f'W={w} L={l} m={m}', ha='center', va='center', fontsize=5, color=C_LABEL)

def passive_box(ax, x, y, name, val, color):
    rect = FancyBboxPatch((x-0.5, y-0.3), 1.0, 0.6,
                           boxstyle="round,pad=0.05",
                           facecolor=color, alpha=0.2, edgecolor=color, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x, y+0.05, name, ha='center', va='center', fontsize=7, fontweight='bold')
    ax.text(x, y-0.15, val, ha='center', va='center', fontsize=6, color=C_LABEL)

def wire(ax, points, color=C_WIRE, lw=1):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color=color, linewidth=lw, solid_capstyle='round')

def dot(ax, x, y, color=C_WIRE):
    ax.plot(x, y, 'o', color=color, markersize=3, zorder=5)

def net_label(ax, x, y, text, ha='center', va='bottom', fontsize=6):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fontsize, color=C_NET, fontstyle='italic')

def port_label(ax, x, y, text, direction='in'):
    color = '#006600' if direction == 'in' else '#660000' if direction == 'out' else C_SUPPLY
    marker = '>' if direction == 'in' else '<' if direction == 'out' else 's'
    ax.plot(x, y, marker, color=color, markersize=8, zorder=5)
    offset = 0.3 if direction == 'in' else -0.3
    ax.text(x - offset, y, text, ha='right' if direction == 'in' else 'left',
            va='center', fontsize=8, fontweight='bold', color=color)

# ── Section labels ──
ax.text(1.5, 13.8, 'ENABLE', ha='center', fontsize=10, fontweight='bold', color=C_SECTION,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0f0f0', edgecolor=C_SECTION))
ax.text(4.5, 13.8, 'BIAS', ha='center', fontsize=10, fontweight='bold', color=C_SECTION,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0f0f0', edgecolor=C_SECTION))
ax.text(10, 13.8, 'DIFF PAIR + MIRROR', ha='center', fontsize=10, fontweight='bold', color=C_SECTION,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0f0f0', edgecolor=C_SECTION))
ax.text(15, 13.8, 'MILLER COMP', ha='center', fontsize=10, fontweight='bold', color=C_SECTION,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0f0f0', edgecolor=C_SECTION))
ax.text(18, 13.8, 'STAGE 2', ha='center', fontsize=10, fontweight='bold', color=C_SECTION,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0f0f0', edgecolor=C_SECTION))

# ── Supply rails ──
wire(ax, [(-0.5, 13), (20, 13)], color=C_SUPPLY, lw=2)
wire(ax, [(-0.5, 0.5), (20, 0.5)], color=C_SUPPLY, lw=2)
ax.text(-0.8, 13, 'pvdd', ha='right', va='center', fontsize=9, fontweight='bold', color=C_SUPPLY)
ax.text(-0.8, 0.5, 'gnd', ha='right', va='center', fontsize=9, fontweight='bold', color=C_SUPPLY)

# ═══════════════════ ENABLE SECTION ═══════════════════

# XMen: en controls ibias pass-gate
mos_box(ax, 1.5, 2.5, 'XMen', 'NMOS HV', 20, 1, 1, C_NMOS)
port_label(ax, -0.2, 2.5, 'en', 'in')
wire(ax, [(-0.1, 2.5), (0.9, 2.5)])
net_label(ax, 1.5, 1.8, 'gnd')
wire(ax, [(1.5, 2.1), (1.5, 0.5)])
net_label(ax, 1.5, 3.2, 'ibias_en')
wire(ax, [(1.5, 2.9), (1.5, 3.5)])

# XMpu: pullup for enable
mos_box(ax, 1.5, 11.5, 'XMpu', 'PMOS HV', 20, 1, 1, C_PMOS)
wire(ax, [(1.5, 11.9), (1.5, 13)])
port_label(ax, -0.2, 11.5, 'en', 'in')
wire(ax, [(-0.1, 11.5), (0.9, 11.5)])
net_label(ax, 1.5, 10.8, 'vout_gate')
wire(ax, [(1.5, 11.1), (1.5, 10.5)])

# ═══════════════════ BIAS SECTION ═══════════════════

# XMbn0: diode-connected NMOS, ibias mirror
mos_box(ax, 4, 2.5, 'XMbn0', 'NMOS HV', 20, 8, 1, C_NMOS)
port_label(ax, 2.5, 3.5, 'ibias', 'in')
wire(ax, [(2.6, 3.5), (4, 3.5)])
wire(ax, [(4, 3.5), (4, 2.9)])
wire(ax, [(1.5, 3.5), (4, 3.5)])
dot(ax, 4, 3.5)
dot(ax, 1.5, 3.5)
net_label(ax, 3, 3.7, 'ibias_en')
# Diode connection
wire(ax, [(3.4, 2.5), (3.2, 2.5), (3.2, 3.5)])
dot(ax, 3.2, 3.5)
wire(ax, [(4, 2.1), (4, 0.5)])

# XMbn_pb: NMOS mirror for pb_tail (m=20)
mos_box(ax, 6, 2.5, 'XMbn_pb', 'NMOS HV', 20, 8, 20, C_NMOS)
wire(ax, [(5.4, 2.5), (4.6, 2.5)])
net_label(ax, 5, 2.2, 'ibias_en')
wire(ax, [(6, 2.1), (6, 0.5)])
net_label(ax, 6, 3.2, 'pb_tail')
wire(ax, [(6, 2.9), (6, 4)])

# XMbp0: PMOS diode for pb_tail bias (m=4)
mos_box(ax, 6, 5, 'XMbp0', 'PMOS HV', 20, 4, 4, C_PMOS)
wire(ax, [(6, 5.4), (6, 6)])
wire(ax, [(6, 6), (6, 13)])
wire(ax, [(6, 4.6), (6, 4)])
dot(ax, 6, 4)
# Diode connection
wire(ax, [(5.4, 5), (5.2, 5), (5.2, 4), (6, 4)])
dot(ax, 5.2, 4)
net_label(ax, 6.3, 4, 'pb_tail', ha='left')

# ═══════════════════ DIFF PAIR + MIRROR ═══════════════════

# XMtail: PMOS tail current source (m=4)
mos_box(ax, 10, 10, 'XMtail', 'PMOS HV', 20, 4, 4, C_PMOS)
wire(ax, [(10, 10.4), (10, 13)])
wire(ax, [(9.4, 10), (8, 10)])
wire(ax, [(8, 10), (8, 4), (6, 4)])
dot(ax, 6, 4)
net_label(ax, 8.2, 10.2, 'pb_tail')
net_label(ax, 10, 9.3, 'tail_s')
wire(ax, [(10, 9.6), (10, 9)])

# XM1: left diff pair PMOS (vref input)
mos_box(ax, 9, 7.5, 'XM1', 'PMOS HV', 50, 4, 2, C_PMOS)
wire(ax, [(9, 7.9), (9, 9), (10, 9)])
dot(ax, 10, 9)
port_label(ax, 7, 7.5, 'vref', 'in')
wire(ax, [(7.1, 7.5), (8.4, 7.5)])
net_label(ax, 9, 6.8, 'd1')
wire(ax, [(9, 7.1), (9, 6.5)])

# XM2: right diff pair PMOS (vfb input)
mos_box(ax, 11, 7.5, 'XM2', 'PMOS HV', 50, 4, 2, C_PMOS)
wire(ax, [(11, 7.9), (11, 9), (10, 9)])
port_label(ax, 13, 7.5, 'vfb', 'in')
wire(ax, [(12.9, 7.5), (11.6, 7.5)])
net_label(ax, 11, 6.8, 'd2')
wire(ax, [(11, 7.1), (11, 6.5)])

# XMn_l: NMOS mirror load left (diode)
mos_box(ax, 9, 4.5, 'XMn_l', 'NMOS HV', 20, 8, 2, C_NMOS)
wire(ax, [(9, 4.9), (9, 6.5)])
dot(ax, 9, 6.5)
wire(ax, [(9, 4.1), (9, 0.5)])
# Diode connection
wire(ax, [(8.4, 4.5), (8.2, 4.5), (8.2, 6.5), (9, 6.5)])
dot(ax, 8.2, 6.5)
net_label(ax, 8.5, 6.7, 'd1')

# XMn_r: NMOS mirror load right
mos_box(ax, 11, 4.5, 'XMn_r', 'NMOS HV', 20, 8, 2, C_NMOS)
wire(ax, [(11, 4.9), (11, 6.5)])
wire(ax, [(11, 4.1), (11, 0.5)])
# Gate connected to d1
wire(ax, [(10.4, 4.5), (8.2, 4.5)])
dot(ax, 8.2, 4.5)
net_label(ax, 11.3, 6.7, 'd2', ha='left')

# ═══════════════════ MILLER COMPENSATION ═══════════════════

# Cc: Miller cap
passive_box(ax, 14, 6.5, 'Cc', '1.3nF', C_PASSIVE)
wire(ax, [(11, 6.5), (13.5, 6.5)])
dot(ax, 11, 6.5)
net_label(ax, 12.5, 6.7, 'd2')

# Rc: Miller resistor
passive_box(ax, 16, 6.5, 'Rc', '11.38k', C_PASSIVE)
wire(ax, [(14.5, 6.5), (15.5, 6.5)])
net_label(ax, 15, 6.7, 'comp_mid')

# ═══════════════════ STAGE 2 ═══════════════════

# XMp_ld: PMOS active load (m=8)
mos_box(ax, 18, 10, 'XMp_ld', 'PMOS HV', 20, 4, 8, C_PMOS)
wire(ax, [(18, 10.4), (18, 13)])
wire(ax, [(17.4, 10), (16.5, 10)])
wire(ax, [(16.5, 10), (16.5, 4), (8, 4)])
dot(ax, 8, 4)
net_label(ax, 16.7, 10.2, 'pb_tail')
net_label(ax, 18, 9.3, 'vout_gate')
wire(ax, [(18, 9.6), (18, 8.5)])

# XMcs: NMOS common-source (stage 2 gain)
mos_box(ax, 18, 4.5, 'XMcs', 'NMOS HV', 20, 1, 1, C_NMOS)
wire(ax, [(18, 4.9), (18, 8.5)])
dot(ax, 18, 8.5)
wire(ax, [(18, 4.1), (18, 0.5)])
wire(ax, [(17.4, 4.5), (13, 4.5), (13, 6.5)])
dot(ax, 13, 6.5)
net_label(ax, 13, 4.2, 'd2')

# Output wire
wire(ax, [(16.5, 6.5), (18, 6.5)])
dot(ax, 18, 6.5)
wire(ax, [(18, 8.5), (20, 8.5)])
port_label(ax, 20.5, 8.5, 'vout_gate', 'out')
net_label(ax, 19, 8.7, 'vout_gate')

# Pullup output connection
wire(ax, [(1.5, 10.5), (1.5, 8.5), (3.5, 8.5)])
wire(ax, [(3.5, 8.5), (3.5, 8.5)])
net_label(ax, 2, 8.7, 'vout_gate')

# ── Title block ──
title_rect = FancyBboxPatch((13.5, -0.5), 7, 1.8,
                             boxstyle="round,pad=0.1",
                             facecolor='#f8f8f0', edgecolor='#333333', linewidth=1.5)
ax.add_patch(title_rect)
ax.text(17, 1.0, 'Block 00: Error Amplifier', ha='center', va='center',
        fontsize=12, fontweight='bold')
ax.text(17, 0.5, 'PVDD 5V LDO  --  SkyWater SKY130A', ha='center', va='center',
        fontsize=9)
ax.text(17, 0.1, '2026-03-28', ha='center', va='center',
        fontsize=8, color='#666666')

plt.tight_layout()
plt.savefig('/home/ubuntu/analog-ai-chips/pvdd_regulator/00_error_amp/error_amp.png',
            dpi=150, bbox_inches='tight', facecolor='white')
print("Saved error_amp.png")
