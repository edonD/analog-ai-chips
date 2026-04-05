# CAD Expert Review: Summary and Action Plan

**Date:** 2026-04-05
**Status:** 5/5 expert reviews complete

---

## Prioritized Issue List

### Critical (Must Fix)

| # | Issue | Source | Impact | Effort |
|---|-------|--------|--------|--------|
| C1 | **Generalization unproven** -- 4/4 accuracy on 4 training points with 36 free parameters is not meaningful | Expert 5 | Credibility | Medium (12 variant sims) |
| C2 | **Transistor-level envelope not verified in full chain** -- the include is changed but no sim results exist | Expert 3 | Design integrity | Medium (4 sims at 50ms) |
| C3 | **PGA uses behavioral OTA** -- signal path contains ideal VCCS model | Expert 3 | Accuracy of results | Low (1-line fix + verify) |

### Important (Should Fix)

| # | Issue | Source | Impact | Effort |
|---|-------|--------|--------|--------|
| I1 | PGA clips fault signals at 4x gain | Expert 5 | Signal integrity | Investigation only |
| I2 | No PVT corner testing | Expert 2 | Robustness unknown | High (1+ corner sim) |
| I3 | Power values show negative sign convention | Expert 2 | Report accuracy | Low (fix analysis script) |
| I4 | 3 of 8 classifier inputs carry negligible info | Expert 5 | Design efficiency | Low priority |

### Minor (Cosmetic / Future Work)

| # | Issue | Source | Notes |
|---|-------|--------|-------|
| M1 | Digital clocks unconnected to analog path | Expert 1 | Harmless |
| M2 | BPF negative outputs unused | Expert 1 | Design choice |
| M3 | RMS_ref is constant (1.616V) | Expert 5 | Wastes 1 classifier input |
| M4 | No .tran maxstep (affects sim speed) | Expert 4 | Optimization |
| M5 | Bias sources all ideal | Expert 3 | Future work |

---

## What MUST Be Fixed for Professional Design

1. **Prove generalization (C1):** Run at least 8 variant simulations on UNSEEN data.
   If accuracy drops below 75%, retrain classifier with more training data.

2. **Verify transistor-level signal path (C2, C3):** Replace PGA behavioral OTA
   with real OTA, then run full-chain with transistor-level envelope detector.
   This makes the analog path 100% transistor-level (PGA -> BPF -> Envelope -> RMS).

3. **Honest reporting:** Update all claims to reflect actual verification level.
   Current reports sometimes say "transistor-level" when behavioral models are used.

---

## What Can Be Documented as "Future Work"

- PVT corner sweep (requires 4+ additional sims at each corner)
- Real CWRU accelerometer data injection
- Transistor-level bias generator
- Layout and parasitic extraction
- Tape-out

---

## Concrete Action Plan

### Phase 3A: Fix PGA OTA (30 minutes)
1. Change `pga_fixed.spice` line 79 to use `ota_pga_v2` instead of `ota_behavioral`
2. Fix port mapping (ota_pga_v2 has 9 pins vs ota_behavioral's 5)
3. Quick 50ms sim of normal case to verify no convergence issues

### Phase 3B: Verify Transistor-Level Envelope (2-3 hours)
1. Working copy already includes `envelope_peak_transistor.spice`
2. Run 4x 50ms sims in parallel (one per test case)
3. Analyze results -- if accuracy holds, the TL envelope is validated
4. If accuracy drops, may need to adjust bias or retrain classifier

### Phase 3C: Generalization Testing (4-6 hours)
1. Variant stimuli and netlists already generated (12 cases)
2. Run 12x 50ms sims (can run 4 at a time in parallel: 3 batches)
3. Analyze results. Compute accuracy on unseen variants.
4. If accuracy < 75%: retrain classifier on combined training+variant data

### Phase 3D: Documentation (1 hour)
1. Update all READMEs and reports with verified numbers
2. Correct any "transistor-level" claims to match reality
3. Write final honest assessment

### Total Estimated Time: 8-10 hours

---

## Key Risks

1. **Transistor-level envelope may shift features** -- behavioral model has ideal
   rectification, real circuit has offset and gain error. ENV values may shift
   by 10-50 mV, potentially breaking thin classification margins.
   **Mitigation:** If features shift, retrain classifier on new features.

2. **50ms sims may not reach steady state** -- peak detector decay tau is 20ms,
   BPF settling is ~5-10ms. 50ms gives only ~1 decay time constant after settling.
   **Mitigation:** Use last 20ms for analysis, or extend to 100ms if needed.

3. **Generalization may fail** -- classifier overfit on 4 points is nearly certain.
   **Mitigation:** Retrain with regularization or more training data.
