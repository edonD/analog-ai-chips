#!/usr/bin/env python3
"""Generate SPICE PWL stimulus files for VibroSense-1 full-chain simulation.

Since CWRU .mat files may not be available, generates synthetic bearing
vibration signals based on known fault characteristic frequencies.

Bearing: 6205-2RS (CWRU test rig)
Shaft speed: 1797 RPM (29.95 Hz)
BPFI = 5.415 * f_shaft = 162.2 Hz  (inner race fault frequency)
BPFO = 3.585 * f_shaft = 107.4 Hz  (outer race fault frequency)
BSF  = 2.357 * f_shaft = 70.6 Hz   (ball spin frequency)
"""

import numpy as np
import os
import sys

# Parameters
FS = 12000       # Sample rate (Hz) — matches CWRU
DURATION = 0.2   # Simulation duration (seconds) — short for practical sim time
V_SCALE = 0.1    # Volts per g
V_OFFSET = 0.9   # DC bias (mid-supply)
SHAFT_RPM = 1797
F_SHAFT = SHAFT_RPM / 60.0  # ~29.95 Hz

# Characteristic frequencies
BPFI = 5.415 * F_SHAFT  # ~162.2 Hz
BPFO = 3.585 * F_SHAFT  # ~107.4 Hz
BSF  = 2.357 * F_SHAFT  # ~70.6 Hz

def generate_bearing_signal(fault_type, duration=DURATION, fs=FS,
                            snr_db=20, fault_amplitude=3.0):
    """Generate synthetic bearing vibration signal.

    Returns time array and voltage array.
    """
    np.random.seed(42)  # Reproducible
    n_samples = int(duration * fs)
    t = np.arange(n_samples) / fs

    # Base: broadband noise (normal vibration)
    noise = np.random.randn(n_samples)
    # Shape noise spectrum (more energy at low freq, typical of machinery)
    from scipy.signal import lfilter
    b_lpf = [0.1, 0.2, 0.3, 0.2, 0.1]
    noise = lfilter(b_lpf, [1.0], noise)
    noise = noise / np.std(noise)  # normalize

    signal = noise * 0.3  # baseline noise level

    if fault_type == 'normal':
        pass  # just noise

    elif fault_type == 'inner_race':
        # Periodic impulses at BPFI, amplitude-modulated by shaft rotation
        period_samples = int(fs / BPFI)
        impulse_train = np.zeros(n_samples)
        for i in range(0, n_samples, period_samples):
            impulse_train[i] = fault_amplitude
        # Impulse response: decaying high-frequency sinusoid (~3 kHz resonance)
        n_ir = min(200, period_samples - 1)
        ir_t = np.arange(n_ir) / fs
        impulse_resp = np.exp(-ir_t * 800) * np.sin(2 * np.pi * 3000 * ir_t)
        fault_signal = np.convolve(impulse_train, impulse_resp, mode='same')
        # AM by shaft rotation (inner race rotates with shaft)
        am = 1.0 + 0.5 * np.cos(2 * np.pi * F_SHAFT * t)
        signal += fault_signal * am

    elif fault_type == 'outer_race':
        # Periodic impulses at BPFO (no AM — outer race is stationary)
        period_samples = int(fs / BPFO)
        impulse_train = np.zeros(n_samples)
        for i in range(0, n_samples, period_samples):
            impulse_train[i] = fault_amplitude * 0.8
        n_ir = min(200, period_samples - 1)
        ir_t = np.arange(n_ir) / fs
        impulse_resp = np.exp(-ir_t * 600) * np.sin(2 * np.pi * 2500 * ir_t)
        signal += np.convolve(impulse_train, impulse_resp, mode='same')

    elif fault_type == 'ball':
        # Periodic impulses at 2*BSF (ball contacts both races per revolution)
        f_fault = 2.0 * BSF
        period_samples = int(fs / f_fault)
        impulse_train = np.zeros(n_samples)
        for i in range(0, n_samples, period_samples):
            impulse_train[i] = fault_amplitude * 0.6
        n_ir = min(200, period_samples - 1)
        ir_t = np.arange(n_ir) / fs
        impulse_resp = np.exp(-ir_t * 500) * np.sin(2 * np.pi * 3500 * ir_t)
        # Random AM (ball defect contact is intermittent)
        am = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * BSF * t))
        signal += np.convolve(impulse_train, impulse_resp, mode='same') * am

    # Scale to voltage
    voltage = signal * V_SCALE + V_OFFSET
    voltage = np.clip(voltage, 0.01, 1.79)  # Stay within rails with margin

    return t, voltage


def write_pwl(t, voltage, filename, fault_type, comment=""):
    """Write PWL stimulus file for ngspice."""
    with open(filename, 'w') as f:
        f.write(f"* VibroSense-1 Stimulus: {fault_type}\n")
        f.write(f"* {comment}\n")
        f.write(f"* {len(t)} samples at {FS} Hz, {DURATION:.3f} sec\n")
        f.write(f"* V_scale={V_SCALE} V/g, V_offset={V_OFFSET} V\n")
        f.write(f"* Use: .include this_file.pwl  (replaces Vin in top netlist)\n\n")
        f.write(f"Vin vin gnd PWL(\n")
        for i in range(len(t)):
            f.write(f"+  {t[i]:.9f} {voltage[i]:.6f}\n")
        f.write(f"+  {DURATION:.9f} {V_OFFSET:.6f})\n")


def main():
    outdir = os.path.join(os.path.dirname(__file__), '..', 'stimuli')
    os.makedirs(outdir, exist_ok=True)

    fault_types = {
        'normal':     'Normal bearing operation (broadband noise only)',
        'inner_race': f'Inner race fault (BPFI={BPFI:.1f} Hz, AM by shaft)',
        'outer_race': f'Outer race fault (BPFO={BPFO:.1f} Hz, stationary)',
        'ball':       f'Ball fault (2*BSF={2*BSF:.1f} Hz, intermittent)',
    }

    for fault_type, comment in fault_types.items():
        print(f"Generating {fault_type} stimulus...")
        t, voltage = generate_bearing_signal(fault_type)
        outfile = os.path.join(outdir, f'{fault_type}_stimulus.pwl')
        write_pwl(t, voltage, outfile, fault_type, comment)
        print(f"  -> {outfile} ({len(t)} samples, "
              f"Vmin={voltage.min():.3f}, Vmax={voltage.max():.3f})")

    print(f"\nAll stimuli generated in {outdir}/")
    print(f"Duration: {DURATION*1000:.0f} ms each")
    print(f"Sample rate: {FS} Hz")


if __name__ == '__main__':
    main()
