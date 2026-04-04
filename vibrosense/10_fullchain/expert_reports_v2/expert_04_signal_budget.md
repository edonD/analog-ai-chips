# Expert Report 04: End-to-End Signal Level Budget

## 1. Overview

Signal chain: Stimulus -> PGA -> BPF -> Envelope -> Classifier

The classifier was trained on features normalized to [0, 1], scaled to [0, 1.8V]
in the SPICE behavioral model. We trace actual signal levels through every stage
to find where the information is lost.

## 2. Stage-by-Stage Budget (Current Design)

### Stage 0: Stimulus Generation

| Parameter | Normal | Inner Race | Outer Race | Ball |
|-----------|--------|------------|------------|------|
| Fault amplitude (g) | 0 | 3.0 | 2.4 | 1.8 |
| V_SCALE | 0.02 | 0.02 | 0.02 | 0.02 |
| Peak deviation from VCM | ~6 mV | ~60 mV | ~48 mV | ~36 mV |
| Broadband noise | ~12 mVpp | ~12 mVpp | ~12 mVpp | ~12 mVpp |

### Stage 1: PGA (16x gain)

| Parameter | Normal | Inner Race | Outer Race | Ball |
|-----------|--------|------------|------------|------|
| Input pp | ~12 mV | ~120 mV | ~96 mV | ~72 mV |
| Output pp (16x) | ~192 mV | ~1920 mV* | ~1536 mV* | ~1152 mV |
| *Clipped to rail | ~192 mV | ~1700 mV | ~1536 mV | ~1152 mV |

*Fault impulses clip at 1.75V output limit. Continuous signal portions don't clip.

### Stage 2: Band-Pass Filter (5 channels)

Each BPF selects a narrow band. Signal energy SPLITS across bands.
Typical energy distribution for impulse-type faults:
- Most energy in resonance band (~3 kHz for inner race)
- Some energy in adjacent bands
- Little energy in distant bands

Estimated BPF output (mVpp) per channel:

| Channel | Center Hz | Normal | Inner Race | Outer Race | Ball |
|---------|-----------|--------|------------|------------|------|
| BPF1    | 227       | ~5-10  | ~5-10      | ~5-10      | ~5-10 |
| BPF2    | 1001      | ~10-20 | ~30-60     | ~30-50     | ~20-40 |
| BPF3    | 3162      | ~5-15  | ~50-100    | ~40-80     | ~30-60 |
| BPF4    | 7236*     | ~3-8   | ~30-60     | ~20-40     | ~30-50 |
| BPF5    | 14639*    | ~2-5   | ~10-30     | ~5-15      | ~10-20 |

*BPF4 and BPF5 are detuned due to bias mismatch (see Expert 02)

### Stage 3: Envelope Detector

The envelope converts BPF AC amplitude to DC offset above VCM (0.9V).

From actual simulation data (mean envelope values):

| Channel | Normal (mV>VCM) | Inner (mV>VCM) | Outer (mV>VCM) | Ball (mV>VCM) |
|---------|-----------------|----------------|----------------|---------------|
| ENV1   | +4.34           | +4.34          | +4.07          | +4.42         |
| ENV2   | +6.42           | +8.80          | +8.55          | +7.99         |
| ENV3   | +3.24           | +9.69          | +9.38          | +8.11         |
| ENV4   | +1.93           | +8.50          | +6.85          | +7.65         |
| ENV5   | +1.45           | +6.38          | +4.24          | +5.36         |

### Stage 4: Classifier Input

The classifier behavioral model divides each input by 1.8V and multiplies by weights.
With envelope values near 0.9V (VCM), the normalized value is ~0.5 for ALL inputs.

| Feature | Normal (norm) | Inner (norm) | Outer (norm) | Ball (norm) |
|---------|---------------|--------------|--------------|-------------|
| ENV1   | 0.50241       | 0.50241      | 0.50226      | 0.50246     |
| ENV2   | 0.50357       | 0.50489      | 0.50475      | 0.50444     |
| ENV3   | 0.50180       | 0.50538      | 0.50521      | 0.50451     |
| ENV4   | 0.50107       | 0.50472      | 0.50380      | 0.50425     |
| ENV5   | 0.50081       | 0.50354      | 0.50236      | 0.50298     |

**All normalized features are ~0.502 +/- 0.004**
The classifier needs features distributed across [0, 1] to discriminate.

## 3. The Gain Budget Gap

| Stage | Input Range | Output Range | Gain | Information Loss |
|-------|-------------|-------------|------|-----------------|
| Stimulus | -- | 12-120 mVpp | -- | None |
| PGA (16x) | 12-120 mVpp | 192-1700 mVpp | 16x | Some clipping |
| BPF (band split) | 192-1700 mVpp | 5-100 mVpp | 0.03-0.06x | Energy splitting |
| Envelope | 5-100 mVpp | 0.9+1 to 0.9+10 mV | DC conversion | Small offset |
| Classifier norm | 0.901-0.910 V | 0.500-0.506 | /1.8V | **MASSIVE** |

**The critical bottleneck**: Band-splitting reduces the signal by 15-30x,
then the envelope produces only millivolt DC offsets. These millivolt offsets
become indistinguishable when normalized to the full 0-1.8V range.

## 4. What the Classifier Actually Sees

Computing actual classifier scores with the real envelope values:

### normal
Features: ['0.9043', '0.9064', '0.9032', '0.9019', '0.9015', '1.5678', '1.0133', '1.5678']
Scores: Normal=-14.895, Inner=7.918, Ball=-2.337, Outer=8.280
Winner: **Outer Race** (score=8.280)
Expected: **normal**

### inner_race
Features: ['0.9043', '0.9088', '0.9097', '0.9085', '0.9064', '1.5653', '1.1336', '1.5653']
Scores: Normal=-15.445, Inner=8.202, Ball=-2.070, Outer=8.217
Winner: **Outer Race** (score=8.217)
Expected: **inner_race**

### outer_race
Features: ['0.9041', '0.9085', '0.9094', '0.9068', '0.9042', '1.5664', '1.0883', '1.5664']
Scores: Normal=-15.247, Inner=8.114, Ball=-2.160, Outer=8.222
Winner: **Outer Race** (score=8.222)
Expected: **outer_race**

### ball
Features: ['0.9044', '0.9080', '0.9081', '0.9076', '0.9054', '1.5675', '1.0638', '1.5675']
Scores: Normal=-15.161, Inner=8.057, Ball=-2.216, Outer=8.261
Winner: **Outer Race** (score=8.261)
Expected: **ball**

## 5. Proposed Signal Level Plan

### Option A: Increase stimulus amplitude (easiest)
- V_SCALE: 0.02 -> 0.2 (10x)
- PGA: 16x -> 4x
- Net: 0.8 V/g vs current 0.32 V/g (2.5x increase)
- Expected envelope spread: ~15-25 mV (3x improvement)
- Still insufficient for 0-1.8V classifier range

### Option B: Add post-envelope amplifier (medium effort)
- Add a 50-100x amplifier after each envelope LPF
- Envelope offset of 5 mV * 100 = 500 mV
- Needs DC level shifting (remove VCM before amplification)
- Would require AC-coupled gain stage or differential measurement

### Option C: Retrain classifier for actual voltage range (best)
- The classifier was trained with MinMaxScaler mapping features to [0, 1]
- The behavioral model scales [0,1] to [0, 1.8V]
- Actual features are in range [0.900, 0.910V]
- **Retrain**: normalize to actual envelope output range, not [0, 1.8V]
- Retrain the behavioral classifier to expect inputs centered at 0.9V
  with millivolt-scale variations
- This is a WEIGHT RESCALING problem, not a hardware problem

### Option D: Combined approach (recommended)
1. Increase V_SCALE to 0.1 V/g, keep PGA at 16x (5x signal boost)
2. Retrain classifier with features in actual analog voltage range
3. This gives envelope spreads of ~30-50 mV
4. Rescale classifier weights for the [0.88, 0.95V] feature range
5. Expected accuracy: 75-90% (envelope features become meaningful)

## 6. Key Numbers

| Metric | Current | Needed for 80%+ accuracy |
|--------|---------|--------------------------|
| Envelope spread (max across cases) | 6.6 mV | >50 mV |
| Feature normalized range | 0.500-0.506 | 0.0-1.0 |
| Classifier score margin | <0.1 | >1.0 |
| Signal-to-classifier-noise ratio | ~0 dB | >20 dB |