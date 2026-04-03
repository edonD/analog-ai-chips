#!/usr/bin/env python3
"""Generate all 5 verification plots after FIX-19/FIX-20."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import re, os, csv

os.chdir('/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration')

results = []  # For verification_pvt.txt

# ============================================================
# PLOT 1: Current Limit Characteristic (3 corners)
# ============================================================
print("=== Plot 1: Current Limit ===")
csv_data = {}
with open('ilim_sweep_data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row['corner'], row['temp'])
        if key not in csv_data:
            csv_data[key] = {'iload': [], 'pvdd': []}
        try:
            iload_a = float(row['iload'])
            pvdd = float(row['pvdd'])
            csv_data[key]['iload'].append(iload_a * 1000)  # mA
            csv_data[key]['pvdd'].append(pvdd)
        except (ValueError, KeyError):
            pass

fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
corner_styles = {
    ('tt', '27'): ('b-o', 'TT 27C'),
    ('ss', '150'): ('r-s', 'SS 150C'),
    ('ff', '-40'): ('g-^', 'FF -40C'),
}

for key, style_info in corner_styles.items():
    if key in csv_data:
        d = csv_data[key]
        # Sort by iload
        pairs = sorted(zip(d['iload'], d['pvdd']))
        iload = [p[0] for p in pairs]
        pvdd = [p[1] for p in pairs]
        ax.plot(iload, pvdd, style_info[0], markersize=5, linewidth=1.5, label=style_info[1])

        # Find regulation limit
        for i, v in enumerate(pvdd):
            if v < 4.9 and iload[i] > 5:
                results.append(f"  {style_info[1]}: regulation lost at ~{iload[i]:.0f} mA (PVDD={v:.3f}V)")
                break

ax.axhline(y=5.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5, label='PVDD=5.0V target')
ax.axhline(y=4.825, color='red', linestyle=':', linewidth=0.8, alpha=0.4, label='Spec min (4.825V)')
ax.set_xlabel('Load Current (mA)', fontsize=12)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_title('Current Limit Characteristic — Post FIX-19/FIX-20', fontsize=14, fontweight='bold')
ax.set_xlim(-5, 120)
ax.set_ylim(-0.5, 5.5)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plot_current_limit.png')
plt.close()
print("Saved plot_current_limit.png")

# ============================================================
# PLOT 2: PVT DC Regulation Bar Chart
# ============================================================
print("=== Plot 2: PVT DC Regulation ===")
corners = ['tt', 'ss', 'ff', 'sf', 'fs']
temps = [-40, 27, 150]
pvt_data = {}

for c in corners:
    for t in temps:
        fname = f'pvt_v2_results/a_{c}_{t}.log'
        try:
            with open(fname) as f:
                for line in f:
                    m = re.search(r'pvdd_final\s+=\s+([\d.eE+-]+)', line)
                    if m:
                        pvt_data[(c, t)] = float(m.group(1))
        except FileNotFoundError:
            print(f"  WARNING: {fname} not found")

corner_labels = ['TT', 'SS', 'FF', 'SF', 'FS']
temp_labels = ['-40C', '27C', '150C']

fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
temp_colors = ['#2196F3', '#4CAF50', '#FF9800']
n_corners = len(corners)
bar_width = 0.22
x = np.arange(n_corners)

all_pvdd = []
for i, t in enumerate(temps):
    vals = [pvt_data.get((c, t), 0) for c in corners]
    all_pvdd.extend([v for v in vals if v > 0])
    bars = ax.bar(x + i * bar_width, vals, bar_width, label=temp_labels[i],
                  color=temp_colors[i], edgecolor='black', linewidth=0.5)
    for bar, v in zip(bars, vals):
        if v > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0001,
                    f'{v:.4f}', ha='center', va='bottom', fontsize=7, rotation=45)

if all_pvdd:
    ymin = min(all_pvdd) - 0.005
    ymax = max(all_pvdd) + 0.005
    ax.set_ylim(ymin, ymax)

    pvdd_min = min(all_pvdd)
    pvdd_max = max(all_pvdd)
    pvdd_spread = (pvdd_max - pvdd_min) * 1000
    all_pass = all(4.825 <= v <= 5.175 for v in all_pvdd)
    status = "All PASS" if all_pass else "SOME FAIL"
    results.append(f"\nPVT DC Regulation:")
    results.append(f"  PVDD range: {pvdd_min:.4f}V to {pvdd_max:.4f}V (spread: {pvdd_spread:.1f} mV)")
    results.append(f"  Status: {status}")
    for c in corners:
        for t in temps:
            v = pvt_data.get((c, t), 0)
            if v > 0:
                pf = "PASS" if 4.825 <= v <= 5.175 else "FAIL"
                results.append(f"  {c.upper()} {t:>4d}C: {v:.4f}V [{pf}]")

ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_xlabel('Process Corner', fontsize=12)
ax.set_title(f'DC Regulation Across 15 PVT Corners — {status}', fontsize=14, fontweight='bold')
ax.set_xticks(x + bar_width)
ax.set_xticklabels(corner_labels, fontsize=11)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)
ax.axhline(y=5.000, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
ax.text(0.98, 0.95, f'Spec: 4.825V - 5.175V\nSpread: {pvdd_spread:.1f} mV',
        transform=ax.transAxes, ha='right', va='top', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3',
                  facecolor='lightgreen' if all_pass else 'lightyellow', alpha=0.8))
plt.tight_layout()
plt.savefig('plot_pvt_dc_regulation.png')
plt.close()
print("Saved plot_pvt_dc_regulation.png")

# ============================================================
# PLOT 3: PVT Temperature
# ============================================================
print("=== Plot 3: PVT Temperature ===")
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
markers = ['o', 's', '^', 'D', 'v']

for i, c in enumerate(corners):
    vals = [pvt_data.get((c, t), np.nan) for t in temps]
    if not any(np.isnan(v) for v in vals):
        ax.plot(temps, vals, color=colors[i], marker=markers[i], markersize=8,
                linewidth=2, label=corner_labels[i])
        tc = (vals[-1] - vals[0]) / (temps[-1] - temps[0]) * 1e6  # uV/C
        results.append(f"  {corner_labels[i]} TC: {tc:.1f} uV/C")

ax.set_xlabel('Temperature (C)', fontsize=12)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_title('Output Voltage vs Temperature — All Process Corners', fontsize=14, fontweight='bold')
ax.set_xticks(temps)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

if all_pvdd:
    ax.set_ylim(min(all_pvdd) - 0.001, max(all_pvdd) + 0.001)

plt.tight_layout()
plt.savefig('plot_pvt_temperature.png')
plt.close()
print("Saved plot_pvt_temperature.png")

# ============================================================
# PLOT 4: Line Regulation
# ============================================================
print("=== Plot 4: Line Regulation ===")

def read_wrdata(fname):
    """Read ngspice wrdata output. Format: index val1 index val2 ..."""
    cols = []
    with open(fname) as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 4:
                try:
                    cols.append([float(p) for p in parts])
                except ValueError:
                    pass
    if not cols:
        return np.array([]), np.array([])
    data = np.array(cols)
    # wrdata format: time1, v(bvdd), time2, v(pvdd)
    return data[:, 1], data[:, 3]

fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

for label, color, marker in [('5ma', 'b', 'o'), ('10ma', 'r', 's')]:
    fname = f'line_reg_{label}.txt'
    if os.path.exists(fname):
        bvdd, pvdd = read_wrdata(fname)
        if len(bvdd) > 0:
            # Filter to line sweep region (BVDD > 5.3V, after settling)
            # The sweep is 30m-80m, so filter time-based via BVDD values
            mask = (bvdd >= 5.3) & (bvdd <= 10.6) & (pvdd > 4.0)
            bvdd_f = bvdd[mask]
            pvdd_f = pvdd[mask]
            if len(bvdd_f) > 10:
                load_ma = {'5ma': 5, '10ma': 10}[label]
                ax.plot(bvdd_f, pvdd_f, f'{color}-{marker}', markersize=3,
                        linewidth=1.5, label=f'{load_ma} mA load', markevery=max(1, len(bvdd_f)//20))
                dv = (pvdd_f[-1] - pvdd_f[0]) * 1000
                dbvdd = bvdd_f[-1] - bvdd_f[0]
                lr = dv / dbvdd if dbvdd > 0 else 0
                results.append(f"\nLine Regulation ({load_ma}mA): dV={dv:.1f}mV, {lr:.2f} mV/V")

ax.set_xlabel('BVDD (V)', fontsize=12)
ax.set_ylabel('PVDD (V)', fontsize=12)
ax.set_title('Line Regulation — TT 27C', fontsize=14, fontweight='bold')
ax.set_xlim(5.4, 10.5)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('plot_line_regulation.png')
plt.close()
print("Saved plot_line_regulation.png")

# ============================================================
# PLOT 5: UV/OV Thresholds
# ============================================================
print("=== Plot 5: UV/OV ===")

if os.path.exists('uvov_data.txt'):
    data = np.loadtxt('uvov_data.txt')
    # wrdata with 3 vectors: time1 v(pvdd) time2 v(uv_flag) time3 v(ov_flag)
    if data.ndim == 2 and data.shape[1] >= 6:
        pvdd = data[:, 1]
        uv_flag = data[:, 3]
        ov_flag = data[:, 5]

        fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
        ax.plot(pvdd, uv_flag, 'b-', linewidth=1.5, label='UV Flag')
        ax.plot(pvdd, ov_flag, 'r-', linewidth=1.5, label='OV Flag')

        # Find UV trip (uv_flag falls through 1.1V)
        uv_cross = None
        for i in range(1, len(pvdd)):
            if uv_flag[i-1] > 1.1 and uv_flag[i] <= 1.1:
                frac = (1.1 - uv_flag[i]) / (uv_flag[i-1] - uv_flag[i]) if uv_flag[i-1] != uv_flag[i] else 0
                uv_cross = pvdd[i] + frac * (pvdd[i-1] - pvdd[i])
                break

        # Find OV trip (ov_flag rises through 1.1V)
        ov_cross = None
        for i in range(1, len(pvdd)):
            if ov_flag[i-1] < 1.1 and ov_flag[i] >= 1.1:
                frac = (1.1 - ov_flag[i-1]) / (ov_flag[i] - ov_flag[i-1]) if ov_flag[i] != ov_flag[i-1] else 0
                ov_cross = pvdd[i-1] + frac * (pvdd[i] - pvdd[i-1])
                break

        if uv_cross is not None:
            ax.axvline(x=uv_cross, color='b', linestyle=':', linewidth=1, alpha=0.5)
            ax.annotate(f'UV trip\n{uv_cross:.2f} V',
                        xy=(uv_cross, 1.1), xytext=(uv_cross - 1.2, 1.5),
                        fontsize=10, arrowprops=dict(arrowstyle='->', color='blue'),
                        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            uv_pass = "PASS" if 4.0 <= uv_cross <= 4.6 else "FAIL"
            results.append(f"\nUV trip: {uv_cross:.3f}V (spec 4.0-4.6V) [{uv_pass}]")

        if ov_cross is not None:
            ax.axvline(x=ov_cross, color='r', linestyle=':', linewidth=1, alpha=0.5)
            ax.annotate(f'OV trip\n{ov_cross:.2f} V',
                        xy=(ov_cross, 1.1), xytext=(ov_cross + 0.3, 1.5),
                        fontsize=10, arrowprops=dict(arrowstyle='->', color='red'),
                        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
            ov_pass = "PASS" if 5.3 <= ov_cross <= 5.7 else "FAIL"
            results.append(f"OV trip: {ov_cross:.3f}V (spec 5.3-5.7V) [{ov_pass}]")

        ax.axvline(x=5.0, color='green', linestyle='--', linewidth=1, alpha=0.4, label='PVDD=5.0V')
        ax.legend(fontsize=9, loc='center right')
        ax.set_xlabel('PVDD (V)', fontsize=12)
        ax.set_ylabel('Flag Voltage (V)', fontsize=12)
        ax.set_title('UV/OV Comparator Thresholds vs PVDD', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 7)
        ax.set_ylim(-0.1, 2.4)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('plot_uvov.png')
        plt.close()
        print("Saved plot_uvov.png")

# ============================================================
# Write verification_pvt.txt
# ============================================================
print("\n=== Writing verification_pvt.txt ===")
with open('verification_pvt.txt', 'w') as f:
    f.write("PVDD LDO Regulator — Post FIX-19/FIX-20 Verification Results\n")
    f.write("=" * 60 + "\n\n")
    f.write("Current Limit:\n")
    for r in results:
        f.write(r + "\n")
    f.write("\nPlots generated:\n")
    for p in ['plot_current_limit.png', 'plot_pvt_dc_regulation.png',
              'plot_pvt_temperature.png', 'plot_line_regulation.png', 'plot_uvov.png']:
        exists = os.path.exists(p)
        f.write(f"  {p}: {'OK' if exists else 'MISSING'}\n")

print("Saved verification_pvt.txt")
print("\nDone!")
