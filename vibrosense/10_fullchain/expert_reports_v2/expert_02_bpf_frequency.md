# Expert Report 02: BPF Frequency Response Analysis

## 1. BPF Architecture

Each BPF channel uses a Tow-Thomas biquad topology with 3 OTAs per path
(pseudo-differential = 6 OTAs per channel, 30 total for 5 channels).

Topology per half-circuit:
- OTA1: gm-integrator (vinp -> C1 through int2p)
- OTA2: gm-integrator (int1p -> C2 through vcm)
- OTA3: positive feedback (vcm -> int1p, sets Q)
- Pseudo-resistors for DC bias

Transfer function: H(s) = (gm1/C1) * s / [s^2 + (gm3/C1)*s + gm1*gm2/(C1*C2)]
- Center freq: f0 = (1/2pi) * sqrt(gm1*gm2/(C1*C2))
- Q = sqrt(gm1*gm2*C1*C2) / (gm3*C1) = sqrt(C2/C1) when all gm equal
- Passband gain: gm1/gm3 = 1 (unity) when OTAs are identical

## 2. OTA Characteristics

The BPF uses `ota_foldcasc` with these bias conditions:
- VBN = 0.5973V, VBCN = 0.8273V, VBP = 0.81V, VBCP = 0.555V
- Tail current: ~500 nA (from bias generator design)
- Input pair: W=5u L=14u NMOS
- gm estimated: ~6-10 uS at 250nA per side (conservative)

**CRITICAL**: All 5 BPF channels share the SAME bias voltages in the full-chain netlist.
However, BPF ch4 and ch5 were tuned with DIFFERENT bias voltages:
- Ch4: VBN=0.6399, VBP=0.745, VBCN=0.8699, VBCP=0.49 (Iref=440nA)
- Ch5: VBN=0.6914, VBP=0.66, VBCN=0.9214, VBCP=0.405 (Iref=870nA)

**This is a significant error**: Ch4 and Ch5 require higher OTA gm (via higher
bias current) to reach their target frequencies. Using the Ch1 bias (200nA)
will make Ch4 and Ch5 center frequencies too LOW.

## 3. Channel Specifications vs Actual

| Ch | f0 target | f0 tuned | Q   | C1 (pF) | C2 (pF) | Iref (nA) | Bias match? |
|----|-----------|----------|-----|---------|---------|-----------|-------------|
| 1  | 224 Hz | 226.6 Hz | 0.79 | 586.0 | 1042.0 | 200 | YES |
| 2  | 1000 Hz | 1001.4 Hz | 0.707 | 118.0 | 260.0 | 200 | YES |
| 3  | 3162 Hz | 3162.0 Hz | 1.108 | 58.0 | 53.0 | 200 | YES |
| 4  | 7071 Hz | 7235.8 Hz | 1.42 | 59.0 | 29.7 | 440 | **NO** |
| 5  | 14142 Hz | 14639.4 Hz | 1.408 | 41.8 | 21.0 | 870 | **NO** |

## 4. Impact of Wrong Bias on Ch4 and Ch5

When Ch4 is biased at 200nA instead of 440nA:
- gm drops by factor of sqrt(440/200) = 1.48x (subthreshold)
- f0 proportional to gm -> f0 drops from 7236 Hz to ~4900 Hz
- This is now overlapping with Ch3 (3162 Hz) territory

When Ch5 is biased at 200nA instead of 870nA:
- gm drops by factor of sqrt(870/200) = 2.09x
- f0 drops from 14639 Hz to ~7000 Hz
- This now overlaps with Ch4's intended band

**Result**: Channels 3, 4, and 5 may all be sensing similar frequency ranges,
destroying the spectral decomposition that the classifier relies on.

## 5. Do the BPF Center Frequencies Match Bearing Fault Frequencies?

Bearing fault characteristic frequencies (6205 bearing at 1797 RPM):
- FTF (cage): ~12 Hz
- BSF (ball): ~70.6 Hz
- BPFO (outer race): ~107.4 Hz
- BPFI (inner race): ~162.2 Hz

These are FUNDAMENTAL fault frequencies. In real bearings, faults excite
**structural resonances** at much higher frequencies (1-10 kHz), modulated
at the fault frequency. The BPF should capture these resonances, not the
fundamental fault frequencies directly.

Training config band definitions:
- Band 1: 100-500 Hz (structural, low-freq)
- Band 2: 500-1500 Hz (mid-freq bearing tones)
- Band 3: 1500-3000 Hz (high-freq defect harmonics)
- Band 4: 3000-4500 Hz (very high-freq early fault)
- Band 5: 4500-5900 Hz (near-Nyquist)

BPF center frequencies vs band centers:

| Band | Config range | Config center | BPF f0 (tuned) | Match? |
|------|-------------|--------------|----------------|--------|
| 1    | 100-500 Hz  | 224 Hz       | 226.6 Hz       | Good   |
| 2    | 500-1500 Hz | 866 Hz       | 1001 Hz        | Fair   |
| 3    | 1500-3000 Hz| 2121 Hz      | 3162 Hz        | High   |
| 4    | 3000-4500 Hz| 3674 Hz      | 7236 Hz        | **Way too high** |
| 5    | 4500-5900 Hz| 5153 Hz      | 14639 Hz       | **Way too high** |

**CRITICAL FINDING**: BPF channels 4 and 5 are centered WAY above the
training config bands. Ch4 should be ~3674 Hz but is 7236 Hz.
Ch5 should be ~5153 Hz but is 14639 Hz. This means:
1. The analog filters don't match what the classifier was trained on
2. With wrong bias, they shift even further down, but still wrong
3. The spectral features are scrambled vs training expectations

## 6. BPF Bandwidth and Q Analysis

For the Tow-Thomas biquad, BW = f0/Q:

| Ch | f0 (Hz) | Q    | BW (Hz) | -3dB range (Hz) |
|----|---------|------|---------|-----------------|
| 1  | 227 | 0.79 | 287 | 83 - 370 |
| 2  | 1001 | 0.71 | 1416 | 293 - 1710 |
| 3  | 3162 | 1.11 | 2854 | 1735 - 4589 |
| 4  | 7236 | 1.42 | 5096 | 4688 - 9784 |
| 5  | 14639 | 1.41 | 10397 | 9441 - 19838 |

The bandwidths are quite wide (low Q). This means significant overlap
between channels, reducing discrimination ability.

## 7. Conclusions and Recommendations

### Major Issues Found

1. **Bias voltage mismatch**: Ch4 and Ch5 need different bias voltages than Ch1-3.
   The full-chain uses only one set of bias voltages, detuning Ch4/Ch5.

2. **Center frequency mismatch**: Even with correct bias, Ch4 (7236 Hz) and
   Ch5 (14639 Hz) don't match the training config bands (3000-4500 Hz and
   4500-5900 Hz respectively). The BPF was designed with logarithmically-spaced
   centers (224, 1000, 3162, 7071, 14142) but training uses linear-ish bands.

3. **The envelope detector only sees differences in BPF outputs**. If the BPFs
   don't correctly decompose the spectrum, the envelope features are meaningless.

### Recommendations

1. **Retune BPF channels 4 and 5** to match training config: f0=3674 Hz and f0=5153 Hz
2. **Add per-channel bias** or redesign to work with single bias at correct current
3. **Alternatively, retrain classifier** with the actual BPF center frequencies
4. **Priority: HIGH** -- This is likely a major contributor to classification failure