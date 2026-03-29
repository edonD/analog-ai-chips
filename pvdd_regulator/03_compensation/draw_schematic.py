#!/usr/bin/env python3
"""Draw Block 03 Compensation Network schematic — xschem dark theme."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(1, 1, figsize=(20, 13))
fig.patch.set_facecolor('#0a0a1a')
ax.set_facecolor('#0a0a1a')
ax.set_xlim(-1, 19)
ax.set_ylim(-1, 14)
ax.set_aspect('equal')
ax.axis('off')

# xschem-style colors (dark background)
C_BG     = '#0a0a1a'
C_WIRE   = '#00e0e0'   # cyan wires
C_TEXT   = '#c8c800'   # yellow text
C_LABEL  = '#00ff00'   # green net labels
C_PIN    = '#ff4444'   # red pin labels
C_DEVICE = '#00c8c8'   # device outlines
C_PARAM  = '#44ff44'   # green param text
C_DIM    = '#888800'   # dim yellow annotations
C_TITLE  = '#00e0e0'   # cyan title
C_SECTION= '#c8c800'   # yellow section headers
C_SPEC   = '#44cc44'   # green spec text
C_PASS   = '#00ff00'   # bright green PASS
C_SUPPLY = '#ff8800'   # orange supply labels
C_GRAY   = '#666688'   # dim annotations

# ================================================================
# TITLE BLOCK
# ================================================================
ax.text(0, 13.3, 'BLOCK 03: COMPENSATION NETWORK', fontsize=20, fontweight='bold',
        color=C_TITLE, family='monospace')
ax.text(0, 12.75, 'PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Miller + Output Decoupling',
        fontsize=10, color=C_DIM)
ax.text(0, 12.35, 'All PDK: sky130_fd_pr__cap_mim_m3_1, sky130_fd_pr__res_xhigh_po   (Vds max 10.5V)',
        fontsize=8, color=C_GRAY)
ax.text(0, 12.0, '.subckt compensation  vout_gate  pvdd  gnd',
        fontsize=9, family='monospace', color='#aa44aa')

# --- Pin list ---
ax.text(0, 11.3, 'vout_gate', fontsize=9, color=C_PIN, family='monospace')
ax.plot([-0.3, 0], [11.3, 11.3], color=C_PIN, linewidth=1.5)
ax.plot(-0.3, 11.3, '<', color=C_PIN, markersize=5)

ax.text(2.5, 11.3, 'pvdd', fontsize=9, color=C_SUPPLY, family='monospace')
ax.plot([2.2, 2.5], [11.3, 11.3], color=C_SUPPLY, linewidth=1.5)
ax.text(2.25, 11.3, '<>', fontsize=7, color=C_SUPPLY, ha='center')

ax.text(4.2, 11.3, 'gnd', fontsize=9, color=C_SUPPLY, family='monospace')
ax.plot([3.9, 4.2], [11.3, 11.3], color=C_SUPPLY, linewidth=1.5)
ax.text(3.95, 11.3, '<>', fontsize=7, color=C_SUPPLY, ha='center')

# ================================================================
# SECTION LABELS
# ================================================================
ax.text(4.5, 10.3, 'MILLER COMPENSATION', fontsize=14, fontweight='bold',
        color=C_SECTION, family='monospace')
ax.text(14, 10.3, 'OUTPUT DECOUPLING', fontsize=14, fontweight='bold',
        color=C_SECTION, family='monospace')

# ================================================================
# COMPENSATION CIRCUIT
# ================================================================

y_main = 8.0

# --- vout_gate input ---
ax.text(0.2, y_main + 0.4, 'vout_gate', fontsize=11, fontweight='bold',
        color=C_LABEL, family='monospace')
ax.plot([1.5, 3.0], [y_main, y_main], color=C_WIRE, linewidth=2)

# --- XCc: MIM cap symbol (two parallel plates) ---
cx = 4.0
# Plates
ax.plot([cx - 0.12, cx - 0.12], [y_main - 0.5, y_main + 0.5], color=C_DEVICE, linewidth=3)
ax.plot([cx + 0.12, cx + 0.12], [y_main - 0.5, y_main + 0.5], color=C_DEVICE, linewidth=3)
# Leads
ax.plot([3.0, cx - 0.12], [y_main, y_main], color=C_WIRE, linewidth=2)
ax.plot([cx + 0.12, 5.5], [y_main, y_main], color=C_WIRE, linewidth=2)
# Labels
ax.text(cx, y_main + 0.85, 'XCc', fontsize=10, ha='center', color=C_TEXT, family='monospace')
ax.text(cx + 0.5, y_main + 0.6, 'cap_mim_m3_1', fontsize=7, color=C_GRAY, family='monospace')
ax.text(cx, y_main - 0.8, 'W=122  L=122', fontsize=8, ha='center', color=C_PARAM, family='monospace')
ax.text(cx, y_main - 1.1, '~30 pF', fontsize=9, ha='center', fontweight='bold', color=C_SPEC)
ax.text(cx, y_main - 1.4, '14,884 um²', fontsize=7, ha='center', color=C_GRAY)

# --- cc_mid net label ---
ax.plot(5.5, y_main, 'o', color=C_LABEL, markersize=5, zorder=5)
ax.text(5.5, y_main + 0.35, 'cc_mid', fontsize=9, ha='center', color=C_LABEL, family='monospace')

# Wire to XRz
ax.plot([5.5, 7.0], [y_main, y_main], color=C_WIRE, linewidth=2)

# --- XRz: Resistor symbol (zigzag) ---
rx = 8.2
pts_x = [7.0, 7.3, 7.6, 7.9, 8.2, 8.5, 8.8, 9.1, 9.4]
pts_y = [y_main, y_main+0.3, y_main-0.3, y_main+0.3, y_main-0.3,
         y_main+0.3, y_main-0.3, y_main+0.3, y_main]
ax.plot(pts_x, pts_y, color=C_DEVICE, linewidth=2)
# Leads
ax.plot([9.4, 11.0], [y_main, y_main], color=C_WIRE, linewidth=2)
# Body tap (substrate connection)
ax.plot([rx, rx], [y_main - 0.3, y_main - 1.2], color=C_WIRE, linewidth=1, linestyle='--')
ax.text(rx, y_main - 1.45, 'sub=gnd', fontsize=7, ha='center', color=C_GRAY)
# Labels
ax.text(rx, y_main + 0.75, 'XRz', fontsize=10, ha='center', color=C_TEXT, family='monospace')
ax.text(rx + 0.8, y_main + 0.5, 'res_xhigh_po', fontsize=7, color=C_GRAY, family='monospace')
ax.text(rx, y_main - 0.65, 'W=4  L=10', fontsize=8, ha='center', color=C_PARAM, family='monospace')
ax.text(rx, y_main - 0.9, '~5 kΩ', fontsize=9, ha='center', fontweight='bold', color=C_SPEC)
ax.text(rx, y_main + 1.1, 'LHP zero', fontsize=8, ha='center', color=C_DIM, style='italic')

# --- Junction at pvdd ---
ax.plot(11.0, y_main, 'o', color=C_WIRE, markersize=5, zorder=5)

# Wire continues right to pvdd label
ax.plot([11.0, 12.5], [y_main, y_main], color=C_WIRE, linewidth=2)
ax.text(12.8, y_main, 'pvdd', fontsize=11, fontweight='bold',
        color=C_SUPPLY, family='monospace')

# ================================================================
# OUTPUT DECOUPLING: XCout from pvdd to gnd (vertical)
# ================================================================

x_cout = 15.5

# Wire from junction to Cout
ax.plot([11.0, x_cout], [y_main, y_main], color=C_WIRE, linewidth=2)
ax.plot([x_cout, x_cout], [y_main, y_main - 1.0], color=C_WIRE, linewidth=2)

# Cap plates (vertical orientation)
cy = y_main - 1.8
ax.plot([x_cout - 0.5, x_cout + 0.5], [cy + 0.12, cy + 0.12], color=C_DEVICE, linewidth=3)
ax.plot([x_cout - 0.5, x_cout + 0.5], [cy - 0.12, cy - 0.12], color=C_DEVICE, linewidth=3)
# Leads
ax.plot([x_cout, x_cout], [y_main - 1.0, cy + 0.12], color=C_WIRE, linewidth=2)
ax.plot([x_cout, x_cout], [cy - 0.12, cy - 1.0], color=C_WIRE, linewidth=2)

# GND symbol
gy = cy - 1.2
ax.plot([x_cout - 0.35, x_cout + 0.35], [gy, gy], color=C_WIRE, linewidth=2.5)
ax.plot([x_cout - 0.22, x_cout + 0.22], [gy - 0.15, gy - 0.15], color=C_WIRE, linewidth=2)
ax.plot([x_cout - 0.10, x_cout + 0.10], [gy - 0.30, gy - 0.30], color=C_WIRE, linewidth=1.5)

# Labels
ax.text(x_cout + 0.9, cy + 0.5, 'XCout', fontsize=10, color=C_TEXT, family='monospace')
ax.text(x_cout + 0.9, cy + 0.15, 'cap_mim_m3_1', fontsize=7, color=C_GRAY, family='monospace')
ax.text(x_cout + 0.9, cy - 0.2, 'W=187  L=187', fontsize=8, color=C_PARAM, family='monospace')
ax.text(x_cout + 0.9, cy - 0.55, '~70 pF', fontsize=9, fontweight='bold', color=C_SPEC)
ax.text(x_cout + 0.9, cy - 0.85, '34,969 um²', fontsize=7, color=C_GRAY)

# PVDD supply symbol at top
ax.plot([x_cout - 0.3, x_cout + 0.3], [y_main + 0.15, y_main + 0.15],
        color=C_SUPPLY, linewidth=2.5)
ax.text(x_cout, y_main + 0.5, 'PVDD', fontsize=9, ha='center',
        fontweight='bold', color=C_SUPPLY, family='monospace')

# ================================================================
# CHARACTERIZATION BOX
# ================================================================
ax.text(0, 3.5, 'CHARACTERIZATION  (TT 27C, BVDD = 7.0V, real Block 02 feedback)',
        fontsize=12, fontweight='bold', color=C_SECTION, family='monospace')

specs = [
    ('PM at 0 mA',      '45.8 deg',   'spec >= 45 deg',   'PASS'),
    ('PM at 100 uA',    '84.4 deg',   'spec >= 45 deg',   'PASS'),
    ('PM at 1 mA',      '80.7 deg',   'spec >= 45 deg',   'PASS'),
    ('PM at 10 mA',     '58.4 deg',   'spec >= 45 deg',   'PASS'),
    ('PM at 50 mA',     '46.6 deg',   'spec >= 45 deg',   'PASS'),
    ('GM all loads',     '> 100 dB',   'spec >= 10 dB',    'PASS'),
    ('Undershoot 1->10', '116 mV',    'spec <= 150 mV',   'PASS'),
    ('Overshoot 10->1',  '150 mV',    'spec <= 150 mV',   'PASS'),
    ('Settling time',    '1.0 us',    'spec <= 10 us',    'PASS'),
    ('Comp area',        '49,901 um²','spec <= 50,000',   'PASS'),
]

for i, (param, val, spec, status) in enumerate(specs):
    yy = 2.9 - i * 0.28
    ax.text(0.2, yy, param, fontsize=8, color=C_SPEC, family='monospace')
    ax.text(5.5, yy, f'=  {val}', fontsize=8, color=C_SPEC, family='monospace')
    ax.text(9.5, yy, spec, fontsize=7.5, color=C_DIM, family='monospace')
    ax.text(13.5, yy, status, fontsize=8, fontweight='bold',
            color=C_PASS, family='monospace')

ax.text(0, -0.1, 'All 12/12 specs PASS', fontsize=14, fontweight='bold',
        color=C_PASS, family='monospace')

# ================================================================
# XSCHEM-STYLE TITLE BAR (bottom)
# ================================================================
ax.plot([-0.8, 18.8], [-0.6, -0.6], color=C_WIRE, linewidth=1)
ax.text(0, -0.85, 'Block 03: Compensation -- Analog AI Chips PVDD LDO Regulator',
        fontsize=8, color=C_DIM)
ax.text(17.5, -0.85, 'compensation.sch', fontsize=8, color=C_DIM, ha='right')

plt.savefig('compensation_export.png', dpi=200, bbox_inches='tight',
            facecolor=C_BG, edgecolor='none')
print("Saved compensation_export.png")
