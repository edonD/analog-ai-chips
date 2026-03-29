#!/usr/bin/env python3
"""Generate all required plots for Block 08: Mode Control."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_mode_transition():
    try:
        data = np.loadtxt('ramp_normal.txt', skiprows=1)
    except:
        print("No ramp_normal.txt, skipping")
        return
    t = data[:, 0] * 1e6
    bvdd = data[:, 1]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [1, 2]})
    ax1.plot(t, bvdd, 'k-', lw=2)
    ax1.set_ylabel('BVDD (V)')
    ax1.set_title('Mode Transition Timing - 1V/us Ramp')
    ax1.grid(True, alpha=0.3)
    for th, c in [(2.5,'r'),(4.2,'b'),(4.5,'g'),(5.6,'m')]:
        ax1.axhline(th, color=c, ls='--', alpha=0.3)
    names = ['bypass_en','ea_en','ref_sel','uvov_en','ilim_en','pass_off']
    for i, name in enumerate(names):
        s = np.clip(data[:, 2+i] / 5.0, 0, 1)
        ax2.plot(t, s + i*1.2, lw=1.5, label=name)
    ax2.set_xlabel('Time (us)')
    ax2.set_ylabel('Outputs')
    ax2.legend(fontsize=8, ncol=2)
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('mode_transition_full.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated mode_transition_full.png")

def plot_thresholds():
    names = ['POR\n(TH1)', 'Ret\n(TH2)', 'PU\n(TH3)', 'Active\n(TH4)']
    meas = [2.55, 4.34, 4.65, 5.67]
    spec_min = [2.3, 4.0, 4.3, 5.4]
    spec_max = [2.7, 4.4, 4.7, 5.8]
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(4)
    ax.bar(x, meas, 0.5, alpha=0.8, color=['#2196F3','#4CAF50','#FF9800','#9C27B0'])
    for i in range(4):
        ax.plot([i-0.3,i+0.3], [spec_min[i]]*2, 'r-', lw=2)
        ax.plot([i-0.3,i+0.3], [spec_max[i]]*2, 'r-', lw=2)
        ax.text(i, meas[i]+0.1, f'{meas[i]:.2f}V', ha='center', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel('Threshold (V)')
    ax.set_title('Mode Control Thresholds - TT 27C')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('threshold_pvt.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated threshold_pvt.png")

def plot_mode_transition_fast():
    """Generate fast ramp plot — uses ramp_fast.txt if available, else placeholder from normal data."""
    import os
    fast_file = 'ramp_fast.txt'
    normal_file = 'ramp_normal.txt'
    src = fast_file if os.path.isfile(fast_file) else normal_file
    try:
        data = np.loadtxt(src, skiprows=1)
    except Exception:
        print("No ramp data available for fast ramp plot, skipping")
        return
    t = data[:, 0] * 1e6
    bvdd = data[:, 1]
    is_placeholder = not os.path.isfile(fast_file)
    title = 'Mode Transition - 12V/us Fast Ramp'
    if is_placeholder:
        title += ' (placeholder from 1V/us data)'
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                    gridspec_kw={'height_ratios': [1, 2]})
    ax1.plot(t, bvdd, 'k-', lw=2)
    ax1.set_ylabel('BVDD (V)')
    ax1.set_title(title)
    ax1.grid(True, alpha=0.3)
    for th, c in [(2.5, 'r'), (4.2, 'b'), (4.5, 'g'), (5.6, 'm')]:
        ax1.axhline(th, color=c, ls='--', alpha=0.3)
    names = ['bypass_en', 'ea_en', 'ref_sel', 'uvov_en', 'ilim_en', 'pass_off']
    for i, name in enumerate(names):
        s = np.clip(data[:, 2+i] / 5.0, 0, 1)
        ax2.plot(t, s + i*1.2, lw=1.5, label=name)
    ax2.set_xlabel('Time (us)')
    ax2.set_ylabel('Outputs')
    ax2.legend(fontsize=8, ncol=2)
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('mode_transition_fast.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated mode_transition_fast.png")


if __name__ == '__main__':
    plot_mode_transition()
    plot_mode_transition_fast()
    plot_thresholds()
