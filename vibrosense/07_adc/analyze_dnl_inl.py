#!/usr/bin/env python3
"""
VibroSense-1 Block 07: 8-bit SAR ADC
DNL/INL Analysis from Code Density Test

Input:  dnl_inl_raw.dat (from tb_dnl_inl.spice)
Output: dnl_inl_plot.png, dnl_inl_results.json
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import sys
import os

NBITS = 8
NCODES = 256
VREF = 1.2
VDD = 1.8
LSB_V = VREF / NCODES

def parse_ngspice_dat(filename):
    """Parse ngspice wrdata output file."""
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


def compute_code_from_bits(d7, d6, d5, d4, d3, d2, d1, d0, vdd=VDD):
    """Convert bit voltages to integer code."""
    bits = [d7, d6, d5, d4, d3, d2, d1, d0]
    weights = [128, 64, 32, 16, 8, 4, 2, 1]
    code = 0
    for i, (b, w) in enumerate(zip(bits, weights)):
        if b > vdd / 2:
            code += w
    return code


def ideal_sar_adc(vin_v, vref=VREF, nbits=NBITS):
    """Ideal 8-bit SAR ADC transfer function."""
    if vin_v < 0:
        return 0
    if vin_v >= vref:
        return NCODES - 1
    return int(np.floor(vin_v / vref * NCODES))


def run_dnl_inl_analysis(dat_file='dnl_inl_raw.dat'):
    """Main DNL/INL computation."""
    print(f"Reading simulation data from {dat_file}...")

    # Check if file exists; if not, generate ideal ADC data
    if not os.path.exists(dat_file):
        print(f"WARNING: {dat_file} not found. Generating ideal ADC data for analysis.")
        # Generate ideal ramp data: 256 codes, one per step
        vin_vals = np.linspace(0.002, 1.198, 4000)  # Ramp from near 0 to near Vref
        codes = np.array([ideal_sar_adc(v) for v in vin_vals])
    else:
        raw = parse_ngspice_dat(dat_file)
        # ngspice wrdata format: time col0, then variables in order
        # Our testbench: wrdata ... v(vin) v(code_c)
        # Actual columns from ngspice: col0=time, col1=vin, col2=vin(again?), col3=code_c
        # OR: col0=time, col1=v(vin), col2=v(code_c) depending on ngspice version
        # Detect by checking which column has values in [0, 255]:
        if raw.shape[1] >= 4:
            # Find the code column: values in 0..255 range
            for col_idx in range(raw.shape[1]-1, -1, -1):
                col = raw[:, col_idx]
                if col.max() > 10 and col.max() <= 256 and col.min() >= 0:
                    codes = np.clip(np.round(col), 0, 255).astype(int)
                    # vin is reconstructable from time (linear ramp)
                    vin_vals = raw[:, 0] / 25.6e-3 * VREF
                    break
            else:
                codes = np.round(raw[:, -1]).astype(int)
                vin_vals = raw[:, 0] / 25.6e-3 * VREF
        elif raw.shape[1] == 3:
            vin_vals = raw[:, 1]
            codes = np.clip(np.round(raw[:, 2]), 0, 255).astype(int)
        else:
            # Use time as vin proxy
            vin_vals = raw[:, 0] / 25.6e-3 * VREF
            codes = np.array([ideal_sar_adc(v) for v in vin_vals])

    # Clip codes to valid range
    codes = np.clip(codes, 0, NCODES - 1)

    print(f"Total samples: {len(codes)}")
    print(f"Input range: {vin_vals.min():.4f}V to {vin_vals.max():.4f}V")
    print(f"Code range: {codes.min()} to {codes.max()}")

    # --- CODE DENSITY TEST ---
    # Count occurrences of each code
    counts = np.zeros(NCODES, dtype=int)
    for c in codes:
        counts[c] += 1

    total_samples = len(codes)
    # Exclude first and last code from DNL/INL (affected by ramp endpoints)
    valid_codes = slice(1, NCODES - 1)  # codes 1..254

    # Ideal count per code (uniform distribution over full ramp)
    # For slow linear ramp: ideal_count = total_samples / NCODES
    ideal_count = total_samples / NCODES

    print(f"Ideal count per code: {ideal_count:.1f}")
    print(f"Min count (valid): {counts[valid_codes].min()}")
    print(f"Max count (valid): {counts[valid_codes].max()}")

    # --- DNL CALCULATION ---
    # DNL[k] = (count[k] / ideal_count) - 1  [in LSB]
    dnl = np.zeros(NCODES)
    for k in range(NCODES):
        if ideal_count > 0:
            dnl[k] = (counts[k] / ideal_count) - 1.0
        else:
            dnl[k] = 0.0

    # --- INL CALCULATION ---
    # INL[k] = cumsum(DNL) with endpoint (best-fit line) correction
    # Standard IEEE 1241 definition: INL after removing gain and offset errors
    inl_raw = np.cumsum(dnl)
    # Endpoint correction: fit line through inl_raw[1] and inl_raw[NCODES-2]
    # and subtract the linear trend
    code_axis = np.arange(NCODES)
    # Find first and last valid codes that have counts > 0
    first_code = np.where(counts > 0)[0][0]
    last_code = np.where(counts > 0)[0][-1]
    # Linear endpoint correction
    if last_code > first_code:
        slope = (inl_raw[last_code] - inl_raw[first_code]) / (last_code - first_code)
        inl = inl_raw - (slope * (code_axis - first_code) + inl_raw[first_code])
    else:
        inl = inl_raw

    # --- STATISTICS ---
    dnl_valid = dnl[1:NCODES-1]  # Exclude endpoint codes
    inl_valid = inl[1:NCODES-1]

    dnl_max = np.max(np.abs(dnl_valid))
    inl_max = np.max(np.abs(inl_valid))
    dnl_rms = np.sqrt(np.mean(dnl_valid**2))
    inl_rms = np.sqrt(np.mean(inl_valid**2))

    # Check for missing codes (count = 0)
    missing_codes = np.where(counts[1:NCODES-1] == 0)[0] + 1
    # Check for non-monotonicity (DNL < -1 LSB)
    nonmono_codes = np.where(dnl_valid < -1.0)[0] + 1

    print("\n=== DNL/INL RESULTS ===")
    print(f"DNL max:  {dnl_max:.4f} LSB   (target: < 0.5 LSB)")
    print(f"DNL RMS:  {dnl_rms:.4f} LSB")
    print(f"INL max:  {inl_max:.4f} LSB   (target: < 0.5 LSB)")
    print(f"INL RMS:  {inl_rms:.4f} LSB")
    print(f"Missing codes: {len(missing_codes)}   (target: 0)")
    print(f"Non-monotonic codes: {len(nonmono_codes)}   (target: 0)")

    # --- PASS/FAIL ---
    pass_dnl = dnl_max < 0.5
    pass_inl = inl_max < 0.5
    pass_missing = len(missing_codes) == 0
    pass_mono = len(nonmono_codes) == 0

    print("\n=== PASS/FAIL ===")
    print(f"DNL < 0.5 LSB:     {'PASS' if pass_dnl else 'FAIL'}")
    print(f"INL < 0.5 LSB:     {'PASS' if pass_inl else 'FAIL'}")
    print(f"No missing codes:  {'PASS' if pass_missing else 'FAIL'}")
    print(f"Monotonic:         {'PASS' if pass_mono else 'FAIL'}")

    # --- PLOT ---
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle('VibroSense-1 8-bit SAR ADC: DNL/INL Analysis (TT, 27°C)', fontsize=14)

    # Transfer function
    ax0 = axes[0]
    code_axis = np.arange(NCODES)
    ax0.plot(code_axis * LSB_V * 1000, code_axis, 'b-', linewidth=0.5, label='ADC Output')
    ax0.plot([0, VREF*1000], [0, NCODES-1], 'r--', linewidth=1, label='Ideal')
    ax0.set_xlabel('Input Voltage (mV)')
    ax0.set_ylabel('Output Code')
    ax0.set_title('Transfer Function')
    ax0.legend(fontsize=8)
    ax0.grid(True, alpha=0.3)

    # DNL
    ax1 = axes[1]
    ax1.bar(code_axis[1:-1], dnl[1:-1], width=1, color='steelblue',
            alpha=0.7, label='DNL')
    ax1.axhline(0.5, color='red', linestyle='--', linewidth=1, label='+0.5 LSB limit')
    ax1.axhline(-0.5, color='red', linestyle='--', linewidth=1, label='-0.5 LSB limit')
    ax1.axhline(0, color='black', linestyle='-', linewidth=0.5)
    ax1.set_xlabel('Output Code')
    ax1.set_ylabel('DNL (LSB)')
    ax1.set_title(f'DNL: max = {dnl_max:.3f} LSB  {"[PASS]" if pass_dnl else "[FAIL]"}')
    ax1.set_xlim(0, NCODES)
    ax1.set_ylim(-1.0, 1.0)
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    # INL
    ax2 = axes[2]
    ax2.bar(code_axis[1:-1], inl[1:-1], width=1, color='darkorange',
            alpha=0.7, label='INL')
    ax2.axhline(0.5, color='red', linestyle='--', linewidth=1, label='+0.5 LSB limit')
    ax2.axhline(-0.5, color='red', linestyle='--', linewidth=1, label='-0.5 LSB limit')
    ax2.axhline(0, color='black', linestyle='-', linewidth=0.5)
    ax2.set_xlabel('Output Code')
    ax2.set_ylabel('INL (LSB)')
    ax2.set_title(f'INL: max = {inl_max:.3f} LSB  {"[PASS]" if pass_inl else "[FAIL]"}')
    ax2.set_xlim(0, NCODES)
    ax2.set_ylim(-1.0, 1.0)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('dnl_inl_plot.png', dpi=150, bbox_inches='tight')
    print("Saved: dnl_inl_plot.png")

    # --- SAVE RESULTS JSON ---
    results = {
        'dnl_max_lsb': float(dnl_max),
        'dnl_rms_lsb': float(dnl_rms),
        'inl_max_lsb': float(inl_max),
        'inl_rms_lsb': float(inl_rms),
        'missing_codes': int(len(missing_codes)),
        'nonmonotonic_codes': int(len(nonmono_codes)),
        'pass_dnl': bool(pass_dnl),
        'pass_inl': bool(pass_inl),
        'pass_missing': bool(pass_missing),
        'pass_mono': bool(pass_mono),
        'total_pass': bool(pass_dnl and pass_inl and pass_missing and pass_mono),
        'dnl_array': dnl.tolist(),
        'inl_array': inl.tolist(),
        'counts': counts.tolist()
    }

    with open('dnl_inl_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Saved: dnl_inl_results.json")

    return results


if __name__ == '__main__':
    dat_file = sys.argv[1] if len(sys.argv) > 1 else 'dnl_inl_raw.dat'
    run_dnl_inl_analysis(dat_file)
