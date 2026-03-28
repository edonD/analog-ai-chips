#!/usr/bin/env python3
"""Generate all required plots for Block 00: Error Amplifier.

All data comes from actual simulation output files:
- ac_gain.dat: Bode gain/phase
- swing.dat: Output swing
- psrr.dat: PSRR vs frequency
- noise_spectral.dat: Input-referred noise spectral density
- run.log: PVT corner results
"""

import re
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))

plt.rcParams.update({
    'figure.dpi': 150,
    'font.size': 11,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'lines.linewidth': 1.5,
})


def parse_pvt_results(log_path='run.log'):
    """Parse PVT results from run.log.
    Returns list of (corner, temp, gain, pm, ugb) tuples.
    Deduplicates (keeps first occurrence of each corner/temp pair).
    """
    results = []
    seen = set()
    pattern = re.compile(
        r'^PVT\s+(\w+)\s+(-?\d+)\s+C:\s+gain=([\d.]+)\s+dB,\s+PM=([\d.]+)\s+deg,\s+UGB=([\d.]+)\s+kHz'
    )
    try:
        with open(log_path) as f:
            for line in f:
                m = pattern.match(line.strip())
                if m:
                    corner = m.group(1)
                    temp = int(m.group(2))
                    key = (corner, temp)
                    if key not in seen:
                        seen.add(key)
                        results.append((
                            corner, temp,
                            float(m.group(3)),
                            float(m.group(4)),
                            float(m.group(5)),
                        ))
    except FileNotFoundError:
        pass
    return results


def extract_from_log(log_path, key):
    """Extract a numeric value from run.log by key prefix."""
    try:
        with open(log_path) as f:
            for line in f:
                s = line.strip()
                if s.startswith(key):
                    after = s[len(key):].lstrip(':').strip()
                    try:
                        return float(after.split()[0])
                    except (ValueError, IndexError):
                        pass
    except FileNotFoundError:
        pass
    return None


# ── Bode: gain and phase vs frequency ─────────────────────────────────
def plot_bode():
    d = np.loadtxt('ac_gain.dat')
    freq = d[:, 0]
    gain = d[:, 1]
    phase = d[:, 3]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.suptitle('Open-Loop Bode Plot -- Error Amplifier (TT 27C)', fontweight='bold')

    ax1.semilogx(freq, gain, 'b-')
    ax1.set_ylabel('Gain (dB)')
    ax1.axhline(0, color='k', ls='--', lw=0.8)
    # Mark DC gain
    ax1.annotate(f'DC gain = {gain[0]:.1f} dB', xy=(freq[0], gain[0]),
                 xytext=(freq[5]*10, gain[0]-8), fontsize=10,
                 arrowprops=dict(arrowstyle='->', color='blue'))

    # Find UGB
    idx_ugb = np.argmin(np.abs(gain))
    if idx_ugb > 0:
        ugb_khz = freq[idx_ugb] / 1e3
        ax1.axvline(freq[idx_ugb], color='r', ls=':', lw=0.8,
                     label=f'UGB = {ugb_khz:.0f} kHz')
        ax1.legend(loc='upper right')

        # Annotate gain slope at UGB
        slope = extract_from_log('run.log', 'gain_slope_dBdec:')
        if slope is not None:
            ax1.annotate(f'Slope = {slope:.1f} dB/dec',
                         xy=(freq[idx_ugb], 0),
                         xytext=(freq[idx_ugb]*3, 15), fontsize=9,
                         arrowprops=dict(arrowstyle='->', color='darkgreen'),
                         color='darkgreen')

    ax2.semilogx(freq, phase, 'r-')
    ax2.set_ylabel('Phase (deg)')
    ax2.set_xlabel('Frequency (Hz)')

    # PM target band
    ax2.axhspan(-180 + 60, -180 + 80, alpha=0.15, color='green', label='PM target [60, 80] deg')

    # Mark phase margin at UGB
    if idx_ugb > 0:
        pm = 180 + phase[idx_ugb]
        ax2.axvline(freq[idx_ugb], color='r', ls=':', lw=0.8)
        ax2.axhline(-180, color='k', ls='--', lw=0.8)
        ax2.annotate(f'PM = {pm:.1f} deg', xy=(freq[idx_ugb], phase[idx_ugb]),
                     xytext=(freq[idx_ugb]*5, phase[idx_ugb]+15), fontsize=10,
                     arrowprops=dict(arrowstyle='->', color='red'))
    ax2.legend(loc='lower left')

    plt.tight_layout()
    plt.savefig('bode_gain_phase.png', bbox_inches='tight')
    plt.close()
    print('  bode_gain_phase.png')


# ── Output swing ──────────────────────────────────────────────────────
def plot_swing():
    d = np.loadtxt('swing.dat')
    vin = d[:, 0]
    vout = d[:, 1]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(vin, vout, 'b-')
    ax.set_xlabel('Feedback Input Voltage (V)')
    ax.set_ylabel('Output Voltage (V)')
    ax.set_title('Output Swing -- Vout vs Input DC Sweep', fontweight='bold')
    ax.axhline(0.5, color='r', ls='--', lw=0.8, label='Swing low spec (0.5 V)')
    ax.axhline(4.5, color='orange', ls='--', lw=0.8, label='Swing high spec (4.5 V)')
    ax.legend()
    plt.tight_layout()
    plt.savefig('output_swing.png', bbox_inches='tight')
    plt.close()
    print('  output_swing.png')


# ── PSRR vs frequency ────────────────────────────────────────────────
def plot_psrr():
    d = np.loadtxt('psrr.dat')
    freq = d[:, 0]
    psrr = d[:, 1]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.semilogx(freq, psrr, 'g-')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Supply-to-Output Gain (dB)')
    ax.set_title('Power Supply Rejection vs Frequency', fontweight='bold')
    ax.annotate(f'DC = {psrr[0]:.1f} dB', xy=(freq[0], psrr[0]),
                xytext=(freq[5]*10, psrr[0]+5), fontsize=10,
                arrowprops=dict(arrowstyle='->', color='green'))
    ax.legend()
    plt.tight_layout()
    plt.savefig('psrr_vs_freq.png', bbox_inches='tight')
    plt.close()
    print('  psrr_vs_freq.png')


# ── Noise spectral density ───────────────────────────────────────────
def plot_noise():
    noise_file = 'noise_spectral.dat'
    has_data = False
    if os.path.exists(noise_file) and os.path.getsize(noise_file) > 0:
        try:
            d = np.loadtxt(noise_file)
            if d.ndim == 2 and d.shape[0] > 5:
                freq = d[:, 0]
                # inoise_spectrum is in V/sqrt(Hz), convert to nV/sqrt(Hz)
                noise_nv = d[:, 1] * 1e9
                if np.any(noise_nv > 0):
                    has_data = True
        except Exception:
            pass

    fig, ax = plt.subplots(figsize=(9, 5))
    if has_data:
        ax.loglog(freq, noise_nv, 'purple')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Input-Referred Noise (nV/sqrt(Hz))')
        ax.set_title('Input-Referred Noise Spectral Density (Simulated)', fontweight='bold')

        # Get integrated noise
        inoise = extract_from_log('run.log', 'inoise_total_uVrms:')
        note = 'Note: SKY130 HV device models produce "conductance reset" warnings\n'
        note += 'during noise analysis, which may inflate high-frequency noise.'
        if inoise is not None:
            note += f'\nIntegrated input-referred noise (10 Hz - 1 MHz): {inoise:.1f} uVrms'
        ax.text(0.5, 0.02, note,
                transform=ax.transAxes, ha='center', va='bottom', fontsize=8,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    else:
        ax.text(0.5, 0.5, 'NO DATA -- noise simulation failed or produced no output',
                transform=ax.transAxes, ha='center', va='center', fontsize=14,
                bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='red', lw=2))
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Input-Referred Noise (nV/sqrt(Hz))')
        ax.set_title('Input-Referred Noise Spectral Density', fontweight='bold')

    plt.tight_layout()
    plt.savefig('noise_spectral.png', bbox_inches='tight')
    plt.close()
    print('  noise_spectral.png')


# ── PVT gain ─────────────────────────────────────────────────────────
def plot_pvt_gain():
    pvt = parse_pvt_results()
    if not pvt:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(0.5, 0.5, 'NO DATA -- PVT simulation failed',
                transform=ax.transAxes, ha='center', va='center', fontsize=14,
                bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='red', lw=2))
        ax.set_title('DC Gain Across PVT Corners', fontweight='bold')
        plt.savefig('pvt_gain.png', bbox_inches='tight')
        plt.close()
        print('  pvt_gain.png (NO DATA)')
        return

    # Group by corner
    corners_order = ['tt', 'ss', 'ff', 'sf', 'fs']
    temps_order = [-40, 27, 150]
    colors = {'tt': '#2196F3', 'ss': '#FF5722', 'ff': '#4CAF50', 'sf': '#9C27B0', 'fs': '#FF9800'}

    labels = []
    gains = []
    bar_colors = []
    for corner in corners_order:
        for temp in temps_order:
            for c, t, g, p, u in pvt:
                if c == corner and t == temp:
                    labels.append(f'{corner.upper()}\n{temp}C')
                    gains.append(g)
                    bar_colors.append(colors.get(corner, '#999'))
                    break

    fig, ax = plt.subplots(figsize=(14, 5))
    x = np.arange(len(labels))
    bars = ax.bar(x, gains, color=bar_colors, width=0.7, edgecolor='black', lw=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('DC Gain (dB)')
    ax.set_title(f'DC Gain Across All {len(gains)} PVT Corners', fontweight='bold')
    ax.axhline(60, color='r', ls='--', lw=1.2, label='Spec min (60 dB)')
    ax.set_ylim(min(gains) - 5, max(gains) + 5)
    for bar, val in zip(bars, gains):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{val:.1f}', ha='center', fontsize=7, fontweight='bold')
    ax.legend()
    plt.tight_layout()
    plt.savefig('pvt_gain.png', bbox_inches='tight')
    plt.close()
    print('  pvt_gain.png')


# ── PVT phase margin ─────────────────────────────────────────────────
def plot_pvt_pm():
    pvt = parse_pvt_results()
    if not pvt:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(0.5, 0.5, 'NO DATA -- PVT simulation failed',
                transform=ax.transAxes, ha='center', va='center', fontsize=14,
                bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='red', lw=2))
        ax.set_title('Phase Margin Across PVT Corners', fontweight='bold')
        plt.savefig('pvt_pm.png', bbox_inches='tight')
        plt.close()
        print('  pvt_pm.png (NO DATA)')
        return

    corners_order = ['tt', 'ss', 'ff', 'sf', 'fs']
    temps_order = [-40, 27, 150]
    colors = {'tt': '#2196F3', 'ss': '#FF5722', 'ff': '#4CAF50', 'sf': '#9C27B0', 'fs': '#FF9800'}

    labels = []
    pms = []
    bar_colors = []
    for corner in corners_order:
        for temp in temps_order:
            for c, t, g, p, u in pvt:
                if c == corner and t == temp:
                    labels.append(f'{corner.upper()}\n{temp}C')
                    pms.append(p)
                    bar_colors.append(colors.get(corner, '#999'))
                    break

    fig, ax = plt.subplots(figsize=(14, 5))
    x = np.arange(len(labels))
    bars = ax.bar(x, pms, color=bar_colors, width=0.7, edgecolor='black', lw=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('Phase Margin (deg)')
    ax.set_title(f'Phase Margin Across All {len(pms)} PVT Corners', fontweight='bold')

    # Target band [60, 80]
    ax.axhspan(60, 80, alpha=0.15, color='green', label='Target band [60, 80] deg')
    ax.axhline(55, color='r', ls='--', lw=1.2, label='PVT pass min (55 deg)')
    ax.set_ylim(0, max(pms) + 10)
    for bar, val in zip(bars, pms):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.1f}', ha='center', fontsize=7, fontweight='bold')
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('pvt_pm.png', bbox_inches='tight')
    plt.close()
    print('  pvt_pm.png')


if __name__ == '__main__':
    print('Generating plots...')
    plot_bode()
    plot_swing()
    plot_psrr()
    plot_noise()
    plot_pvt_gain()
    plot_pvt_pm()
    print('Done -- all plots generated.')
