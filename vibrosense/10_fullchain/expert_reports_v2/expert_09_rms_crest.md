# Expert Report 09: RMS/Crest Feature Analysis

## 1. RMS/Crest Architecture (Block 05)

### True RMS Detector
- Single-pair MOSFET square-law squarer
- Signal NFET: gate = vout_pga = VCM + V_signal
- Reference NFET: gate = VCM
- Difference current: dI = (K/2)[2*Vov*V + V^2]
- After LPF: mean(dI) = (K/2)*RMS^2 (linear term cancels)
- Load R = 100k, passive RC LPF (fc=50 Hz, R=3.18M, C=1nF)

The RMS output is a voltage that drops proportional to RMS^2:
- rms_out = VDD - R_load * Id_signal
- rms_ref = VDD - R_load * Id_reference
- Difference: rms_ref - rms_out proportional to RMS^2

### Peak Detector
- OTA5 (5T OTA, high gain) + NMOS source follower + 500pF hold cap
- Slow discharge via subthreshold NMOS (Vgs=0, W=0.42u L=20u)
- Reset via NMOS switch

## 2. RMS/Crest Feature Values from Simulation

### From fullchain_analysis.json (last 50ms average)

| Test Case | rms_out (V) | peak_out (V) | rms_ref* |
|-----------|-------------|--------------|----------|
| normal       | 1.5678 | 1.0133 | N/A |
| inner_race   | 1.5653 | 1.1336 | N/A |
| outer_race   | 1.5664 | 1.0883 | N/A |
| ball         | 1.5675 | 1.0638 | N/A |

*rms_ref not stored in analysis JSON separately

### From Raw Data (last 50ms)

| Test Case | rms_out (V) | rms_ref (V) | peak_out (V) | rms_out-ref (mV) | rms std (mV) |
|-----------|-------------|-------------|--------------|-----------------|--------------|
| normal       | 1.5678 | 1.6162 | 1.0133 | -48.4 | 4.54 |
| inner_race   | 1.5653 | 1.6162 | 1.1336 | -50.9 | 6.38 |
| outer_race   | 1.5664 | 1.6162 | 1.0883 | -49.7 | 4.45 |
| ball         | 1.5675 | 1.6162 | 1.0638 | -48.6 | 5.41 |

### Feature Spreads

- **rms_out spread**: 2.4 mV (1.5653 to 1.5678)
- **peak_out spread**: 120.2 mV (1.0133 to 1.1336)
- **rms_ref spread**: 0.0 mV (1.6162 to 1.6162)

## 3. Are RMS and Peak Features Providing Differentiation?

### RMS Output (Feature 5 in classifier)

The RMS detector processes the PGA output directly (broadband).
This means it captures TOTAL vibration energy, not band-specific.

RMS spread across test cases: **2.4 mV**

This is similar to the envelope spreads -- minimal differentiation.

### Peak Output (Feature 6 in classifier)

The peak detector captures the maximum PGA output voltage.
Fault signals have higher peaks than normal vibration.

Peak spread across test cases: **120.2 mV**

**The peak detector provides SIGNIFICANT differentiation!**
This is the BEST differentiating feature in the analog chain.

| Test Case | Peak (V) | Interpretation |
|-----------|----------|----------------|
| normal       | 1.0133 | Lowest (smooth) |
| inner_race   | 1.1336 | Highest (impulsive) |
| outer_race   | 1.0883 | Medium |
| ball         | 1.0638 | Medium |


### RMS Reference (Feature 7 in classifier -- proxy for kurtosis)

In the full-chain, rms_ref is used as a proxy for kurtosis (feature 7).
The rms_ref is the LPF output of the REFERENCE squarer NFET (gate=VCM).
It should be approximately constant across test cases since VCM doesn't change.

RMS ref spread: **0.0 mV** -- Essentially constant

Using rms_ref as kurtosis proxy is **not useful** because it doesn't
depend on the signal at all. It's a constant voltage from the reference
NFET biased at VCM. The classifier's kurtosis weight is being wasted
on a non-informative feature.

## 4. Classifier Weight Analysis for RMS/Crest/Kurtosis

From the trained weights:

| Feature | Normal | Inner Race | Ball | Outer Race |
|---------|--------|------------|------|------------|
| RMS (f5) | -5.03 | -2.91 | -2.91 | +9.77 |
| Peak (f6) | -7.14 | +3.43 | +3.43 | -0.80 |
| Kurtosis/Ref (f7) | -0.80 | +5.55 | -5.03 | -0.80 |

Key observations:
- **Outer Race class has heavy positive weight on RMS (+9.77)**: Expects higher
  RMS for outer race faults. Since rms_out is ~1.57V for all cases,
  this doesn't help differentiate.
- **Inner Race and Ball have positive weight on Peak (+3.43)**: Expects impulsive
  signals. The peak detector DOES show different values across cases.
- **Kurtosis/Ref weight is wasted**: rms_ref is constant, so this feature
  contributes the same bias to all test cases regardless of class.

## 5. Impact Assessment

### How much do RMS/Peak features contribute to classification?

Calculating score contribution from features 5-7:

**normal**:
  Class 0 (Normal): RMS=-4.378 + Peak=-4.020 + Ref=-0.716 = -9.113
  Class 1 (Inner ): RMS=-2.536 + Peak=+1.932 + Ref=+4.979 = +4.374
  Class 2 (Ball  ): RMS=-2.536 + Peak=+1.932 + Ref=-4.513 = -5.117
  Class 3 (Outer ): RMS=+8.513 + Peak=-0.449 + Ref=-0.716 = +7.349

**inner_race**:
  Class 0 (Normal): RMS=-4.371 + Peak=-4.497 + Ref=-0.716 = -9.583
  Class 1 (Inner ): RMS=-2.532 + Peak=+2.161 + Ref=+4.979 = +4.607
  Class 2 (Ball  ): RMS=-2.532 + Peak=+2.161 + Ref=-4.513 = -4.884
  Class 3 (Outer ): RMS=+8.500 + Peak=-0.502 + Ref=-0.716 = +7.282

**outer_race**:
  Class 0 (Normal): RMS=-4.374 + Peak=-4.317 + Ref=-0.716 = -9.406
  Class 1 (Inner ): RMS=-2.534 + Peak=+2.074 + Ref=+4.979 = +4.519
  Class 2 (Ball  ): RMS=-2.534 + Peak=+2.074 + Ref=-4.513 = -4.972
  Class 3 (Outer ): RMS=+8.506 + Peak=-0.482 + Ref=-0.716 = +7.308

**ball**:
  Class 0 (Normal): RMS=-4.377 + Peak=-4.220 + Ref=-0.716 = -9.312
  Class 1 (Inner ): RMS=-2.536 + Peak=+2.028 + Ref=+4.979 = +4.471
  Class 2 (Ball  ): RMS=-2.536 + Peak=+2.028 + Ref=-4.513 = -5.021
  Class 3 (Outer ): RMS=+8.512 + Peak=-0.471 + Ref=-0.716 = +7.325


## 6. Conclusions

1. **RMS output provides marginal differentiation**: Spread is small (~2-3 mV)
   because V_SCALE=0.02 means the broadband signal difference between
   normal and fault is tiny at the PGA output.

2. **Peak output provides the BEST differentiation**: 120 mV spread across
   test cases. Inner race (most impulsive) has the highest peak.
   This is the most useful feature in the current design.

3. **rms_ref as kurtosis proxy is useless**: It's a constant voltage that
   doesn't depend on the signal content. This wastes one of 8 classifier inputs.

4. **Recommendations**:
   - Replace rms_ref with an actual kurtosis approximation circuit
   - Increase V_SCALE to improve RMS differentiation
   - The peak detector is the "hidden hero" -- its 120 mV spread is
     18x larger than the best envelope spread (6.6 mV)