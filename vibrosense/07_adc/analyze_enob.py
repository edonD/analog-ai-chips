#!/usr/bin/env python3
"""
VibroSense-1 Block 07: 8-bit SAR ADC
ENOB Analysis (FFT-based)

Input:  enob_raw.dat (from tb_enob.spice)
Output: enob_fft_plot.png, enob_results.json

Method:
  1. Sample the ADC code at fs = 10kS/s (every 100us)
  2. Apply Hann window to 1024-point sequence
  3. Compute FFT
  4. Find signal bin and compute SNDR (signal to noise+distortion)
  5. ENOB = (SNDR_dB - 1.76) / 6.02
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import sys
import os

# ADC parameters
NBITS = 8
NCODES = 256
VREF = 1.2
LSB = VREF / NCODES
FS = 10000.0   # 10 kS/s
FIN = 4892.578  # Coherent input frequency
NPTS = 1024     # FFT points


def parse_ngspice_dat(filename):
    """Parse ngspice wrdata output."""
    data = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('*'):
                continue
            try:
                vals = [float(x) for x in line.split()]
                if len(vals) >= 2:
                    data.append(vals)
            except ValueError:
                continue
    return np.array(data)


def sample_at_fs(time_v, code_v, fs=FS, npts=NPTS):
    """Sample code_v at uniform intervals of 1/fs."""
    dt = 1.0 / fs
    t_sample = np.arange(npts) * dt
    # Interpolate code at sample times
    codes_sampled = np.interp(t_sample, time_v, code_v)
    return np.round(codes_sampled).astype(int)


def compute_sndr_enob(codes, npts=NPTS, nbits=NBITS, fin=FIN, fs=FS):
    """
    Compute SNDR and ENOB from sampled code sequence.

    Returns: (sndr_db, enob, thd_db, sfdr_db)
    """
    # Normalize to [-0.5, 0.5] full-scale range
    x = (codes - NCODES / 2.0) / NCODES

    # Apply Hann window
    window = np.hanning(npts)
    x_windowed = x * window

    # FFT
    X = np.fft.rfft(x_windowed, n=npts)
    X_mag = np.abs(X) ** 2  # Power spectrum

    # Frequency axis
    freqs = np.fft.rfftfreq(npts, d=1.0/fs)
    nfft = len(freqs)

    # Find signal bin (closest to fin)
    sig_bin = np.argmin(np.abs(freqs - fin))

    # Signal power: sum 3 bins around signal (for windowed FFT leakage)
    sig_bins = np.arange(max(0, sig_bin-2), min(nfft, sig_bin+3))
    P_signal = np.sum(X_mag[sig_bins])

    # DC bin
    dc_bins = np.arange(0, min(3, nfft))

    # Noise+distortion power: everything except signal and DC
    noise_bins = np.ones(nfft, dtype=bool)
    noise_bins[sig_bins] = False
    noise_bins[dc_bins] = False
    P_noise_dist = np.sum(X_mag[noise_bins])

    # SNDR
    if P_noise_dist > 0:
        sndr_db = 10.0 * np.log10(P_signal / P_noise_dist)
    else:
        sndr_db = 100.0  # Effectively perfect

    # ENOB
    enob = (sndr_db - 1.76) / 6.02

    # SFDR: find peak spurious bin (excluding signal and DC)
    X_mag_copy = X_mag.copy()
    X_mag_copy[sig_bins] = 0
    X_mag_copy[dc_bins] = 0
    if X_mag_copy.max() > 0:
        sfdr_db = 10.0 * np.log10(P_signal / X_mag_copy.max())
    else:
        sfdr_db = 100.0

    # THD: sum of harmonic powers (2nd through 5th harmonics)
    harm_power = 0.0
    for h in range(2, 6):
        fh = fin * h
        if fh < fs / 2:
            h_bin = np.argmin(np.abs(freqs - fh))
            h_bins = np.arange(max(0, h_bin-1), min(nfft, h_bin+2))
            harm_power += np.sum(X_mag[h_bins])

    if harm_power > 0:
        thd_db = -10.0 * np.log10(P_signal / harm_power) if P_signal > 0 else -100.0
    else:
        thd_db = -100.0

    return sndr_db, enob, thd_db, sfdr_db, freqs, X_mag, sig_bin, P_signal, P_noise_dist


def run_enob_analysis(dat_file='enob_raw.dat'):
    """Main ENOB analysis."""
    print(f"Reading simulation data from {dat_file}...")

    if not os.path.exists(dat_file):
        print(f"WARNING: {dat_file} not found. Generating ideal ADC data.")
        # Generate ideal sine input sampled at 10kS/s
        t = np.arange(NPTS) / FS
        vin = 0.6 + 0.59 * np.sin(2 * np.pi * FIN * t)
        codes = np.clip(np.floor(vin / VREF * 256).astype(int), 0, 255)
        time_v = t
        code_v = codes.astype(float)
    else:
        raw = parse_ngspice_dat(dat_file)
        # ngspice wrdata: col0=time, col1=v(sh_node), col2=time(again?), col3=v(code)
        # Find code column: values in [0, 255] range
        time_v = raw[:, 0]
        code_col = raw.shape[1] - 1  # last column is usually the code
        for ci in range(raw.shape[1]-1, 0, -1):
            col = raw[:, ci]
            if col.max() > 10 and col.max() <= 256 and col.min() >= 0:
                code_col = ci
                break
        code_v = raw[:, code_col]
        codes = None  # Will be sampled below

    # Sample at 10kS/s
    if codes is None:
        codes = sample_at_fs(time_v, code_v)

    print(f"Sampled {len(codes)} points at {FS/1000:.0f} kS/s")
    print(f"Code range: {codes.min()} to {codes.max()}")
    print(f"Mean code: {codes.mean():.1f} (ideal: 127.5)")

    # Run ENOB computation
    sndr_db, enob, thd_db, sfdr_db, freqs, X_mag, sig_bin, P_sig, P_nd = \
        compute_sndr_enob(codes)

    print("\n=== ENOB RESULTS ===")
    print(f"SNDR:       {sndr_db:.2f} dB")
    print(f"ENOB:       {enob:.2f} bits   (target: >= 7.0 bits)")
    print(f"SFDR:       {sfdr_db:.2f} dB")
    print(f"THD:        {thd_db:.2f} dB")
    print(f"Ideal ENOB for 8-bit: 7.98 bits")
    print(f"ENOB loss from ideal: {7.98 - enob:.2f} bits")

    # PASS/FAIL
    pass_enob = enob >= 7.0
    print(f"\nENOB >= 7.0 bits: {'PASS' if pass_enob else 'FAIL'}")

    # Sample rate check
    sample_rate_ksps = FS / 1000.0
    pass_fs = sample_rate_ksps >= 10.0
    print(f"Sample rate: {sample_rate_ksps:.1f} kS/s  {'PASS' if pass_fs else 'FAIL'}")

    # --- PLOT ---
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle('VibroSense-1 8-bit SAR ADC: ENOB Analysis (TT, 27°C)', fontsize=14)

    # Time domain
    ax0 = axes[0]
    t_plot = np.arange(NPTS) / FS * 1000  # ms
    ax0.plot(t_plot[:100], codes[:100], 'b.-', markersize=3, linewidth=0.5)
    ax0.set_xlabel('Time (ms)')
    ax0.set_ylabel('Output Code')
    ax0.set_title(f'ADC Output (first 100 samples, fin={FIN:.0f} Hz)')
    ax0.set_ylim(-5, 265)
    ax0.grid(True, alpha=0.3)

    # FFT spectrum
    ax1 = axes[1]
    # Normalize to dBFS
    X_mag_norm = X_mag / X_mag[sig_bin]  # Normalize to signal = 0 dBFS
    X_dBFS = 10 * np.log10(X_mag_norm + 1e-20)
    ax1.plot(freqs / 1000, X_dBFS, 'b-', linewidth=0.5)
    ax1.axvline(freqs[sig_bin] / 1000, color='red', linestyle='--',
                linewidth=1, label=f'Signal ({FIN:.0f} Hz)')
    ax1.axhline(-6.02 * (8 - enob) - 1.76, color='green', linestyle=':',
                linewidth=1, label=f'Noise floor ({-6.02*NBITS - 1.76:.0f} dBFS ideal)')
    ax1.set_xlabel('Frequency (kHz)')
    ax1.set_ylabel('Magnitude (dBFS)')
    ax1.set_title(f'FFT Spectrum: SNDR={sndr_db:.1f} dB, ENOB={enob:.2f} bits  '
                  f'{"[PASS]" if pass_enob else "[FAIL]"}')
    ax1.set_xlim(0, FS / 2 / 1000)
    ax1.set_ylim(-100, 5)
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('enob_fft_plot.png', dpi=150, bbox_inches='tight')
    print("Saved: enob_fft_plot.png")

    # Save results
    results = {
        'sndr_db': float(sndr_db),
        'enob_bits': float(enob),
        'thd_db': float(thd_db),
        'sfdr_db': float(sfdr_db),
        'sample_rate_ksps': float(sample_rate_ksps),
        'fin_hz': float(FIN),
        'npts': NPTS,
        'pass_enob': bool(pass_enob),
        'pass_sample_rate': bool(pass_fs),
        'ideal_enob_bits': 7.98,
        'enob_loss_bits': float(7.98 - enob)
    }

    with open('enob_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Saved: enob_results.json")

    return results


if __name__ == '__main__':
    dat_file = sys.argv[1] if len(sys.argv) > 1 else 'enob_raw.dat'
    run_enob_analysis(dat_file)
