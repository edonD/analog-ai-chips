#!/usr/bin/env python3
"""
Visualize how VibroSense-1 detects bearing faults.

Shows the full signal flow from raw vibration → frequency bands →
envelope voltages → capacitor scoring → classification decision.
"""

import numpy as np
from scipy.signal import butter, lfilter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Generate realistic synthetic vibration signals for each fault type
# ---------------------------------------------------------------------------

def make_vibration(fault_type, fs=12000, duration=0.1):
    """Generate a vibration signal that looks like a real bearing fault."""
    t = np.arange(int(fs * duration)) / fs
    n = len(t)
    rng = np.random.RandomState(42)

    # Base signal: shaft rotation at ~30 Hz + harmonics
    signal = 0.3 * np.sin(2 * np.pi * 30 * t)
    signal += 0.1 * np.sin(2 * np.pi * 60 * t)
    signal += rng.normal(0, 0.05, n)  # noise floor

    if fault_type == 'Normal':
        pass  # just the base

    elif fault_type == 'Inner Race':
        # Inner race defects: strong energy at 1500-3000 Hz
        # Characteristic: amplitude-modulated at shaft speed
        carrier = np.sin(2 * np.pi * 2200 * t)
        modulation = 0.5 + 0.5 * np.sin(2 * np.pi * 30 * t)
        signal += 0.8 * carrier * modulation
        signal += 0.3 * np.sin(2 * np.pi * 1800 * t)
        # Some impulses
        impulse_period = int(fs / 150)  # ~150 Hz BPFI
        for k in range(0, n, impulse_period):
            if k < n:
                width = min(20, n - k)
                signal[k:k+width] += 0.6 * np.exp(-np.arange(width) / 5)

    elif fault_type == 'Ball':
        # Ball defects: energy at 3000-4500 Hz
        signal += 0.7 * np.sin(2 * np.pi * 3800 * t)
        signal += 0.4 * np.sin(2 * np.pi * 4200 * t)
        # Irregular impulses (ball defect modulates irregularly)
        impulse_period = int(fs / 120)
        for k in range(0, n, impulse_period):
            jitter = rng.randint(-10, 10)
            pos = k + jitter
            if 0 <= pos < n - 20:
                signal[pos:pos+15] += 0.8 * np.exp(-np.arange(15) / 4)

    elif fault_type == 'Outer Race':
        # Outer race: energy at 4500-5900 Hz + high broadband RMS
        signal += 1.0 * np.sin(2 * np.pi * 5200 * t)
        signal += 0.6 * np.sin(2 * np.pi * 4800 * t)
        signal += 0.5 * np.sin(2 * np.pi * 5500 * t)
        # Strong periodic impulses at BPFO
        impulse_period = int(fs / 90)  # ~90 Hz BPFO
        for k in range(0, n, impulse_period):
            if k < n - 15:
                signal[k:k+15] += 1.2 * np.exp(-np.arange(15) / 3)
        # Higher overall noise floor
        signal += rng.normal(0, 0.2, n)

    return t, signal


# ---------------------------------------------------------------------------
# Main visualization
# ---------------------------------------------------------------------------

def main():
    fs = 12000
    duration = 0.1  # 100ms for visualization
    bands = [(100, 500), (500, 1500), (1500, 3000), (3000, 4500), (4500, 5900)]
    band_names = ['BPF1\n100-500Hz', 'BPF2\n500-1500Hz', 'BPF3\n1500-3000Hz',
                  'BPF4\n3000-4500Hz', 'BPF5\n4500-5900Hz']
    fault_types = ['Normal', 'Inner Race', 'Ball', 'Outer Race']
    colors = ['#2196F3', '#F44336', '#4CAF50', '#FF9800']

    # Load trained weights
    weights_path = os.path.join(SCRIPT_DIR, 'results', 'trained_weights.json')
    with open(weights_path) as f:
        trained = json.load(f)
    W = np.array(trained['quantized_weights'])  # (4, 8)
    B = np.array(trained['quantized_biases'])    # (4,)
    class_names = trained['class_names']

    # Envelope LPF
    tau = 1.0 / (2 * np.pi * 10)
    alpha = 1 - np.exp(-1.0 / (fs * tau))

    # ---------------------------------------------------------------------------
    # Figure: 4 fault types, show raw signal + 5 band energies + neuron scores
    # ---------------------------------------------------------------------------

    fig = plt.figure(figsize=(20, 24))

    for fault_idx, fault_type in enumerate(fault_types):
        t, signal = make_vibration(fault_type, fs, duration)

        # --- Row 1: Raw vibration signal ---
        ax_raw = fig.add_subplot(4, 3, fault_idx * 3 + 1) if fault_idx < 4 else None
        ax_raw = fig.add_axes([0.05, 0.76 - fault_idx * 0.24, 0.28, 0.18])
        ax_raw.plot(t * 1000, signal, color=colors[fault_idx], linewidth=0.5)
        ax_raw.set_title(f'{fault_type}', fontsize=14, fontweight='bold',
                         color=colors[fault_idx])
        ax_raw.set_ylabel('Accel (g)', fontsize=9)
        ax_raw.set_ylim(-3, 3)
        if fault_idx == 3:
            ax_raw.set_xlabel('Time (ms)', fontsize=9)
        ax_raw.grid(True, alpha=0.2)
        ax_raw.tick_params(labelsize=8)

        # --- Filter into 5 bands and get envelope energies ---
        band_energies = []
        for i, (f_low, f_high) in enumerate(bands):
            b, a = butter(2, [f_low, f_high], btype='band', fs=fs)
            filtered = lfilter(b, a, signal)
            rectified = np.abs(filtered)
            envelope = lfilter([alpha], [1, -(1 - alpha)], rectified)
            energy = np.mean(envelope)
            band_energies.append(energy)

        # RMS, crest, kurtosis
        rms_val = np.sqrt(np.mean(signal ** 2))
        crest_val = np.max(np.abs(signal)) / (rms_val + 1e-10)
        from scipy.stats import kurtosis
        kurt_val = kurtosis(signal, fisher=True)

        features = band_energies + [rms_val, crest_val, kurt_val]

        # --- Row 2: Band energy bar chart ---
        ax_bands = fig.add_axes([0.38, 0.76 - fault_idx * 0.24, 0.28, 0.18])
        bar_colors = ['#BBDEFB', '#BBDEFB', '#BBDEFB', '#BBDEFB', '#BBDEFB',
                       '#C8E6C9', '#FFF9C4', '#FFE0B2']

        # Highlight the dominant band for this fault type
        max_band = np.argmax(band_energies)
        highlight = list(bar_colors)
        highlight[max_band] = colors[fault_idx]

        x_labels = ['BPF1', 'BPF2', 'BPF3', 'BPF4', 'BPF5', 'RMS', 'Crest', 'Kurt']
        bars = ax_bands.bar(range(8), features, color=highlight, edgecolor='gray',
                            linewidth=0.5)
        ax_bands.set_xticks(range(8))
        ax_bands.set_xticklabels(x_labels, fontsize=8)
        ax_bands.set_title('8 Feature Voltages', fontsize=11)
        ax_bands.set_ylabel('Voltage (V)', fontsize=9)
        ax_bands.tick_params(labelsize=8)
        ax_bands.grid(True, alpha=0.2, axis='y')

        # Annotate the dominant band
        ax_bands.annotate(f'Loudest!',
                          xy=(max_band, features[max_band]),
                          xytext=(max_band, features[max_band] * 1.15 + 0.05),
                          ha='center', fontsize=8, fontweight='bold',
                          color=colors[fault_idx],
                          arrowprops=dict(arrowstyle='->', color=colors[fault_idx]))

        # --- Row 3: Neuron scores (capacitor dot products) ---
        ax_scores = fig.add_axes([0.72, 0.76 - fault_idx * 0.24, 0.24, 0.18])

        # Compute scores: each neuron = dot(features, weights) + bias
        # Normalize features to [0,1] using the trained normalization
        norm_min = np.array(trained['normalization']['min'])
        norm_max = np.array(trained['normalization']['max'])
        feat_arr = np.array(features)
        feat_norm = np.clip((feat_arr - norm_min) / (norm_max - norm_min + 1e-10), 0, 1)

        scores = W @ feat_norm + B
        winner = np.argmax(scores)

        # Bar chart of neuron scores
        neuron_colors = ['#90CAF9', '#EF9A9A', '#A5D6A7', '#FFCC80']
        neuron_colors[winner] = colors[winner]  # highlight winner

        bars = ax_scores.barh(range(4), scores, color=neuron_colors,
                              edgecolor='gray', linewidth=0.5)
        ax_scores.set_yticks(range(4))
        ax_scores.set_yticklabels(class_names, fontsize=9)
        ax_scores.set_title('Neuron Scores (cap x voltage)', fontsize=11)
        ax_scores.tick_params(labelsize=8)
        ax_scores.grid(True, alpha=0.2, axis='x')

        # Mark the winner
        ax_scores.annotate(f'WINNER',
                           xy=(scores[winner], winner),
                           xytext=(scores[winner] + 0.5, winner),
                           fontsize=10, fontweight='bold', color=colors[winner],
                           va='center')

        # Check if classification is correct
        correct = (winner == fault_idx)
        symbol = 'Correct!' if correct else 'Wrong!'
        ax_scores.text(0.98, 0.02, symbol, transform=ax_scores.transAxes,
                       fontsize=10, ha='right', va='bottom',
                       color='green' if correct else 'red', fontweight='bold')

    # Main title
    fig.suptitle('VibroSense-1: How Capacitors Detect Bearing Faults\n'
                 'Vibration → Filter into bands → Measure energy → '
                 'Capacitors score each class → Winner = diagnosis',
                 fontsize=16, fontweight='bold', y=0.98)

    # Column headers
    fig.text(0.19, 0.955, 'Raw Vibration Signal', ha='center', fontsize=12,
             fontstyle='italic', color='gray')
    fig.text(0.52, 0.955, '8 Feature Voltages (from analog chain)',
             ha='center', fontsize=12, fontstyle='italic', color='gray')
    fig.text(0.84, 0.955, 'Neuron Scores (32 capacitors)',
             ha='center', fontsize=12, fontstyle='italic', color='gray')

    plt.savefig(os.path.join(SCRIPT_DIR, 'results', 'how_detection_works.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: results/how_detection_works.png")

    # ---------------------------------------------------------------------------
    # Figure 2: Capacitor weight map with arrows showing the logic
    # ---------------------------------------------------------------------------

    fig2, axes = plt.subplots(2, 2, figsize=(16, 12))

    for fault_idx, (fault_type, ax) in enumerate(zip(fault_types, axes.flat)):
        t, signal = make_vibration(fault_type, fs, duration)

        # Get band-filtered signals
        for i, (f_low, f_high) in enumerate(bands):
            b, a = butter(2, [f_low, f_high], btype='band', fs=fs)
            filtered = lfilter(b, a, signal)

            # Plot filtered signal (offset for visibility)
            offset = (4 - i) * 1.5
            ax.fill_between(t * 1000, offset - np.abs(filtered) * 0.8,
                            offset + np.abs(filtered) * 0.8,
                            alpha=0.4, color=plt.cm.viridis(i / 5))
            ax.plot(t * 1000, offset + filtered * 0.8,
                    color=plt.cm.viridis(i / 5), linewidth=0.3)

            # Show cap value for this fault's neuron
            cap_val = W[fault_idx, i]
            cap_fF = int(round(cap_val / (trained['quantization']['w_scale']))) * int(trained['quantization']['c_unit_fF'])

            # Annotate with cap value
            ax.text(duration * 1000 + 1, offset,
                    f'{band_names[i].split(chr(10))[0]}: '
                    f'{band_names[i].split(chr(10))[1]}',
                    fontsize=8, va='center', ha='left')

        ax.set_title(f'{fault_type}', fontsize=14, fontweight='bold',
                     color=colors[fault_idx])
        ax.set_ylabel('Frequency Band', fontsize=10)
        ax.set_yticks([i * 1.5 for i in range(5)])
        ax.set_yticklabels(['BPF5', 'BPF4', 'BPF3', 'BPF2', 'BPF1'], fontsize=9)
        ax.set_xlabel('Time (ms)', fontsize=9)
        ax.set_xlim(0, duration * 1000 * 1.5)
        ax.grid(True, alpha=0.1)

    fig2.suptitle('What Each Frequency Band Looks Like for Each Fault Type\n'
                  'The training learned which bands light up for which fault → '
                  'that became capacitor values',
                  fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig(os.path.join(SCRIPT_DIR, 'results', 'band_signatures.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: results/band_signatures.png")

    # ---------------------------------------------------------------------------
    # Figure 3: The capacitor "multiplication" — most intuitive view
    # ---------------------------------------------------------------------------

    fig3, axes3 = plt.subplots(1, 4, figsize=(20, 6))

    for fault_idx, (fault_type, ax) in enumerate(zip(fault_types, axes3)):
        t, signal = make_vibration(fault_type, fs, duration)

        # Extract features
        band_energies = []
        for f_low, f_high in bands:
            b, a = butter(2, [f_low, f_high], btype='band', fs=fs)
            filtered = lfilter(b, a, signal)
            rectified = np.abs(filtered)
            envelope = lfilter([alpha], [1, -(1 - alpha)], rectified)
            band_energies.append(np.mean(envelope))

        rms_val = np.sqrt(np.mean(signal ** 2))
        crest_val = np.max(np.abs(signal)) / (rms_val + 1e-10)
        kurt_val = kurtosis(signal, fisher=True)
        features = np.array(band_energies + [rms_val, crest_val, kurt_val])

        # Normalize
        feat_norm = np.clip((features - norm_min) / (norm_max - norm_min + 1e-10), 0, 1)

        # For each neuron, show feature * weight product
        feat_labels = ['BPF1', 'BPF2', 'BPF3', 'BPF4', 'BPF5', 'RMS', 'Crst', 'Kurt']
        x = np.arange(8)
        width = 0.18

        for cls in range(4):
            products = feat_norm * W[cls]
            offset = (cls - 1.5) * width
            clr = colors[cls]
            alpha_val = 1.0 if cls == fault_idx else 0.25
            ax.bar(x + offset, products, width, color=clr, alpha=alpha_val,
                   edgecolor='gray' if cls == fault_idx else 'none',
                   linewidth=0.5 if cls == fault_idx else 0)

        ax.set_xticks(x)
        ax.set_xticklabels(feat_labels, fontsize=8)
        ax.set_title(f'Input: {fault_type}', fontsize=12, fontweight='bold',
                     color=colors[fault_idx])
        ax.set_ylabel('Feature x Weight (cap contribution)' if fault_idx == 0 else '',
                      fontsize=9)
        ax.tick_params(labelsize=8)
        ax.grid(True, alpha=0.2, axis='y')

        # Show total scores
        scores = W @ feat_norm + B
        winner = np.argmax(scores)
        result = class_names[winner]
        ax.text(0.5, -0.15, f'Winner: {result}',
                transform=ax.transAxes, ha='center', fontsize=11,
                fontweight='bold', color=colors[winner],
                bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[winner],
                          alpha=0.15))

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors[i], label=class_names[i])
                       for i in range(4)]
    fig3.legend(handles=legend_elements, loc='upper center', ncol=4,
                fontsize=11, bbox_to_anchor=(0.5, 0.98))

    fig3.suptitle('Capacitor x Voltage Products — How Each Neuron Scores\n'
                  'Bright bars = the winning neuron. '
                  'Big cap on a loud band = high score = that neuron wins.',
                  fontsize=14, fontweight='bold', y=1.06)
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'results', 'capacitor_scoring.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: results/capacitor_scoring.png")


if __name__ == '__main__':
    main()
