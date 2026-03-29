#!/usr/bin/env python3
"""Draw Block 03 Compensation Network schematic — matplotlib export."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(1, 1, figsize=(18, 12))
ax.set_xlim(-1, 17)
ax.set_ylim(-1, 13)
ax.set_aspect('equal')
ax.axis('off')

# Colors
C_CAP   = '#2e7d32'   # green for caps
C_RES   = '#e65100'   # orange for resistors
C_WIRE  = '#333333'
C_LABEL = '#000000'
C_NET   = '#0066cc'
C_SUPPLY= '#cc6600'
C_SECTION='#888888'
C_TITLE = '#1a237e'

# ================================================================
# TITLE
# ================================================================
ax.text(8, 12.5, 'BLOCK 03: COMPENSATION NETWORK', ha='center', va='center',
        fontsize=18, fontweight='bold', color=C_TITLE)
ax.text(8, 12.0, 'PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Miller + Output Decoupling',
        ha='center', va='center', fontsize=10, color='#555')
ax.text(8, 11.65, '.subckt compensation  vout_gate  pvdd  gnd',
        ha='center', va='center', fontsize=9, family='monospace', color='#888')

# ================================================================
# SECTION LABELS
# ================================================================
ax.text(5, 10.8, 'MILLER COMPENSATION (pole-splitting + LHP zero)',
        ha='center', va='center', fontsize=12, fontweight='bold', color=C_SECTION)
ax.text(13, 10.8, 'OUTPUT DECOUPLING',
        ha='center', va='center', fontsize=12, fontweight='bold', color=C_SECTION)

# ================================================================
# HELPERS
# ================================================================
def draw_cap(ax, x, y, name, value, area, orient='h'):
    """Draw a capacitor symbol (two parallel plates)."""
    if orient == 'h':  # horizontal: signal flows left→right
        # Plates
        ax.plot([x-0.15, x-0.15], [y-0.4, y+0.4], color=C_CAP, linewidth=3)
        ax.plot([x+0.15, x+0.15], [y-0.4, y+0.4], color=C_CAP, linewidth=3)
        # Leads
        ax.plot([x-0.8, x-0.15], [y, y], color=C_WIRE, linewidth=1.5)
        ax.plot([x+0.15, x+0.8], [y, y], color=C_WIRE, linewidth=1.5)
    else:  # vertical: signal flows top→bottom
        ax.plot([x-0.4, x+0.4], [y+0.15, y+0.15], color=C_CAP, linewidth=3)
        ax.plot([x-0.4, x+0.4], [y-0.15, y-0.15], color=C_CAP, linewidth=3)
        ax.plot([x, x], [y+0.15, y+0.8], color=C_WIRE, linewidth=1.5)
        ax.plot([x, x], [y-0.15, y-0.8], color=C_WIRE, linewidth=1.5)
    # Labels
    ax.text(x, y+0.7 if orient=='h' else y+1.1, name, ha='center', va='center',
            fontsize=10, fontweight='bold', color=C_CAP)
    ax.text(x, y+0.45 if orient=='h' else y+0.95, value, ha='center', va='center',
            fontsize=9, color=C_CAP)
    if area:
        ax.text(x, y-0.65 if orient=='h' else y-1.1, area, ha='center', va='center',
                fontsize=7, color='#666')

def draw_res(ax, x, y, name, value, orient='h'):
    """Draw a resistor symbol (zigzag)."""
    if orient == 'h':
        # Zigzag
        pts_x = [x-0.7, x-0.5, x-0.3, x-0.1, x+0.1, x+0.3, x+0.5, x+0.7]
        pts_y = [y, y+0.2, y-0.2, y+0.2, y-0.2, y+0.2, y-0.2, y]
        ax.plot(pts_x, pts_y, color=C_RES, linewidth=2)
        # Leads
        ax.plot([x-1.2, x-0.7], [y, y], color=C_WIRE, linewidth=1.5)
        ax.plot([x+0.7, x+1.2], [y, y], color=C_WIRE, linewidth=1.5)
    else:
        pts_y = [y-0.7, y-0.5, y-0.3, y-0.1, y+0.1, y+0.3, y+0.5, y+0.7]
        pts_x = [x, x+0.2, x-0.2, x+0.2, x-0.2, x+0.2, x-0.2, x]
        ax.plot(pts_x, pts_y, color=C_RES, linewidth=2)
        ax.plot([x, x], [y-0.7, y-1.2], color=C_WIRE, linewidth=1.5)
        ax.plot([x, x], [y+0.7, y+1.2], color=C_WIRE, linewidth=1.5)
    ax.text(x, y+0.5 if orient=='h' else y+1.3, name, ha='center', va='center',
            fontsize=10, fontweight='bold', color=C_RES)
    ax.text(x, y+0.3 if orient=='h' else y+1.1, value, ha='center', va='center',
            fontsize=9, color=C_RES)

def gnd_sym(ax, x, y):
    """Draw ground symbol."""
    ax.plot([x-0.3, x+0.3], [y, y], color=C_WIRE, linewidth=2)
    ax.plot([x-0.2, x+0.2], [y-0.12, y-0.12], color=C_WIRE, linewidth=1.5)
    ax.plot([x-0.1, x+0.1], [y-0.24, y-0.24], color=C_WIRE, linewidth=1)

def vdd_sym(ax, x, y, label='PVDD'):
    """Draw supply symbol."""
    ax.plot([x-0.3, x+0.3], [y, y], color=C_SUPPLY, linewidth=2.5)
    ax.text(x, y+0.25, label, ha='center', va='center', fontsize=9,
            fontweight='bold', color=C_SUPPLY)

# ================================================================
# MILLER PATH: vout_gate → XCc → cc_mid → XRz → pvdd
# Main signal path at y=8
# ================================================================

y_main = 8.0

# vout_gate input
ax.annotate('', xy=(1.5, y_main), xytext=(0.3, y_main),
            arrowprops=dict(arrowstyle='->', color=C_WIRE, lw=2))
ax.text(0, y_main+0.3, 'vout_gate', ha='center', va='center',
        fontsize=11, fontweight='bold', color=C_NET,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='#e3f2fd', edgecolor=C_NET))
ax.text(0, y_main-0.35, '(error amp out)', ha='center', va='center',
        fontsize=7, color='#888')

# Wire from input to XCc
ax.plot([1.5, 2.8], [y_main, y_main], color=C_WIRE, linewidth=1.5)

# XCc: Miller cap
draw_cap(ax, 3.6, y_main, 'XCc', '~30 pF', '14,884 um²', orient='h')
ax.text(3.6, y_main-0.9, 'sky130_fd_pr__cap_mim_m3_1', ha='center', va='center',
        fontsize=6.5, family='monospace', color='#888')
ax.text(3.6, y_main-1.1, 'W=122  L=122', ha='center', va='center',
        fontsize=7, family='monospace', color='#555')

# Wire XCc→XRz
ax.plot([4.4, 5.3], [y_main, y_main], color=C_WIRE, linewidth=1.5)

# Net label: cc_mid
ax.plot(5.3, y_main, 'o', color=C_NET, markersize=4)
ax.text(5.3, y_main+0.3, 'cc_mid', ha='center', va='center',
        fontsize=8, color=C_NET)

# XRz: nulling resistor
draw_res(ax, 6.5, y_main, 'XRz', '~5 kΩ', orient='h')
ax.text(6.5, y_main-0.5, 'sky130_fd_pr__res_xhigh_po', ha='center', va='center',
        fontsize=6.5, family='monospace', color='#888')
ax.text(6.5, y_main-0.7, 'W=4  L=10', ha='center', va='center',
        fontsize=7, family='monospace', color='#555')
ax.text(6.5, y_main-0.95, 'LHP zero at ~1.06 MHz', ha='center', va='center',
        fontsize=7, style='italic', color=C_RES)

# Rz body to gnd
ax.plot([6.5, 6.5], [y_main-0.3, y_main-1.4], color=C_WIRE, linewidth=1, linestyle='--')
ax.text(6.5, y_main-1.55, 'sub=gnd', ha='center', va='center', fontsize=6, color='#aaa')

# Wire XRz→pvdd
ax.plot([7.7, 9.5], [y_main, y_main], color=C_WIRE, linewidth=1.5)

# Junction dot where Cout connects
ax.plot(9.5, y_main, 'o', color=C_WIRE, markersize=5, zorder=5)

# pvdd label
ax.text(10.5, y_main+0.3, 'pvdd', ha='center', va='center',
        fontsize=11, fontweight='bold', color=C_SUPPLY,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='#fff3e0', edgecolor=C_SUPPLY))
ax.text(10.5, y_main-0.35, '(5.0V regulated)', ha='center', va='center',
        fontsize=7, color='#888')
ax.plot([9.5, 10.0], [y_main, y_main], color=C_WIRE, linewidth=1.5)

# ================================================================
# OUTPUT DECOUPLING: XCout from pvdd to gnd (vertical)
# ================================================================

x_cout = 13.0
y_cout = 6.0

# Wire from pvdd junction down to Cout
ax.plot([9.5, x_cout], [y_main, y_main], color=C_WIRE, linewidth=1.5)
ax.plot([x_cout, x_cout], [y_main, y_cout+0.8], color=C_WIRE, linewidth=1.5)

# Cout cap (vertical)
draw_cap(ax, x_cout, y_cout, 'XCout', '~70 pF', '34,969 um²', orient='v')
ax.text(x_cout, y_cout-1.4, 'sky130_fd_pr__cap_mim_m3_1', ha='center', va='center',
        fontsize=6.5, family='monospace', color='#888')
ax.text(x_cout, y_cout-1.6, 'W=187  L=187', ha='center', va='center',
        fontsize=7, family='monospace', color='#555')

# GND at bottom
ax.plot([x_cout, x_cout], [y_cout-0.8, y_cout-1.8], color=C_WIRE, linewidth=1.5)
gnd_sym(ax, x_cout, y_cout-1.8)

# pvdd marker at top
vdd_sym(ax, x_cout, y_main+0.15, 'PVDD')

# ================================================================
# AREA BUDGET TABLE
# ================================================================
table_y = 3.0
ax.text(3, table_y+1.2, 'AREA BUDGET', ha='center', fontsize=11, fontweight='bold', color=C_TITLE)

table_data = [
    ('XCc  (Miller)',  '30 pF',  '14,884 um²', C_CAP),
    ('XRz  (Nulling)', '5 kΩ',   '48 um²',     C_RES),
    ('XCout (Decoup)', '70 pF',  '34,969 um²', C_CAP),
    ('TOTAL',          '',       '49,901 um²', C_TITLE),
]
for i, (name, val, area, color) in enumerate(table_data):
    yy = table_y + 0.6 - i*0.45
    weight = 'bold' if name == 'TOTAL' else 'normal'
    ax.text(1.0, yy, name, ha='left', fontsize=9, fontweight=weight, color=color)
    ax.text(3.5, yy, val, ha='center', fontsize=9, color=color)
    ax.text(5.5, yy, area, ha='right', fontsize=9, fontweight=weight, color=color)
if table_data:
    ax.plot([0.8, 5.7], [table_y+0.8, table_y+0.8], color='#ccc', linewidth=0.5)
    ax.plot([0.8, 5.7], [table_y-0.6+0.45, table_y-0.6+0.45], color='#ccc', linewidth=0.5)
    ax.text(5.8, table_y+0.6-3*0.45, '(< 50,000 limit)', fontsize=7, color='#888')

# ================================================================
# SPEC TABLE
# ================================================================
spec_y = 3.0
spec_x = 9.0
ax.text(12.5, spec_y+1.2, 'KEY RESULTS  (TT 27°C)', ha='center', fontsize=11,
        fontweight='bold', color=C_TITLE)

specs = [
    ('PM (worst)',  '45.8°',  '≥ 45°',  'PASS'),
    ('Undershoot',  '116 mV', '≤ 150',  'PASS'),
    ('Overshoot',   '150 mV', '≤ 150',  'PASS'),
    ('Settling',    '1.0 µs', '≤ 10',   'PASS'),
    ('GM (worst)',  '>100 dB','≥ 10',   'PASS'),
]
for i, (param, val, spec, status) in enumerate(specs):
    yy = spec_y + 0.6 - i*0.4
    ax.text(spec_x, yy, param, ha='left', fontsize=8.5)
    ax.text(spec_x+3, yy, val, ha='center', fontsize=8.5, fontweight='bold')
    ax.text(spec_x+4.5, yy, spec, ha='center', fontsize=7.5, color='#888')
    color_s = '#2e7d32' if status == 'PASS' else '#c62828'
    ax.text(spec_x+5.8, yy, status, ha='center', fontsize=8.5, fontweight='bold', color=color_s)

ax.text(12.5, spec_y-1.3, '12/12 specs PASS', ha='center', fontsize=14,
        fontweight='bold', color='#2e7d32',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', edgecolor='#2e7d32', linewidth=2))

# ================================================================
# SIGNAL FLOW ANNOTATION
# ================================================================
ax.annotate('', xy=(9.0, y_main+1.5), xytext=(1.5, y_main+1.5),
            arrowprops=dict(arrowstyle='->', color='#aaa', lw=1.5, linestyle='--'))
ax.text(5.3, y_main+1.8, 'Miller feedback path: gate → output (pole splitting)',
        ha='center', va='center', fontsize=8, style='italic', color='#888')

plt.tight_layout()
plt.savefig('compensation_export.png', dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved compensation_export.png")
