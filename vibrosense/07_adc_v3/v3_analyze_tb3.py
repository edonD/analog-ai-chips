#!/usr/bin/env python3
"""
v3_analyze_tb3.py — DNL/INL Analysis from Code Density
Post-processes ngspice wrdata output from TB3 (slow ramp, 2048+ conversions)

Usage: python3 v3_analyze_tb3.py v3_tb3_dnl_inl.dat
"""

import numpy as np
import sys
from v3_parse_codes import load_and_extract_codes


def compute_dnl_inl(codes, nbits=8):
    """Compute DNL and INL from code histogram."""
    n_codes = 2**nbits  # 256
    hist = np.zeros(n_codes, dtype=int)
    for c in codes:
        if 0 <= c < n_codes:
            hist[c] += 1

    # DNL/INL computed over inner codes (1..254), excluding partial end bins
    inner = hist[1:n_codes-1].astype(float)  # codes 1..254 = 254 bins
    total_inner = np.sum(inner)
    H_ideal = total_inner / len(inner)

    dnl = inner / H_ideal - 1.0
    inl = np.cumsum(dnl)
    # Center INL (remove best-fit line endpoint offset)
    inl = inl - np.linspace(inl[0], inl[-1], len(inl))

    missing = np.where(inner == 0)[0] + 1  # +1 offset for code number

    return hist, dnl, inl, missing, H_ideal


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 v3_analyze_tb3.py <wrdata_file>")
        sys.exit(1)

    codes = load_and_extract_codes(sys.argv[1])

    if len(codes) < 256:
        print(f"ERROR: Only {len(codes)} conversions found, need at least 256")
        sys.exit(1)

    print(f"\n=== TB3: DNL/INL Analysis ===")
    print(f"Total conversions: {len(codes)}")
    print(f"Code range: {codes.min()} to {codes.max()}")

    hist, dnl, inl, missing, H_ideal = compute_dnl_inl(codes)

    print(f"Ideal hits per bin: {H_ideal:.2f}")
    print(f"\nHistogram (first/last 10 codes):")
    for i in range(10):
        print(f"  Code {i:3d}: {hist[i]:4d} hits")
    print(f"  ...")
    for i in range(246, 256):
        print(f"  Code {i:3d}: {hist[i]:4d} hits")

    print(f"\n--- DNL Results ---")
    print(f"Max DNL:  {np.max(dnl):+.4f} LSB (at code {np.argmax(dnl)+1})")
    print(f"Min DNL:  {np.min(dnl):+.4f} LSB (at code {np.argmin(dnl)+1})")
    print(f"Max |DNL|: {np.max(np.abs(dnl)):.4f} LSB")
    print(f"Target: < 0.5 LSB → {'PASS' if np.max(np.abs(dnl)) < 0.5 else 'FAIL'}")

    print(f"\n--- INL Results ---")
    print(f"Max INL:  {np.max(inl):+.4f} LSB (at code {np.argmax(inl)+1})")
    print(f"Min INL:  {np.min(inl):+.4f} LSB (at code {np.argmin(inl)+1})")
    print(f"Max |INL|: {np.max(np.abs(inl)):.4f} LSB")
    print(f"Target: < 0.5 LSB → {'PASS' if np.max(np.abs(inl)) < 0.5 else 'FAIL'}")

    print(f"\n--- Missing Codes ---")
    if len(missing) == 0:
        print(f"Missing codes: 0 → PASS")
    else:
        print(f"Missing codes: {len(missing)} → FAIL")
        print(f"  Codes with zero hits: {missing.tolist()}")

    # Summary for README
    print(f"\n=== Summary for README ===")
    print(f"Total conversions: {len(codes)}")
    print(f"Max |DNL|: {np.max(np.abs(dnl)):.3f} LSB {'PASS' if np.max(np.abs(dnl)) < 0.5 else 'FAIL'}")
    print(f"Max |INL|: {np.max(np.abs(inl)):.3f} LSB {'PASS' if np.max(np.abs(inl)) < 0.5 else 'FAIL'}")
    print(f"Missing codes: {len(missing)} {'PASS' if len(missing)==0 else 'FAIL'}")


if __name__ == "__main__":
    main()
