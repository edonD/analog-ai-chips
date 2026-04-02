#!/usr/bin/env python3
"""Generate load transient plots from ngspice wrdata output."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def load_wrdata(fname):
    """Load ngspice wrdata file (time, value columns)."""
    data = np.loadtxt(fname)
    t = data[:, 0]
    v = data[:, 1]
    return t, v

# Load all data
t_tt, v_tt = load_wrdata('lt_tt27_data.txt')
t_ss, v_ss = load_wrdata('lt_ss27_data.txt')
t_fs, v_fs = load_wrdata('lt_fs150_data.txt')
t_tm, v_tm = load_wrdata('lt_ttm40_data.txt')

# Convert to ms
t_tt_ms = t_tt * 1e3
t_ss_ms = t_ss * 1e3
t_fs_ms = t_fs * 1e3
t_tm_ms = t_tm * 1e3

# ============================================================
# Plot 1: Single TT 27C trace
# ============================================================
fig1, ax1 = plt.subplots(figsize=(10, 6))

# Zoom window
x1, x2 = 9.5, 13.0
y1, y2 = 4.8, 5.1

mask_tt = (t_tt_ms >= x1) & (t_tt_ms <= x2)
ax1.plot(t_tt_ms[mask_tt], v_tt[mask_tt], 'b-', linewidth=2, label='TT 27°C')

# Spec limits
ax1.axhline(4.825, color='gray', linewidth=0.8, linestyle='--', label='Spec limits (±3.5%)')
ax1.axhline(5.175, color='gray', linewidth=0.8, linestyle='--')

# Find undershoot (min around 10ms step-up) and overshoot (max around 12ms step-down)
mask_step_up = (t_tt_ms >= 9.99) & (t_tt_ms <= 10.5)
mask_step_dn = (t_tt_ms >= 11.99) & (t_tt_ms <= 12.5)

# Get steady-state before step (around 9.9-10ms)
mask_ss1 = (t_tt_ms >= 9.5) & (t_tt_ms <= 9.99)
v_ss_before = np.mean(v_tt[mask_ss1])

# Get steady-state during high load (around 11.5-12ms)
mask_ss2 = (t_tt_ms >= 11.5) & (t_tt_ms <= 11.99)
v_ss_during = np.mean(v_tt[mask_ss2])

# Undershoot at step-up (load increases, voltage drops)
v_min = np.min(v_tt[mask_step_up])
t_min = t_tt_ms[mask_step_up][np.argmin(v_tt[mask_step_up])]
undershoot_mv = (v_ss_before - v_min) * 1000

# Overshoot at step-down (load decreases, voltage rises)
v_max = np.max(v_tt[mask_step_dn])
t_max = t_tt_ms[mask_step_dn][np.argmax(v_tt[mask_step_dn])]
overshoot_mv = (v_max - v_ss_during) * 1000

# Annotate undershoot
ax1.annotate(f'Undershoot: {undershoot_mv:.0f} mV',
             xy=(t_min, v_min), xytext=(t_min + 0.5, v_min - 0.03),
             arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
             fontsize=11, color='red', fontweight='bold')

# Annotate overshoot
ax1.annotate(f'Overshoot: {overshoot_mv:.0f} mV',
             xy=(t_max, v_max), xytext=(t_max + 0.3, v_max + 0.02),
             arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
             fontsize=11, color='red', fontweight='bold')

ax1.set_xlim(x1, x2)
ax1.set_ylim(y1, y2)
ax1.set_xlabel('Time (ms)', fontsize=12)
ax1.set_ylabel('PVDD (V)', fontsize=12)
ax1.set_title('Load Transient Response (1→10→1 mA) — TT 27°C', fontsize=14)
ax1.legend(fontsize=11, loc='lower right')
ax1.grid(True, alpha=0.3)
fig1.tight_layout()
fig1.savefig('plot_load_transient.png', dpi=150)
print(f"Plot 1 saved: plot_load_transient.png")
print(f"  Undershoot: {undershoot_mv:.1f} mV at t={t_min:.3f} ms")
print(f"  Overshoot:  {overshoot_mv:.1f} mV at t={t_max:.3f} ms")

# ============================================================
# Plot 2: PVT overlay
# ============================================================
fig2, ax2 = plt.subplots(figsize=(10, 6))

x1, x2 = 9.5, 13.0
y1, y2 = 4.7, 5.2

corners = [
    (t_tt_ms, v_tt, 'TT 27°C', 'blue'),
    (t_ss_ms, v_ss, 'SS 27°C', 'red'),
    (t_fs_ms, v_fs, 'FS 150°C', 'orange'),
    (t_tm_ms, v_tm, 'TT -40°C', 'green'),
]

# Find worst undershoot across all corners
worst_undershoot = 0
worst_corner = ''
worst_t = 0
worst_v = 0

for t_ms, v, label, color in corners:
    mask = (t_ms >= x1) & (t_ms <= x2)
    ax2.plot(t_ms[mask], v[mask], color=color, linewidth=1.5, label=label)

    # Find undershoot for this corner
    mask_su = (t_ms >= 9.99) & (t_ms <= 10.5)
    mask_pre = (t_ms >= 9.5) & (t_ms <= 9.99)
    if np.sum(mask_su) > 0 and np.sum(mask_pre) > 0:
        v_pre = np.mean(v[mask_pre])
        v_min_c = np.min(v[mask_su])
        t_min_c = t_ms[mask_su][np.argmin(v[mask_su])]
        us = (v_pre - v_min_c) * 1000
        if us > worst_undershoot:
            worst_undershoot = us
            worst_corner = label
            worst_t = t_min_c
            worst_v = v_min_c

# Spec limits
ax2.axhline(4.825, color='gray', linewidth=0.8, linestyle='--', label='Spec limits (±3.5%)')
ax2.axhline(5.175, color='gray', linewidth=0.8, linestyle='--')

# Annotate worst undershoot
ax2.annotate(f'Worst undershoot: {worst_undershoot:.0f} mV ({worst_corner})',
             xy=(worst_t, worst_v), xytext=(worst_t + 0.5, worst_v - 0.05),
             arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5),
             fontsize=10, color='darkred', fontweight='bold')

ax2.set_xlim(x1, x2)
ax2.set_ylim(y1, y2)
ax2.set_xlabel('Time (ms)', fontsize=12)
ax2.set_ylabel('PVDD (V)', fontsize=12)
ax2.set_title('Load Transient — Worst PVT Corners', fontsize=14)
ax2.legend(fontsize=10, loc='lower right')
ax2.grid(True, alpha=0.3)
fig2.tight_layout()
fig2.savefig('plot_pvt_load_transient.png', dpi=150)
print(f"\nPlot 2 saved: plot_pvt_load_transient.png")
print(f"  Worst undershoot: {worst_undershoot:.1f} mV ({worst_corner})")
