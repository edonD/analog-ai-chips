# CAD Expert Review #1: Netlist Integrity

**Reviewer:** CAD Expert 1 (Netlist Integrity)
**Date:** 2026-04-05

---

## Top-Level Netlist Analysis (`vibrosense1_peak_normal.spice`)

### Include Chain
The top-level includes 11 subcircuit files. All paths verified to exist.

### Port Consistency Check

| Instantiation | Subcircuit Def | Ports Match? | Notes |
|---------------|---------------|--------------|-------|
| `Xpga vin vout_pga vcm vdd_pga vss g1 g0 pga` | `.subckt pga vin vout vcm vdd vss g1 g0` | YES (7 pins) | OK |
| `Xbpf1 vout_pga vcm vbpf1p vbpf1n vdd_bpf1 vss vcm vbn vbcn vbp vbcp bpf_ch1_real` | `.subckt bpf_ch1_real vinp vinn bp_outp bp_outn vdd vss vcm vbn vbcn vbp vbcp` | YES (11 pins) | OK |
| `Xbpf4 ... vbn_ch4 vbcn_ch4 vbp_ch4 vbcp_ch4 bpf_ch4_real` | `.subckt bpf_ch4_real ... vbn vbcn vbp vbcp` | YES (11 pins) | Per-channel bias correctly connected |
| `Xenv1 vbpf1p vcm venv1 vdd_env1 vss vbn_env vbn_lpf envelope_det` | `.subckt envelope_det vin vcm vout vdd gnd vbn vbn_lpf` | YES (7 pins) | OK |
| `Xrms vout_pga rms_out rms_ref peak_out vdd_rms vss reset vbn_rms vcm rms_crest_top` | `.subckt rms_crest_top inp rms_out rms_ref peak_out vdd vss reset vbn vcm` | YES (9 pins) | OK |
| `Xclass venv1-5 rms_out peak_out rms_ref class_out class_valid_out vdd_class vss classifier_behavioral` | `.subckt classifier_behavioral in0-7 class_out class_valid_out vdd vss` | YES (12 pins) | OK |
| `Xdigital phi_s phi_sb phi_e phi_eb phi_r g1 g0 irq_n class_valid vdd vss digital_wrapper` | `.subckt digital_wrapper phi_s phi_sb phi_e phi_eb phi_r g1 g0 irq_n class_valid vdd vss` | YES (11 pins) | OK |

### Dangling Net Check

**No dangling nets found.** All internal nets are connected:
- `vout_pga`: PGA output -> BPF inputs + RMS input
- `vbpf{1-5}p/n`: BPF outputs -> envelope inputs (p only) + saved
- `venv{1-5}`: envelope outputs -> classifier inputs
- `rms_out`, `peak_out`, `rms_ref`: RMS block -> classifier
- `class_out`: classifier -> saved
- Digital clocks (`phi_s`, etc.): digital wrapper -> saved but NOT connected to any analog block

### Issues Found

1. **ISSUE: Digital clocks are unconnected to analog path.** The digital wrapper
   generates `phi_s`, `phi_sb`, `phi_e`, `phi_eb`, `phi_r` clocks, but NO analog
   block uses them. The classifier operates continuously (no sample/hold phases).
   The FSM phases have no functional effect in the current design.
   **Severity: Low** -- design works without them, but it means the "1 kHz classification
   rate" claim is misleading. The classifier is actually continuous.

2. **ISSUE: `class_valid` mismatch.** The top-level connects `class_valid` from
   the digital wrapper, but the classifier has its own `class_valid_out` (hardcoded
   to 0V). These are different nets. Neither is used functionally.
   **Severity: Low** -- cosmetic, no functional impact.

3. **ISSUE: BPF negative outputs unused.** `vbpf{1-5}n` are saved but not connected
   to anything downstream. Only the positive outputs feed the envelope detectors.
   **Severity: Low** -- single-ended operation is intentional, but the negative
   outputs could carry useful information for a differential envelope detector.

4. **ISSUE: `.option scale=1e-6` removed but some files expect it.** The top-level
   comment says "NOTE: .option scale=1e-6 REMOVED because blocks mix unit conventions."
   The PGA file header says "Use with: .option scale=1e-6". However, the fixed copies
   use explicit `u` suffixes, so this should be OK.
   **Severity: Low** -- verified that fixed copies use explicit units.

### Variant Netlist Check

Checked `vibrosense1_variant_normal_v1.spice`: correctly differs only in the
stimulus `.include` line. All 12 variants follow the same pattern.

---

## Verdict: PASS with minor cosmetic issues

The netlist connectivity is correct. All subcircuit ports match their definitions.
No missing connections that would affect functionality. The digital wrapper is
functionally inert but harmless.
