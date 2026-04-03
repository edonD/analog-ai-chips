#!/usr/bin/env python3
"""VibroSense-1 Full-Chain Result Visualization.

Generates publication-quality plots of simulation results.
"""

import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Import the raw file parser from analyze_results
sys.path.insert(0, os.path.dirname(__file__))
from analyze_results import parse_ngspice_raw

BASE = os.path.dirname(os.path.abspath(__file__))
FULLCHAIN = os.path.dirname(BASE)
RESULTS = os.path.join(FULLCHAIN, 'results')
WAVEFORMS = os.path.join(RESULTS, 'waveforms')


def plot_quick_test():
    """Plot the quick 25ms test waveforms."""
    raw_file = os.path.join(RESULTS, 'fullchain_quick.raw')
    if not os.path.exists(raw_file):
        print("No quick test raw file")
        return

    data, _ = parse_ngspice_raw(raw_file)
    time = data['time'] * 1e3  # ms

    os.makedirs(WAVEFORMS, exist_ok=True)

    # --- Plot 1: Full signal chain ---
    fig, axes = plt.subplots(5, 1, figsize=(14, 16), sharex=True)

    # Input
    axes[0].plot(time, data['v(vin)'], 'b-', linewidth=0.5)
    axes[0].set_ylabel('V(in) [V]')
    axes[0].set_title('VibroSense-1 Full Signal Chain (25ms, 1kHz Sine Input)')
    axes[0].axhline(0.9, color='gray', linestyle='--', alpha=0.5)

    # PGA output
    axes[1].plot(time, data['v(vout_pga)'], 'r-', linewidth=0.5)
    axes[1].set_ylabel('V(PGA) [V]')
    axes[1].axhline(0.9, color='gray', linestyle='--', alpha=0.5)
    axes[1].text(0.02, 0.95, 'Gain = 16x', transform=axes[1].transAxes,
                 fontsize=10, va='top')

    # Filter outputs
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    labels = ['BPF1 (224Hz)', 'BPF2 (1kHz)', 'BPF3 (2.25kHz)',
              'BPF4 (3.75kHz)', 'BPF5 (5.2kHz)']
    for i, (c, lbl) in enumerate(zip(colors, labels)):
        axes[2].plot(time, data[f'v(vbpf{i+1}p)'], color=c, linewidth=0.5,
                     label=lbl, alpha=0.7)
    axes[2].set_ylabel('V(BPF) [V]')
    axes[2].legend(loc='upper right', fontsize=7, ncol=3)

    # Envelope outputs
    for i, (c, lbl) in enumerate(zip(colors, labels)):
        axes[3].plot(time, data[f'v(venv{i+1})'], color=c, linewidth=1,
                     label=f'ENV{i+1}')
    axes[3].set_ylabel('V(ENV) [V]')
    axes[3].legend(loc='upper right', fontsize=7, ncol=5)

    # Classifier output
    axes[4].plot(time, data['v(class_out)'], 'k-', linewidth=1)
    axes[4].set_ylabel('Class [V]')
    axes[4].set_xlabel('Time [ms]')
    axes[4].set_yticks([0, 0.45, 0.9, 1.35])
    axes[4].set_yticklabels(['Normal\n(0V)', 'Inner Race\n(0.45V)',
                              'Ball\n(0.9V)', 'Outer Race\n(1.35V)'])

    plt.tight_layout()
    outfile = os.path.join(WAVEFORMS, 'fullchain_quick_test.png')
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {outfile}")

    # --- Plot 2: Power breakdown ---
    results_file = os.path.join(RESULTS, 'quick_test_results.json')
    if os.path.exists(results_file):
        with open(results_file) as f:
            results = json.load(f)

        if 'power_blocks' in results:
            blocks = results['power_blocks']
            names = list(blocks.keys())
            powers = [abs(blocks[n]) for n in names]

            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(names, powers, color='steelblue')
            ax.set_xlabel('Power (uW)')
            ax.set_title('VibroSense-1 Power Breakdown')
            total = sum(powers)
            ax.axvline(total, color='red', linestyle='--',
                       label=f'Total: {total:.1f} uW')
            ax.legend()
            for bar, power in zip(bars, powers):
                ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{power:.1f}', va='center', fontsize=8)

            plt.tight_layout()
            outfile = os.path.join(WAVEFORMS, 'power_breakdown.png')
            plt.savefig(outfile, dpi=150, bbox_inches='tight')
            plt.close()
            print(f"Saved: {outfile}")


def plot_bearing_tests():
    """Plot results from bearing fault test cases."""
    test_cases = ['normal', 'inner_race', 'outer_race', 'ball']
    class_names = ['Normal', 'Inner Race', 'Ball', 'Outer Race']
    expected_class = {'normal': 0, 'inner_race': 1, 'outer_race': 3, 'ball': 2}

    available = []
    for tc in test_cases:
        raw = os.path.join(RESULTS, f'fullchain_{tc}.raw')
        if os.path.exists(raw):
            available.append(tc)

    if not available:
        print("No bearing test results available yet")
        return

    os.makedirs(WAVEFORMS, exist_ok=True)

    # --- Plot: Comparison across test cases ---
    n_tests = len(available)
    fig, axes = plt.subplots(n_tests, 4, figsize=(20, 4*n_tests))
    if n_tests == 1:
        axes = axes.reshape(1, -1)

    for row, tc in enumerate(available):
        data, _ = parse_ngspice_raw(os.path.join(RESULTS, f'fullchain_{tc}.raw'))
        time = data['time'] * 1e3

        # Column 1: Input
        axes[row, 0].plot(time, data['v(vin)'], 'b-', linewidth=0.3)
        axes[row, 0].set_ylabel(f'{tc}\nV(in) [V]')
        axes[row, 0].set_ylim(0, 1.8)

        # Column 2: Envelope outputs
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        for i, c in enumerate(colors):
            if f'v(venv{i+1})' in data:
                axes[row, 1].plot(time, data[f'v(venv{i+1})'], color=c,
                                  linewidth=0.5, label=f'ENV{i+1}')
        axes[row, 1].set_ylabel('V(ENV) [V]')
        if row == 0:
            axes[row, 1].legend(fontsize=6, ncol=5)

        # Column 3: RMS and Peak
        if 'v(rms_out)' in data:
            axes[row, 2].plot(time, data['v(rms_out)'], 'r-', linewidth=1,
                              label='RMS')
        if 'v(peak_out)' in data:
            axes[row, 2].plot(time, data['v(peak_out)'], 'b-', linewidth=1,
                              label='Peak')
        axes[row, 2].set_ylabel('V [V]')
        if row == 0:
            axes[row, 2].legend(fontsize=8)

        # Column 4: Classifier output
        if 'v(class_out)' in data:
            axes[row, 3].plot(time, data['v(class_out)'], 'k-', linewidth=1)
            axes[row, 3].set_yticks([0, 0.45, 0.9, 1.35])
            axes[row, 3].set_yticklabels(['N', 'IR', 'B', 'OR'], fontsize=7)
            axes[row, 3].set_ylim(-0.2, 1.6)
            exp = expected_class[tc]
            axes[row, 3].axhline(exp * 0.45, color='green', linestyle='--',
                                 alpha=0.5, label=f'Expected: {class_names[exp]}')
            axes[row, 3].legend(fontsize=7)

    for j in range(4):
        axes[-1, j].set_xlabel('Time [ms]')

    titles = ['Input Stimulus', 'Envelope Features', 'RMS/Peak',
              'Classifier Output']
    for j, t in enumerate(titles):
        axes[0, j].set_title(t)

    plt.suptitle('VibroSense-1 Full-Chain Bearing Fault Classification',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    outfile = os.path.join(WAVEFORMS, 'bearing_test_comparison.png')
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {outfile}")


def main():
    plot_quick_test()
    plot_bearing_tests()
    print("\nAll plots generated.")


if __name__ == '__main__':
    main()
