#!/usr/bin/env python3
"""
v3_analyze_tb4.py — ENOB via FFT from Coherent Sine
Post-processes ngspice wrdata output from TB4

Usage: python3 v3_analyze_tb4.py v3_tb4_enob.dat
"""

import numpy as np
import sys
from v3_parse_codes import load_and_extract_codes


def compute_enob(codes, M=89, N=1024, nbits=8):
    """Compute ENOB from FFT of coherent-sampled codes.

    Args:
        codes: array of ADC output codes
        M: number of signal cycles in N samples (prime)
        N: FFT length (number of samples)
        nbits: ADC resolution

    Returns: ENOB, SNDR, SFDR, THD, power_spectrum
    """
    if len(codes) < N:
        raise ValueError(f"Need at least {N} codes, got {len(codes)}")

    x = codes[:N].astype(float)

    # Remove DC
    x_ac = x - np.mean(x)

    # FFT (no windowing for coherent sampling)
    X = np.fft.rfft(x_ac)
    P = np.abs(X)**2 / N  # normalize by N

    # Signal power at bin M
    P_signal = P[M]

    # Find harmonics (up to 7th)
    harmonics = []
    for h in range(2, 8):
        hbin = (h * M) % N
        if hbin > N // 2:
            hbin = N - hbin
        harmonics.append(hbin)

    # Total harmonic distortion
    P_harmonics = sum(P[hbin] for hbin in harmonics if hbin != M and hbin != 0)

    # Noise + distortion: everything except DC and signal
    P_nd = np.sum(P[1:]) - P_signal  # exclude DC bin

    if P_nd <= 0 or P_signal <= 0:
        return 0, 0, 0, 0, P

    SNDR = 10 * np.log10(P_signal / P_nd)
    ENOB = (SNDR - 1.76) / 6.02

    # SFDR: signal to largest spur
    P_copy = P.copy()
    P_copy[0] = 0  # exclude DC
    P_copy[M] = 0  # exclude signal
    P_spur = np.max(P_copy)
    if P_spur > 0:
        SFDR = 10 * np.log10(P_signal / P_spur)
    else:
        SFDR = float('inf')

    # THD
    if P_harmonics > 0:
        THD = 10 * np.log10(P_harmonics / P_signal)
    else:
        THD = -float('inf')

    return ENOB, SNDR, SFDR, THD, P


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 v3_analyze_tb4.py <wrdata_file>")
        sys.exit(1)

    M = 43    # Signal cycles (prime)
    N = 512   # FFT length
    fs = 500e3  # Sample rate (500 kSPS at 5MHz clock)
    fin = fs * M / N

    codes = load_and_extract_codes(sys.argv[1])

    if len(codes) < N:
        print(f"ERROR: Only {len(codes)} conversions found, need at least {N}")
        sys.exit(1)

    # Skip first few conversions (startup transient)
    skip = min(10, len(codes) - N)
    codes_fft = codes[skip:skip+N]

    print(f"\n=== TB4: ENOB via FFT ===")
    print(f"FFT length N = {N}")
    print(f"Signal cycles M = {M} (prime)")
    print(f"Sample rate fs = {fs/1e3:.1f} kSPS")
    print(f"Signal freq fin = {fin:.2f} Hz")
    print(f"Total conversions available: {len(codes)}")
    print(f"Using conversions {skip} to {skip+N}")
    print(f"Code range: {codes_fft.min()} to {codes_fft.max()}")
    print(f"Code mean: {codes_fft.mean():.1f}, std: {codes_fft.std():.1f}")

    ENOB, SNDR, SFDR, THD, P = compute_enob(codes_fft, M=M, N=N)

    print(f"\n--- FFT Results ---")
    print(f"SNDR:  {SNDR:.2f} dB")
    print(f"ENOB:  {ENOB:.2f} bits")
    print(f"SFDR:  {SFDR:.2f} dB")
    print(f"THD:   {THD:.2f} dB")
    print(f"\nTarget ENOB >= 7.0 bits → {'PASS' if ENOB >= 7.0 else 'FAIL'}")

    # Full-scale sine theoretical SNDR for N-bit ideal ADC: 6.02*N + 1.76
    ideal_sndr = 6.02 * 8 + 1.76
    print(f"\nIdeal 8-bit SNDR: {ideal_sndr:.2f} dB (ENOB = 8.00)")
    print(f"Actual vs ideal:  {SNDR - ideal_sndr:+.2f} dB ({ENOB - 8:.2f} bits)")

    # Summary
    print(f"\n=== Summary for README ===")
    print(f"ENOB: {ENOB:.2f} bits {'PASS' if ENOB >= 7.0 else 'FAIL'} (target >= 7.0)")
    print(f"SNDR: {SNDR:.2f} dB")
    print(f"SFDR: {SFDR:.2f} dB")


if __name__ == "__main__":
    main()
