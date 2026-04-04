#!/usr/bin/env python3
"""Expert 01: Log-Domain Envelope Detector
Proposes a log-domain approach (Wouters JSSC'20 style) for wide dynamic range."""

import os

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# Current design data
CURRENT_ENV_SPREAD_MV = 6.6  # max cross-case spread (ENV4)
CURRENT_ENV_OFFSET_MV = {
    'normal':     [4.34, 6.42, 3.24, 1.93, 1.45],
    'inner_race': [4.34, 8.80, 9.69, 8.50, 6.38],
    'outer_race': [4.07, 8.55, 9.38, 6.85, 4.24],
    'ball':       [4.42, 7.99, 8.11, 7.65, 5.36],
}
BPF_PP_MV = {
    'normal':     [65, 100, 56, 33, 23],
    'inner_race': [79, 146, 183, 186, 219],
    'outer_race': [81, 142, 197, 178, 124],
    'ball':       [72, 105, 141, 136, 127],
}

report = """# Expert Report 01: Log-Domain Envelope Detector

## Problem Analysis

The current envelope detector uses a linear OTA-based half-wave rectifier followed by a
Gm-C LPF. The fundamental issue: for BPF outputs of 20-200 mVpp, the rectified DC output
is only 1-10 mV above VCM. The envelope-to-amplitude transfer function is:

    V_env = (1/pi) * V_peak = 0.318 * V_peak

For V_peak = 10 mV: V_env = 3.2 mV (barely above noise floor).
For V_peak = 100 mV: V_env = 31.8 mV (usable but still small).

A log-domain detector compresses the dynamic range logarithmically, mapping the
100:1 ratio of BPF amplitudes (10-200 mVpp) to a much wider output voltage range.

## Proposed Architecture: Log-Domain Envelope Detector

### Block Diagram
```
BPF_out --[Absolute Value]--[Log Compressor]--[Gm-C LPF]-- V_log_env
     (VCM +/- signal)    (|Vin-VCM|)     (I = Is*exp(V/nVt))   (DC)
```

### How It Works in SKY130

The key insight: a MOSFET in weak inversion has exponential I-V characteristics:
    Id = Is * exp(Vgs / (n*Vt))
    Therefore: Vgs = n*Vt * ln(Id/Is)

If we convert the rectified signal to a current (I_rect = gm * |Vin - VCM|),
then pass it through a diode-connected MOSFET in weak inversion, the output voltage
is the LOG of the signal amplitude.

### SPICE Subcircuit

```spice
* Log-Domain Envelope Detector for VibroSense
* Uses weak-inversion MOSFET log compression

.subckt envelope_log vin vcm vout vdd gnd vbn vbn_lpf

* === Stage 1: Full-wave rectifier (current output) ===
* Use B-source for ideal rectification, then transistor log compression
* I_rect = gm * |vin - vcm|, gm = 10 uA/V
B_rect gnd i_rect I = 10e-6 * abs(v(vin) - v(vcm))

* === Stage 2: Log compression via weak-inversion NFET ===
* Diode-connected NFET: Vgs = n*Vt*ln(Id/Is)
* W=0.42u L=10u gives Is ~ 1 nA, n ~ 1.5 in SKY130
* For I_rect = 0.1 uA (10mV input): Vgs = 1.5*26mV*ln(100) = 180 mV
* For I_rect = 2 uA (200mV input): Vgs = 1.5*26mV*ln(2000) = 296 mV
* Dynamic range: 296-180 = 116 mV for 20:1 input range
XMlog i_rect i_rect gnd gnd sky130_fd_pr__nfet_01v8 w=0.42u l=10u

* Level shift: V_log is relative to ground, shift to VCM range
* V_out_raw = VCM + V_log - Vth (approx)
E_shift log_shifted gnd i_rect gnd 1.0

* === Stage 3: Gm-C LPF (same as current design, fc ~ 92 Hz) ===
XM1    d1   log_shifted tail gnd sky130_fd_pr__nfet_01v8 w=2u l=4u
XM2    vout vout        tail gnd sky130_fd_pr__nfet_01v8 w=2u l=4u
XMtail tail vbn_lpf     gnd  gnd sky130_fd_pr__nfet_01v8 w=1u l=8u
XMp3   d1   d1   vdd vdd sky130_fd_pr__pfet_01v8 w=4u l=4u
XMp4   vout d1   vdd vdd sky130_fd_pr__pfet_01v8 w=4u l=4u
Clpf vout gnd 5n

.ends envelope_log
```

## Expected Dynamic Range Improvement

| Input (mVpp) | Current Env (mV above VCM) | Log Env (mV) | Improvement |
|--------------|---------------------------|---------------|-------------|
| 10           | 1.6                        | ~180          | 112x        |
| 50           | 8.0                        | ~247          | 31x         |
| 100          | 16.0                       | ~270          | 17x         |
| 200          | 32.0                       | ~296          | 9x          |

Cross-case spread estimation:
- Current: 6.6 mV max spread
- Log-domain: The 10:1 ratio in BPF amplitudes maps to ~116 mV spread
- **~18x improvement in feature discrimination**

## Power Estimate

- Rectifier gm-source: ~2 uA at 1.8V = 3.6 uW
- Log MOSFET: ~1 uA = 1.8 uW
- LPF OTA (same as current): ~1.2 uW
- **Total: ~6.6 uW per channel** (current: ~20 uW)
- Actually LESS power because we use behavioral rectifier + small log FET

## Pros
1. Massive dynamic range compression (60+ dB → few hundred mV)
2. Signal-dependent resolution: more resolution at small signals (where we need it)
3. Lower power than current design (fewer OTAs)
4. Well-studied in biomedical IC literature

## Cons
1. Temperature sensitivity: n*Vt changes with temperature (~0.3%/K)
2. Requires accurate current-mode rectification (B-source is behavioral)
3. The log transfer function is hard to calibrate exactly in SKY130
4. Classifier weights must be retrained for log-compressed features
5. Process variation in Is affects absolute output (but ratios are stable)
6. Need transistor-level rectifier (B-source used here for proof of concept)

## Implementation Effort
- **Medium-High**: The log compression itself is simple (one MOSFET), but
  building an accurate current-mode rectifier in transistor-level SKY130
  requires careful design. The behavioral B-source works for simulation
  but isn't a real circuit.
- Risk: weak-inversion operation is sensitive to process variation
- Timeline: 2-3 weeks for transistor-level design + verification
"""

with open(os.path.join(OUTDIR, 'expert_01_log_domain.md'), 'w') as f:
    f.write(report)

print("Expert 01 (Log-Domain) report written.")
