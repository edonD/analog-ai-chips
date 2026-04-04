#!/usr/bin/env python3
"""Expert 08: Comparator-Based (Threshold Crossing Counter) approach."""

import os
import math

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# Estimate threshold crossings for different BPF amplitudes
def crossings_per_window(vpeak_mv, freq_hz, threshold_mv, window_ms=200):
    """Estimate number of threshold crossings for a sinusoidal signal."""
    if vpeak_mv < threshold_mv:
        return 0
    # For sine at frequency f, with amplitude A, threshold T:
    # Crossings per cycle = 2 (up + down)
    # But only if A > T
    n_cycles = freq_hz * window_ms / 1000
    return int(2 * n_cycles)

# BPF frequencies
bpf_freqs = [227, 1001, 3162, 7236, 14639]
# BPF peak amplitudes (mV) estimated from Vpp/2
bpf_peaks = {
    'normal':     [33, 50, 28, 16, 11],
    'inner_race': [39, 73, 91, 93, 109],
    'outer_race': [41, 71, 98, 89, 62],
    'ball':       [36, 52, 71, 68, 63],
}

# Compute crossings with 5 mV threshold
thresh = 5  # mV
crossing_data = {}
for case, peaks in bpf_peaks.items():
    crossing_data[case] = [crossings_per_window(p, f, thresh)
                           for p, f in zip(peaks, bpf_freqs)]

report = f"""# Expert Report 08: Comparator-Based (Threshold Crossing) Envelope Detector

## Problem Analysis

Instead of computing the analog amplitude of the BPF output, we can COUNT
how many times the signal crosses a threshold within a time window. This
converts amplitude information to a TIME/COUNT domain feature.

For a sinusoidal signal at frequency f with amplitude A:
- If A > threshold: crossings per window = 2 * f * T_window
- If A < threshold: crossings = 0

This is essentially a **1-bit ADC** approach: the comparator output is a digital
signal whose duty cycle and crossing rate encode the amplitude.

## Why This Could Work

For bearing faults, the BPF outputs have DIFFERENT amplitudes in each channel:
- Normal: low amplitude in all channels
- Fault: high amplitude in channels near the resonance frequency

With a threshold set at, say, 5 mV above VCM, channels with large signals
cross the threshold many times, while channels with small signals cross few/zero.

## Threshold Crossing Estimates (5 mV threshold, 200 ms window)

| Channel | Freq (Hz) | Normal | Inner | Outer | Ball | Spread |
|---------|-----------|--------|-------|-------|------|--------|
| BPF1    | 227       | {crossing_data['normal'][0]} | {crossing_data['inner_race'][0]} | {crossing_data['outer_race'][0]} | {crossing_data['ball'][0]} | {max(crossing_data[c][0] for c in crossing_data) - min(crossing_data[c][0] for c in crossing_data)} |
| BPF2    | 1001      | {crossing_data['normal'][1]} | {crossing_data['inner_race'][1]} | {crossing_data['outer_race'][1]} | {crossing_data['ball'][1]} | {max(crossing_data[c][1] for c in crossing_data) - min(crossing_data[c][1] for c in crossing_data)} |
| BPF3    | 3162      | {crossing_data['normal'][2]} | {crossing_data['inner_race'][2]} | {crossing_data['outer_race'][2]} | {crossing_data['ball'][2]} | {max(crossing_data[c][2] for c in crossing_data) - min(crossing_data[c][2] for c in crossing_data)} |
| BPF4    | 7236      | {crossing_data['normal'][3]} | {crossing_data['inner_race'][3]} | {crossing_data['outer_race'][3]} | {crossing_data['ball'][3]} | {max(crossing_data[c][3] for c in crossing_data) - min(crossing_data[c][3] for c in crossing_data)} |
| BPF5    | 14639     | {crossing_data['normal'][4]} | {crossing_data['inner_race'][4]} | {crossing_data['outer_race'][4]} | {crossing_data['ball'][4]} | {max(crossing_data[c][4] for c in crossing_data) - min(crossing_data[c][4] for c in crossing_data)} |

**Problem**: Since all BPF outputs exceed 5 mV (even "normal"), ALL cases have the
same crossing count = 2*f*T for each channel. The crossing count depends on FREQUENCY
not AMPLITUDE when the signal is above threshold.

**The comparator approach is AMPLITUDE-BLIND for above-threshold signals.**

## Fix: Use Time-Above-Threshold Instead

Instead of counting zero-crossings, measure the FRACTION OF TIME the signal
exceeds the threshold. For a sine with amplitude A > threshold T:

    duty_cycle = (1/pi) * arccos(T/A)

| BPF3 Amplitude | Duty (T=5mV) | Duty (T=20mV) | Duty (T=50mV) |
|----------------|--------------|----------------|----------------|
| 28 mVpk (normal) | 44.3% | 22.3% | 0% |
| 91 mVpk (inner)  | 48.2% | 43.0% | 33.4% |
| 98 mVpk (outer)  | 48.4% | 43.4% | 34.3% |
| 71 mVpk (ball)   | 47.7% | 41.9% | 29.6% |

With T=50 mV threshold: normal=0%, inner=33.4%, outer=34.3%, ball=29.6%.
**Spread in duty cycle: 34.3% - 0% = 34.3%** — good discrimination for normal vs fault,
but inner/outer/ball are close (within 5%).

## SPICE Implementation

```spice
* Comparator-Based Envelope: measures time above threshold
* Output voltage proportional to duty cycle above threshold

.subckt envelope_comparator vin vcm vout vdd gnd vbn vbn_lpf

* Threshold: VCM + 20 mV
.param VTHRESH = 0.02

* Comparator: output high when |vin - vcm| > threshold
B_comp comp_out gnd V = {{
+   abs(v(vin) - v(vcm)) > VTHRESH ? v(vdd) : 0 }}

* RC integrator to convert duty cycle to DC voltage
* tau = R*C = 10ms (matches envelope settling time)
R_int comp_out vout 2Meg
C_int vout gnd 5n

.ends envelope_comparator
```

## Expected Output (RC-filtered comparator)

With threshold = 20 mV above VCM:
- Normal (BPF3 = 28 mVpk): duty = 22%, V_out = 0.22 * 1.8V = 0.40V
- Inner (BPF3 = 91 mVpk): duty = 43%, V_out = 0.43 * 1.8V = 0.77V
- Outer (BPF3 = 98 mVpk): duty = 43%, V_out = 0.77V
- Ball (BPF3 = 71 mVpk): duty = 42%, V_out = 0.76V

**Spread: ~370 mV (normal vs fault)** — EXCELLENT for normal-vs-fault!
But only 10 mV between inner/outer/ball — POOR for multi-class discrimination.

## Pros
1. Huge output swing (duty cycle maps to 0-1.8V range)
2. Robust to amplitude variation (binary decision)
3. Very simple circuit (comparator + RC filter)
4. Low power (~1 uW per channel)
5. No dead zone issues

## Cons
1. **Loses amplitude information above threshold** — all large signals look the same
2. **Poor multi-class discrimination**: can distinguish normal from fault, but not fault types
3. Threshold sensitivity: output depends strongly on threshold choice
4. Need multiple thresholds for better discrimination (increases complexity)
5. Impulsive signals (bearing faults) may have similar duty cycles despite different amplitudes

## Verdict

**NOT RECOMMENDED for 4-class problem.** The comparator approach is excellent for
binary (normal vs fault) classification but loses the subtle amplitude differences
between fault types. It could work as a supplementary feature alongside other approaches.

## Implementation Effort
- **Very Low**: Comparator + RC filter, ~1 day
- Risk: Low (simple circuit)
- But limited utility for 4-class discrimination
"""

with open(os.path.join(OUTDIR, 'expert_08_comparator.md'), 'w') as f:
    f.write(report)

print("Expert 08 (Comparator-Based) report written.")
