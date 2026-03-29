#!/usr/bin/env python3
"""Draw a block-level schematic of the current limiter circuit."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(1, 1, figsize=(18, 11))
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

# ---- Section labels ----
ax.text(3, 13.8, 'SENSE MIRROR', ha='center', fontsize=10, fontweight='bold', color=C_SECTION,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0f0f0', edgecolor=C_SECTION))
ax.text(8.5, 13.8, 'DETECTION', ha='center', fontsize=10, fontweight='bold', color=C_SECTION,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0f0f0', edgecolor=C_SECTION))
ax.text(13.5, 13.8, 'CLAMP', ha='center', fontsize=10, fontweight='bold', color=C_SECTION,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0f0f0', edgecolor=C_SECTION))
ax.text(18, 13.8, 'FLAG OUTPUT', ha='center', fontsize=10, fontweight='bold', color=C_SECTION,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0f0f0', edgecolor=C_SECTION))

# ---- Supply rails ----
wire(ax, [(-0.5, 13), (20.5, 13)], color=C_SUPPLY, lw=2)
wire(ax, [(-0.5, 0.5), (20.5, 0.5)], color=C_SUPPLY, lw=2)
ax.text(-0.8, 13, 'bvdd', ha='right', va='center', fontsize=9, fontweight='bold', color=C_SUPPLY)
ax.text(-0.8, 0.5, 'gnd', ha='right', va='center', fontsize=9, fontweight='bold', color=C_SUPPLY)

# ======================================================================
# SENSE MIRROR: XMs (PMOS at top) + XRs (resistor at bottom)
# ======================================================================

# XMs: Sense PMOS (W=2u L=0.5u, source=bvdd, gate=gate, drain=sense_n)
mos_box(ax, 3, 10.5, 'XMs', 'PMOS HV', 2, 0.5, 1, C_PMOS)
wire(ax, [(3, 10.9), (3, 13)])           # source to bvdd
port_label(ax, 0, 10.5, 'gate', 'in')     # gate input port
wire(ax, [(0.1, 10.5), (2.4, 10.5)])     # gate wire
net_label(ax, 3, 9.8, 'sense_n')
wire(ax, [(3, 10.1), (3, 7)])             # drain to sense_n node

# XRs: Sense resistor (W=1 L=3.12, ~6.2k)
passive_box(ax, 3, 5.5, 'XRs', '~6.2k', C_PASSIVE)
wire(ax, [(3, 5.8), (3, 7)])              # top to sense_n
dot(ax, 3, 7)
wire(ax, [(3, 5.2), (3, 0.5)])            # bottom to gnd

# ======================================================================
# DETECTION: XRpu (pull-up at top) + XMdet (NMOS at bottom)
# ======================================================================

# XRpu: Pull-up resistor (W=1 L=5, ~10.5k)
passive_box(ax, 8.5, 11, 'XRpu', '~10.5k', C_PASSIVE)
wire(ax, [(8.5, 11.3), (8.5, 13)])       # top to bvdd
net_label(ax, 8.5, 9.8, 'det_n')
wire(ax, [(8.5, 10.7), (8.5, 7)])         # bottom to det_n node
dot(ax, 8.5, 7)

# XMdet: Detection NMOS (W=5u L=1u, gate=sense_n, drain=det_n)
mos_box(ax, 8.5, 4.5, 'XMdet', 'NMOS HV', 5, 1, 1, C_NMOS)
wire(ax, [(8.5, 4.9), (8.5, 7)])          # drain to det_n
wire(ax, [(8.5, 4.1), (8.5, 0.5)])        # source to gnd

# Gate of XMdet connected to sense_n
wire(ax, [(7.9, 4.5), (6, 4.5), (6, 7), (3, 7)])  # route sense_n to gate
dot(ax, 6, 7)
net_label(ax, 4.5, 7.2, 'sense_n')

# ======================================================================
# CLAMP: XMclamp (PMOS, gate=det_n, source=bvdd, drain=gate)
# Feedback: drain connects back to gate port
# ======================================================================

# XMclamp: Clamp PMOS (W=20u L=1u)
mos_box(ax, 13.5, 10.5, 'XMclamp', 'PMOS HV', 20, 1, 1, C_PMOS)
wire(ax, [(13.5, 10.9), (13.5, 13)])      # source to bvdd

# Gate of XMclamp connected to det_n
wire(ax, [(12.9, 10.5), (11, 10.5), (11, 7), (8.5, 7)])
dot(ax, 8.5, 7)
net_label(ax, 9.8, 7.2, 'det_n')

# Drain of XMclamp → gate port (FEEDBACK)
wire(ax, [(13.5, 10.1), (13.5, 8.5)])
net_label(ax, 13.8, 9.0, 'gate', ha='left')
# Feedback path drawn as a bold wire going left back to gate
wire(ax, [(13.5, 8.5), (13.5, 8), (0.5, 8), (0.5, 10.5), (0.1, 10.5)],
     color='#8B0000', lw=1.8)
dot(ax, 0.1, 10.5, color='#8B0000')
dot(ax, 13.5, 8.5)

# Feedback annotation
ax.text(7, 8.25, 'FEEDBACK: XMclamp drain -> gate', ha='center', va='bottom',
        fontsize=6.5, fontstyle='italic', color='#8B0000',
        bbox=dict(boxstyle='round,pad=0.15', facecolor='#fff0f0', edgecolor='#8B0000', alpha=0.7))

# ======================================================================
# FLAG OUTPUT: XMfp (PMOS) + XMfn (NMOS) — inverter
# Input = det_n, Output = ilim_flag
# ======================================================================

# XMfp: Flag PMOS (W=2u L=1u, source=pvdd)
mos_box(ax, 18, 10.5, 'XMfp', 'PMOS HV', 2, 1, 1, C_PMOS)
wire(ax, [(18, 10.9), (18, 12)])
# pvdd label (not bvdd — this one connects to pvdd)
ax.text(18, 12.3, 'pvdd', ha='center', va='bottom', fontsize=7, fontweight='bold', color='#cc00cc')
wire(ax, [(18, 12), (18, 12.5)], color='#cc00cc', lw=1.5)
dot(ax, 18, 12.5, color='#cc00cc')
# pvdd supply stub (separate from bvdd rail)
ax.plot(17.5, 12.5, 's', color='#cc00cc', markersize=5)
wire(ax, [(17.5, 12.5), (18.5, 12.5)], color='#cc00cc', lw=1.5)

# Gate of XMfp connected to det_n
wire(ax, [(17.4, 10.5), (16, 10.5), (16, 7), (11, 7)])
dot(ax, 11, 7)

# XMfn: Flag NMOS (W=2u L=1u, source=gnd)
mos_box(ax, 18, 4.5, 'XMfn', 'NMOS HV', 2, 1, 1, C_NMOS)
wire(ax, [(18, 4.1), (18, 0.5)])          # source to gnd

# Gate of XMfn connected to det_n
wire(ax, [(17.4, 4.5), (16, 4.5), (16, 7)])
dot(ax, 16, 7)
net_label(ax, 15, 7.2, 'det_n')

# Connect drains of XMfp and XMfn → ilim_flag
net_label(ax, 18, 9.3, 'ilim_flag')
wire(ax, [(18, 10.1), (18, 7.5)])
wire(ax, [(18, 4.9), (18, 7.5)])
dot(ax, 18, 7.5)

# Output port
wire(ax, [(18, 7.5), (20, 7.5)])
port_label(ax, 20.5, 7.5, 'ilim_flag', 'out')

# ---- Additional port labels ----
# bvdd supply port
port_label(ax, -0.2, 13, 'bvdd', 'supply')
# gnd supply port
port_label(ax, -0.2, 0.5, 'gnd', 'supply')
# pvdd supply port (at flag section)
ax.text(19.2, 12.5, '(supply)', ha='left', va='center', fontsize=5.5, color='#cc00cc')

# ---- Title block ----
title_rect = FancyBboxPatch((12.5, -0.5), 8.2, 2.0,
                             boxstyle="round,pad=0.1",
                             facecolor='#f8f8f0', edgecolor='#333333', linewidth=1.5)
ax.add_patch(title_rect)
ax.text(16.6, 1.2, 'Block 04: Current Limiter', ha='center', va='center',
        fontsize=12, fontweight='bold')
ax.text(16.6, 0.7, 'PVDD 5V LDO  --  SkyWater SKY130A', ha='center', va='center',
        fontsize=9)
ax.text(16.6, 0.3, 'Sense-Mirror Brick-Wall Limiter', ha='center', va='center',
        fontsize=8, color='#666666')
ax.text(16.6, -0.1, '2026-03-29', ha='center', va='center',
        fontsize=8, color='#666666')

# ---- Characterization box ----
char_rect = FancyBboxPatch((-0.8, -0.5), 12, 2.0,
                            boxstyle="round,pad=0.1",
                            facecolor='#f0f8f0', edgecolor='#228B22', linewidth=1.2)
ax.add_patch(char_rect)
ax.text(5.2, 1.2, 'CHARACTERIZATION (v3)', ha='center', va='center',
        fontsize=9, fontweight='bold', color='#228B22')

char_lines = [
    'Ilim TT 27C = 79.9 mA [60-80]    Ilim SS 150C = 136.8 mA [>=50]    Ilim FF -40C = 43.4 mA [<=100]',
    'Response = 0.1 us [<=10]    PVDD impact = 0.1 mV [<=10]    Iq = 0.0002 uA [<=10]    Loop PM = 104.5 deg [>=45]',
]
ax.text(5.2, 0.65, char_lines[0], ha='center', va='center', fontsize=6, color='#333333', family='monospace')
ax.text(5.2, 0.2, char_lines[1], ha='center', va='center', fontsize=6, color='#333333', family='monospace')
ax.text(5.2, -0.2, '9/9 PASS    Primary: ilim_ss150 = 136.8 mA', ha='center', va='center',
        fontsize=8, fontweight='bold', color='#228B22')

plt.tight_layout()
plt.savefig('/home/ubuntu/analog-ai-chips/pvdd_regulator/04_current_limiter/current_limiter_export.png',
            dpi=150, bbox_inches='tight', facecolor='white')
print("Saved current_limiter_export.png")
