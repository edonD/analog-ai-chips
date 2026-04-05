#!/usr/bin/env python3
"""Generate VARIANT stimuli for generalization testing.

Creates variations of the 4 bearing fault types with:
- Different fault severity (amplitude scaling: 0.5x, 1.0x, 2.0x)
- Different noise levels (SNR: 15dB, 20dB, 25dB)
- Slightly shifted fault frequencies (+/- 5%)
- Different random seeds for noise
"""

import numpy as np
import os
import sys

# Parameters (from generate_stimuli.py)
FS = 12000
DURATION = 0.2
V_SCALE = 0.1
V_OFFSET = 0.9
SHAFT_RPM = 1797
F_SHAFT = SHAFT_RPM / 60.0

# Characteristic frequencies
BPFI = 5.415 * F_SHAFT
BPFO = 3.585 * F_SHAFT
BSF  = 2.357 * F_SHAFT


def generate_bearing_signal(fault_type, duration=DURATION, fs=FS,
                            noise_level=0.3, fault_amplitude=3.0,
                            freq_shift=1.0, seed=42):
    """Generate synthetic bearing vibration signal with configurable params."""
    np.random.seed(seed)
    n_samples = int(duration * fs)
    t = np.arange(n_samples) / fs

    # Base: broadband noise
    from scipy.signal import lfilter
    noise = np.random.randn(n_samples)
    b_lpf = [0.1, 0.2, 0.3, 0.2, 0.1]
    noise = lfilter(b_lpf, [1.0], noise)
    noise = noise / np.std(noise)
    signal = noise * noise_level

    if fault_type == 'normal':
        pass

    elif fault_type == 'inner_race':
        f_fault = BPFI * freq_shift
        period_samples = max(2, int(fs / f_fault))
        impulse_train = np.zeros(n_samples)
        for i in range(0, n_samples, period_samples):
            impulse_train[i] = fault_amplitude
        n_ir = min(200, period_samples - 1)
        ir_t = np.arange(n_ir) / fs
        impulse_resp = np.exp(-ir_t * 800) * np.sin(2 * np.pi * 3000 * freq_shift * ir_t)
        fault_signal = np.convolve(impulse_train, impulse_resp, mode='same')
        am = 1.0 + 0.5 * np.cos(2 * np.pi * F_SHAFT * t)
        signal += fault_signal * am

    elif fault_type == 'outer_race':
        f_fault = BPFO * freq_shift
        period_samples = max(2, int(fs / f_fault))
        impulse_train = np.zeros(n_samples)
        for i in range(0, n_samples, period_samples):
            impulse_train[i] = fault_amplitude * 0.8
        n_ir = min(200, period_samples - 1)
        ir_t = np.arange(n_ir) / fs
        impulse_resp = np.exp(-ir_t * 600) * np.sin(2 * np.pi * 2500 * freq_shift * ir_t)
        signal += np.convolve(impulse_train, impulse_resp, mode='same')

    elif fault_type == 'ball':
        f_fault = 2.0 * BSF * freq_shift
        period_samples = max(2, int(fs / f_fault))
        impulse_train = np.zeros(n_samples)
        for i in range(0, n_samples, period_samples):
            impulse_train[i] = fault_amplitude * 0.6
        n_ir = min(200, period_samples - 1)
        ir_t = np.arange(n_ir) / fs
        impulse_resp = np.exp(-ir_t * 500) * np.sin(2 * np.pi * 3500 * freq_shift * ir_t)
        am = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * BSF * freq_shift * t))
        signal += np.convolve(impulse_train, impulse_resp, mode='same') * am

    voltage = signal * V_SCALE + V_OFFSET
    voltage = np.clip(voltage, 0.01, 1.79)
    return t, voltage


def write_pwl(t, voltage, filename, fault_type, comment=""):
    """Write PWL stimulus file for ngspice."""
    with open(filename, 'w') as f:
        f.write(f"* VibroSense-1 Variant Stimulus: {fault_type}\n")
        f.write(f"* {comment}\n")
        f.write(f"* {len(t)} samples at {FS} Hz, {DURATION:.3f} sec\n")
        f.write(f"* V_scale={V_SCALE} V/g, V_offset={V_OFFSET} V\n")
        f.write(f"Vin vin gnd PWL(\n")
        for i in range(len(t)):
            f.write(f"+  {t[i]:.9f} {voltage[i]:.6f}\n")
        f.write(f"+  {DURATION:.9f} {V_OFFSET:.6f})\n")


def main():
    outdir = os.path.join(os.path.dirname(__file__), '..', 'stimuli')
    os.makedirs(outdir, exist_ok=True)

    # Define variant test cases
    # Format: (name, fault_type, params_dict)
    variants = [
        # Severity variants (amplitude scaling)
        ('normal_v1',      'normal',     dict(noise_level=0.3, fault_amplitude=3.0, freq_shift=1.0, seed=100)),
        ('normal_v2',      'normal',     dict(noise_level=0.5, fault_amplitude=3.0, freq_shift=1.0, seed=200)),
        ('inner_race_v1',  'inner_race', dict(noise_level=0.3, fault_amplitude=1.5, freq_shift=1.0, seed=101)),
        ('inner_race_v2',  'inner_race', dict(noise_level=0.3, fault_amplitude=6.0, freq_shift=1.0, seed=102)),
        ('inner_race_v3',  'inner_race', dict(noise_level=0.4, fault_amplitude=3.0, freq_shift=0.95, seed=103)),
        ('outer_race_v1',  'outer_race', dict(noise_level=0.3, fault_amplitude=1.2, freq_shift=1.0, seed=201)),
        ('outer_race_v2',  'outer_race', dict(noise_level=0.3, fault_amplitude=4.8, freq_shift=1.0, seed=202)),
        ('outer_race_v3',  'outer_race', dict(noise_level=0.4, fault_amplitude=2.4, freq_shift=1.05, seed=203)),
        ('ball_v1',        'ball',       dict(noise_level=0.3, fault_amplitude=0.9, freq_shift=1.0, seed=301)),
        ('ball_v2',        'ball',       dict(noise_level=0.3, fault_amplitude=3.6, freq_shift=1.0, seed=302)),
        ('ball_v3',        'ball',       dict(noise_level=0.4, fault_amplitude=1.8, freq_shift=0.95, seed=303)),
        # Edge case: very mild fault (hard to distinguish from normal)
        ('inner_race_mild', 'inner_race', dict(noise_level=0.4, fault_amplitude=1.0, freq_shift=1.0, seed=150)),
    ]

    for name, fault_type, params in variants:
        print(f"Generating {name} ({fault_type})...")
        t, voltage = generate_bearing_signal(fault_type, **params)
        outfile = os.path.join(outdir, f'{name}_stimulus.pwl')
        write_pwl(t, voltage, outfile, fault_type,
                  f"Variant: amp={params['fault_amplitude']}, noise={params['noise_level']}, "
                  f"freq_shift={params['freq_shift']}, seed={params['seed']}")
        print(f"  -> {outfile} (Vmin={voltage.min():.3f}, Vmax={voltage.max():.3f})")

    print(f"\n{len(variants)} variant stimuli generated")
    return variants


if __name__ == '__main__':
    main()
