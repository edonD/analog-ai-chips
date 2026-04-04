# Expert Report 01: PGA Dynamic Range Analysis

## 1. PGA Architecture Summary

The PGA (Programmable Gain Amplifier) uses a capacitive-feedback topology:
- Topology: `vin --[Cin_k]-- mid_k --[NMOS switch]-- inn --[Cf]-- vout`
- Feedback cap: Cf = 1 pF (fixed)
- Gain = Cin/Cf, selected by 2-bit digital control (g1, g0)
- OTA: behavioral model (gm=30uS, Rout=33MOhm, GBW~480kHz)

### Gain Settings

| g1 | g0 | Cin (pF) | Gain | 
|----|----|----------|------|
| 0  | 0  | 1        | 1x   |
| 0  | 1  | 4        | 4x   |
| 1  | 0  | 16       | 16x  |
| 1  | 1  | 64       | 64x  |

## 2. Current Configuration in Full-Chain

From `vibrosense1_top.spice`:
- **Comment says 16x** (`PGA (16x gain)`)
- **Digital wrapper sets g1=1, g0=0** which selects gain setting 2 = 16x
- But the commit history says `reduce gain to 4x` -- let's check the digital wrapper

From `digital_wrapper.spice`:
  `*   4. PGA gain control (fixed at 16x: g1=1, g0=0)`
  `+ g1 g0`
  `* PGA Gain Control (fixed 4x = g1=0, g0=1)`
  `Vg1 g1 vss DC 0`
  `Vg0 g0 vss DC 1.8`

### Verified Gain from Simulation Data

- Input Vpp: 100.0 mV
- PGA output Vpp: 1600.4 mV
- Measured gain: **16.0x**
- This confirms the PGA is operating at **16x gain** (not 4x as commit says)

## 3. Stimulus Amplitude Analysis

From `generate_stimuli.py`:
- V_SCALE = 0.02 V/g
- V_OFFSET = 0.9 V (VCM)
- Fault amplitude = 3.0 g (for inner race)
- Max signal: 3.0 * 0.02 = 60 mV above VCM
- Typical noise floor: 0.3 * 0.02 = 6 mV above VCM

### Signal Level Calculation

| Signal Component | Amplitude (mVpp around VCM) | After PGA (16x) |
|------------------|-----------------------------|-----------------|
| Noise floor      | ~12 mVpp                    | ~192 mVpp       |
| Inner race fault | ~120 mVpp (impulses)        | ~1920 mVpp (CLIPS!) |
| Outer race fault | ~96 mVpp                    | ~1536 mVpp (CLIPS!) |
| Ball fault       | ~72 mVpp                    | ~1152 mVpp (CLIPS!) |

## 4. Output Swing and Clipping Analysis

The OTA (behavioral) has:
- Soft clamping at 0.05V and 1.75V
- Output range: 0.05V to 1.75V = 1.7V swing
- Maximum undistorted Vpp: 1.7V around VCM (0.9V) = 0.05V to 1.75V

At 16x gain with 100mVpp input (typical default):
- PGA output: 1.6Vpp, centered at 0.9V -> 0.1V to 1.7V
- This is **near the clipping limit** but just barely fits

**CRITICAL FINDING**: The fault impulses from synthetic stimuli are
broadband (contain energy from DC to ~6kHz). After PGA at 16x,
transient impulses will clip. However, the AVERAGE signal level
within each BPF band is much smaller than the peak impulse.

## 5. What the BPF Actually Sees

The BPF channels select narrow bands. The energy in each band is
a FRACTION of the total broadband signal. For a fault impulse:
- Total impulse: ~120 mVpp input -> ~1920 mVpp after PGA (clips to ~1700 mVpp)
- Energy per BPF band: roughly 1/5 to 1/20 of total, depending on resonance
- Expected BPF output: ~50-200 mVpp per channel for fault cases
- Expected BPF output: ~10-30 mVpp for normal (noise only)

## 6. From Quick Test Data

With default 1kHz sine, 100mVpp input at 16x gain:
- BPF1 output: 999.0 mVpp
- BPF2 output: 994.9 mVpp
- BPF3 output: 988.8 mVpp
- BPF4 output: 984.8 mVpp
- BPF5 output: 983.7 mVpp

All BPF channels show ~990 mVpp with a 1kHz input of 1.6Vpp PGA output.
This suggests the BPFs have approximately **0.6x passband gain** (990/1600).
The BPFs are not amplifying; they're attenuating. This is expected for a
Tow-Thomas topology at unity Q.

## 7. Optimal Operating Point Recommendation

### The Real Problem is NOT PGA Gain

Current signal budget:
- Synthetic stimulus: ~120 mVpp max fault impulse, ~12 mVpp noise
- PGA at 16x: ~1920 mVpp fault (clips), ~192 mVpp noise
- BPF passband gain ~0.6x: fault band energy ~50-200 mVpp, noise ~10-30 mVpp
- Envelope detector: needs ~100 mVpp to produce meaningful DC shift

### Recommendations

1. **V_SCALE is too low**: At 0.02 V/g, the stimulus represents a sensor
   with very low sensitivity. Real ADXL355 has 660 mV/g. Increasing V_SCALE
   to 0.1 V/g (5x) would give 5x larger signals at the PGA input.

2. **Keep 16x gain**: The 16x gain setting is correct for the config (bearing_cwru.json
   specifies pga_gain=16x). The gain was reduced to 4x in a previous commit to prevent
   clipping, but this was counterproductive -- it reduced BPF output amplitude by 4x,
   making the envelope detector's job much harder.

3. **Increase V_SCALE to 0.1, use 4x PGA gain**: This gives the same total gain
   (0.1 * 4 = 0.4 V/g) as (0.02 * 16 = 0.32 V/g) but with less clipping risk
   because the signal is larger before the capacitive feedback introduces noise.

4. **Best option: V_SCALE=0.2, PGA=4x**: This gives 0.8 V/g overall gain,
   producing ~500 mVpp signals in active BPF bands for fault cases, which
   would produce ~50-100 mV DC shifts at the envelope detector output.

## 8. Key Quantitative Findings

| Parameter | Current | Recommended |
|-----------|---------|-------------|
| V_SCALE   | 0.02 V/g | 0.2 V/g   |
| PGA Gain  | 16x (confirmed) | 4x  |
| Total gain| 0.32 V/g | 0.8 V/g    |
| BPF band energy (fault) | 30-100 mVpp | 150-500 mVpp |
| BPF band energy (normal)| 5-15 mVpp | 25-75 mVpp |
| Envelope DC shift (fault)| ~4-7 mV | ~30-100 mV |
| Envelope DC shift (normal)| ~1-3 mV | ~5-15 mV |
| Feature spread | ~7 mV | ~50-90 mV |

**Bottom line**: The PGA dynamic range problem is actually a stimulus amplitude
problem. V_SCALE=0.02 generates signals that are too small after band-splitting
to produce meaningful envelope differentiation. Increasing V_SCALE by 10x while
reducing PGA gain to 4x would dramatically improve feature separation.