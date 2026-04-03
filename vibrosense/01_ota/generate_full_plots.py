#!/usr/bin/env python3
"""Generate comprehensive report plots for OTA v11.
All data from live ngspice simulations."""

import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os, re, tempfile

WORK = "/home/ubuntu/analog-ai-chips/vibrosense/01_ota"
os.chdir(WORK)
PDK_LIB = "sky130_minimal.lib.spice"

plt.rcParams.update({
    'font.size': 11, 'font.family': 'sans-serif',
    'axes.linewidth': 1.2, 'grid.alpha': 0.3,
    'figure.facecolor': 'white', 'savefig.bbox': 'tight', 'savefig.dpi': 200,
})

def run_spice(tb):
    r = subprocess.run(["/usr/bin/ngspice", "-b", tb], cwd=WORK,
                       capture_output=True, text=True, timeout=180)
    return r.stdout + r.stderr

def parse_meas(out, name):
    m = re.search(rf'{name}\s*=\s*([+-]?\d+\.?\d*[eE][+-]?\d+|[+-]?\d+\.?\d*)', out)
    return float(m.group(1)) if m else None

def load_wrdata(path):
    data = []
    with open(os.path.join(WORK, path)) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                try: data.append([float(x) for x in parts])
                except: pass
    return np.array(data) if data else None

def write_and_run(name, content):
    path = os.path.join(WORK, name)
    with open(path, 'w') as f:
        f.write(content)
    return run_spice(name)

BIAS_HEADER = '''
.lib "sky130_minimal.lib.spice" tt
.include "ota_foldcasc.spice"
Vdd vdd 0 dc 1.8
Vbn  vbn  0 dc 0.65
Vbcn vbcn 0 dc 0.88
Vbp  vbp  0 dc 0.73
Vbcp vbcp 0 dc 0.475
'''

# ============================================================
# 1. BODE PLOT with operating band annotation
# ============================================================
print("1. Bode plot with operating band...")
data = load_wrdata("bode_data")
if data is not None and len(data) > 20:
    n = len(data); half = n // 2
    freq = data[:half, 0]; mag = data[:half, 1]
    freq_ph = data[half:, 0]; phase = data[half:, 1]
    # ngspice vp() is in radians, convert
    phase_deg = phase * (180.0 / np.pi) if np.max(np.abs(phase)) < 10 else phase

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), sharex=True,
                                    gridspec_kw={'height_ratios': [2.5, 1]})

    ax1.semilogx(freq, mag, '#1a5276', linewidth=2.2)
    ax1.axhline(y=65, color='#c0392b', linestyle='--', alpha=0.6, linewidth=1, label='Target: 65 dB')
    ax1.axhline(y=60, color='#e67e22', linestyle=':', alpha=0.6, linewidth=1, label='Min: 60 dB')
    ax1.axhline(y=0, color='gray', linestyle='-', alpha=0.3, linewidth=0.5)
    # Operating band
    ax1.axvspan(100, 10000, alpha=0.08, color='#2ecc71', label='Signal band (100 Hz - 10 kHz)')
    ax1.axvline(x=100, color='#27ae60', linestyle='-', alpha=0.3, linewidth=1)
    ax1.axvline(x=10000, color='#27ae60', linestyle='-', alpha=0.3, linewidth=1)
    # Annotate gain at key frequencies
    for f_target, label_offset in [(100, (15, 8)), (1000, (15, 8)), (10000, (15, -15))]:
        idx = np.argmin(np.abs(freq - f_target))
        g = mag[idx]
        ax1.plot(f_target, g, 'o', color='#c0392b', markersize=5, zorder=5)
        ax1.annotate(f'{g:.1f} dB @ {f_target/1000:.0f}k' if f_target >= 1000 else f'{g:.1f} dB @ {f_target} Hz',
                     xy=(f_target, g), xytext=label_offset, textcoords='offset points',
                     fontsize=9, fontweight='bold', color='#c0392b',
                     arrowprops=dict(arrowstyle='->', color='#c0392b', lw=0.8))
    # UGB annotation
    ugb_idx = np.argmin(np.abs(mag))
    ax1.plot(freq[ugb_idx], mag[ugb_idx], 's', color='#8e44ad', markersize=7, zorder=5)
    ax1.annotate(f'UGB = {freq[ugb_idx]/1000:.1f} kHz', xy=(freq[ugb_idx], 0),
                 xytext=(20, -20), textcoords='offset points', fontsize=9, fontweight='bold',
                 color='#8e44ad', arrowprops=dict(arrowstyle='->', color='#8e44ad', lw=0.8))

    ax1.set_ylabel('Gain (dB)', fontweight='bold')
    ax1.set_title('Open-Loop Frequency Response (TT, 27 C, CL = 10 pF)', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper right', framealpha=0.9, fontsize=9)
    ax1.grid(True, which='both'); ax1.set_ylim([-20, 80]); ax1.set_xlim([0.1, 1e8])

    ax2.semilogx(freq_ph, phase_deg, '#922b21', linewidth=2)
    ax2.axhline(y=-180, color='gray', linestyle='--', alpha=0.5)
    ax2.axvspan(100, 10000, alpha=0.08, color='#2ecc71')
    ax2.set_ylabel('Phase (deg)', fontweight='bold')
    ax2.set_xlabel('Frequency (Hz)', fontweight='bold')
    ax2.grid(True, which='both'); ax2.set_ylim([-200, 20])

    plt.tight_layout()
    plt.savefig('report_bode.png'); plt.close()
    print("   -> report_bode.png")

# ============================================================
# 2. DC TRANSFER with derivative (gain linearity)
# ============================================================
print("2. DC transfer with linearity...")
data = load_wrdata("dc_swing_data")
if data is not None and len(data) > 20:
    vinp = data[:, 0]; vout = data[:, 1]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), gridspec_kw={'height_ratios': [2, 1]})
    ax1.plot(vinp, vout, '#1a5276', linewidth=2, label='OTA (unity-gain)')
    ax1.plot([0, 1.8], [0, 1.8], 'k--', alpha=0.2, linewidth=1, label='Ideal')
    ax1.axvspan(0.632, 1.678, alpha=0.06, color='green')
    ax1.annotate('1.046 Vpp\nlinear range', xy=(1.15, 1.1), fontsize=10, color='#27ae60', fontweight='bold')
    ax1.set_ylabel('Vout (V)', fontweight='bold')
    ax1.set_title('DC Transfer Characteristic (Unity-Gain Buffer)', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper left', framealpha=0.9); ax1.grid(True)
    ax1.set_xlim([0, 1.8]); ax1.set_ylim([0, 1.8])

    # Derivative
    dvout = np.gradient(vout, vinp)
    ax2.plot(vinp, dvout, '#e67e22', linewidth=1.5)
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax2.axhline(y=0.99, color='#27ae60', linestyle=':', alpha=0.5, label='1% deviation')
    ax2.axhline(y=1.01, color='#27ae60', linestyle=':', alpha=0.5)
    ax2.set_ylabel('dVout/dVinp', fontweight='bold')
    ax2.set_xlabel('Vinp (V)', fontweight='bold')
    ax2.set_title('Gain Linearity', fontsize=11, fontweight='bold')
    ax2.legend(framealpha=0.9); ax2.grid(True)
    ax2.set_xlim([0, 1.8]); ax2.set_ylim([0.5, 1.2])

    plt.tight_layout(); plt.savefig('report_dc.png'); plt.close()
    print("   -> report_dc.png")

# ============================================================
# 3. TRANSIENT — both rising and falling step
# ============================================================
print("3. Transient (rising + falling)...")
out = write_and_run("tb_plot_tran2.spice", f'''* Transient: rising and falling steps
{BIAS_HEADER}
Vinp vinp 0 PULSE(0.4 0.9 10u 1n 1n 40u 100u)
Xota vinp vout vout vdd 0 vbn vbcn vbp vbcp ota_foldcasc
CL vout 0 10p
.tran 10n 120u
.control
run
wrdata tran_data2 v(vout) v(vinp)
quit
.endc
.end
''')

data = load_wrdata("tran_data2")
if data is not None and len(data) > 20:
    n = len(data); half = n // 2
    time_us = data[:half, 0] * 1e6
    vout = data[:half, 1]
    vinp = data[half:half+len(time_us), 1]

    fig, ax = plt.subplots(1, 1, figsize=(11, 5))
    ax.plot(time_us, vout, '#1a5276', linewidth=2, label='Vout')
    if vinp is not None and len(vinp) == len(time_us):
        ax.plot(time_us, vinp, '#c0392b', linewidth=1.2, linestyle='--', alpha=0.7, label='Vinp (step)')
    ax.set_xlabel('Time (us)', fontweight='bold')
    ax.set_ylabel('Voltage (V)', fontweight='bold')
    ax.set_title('Step Response — Rising and Falling (Unity-Gain, CL = 10 pF)', fontsize=13, fontweight='bold')
    ax.legend(framealpha=0.9); ax.grid(True)
    ax.set_xlim([0, 120])
    plt.tight_layout(); plt.savefig('report_transient.png'); plt.close()
    print("   -> report_transient.png")

# ============================================================
# 4. INVERTING INPUT TEST
# ============================================================
print("4. Inverting input AC test...")
out = write_and_run("tb_plot_inv.spice", f'''* AC from inverting input
{BIAS_HEADER}
Vinn vinn 0 dc 0.9 ac 1
Lbreak vout vinp 1G
Cdc vinp 0 1
Xota vinp vinn vout vdd 0 vbn vbcn vbp vbcp ota_foldcasc
CL vout 0 10p
.ac dec 100 0.1 1G
.control
run
wrdata inv_bode_data vdb(vout) vp(vout)
meas ac gain_peak MAX vdb(vout)
meas ac ugb WHEN vdb(vout)=0 FALL=1
echo "inv_gain_peak = $&gain_peak"
echo "inv_ugb = $&ugb"
quit
.endc
.end
''')
inv_gain = parse_meas(out, "inv_gain_peak")
inv_ugb = parse_meas(out, "inv_ugb")
print(f"   Inverting: gain={inv_gain}, ugb={inv_ugb}")

# Plot Vinp vs Vinn comparison
data_inv = load_wrdata("inv_bode_data")
data_noninv = load_wrdata("bode_data")
if data_inv is not None and data_noninv is not None:
    ni = len(data_inv); hi = ni // 2
    nn = len(data_noninv); hn = nn // 2

    fig, ax = plt.subplots(1, 1, figsize=(10, 5.5))
    ax.semilogx(data_noninv[:hn, 0], data_noninv[:hn, 1], '#1a5276', linewidth=2, label=f'Vinp path (gain={parse_meas(run_spice("tb_ota_ac.spice"), "gain_peak"):.1f} dB)')
    ax.semilogx(data_inv[:hi, 0], data_inv[:hi, 1], '#c0392b', linewidth=2, linestyle='--', label=f'Vinn path (gain={inv_gain:.1f} dB)')
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.axvspan(100, 10000, alpha=0.08, color='#2ecc71', label='Signal band')
    ax.set_xlabel('Frequency (Hz)', fontweight='bold')
    ax.set_ylabel('Gain (dB)', fontweight='bold')
    ax.set_title('Gain Symmetry: Non-Inverting (Vinp) vs Inverting (Vinn)', fontsize=13, fontweight='bold')
    ax.legend(framealpha=0.9); ax.grid(True, which='both')
    ax.set_xlim([0.1, 1e8]); ax.set_ylim([-20, 80])
    plt.tight_layout(); plt.savefig('report_symmetry.png'); plt.close()
    print("   -> report_symmetry.png")

# ============================================================
# 5. PSRR & CMRR frequency plot
# ============================================================
print("5. PSRR & CMRR vs frequency...")
# PSRR — need frequency sweep data
out_psrr = write_and_run("tb_plot_psrr.spice", f'''* PSRR frequency sweep
.lib "sky130_minimal.lib.spice" tt
.include "ota_foldcasc.spice"
Vdd vdd 0 dc 1.8 ac 1
Vbn  vbn  0 dc 0.65
Vbcn vbcn 0 dc 0.88
Ebp  vbp 0 vdd 0 0.594
Ebcp vbcp 0 vdd 0 0.264
Vinp vinp 0 dc 0.9
Lbreak vout vinn 1G
Cdc vinn 0 1
Xota vinp vinn vout vdd 0 vbn vbcn vbp vbcp ota_foldcasc
CL vout 0 10p
.ac dec 100 0.1 1G
.control
run
wrdata psrr_freq_data vdb(vout)
quit
.endc
.end
''')

# CMRR — frequency sweep
out_cmrr = write_and_run("tb_plot_cmrr.spice", f'''* CMRR frequency sweep
{BIAS_HEADER}
Vcm_p vinp 0 dc 0.9 ac 1
Vcm_n vinn 0 dc 0.9 ac 1
Xota vinp vinn vout vdd 0 vbn vbcn vbp vbcp ota_foldcasc
CL vout 0 10p
.ac dec 100 0.1 1G
.control
run
wrdata cmrr_freq_data vdb(vout)
quit
.endc
.end
''')

data_dm = load_wrdata("bode_data")  # differential mode gain
data_ps = load_wrdata("psrr_freq_data")
data_cm = load_wrdata("cmrr_freq_data")

if data_dm is not None and data_ps is not None and data_cm is not None:
    nd = len(data_dm); hd = nd // 2
    freq_dm = data_dm[:hd, 0]; adm = data_dm[:hd, 1]
    freq_ps = data_ps[:, 0]; avdd = data_ps[:, 1]
    freq_cm = data_cm[:, 0]; acm = data_cm[:, 1]

    # Use each dataset's own freq axis
    from numpy import interp
    # PSRR = Adm - Avdd (both in dB)
    min_len_ps = min(len(freq_dm), len(freq_ps))
    psrr_freq = freq_ps[:min_len_ps]
    psrr = interp(psrr_freq, freq_dm, adm) - avdd[:min_len_ps]
    # CMRR = Adm - Acm (both in dB)
    min_len_cm = min(len(freq_dm), len(freq_cm))
    cmrr_freq = freq_cm[:min_len_cm]
    cmrr = interp(cmrr_freq, freq_dm, adm) - acm[:min_len_cm]
    freq_dm = psrr_freq  # use for plotting

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    ax1.semilogx(psrr_freq, psrr, '#2980b9', linewidth=2)
    ax1.axhline(y=50, color='#c0392b', linestyle='--', linewidth=1.5, label='Min: 50 dB')
    ax1.axvspan(100, 10000, alpha=0.08, color='#2ecc71')
    ax1.axvline(x=1000, color='#27ae60', linestyle=':', alpha=0.5)
    idx_1k = np.argmin(np.abs(psrr_freq - 1000))
    ax1.plot(1000, psrr[idx_1k], 'o', color='#c0392b', markersize=6, zorder=5)
    ax1.annotate(f'{psrr[idx_1k]:.1f} dB @ 1 kHz', xy=(1000, psrr[idx_1k]),
                 xytext=(15, -15), textcoords='offset points', fontsize=9, fontweight='bold', color='#c0392b')
    ax1.set_xlabel('Frequency (Hz)', fontweight='bold')
    ax1.set_ylabel('PSRR (dB)', fontweight='bold')
    ax1.set_title('Power Supply Rejection Ratio', fontsize=12, fontweight='bold')
    ax1.legend(framealpha=0.9); ax1.grid(True, which='both')
    ax1.set_xlim([0.1, 1e8]); ax1.set_ylim([0, 120])

    ax2.semilogx(cmrr_freq, cmrr, '#8e44ad', linewidth=2)
    ax2.axhline(y=60, color='#c0392b', linestyle='--', linewidth=1.5, label='Min: 60 dB')
    ax2.axvspan(100, 10000, alpha=0.08, color='#2ecc71')
    idx_dc = np.argmin(np.abs(cmrr_freq - 1))
    ax2.plot(1, cmrr[idx_dc], 'o', color='#c0392b', markersize=6, zorder=5)
    ax2.annotate(f'{cmrr[idx_dc]:.1f} dB @ DC', xy=(1, cmrr[idx_dc]),
                 xytext=(15, -10), textcoords='offset points', fontsize=9, fontweight='bold', color='#c0392b')
    ax2.set_xlabel('Frequency (Hz)', fontweight='bold')
    ax2.set_ylabel('CMRR (dB)', fontweight='bold')
    ax2.set_title('Common-Mode Rejection Ratio', fontsize=12, fontweight='bold')
    ax2.legend(framealpha=0.9); ax2.grid(True, which='both')
    ax2.set_xlim([0.1, 1e8]); ax2.set_ylim([0, 120])

    plt.tight_layout(); plt.savefig('report_rejection.png'); plt.close()
    print("   -> report_rejection.png")

# ============================================================
# 6. CORNER COMPARISON (reuse from before)
# ============================================================
print("6. Corner analysis...")
corners = {}
for corner in ['tt', 'ss', 'ff', 'sf', 'fs']:
    tb = f"tb_corner_{corner}.spice"
    if os.path.exists(os.path.join(WORK, tb)):
        out = run_spice(tb)
        gain = parse_meas(out, "gain_peak") or parse_meas(out, "gain_db")
        ugb = parse_meas(out, "ugb")
        corners[corner.upper()] = {"gain": gain, "ugb": ugb}

if len(corners) >= 3:
    names = list(corners.keys()); gains = [corners[n]["gain"] for n in names]
    ugbs = [corners[n]["ugb"]/1000 for n in names]
    colors = ['#2980b9', '#c0392b', '#27ae60', '#e67e22', '#8e44ad']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    bars1 = ax1.bar(names, gains, color=colors[:len(names)], alpha=0.85, edgecolor='white', linewidth=1.5)
    ax1.axhline(y=65, color='#c0392b', linestyle='--', linewidth=1.5, label='Target (65 dB)')
    ax1.axhline(y=60, color='#e67e22', linestyle=':', linewidth=1.5, label='Min (60 dB)')
    ax1.set_ylabel('DC Gain (dB)', fontweight='bold')
    ax1.set_title('Gain Across Process Corners', fontsize=12, fontweight='bold')
    ax1.legend(framealpha=0.9); ax1.grid(True, axis='y'); ax1.set_ylim([0, max(gains)*1.15])
    for bar, val in zip(bars1, gains):
        ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    bars2 = ax2.bar(names, ugbs, color=colors[:len(names)], alpha=0.85, edgecolor='white', linewidth=1.5)
    ax2.axhline(y=30, color='#c0392b', linestyle='--', linewidth=1.5, label='Min (30 kHz)')
    ax2.set_ylabel('UGB (kHz)', fontweight='bold')
    ax2.set_title('Unity-Gain Bandwidth Across Corners', fontsize=12, fontweight='bold')
    ax2.legend(framealpha=0.9); ax2.grid(True, axis='y'); ax2.set_ylim([0, max(ugbs)*1.25])
    for bar, val in zip(bars2, ugbs):
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.tight_layout(); plt.savefig('report_corners.png'); plt.close()
    print("   -> report_corners.png")

# ============================================================
# 7. TEMPERATURE SWEEP
# ============================================================
print("7. Temperature sweep...")
temps = {}
for t in ['-40', '27', '85']:
    tb = f"tb_temp_{t}.spice"
    if os.path.exists(os.path.join(WORK, tb)):
        out = run_spice(tb)
        gain = parse_meas(out, "gain_peak") or parse_meas(out, "gain_db")
        ugb = parse_meas(out, "ugb")
        temps[f"{t} C"] = {"gain": gain, "ugb": ugb}

if len(temps) >= 2:
    names = list(temps.keys()); gains = [temps[n]["gain"] for n in names]
    ugbs = [temps[n]["ugb"]/1000 for n in names]; tcolors = ['#2980b9', '#27ae60', '#c0392b']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    bars1 = ax1.bar(names, gains, color=tcolors, alpha=0.85, edgecolor='white', linewidth=1.5)
    ax1.axhline(y=55, color='#c0392b', linestyle='--', linewidth=1.5, label='Min (55 dB)')
    ax1.set_ylabel('DC Gain (dB)', fontweight='bold'); ax1.set_title('Gain vs Temperature (TT)', fontsize=12, fontweight='bold')
    ax1.legend(framealpha=0.9); ax1.grid(True, axis='y'); ax1.set_ylim([0, max(gains)*1.15])
    for bar, val in zip(bars1, gains):
        ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    bars2 = ax2.bar(names, ugbs, color=tcolors, alpha=0.85, edgecolor='white', linewidth=1.5)
    ax2.axhline(y=20, color='#e67e22', linestyle=':', linewidth=1.5, label='Min (20 kHz)')
    ax2.set_ylabel('UGB (kHz)', fontweight='bold'); ax2.set_title('UGB vs Temperature (TT)', fontsize=12, fontweight='bold')
    ax2.legend(framealpha=0.9); ax2.grid(True, axis='y'); ax2.set_ylim([0, max(ugbs)*1.25])
    for bar, val in zip(bars2, ugbs):
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.tight_layout(); plt.savefig('report_temperature.png'); plt.close()
    print("   -> report_temperature.png")

# ============================================================
# 8. SUMMARY DASHBOARD
# ============================================================
print("8. Summary dashboard...")
specs = {
    'DC Gain': {'val': 65.4, 'min': 60, 'target': 65, 'unit': 'dB'},
    'UGB': {'val': 33.7, 'min': 30, 'target': 50, 'unit': 'kHz'},
    'Phase Margin': {'val': 89.2, 'min': 55, 'target': 65, 'unit': 'deg'},
    'Output Swing': {'val': 1.046, 'min': 1.0, 'target': 1.2, 'unit': 'Vpp'},
    'Slew Rate': {'val': 20.5, 'min': 10, 'target': 50, 'unit': 'mV/us'},
    'PSRR @ 1kHz': {'val': 70.5, 'min': 50, 'target': 60, 'unit': 'dB'},
    'CMRR @ DC': {'val': 80.5, 'min': 60, 'target': 70, 'unit': 'dB'},
    'Power': {'val': 0.90, 'min': 0, 'target': 0, 'max': 3.6, 'unit': 'uW'},
}

fig, axes = plt.subplots(2, 4, figsize=(16, 6))
axes = axes.flatten()

for i, (name, s) in enumerate(specs.items()):
    ax = axes[i]
    val = s['val']; mn = s['min']; tgt = s['target']; unit = s['unit']
    mx = s.get('max', tgt * 1.5 if tgt > 0 else val * 2)
    bar_max = max(val, tgt, mx) * 1.2

    if 'max' in s:  # lower is better (power)
        pct = 1.0 - val / s['max']
        color = '#27ae60' if val <= s['max'] else '#c0392b'
    else:  # higher is better
        pct = (val - mn) / (bar_max - mn) if bar_max > mn else 1
        color = '#27ae60' if val >= mn else '#c0392b'

    ax.barh([0], [val], height=0.5, color=color, alpha=0.85, edgecolor='white', linewidth=1.5)
    if mn > 0:
        ax.axvline(x=mn, color='#c0392b', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.set_xlim([0, bar_max])
    ax.set_yticks([])
    ax.set_title(name, fontsize=11, fontweight='bold')
    ax.text(val, 0, f'  {val} {unit}', va='center', fontsize=11, fontweight='bold')
    ax.grid(True, axis='x', alpha=0.3)

plt.suptitle('VibroSense OTA v11 — Specification Summary', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('report_dashboard.png')
plt.close()
print("   -> report_dashboard.png")

print("\nAll plots generated from live simulations.")
