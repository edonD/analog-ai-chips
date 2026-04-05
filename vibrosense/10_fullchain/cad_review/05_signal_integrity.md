# CAD Expert Review #5: Signal Integrity

**Reviewer:** CAD Expert 5 (Signal Integrity)
**Date:** 2026-04-05

---

## Signal Chain Trace: Input to Classification

### Stage 1: Input Stimulus -> PGA

- **Input:** VCM=0.9V, signal amplitude 50-300 mVpp depending on fault type
- **PGA gain:** 4x (g1=0, g0=1.8)
- **PGA output:** 0.9V +/- 200-1200 mVpp
- **PGA clipping risk:** At 4x gain, inner_race (largest signal) reaches ~0.77Vpp * 4 = 3.08Vpp.
  With 1.8V supply, output swings 0.9 +/- 1.54V = [-0.64V, 2.44V]. The behavioral
  OTA clamps at [0.05V, 1.75V], so ~30% of inner_race peaks are clipped.
- **Impact:** Moderate. Clipping distorts the spectral content of the PGA output,
  adding harmonics. This affects fault signals more than normal (which stays within
  rails), potentially helping discrimination through an unintended mechanism.

### Stage 2: PGA -> BPF Bank

- **BPF input:** single-ended positive output (vout_pga), with VCM as reference
- **BPF outputs:** Differential (bp_outp/bp_outn), but only positive used downstream
- **Expected BPF output levels:** VCM +/- signal at each band

Key BPF characteristics:
| Channel | Center | Q | Expected Output (fault) |
|---------|--------|---|------------------------|
| CH1 | 100 Hz | ~10 | Low (bearing faults have little 100 Hz energy) |
| CH2 | 300 Hz | ~10 | Low to moderate |
| CH3 | 1 kHz | ~10 | Moderate (near fault resonance frequencies) |
| CH4 | 3 kHz | ~10 | HIGH (3 kHz is inner race resonance frequency) |
| CH5 | 6 kHz | ~10 | Moderate-high (harmonics of fault resonances) |

### Stage 3: BPF -> Peak Envelope Detector

The behavioral peak envelope detector:
1. Full-wave rectifies: `|vin - vcm|` (always positive)
2. Tracks peak with fast charge, slow 20ms decay
3. Outputs: `vcm + peak_amplitude`

**Measured envelope values (last 50ms steady state):**

| Channel | Normal (V) | Inner Race (V) | Outer Race (V) | Ball (V) | Spread (mV) |
|---------|-----------|-----------------|-----------------|----------|-------------|
| ENV1 (100 Hz) | 0.9558 | 0.9520 | 0.9541 | 0.9542 | 3.8 |
| ENV2 (300 Hz) | 0.9968 | 0.9950 | 0.9968 | 0.9917 | 5.1 |
| ENV3 (1 kHz) | 1.0034 | 1.0062 | 1.0100 | 1.0031 | 6.9 |
| ENV4 (3 kHz) | 0.9358 | 1.0305 | 1.0261 | 1.0212 | **94.7** |
| ENV5 (6 kHz) | 0.9182 | 1.0258 | 1.0059 | 1.0043 | **107.6** |

**Key observations:**
- ENV1-ENV3 carry almost no discriminative information (3-7 mV spread).
  These channels are wasted in the current design.
- ENV4 and ENV5 dominate classification. Normal has LOW values (~0.93-0.92V),
  while all three fault types have HIGH values (~1.00-1.03V).
- The three fault types (inner_race, outer_race, ball) are VERY close together
  in ENV4/ENV5 space. Separation between faults relies on subtle differences
  of 5-15 mV.

### Stage 4: Additional Features (RMS/Crest)

| Feature | Normal | Inner Race | Outer Race | Ball | Spread |
|---------|--------|------------|------------|------|--------|
| RMS_out | 1.5509 | 1.5125 | 1.5178 | 1.5292 | 38.4 mV |
| Peak_out | 1.1844 | 1.2391 | 1.2342 | 1.2274 | 54.7 mV |
| RMS_ref | 1.6162 | 1.6162 | 1.6162 | 1.6162 | 0.0 mV |

- RMS_out: Normal is HIGHEST (counterintuitive). May be because fault signals
  cause PGA clipping, reducing measured RMS.
- Peak_out: Inner race is HIGHEST (expected -- largest impulse amplitudes).
- RMS_ref: CONSTANT (1.616V) -- carries zero information. Wastes a classifier input.

### Stage 5: Classifier

The classifier receives 8 features. Analysis of discriminative power:
1. **ENV5 (107.6 mV spread)** -- PRIMARY discriminator (normal vs fault)
2. **ENV4 (94.7 mV spread)** -- PRIMARY discriminator (normal vs fault)
3. **Peak_out (54.7 mV)** -- SECONDARY (inner_race vs others)
4. **RMS_out (38.4 mV)** -- SECONDARY (normal vs fault, inverted)
5. **ENV3 (6.9 mV)** -- WEAK
6. **ENV2 (5.1 mV)** -- NEGLIGIBLE
7. **ENV1 (3.8 mV)** -- NEGLIGIBLE
8. **RMS_ref (0.0 mV)** -- USELESS (constant)

**Effective useful features: 4 out of 8.** The classifier has to distinguish
4 classes using effectively 4 features with varying quality. This is a tight
design -- any degradation in ENV4/ENV5 could cause misclassification.

---

## Signal Quality Assessment by Stage

| Stage | Quality | Notes |
|-------|---------|-------|
| Input | GOOD | Well-defined synthetic stimuli |
| PGA | FAIR | 4x gain causes clipping on fault signals |
| BPF bank | GOOD | Clean spectral separation, proper biasing |
| Envelope (ch1-3) | POOR | Only 3-7 mV spread, not useful |
| Envelope (ch4-5) | GOOD | 95-108 mV spread, primary discriminators |
| RMS/Crest | FAIR | 38-55 mV spread, useful as secondary features |
| Classifier | FAIR | 4/4 accuracy but thin margins |

---

## Root Cause of Thin Margins

The fundamental issue is that the three fault types produce similar spectral
signatures in the 3-6 kHz range (all have resonance frequencies in this band).
The differences are:
- Inner race: 3 kHz resonance + shaft AM -> slightly higher ENV4
- Outer race: 2.5 kHz resonance -> similar ENV4, lower ENV5
- Ball: 3.5 kHz resonance + random AM -> between the other two

With only 10-15 mV separating the three fault types in each envelope channel,
the classifier must rely on very precise feature measurements. This is where
the behavioral-to-transistor transition is most risky.

---

## Verdict: Signal quality is adequate but fragile

The signal chain works but relies on ~10 mV feature differences for fault-type
discrimination. ENV4 and ENV5 carry almost all the information. The PGA clipping
may actually help (adds harmonics that differentiate), but this is not a robust
design principle. Main risk: transistor-level non-idealities could easily shift
envelopes by 10-20 mV, breaking the thin inter-fault margins.
