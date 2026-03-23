#!/usr/bin/env python3
"""Generate final report plots — correct data parsing."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import subprocess, os, re

WORK = "/home/ubuntu/analog-ai-chips/vibrosense/01_ota"
os.chdir(WORK)

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

# ============================================================
# 1. BODE PLOT — full range, correct parsing
# ============================================================
print("1. Bode plot...")
# bode_data: 4 columns — freq, mag_dB, freq, phase_rad
data = np.loadtxt("bode_data")
freq = data[:, 0]
mag_db = data[:, 1]
phase_rad = data[:, 3]
phase_deg = np.degrees(phase_rad)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), sharex=True,
                                gridspec_kw={'height_ratios': [2.5, 1]})

ax1.semilogx(freq, mag_db, '#1a5276', linewidth=2.2)
ax1.axhline(y=65, color='#c0392b', linestyle='--', alpha=0.6, linewidth=1, label='Target: 65 dB')
ax1.axhline(y=60, color='#e67e22', linestyle=':', alpha=0.6, linewidth=1, label='Min: 60 dB')
ax1.axhline(y=0, color='gray', linestyle='-', alpha=0.3, linewidth=0.5)
ax1.axvspan(100, 10000, alpha=0.08, color='#2ecc71', label='Signal band (100 Hz - 10 kHz)')

# Annotate gain at key frequencies
for f_target in [100, 1000, 10000]:
    idx = np.argmin(np.abs(freq - f_target))
    g = mag_db[idx]
    label = f'{g:.1f} dB @ {f_target/1000:.0f}k' if f_target >= 1000 else f'{g:.1f} dB @ {f_target} Hz'
    offset = (15, 10) if f_target < 10000 else (15, -15)
    ax1.plot(f_target, g, 'o', color='#c0392b', markersize=5, zorder=5)
    ax1.annotate(label, xy=(f_target, g), xytext=offset, textcoords='offset points',
                 fontsize=9, fontweight='bold', color='#c0392b',
                 arrowprops=dict(arrowstyle='->', color='#c0392b', lw=0.8))

# UGB
ugb_idx = np.argmin(np.abs(mag_db[mag_db > -50]))  # find closest to 0dB
for i in range(len(mag_db) - 1):
    if mag_db[i] > 0 and mag_db[i+1] <= 0:
        ugb_idx = i; break
ugb_freq = freq[ugb_idx]
ax1.plot(ugb_freq, 0, 's', color='#8e44ad', markersize=7, zorder=5)
ax1.annotate(f'UGB = {ugb_freq/1000:.1f} kHz', xy=(ugb_freq, 0),
             xytext=(20, -25), textcoords='offset points', fontsize=9, fontweight='bold',
             color='#8e44ad', arrowprops=dict(arrowstyle='->', color='#8e44ad', lw=0.8))

# PM annotation
pm = phase_deg[ugb_idx] + 180
ax1.set_ylabel('Gain (dB)', fontweight='bold')
ax1.set_title('Open-Loop Frequency Response (TT, 27 C, CL = 10 pF)', fontsize=13, fontweight='bold')
ax1.legend(loc='upper right', framealpha=0.9, fontsize=9)
ax1.grid(True, which='both'); ax1.set_ylim([-100, 80]); ax1.set_xlim([0.1, 1e9])

ax2.semilogx(freq, phase_deg, '#922b21', linewidth=2)
ax2.axhline(y=-180, color='gray', linestyle='--', alpha=0.5)
ax2.axhline(y=-90, color='gray', linestyle=':', alpha=0.3)
ax2.axvspan(100, 10000, alpha=0.08, color='#2ecc71')
# PM annotation on phase plot
ax2.plot(ugb_freq, phase_deg[ugb_idx], 's', color='#8e44ad', markersize=6, zorder=5)
ax2.annotate(f'PM = {pm:.0f} deg', xy=(ugb_freq, phase_deg[ugb_idx]),
             xytext=(15, -20), textcoords='offset points', fontsize=9, fontweight='bold', color='#8e44ad')
ax2.set_ylabel('Phase (deg)', fontweight='bold')
ax2.set_xlabel('Frequency (Hz)', fontweight='bold')
ax2.grid(True, which='both'); ax2.set_ylim([-200, 20])

plt.tight_layout(); plt.savefig('report_bode.png'); plt.close()
print(f"   -> report_bode.png (DC gain={mag_db[0]:.1f}dB, UGB={ugb_freq/1000:.1f}kHz, PM={pm:.0f}deg)")

# ============================================================
# 2. DC TRANSFER — full range with linearity
# ============================================================
print("2. DC transfer...")
# dc_swing_data: 2 columns — Vinp, Vout
data = np.loadtxt("dc_swing_data")
vinp = data[:, 0]
vout = data[:, 1]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), gridspec_kw={'height_ratios': [2, 1]})

ax1.plot(vinp, vout, '#1a5276', linewidth=2, label='OTA (unity-gain buffer)')
ax1.plot([0, 1.8], [0, 1.8], 'k--', alpha=0.2, linewidth=1, label='Ideal (Vout = Vinp)')

# Find linear range (where derivative is within 5% of 1.0)
dvout = np.gradient(vout, vinp)
linear_mask = (dvout > 0.95) & (dvout < 1.05)
if np.any(linear_mask):
    lin_start = vinp[np.argmax(linear_mask)]
    lin_end = vinp[len(linear_mask) - 1 - np.argmax(linear_mask[::-1])]
    ax1.axvspan(lin_start, lin_end, alpha=0.06, color='green')
    swing = vout[np.argmax(linear_mask[::-1])] - vout[np.argmax(linear_mask)]

ax1.set_ylabel('Vout (V)', fontweight='bold')
ax1.set_title('DC Transfer Characteristic (Unity-Gain Buffer)', fontsize=13, fontweight='bold')
ax1.legend(loc='upper left', framealpha=0.9); ax1.grid(True)
ax1.set_xlim([0, 1.8]); ax1.set_ylim([0, 1.8])
ax1.annotate(f'Vout range: {vout.min():.3f} V to {vout.max():.3f} V\nSwing: {vout.max()-vout.min():.3f} Vpp',
             xy=(0.05, 1.5), fontsize=10, fontweight='bold', color='#1a5276',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Derivative plot
ax2.plot(vinp, dvout, '#e67e22', linewidth=1.5)
ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Unity gain')
ax2.axhline(y=0.95, color='#27ae60', linestyle=':', alpha=0.5, label='5% deviation')
ax2.axhline(y=1.05, color='#27ae60', linestyle=':', alpha=0.5)
ax2.set_ylabel('dVout/dVinp', fontweight='bold')
ax2.set_xlabel('Vinp (V)', fontweight='bold')
ax2.set_title('Gain Linearity', fontsize=11, fontweight='bold')
ax2.legend(framealpha=0.9); ax2.grid(True)
ax2.set_xlim([0, 1.8]); ax2.set_ylim([0, 1.3])

plt.tight_layout(); plt.savefig('report_dc.png'); plt.close()
print(f"   -> report_dc.png (Vout: {vout.min():.3f} to {vout.max():.3f}, swing={vout.max()-vout.min():.3f} Vpp)")

# ============================================================
# 3. TRANSIENT — rising + falling
# ============================================================
print("3. Transient...")
# tran_data2: wrdata v(vout) v(vinp) — 4 columns: time, vout, time, vinp
data = np.loadtxt("tran_data2")
if data.shape[1] == 4:
    time_us = data[:, 0] * 1e6
    vout_t = data[:, 1]
    vinp_t = data[:, 3]
elif data.shape[1] == 2:
    time_us = data[:, 0] * 1e6
    vout_t = data[:, 1]
    vinp_t = None

fig, ax = plt.subplots(1, 1, figsize=(11, 5))
ax.plot(time_us, vout_t, '#1a5276', linewidth=2, label='Vout')
if vinp_t is not None:
    ax.plot(time_us, vinp_t, '#c0392b', linewidth=1.2, linestyle='--', alpha=0.7, label='Vinp')
ax.set_xlabel('Time (us)', fontweight='bold')
ax.set_ylabel('Voltage (V)', fontweight='bold')
ax.set_title('Step Response — Rising & Falling (Unity-Gain, CL = 10 pF)', fontsize=13, fontweight='bold')
ax.legend(framealpha=0.9); ax.grid(True)
ax.set_xlim([0, max(time_us)])
plt.tight_layout(); plt.savefig('report_transient.png'); plt.close()
print("   -> report_transient.png")

# ============================================================
# 4. PSRR & CMRR — correct freq axis
# ============================================================
print("4. PSRR & CMRR...")
bode = np.loadtxt("bode_data")
freq_dm = bode[:, 0]; adm = bode[:, 1]

if os.path.exists("psrr_freq_data") and os.path.exists("cmrr_freq_data"):
    psrr_raw = np.loadtxt("psrr_freq_data")
    cmrr_raw = np.loadtxt("cmrr_freq_data")

    freq_ps = psrr_raw[:, 0]; avdd = psrr_raw[:, 1]
    freq_cm = cmrr_raw[:, 0]; acm = cmrr_raw[:, 1]

    # PSRR = Adm - Avdd, CMRR = Adm - Acm (interpolate Adm to each freq axis)
    psrr = np.interp(freq_ps, freq_dm, adm) - avdd
    cmrr = np.interp(freq_cm, freq_dm, adm) - acm

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    ax1.semilogx(freq_ps, psrr, '#2980b9', linewidth=2)
    ax1.axhline(y=50, color='#c0392b', linestyle='--', linewidth=1.5, label='Min: 50 dB')
    ax1.axvspan(100, 10000, alpha=0.08, color='#2ecc71')
    idx_1k = np.argmin(np.abs(freq_ps - 1000))
    ax1.plot(freq_ps[idx_1k], psrr[idx_1k], 'o', color='#c0392b', markersize=6, zorder=5)
    ax1.annotate(f'{psrr[idx_1k]:.1f} dB @ 1 kHz', xy=(freq_ps[idx_1k], psrr[idx_1k]),
                 xytext=(15, -15), textcoords='offset points', fontsize=9, fontweight='bold', color='#c0392b')
    ax1.set_xlabel('Frequency (Hz)', fontweight='bold')
    ax1.set_ylabel('PSRR (dB)', fontweight='bold')
    ax1.set_title('Power Supply Rejection Ratio', fontsize=12, fontweight='bold')
    ax1.legend(framealpha=0.9); ax1.grid(True, which='both')
    ax1.set_xlim([0.1, 1e9]); ax1.set_ylim([0, 140])

    ax2.semilogx(freq_cm, cmrr, '#8e44ad', linewidth=2)
    ax2.axhline(y=60, color='#c0392b', linestyle='--', linewidth=1.5, label='Min: 60 dB')
    ax2.axvspan(100, 10000, alpha=0.08, color='#2ecc71')
    idx_dc = np.argmin(np.abs(freq_cm - 1))
    ax2.plot(freq_cm[idx_dc], cmrr[idx_dc], 'o', color='#c0392b', markersize=6, zorder=5)
    ax2.annotate(f'{cmrr[idx_dc]:.1f} dB @ DC', xy=(freq_cm[idx_dc], cmrr[idx_dc]),
                 xytext=(15, -10), textcoords='offset points', fontsize=9, fontweight='bold', color='#c0392b')
    ax2.set_xlabel('Frequency (Hz)', fontweight='bold')
    ax2.set_ylabel('CMRR (dB)', fontweight='bold')
    ax2.set_title('Common-Mode Rejection Ratio', fontsize=12, fontweight='bold')
    ax2.legend(framealpha=0.9); ax2.grid(True, which='both')
    ax2.set_xlim([0.1, 1e9]); ax2.set_ylim([0, 140])

    plt.tight_layout(); plt.savefig('report_rejection.png'); plt.close()
    print("   -> report_rejection.png")

# ============================================================
# 5-7. Corners, Temperature, Dashboard (reuse from before — these were correct)
# ============================================================
print("5. Corners...")
corners = {}
for corner in ['tt', 'ss', 'ff', 'sf', 'fs']:
    tb = f"tb_corner_{corner}.spice"
    if os.path.exists(tb):
        out = run_spice(tb)
        gain = parse_meas(out, "gain_peak") or parse_meas(out, "gain_db")
        ugb = parse_meas(out, "ugb")
        corners[corner.upper()] = {"gain": gain, "ugb": ugb}

if len(corners) >= 3:
    names = list(corners.keys()); gains = [corners[n]["gain"] for n in names]
    ugbs = [corners[n]["ugb"]/1000 for n in names]
    colors = ['#2980b9', '#c0392b', '#27ae60', '#e67e22', '#8e44ad']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    bars1 = ax1.bar(names, gains, color=colors, alpha=0.85, edgecolor='white', linewidth=1.5)
    ax1.axhline(y=65, color='#c0392b', linestyle='--', linewidth=1.5, label='Target (65 dB)')
    ax1.axhline(y=60, color='#e67e22', linestyle=':', linewidth=1.5, label='Min (60 dB)')
    ax1.set_ylabel('DC Gain (dB)', fontweight='bold')
    ax1.set_title('Gain Across Process Corners', fontsize=12, fontweight='bold')
    ax1.legend(framealpha=0.9); ax1.grid(True, axis='y'); ax1.set_ylim([0, max(gains)*1.15])
    for bar, val in zip(bars1, gains):
        ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    bars2 = ax2.bar(names, ugbs, color=colors, alpha=0.85, edgecolor='white', linewidth=1.5)
    ax2.axhline(y=30, color='#c0392b', linestyle='--', linewidth=1.5, label='Min (30 kHz)')
    ax2.set_ylabel('UGB (kHz)', fontweight='bold')
    ax2.set_title('Unity-Gain Bandwidth Across Corners', fontsize=12, fontweight='bold')
    ax2.legend(framealpha=0.9); ax2.grid(True, axis='y'); ax2.set_ylim([0, max(ugbs)*1.25])
    for bar, val in zip(bars2, ugbs):
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.tight_layout(); plt.savefig('report_corners.png'); plt.close()
    print("   -> report_corners.png")

print("6. Temperature...")
temps = {}
for t in ['-40', '27', '85']:
    tb = f"tb_temp_{t}.spice"
    if os.path.exists(tb):
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

print("\nDone — all plots from live simulations.")
