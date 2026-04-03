# Expert 09: Integration Plan

## Required Files (per program.md)

| File | Status |
|------|--------|
| bias_generator.spice | MISSING |
| ota.spice | MISSING |
| pga.spice | EXISTS (3264 bytes) |
| bpf.spice | MISSING |
| envelope.spice | MISSING |
| rms.spice | MISSING |
| crest.spice | MISSING |
| classifier.spice | MISSING |
| adc.spice | MISSING |

## Actually Available Files

| File | Status |
|------|--------|
| Block 00 bias | EXISTS (2827 bytes) |
| Block 01 OTA | EXISTS (4033 bytes) |
| Block 02 PGA | EXISTS (3264 bytes) |
| Block 02 PGA real | EXISTS (7174 bytes) |
| Block 03 filter bank | EXISTS (2607 bytes) |
| Block 03 BPF ch1 | EXISTS (1253 bytes) |
| Block 03 BPF ch1 real | EXISTS (975 bytes) |
| Block 04 envelope | EXISTS (2604 bytes) |
| Block 04 OTA dep | EXISTS (2824 bytes) |
| Block 05 rms_crest | EXISTS (4550 bytes) |
| Block 06 classifier | EXISTS (0 bytes) |
| Block 06 clkgen | EXISTS (3073 bytes) |
| Block 07 ADC v3 | EXISTS (4132 bytes) |
| Block 08 digital RTL | EXISTS (6087 bytes) |
| Block 08 synthesized | EXISTS (117698 bytes) |
| Block 09 weights | EXISTS (3526 bytes) |
| Block 09 vectors | EXISTS (9025 bytes) |

## SKY130 PDK
- Library location: /home/ubuntu/analog-ai-chips/vibrosense/05_rms_crest/sky130.lib.spice

## Gap Analysis

### Files That Need Creation

1. **bias_generator.spice** — Wrapper around design.cir, add current mirror outputs
2. **ota.spice** — Rename/wrapper for ota_foldcasc.spice
3. **bpf.spice** — Unified wrapper or use individual channel files
4. **envelope.spice** — Wrapper around envelope_det.spice
5. **rms.spice** — Extract from design.cir or create wrapper
6. **crest.spice** — Extract from design.cir or create wrapper
7. **classifier.spice** — May need behavioral model (design.cir is empty)
8. **adc.spice** — Wrapper around v3_sar_adc.spice
9. **digital_wrapper.spice** — Behavioral SPICE model of digital block

## Recommended Integration Strategy

### Phase A: Behavioral Integration (fast, validates signal chain)
Use behavioral/ideal models where transistor-level doesn't exist:
1. Ideal bias sources (voltage + current)
2. Real PGA (pga_real.spice)
3. Real BPF channels (bpf_ch1-5_real.spice)
4. Real envelope detectors (envelope_det.spice + ota_pga_v2.spice)
5. Real RMS/crest (design.cir from Block 05)
6. **Behavioral classifier** — VCVS-based MAC
7. Behavioral digital wrapper — PWL FSM clocks + voltage comparators
8. Skip ADC for initial integration

### Phase B: Transistor-Level (slower, more accurate)
Replace behavioral blocks with real transistor implementations.

## Top-Level Netlist Assembly Plan

```spice
* vibrosense1_top.spice

* PDK
.lib "/home/ubuntu/analog-ai-chips/vibrosense/05_rms_crest/sky130.lib.spice" tt

* Block subcircuits
.include ../00_bias/design.cir
.include ../01_ota/ota_foldcasc.spice
.include ../02_pga/pga_real.spice
.include ../03_filters/bpf_ch1_real.spice
.include ../03_filters/bpf_ch2_real.spice
.include ../03_filters/bpf_ch3_real.spice
.include ../03_filters/bpf_ch4_real.spice
.include ../03_filters/bpf_ch5_real.spice
.include ../04_envelope/ota_pga_v2.spice
.include ../04_envelope/envelope_det.spice
.include ../05_rms_crest/design.cir
.include ./netlists/classifier_behavioral.spice
.include ./netlists/digital_wrapper.spice

* Weight parameters
.include ../09_training/results/weights_spice.txt

* Supply
Vdd vdd gnd 1.8
Vss vss gnd 0

* Bias (ideal for now)
Ibias_1u vdd ibias_1u DC 1u
Ibias_5u vdd ibias_5u DC 5u
Ibias_10u vdd ibias_10u DC 10u
Vvcm vcm gnd 0.9
Vvbn vbn gnd 0.65
...
```

## Critical Path
1. Assemble top-level with behavioral classifier -> 1 day
2. Run with feature_vectors_spice.txt -> validate classifier accuracy
3. Add real analog front-end -> run with PWL stimulus
4. Measure power, accuracy, latency

## Risk Assessment
| Risk | Impact | Mitigation |
|------|--------|------------|
| Classifier has no transistor netlist | HIGH | Use behavioral model |
| Interface mismatches | MEDIUM | Create adapter wrappers |
| SPICE convergence | HIGH | Use .option gmin, reltol, method=gear |
| Missing CWRU data | MEDIUM | Generate synthetic stimulus |
| Long simulation time | LOW | Use short test (20ms with vectors) |
