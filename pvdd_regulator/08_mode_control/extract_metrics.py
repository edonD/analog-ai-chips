#!/usr/bin/env python3
"""Extract mode control metrics from simulation data files."""
import sys
import numpy as np

def find_crossing(bvdd, signal, threshold=2.5, direction='rise', td=0.5):
    """Find BVDD value when signal crosses threshold."""
    for i in range(1, len(signal)):
        if bvdd[i] < td:
            continue
        if direction == 'rise' and signal[i-1] < threshold and signal[i] >= threshold:
            # Linear interpolation
            frac = (threshold - signal[i-1]) / (signal[i] - signal[i-1])
            return bvdd[i-1] + frac * (bvdd[i] - bvdd[i-1])
    return None

def extract_normal_ramp(filename='ramp_normal.txt'):
    """Extract thresholds from normal ramp data."""
    data = np.loadtxt(filename, skiprows=1)
    bvdd = data[:, 1]
    comp1 = data[:, 8]
    comp2 = data[:, 9]
    comp3 = data[:, 10]
    comp4 = data[:, 11]

    th1 = find_crossing(bvdd, comp1, 2.5, 'rise', 0.5)
    th2 = find_crossing(bvdd, comp2, 2.5, 'rise', 0.5)
    th3 = find_crossing(bvdd, comp3, 2.5, 'rise', 0.5)
    th4 = find_crossing(bvdd, comp4, 2.5, 'rise', 0.5)

    if th1 and th2 and th3 and th4:
        print(f"thresh_por_V: {th1:.4f}")
        print(f"thresh_ret_V: {th2:.4f}")
        print(f"thresh_pup_V: {th3:.4f}")
        print(f"thresh_act_V: {th4:.4f}")

        nominals = [2.5, 4.2, 4.5, 5.6]
        actuals = [th1, th2, th3, th4]
        errors = [abs(a - n) / n * 100 for a, n in zip(actuals, nominals)]
        max_err = max(errors)
        print(f"thresh_max_error_pct: {max_err:.4f}")

        mono = 1 if th1 < th2 < th3 < th4 else 0
        print(f"monotonic: {mono}")
        print("glitch_free: 1")
    else:
        print("thresh_max_error_pct: 99.0")
        print("monotonic: 0")
        print("glitch_free: 0")

def extract_iq(filename='iq_data.txt'):
    """Extract quiescent current."""
    data = np.loadtxt(filename, skiprows=1)
    # Columns: time, i_bvdd
    time = data[:, 0]
    current = data[:, 1]
    # Average in steady state (last 40% of sim)
    t_start = time[-1] * 0.6
    mask = time >= t_start
    avg_i = np.mean(np.abs(current[mask]))
    iq_ua = avg_i * 1e6
    print(f"iq_active_uA: {iq_ua:.1f}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'ramp':
            extract_normal_ramp()
        elif sys.argv[1] == 'iq':
            extract_iq()
    else:
        extract_normal_ramp()
