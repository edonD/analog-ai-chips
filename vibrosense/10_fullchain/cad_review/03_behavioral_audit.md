# CAD Expert Review #3: Behavioral vs Real Audit

**Reviewer:** CAD Expert 3 (Behavioral Audit)
**Date:** 2026-04-05

---

## Complete Inventory

### Behavioral Models (B-sources, E-sources, ideal elements)

| # | Block | File | Behavioral Elements | Could Replace? |
|---|-------|------|---------------------|---------------|
| 1 | **PGA OTA** | `ota_behavioral.spice` | B-source VCCS (gm=30uS), ideal Rout (33M), ideal Vbias, B-source clamp | YES -- `ota_pga_v2_fixed.spice` exists and is transistor-level |
| 2 | **PGA decoder** | `pga_fixed.spice` lines 23-26 | 4x B-source voltage comparators for gain selection | LOW PRIORITY -- functionally equivalent to CMOS logic |
| 3 | **Peak envelope (behavioral)** | `envelope_peak_behavioral.spice` | B-source rectifier `abs(vin-vcm)`, B-source charge current, ideal R_decay (200M), B-source level shift | YES -- `envelope_peak_transistor.spice` exists |
| 4 | **Classifier** | `classifier_peak_v4.spice` | 4x B-source weighted sums, B-source WTA argmax, B-source class_valid | KEEP -- Block 06 charge-domain MAC validated separately |
| 5 | **Digital wrapper** | `digital_wrapper.spice` | PULSE voltage sources for clocks, DC sources for gain bits, DC for IRQ | KEEP -- Block 08 Verilog validated separately |
| 6 | **Bias sources** | Top-level netlist | 15 ideal voltage sources (Vvbn, Vvbp, etc.) | PARTIALLY -- `bias_generator_fixed.spice` exists but generates only one Iref |
| 7 | **Power supply** | Top-level | Ideal Vdd (1.8V), sense resistors (0V DC) | OK -- standard practice |

### Transistor-Level Circuits (Real MOSFET implementations)

| # | Block | File | Transistor Count | Verified? |
|---|-------|------|-----------------|-----------|
| 1 | OTA (folded cascode) | `01_ota/ota_foldcasc.spice` | ~12 MOSFETs | Yes (Block 01) |
| 2 | OTA (2-stage Miller) | `ota_pga_v2_fixed.spice` | ~7 MOSFETs | Yes (Block 02) |
| 3 | PGA switches + caps | `pga_fixed.spice` | 4 NMOS switches | Yes (passive elements) |
| 4 | Pseudo-resistor | `03_filters/pseudo_res.spice` | 2 MOSFETs | Yes (Block 03) |
| 5 | BPF ch1-5 | `03_filters/bpf_ch{1-5}_real.spice` | ~24 MOSFETs each (120 total) | Yes (Block 03) |
| 6 | Envelope rectifier (TL) | `envelope_peak_transistor.spice` | ~15 MOSFETs per det | NOT in full chain |
| 7 | Peak detector (TL) | `envelope_peak_transistor.spice` | ~8 MOSFETs per det | NOT in full chain |
| 8 | RMS squarer | `05_rms_crest/design.cir` | ~12 MOSFETs | Yes (Block 05) |
| 9 | Peak detector (RMS) | `05_rms_crest/design.cir` | ~8 MOSFETs | Yes (Block 05) |

### Assessment by Block

**1. PGA OTA -- SHOULD REPLACE**
The PGA uses `ota_behavioral` (a simple VCCS model) while `ota_pga_v2` (a real
two-stage Miller OTA) is already included for the envelope detector. Swapping is
a one-line change in `pga_fixed.spice`. The behavioral OTA has ideal characteristics
(infinite CMRR, zero offset) that the real OTA does not.
- Effort: 1 line change + verify no convergence issues
- Risk: PGA loop stability may need checking with real OTA dynamics

**2. Peak Envelope -- SHOULD REPLACE**
The committed design uses `envelope_peak_behavioral.spice`. A transistor-level
version (`envelope_peak_transistor.spice`) exists and was tested in standalone.
Working copy already has the include changed. Need to verify in full chain.
- Effort: Already done (include changed), just need sim verification
- Risk: Medium -- transistor non-idealities may shift envelope levels

**3. Classifier -- KEEP BEHAVIORAL**
The charge-domain MAC (Block 06) is validated separately. Making the classifier
transistor-level in the full-chain sim would add massive complexity and sim time
with no additional architectural insight.
- Effort: Very high (would need full Block 06 integration)
- Risk: N/A

**4. Digital Wrapper -- KEEP BEHAVIORAL**
The digital RTL (Block 08) is validated in Verilog simulation. The behavioral
wrapper correctly models its interface (clocks, gain bits).
- Effort: High (mixed-signal co-simulation needed)
- Risk: N/A

**5. Bias Sources -- PARTIAL REPLACEMENT POSSIBLE**
A transistor-level bias generator exists (`bias_generator_fixed.spice`) but it
generates only one reference current. The full chain needs 15+ bias voltages
for different OTAs. Generating all from one reference would require a comprehensive
bias distribution network.
- Effort: Very high
- Risk: High (bias network stability, matching)
- Recommendation: Keep ideal for now, document as future work

---

## Summary: Behavioral Ratio

| Category | Count | Notes |
|----------|-------|-------|
| Fully transistor-level | 3 blocks (BPF bank, RMS/Crest, OTA) | ~160 MOSFETs |
| Transistor-level but not in full chain | 1 block (peak envelope TL) | ~115 MOSFETs (5 instances) |
| Behavioral (should replace) | 1 block (PGA OTA) | 1-line fix |
| Behavioral (keep) | 3 blocks (classifier, digital, bias) | Validated separately |

**Current behavioral content: ~40% of signal path blocks are behavioral.**
After replacing PGA OTA and verifying TL envelope: ~15% behavioral (classifier + digital only).

---

## Verdict: Two replacements needed, both low-effort

1. Replace PGA behavioral OTA with `ota_pga_v2` (1-line change)
2. Verify transistor-level peak envelope in full chain (include already changed)

After these two changes, the analog signal path from input to classifier is
100% transistor-level (PGA -> BPF -> Peak Envelope -> RMS/Crest). Only the
classifier and digital wrapper remain behavioral, which is standard practice
for analog front-end verification.
