#!/usr/bin/env python3
"""Compare behavioral vs transistor-level envelope detector."""

import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import re

WORK_DIR = os.path.dirname(os.path.abspath(__file__))

def run_ngspice(spice_file, timeout=180):
    proc = subprocess.run(['ngspice', '-b', spice_file], capture_output=True,
                          text=True, timeout=timeout, cwd=WORK_DIR)
    return proc.stdout + proc.stderr

def test_amplitude(model_type, vpp, freq=3162):
    """Run a single amplitude test."""
    vpeak = vpp / 2.0

    if model_type == 'behavioral':
        spice = f"""* Behavioral envelope det - {vpp*1000:.0f}mVpp
.title Behavioral Amp Test
.include envelope_det.spice
Vdd vdd 0 1.8
Vss vss 0 0
Vcm vcm 0 0.9
Vin vin vcm sin(0 {vpeak} {freq})
Xenv vin vcm vout vdd vss envelope_det
.tran 1u 400m uic
.control
run
meas tran vout_avg avg v(vout) from=300m to=400m
echo "RESULT vout_avg=$&vout_avg"
quit
.endc
.end
"""
    else:  # transistor-level
        spice = f"""* Transistor-level envelope det - {vpp*1000:.0f}mVpp
.title Transistor-Level Amp Test
.include "../01_ota/models/sky130_fd_pr__nfet_01v8__tt_standalone.spice"
.include "../01_ota/models/sky130_fd_pr__pfet_01v8__tt_standalone.spice"
.include envelope_det_tran.spice
Vdd vdd 0 1.8
Vss vss 0 0
Vcm vcm 0 0.9
Vbn_lpf vbn_lpf 0 0.58
Vin vin vcm sin(0 {vpeak} {freq})
Xenv vin vcm vout vdd vss vbn_lpf envelope_det_tran
.tran 1u 500m uic
.control
run
meas tran vout_avg avg v(vout) from=400m to=500m
echo "RESULT vout_avg=$&vout_avg"
quit
.endc
.end
"""

    fname = f'tb_cmp_{model_type}_{int(vpp*1000)}.spice'
    with open(os.path.join(WORK_DIR, fname), 'w') as f:
        f.write(spice)

    out = run_ngspice(fname)
    m = re.search(r'vout_avg\s*=\s*([\d.eE+-]+)', out)
    if m:
        return float(m.group(1))
    return None


def main():
    print("=" * 60)
    print("Behavioral vs Transistor-Level Comparison")
    print("=" * 60)

    amplitudes = [0.010, 0.020, 0.050, 0.100, 0.200, 0.500]
    vcm = 0.9

    behav_results = []
    tran_results = []
    expected = []

    for vpp in amplitudes:
        vpeak = vpp / 2.0
        exp_dc = (2.0/np.pi) * vpeak
        expected.append(exp_dc)

        # Behavioral
        v_b = test_amplitude('behavioral', vpp)
        behav_results.append(v_b)

        # Transistor-level (output at VCM + envelope)
        v_t = test_amplitude('transistor', vpp)
        if v_t is not None:
            v_t -= vcm  # Remove VCM offset
        tran_results.append(v_t)

        err_b = ((v_b - exp_dc)/exp_dc*100) if v_b else None
        err_t = ((v_t - exp_dc)/exp_dc*100) if v_t else None

        print(f"  {vpp*1000:6.0f} mVpp: Behav={v_b*1000:.3f}mV "
              f"Tran={v_t*1000:.3f}mV "
              f"Expected={exp_dc*1000:.3f}mV "
              f"Err_B={err_b:+.1f}% Err_T={err_t:+.1f}%")

    # Plot comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    amps_mv = np.array(amplitudes) * 1000
    exp_mv = np.array(expected) * 1000
    beh_mv = np.array([v*1000 if v else 0 for v in behav_results])
    tra_mv = np.array([v*1000 if v else 0 for v in tran_results])

    ax1.plot(amps_mv, exp_mv, 'k--', linewidth=2, label='Ideal (2/π × Vpeak)')
    ax1.plot(amps_mv, beh_mv, 'bo-', markersize=8, linewidth=2, label='Behavioral')
    ax1.plot(amps_mv, tra_mv, 'rs-', markersize=8, linewidth=2, label='Transistor-level')
    ax1.set_xlabel('Input Amplitude (mVpp)')
    ax1.set_ylabel('DC Output (mV)')
    ax1.set_title('Rectification Linearity: Behavioral vs Transistor-Level')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    err_b = [(beh_mv[i]-exp_mv[i])/exp_mv[i]*100 for i in range(len(amps_mv))]
    err_t = [(tra_mv[i]-exp_mv[i])/exp_mv[i]*100 for i in range(len(amps_mv))]

    x = np.arange(len(amps_mv))
    w = 0.35
    ax2.bar(x - w/2, np.abs(err_b), w, label='Behavioral', color='blue', alpha=0.7)
    ax2.bar(x + w/2, np.abs(err_t), w, label='Transistor-level', color='red', alpha=0.7)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'{a:.0f}' for a in amps_mv])
    ax2.set_xlabel('Input Amplitude (mVpp)')
    ax2.set_ylabel('Error (%)')
    ax2.set_title('Rectification Error Comparison')
    ax2.axhline(y=5, color='r', linestyle='--', label='5% spec limit')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(WORK_DIR, 'plot_behav_vs_tran.png'), dpi=150)
    plt.close()
    print("\n  Saved plot_behav_vs_tran.png")


if __name__ == '__main__':
    main()
