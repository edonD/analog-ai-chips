# Expert Report 06: Bearing Fault Frequency and Domain Analysis

## 1. Bearing Defect Frequency Theory

For a rolling element bearing, defect frequencies are:

- **BPFO** (Ball Pass Frequency, Outer race) = (n/2) * f_s * (1 - d/D * cos(alpha))
- **BPFI** (Ball Pass Frequency, Inner race) = (n/2) * f_s * (1 + d/D * cos(alpha))
- **BSF** (Ball Spin Frequency) = (D/(2*d)) * f_s * (1 - (d/D)^2 * cos^2(alpha))
- **FTF** (Fundamental Train/Cage Frequency) = (f_s/2) * (1 - d/D * cos(alpha))

Where:
- n = number of rolling elements
- f_s = shaft frequency
- d = ball diameter
- D = pitch diameter
- alpha = contact angle

## 2. CWRU Test Bearing Parameters (6205-2RS)

| Parameter | Value |
|-----------|-------|
| Balls (n) | 9 |
| Ball diameter (d) | 7.94 mm |
| Pitch diameter (D) | 39.04 mm |
| Contact angle (alpha) | 0 degrees |
| d/D | 0.2034 |

## 3. Fault Frequencies at Different Shaft Speeds

| RPM  | f_shaft | BPFO (Hz) | BPFI (Hz) | BSF (Hz)  | FTF (Hz)  |
|------|---------|-----------|-----------|-----------|-----------|
| 1797 | 29.9 Hz | 107.4 | 162.2 | 70.6 | 11.9 |
| 1772 | 29.5 Hz | 105.9 | 159.9 | 69.6 | 11.8 |
| 1750 | 29.2 Hz | 104.6 | 157.9 | 68.7 | 11.6 |
| 1730 | 28.8 Hz | 103.4 | 156.1 | 68.0 | 11.5 |

At 1797 RPM (the CWRU standard):
- BPFO = 107.4 Hz
- BPFI = 162.2 Hz
- BSF = 70.6 Hz

## 4. Stimulus Script Values vs Correct Values

From `generate_stimuli.py`:
- BPFI = 5.415 * f_shaft = 162.2 Hz
- BPFO = 3.585 * f_shaft = 107.4 Hz
- BSF = 2.357 * f_shaft = 70.6 Hz

Correct values:
- BPFI = 162.2 Hz  (script: 162.2 Hz) -- MATCH
- BPFO = 107.4 Hz  (script: 107.4 Hz) -- MATCH
- BSF = 70.6 Hz   (script: 70.6 Hz) -- MATCH

**The fundamental frequencies in the script are approximately correct.**

## 5. How Bearing Faults Actually Manifest in Vibration

Bearing fault frequencies (100-162 Hz) are NOT directly visible in the
vibration spectrum as pure tones. Instead:

1. **Impact mechanism**: Each time a defect passes through the loaded zone,
   it produces a short impulse that excites the bearing's structural resonance
   (typically 2-10 kHz).

2. **The vibration signal**: Carrier = high-frequency resonance (kHz)
   modulated at the fault frequency (Hz). This is AM modulation.

3. **Envelope analysis principle**: The BPF isolates the resonance band,
   the envelope detector demodulates the AM, and the resulting signal
   shows the fault frequency. Different fault types excite different
   resonances with different modulation patterns.

4. **Key distinction between fault types**:
   - Inner race: AM modulated by shaft frequency (because inner race rotates)
   - Outer race: NO amplitude modulation (stationary race)
   - Ball fault: Intermittent contact, 2x BSF repetition rate
   - Normal: Random broadband, no periodic components

## 6. Synthetic Stimulus Realism Assessment

The synthetic stimuli in `generate_stimuli.py` model:

| Feature | Synthetic | Real CWRU | Realistic? |
|---------|-----------|-----------|------------|
| Impulse repetition | Correct | Correct | YES |
| Resonance frequency | 2.5-3.5 kHz | 2-6 kHz | YES |
| Impulse decay | exp(-600 to -800) | varies | FAIR |
| AM for inner race | cos(f_shaft) | cos(f_shaft) | YES |
| No AM for outer | Yes | Yes | YES |
| Ball intermittent | abs(sin(BSF)) | random | FAIR |
| Noise floor | Gaussian | Colored | FAIR |
| Duration | 200 ms | 10+ seconds | **SHORT** |
| Number of impulses | ~20-30 | ~1000+ | **LOW** |

### Biggest Issue: 200 ms Duration

At BPFI = 162.2 Hz, one period = 6.2 ms. In 200 ms, there are ~32 impulses.
This is barely enough for envelope detection to produce a stable DC.
Real CWRU recordings are 10+ seconds (>1600 impulses).

At BPFO = 107.4 Hz, one period = 9.3 ms. In 200 ms, ~21 impulses.
At 2*BSF = 141.2 Hz, one period = 7.1 ms. In 200 ms, ~28 impulses.

The envelope LPF has fc=92 Hz, settling time ~8.7 ms. With 200 ms sim,
the envelope has time to settle, but the STATISTICAL quality of the
envelope is poor with so few impulses.

## 7. Do Fault Frequencies Fall Within BPF Bands?

The FUNDAMENTAL fault frequencies (70-162 Hz) are in BPF1's range (100-500 Hz).
But that's the wrong question. What matters is:
- Which BPF band captures the RESONANCE excited by each fault type?

Synthetic stimulus resonances:
- Inner race: 3000 Hz resonance -> BPF3 (3162 Hz center) -- **GOOD MATCH**
- Outer race: 2500 Hz resonance -> BPF2/BPF3 boundary -- **FAIR**
- Ball fault: 3500 Hz resonance -> BPF3/BPF4 boundary -- **FAIR**

**Problem**: The resonances are clustered around 2500-3500 Hz, which is
BPF3's passband. This means BPF3 will respond to ALL fault types,
and the discrimination relies on subtle amplitude differences between
BPF2 (1001 Hz) and BPF4 (7236 Hz) sidebands. With the current signal
levels, these sideband differences are in the noise.

## 8. Recommendations

1. **Spread resonance frequencies**: Each fault type should excite a DIFFERENT
   resonance band. This could be done by adjusting the synthetic impulse
   response frequencies (e.g., inner=2 kHz, outer=3.5 kHz, ball=5 kHz)
   or by using real CWRU data which naturally has this separation.

2. **Increase simulation duration** to at least 500 ms for better envelope
   statistics (more impulse averaging).

3. **Increase fault amplitude**: fault_amplitude=3.0 with V_SCALE=0.02 gives
   only 60 mV peak stimulus. Real accelerometers produce 0.5-5V peak for
   damaged bearings. Increase V_SCALE to at least 0.1 V/g.

4. **Consider using actual CWRU .mat files** instead of synthetic data.
   The download script exists (`download_cwru.py`) but wasn't used.