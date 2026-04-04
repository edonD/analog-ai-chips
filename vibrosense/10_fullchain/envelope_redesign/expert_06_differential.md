# Expert Report 06: Differential Envelope Detector

## Problem Analysis

The fundamental issue: all 5 envelope outputs sit at ~0.900-0.910V (near VCM).
The ABSOLUTE values are almost identical. But the DIFFERENCES between channels
contain discriminating information because different fault types excite different
frequency bands.

For example:
- Inner race fault: strong in BPF3, BPF4, BPF5 → higher envelopes in those channels
- Normal: roughly uniform low energy across channels
- The PATTERN of envelope ratios is the discriminating feature

By computing ENV[i] - ENV[j] (differential), we:
1. CANCEL the common-mode (0.9V disappears)
2. AMPLIFY the differences (which are the signal)

## Differential Features (from current data, mV)

| Pair | Normal | Inner | Outer | Ball | Spread |
|------|--------|-------|-------|------|--------|
| ENV3-ENV1 | -1.10 | +5.35 | +5.31 | +3.69 | 6.45 |
| ENV4-ENV1 | -2.41 | +4.16 | +2.78 | +3.23 | 6.57 |
| ENV5-ENV1 | -2.89 | +2.04 | +0.17 | +0.94 | 4.93 |
| ENV3-ENV2 | -3.18 | +0.89 | +0.83 | +0.12 | 4.07 |
| ENV4-ENV2 | -4.49 | -0.30 | -1.70 | -0.34 | 4.19 |

**Best differential spread: 6.6 mV**

Compared to best single-channel spread of 6.6 mV, the differential
approach gives similar or slightly better discrimination.

## The Problem with Differential

The differential of two small numbers is still a small number.
ENV3 - ENV1 for inner race = 9.69 - 4.34 = 5.35 mV
ENV3 - ENV1 for normal = 3.24 - 4.34 = -1.10 mV
Spread = 6.45 mV — same as single-channel ENV3 spread!

**The differential approach does NOT improve dynamic range. It only removes
common-mode, which wasn't the problem.** The problem is that the individual
envelope values are too small, not that VCM is large.

## Proposed Architecture (if we still want differential)

```
ENV_i --+--[Differential OTA]-- V_diff_ij = G * (ENV_i - ENV_j)
        |                           with G = 100x to amplify mV to hundreds of mV
ENV_j --+
```

### SPICE Subcircuit

```spice
* Differential Envelope Feature Extractor
* Computes V_out = VCM + G * (V_env_i - V_env_j)

.subckt env_diff in_p in_n vcm vout vdd gnd vbn

* Gain = 100x differential
* Behavioral (for concept validation)
B_diff vout gnd V = {
+   max(0.05, min(1.75,
+   v(vcm) + 100.0 * (v(in_p) - v(in_n))
+   )) }

.ends env_diff
```

## Expected Output with 100x Differential Gain

| Pair | Normal (mV from VCM) | Inner (mV) | Outer (mV) | Ball (mV) | Spread (mV) |
|------|---------------------|-----------|-----------|----------|-------------|
| ENV3-ENV1 | -110 | +535 | +531 | +369 | 645 |
| ENV4-ENV1 | -241 | +416 | +278 | +323 | 657 |
| ENV5-ENV1 | -289 | +204 | +17  | +94  | 493 |
| ENV3-ENV2 | -318 | +89  | +83  | +12  | 407 |
| ENV4-ENV2 | -449 | -30  | -170 | -34  | 419 |

**With 100x gain, spreads of 400-660 mV.** This is substantial!

But this requires 100x gain on millivolt signals — same offset problem
as Expert 05 (post-gain). Offset of 5 mV * 100 = 500 mV error.

## Advantage over Post-Gain

The differential approach has one advantage over single-ended gain:
**correlated offset cancels**. If both envelope detectors have similar OTA
offset (they share the same vbn bias), the offset appears in both ENV_i and
ENV_j and cancels in the difference.

In practice, offset matching between two different OTAs is ~1-5 mV in SKY130,
so differential reduces offset from ~20 mV to ~3 mV. At 100x gain:
3 mV * 100 = 300 mV offset error (still large but better than 2000 mV).

## Power Estimate
- Differential amplifier (OTA): ~5 uW per pair
- 5 differential pairs: ~25 uW total
- Plus existing 5 envelope detectors: ~100 uW
- **Total: ~125 uW** (significant increase)

## Pros
1. Removes common-mode voltage (VCM cancels)
2. Correlated offset partially cancels
3. Conceptually elegant (spectral shape features)
4. Can extract more features from same channels (C(5,2) = 10 pairs)

## Cons
1. Does NOT improve fundamental dynamic range — differential of small numbers is small
2. Still needs high gain (100x) with associated offset problems
3. Increased complexity (5 more amplifiers)
4. Reduces number of independent features (from 5 single-ended to 5 differential)
5. Needs matched envelope detectors for offset cancellation

## Verdict

**NOT RECOMMENDED.** The differential approach solves the wrong problem (common-mode
removal) when the real problem is small signal amplitude. It still needs high gain,
with the same offset issues as Expert 05. The marginal benefit (offset matching)
doesn't justify the additional complexity.

## Implementation Effort
- **Medium**: 5 differential amplifiers, similar to post-gain approach
- Risk: Medium (offset matching, gain accuracy)
- Timeline: 2 weeks
