#!/usr/bin/env python3
"""TB2: Multi-tone intermodulation analysis.

With a perfectly linear behavioral OTA, each channel's output contains
ONLY the tone at its own f0 (no intermod products). This validates the
topology provides inherent channel isolation through frequency selectivity.
"""
import numpy as np
import json

channels = {
    1: {'f0': 224},
    2: {'f0': 1000},
    3: {'f0': 3162},
    4: {'f0': 7071},
    5: {'f0': 14142},
}

all_f0 = [224, 1000, 3162, 7071, 14142]

print("=" * 78)
print("TB2: Multi-Tone Intermodulation Test")
print("=" * 78)
print("Input: 5 simultaneous tones (100 mVpk each) at all channel f0 values\n")

results = {}
all_pass = True

for ch in range(1, 6):
    f0 = channels[ch]['f0']
    data = np.loadtxt(f'intermod_ch{ch}.txt')
    time = data[:, 0]
    vout = data[:, 1]

    vout_ac = vout - np.mean(vout)

    # FFT
    N = len(vout_ac)
    dt = np.mean(np.diff(time))
    fft_mag = 2.0 * np.abs(np.fft.rfft(vout_ac * np.hanning(N))) / N
    fft_freqs = np.fft.rfftfreq(N, dt)

    # Desired tone magnitude
    desired_idx = np.argmin(np.abs(fft_freqs - f0))
    desired_mag = fft_mag[desired_idx]

    # Check other channel tones at this output
    print(f"Ch{ch} output (f0={f0}Hz): desired={desired_mag*1000:.3f}mV")
    ch_pass = True
    intermod_worst = 0

    for other_f0 in all_f0:
        if other_f0 == f0:
            continue
        other_idx = np.argmin(np.abs(fft_freqs - other_f0))
        other_mag = fft_mag[other_idx]
        if desired_mag > 0:
            rejection = 20 * np.log10(desired_mag / (other_mag + 1e-30))
        else:
            rejection = 0
        passes = rejection > 20
        if not passes:
            ch_pass = False
            all_pass = False
        if rejection < intermod_worst or intermod_worst == 0:
            intermod_worst = rejection
        print(f"  Tone @{other_f0}Hz: {other_mag*1000:.4f}mV "
              f"(rejection: {rejection:.1f}dB) {'PASS' if passes else 'FAIL'}")

    # Also check common intermod products (f1±f2)
    for i, fi in enumerate(all_f0):
        for j, fj in enumerate(all_f0):
            if i >= j:
                continue
            for f_im in [fi + fj, abs(fi - fj)]:
                if f_im < 1 or f_im > fft_freqs[-1]:
                    continue
                im_idx = np.argmin(np.abs(fft_freqs - f_im))
                im_mag = fft_mag[im_idx]
                if desired_mag > 0:
                    im_rej = 20 * np.log10(desired_mag / (im_mag + 1e-30))
                else:
                    im_rej = 0
                # Only report if within this channel's passband
                bw = f0 / channels[ch].get('Q', 1.0) if 'Q' in channels[ch] else f0
                if abs(f_im - f0) < bw:
                    if im_rej < 20:
                        print(f"  IM @{f_im}Hz: {im_mag*1000:.4f}mV "
                              f"(rejection: {im_rej:.1f}dB) WARN")

    results[ch] = {
        'desired_mV': round(float(desired_mag * 1000), 3),
        'worst_intermod_rejection_dB': round(float(intermod_worst), 1),
        'pass': ch_pass,
    }
    print(f"  → Channel {ch}: {'PASS' if ch_pass else 'FAIL'} "
          f"(worst rejection: {intermod_worst:.1f}dB)")

print(f"\n{'='*78}")
print(f"TB2 OVERALL: {'ALL PASS' if all_pass else 'FAIL'}")
print(f"{'='*78}")

with open('tb2_results.json', 'w') as f:
    json.dump(results, f, indent=2)
