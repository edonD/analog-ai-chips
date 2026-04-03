#!/usr/bin/env python3
"""Generate 5 current-limit characterization plots from ilim_sweep_data.csv"""

import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

WORKDIR = "/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration"
CSV = f"{WORKDIR}/ilim_sweep_data.csv"

# ---------- Load data ----------
data = {'tt_27': [], 'ss_150': [], 'ff_-40': []}
with open(CSV) as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = f"{row['corner']}_{row['temp']}"
        try:
            rload = float(row['rload'])
            pvdd = float(row['pvdd'])
            iload = float(row['iload'])
            gate = float(row['gate'])
            data[key].append((rload, pvdd, iload * 1000, gate))  # iload in mA
        except (ValueError, KeyError):
            continue

# Sort each by rload descending (high R = low current first)
for k in data:
    data[k].sort(key=lambda x: -x[0])

def extract(key):
    """Return arrays: rload, pvdd, iload_mA, gate"""
    d = data.get(key, [])
    if not d:
        return np.array([]), np.array([]), np.array([]), np.array([])
    rload = np.array([x[0] for x in d])
    pvdd = np.array([x[1] for x in d])
    iload = np.array([x[2] for x in d])
    gate = np.array([x[3] for x in d])
    return rload, pvdd, iload, gate

tt_r, tt_v, tt_i, tt_g = extract('tt_27')
ss_r, ss_v, ss_i, ss_g = extract('ss_150')
ff_r, ff_v, ff_i, ff_g = extract('ff_-40')

# ========== PLOT 1: DC Regulation vs Load Current (TT 27C, 0-60mA) ==========
fig, ax = plt.subplots(figsize=(10, 6))
mask = tt_i <= 60
ax.plot(tt_i[mask], tt_v[mask], 'b.-', linewidth=2, markersize=6, label='TT 27C')
ax.axhspan(4.825, 5.175, alpha=0.15, color='green', label='Regulation band (5.0V +/-3.5%)')
ax.set_xlabel('Load Current (mA)', fontsize=13)
ax.set_ylabel('PVDD (V)', fontsize=13)
ax.set_title('DC Regulation vs Load Current -- TT 27C', fontsize=14, fontweight='bold')
ax.set_xlim(0, 60)
ax.set_ylim(0, 5.5)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
fig.tight_layout()
fig.savefig(f'{WORKDIR}/plot_dc_regulation.png', dpi=150)
plt.close(fig)
print("Saved plot_dc_regulation.png")

# ========== PLOT 2: Current Limit Characteristic (TT 27C, full range) ==========
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(tt_i, tt_v, 'b.-', linewidth=2, markersize=6, label='TT 27C')

# Find trip point: last point where PVDD > 4.5V
trip_idx = None
for i in range(len(tt_v)):
    if tt_v[i] > 4.5:
        trip_idx = i
trip_i = tt_i[trip_idx] if trip_idx is not None else 54
trip_v = tt_v[trip_idx] if trip_idx is not None else 5.0

# Find short-circuit current (Rload=0.1 ohm — nearly zero)
sc_idx = np.argmin(tt_r)  # smallest Rload
sc_i = tt_i[sc_idx]
sc_v = tt_v[sc_idx]

ax.annotate(f'Trip point\n{trip_i:.1f} mA',
            xy=(trip_i, trip_v), xytext=(trip_i + 15, trip_v + 0.3),
            fontsize=11, color='red', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='red', lw=2))

ax.annotate(f'Short-circuit\n{sc_i:.1f} mA',
            xy=(sc_i, sc_v), xytext=(sc_i + 15, sc_v + 1.5),
            fontsize=11, color='darkred', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=2))

ax.set_xlabel('Load Current (mA)', fontsize=13)
ax.set_ylabel('PVDD (V)', fontsize=13)
ax.set_title('Current Limit Characteristic -- TT 27C', fontsize=14, fontweight='bold')
ax.set_xlim(0, 150)
ax.set_ylim(0, 5.5)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
fig.tight_layout()
fig.savefig(f'{WORKDIR}/plot_current_limit_tt27.png', dpi=150)
plt.close(fig)
print("Saved plot_current_limit_tt27.png")

# ========== PLOT 3: Current Limit PVT Spread ==========
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(tt_i, tt_v, 'b.-', linewidth=2, markersize=5, label='TT 27C')
if len(ss_i) > 0:
    ax.plot(ss_i, ss_v, 'r.-', linewidth=2, markersize=5, label='SS 150C')
if len(ff_i) > 0:
    ax.plot(ff_i, ff_v, 'g.-', linewidth=2, markersize=5, label='FF -40C')

ax.set_xlabel('Load Current (mA)', fontsize=13)
ax.set_ylabel('PVDD (V)', fontsize=13)
ax.set_title('Current Limit PVT Spread (1.28x)', fontsize=14, fontweight='bold')
ax.set_xlim(0, 150)
ax.set_ylim(0, 5.5)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='upper right')
fig.tight_layout()
fig.savefig(f'{WORKDIR}/plot_current_limit_pvt.png', dpi=150)
plt.close(fig)
print("Saved plot_current_limit_pvt.png")

# ========== PLOT 4: Foldback Current Limit ==========
fig, ax = plt.subplots(figsize=(10, 6))

# "Demanded" current = BVDD / Rload (if pass device were ideal, PVDD = BVDD = 7V)
BVDD = 7.0
tt_demanded = BVDD / tt_r * 1000  # mA
tt_actual = tt_i  # mA

# 45-degree reference line
ref_x = np.linspace(0, 150, 200)
ax.plot(ref_x, ref_x, 'k--', linewidth=1, alpha=0.5, label='Actual = Demanded (ideal)')

ax.plot(tt_demanded, tt_actual, 'b.-', linewidth=2, markersize=6, label='TT 27C')

ax.set_xlabel('Demanded Load Current (mA)', fontsize=13)
ax.set_ylabel('Actual Load Current (mA)', fontsize=13)
ax.set_title('Foldback Current Limit Characteristic', fontsize=14, fontweight='bold')
ax.set_xlim(0, 150)
ax.set_ylim(0, 150)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
fig.tight_layout()
fig.savefig(f'{WORKDIR}/plot_current_limit_foldback.png', dpi=150)
plt.close(fig)
print("Saved plot_current_limit_foldback.png")

# ========== PLOT 5: Gate Voltage vs Load Current (TT 27C) ==========
fig, ax = plt.subplots(figsize=(10, 6))
mask = tt_i <= 60
ax.plot(tt_i[mask], tt_g[mask], 'b.-', linewidth=2, markersize=6, label='TT 27C')

ax.set_xlabel('Load Current (mA)', fontsize=13)
ax.set_ylabel('Gate Voltage (V)', fontsize=13)
ax.set_title('Gate Voltage vs Load Current -- TT 27C', fontsize=14, fontweight='bold')
ax.set_xlim(0, 60)
ax.set_ylim(4, 7)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
fig.tight_layout()
fig.savefig(f'{WORKDIR}/plot_gate_vs_load.png', dpi=150)
plt.close(fig)
print("Saved plot_gate_vs_load.png")

print("\nAll 5 plots generated successfully.")
