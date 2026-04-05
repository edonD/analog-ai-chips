# VibroSense-1 Full-Chain Diagnosis

**Date:** 2026-04-05
**Reviewer:** Chief Engineer Supervisor

---

## Current State Summary

VibroSense-1 achieves 4/4 (100%) classification accuracy on 4 synthetic bearing
fault test cases, with ~58 uW estimated system power on SKY130A. This was achieved
over multiple iterations (v1 at 25% -> v4 at 100%) through peak detector envelope
redesign and classifier retraining.

---

## What Works

1. **Signal chain topology is sound.** PGA -> 5-ch BPF -> Peak Envelope -> Classifier
   is a reasonable architecture for bearing fault detection.

2. **Transistor-level BPF bank (Block 03).** 5 Gm-C bandpass filters at 100, 300,
   1k, 3k, 6k Hz. Real transistor-level with SKY130 MOSFETs. These produce
   measurable spectral separation.

3. **Transistor-level RMS/Crest detector (Block 05).** Real analog circuit that
   extracts broadband features.

4. **Power budget.** 51 uW measured analog chain is well within the 300 uW target.

5. **Feature separation.** ENV4 (3 kHz) and ENV5 (6 kHz) show 95-108 mV spread
   between normal and fault conditions -- physically meaningful and consistent
   with bearing fault physics.

6. **Simulation infrastructure.** PWL stimulus generation, ngspice batch simulation,
   automated result parsing and accuracy computation all work.

---

## What's Behavioral (Fake) vs Transistor-Level (Real)

### Transistor-Level (Verified in SPICE)
| Block | File | Status |
|-------|------|--------|
| OTA (folded cascode) | `01_ota/ota_foldcasc.spice` | Real, used by BPFs |
| OTA (2-stage Miller) | `ota_pga_v2_fixed.spice` | Real, used by PGA and rectifier |
| PGA (cap-feedback) | `pga_fixed.spice` | Mostly real -- uses NMOS switches + caps, but OTA is behavioral* |
| BPF bank (5 ch) | `03_filters/bpf_ch{1-5}_real.spice` | Real Gm-C filters |
| Pseudo-resistor | `03_filters/pseudo_res.spice` | Real MOSFET pair |
| RMS/Crest detector | `05_rms_crest/design.cir` | Real transistor-level |
| Peak envelope (new) | `envelope_peak_transistor.spice` | Real, but NOT YET VERIFIED in full chain |

### Behavioral (B-sources / Ideal Elements)
| Block | File | Nature |
|-------|------|--------|
| PGA OTA | `ota_behavioral.spice` | VCCS with ideal Rout, bias, clamp |
| Classifier | `classifier_peak_v4.spice` | B-source weighted sums + WTA |
| Digital wrapper | `digital_wrapper.spice` | PULSE sources for clocks, fixed gain |
| Bias generator | Ideal voltage sources | `Vvbn`, `Vvbp`, etc. in top netlist |

### Critical Finding: PGA Uses Behavioral OTA
The PGA (`pga_fixed.spice`) instantiates `ota_behavioral`, NOT the transistor-level
`ota_pga_v2`. Line 79: `Xota vcm inn vout vdd vss ota_behavioral`. The transistor-level
OTA (`ota_pga_v2_fixed.spice`) is included but only used by the envelope rectifier.

---

## What Simulations Have Actually Been Verified

### Verified (with committed results)
- 4x 200ms transient sims with behavioral peak envelope: 4/4 accuracy (committed ece4155)
- Sim times: 2600-4300 seconds per case (45-72 minutes each)
- All converged successfully, no warnings in logs

### Partially Verified
- Transistor-level envelope detector: standalone testbench ran OK (`tb_envelope_tl.log`,
  0.8s sim time on 50ms test). Output: vout_final=1.038V for a test signal.
  NOT run in full-chain context.

### NOT Verified
- Transistor-level peak envelope in full chain (working copy has the include changed
  but no results exist)
- Variant/generalization test cases (12 variant netlists exist, stimuli generated,
  but no simulations run)
- Any PVT corners
- Any real CWRU data
- PGA with transistor-level OTA

---

## Overfit Risk Assessment

The classifier has 32 weights + 4 biases = 36 free parameters, trained on exactly
4 data points (one per class). This is a rank-4 system with 8 features per point --
the pseudo-inverse gives an exact fit by construction. The 100% training accuracy
is mathematically guaranteed, not a validation result.

The confidence margins confirm this concern:
- Normal: 92% (strong)
- Outer race: 64% (moderate)
- Ball: 54% (weak)
- Inner race: 42% (very weak)

Any feature perturbation from temperature, process variation, or stimulus variation
could flip inner_race and ball classifications.

---

## What Needs to Be Done for Professional Design

### Must Fix (Critical)
1. **Run generalization test** -- simulate variant stimuli to test overfit
2. **Verify transistor-level envelope in full chain** -- the behavioral-to-real
   transition is the biggest risk
3. **Fix PGA OTA** -- currently uses behavioral OTA, should use ota_pga_v2

### Should Fix (Important)
4. **Run at least one PVT corner** -- SS corner at 85C minimum
5. **Retrain classifier with regularization** if generalization fails
6. **Power measurement correction** -- some power values show negative (sign convention)

### Nice to Have (Future Work)
7. Replace all ideal bias sources with transistor-level bias generator
8. Layout and parasitic extraction
9. Real CWRU accelerometer data injection
10. Tape-out on SKY130 MPW shuttle

---

## Simulation Time Budget

Each 200ms full-chain sim takes 45-72 minutes. For practical iteration:
- 50ms sims: ~12-18 min (estimate, proportional)
- 100ms sims: ~25-35 min
- Running 4 cases in parallel: possible (32 GB RAM, each uses ~1 GB)

Strategy: Use 50ms for quick iteration, 100ms for variant tests, 200ms only for final.
