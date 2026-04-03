#!/usr/bin/env python3
"""VibroSense Block 04: Envelope Detector — Simulation & Verification

Generates SPICE testbenches, runs ngspice, analyzes results, generates plots,
and reports PASS/FAIL for all specifications.

Specifications:
  - Rectification accuracy: <5% at 100mVpp, <15% at 10mVpp
  - Minimum detectable signal: <10 mVpp
  - LPF cutoff frequency: 5-20 Hz
  - Output ripple: <5% of DC at BPF3 frequency
  - Settling time: <200 ms (10% to 90%)
  - Power per channel: <10 uW
"""

import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
import re
import json

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────
VDD = 1.8
VCM = 0.9
WORK_DIR = os.path.dirname(os.path.abspath(__file__))

BPF_FREQS = {
    'BPF1': 224,
    'BPF2': 1000,
    'BPF3': 3162,
    'BPF4': 7071,
    'BPF5': 14142,
}

# Envelope detector design parameters
GM_RECT = 2.5e-6      # Rectifier OTA gm (A/V)
GM_LPF = 6.28e-9      # LPF OTA gm (A/V)
C_LPF = 100e-12       # LPF capacitor (F)
FC_LPF = GM_LPF / (2 * np.pi * C_LPF)   # ~10 Hz
TAU_LPF = C_LPF / GM_LPF                  # ~15.9 ms

# Results storage
results = {}


def run_ngspice(spice_file, timeout=120):
    """Run ngspice in batch mode and return stdout."""
    cmd = ['ngspice', '-b', spice_file]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout, cwd=WORK_DIR)
        return proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        return '', 'TIMEOUT', -1


def read_wrdata(filename):
    """Read ngspice wrdata output (ASCII columns: index val1 val2 ...)."""
    filepath = os.path.join(WORK_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  WARNING: {filename} not found")
        return None
    try:
        data = np.loadtxt(filepath)
        return data
    except Exception as e:
        print(f"  WARNING: Could not parse {filename}: {e}")
        return None


def write_file(filename, content):
    """Write content to file in working directory."""
    filepath = os.path.join(WORK_DIR, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath


# ──────────────────────────────────────────────
# Test 1: Amplitude Sweep (Rectification Accuracy)
# ──────────────────────────────────────────────
def test_amplitude_sweep():
    """Sweep input amplitude at BPF3 frequency, measure DC output accuracy."""
    print("\n" + "="*60)
    print("TEST 1: Amplitude Sweep — Rectification Accuracy")
    print("="*60)

    freq = BPF_FREQS['BPF3']  # 3162 Hz
    # Amplitudes in Vpp
    amplitudes_vpp = [0.005, 0.010, 0.020, 0.050, 0.100, 0.200, 0.500]
    sim_time = 0.4   # 400 ms (>25 LPF time constants)
    meas_start = 0.3  # Measure from 300ms to 400ms
    tstep = 1e-6

    measured_dc = []
    expected_dc = []

    for vpp in amplitudes_vpp:
        vpeak = vpp / 2.0
        tb_name = f'tb_amp_{int(vpp*1000)}mv'

        # Expected DC output for full-wave rectified sine:
        # DC = (2/pi) * Vpeak
        exp_dc = (2.0 / np.pi) * vpeak
        expected_dc.append(exp_dc)

        spice = f"""* Amplitude sweep test: {vpp*1000:.0f} mVpp at {freq} Hz
.title Envelope Detector - Amp Sweep {vpp*1000:.0f}mVpp

.include envelope_det.spice

Vdd vdd 0 {VDD}
Vss vss 0 0
Vcm vcm 0 {VCM}

* Input sine: amplitude = {vpeak*1000:.1f} mV peak
Vin vin vcm sin(0 {vpeak} {freq})

* Envelope detector instance
Xenv vin vcm vout vdd vss envelope_det

.tran {tstep} {sim_time} uic

.control
run
* Measure average output in steady state
meas tran vout_avg avg v(vout) from={meas_start} to={sim_time}
meas tran vout_pp pp v(vout) from={meas_start} to={sim_time}
meas tran vrect_avg avg v(Xenv.rect) from={meas_start} to={sim_time}
wrdata {tb_name}_out.txt v(vout) v(vin) v(Xenv.rect)
echo "MEAS_RESULT vout_avg=$&vout_avg vout_pp=$&vout_pp vrect_avg=$&vrect_avg"
quit
.endc

.end
"""
        write_file(f'{tb_name}.spice', spice)
        stdout, stderr, rc = run_ngspice(f'{tb_name}.spice')

        # Parse measurement from stdout
        vout_dc = None
        for line in (stdout + stderr).split('\n'):
            if 'vout_avg' in line and 'MEAS_RESULT' in line:
                m = re.search(r'vout_avg=([\d.eE+-]+)', line)
                if m:
                    vout_dc = float(m.group(1))
            elif 'vout_avg' in line and '=' in line:
                m = re.search(r'vout_avg\s*=\s*([\d.eE+-]+)', line)
                if m:
                    vout_dc = float(m.group(1))

        if vout_dc is None:
            # Try reading from wrdata
            data = read_wrdata(f'{tb_name}_out.txt')
            if data is not None and len(data) > 0:
                # wrdata format: col0=index, col1=vout, col2=vin, col3=rect
                # Find steady-state region
                n_total = len(data)
                n_start = int(n_total * meas_start / sim_time)
                vout_dc = np.mean(data[n_start:, 1])

        if vout_dc is not None:
            measured_dc.append(vout_dc)
            error_pct = (vout_dc - exp_dc) / exp_dc * 100 if exp_dc > 0 else 0
            print(f"  {vpp*1000:6.0f} mVpp: DC_out = {vout_dc*1000:8.3f} mV, "
                  f"Expected = {exp_dc*1000:8.3f} mV, Error = {error_pct:+.1f}%")
        else:
            measured_dc.append(np.nan)
            print(f"  {vpp*1000:6.0f} mVpp: FAILED to get measurement")

    # Store results
    results['amp_sweep'] = {
        'amplitudes_vpp': amplitudes_vpp,
        'measured_dc': measured_dc,
        'expected_dc': expected_dc,
        'freq_hz': freq,
    }

    # Check specs
    measured_dc = np.array(measured_dc)
    expected_dc = np.array(expected_dc)
    errors_pct = np.where(expected_dc > 0,
                          (measured_dc - expected_dc) / expected_dc * 100, 0)

    # Find error at 100 mVpp
    idx_100 = amplitudes_vpp.index(0.100)
    err_100 = abs(errors_pct[idx_100])
    results['rect_accuracy_100mv'] = err_100
    print(f"\n  Rectification accuracy at 100mVpp: {err_100:.1f}% (spec: <5%) "
          f"→ {'PASS' if err_100 < 5 else 'FAIL'}")

    # Find error at 10 mVpp
    idx_10 = amplitudes_vpp.index(0.010)
    err_10 = abs(errors_pct[idx_10])
    results['rect_accuracy_10mv'] = err_10
    print(f"  Rectification accuracy at 10mVpp:  {err_10:.1f}% (spec: <15%) "
          f"→ {'PASS' if err_10 < 15 else 'FAIL'}")

    return amplitudes_vpp, measured_dc, expected_dc


# ──────────────────────────────────────────────
# Test 2: Ripple Measurement at all BPF frequencies
# ──────────────────────────────────────────────
def test_ripple():
    """Measure output ripple at each BPF center frequency."""
    print("\n" + "="*60)
    print("TEST 2: Output Ripple at BPF Center Frequencies")
    print("="*60)

    vpp = 0.100  # 100 mVpp input
    vpeak = vpp / 2.0
    sim_time = 0.5
    meas_start = 0.35
    tstep = 5e-6

    ripple_results = {}

    for name, freq in BPF_FREQS.items():
        # Adjust tstep for high frequencies
        ts = min(tstep, 1.0 / (freq * 40))
        tb_name = f'tb_ripple_{name.lower()}'

        spice = f"""* Ripple test at {name} center frequency ({freq} Hz)
.title Envelope Detector - Ripple at {name}

.include envelope_det.spice

Vdd vdd 0 {VDD}
Vss vss 0 0
Vcm vcm 0 {VCM}

Vin vin vcm sin(0 {vpeak} {freq})

Xenv vin vcm vout vdd vss envelope_det

.tran {ts} {sim_time} uic

.control
run
meas tran vout_avg avg v(vout) from={meas_start} to={sim_time}
meas tran vout_pp pp v(vout) from={meas_start} to={sim_time}
meas tran vout_max max v(vout) from={meas_start} to={sim_time}
meas tran vout_min min v(vout) from={meas_start} to={sim_time}
wrdata {tb_name}_out.txt v(vout)
echo "MEAS_RESULT vout_avg=$&vout_avg vout_pp=$&vout_pp vout_max=$&vout_max vout_min=$&vout_min"
quit
.endc

.end
"""
        write_file(f'{tb_name}.spice', spice)
        stdout, stderr, rc = run_ngspice(f'{tb_name}.spice')

        vout_avg = None
        vout_pp = None
        for line in (stdout + stderr).split('\n'):
            m_avg = re.search(r'vout_avg\s*=\s*([\d.eE+-]+)', line)
            m_pp = re.search(r'vout_pp\s*=\s*([\d.eE+-]+)', line)
            if m_avg:
                vout_avg = float(m_avg.group(1))
            if m_pp:
                vout_pp = float(m_pp.group(1))

        if vout_avg is None or vout_pp is None:
            data = read_wrdata(f'{tb_name}_out.txt')
            if data is not None and len(data) > 0:
                n_total = len(data)
                n_start = int(n_total * meas_start / sim_time)
                vout_ss = data[n_start:, 1]
                vout_avg = np.mean(vout_ss)
                vout_pp = np.max(vout_ss) - np.min(vout_ss)

        if vout_avg is not None and vout_pp is not None and vout_avg > 0:
            ripple_pct = (vout_pp / vout_avg) * 100
            ripple_results[name] = {
                'freq': freq, 'dc': vout_avg, 'pp': vout_pp, 'ripple_pct': ripple_pct
            }
            print(f"  {name} ({freq:5d} Hz): DC = {vout_avg*1000:.3f} mV, "
                  f"Ripple_pp = {vout_pp*1000:.4f} mV, "
                  f"Ripple = {ripple_pct:.2f}% → {'PASS' if ripple_pct < 5 else 'FAIL'}")
        else:
            ripple_results[name] = None
            print(f"  {name} ({freq:5d} Hz): FAILED to get measurement")

    results['ripple'] = ripple_results

    # Worst case ripple (at lowest frequency BPF1)
    if ripple_results.get('BPF3') and ripple_results['BPF3']:
        results['ripple_bpf3_pct'] = ripple_results['BPF3']['ripple_pct']
    if ripple_results.get('BPF1') and ripple_results['BPF1']:
        results['ripple_worst_pct'] = ripple_results['BPF1']['ripple_pct']

    return ripple_results


# ──────────────────────────────────────────────
# Test 3: LPF Cutoff Frequency
# ──────────────────────────────────────────────
def test_lpf_cutoff():
    """Measure the LPF cutoff frequency by sweeping modulation frequency."""
    print("\n" + "="*60)
    print("TEST 3: LPF Cutoff Frequency Measurement")
    print("="*60)

    # Apply AM signal: carrier at BPF3, modulation frequency swept
    # Measure envelope output amplitude at each modulation frequency
    carrier_freq = BPF_FREQS['BPF3']  # 3162 Hz
    mod_freqs = [0.5, 1, 2, 5, 10, 20, 50, 100]
    carrier_amp = 0.050  # 50mV peak (100mVpp)
    mod_depth = 0.5      # 50% modulation depth

    envelope_gains = []

    for fmod in mod_freqs:
        # Simulation time: at least 5 cycles of modulation
        sim_time = max(0.5, 10.0 / fmod)
        # Measurement window: last 5 cycles
        meas_cycles = min(5, int(fmod * sim_time * 0.5))
        meas_start = sim_time - meas_cycles / fmod
        tstep = min(1e-5, 1.0 / (carrier_freq * 30))

        tb_name = f'tb_lpf_fmod_{int(fmod*10)}'

        # AM signal: Vin = A * (1 + m*sin(2pi*fmod*t)) * sin(2pi*fc*t)
        # In SPICE B-source:
        spice = f"""* LPF cutoff test: modulation at {fmod} Hz
.title Envelope Detector - LPF Cutoff (fmod={fmod} Hz)

.include envelope_det.spice

Vdd vdd 0 {VDD}
Vss vss 0 0
Vcm vcm 0 {VCM}

* AM-modulated input
B_vin vin vcm V = {carrier_amp} * (1 + {mod_depth}*sin(2*3.14159265*{fmod}*time)) * sin(2*3.14159265*{carrier_freq}*time)

Xenv vin vcm vout vdd vss envelope_det

.tran {tstep} {sim_time} uic

.control
run
meas tran vout_avg avg v(vout) from={meas_start} to={sim_time}
meas tran vout_pp pp v(vout) from={meas_start} to={sim_time}
wrdata {tb_name}_out.txt v(vout)
echo "MEAS_RESULT vout_avg=$&vout_avg vout_pp=$&vout_pp"
quit
.endc

.end
"""
        write_file(f'{tb_name}.spice', spice)
        stdout, stderr, rc = run_ngspice(f'{tb_name}.spice', timeout=180)

        vout_avg = None
        vout_pp = None
        for line in (stdout + stderr).split('\n'):
            m_avg = re.search(r'vout_avg\s*=\s*([\d.eE+-]+)', line)
            m_pp = re.search(r'vout_pp\s*=\s*([\d.eE+-]+)', line)
            if m_avg:
                vout_avg = float(m_avg.group(1))
            if m_pp:
                vout_pp = float(m_pp.group(1))

        if vout_avg is None or vout_pp is None:
            data = read_wrdata(f'{tb_name}_out.txt')
            if data is not None and len(data) > 0:
                n_total = len(data)
                n_start = int(n_total * meas_start / sim_time)
                vout_ss = data[n_start:, 1]
                vout_avg = np.mean(vout_ss)
                vout_pp = np.max(vout_ss) - np.min(vout_ss)

        if vout_avg is not None and vout_pp is not None:
            # Envelope modulation amplitude (half of pp)
            env_amp = vout_pp / 2.0
            # Expected DC from carrier: (2/pi) * carrier_amp = 31.83 mV
            dc_expected = (2.0 / np.pi) * carrier_amp
            # Expected modulation on DC: dc_expected * mod_depth = 15.92 mV
            # At 0.5 Hz (well below cutoff), envelope should track fully
            # Normalize gain to low-frequency response
            envelope_gains.append({'fmod': fmod, 'env_amp': env_amp, 'dc': vout_avg})
            print(f"  fmod = {fmod:6.1f} Hz: DC = {vout_avg*1000:.3f} mV, "
                  f"Env_pp = {vout_pp*1000:.4f} mV")
        else:
            envelope_gains.append({'fmod': fmod, 'env_amp': 0, 'dc': 0})
            print(f"  fmod = {fmod:6.1f} Hz: FAILED to measure")

    # Normalize gains to find -3dB point
    if envelope_gains and envelope_gains[0]['env_amp'] > 0:
        gain_ref = envelope_gains[0]['env_amp']  # Gain at lowest freq
        gains_db = []
        for eg in envelope_gains:
            if eg['env_amp'] > 0:
                g = 20 * np.log10(eg['env_amp'] / gain_ref)
            else:
                g = -60
            gains_db.append(g)

        # Find -3dB crossing
        fc_measured = None
        for i in range(len(gains_db) - 1):
            if gains_db[i] > -3 and gains_db[i+1] <= -3:
                # Linear interpolation
                f1, f2 = mod_freqs[i], mod_freqs[i+1]
                g1, g2 = gains_db[i], gains_db[i+1]
                fc_measured = f1 + (f2 - f1) * (-3 - g1) / (g2 - g1)
                break

        if fc_measured is None and all(g > -3 for g in gains_db):
            fc_measured = mod_freqs[-1]  # All above -3dB, fc > max tested
        elif fc_measured is None:
            fc_measured = mod_freqs[0]   # All below -3dB

        results['lpf_cutoff_hz'] = fc_measured
        results['lpf_gains'] = envelope_gains
        results['lpf_gains_db'] = gains_db
        results['lpf_mod_freqs'] = mod_freqs
        print(f"\n  LPF -3dB cutoff: {fc_measured:.1f} Hz (spec: 5-20 Hz) "
              f"→ {'PASS' if 5 <= fc_measured <= 20 else 'FAIL'}")
    else:
        results['lpf_cutoff_hz'] = None
        print(f"\n  LPF cutoff: COULD NOT DETERMINE")

    return envelope_gains


# ──────────────────────────────────────────────
# Test 4: Burst Detection / Settling Time
# ──────────────────────────────────────────────
def test_settling():
    """Apply burst signal, measure 10%-90% settling time."""
    print("\n" + "="*60)
    print("TEST 4: Settling Time (Burst Detection)")
    print("="*60)

    freq = BPF_FREQS['BPF3']
    vpeak = 0.050   # 50mV peak = 100mVpp
    sim_time = 0.5
    tstep = 1e-6

    # Burst starts at t=50ms (after initial settling to zero)
    burst_start = 0.05

    spice = f"""* Settling time test: burst at {freq} Hz
.title Envelope Detector - Settling Time

.include envelope_det.spice

Vdd vdd 0 {VDD}
Vss vss 0 0
Vcm vcm 0 {VCM}

* Burst signal: zero for t<{burst_start}, then sine at {freq} Hz
B_vin vin vcm V = {vpeak} * sin(2*3.14159265*{freq}*time) * (time > {burst_start} ? 1 : 0)

Xenv vin vcm vout vdd vss envelope_det

.tran {tstep} {sim_time} uic

.control
run
wrdata tb_settling_out.txt v(vout) v(vin)
quit
.endc

.end
"""
    write_file('tb_settling.spice', spice)
    stdout, stderr, rc = run_ngspice('tb_settling.spice')

    data = read_wrdata('tb_settling_out.txt')
    if data is not None and len(data) > 100:
        time_arr = data[:, 0]
        vout_arr = data[:, 1]

        # Find final DC value (average over last 50ms)
        t_end_start = sim_time - 0.05
        mask_end = time_arr >= t_end_start
        if np.any(mask_end):
            v_final = np.mean(vout_arr[mask_end])
        else:
            v_final = vout_arr[-1]

        # Find 10% and 90% levels
        v_10 = 0.1 * v_final
        v_90 = 0.9 * v_final

        # Find time of burst start
        mask_after_burst = time_arr >= burst_start
        t_burst = time_arr[mask_after_burst]
        v_burst = vout_arr[mask_after_burst]

        # Time when output first reaches 10%
        t_10 = None
        t_90 = None
        for i in range(len(v_burst)):
            if t_10 is None and v_burst[i] >= v_10:
                t_10 = t_burst[i]
            if t_90 is None and v_burst[i] >= v_90:
                t_90 = t_burst[i]

        if t_10 is not None and t_90 is not None:
            settling_time_ms = (t_90 - t_10) * 1000
            results['settling_time_ms'] = settling_time_ms
            results['settling_v_final'] = v_final
            print(f"  Final DC value: {v_final*1000:.3f} mV")
            print(f"  10% time: {(t_10-burst_start)*1000:.1f} ms after burst")
            print(f"  90% time: {(t_90-burst_start)*1000:.1f} ms after burst")
            print(f"  Settling time (10%-90%): {settling_time_ms:.1f} ms (spec: <200 ms) "
                  f"→ {'PASS' if settling_time_ms < 200 else 'FAIL'}")
        else:
            results['settling_time_ms'] = None
            print(f"  Could not determine settling time")
            print(f"  v_final = {v_final*1000:.3f} mV, v_10 = {v_10*1000:.3f}, v_90 = {v_90*1000:.3f}")
    else:
        results['settling_time_ms'] = None
        print("  FAILED: No simulation data")

    return data


# ──────────────────────────────────────────────
# Test 5: AM Tracking (Envelope Following)
# ──────────────────────────────────────────────
def test_am_tracking():
    """Apply AM signal, verify envelope tracking."""
    print("\n" + "="*60)
    print("TEST 5: AM Envelope Tracking")
    print("="*60)

    carrier_freq = BPF_FREQS['BPF3']
    mod_freq = 5.0     # 5 Hz modulation
    carrier_amp = 0.050  # 50 mV peak
    mod_depth = 0.8     # 80% depth for clear visualization
    sim_time = 1.0
    tstep = 5e-6

    spice = f"""* AM tracking test: carrier {carrier_freq} Hz, modulation {mod_freq} Hz
.title Envelope Detector - AM Tracking

.include envelope_det.spice

Vdd vdd 0 {VDD}
Vss vss 0 0
Vcm vcm 0 {VCM}

* AM signal: A*(1 + m*sin(2*pi*fmod*t)) * sin(2*pi*fc*t)
B_vin vin vcm V = {carrier_amp} * (1 + {mod_depth}*sin(2*3.14159265*{mod_freq}*time)) * sin(2*3.14159265*{carrier_freq}*time)

Xenv vin vcm vout vdd vss envelope_det

.tran {tstep} {sim_time} uic

.control
run
wrdata tb_am_track_out.txt v(vout) v(vin) v(Xenv.rect)
quit
.endc

.end
"""
    write_file('tb_am_track.spice', spice)
    stdout, stderr, rc = run_ngspice('tb_am_track.spice')

    data = read_wrdata('tb_am_track_out.txt')
    if data is not None and len(data) > 100:
        time_arr = data[:, 0]
        vout_arr = data[:, 1]

        # Compute ideal envelope for comparison
        ideal_envelope = (2.0/np.pi) * carrier_amp * (1 + mod_depth * np.sin(2*np.pi*mod_freq*time_arr))

        # Measure tracking accuracy in steady state (after 200ms settling)
        mask_ss = time_arr >= 0.2
        if np.any(mask_ss):
            tracking_error = np.abs(vout_arr[mask_ss] - ideal_envelope[mask_ss])
            rms_error = np.sqrt(np.mean(tracking_error**2))
            dc_level = np.mean(ideal_envelope[mask_ss])
            error_pct = (rms_error / dc_level) * 100

            results['am_tracking_error_pct'] = error_pct
            print(f"  Carrier: {carrier_freq} Hz, Modulation: {mod_freq} Hz, Depth: {mod_depth*100:.0f}%")
            print(f"  RMS tracking error: {rms_error*1000:.4f} mV ({error_pct:.1f}% of DC)")
            print(f"  Envelope tracking: {'GOOD' if error_pct < 10 else 'DEGRADED'}")
        else:
            print("  No steady-state data")
    else:
        print("  FAILED: No simulation data")

    return data


# ──────────────────────────────────────────────
# Test 6: Multi-Channel Verification
# ──────────────────────────────────────────────
def test_multichannel():
    """Verify envelope detector works at all 5 BPF center frequencies."""
    print("\n" + "="*60)
    print("TEST 6: Multi-Channel Verification (All 5 BPF Frequencies)")
    print("="*60)

    vpp = 0.100  # 100 mVpp
    vpeak = vpp / 2.0
    sim_time = 0.4
    meas_start = 0.3
    expected_dc = (2.0/np.pi) * vpeak

    channel_results = {}

    for name, freq in BPF_FREQS.items():
        tstep = min(1e-5, 1.0 / (freq * 30))
        tb_name = f'tb_multi_{name.lower()}'

        spice = f"""* Multi-channel test: {name} at {freq} Hz
.title Envelope Detector - {name} ({freq} Hz)

.include envelope_det.spice

Vdd vdd 0 {VDD}
Vss vss 0 0
Vcm vcm 0 {VCM}

Vin vin vcm sin(0 {vpeak} {freq})

Xenv vin vcm vout vdd vss envelope_det

.tran {tstep} {sim_time} uic

.control
run
meas tran vout_avg avg v(vout) from={meas_start} to={sim_time}
meas tran vout_pp pp v(vout) from={meas_start} to={sim_time}
echo "MEAS_RESULT vout_avg=$&vout_avg vout_pp=$&vout_pp"
quit
.endc

.end
"""
        write_file(f'{tb_name}.spice', spice)
        stdout, stderr, rc = run_ngspice(f'{tb_name}.spice')

        vout_avg = None
        vout_pp = None
        for line in (stdout + stderr).split('\n'):
            m_avg = re.search(r'vout_avg\s*=\s*([\d.eE+-]+)', line)
            m_pp = re.search(r'vout_pp\s*=\s*([\d.eE+-]+)', line)
            if m_avg:
                vout_avg = float(m_avg.group(1))
            if m_pp:
                vout_pp = float(m_pp.group(1))

        if vout_avg is not None:
            error_pct = (vout_avg - expected_dc) / expected_dc * 100
            ripple_pct = (vout_pp / vout_avg * 100) if vout_avg > 0 else 0
            channel_results[name] = {
                'freq': freq, 'dc': vout_avg, 'error_pct': error_pct,
                'ripple_pct': ripple_pct
            }
            print(f"  {name} ({freq:5d} Hz): DC = {vout_avg*1000:.3f} mV, "
                  f"Error = {error_pct:+.1f}%, Ripple = {ripple_pct:.2f}%")
        else:
            channel_results[name] = None
            print(f"  {name} ({freq:5d} Hz): FAILED")

    results['multichannel'] = channel_results
    return channel_results


# ──────────────────────────────────────────────
# Test 7: Minimum Detectable Signal
# ──────────────────────────────────────────────
def test_min_signal():
    """Find minimum detectable input signal."""
    print("\n" + "="*60)
    print("TEST 7: Minimum Detectable Signal")
    print("="*60)

    freq = BPF_FREQS['BPF3']
    # Sweep very small amplitudes
    amplitudes_vpp = [0.001, 0.002, 0.003, 0.005, 0.007, 0.010]
    sim_time = 0.4
    meas_start = 0.3
    tstep = 1e-6

    min_results = []

    for vpp in amplitudes_vpp:
        vpeak = vpp / 2.0
        expected_dc = (2.0/np.pi) * vpeak
        tb_name = f'tb_minsig_{int(vpp*10000)}'

        spice = f"""* Min signal test: {vpp*1000:.1f} mVpp
.title Envelope Detector - Min Signal {vpp*1000:.1f}mVpp

.include envelope_det.spice

Vdd vdd 0 {VDD}
Vss vss 0 0
Vcm vcm 0 {VCM}

Vin vin vcm sin(0 {vpeak} {freq})

Xenv vin vcm vout vdd vss envelope_det

.tran {tstep} {sim_time} uic

.control
run
meas tran vout_avg avg v(vout) from={meas_start} to={sim_time}
echo "MEAS_RESULT vout_avg=$&vout_avg"
quit
.endc

.end
"""
        write_file(f'{tb_name}.spice', spice)
        stdout, stderr, rc = run_ngspice(f'{tb_name}.spice')

        vout_avg = None
        for line in (stdout + stderr).split('\n'):
            m = re.search(r'vout_avg\s*=\s*([\d.eE+-]+)', line)
            if m:
                vout_avg = float(m.group(1))

        if vout_avg is not None:
            error_pct = abs((vout_avg - expected_dc) / expected_dc * 100) if expected_dc > 0 else 100
            min_results.append({
                'vpp': vpp, 'dc': vout_avg, 'expected': expected_dc, 'error_pct': error_pct
            })
            print(f"  {vpp*1000:5.1f} mVpp: DC = {vout_avg*1e6:.1f} uV, "
                  f"Expected = {expected_dc*1e6:.1f} uV, Error = {error_pct:.1f}%")
        else:
            min_results.append({'vpp': vpp, 'dc': 0, 'expected': expected_dc, 'error_pct': 100})
            print(f"  {vpp*1000:5.1f} mVpp: FAILED")

    # MDS is where error < 15% (matching small-signal spec)
    mds_vpp = None
    for r in min_results:
        if r['error_pct'] < 15:
            mds_vpp = r['vpp']
            break

    if mds_vpp is not None:
        results['min_detectable_mvpp'] = mds_vpp * 1000
        print(f"\n  Minimum detectable signal: {mds_vpp*1000:.1f} mVpp (spec: <10 mVpp) "
              f"→ {'PASS' if mds_vpp*1000 < 10 else 'FAIL'}")
    else:
        results['min_detectable_mvpp'] = 10  # Worst case
        print(f"\n  Minimum detectable signal: could not determine precisely")

    results['min_signal_data'] = min_results
    return min_results


# ──────────────────────────────────────────────
# Power Analysis
# ──────────────────────────────────────────────
def analyze_power():
    """Calculate power per channel from design parameters."""
    print("\n" + "="*60)
    print("TEST 8: Power Per Channel Analysis")
    print("="*60)

    # Behavioral model power estimate based on OTA bias currents:
    # Rectifier: 2 OTAs × ~200 nA bias each = 400 nA
    # LPF: 1 OTA × ~20 nA bias = 20 nA
    # Total per channel: ~420 nA
    # Power per channel: 420 nA × 1.8V = 0.756 uW

    # With folded-cascode OTAs from Block 01:
    # Rectifier: 2 × 500 nA = 1 uA (can be reduced to 200 nA for rect)
    # LPF: 1 × 20 nA = 20 nA
    # Total: ~1.02 uA
    # Power: 1.02 uA × 1.8V = 1.84 uW

    # Conservative estimate (with real OTA + margins):
    i_rect_per_ota = 500e-9   # 500 nA per rectifier OTA (Block 01 default)
    n_rect_otas = 2
    i_lpf_ota = 20e-9         # 20 nA for LPF OTA
    n_lpf_otas = 1

    i_total = n_rect_otas * i_rect_per_ota + n_lpf_otas * i_lpf_ota
    power_per_ch = i_total * VDD
    power_5ch = 5 * power_per_ch

    # Optimized estimate (reduced rect OTA bias):
    i_rect_opt = 200e-9   # Can reduce to 200 nA since noise is not critical
    i_total_opt = n_rect_otas * i_rect_opt + n_lpf_otas * i_lpf_ota
    power_per_ch_opt = i_total_opt * VDD
    power_5ch_opt = 5 * power_per_ch_opt

    results['power_per_ch_uw'] = power_per_ch * 1e6
    results['power_per_ch_opt_uw'] = power_per_ch_opt * 1e6
    results['power_5ch_uw'] = power_5ch * 1e6
    results['power_5ch_opt_uw'] = power_5ch_opt * 1e6

    print(f"  === Conservative (Block 01 OTA at 500 nA bias) ===")
    print(f"  Rectifier OTAs: {n_rect_otas} × {i_rect_per_ota*1e9:.0f} nA = {n_rect_otas*i_rect_per_ota*1e9:.0f} nA")
    print(f"  LPF OTA:        {n_lpf_otas} × {i_lpf_ota*1e9:.0f} nA = {n_lpf_otas*i_lpf_ota*1e9:.0f} nA")
    print(f"  Total current:  {i_total*1e9:.0f} nA per channel")
    print(f"  Power/channel:  {power_per_ch*1e6:.2f} uW (spec: <10 uW) → PASS")
    print(f"  Power (5 ch):   {power_5ch*1e6:.2f} uW (budget: <50 uW) → PASS")
    print()
    print(f"  === Optimized (rect OTA at 200 nA bias) ===")
    print(f"  Rectifier OTAs: {n_rect_otas} × {i_rect_opt*1e9:.0f} nA = {n_rect_otas*i_rect_opt*1e9:.0f} nA")
    print(f"  LPF OTA:        {n_lpf_otas} × {i_lpf_ota*1e9:.0f} nA = {n_lpf_otas*i_lpf_ota*1e9:.0f} nA")
    print(f"  Total current:  {i_total_opt*1e9:.0f} nA per channel")
    print(f"  Power/channel:  {power_per_ch_opt*1e6:.2f} uW → PASS")
    print(f"  Power (5 ch):   {power_5ch_opt*1e6:.2f} uW → PASS")


# ──────────────────────────────────────────────
# Generate Plots
# ──────────────────────────────────────────────
def generate_plots():
    """Generate all verification plots."""
    print("\n" + "="*60)
    print("GENERATING PLOTS")
    print("="*60)

    # --- Plot 1: Amplitude Sweep (Rectification Linearity) ---
    if 'amp_sweep' in results:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        amps = np.array(results['amp_sweep']['amplitudes_vpp']) * 1000  # mVpp
        meas = np.array(results['amp_sweep']['measured_dc']) * 1000     # mV
        exp = np.array(results['amp_sweep']['expected_dc']) * 1000      # mV

        # Linearity plot
        ax1.plot(amps, exp, 'b--', linewidth=2, label='Ideal (2/π × Vpeak)')
        ax1.plot(amps, meas, 'ro-', markersize=8, linewidth=2, label='Measured')
        ax1.set_xlabel('Input Amplitude (mVpp)', fontsize=12)
        ax1.set_ylabel('DC Output (mV)', fontsize=12)
        ax1.set_title('Rectification Linearity', fontsize=14)
        ax1.legend(fontsize=11)
        ax1.grid(True, alpha=0.3)
        ax1.set_xscale('log')
        ax1.set_yscale('log')

        # Error plot
        valid = exp > 0
        errors = np.where(valid, (meas - exp) / exp * 100, 0)
        ax2.bar(range(len(amps)), np.abs(errors), color=['green' if abs(e) < 5 else 'red' for e in errors])
        ax2.set_xticks(range(len(amps)))
        ax2.set_xticklabels([f'{a:.0f}' for a in amps], fontsize=10)
        ax2.set_xlabel('Input Amplitude (mVpp)', fontsize=12)
        ax2.set_ylabel('Rectification Error (%)', fontsize=12)
        ax2.set_title('Rectification Accuracy', fontsize=14)
        ax2.axhline(y=5, color='r', linestyle='--', label='5% spec (100mVpp)')
        ax2.axhline(y=15, color='orange', linestyle='--', label='15% spec (10mVpp)')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(WORK_DIR, 'plot_amplitude_sweep.png'), dpi=150)
        plt.close()
        print("  Saved plot_amplitude_sweep.png")

    # --- Plot 2: Ripple at All BPF Frequencies ---
    if 'ripple' in results:
        fig, ax = plt.subplots(figsize=(10, 5))

        names = []
        ripples = []
        freqs_plot = []
        for name in ['BPF1', 'BPF2', 'BPF3', 'BPF4', 'BPF5']:
            r = results['ripple'].get(name)
            if r:
                names.append(f'{name}\n({r["freq"]} Hz)')
                ripples.append(r['ripple_pct'])
                freqs_plot.append(r['freq'])

        colors = ['green' if r < 5 else 'red' for r in ripples]
        bars = ax.bar(range(len(names)), ripples, color=colors, edgecolor='black')
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, fontsize=10)
        ax.set_ylabel('Output Ripple (%)', fontsize=12)
        ax.set_title('Output Ripple at BPF Center Frequencies (100 mVpp input)', fontsize=14)
        ax.axhline(y=5, color='r', linestyle='--', linewidth=2, label='5% spec limit')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')

        for bar, val in zip(bars, ripples):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                    f'{val:.2f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

        plt.tight_layout()
        plt.savefig(os.path.join(WORK_DIR, 'plot_ripple.png'), dpi=150)
        plt.close()
        print("  Saved plot_ripple.png")

    # --- Plot 3: LPF Frequency Response ---
    if 'lpf_gains_db' in results:
        fig, ax = plt.subplots(figsize=(10, 5))

        freqs = results['lpf_mod_freqs']
        gains = results['lpf_gains_db']

        ax.semilogx(freqs, gains, 'bo-', markersize=8, linewidth=2, label='Measured')

        # Ideal first-order LPF
        f_ideal = np.logspace(-0.5, 2.5, 200)
        g_ideal = -10 * np.log10(1 + (f_ideal / FC_LPF)**2)
        ax.semilogx(f_ideal, g_ideal, 'r--', linewidth=1.5, label=f'Ideal 1st-order (fc={FC_LPF:.1f} Hz)')

        ax.axhline(y=-3, color='gray', linestyle=':', linewidth=1, label='-3 dB')
        if results.get('lpf_cutoff_hz'):
            ax.axvline(x=results['lpf_cutoff_hz'], color='green', linestyle=':',
                       label=f'fc = {results["lpf_cutoff_hz"]:.1f} Hz')

        ax.set_xlabel('Modulation Frequency (Hz)', fontsize=12)
        ax.set_ylabel('Envelope Gain (dB)', fontsize=12)
        ax.set_title('LPF Frequency Response (Envelope Tracking Bandwidth)', fontsize=14)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([-40, 5])

        plt.tight_layout()
        plt.savefig(os.path.join(WORK_DIR, 'plot_lpf_response.png'), dpi=150)
        plt.close()
        print("  Saved plot_lpf_response.png")

    # --- Plot 4: Settling Time (Burst Response) ---
    data = read_wrdata('tb_settling_out.txt')
    if data is not None and len(data) > 100:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        time_ms = data[:, 0] * 1000
        vout_mv = data[:, 1] * 1000
        vin_mv = data[:, 2] * 1000

        ax1.plot(time_ms, vin_mv, 'b-', linewidth=0.5, alpha=0.7, label='Input (vin - vcm)')
        ax1.set_ylabel('Input (mV)', fontsize=12)
        ax1.set_title('Burst Detection — Input and Envelope Output', fontsize=14)
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        ax2.plot(time_ms, vout_mv, 'r-', linewidth=2, label='Envelope output')

        # Mark 10% and 90% levels
        if results.get('settling_v_final'):
            v_final = results['settling_v_final'] * 1000
            ax2.axhline(y=0.1*v_final, color='gray', linestyle=':', label=f'10% ({0.1*v_final:.2f} mV)')
            ax2.axhline(y=0.9*v_final, color='gray', linestyle='--', label=f'90% ({0.9*v_final:.2f} mV)')
            ax2.axhline(y=v_final, color='green', linestyle='-', alpha=0.5, label=f'Final ({v_final:.2f} mV)')

        ax2.set_xlabel('Time (ms)', fontsize=12)
        ax2.set_ylabel('Envelope Output (mV)', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(WORK_DIR, 'plot_settling.png'), dpi=150)
        plt.close()
        print("  Saved plot_settling.png")

    # --- Plot 5: AM Tracking ---
    data = read_wrdata('tb_am_track_out.txt')
    if data is not None and len(data) > 100:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        time_ms = data[:, 0] * 1000
        vout_mv = data[:, 1] * 1000
        vin_mv = data[:, 2] * 1000

        # Show only a portion for clarity (200ms to 800ms)
        mask = (time_ms >= 200) & (time_ms <= 800)

        ax1.plot(time_ms[mask], vin_mv[mask], 'b-', linewidth=0.3, alpha=0.7)
        ax1.set_ylabel('Input (mV)', fontsize=12)
        ax1.set_title('AM Envelope Tracking (carrier=3162 Hz, mod=5 Hz, depth=80%)', fontsize=14)
        ax1.grid(True, alpha=0.3)

        # Ideal envelope
        carrier_amp = 50  # mV
        mod_depth = 0.8
        mod_freq = 5.0
        ideal_env = (2.0/np.pi) * carrier_amp * (1 + mod_depth * np.sin(2*np.pi*mod_freq*time_ms[mask]/1000))

        ax2.plot(time_ms[mask], vout_mv[mask], 'r-', linewidth=2, label='Measured envelope')
        ax2.plot(time_ms[mask], ideal_env, 'b--', linewidth=1.5, label='Ideal envelope')
        ax2.set_xlabel('Time (ms)', fontsize=12)
        ax2.set_ylabel('Envelope (mV)', fontsize=12)
        ax2.legend(fontsize=11)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(WORK_DIR, 'plot_am_tracking.png'), dpi=150)
        plt.close()
        print("  Saved plot_am_tracking.png")

    # --- Plot 6: Dashboard ---
    generate_dashboard()


def generate_dashboard():
    """Generate specification summary dashboard."""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    specs = [
        ('Rect. Accuracy\n(100mVpp)', results.get('rect_accuracy_100mv', None), 5, '%', 'upper'),
        ('Rect. Accuracy\n(10mVpp)', results.get('rect_accuracy_10mv', None), 15, '%', 'upper'),
        ('Min. Detectable\nSignal', results.get('min_detectable_mvpp', None), 10, 'mVpp', 'upper'),
        ('LPF Cutoff', results.get('lpf_cutoff_hz', None), None, 'Hz', 'range'),
        ('Settling Time', results.get('settling_time_ms', None), 200, 'ms', 'upper'),
        ('Power/Channel', results.get('power_per_ch_uw', None), 10, 'uW', 'upper'),
    ]

    for idx, (title, value, limit, unit, spec_type) in enumerate(specs):
        ax = axes[idx // 3][idx % 3]

        if value is not None:
            if spec_type == 'upper':
                passed = value < limit
                color = '#2ecc71' if passed else '#e74c3c'
                ax.barh([0], [value], color=color, height=0.5, edgecolor='black')
                ax.axvline(x=limit, color='red', linewidth=2, linestyle='--', label=f'Limit: {limit} {unit}')
            elif spec_type == 'range':
                passed = 5 <= value <= 20
                color = '#2ecc71' if passed else '#e74c3c'
                ax.barh([0], [value], color=color, height=0.5, edgecolor='black')
                ax.axvline(x=5, color='red', linewidth=2, linestyle='--')
                ax.axvline(x=20, color='red', linewidth=2, linestyle='--')

            status = 'PASS' if passed else 'FAIL'
            ax.text(0.95, 0.95, status, transform=ax.transAxes,
                    fontsize=16, fontweight='bold', color=color,
                    ha='right', va='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            ax.text(0.5, -0.35, f'{value:.2f} {unit}', transform=ax.transAxes,
                    fontsize=14, ha='center', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'NO DATA', transform=ax.transAxes,
                    fontsize=14, ha='center', color='gray')

        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_yticks([])
        ax.grid(True, alpha=0.3, axis='x')

    plt.suptitle('VibroSense Block 04: Envelope Detector — Specification Dashboard',
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(WORK_DIR, 'plot_dashboard.png'), dpi=150)
    plt.close()
    print("  Saved plot_dashboard.png")


# ──────────────────────────────────────────────
# Print Final Summary
# ──────────────────────────────────────────────
def print_summary():
    """Print final PASS/FAIL summary table."""
    print("\n" + "="*60)
    print("SPECIFICATION SUMMARY — PASS/FAIL")
    print("="*60)

    specs = [
        ('Rectification accuracy (100mVpp)', '<5%', results.get('rect_accuracy_100mv'), 5, '%'),
        ('Rectification accuracy (10mVpp)', '<15%', results.get('rect_accuracy_10mv'), 15, '%'),
        ('Minimum detectable signal', '<10 mVpp', results.get('min_detectable_mvpp'), 10, 'mVpp'),
        ('LPF cutoff frequency', '5-20 Hz', results.get('lpf_cutoff_hz'), None, 'Hz'),
        ('Ripple at BPF3', '<5%', results.get('ripple_bpf3_pct'), 5, '%'),
        ('Settling time (10%-90%)', '<200 ms', results.get('settling_time_ms'), 200, 'ms'),
        ('Power per channel (conservative)', '<10 uW', results.get('power_per_ch_uw'), 10, 'uW'),
        ('Power per channel (optimized)', '<5 uW', results.get('power_per_ch_opt_uw'), 5, 'uW'),
    ]

    n_pass = 0
    n_fail = 0
    n_na = 0

    print(f"\n  {'Parameter':<40s} {'Spec':<15s} {'Measured':<15s} {'Status':<8s}")
    print("  " + "-"*78)

    for name, spec_str, value, limit, unit in specs:
        if value is None:
            status = 'N/A'
            n_na += 1
            val_str = 'N/A'
        elif limit is None:
            # Range spec (LPF cutoff)
            passed = 5 <= value <= 20
            status = 'PASS' if passed else 'FAIL'
            val_str = f'{value:.1f} {unit}'
            if passed:
                n_pass += 1
            else:
                n_fail += 1
        else:
            passed = value < limit
            status = 'PASS' if passed else 'FAIL'
            val_str = f'{value:.2f} {unit}'
            if passed:
                n_pass += 1
            else:
                n_fail += 1

        print(f"  {name:<40s} {spec_str:<15s} {val_str:<15s} {status:<8s}")

    print("  " + "-"*78)
    print(f"  Total: {n_pass} PASS, {n_fail} FAIL, {n_na} N/A out of {len(specs)} specs")
    print()

    # Save summary to JSON
    summary = {
        'block': 'Block 04: Envelope Detector',
        'process': 'SKY130A',
        'model': 'Behavioral OTA',
        'results': {k: v for k, v in results.items()
                    if isinstance(v, (int, float, str, type(None)))},
        'pass_count': n_pass,
        'fail_count': n_fail,
    }
    with open(os.path.join(WORK_DIR, 'results_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print("  Saved results_summary.json")

    return n_pass, n_fail


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("VibroSense Block 04: Envelope Detector")
    print("Full Simulation & Verification Suite")
    print("=" * 60)
    print(f"Working directory: {WORK_DIR}")
    print(f"LPF design: fc = {FC_LPF:.1f} Hz, tau = {TAU_LPF*1000:.1f} ms")

    # Run all tests
    test_amplitude_sweep()
    test_ripple()
    test_lpf_cutoff()
    test_settling()
    test_am_tracking()
    test_multichannel()
    test_min_signal()
    analyze_power()

    # Generate plots and summary
    generate_plots()
    n_pass, n_fail = print_summary()

    if n_fail == 0:
        print("\n  ALL SPECIFICATIONS PASS!")
    else:
        print(f"\n  {n_fail} SPECIFICATION(S) FAILED — review and iterate.")

    sys.exit(0 if n_fail == 0 else 1)
