#!/usr/bin/env python3
"""
v3_parse_codes.py — Parse ngspice wrdata output and extract ADC codes.
Shared by TB3 and TB4 analysis scripts.

wrdata format: pairs of (time, value) for each signal.
Signals: d7, d6, d5, d4, d3, d2, d1, d0, valid = 9 signals = 18 columns
"""

import numpy as np
import sys


def load_and_extract_codes(filename, threshold=0.9):
    """Load wrdata file and extract ADC output codes at each valid pulse.

    Returns: array of integer codes (0-255), one per conversion.
    """
    print(f"Loading {filename}...")

    # Parse line-by-line for memory efficiency (file may be large)
    codes = []
    prev_valid = False
    code_at_valid = None
    lines_read = 0

    with open(filename) as f:
        for line in f:
            lines_read += 1
            parts = line.split()
            if len(parts) < 18:
                continue

            try:
                # Extract bit values (columns 1,3,5,7,9,11,13,15) and valid (col 17)
                bits = [float(parts[2*i + 1]) for i in range(8)]
                valid_val = float(parts[17])
            except (ValueError, IndexError):
                continue

            is_valid = valid_val > threshold

            if is_valid and not prev_valid:
                # Rising edge of valid — decode the code
                code = 0
                for bit_num in range(8):
                    if bits[bit_num] > threshold:
                        code += (1 << (7 - bit_num))
                codes.append(code)

            prev_valid = is_valid

    codes = np.array(codes, dtype=int)
    print(f"  Read {lines_read} data points, found {len(codes)} conversions")
    return codes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 v3_parse_codes.py <wrdata_file>")
        sys.exit(1)

    codes = load_and_extract_codes(sys.argv[1])
    print(f"  Code range: {codes.min()} to {codes.max()}")
    print(f"  First 10 codes: {codes[:10]}")
    print(f"  Last 10 codes: {codes[-10:]}")
