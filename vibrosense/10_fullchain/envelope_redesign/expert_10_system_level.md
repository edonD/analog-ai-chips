# Expert Report 10: System-Level Architecture Review

## Problem Analysis

Before redesigning the envelope detector, we should ask: **is the
5-BPF + 5-envelope architecture even the right approach?**

The current architecture:
```
VIN -> PGA(4x) -> 5x BPF -> 5x Envelope -> Classifier(8 inputs)
                          -> RMS detector -----^
                          -> Peak detector ----^
                          -> (kurtosis proxy) -^
```

This produces 8 features: 5 envelopes + RMS + Peak + kurtosis_proxy.

Key observation from Expert 09 (RMS/Crest):
- **Peak detector: 120 mV spread** (excellent)
- **RMS detector: 2.4 mV spread** (poor)
- **Best envelope: 6.6 mV spread** (poor)
- **kurtosis_proxy: 0 mV spread** (useless)

**Only 1 out of 8 features provides good discrimination!**

## Alternative Architecture Options

### Option A: Fewer Channels, More Features per Channel

Instead of 5 BPF -> 5 envelope (producing 5 poor features),
use 3 BPF -> 3 envelope + 3 peak + 2 global:

```
VIN -> PGA -> 3x BPF -> 3x Peak Det -> 3 peak features
                      -> 3x Envelope -> 3 envelope features
                      -> RMS ----------> 1 RMS feature
                      -> Peak ---------> 1 peak feature
```

8 features total: 3 per-channel peaks + 3 per-channel envelopes + 2 global.
The per-channel peaks would have 70-100 mV spread each.

### Option B: All-Peak Architecture

Replace ALL envelopes with peak detectors:

```
VIN -> PGA -> 5x BPF -> 5x Peak Det -> 5 peak features
                      -> RMS ---------> 1 RMS feature
                      -> Peak --------> 1 peak feature
                      -> Peak (BPF3) -> 1 additional peak (most informative channel)
```

8 features: 5 per-channel peaks + 2 global + 1 redundant peak.
Expected: each peak feature has 30-100 mV spread.

### Option C: Bypass Envelopes Entirely

Use the existing RMS approach but per-channel:

```
VIN -> PGA -> 5x BPF -> 5x Per-Channel RMS -> 5 RMS features
                      -> Global RMS ----------> 1 feature
                      -> Global Peak ---------> 1 feature
                      -> Crest Factor --------> 1 feature
```

The RMS block uses MOSFET squarer + LPF. Per-channel RMS would capture
the power in each band.

**BUT**: Global RMS only shows 2.4 mV spread. Per-channel would be similar
or worse (due to band-splitting). RMS is NOT the answer.

### Option D: Peak + Envelope Combination (Hybrid)

Use BOTH peak and envelope per channel:
- Peak captures maximum amplitude (impulsive faults)
- Envelope captures average amplitude (continuous faults)
- Crest factor = Peak/Envelope captures impulsiveness

```
VIN -> PGA -> 5x BPF -> 5x Peak Det -----> 5 peak features (GOOD)
                      -> 5x Envelope -----> 5 envelope features
                      -> 5x Crest Factor -> 5 crest features (derived)
```

15 features — too many for 8-input classifier. Select top 8.

### Option E: Redesigned Envelope + Classifier Retraining

Keep the 5-BPF + 5-envelope architecture but:
1. Redesign envelope for much higher output swing (current-mode or log-domain)
2. Replace useless kurtosis_proxy with per-channel peak of best channel
3. Retrain classifier for actual voltage ranges

This is the most CONSERVATIVE approach.

## Quantitative Comparison

| Architecture | # Good Features (>50 mV spread) | Implementation Effort | Risk |
|-------------|--------------------------------|----------------------|------|
| Current (5 env) | 1 (peak only) | None | N/A |
| Option A (3 BPF) | 3-4 (peaks + some env) | Medium | Medium |
| Option B (all peak) | 5-6 (per-channel peaks) | **Low** | **Low** |
| Option C (per-ch RMS) | 1 (still just global peak) | Medium | High |
| Option D (peak + env) | 5+ | Medium | Medium |
| Option E (redesign env) | Depends on approach | Medium-High | Medium |

## Recommendation: Option B (All-Peak) + Improved Envelope

The strongest approach combines:
1. **Replace all 5 envelope detectors with peak detectors** (Expert 04)
   - Each produces 30-100 mV spread
   - Proven circuit (Block 05)
   - Lower power than current envelope

2. **Add behavioral gain to residual envelope info** (if needed)
   - Keep 1-2 envelope detectors for average-amplitude features
   - Apply 10x gain to envelope output

3. **Retrain classifier** for new feature set:
   - Features: 5 per-channel peaks + RMS + global peak + one envelope
   - Expected discrimination: much better

## What About Simply Using RMS Directly?

The existing RMS detector processes the BROADBAND signal. Its 120 mV spread comes
from the PEAK detector, not the RMS output (which has only 2.4 mV spread).

Per-channel RMS would have even LESS spread because:
- RMS propto mean(V^2) — quadratic compression (see Expert 03)
- The broadband RMS already has only 2.4 mV spread
- Per-channel would be at most similar

**RMS is NOT the solution.** Peak detection IS the solution.

## The Deeper Question: Why Does Peak Work So Well?

Peak detector output = maximum |PGA output - VCM| during measurement window.

For bearing faults:
- Inner race: sharp impulses → very high peaks → peak detector captures this
- Outer race: medium impulses → medium peaks
- Ball: smaller impulses → smaller peaks
- Normal: no impulses → lowest peaks

The PEAK captures the fundamental physics of bearing faults: impulsive events
with high crest factor. Averaging (envelope, RMS) dilutes this information.

## Conclusion

**The 5-BPF + 5-envelope architecture is fundamentally mismatched to the signal.**
Bearing faults are impulsive, not sinusoidal. The envelope detector extracts the
AVERAGE amplitude, but the PEAK amplitude is what discriminates fault types.

**Replace envelopes with per-channel peak detectors.** This is the single most
impactful architectural change.

## Implementation Effort
- **Low** (Option B): Swap envelope_det for peak_det_channel, 5 instances
- Timeline: 2-3 days for behavioral, 1 week for transistor-level
- Risk: Low (peak_detector already verified in Block 05)
