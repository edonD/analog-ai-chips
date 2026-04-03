#!/usr/bin/env python3
"""Expert 09: Integration Expert — Map out exact netlist assembly steps"""
import os, json

BASE = "/home/ubuntu/analog-ai-chips/vibrosense"
OUT = f"{BASE}/10_fullchain/expert_reports/expert_09_integration.md"

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return f"[FILE NOT FOUND: {path}]"

def check_file(path):
    if os.path.exists(path):
        size = os.path.getsize(path)
        return f"EXISTS ({size} bytes)"
    return "MISSING"

# Check all required files per program.md
required = {
    'bias_generator.spice': f"{BASE}/00_bias/bias_generator.spice",
    'ota.spice': f"{BASE}/01_ota/ota.spice",
    'pga.spice': f"{BASE}/02_pga/pga.spice",
    'bpf.spice': f"{BASE}/03_filters/bpf.spice",
    'envelope.spice': f"{BASE}/04_envelope/envelope.spice",
    'rms.spice': f"{BASE}/05_rms_crest/rms.spice",
    'crest.spice': f"{BASE}/05_rms_crest/crest.spice",
    'classifier.spice': f"{BASE}/06_classifier/classifier.spice",
    'adc.spice': f"{BASE}/07_adc/adc.spice",
}

# Check actual available files (what we can use instead)
actual = {
    'Block 00 bias': f"{BASE}/00_bias/design.cir",
    'Block 01 OTA': f"{BASE}/01_ota/ota_foldcasc.spice",
    'Block 02 PGA': f"{BASE}/02_pga/pga.spice",
    'Block 02 PGA real': f"{BASE}/02_pga/pga_real.spice",
    'Block 03 filter bank': f"{BASE}/03_filters/filter_bank_top.spice",
    'Block 03 BPF ch1': f"{BASE}/03_filters/bpf_ch1.spice",
    'Block 03 BPF ch1 real': f"{BASE}/03_filters/bpf_ch1_real.spice",
    'Block 04 envelope': f"{BASE}/04_envelope/envelope_det.spice",
    'Block 04 OTA dep': f"{BASE}/04_envelope/ota_pga_v2.spice",
    'Block 05 rms_crest': f"{BASE}/05_rms_crest/design.cir",
    'Block 06 classifier': f"{BASE}/06_classifier/design.cir",
    'Block 06 clkgen': f"{BASE}/06_classifier/clkgen_3ph.spice",
    'Block 07 ADC v3': f"{BASE}/07_adc_v3/v3_sar_adc.spice",
    'Block 08 digital RTL': f"{BASE}/08_digital/rtl/digital_top.v",
    'Block 08 synthesized': f"{BASE}/08_digital/synth/digital_top_synth.v",
    'Block 09 weights': f"{BASE}/09_training/results/weights_spice.txt",
    'Block 09 vectors': f"{BASE}/09_training/results/feature_vectors_spice.txt",
}

# Check SKY130 PDK
pdk_path = os.environ.get('PDK_ROOT', '/usr/share/pdk')
sky130_lib = None
for p in [
    f"{pdk_path}/sky130A/libs.tech/ngspice/sky130.lib.spice",
    "/usr/local/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice",
    "/home/ubuntu/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice",
    f"{BASE}/05_rms_crest/sky130.lib.spice",  # local copy
]:
    if os.path.exists(p):
        sky130_lib = p
        break

req_report = '\n'.join([f"| {name} | {check_file(path)} |" for name, path in required.items()])
act_report = '\n'.join([f"| {name} | {check_file(path)} |" for name, path in actual.items()])

report = f"""# Expert 09: Integration Plan

## Required Files (per program.md)

| File | Status |
|------|--------|
{req_report}

## Actually Available Files

| File | Status |
|------|--------|
{act_report}

## SKY130 PDK
- Library location: {sky130_lib if sky130_lib else 'NOT FOUND — need to locate'}

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
.lib "{sky130_lib}" tt

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
"""

with open(OUT, 'w') as f:
    f.write(report)
print(f"Expert 09 report written to {OUT}")
