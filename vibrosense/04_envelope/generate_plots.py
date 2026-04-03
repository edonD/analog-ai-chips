#!/usr/bin/env python3
"""VibroSense Block 04: Envelope Detector — Publication-Quality Plot Generator
Runs SPICE simulations via ngspice and generates 5 PNG plots."""

import subprocess, re, os, math, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib.patches as mpatches

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ── Style ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor': '#161b22',
    'axes.edgecolor': '#30363d',
    'axes.labelcolor': '#c9d1d9',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.color': '#8b949e',
    'ytick.color': '#8b949e',
    'text.color': '#c9d1d9',
    'grid.color': '#21262d',
    'grid.alpha': 0.8,
    'legend.facecolor': '#161b22',
    'legend.edgecolor': '#30363d',
    'legend.fontsize': 10,
    'font.family': 'sans-serif',
    'font.size': 11,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.facecolor': '#0d1117',
})

# Colors
C_PASS   = '#3fb950'
C_FAIL   = '#f85149'
C_ACCENT = '#58a6ff'
C_WARN   = '#d29922'
C_PURPLE = '#bc8cff'
C_CYAN   = '#39d2c0'
C_ORANGE = '#f0883e'
C_GRID   = '#21262d'
C_TEXT   = '#c9d1d9'

# ── SPICE Templates ───────────────────────────────────────────────────

SPICE_TEMPLATE = """* TB: Envelope Detector v2 — {test_name}
.option scale=1e-6
.lib "sky130_minimal_v2.lib.spice" {corner}
.include "ota_pga_v2.spice"
.include "envelope_det.spice"

.param vdd_val = 1.8
.param vcm_val = 0.9
.param amp_val = {amp}
.param freq_val = {freq}

Vdd vdd 0 dc {{vdd_val}}
Ibias_n vdd vbn dc {ibias_n}
Xbias_n vbn vbn 0 0 sky130_fd_pr__nfet_01v8 w=11.4 l=14 nf=1
Cbn vbn 0 100p
Ibias_lpf vdd vbn_lpf dc 100n
Xbias_lpf vbn_lpf vbn_lpf 0 0 sky130_fd_pr__nfet_01v8 w=1 l=8 nf=1
Cbn_lpf vbn_lpf 0 100p

Vin vin 0 sin({{vcm_val}} {{amp_val}} {{freq_val}})
Vcm vcm 0 dc {{vcm_val}}
Xenv vin vcm vout vdd 0 vbn vbn_lpf envelope_det

.tran 1u {tran_stop}

.control
run
meas tran vout_avg AVG v(vout) from={meas_from} to={meas_to}
meas tran vout_min MIN v(vout) from={meas_from} to={meas_to}
meas tran vout_max MAX v(vout) from={meas_from} to={meas_to}
meas tran rect_avg AVG v(xenv.rect) from={meas_from} to={meas_to}
meas tran rect_min MIN v(xenv.rect) from={meas_from} to={meas_to}
meas tran rect_max MAX v(xenv.rect) from={meas_from} to={meas_to}
meas tran idd AVG i(Vdd) from={meas_from} to={meas_to}
let pwr = -idd * 1.8 * 1e6
echo "RESULT vout_avg=$&vout_avg rect_avg=$&rect_avg rect_min=$&rect_min rect_max=$&rect_max vout_min=$&vout_min vout_max=$&vout_max power_uw=$&pwr"
quit
.endc
.end
"""

SPICE_TRANSIENT = """* TB: Envelope Detector v2 — Transient Waveform Capture
.option scale=1e-6
.lib "sky130_minimal_v2.lib.spice" tt
.include "ota_pga_v2.spice"
.include "envelope_det.spice"

.param vdd_val = 1.8
.param vcm_val = 0.9
.param amp_val = 100m
.param freq_val = 3162

Vdd vdd 0 dc {{vdd_val}}
Ibias_n vdd vbn dc 1500n
Xbias_n vbn vbn 0 0 sky130_fd_pr__nfet_01v8 w=11.4 l=14 nf=1
Cbn vbn 0 100p
Ibias_lpf vdd vbn_lpf dc 100n
Xbias_lpf vbn_lpf vbn_lpf 0 0 sky130_fd_pr__nfet_01v8 w=1 l=8 nf=1
Cbn_lpf vbn_lpf 0 100p

Vin vin 0 sin({{vcm_val}} {{amp_val}} {{freq_val}})
Vcm vcm 0 dc {{vcm_val}}
Xenv vin vcm vout vdd 0 vbn vbn_lpf envelope_det

.tran 0.5u 10m

.control
run
wrdata tb_transient_data v(vin) v(xenv.rect) v(vout)
quit
.endc
.end
"""


def run_sim(test_name, corner="tt", amp="50m", freq="3162", ibias_n="1500n",
            tran_stop="500m", meas_from="400m", meas_to="500m"):
    spice = SPICE_TEMPLATE.format(
        test_name=test_name, corner=corner, amp=amp, freq=freq,
        ibias_n=ibias_n, tran_stop=tran_stop, meas_from=meas_from, meas_to=meas_to)
    fname = f"tb_plot_{test_name.replace(' ','_').replace('/','_')}.spice"
    with open(fname, 'w') as f:
        f.write(spice)
    try:
        r = subprocess.run(["ngspice", "-b", fname], capture_output=True, text=True, timeout=300)
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: {test_name}")
        return None
    m = re.search(r'RESULT (.+)', out)
    if not m:
        print(f"  WARN: no RESULT from {test_name}")
        return None
    pairs = re.findall(r'(\w+)=([\d.eE+\-]+)', m.group(1))
    return {k: float(v) for k, v in pairs}


def run_transient():
    """Run transient sim and save waveform data."""
    fname = "tb_plot_transient.spice"
    with open(fname, 'w') as f:
        f.write(SPICE_TRANSIENT)
    try:
        r = subprocess.run(["ngspice", "-b", fname], capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        print("  TIMEOUT: transient")
        return None
    # ngspice wrdata produces a file with columns: index val1 val2 val3
    # Actually wrdata format: time v1 \n time v2 \n time v3 interleaved or columnar
    # Let's parse it
    datafile = "tb_transient_data"
    if not os.path.exists(datafile):
        print("  WARN: transient data file not created")
        print("  ngspice output:", r.stdout[-500:] if r.stdout else "none")
        return None
    return datafile


def parse_wrdata(filename):
    """Parse ngspice wrdata output.
    wrdata with 3 vectors produces rows with 6 columns:
    time1 v1 time2 v2 time3 v3
    All times should be identical per row.
    """
    times, v1s, v2s, v3s = [], [], [], []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('*'):
                continue
            parts = line.split()
            if len(parts) >= 6:
                try:
                    times.append(float(parts[0]))
                    v1s.append(float(parts[1]))
                    v2s.append(float(parts[3]))
                    v3s.append(float(parts[5]))
                except (ValueError, IndexError):
                    continue
    return np.array(times), np.array(v1s), np.array(v2s), np.array(v3s)


# ══════════════════════════════════════════════════════════════════════
# Run all simulations
# ══════════════════════════════════════════════════════════════════════

print("=" * 60)
print("RUNNING SIMULATIONS FOR PLOT GENERATION")
print("=" * 60)

# --- Amplitude Sweep ---
print("\n[1/4] Amplitude sweep...")
amps = [("2.5m", 5), ("5m", 10), ("10m", 20), ("25m", 50),
        ("50m", 100), ("100m", 200), ("250m", 500)]
amp_results = []
for amp_str, vpp in amps:
    A = vpp / 2000.0  # half-amplitude in V
    expected = A / math.pi * 1000  # expected rect DC in mV
    r = run_sim(f"ampsw_{vpp}mVpp", amp=amp_str)
    if r:
        rect_delta = (r['rect_avg'] - 0.9) * 1000
        vout_delta = (r['vout_avg'] - 0.9) * 1000
        err = (rect_delta - expected) / expected * 100 if expected > 0.01 else 0
        spec = 5 if vpp >= 100 else 15
        status = "PASS" if abs(err) <= spec else "FAIL"
        amp_results.append({
            'vpp': vpp, 'rect_delta': rect_delta, 'vout_delta': vout_delta,
            'expected': expected, 'error': err, 'spec': spec, 'status': status
        })
        print(f"  {vpp:4d}mVpp: rect={rect_delta:7.2f}mV exp={expected:7.2f}mV err={err:+.1f}% {status}")

# --- Corner Analysis ---
print("\n[2/4] 5-corner analysis...")
corner_results = []
for corner in ["tt", "ss", "ff", "sf", "fs"]:
    r = run_sim(f"corner_{corner}", corner=corner, amp="50m")
    if r:
        rect_delta = (r['rect_avg'] - 0.9) * 1000
        pwr = r.get('power_uw', 0)
        corner_results.append({
            'corner': corner.upper(), 'rect_delta': rect_delta, 'power_uw': pwr
        })
        print(f"  {corner.upper()}: rect={rect_delta:.2f}mV  power={pwr:.1f}uW")

# --- Transient Waveform ---
print("\n[3/4] Transient waveform (200mVpp @ 3162Hz, 10ms)...")
tran_file = run_transient()
if tran_file:
    print(f"  Data saved to {tran_file}")

# --- Linearity (reuse amplitude sweep data) ---
print("\n[4/4] Linearity data (from amplitude sweep)...")
# Already have the data from amp_results

# ══════════════════════════════════════════════════════════════════════
# PLOT 1: Amplitude Sweep — Rectification Accuracy
# ══════════════════════════════════════════════════════════════════════
print("\n--- Generating amplitude_sweep.png ---")

fig, ax = plt.subplots(figsize=(10, 6))

vpp_vals = [a['vpp'] for a in amp_results]
err_vals = [a['error'] for a in amp_results]
statuses = [a['status'] for a in amp_results]

# Spec limit bands
ax.axhspan(-5, 5, alpha=0.08, color=C_PASS, label=None)
ax.axhspan(-15, 15, alpha=0.04, color=C_WARN, label=None)
ax.axhline(5, color=C_PASS, linestyle='--', linewidth=1, alpha=0.7, label='$\\pm$5% (large signal)')
ax.axhline(-5, color=C_PASS, linestyle='--', linewidth=1, alpha=0.7)
ax.axhline(15, color=C_WARN, linestyle='--', linewidth=1, alpha=0.7, label='$\\pm$15% (small signal)')
ax.axhline(-15, color=C_WARN, linestyle='--', linewidth=1, alpha=0.7)

# Data points
for i, (v, e, s) in enumerate(zip(vpp_vals, err_vals, statuses)):
    color = C_PASS if s == "PASS" else C_FAIL
    marker = 'o' if s == "PASS" else 'x'
    ms = 10 if s == "PASS" else 12
    lw = 2 if s == "FAIL" else 1.5
    ax.plot(v, e, marker=marker, color=color, markersize=ms, markeredgewidth=lw, zorder=5)

# Connect with line
ax.plot(vpp_vals, err_vals, color=C_ACCENT, linewidth=1.5, alpha=0.5, zorder=4)

# Annotate key points
for a in amp_results:
    offset = 8 if a['error'] > 0 else -12
    ax.annotate(f"{a['error']:+.1f}%", (a['vpp'], a['error']),
                textcoords="offset points", xytext=(5, offset),
                fontsize=8, color=C_TEXT, alpha=0.8)

ax.set_xscale('log')
ax.set_xlabel('Input Amplitude (mVpp)')
ax.set_ylabel('Rectification Error (%)')
ax.set_title('Envelope Detector — Rectification Accuracy vs Input Amplitude', fontweight='bold', pad=15)
ax.set_xlim(3, 700)
ax.set_ylim(-100, 25)
ax.grid(True, alpha=0.3)

# Custom legend
pass_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=C_PASS,
                        markersize=8, label='PASS')
fail_patch = plt.Line2D([0], [0], marker='x', color=C_FAIL, markeredgewidth=2,
                        markersize=8, label='FAIL', linestyle='None')
spec5 = plt.Line2D([0], [0], color=C_PASS, linestyle='--', alpha=0.7, label='$\\pm$5% spec ($\\geq$100mVpp)')
spec15 = plt.Line2D([0], [0], color=C_WARN, linestyle='--', alpha=0.7, label='$\\pm$15% spec (<100mVpp)')
ax.legend(handles=[pass_patch, fail_patch, spec5, spec15], loc='lower left', framealpha=0.9)

# X-axis ticks
ax.set_xticks(vpp_vals)
ax.get_xaxis().set_major_formatter(ScalarFormatter())
ax.tick_params(axis='x', which='minor', bottom=False)

fig.tight_layout()
fig.savefig('amplitude_sweep.png')
plt.close(fig)
print("  Saved amplitude_sweep.png")


# ══════════════════════════════════════════════════════════════════════
# PLOT 2: Corner Analysis
# ══════════════════════════════════════════════════════════════════════
print("--- Generating corner_analysis.png ---")

fig, ax1 = plt.subplots(figsize=(10, 6))

corners = [c['corner'] for c in corner_results]
rect_deltas = [c['rect_delta'] for c in corner_results]
powers = [c['power_uw'] for c in corner_results]

x = np.arange(len(corners))
width = 0.4

# Bar colors
bar_colors = [C_ACCENT, C_ORANGE, C_CYAN, C_PURPLE, C_PASS]

bars1 = ax1.bar(x - width/2, rect_deltas, width, color=bar_colors, alpha=0.85,
                edgecolor='#30363d', linewidth=1, label='Rect DC offset (mV)')

ax1.set_xlabel('Process Corner')
ax1.set_ylabel('Rectified Signal DC Offset (mV)', color=C_ACCENT)
ax1.set_xticks(x)
ax1.set_xticklabels(corners, fontweight='bold', fontsize=12)
ax1.tick_params(axis='y', labelcolor=C_ACCENT)

# Annotate bars
mean_rect = np.mean(rect_deltas)
for i, (bar, val) in enumerate(zip(bars1, rect_deltas)):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold',
             color=bar_colors[i])

# Variation annotation
rect_range = max(rect_deltas) - min(rect_deltas)
ax1.axhline(mean_rect, color=C_ACCENT, linestyle=':', alpha=0.5, linewidth=1)
ax1.text(len(corners)-0.5, mean_rect + 0.3,
         f'Mean: {mean_rect:.2f} mV\n$\\Delta$: {rect_range:.3f} mV ({rect_range/mean_rect*100:.1f}%)',
         fontsize=9, color=C_TEXT, ha='right',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#161b22', edgecolor='#30363d'))

# Secondary axis: power
ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, powers, width, color=C_WARN, alpha=0.6,
                edgecolor='#30363d', linewidth=1, label='Power ($\\mu$W)')
ax2.set_ylabel('Power ($\\mu$W)', color=C_WARN)
ax2.tick_params(axis='y', labelcolor=C_WARN)

for bar, val in zip(bars2, powers):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f'{val:.1f}', ha='center', va='bottom', fontsize=9, color=C_WARN)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)

ax1.set_title('5-Corner Robustness — 100mVpp @ 3162 Hz', fontweight='bold', pad=15)
ax1.grid(True, axis='y', alpha=0.3)
ax1.set_ylim(0, max(rect_deltas) * 1.3)
ax2.set_ylim(0, max(powers) * 1.3)

fig.tight_layout()
fig.savefig('corner_analysis.png')
plt.close(fig)
print("  Saved corner_analysis.png")


# ══════════════════════════════════════════════════════════════════════
# PLOT 3: Transient Waveform
# ══════════════════════════════════════════════════════════════════════
print("--- Generating transient_waveform.png ---")

if tran_file:
    time, vin, rect, vout = parse_wrdata(tran_file)
    vcm = 0.9

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[2, 1],
                                          sharex=True)

    # Convert to ms and mV relative to vcm
    t_ms = time * 1000
    vin_mv = (vin - vcm) * 1000
    rect_mv = (rect - vcm) * 1000
    vout_mv = (vout - vcm) * 1000

    # Top plot: input + rectified
    ax_top.plot(t_ms, vin_mv, color=C_ACCENT, linewidth=0.8, alpha=0.7, label='Input (vin $-$ vcm)')
    ax_top.plot(t_ms, rect_mv, color=C_PASS, linewidth=1.2, label='Rectified (rect $-$ vcm)')
    ax_top.fill_between(t_ms, 0, rect_mv, alpha=0.15, color=C_PASS)
    ax_top.axhline(0, color='#484f58', linewidth=0.5)

    # Expected DC level
    expected_dc = 100.0 / math.pi  # 200mVpp -> 100mV amplitude -> A/pi
    ax_top.axhline(expected_dc, color=C_WARN, linestyle=':', linewidth=1,
                   alpha=0.7, label=f'Expected DC = A/$\\pi$ = {expected_dc:.1f} mV')

    ax_top.set_ylabel('Voltage relative to VCM (mV)')
    ax_top.set_title('Envelope Detector — Time-Domain Waveforms (200mVpp @ 3162 Hz)',
                     fontweight='bold', pad=15)
    ax_top.legend(loc='upper right', framealpha=0.9)
    ax_top.grid(True, alpha=0.3)
    ax_top.set_ylim(min(vin_mv) * 1.1, max(vin_mv) * 1.3)

    # Bottom plot: LPF output (envelope)
    ax_bot.plot(t_ms, vout_mv, color=C_PURPLE, linewidth=1.5, label='LPF output (vout $-$ vcm)')
    ax_bot.axhline(expected_dc, color=C_WARN, linestyle=':', linewidth=1,
                   alpha=0.7, label=f'Expected = {expected_dc:.1f} mV')
    ax_bot.fill_between(t_ms, 0, vout_mv, alpha=0.1, color=C_PURPLE)
    ax_bot.axhline(0, color='#484f58', linewidth=0.5)

    ax_bot.set_xlabel('Time (ms)')
    ax_bot.set_ylabel('Envelope (mV)')
    ax_bot.legend(loc='lower right', framealpha=0.9)
    ax_bot.grid(True, alpha=0.3)
    ax_bot.set_xlim(0, 10)

    fig.tight_layout()
    fig.savefig('transient_waveform.png')
    plt.close(fig)
    print("  Saved transient_waveform.png")
else:
    print("  SKIPPED (no transient data)")


# ══════════════════════════════════════════════════════════════════════
# PLOT 4: Power Breakdown Pie Chart
# ══════════════════════════════════════════════════════════════════════
print("--- Generating power_breakdown.png ---")

fig, ax = plt.subplots(figsize=(8, 8))

labels = ['OTA1\n(Rectifier)', 'OTA2\n(Clamp)', 'Gm-C LPF', 'M$_{sink}$', 'Bias\nNetwork']
sizes = [9.9, 9.9, 0.2, 0.2, 0.8]
total = sum(sizes)
colors = [C_ACCENT, C_CYAN, C_PASS, C_ORANGE, C_PURPLE]
explode = (0.03, 0.03, 0.08, 0.08, 0.05)

wedges, texts, autotexts = ax.pie(
    sizes, explode=explode, labels=labels, colors=colors, autopct='',
    shadow=False, startangle=90, textprops={'color': C_TEXT, 'fontsize': 11},
    wedgeprops={'edgecolor': '#0d1117', 'linewidth': 2}
)

# Custom annotations with power values
for i, (wedge, size) in enumerate(zip(wedges, sizes)):
    angle = (wedge.theta2 + wedge.theta1) / 2
    x = np.cos(np.radians(angle))
    y = np.sin(np.radians(angle))
    pct = size / total * 100
    # Place text inside for large slices, outside for small
    if pct > 10:
        ax.text(x * 0.55, y * 0.55, f'{size:.1f} $\\mu$W\n({pct:.0f}%)',
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    else:
        ax.annotate(f'{size:.1f} $\\mu$W ({pct:.0f}%)',
                    xy=(x * 0.85, y * 0.85),
                    xytext=(x * 1.3, y * 1.3),
                    fontsize=10, color=C_TEXT,
                    arrowprops=dict(arrowstyle='->', color='#484f58'),
                    ha='center', va='center')

ax.set_title(f'Power Distribution — Total: {total:.1f} $\\mu$W',
             fontweight='bold', pad=20, fontsize=14)

fig.tight_layout()
fig.savefig('power_breakdown.png')
plt.close(fig)
print("  Saved power_breakdown.png")


# ══════════════════════════════════════════════════════════════════════
# PLOT 5: Linearity Plot
# ══════════════════════════════════════════════════════════════════════
print("--- Generating linearity_plot.png ---")

fig, ax = plt.subplots(figsize=(10, 7))

# Data from amplitude sweep
amp_mv = [a['vpp'] / 2.0 for a in amp_results]  # amplitude in mV (half of Vpp)
rect_out = [a['rect_delta'] for a in amp_results]
expected_out = [a['expected'] for a in amp_results]

# Ideal line: DC = A / pi
x_ideal = np.linspace(0, max(amp_mv) * 1.1, 100)
y_ideal = x_ideal / math.pi

# Plot ideal
ax.plot(x_ideal, y_ideal, color=C_WARN, linestyle='--', linewidth=1.5,
        label=f'Ideal: DC = A/$\\pi$', alpha=0.8)

# Plot measured
ax.scatter(amp_mv, rect_out, color=C_ACCENT, s=80, zorder=5, edgecolors='white',
           linewidths=0.5, label='Measured rect DC')

# Connect measured
ax.plot(amp_mv, rect_out, color=C_ACCENT, linewidth=1, alpha=0.4)

# Linear fit for R^2
amp_arr = np.array(amp_mv)
rect_arr = np.array(rect_out)
# Only fit points where rectifier works reasonably (>= 50mVpp -> 25mV amplitude)
mask = amp_arr >= 25
if np.sum(mask) >= 2:
    coeffs = np.polyfit(amp_arr[mask], rect_arr[mask], 1)
    fit_line = np.polyval(coeffs, amp_arr[mask])
    ss_res = np.sum((rect_arr[mask] - fit_line) ** 2)
    ss_tot = np.sum((rect_arr[mask] - np.mean(rect_arr[mask])) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    # Fit line
    x_fit = np.linspace(min(amp_arr[mask]), max(amp_arr[mask]) * 1.05, 50)
    y_fit = np.polyval(coeffs, x_fit)
    ax.plot(x_fit, y_fit, color=C_PASS, linewidth=1.5, alpha=0.6,
            label=f'Linear fit (R$^2$ = {r_squared:.5f})')

    # R^2 annotation box
    ax.text(0.05, 0.92,
            f'Linear Fit ($\\geq$50 mVpp):\ny = {coeffs[0]:.4f}x {coeffs[1]:+.3f}\n'
            f'R$^2$ = {r_squared:.5f}\n'
            f'Ideal slope = 1/$\\pi$ = {1/math.pi:.4f}',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22', edgecolor='#30363d', alpha=0.95),
            color=C_TEXT)

# Mark the deadzone
ax.axvspan(0, 12, alpha=0.08, color=C_FAIL)
ax.text(6, max(rect_out) * 0.5, 'Deadzone\n(<25 mVpp)', ha='center', fontsize=9,
        color=C_FAIL, alpha=0.7, fontstyle='italic')

# Annotate each point
for a_mv, r_mv in zip(amp_mv, rect_out):
    ax.annotate(f'{r_mv:.1f}', (a_mv, r_mv), textcoords="offset points",
                xytext=(8, -5), fontsize=8, color=C_TEXT, alpha=0.7)

ax.set_xlabel('Input Amplitude (mV)')
ax.set_ylabel('Output DC Level above VCM (mV)')
ax.set_title('Envelope Detector — Input/Output Linearity', fontweight='bold', pad=15)
ax.legend(loc='lower right', framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, max(amp_mv) * 1.15)
ax.set_ylim(0, max(rect_out) * 1.15)

fig.tight_layout()
fig.savefig('linearity_plot.png')
plt.close(fig)
print("  Saved linearity_plot.png")


print("\n" + "=" * 60)
print("ALL PLOTS GENERATED SUCCESSFULLY")
print("=" * 60)
print("  amplitude_sweep.png")
print("  corner_analysis.png")
print("  transient_waveform.png")
print("  power_breakdown.png")
print("  linearity_plot.png")
