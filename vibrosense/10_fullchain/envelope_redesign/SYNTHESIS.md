# Envelope Redesign: Synthesis of 10 Expert Opinions

**Date**: 2026-04-04
**Objective**: Select the best approach to replace/improve the envelope detector
to increase full-chain classification accuracy from 25% to >75%.

---

## Comparison Matrix

| # | Approach | Spread Improvement | Power/ch | Complexity | Risk | Verdict |
|---|---------|-------------------|----------|------------|------|---------|
| 01 | Log-Domain | ~18x (116 mV range) | 6.6 uW | Medium-High | High | Maybe |
| 02 | Chopper Rectifier | 2x (13 mV) | 4 uW | Medium | Medium | No |
| 03 | Squarer | Worse (quadratic suppresses small signals) | 5 uW | Low | Low | No |
| 04 | **Peak Detector** | **10-15x (70-100 mV/ch)** | **2 uW** | **Low** | **Low** | **YES** |
| 05 | Post-Envelope Gain | 70x on paper, offset-limited | 20-35 uW | Medium | High | No (standalone) |
| 06 | Differential Envelope | Same as single-ended + gain | 5 uW | Medium | Medium | No |
| 07 | Switched-Capacitor | ~10x with SC gain | 3.5 uW | High | Medium | Maybe |
| 08 | Comparator-Based | Binary only, poor multi-class | 1 uW | Very Low | Low | No |
| 09 | Current-Mode | ~40x (400+ mV spread) | 3 uW | Medium | Medium | Strong |
| 10 | System-Level | Architecture depends on chosen approach | - | - | - | Guidance |

---

## Ranking by Expected Impact

### Tier 1: Strongly Recommended

**1. Per-Channel Peak Detector (Expert 04)**
- Expected spread: 70-100 mV per channel (vs 0.3-6.6 mV current)
- Power: 2 uW/ch (10x REDUCTION from current 20 uW/ch)
- Implementation: Copy Block 05 peak_detector, instantiate 5x
- Risk: Low (proven circuit, already in design)
- Settles within 5 ms (within 20 ms budget)
- WHY: Bearing faults are impulsive. Peak captures impulse amplitude directly.
  Envelope (average) dilutes the key discriminating information.

**2. Current-Mode Integrating Rectifier (Expert 09)**
- Expected spread: 400+ mV per channel
- Power: 3 uW/ch
- Implementation: Behavioral B-source for immediate testing; transistor-level later
- Risk: Medium (needs large cap, periodic reset)
- WHY: Natural gain from integration (gm*T/C), eliminates VCM offset problem.

### Tier 2: Potentially Useful as Supplement

**3. Log-Domain (Expert 01)** — Good dynamic range compression but hard to implement
**4. Switched-Capacitor (Expert 07)** — Good gain + auto-zeroing but complex
**5. Post-Gain (Expert 05)** — Simple concept but offset kills it at high gain

### Tier 3: Not Recommended

**6. Chopper (Expert 02)** — Only 2x improvement, insufficient
**7. Differential (Expert 06)** — Solves wrong problem
**8. Comparator (Expert 08)** — Loses amplitude info, poor multi-class
**9. Squarer (Expert 03)** — Makes small signals WORSE

---

## Selected Approach: Hybrid Peak + Current-Mode

### Primary: Per-Channel Peak Detector (behavioral, for immediate results)

Replace all 5 envelope_det instances with peak detectors using behavioral
B-sources. This is the fastest path to working discrimination.

**Implementation plan:**

1. Create `envelope_peak_behavioral.spice` — behavioral peak detector:
   - B-source tracks max(vin - vcm) with slow exponential decay
   - Output starts at VCM, rises to VCM + peak_amplitude
   - Settle time: ~1 cycle of BPF frequency

2. Replace envelope_det in the top-level netlist with envelope_peak_behavioral

3. Retrain classifier weights for peak-detector feature ranges

4. Run all 4 full-chain simulations

### Why Behavioral First?

The transistor-level peak detector (Block 05) requires careful bias tuning.
A behavioral model gives us immediate results to validate the approach.
If it works (>75% accuracy), we can then implement transistor-level.

### Feature Set

The classifier has 8 inputs. New mapping:
- in0-in4: Per-channel peak detector outputs (replacing envelopes)
- in5: Global RMS output (keep as-is)
- in6: Global peak detector (keep as-is)
- in7: RMS reference (was useless; keep for now, retrain weights around it)

---

## Concrete Implementation Plan

### Step 1: Create behavioral peak envelope subcircuit
- File: `envelope_redesign/envelope_peak_behavioral.spice`
- Uses B-source: tracks running max of |vin - vcm|, with slow decay
- Pin-compatible with envelope_det: same port list

### Step 2: Create new top-level netlist
- Copy vibrosense1_top.spice
- Replace `.include envelope_det_fixed.spice` with new subcircuit
- Keep everything else identical

### Step 3: Retrain classifier
- Estimate peak feature values from BPF data
- Compute new classifier weights
- Update classifier_behavioral.spice

### Step 4: Generate per-test-case netlists and run simulations

### Step 5: Parse results and compute accuracy

---

## Expected Outcome

With per-channel peak detection:
- 5 features spanning 30-120 mV each (vs 0.3-6.6 mV)
- Peak detector already proven (120 mV spread on broadband)
- With retrained classifier: **expected accuracy 75-100%**

The current system fails because envelope features are compressed to ~5 mV
in a 1800 mV range. Peak features use 30-120 mV, giving the classifier
20-60x more signal to work with.
