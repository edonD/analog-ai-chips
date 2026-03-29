#!/usr/bin/env python3
"""Generate a professional schematic diagram for Block 08: Mode Control."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(1, 1, figsize=(22, 16))
ax.set_xlim(-1, 21)
ax.set_ylim(-1, 16)
ax.set_aspect('equal')
ax.axis('off')

# ── Title ──
ax.text(10, 15.5, 'BLOCK 08: MODE CONTROL', fontsize=20, fontweight='bold',
        ha='center', va='center', color='#1a1a8a')
ax.text(10, 15.0, 'PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Shared Ladder + PVDD Inverter Threshold Detectors',
        fontsize=9, ha='center', va='center', color='#555')
ax.text(10, 14.6, '.subckt mode_control  bvdd  pvdd  svdd  gnd  vref  en_ret  bypass_en  ea_en  ref_sel  uvov_en  ilim_en  pass_off',
        fontsize=7, ha='center', va='center', family='monospace', color='#800080')

# ── Port Pins ──
ax.text(0.2, 13.8, 'PORT PINS', fontsize=11, fontweight='bold', color='#1a1a8a')
inputs = ['bvdd', 'pvdd', 'svdd', 'gnd', 'vref', 'en_ret']
outputs = ['bypass_en', 'ea_en', 'ref_sel', 'uvov_en', 'ilim_en', 'pass_off']
for i, name in enumerate(inputs):
    y = 13.3 - i * 0.35
    ax.annotate('', xy=(1.0, y), xytext=(0.3, y),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
    ax.text(1.1, y, name, fontsize=8, va='center', family='monospace', color='green')
for i, name in enumerate(outputs):
    y = 13.3 - i * 0.35
    ax.annotate('', xy=(4.0, y), xytext=(3.3, y),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
    ax.text(4.1, y, name, fontsize=8, va='center', family='monospace', color='red')

# ── Resistor Ladder ──
lx = 1.5  # ladder x center
ly_top = 10.5
ly_bot = 4.5
ax.text(lx, 11.2, 'RESISTOR LADDER', fontsize=11, fontweight='bold', ha='center', color='#1a1a8a')
ax.text(lx, 10.85, '~400k total, Iq~17uA', fontsize=7, ha='center', color='#555')

# BVDD at top
ax.text(lx, ly_top + 0.3, 'BVDD', fontsize=9, ha='center', fontweight='bold', color='red')
ax.plot([lx, lx], [ly_top + 0.2, ly_top], 'k-', lw=2)

# Resistor segments and taps
res_data = [
    ('Rtop', 'l=8',   ly_top,   ly_top - 0.8, 'tap1'),
    ('R12',  'l=68',  ly_top - 1.1, ly_top - 2.4, 'tap2'),
    ('R23',  'l=8',   ly_top - 2.7, ly_top - 3.5, 'tap3'),
    ('R34',  'l=21',  ly_top - 3.8, ly_top - 4.6, 'tap4'),
    ('Rbot', 'l=86',  ly_top - 4.9, ly_bot, None),
]

tap_y = {}
for name, dims, yt, yb, tap_name in res_data:
    ymid = (yt + yb) / 2
    # Draw zigzag resistor
    ax.add_patch(FancyBboxPatch((lx - 0.2, yb), 0.4, yt - yb,
                                boxstyle="round,pad=0.05", ec='black', fc='#ffffcc', lw=1.5))
    ax.text(lx, ymid, name, fontsize=7, ha='center', va='center', fontweight='bold')
    ax.text(lx + 0.5, ymid, dims, fontsize=6, ha='left', va='center', color='#666')
    # Connect to previous
    if tap_name:
        tap_y[tap_name] = yb - 0.15
        ax.plot([lx, lx], [yb, yb - 0.3], 'k-', lw=2)
        # Tap dot
        ax.plot(lx, yb - 0.15, 'ko', markersize=5)
        ax.text(lx + 0.4, yb - 0.15, tap_name, fontsize=8, va='center',
                family='monospace', color='#0066cc')
        # Horizontal line to comparators
        ax.plot([lx, 3.5], [yb - 0.15, yb - 0.15], 'b--', lw=0.8, alpha=0.5)

# GND at bottom
ax.plot([lx, lx], [ly_bot, ly_bot - 0.3], 'k-', lw=2)
ax.text(lx, ly_bot - 0.5, 'GND', fontsize=9, ha='center', fontweight='bold')

# Tap capacitors
for tname in ['tap1', 'tap2', 'tap3', 'tap4']:
    ty = tap_y[tname]
    ax.text(lx - 0.8, ty, '100f', fontsize=5, ha='center', va='center', color='#888')

# ── Comparators ──
comp_x = 5.0
ax.text(comp_x + 1.5, 11.2, 'COMPARATORS (PVDD-referenced inverters)', fontsize=11,
        fontweight='bold', ha='center', color='#1a1a8a')
ax.text(comp_x + 1.5, 10.85, 'Each: INV1(tap->c_inv) + INV2(c_inv->comp)', fontsize=7,
        ha='center', color='#555')

comp_data = [
    ('COMP1', 'TH1=2.55V', 'tap1', 'comp1', 10.0),
    ('COMP2', 'TH2=4.34V', 'tap2', 'comp2', 8.5),
    ('COMP3', 'TH3=4.65V', 'tap3', 'comp3', 7.0),
    ('COMP4', 'TH4=5.67V', 'tap4', 'comp4', 5.5),
]

for cname, thresh, tap, out, cy in comp_data:
    # INV1 box
    inv1_x = comp_x
    ax.add_patch(FancyBboxPatch((inv1_x, cy - 0.4), 1.2, 0.8,
                                boxstyle="round,pad=0.05", ec='#333', fc='#e8f0fe', lw=1.5))
    ax.text(inv1_x + 0.6, cy, 'INV1', fontsize=8, ha='center', va='center', fontweight='bold')
    # INV2 box
    inv2_x = comp_x + 1.8
    ax.add_patch(FancyBboxPatch((inv2_x, cy - 0.4), 1.2, 0.8,
                                boxstyle="round,pad=0.05", ec='#333', fc='#e8f0fe', lw=1.5))
    ax.text(inv2_x + 0.6, cy, 'INV2', fontsize=8, ha='center', va='center', fontweight='bold')
    # Connections
    ax.annotate('', xy=(inv1_x, cy), xytext=(inv1_x - 0.8, cy),
                arrowprops=dict(arrowstyle='->', color='blue', lw=1.2))
    ax.text(inv1_x - 1.2, cy, tap, fontsize=7, ha='center', va='center',
            family='monospace', color='#0066cc')
    ax.plot([inv1_x + 1.2, inv2_x], [cy, cy], 'k-', lw=1.5)
    ax.annotate('', xy=(inv2_x + 1.8, cy), xytext=(inv2_x + 1.2, cy),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
    ax.text(inv2_x + 2.1, cy, out, fontsize=7, ha='left', va='center',
            family='monospace', color='#cc0000')
    # Labels
    ax.text(inv1_x + 0.6, cy + 0.55, f'{cname}  ({thresh})', fontsize=8,
            ha='center', va='center', fontweight='bold', color='#1a1a8a')
    # PFET/NFET sizing
    ax.text(inv1_x + 0.6, cy - 0.55, 'P:20/20 N:20/20', fontsize=5,
            ha='center', va='center', color='#666')
    ax.text(inv2_x + 0.6, cy - 0.55, 'P:40/20 N:20/20', fontsize=5,
            ha='center', va='center', color='#666')

# ── Logic Section ──
logic_x = 11.5
ax.text(logic_x + 2.5, 11.2, 'LOGIC: AOI GATES + OUTPUT BUFFERS', fontsize=11,
        fontweight='bold', ha='center', color='#1a1a8a')

logic_blocks = [
    ('pass_off',   'BUF(comp1b)',                    'BVDD < TH1: pass FET off',         10.0),
    ('bypass_en',  'INV(AOI22(c1*c2b, c3*c4b))',     'TH1..TH2 or TH3..TH4: bypass',    8.8),
    ('ea_en',      'INV(AOI21(c2*c3b, c4))',          'TH2..TH3 or >TH4: EA on',         7.6),
    ('ref_sel',    'INV(NOR2(comp1, comp3b))',        '>TH1 and <TH3: ref select',        6.4),
    ('uvov_en',    'BUF(comp4)',                      '>TH4: UV/OV monitor',               5.2),
    ('ilim_en',    'BUF(comp4)',                      '>TH4: current limiter',             4.0),
]

for oname, func, desc, ly in logic_blocks:
    bx = logic_x
    # Logic gate box
    ax.add_patch(FancyBboxPatch((bx, ly - 0.35), 3.5, 0.7,
                                boxstyle="round,pad=0.05", ec='#333', fc='#fff3e0', lw=1.5))
    ax.text(bx + 1.75, ly + 0.05, func, fontsize=7, ha='center', va='center',
            family='monospace', fontweight='bold')
    ax.text(bx + 1.75, ly - 0.2, desc, fontsize=6, ha='center', va='center', color='#666')
    # Output arrow
    ax.annotate('', xy=(bx + 4.5, ly), xytext=(bx + 3.5, ly),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
    ax.text(bx + 4.6, ly, oname, fontsize=9, ha='left', va='center',
            family='monospace', fontweight='bold', color='#cc0000')

# ── Characterization Box ──
char_y = 2.5
ax.add_patch(FancyBboxPatch((0.3, 0.2), 20, 2.5,
                            boxstyle="round,pad=0.1", ec='#1a1a8a', fc='#f0f0ff', lw=2))
ax.text(10, 2.45, 'CHARACTERIZATION  (TT 27C, PVDD = 5.0V, BVDD ramp 0-7V)',
        fontsize=12, ha='center', va='center', fontweight='bold', color='#1a1a8a')

char_lines = [
    'TH1 (pass_off)  = 2.51V     TH2 (bypass_en) = 4.16V     TH3 (ea_en) = 4.44V     TH4 (uvov/ilim) = 5.52V',
    'Hysteresis = 224-244 mV (Schmitt trigger)     |     Iq = 17.3 uA     |     thresh_max_error = 1.43% TT, 8.05% PVT',
    'PVT: 5 process corners (TT/SS/FF/SF/FS) verified     |     Monotonic + Glitch-free     |     specs_pass: 16/16',
]
for i, line in enumerate(char_lines):
    ax.text(10, 1.9 - i * 0.45, line, fontsize=8, ha='center', va='center',
            family='monospace', color='#333')

ax.text(10, 0.5, 'All 16/16 specs PASS', fontsize=14, ha='center', va='center',
        fontweight='bold', color='#006600')

# ── Border ──
ax.add_patch(patches.Rectangle((-0.5, -0.3), 21, 16.3, linewidth=2,
                                edgecolor='#1a1a8a', facecolor='none'))
ax.text(20, -0.1, 'Block 08: Mode Control -- Analog AI Chips PVDD LDO Regulator',
        fontsize=6, ha='right', va='center', color='#999')

plt.tight_layout()
plt.savefig('/home/ubuntu/analog-ai-chips/pvdd_regulator/08_mode_control/mode_control.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print("Saved mode_control.png")
