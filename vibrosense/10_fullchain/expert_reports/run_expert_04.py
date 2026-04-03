#!/usr/bin/env python3
"""Expert 04: Block 05 (RMS/Crest Factor) Analysis"""
import os, json

BASE = "/home/ubuntu/analog-ai-chips/vibrosense"
OUT = f"{BASE}/10_fullchain/expert_reports/expert_04_rms_crest.md"

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return f"[FILE NOT FOUND: {path}]"

design = read_file(f"{BASE}/05_rms_crest/design.cir")
readme = read_file(f"{BASE}/05_rms_crest/README.md")
results = read_file(f"{BASE}/05_rms_crest/results_full.json")
results_summary = read_file(f"{BASE}/05_rms_crest/results_summary.txt")

# Find subcircuit interfaces
subckts = []
for line in design.split('\n'):
    if line.strip().lower().startswith('.subckt'):
        subckts.append(line.strip())

# Check what program.md expects
# rms.spice: Xrms vout_pga vrms ibias_5u vdd vss rms_converter
# crest.spice: Xcrest vout_pga vrms vcrest ibias_1u vdd vss crest_detector

# Check for rms.spice and crest.spice
rms_spice = os.path.exists(f"{BASE}/05_rms_crest/rms.spice")
crest_spice = os.path.exists(f"{BASE}/05_rms_crest/crest.spice")

report = f"""# Expert 04: Block 05 (RMS/Crest Factor) Analysis

## File Status
- `design.cir`: EXISTS ({len(design.split(chr(10)))} lines) — full transistor-level
- `rms.spice`: {'EXISTS' if rms_spice else 'MISSING — program.md expects this'}
- `crest.spice`: {'EXISTS' if crest_spice else 'MISSING — program.md expects this'}

## Subcircuit Interfaces
```
{chr(10).join(subckts)}
```

## Architecture
The design has 4 subcircuits:
1. **ota5** — 5T OTA for peak detector (ports: vip vim vout vdd vss vbn)
2. **rms_squarer** — Single-pair MOSFET square-law (ports: inp vcm sq_sig sq_ref vdd vss)
3. **lpf_rc** — Passive R-C LPF at 50Hz (ports: inp out vdd vss)
4. **peak_detector** — Active peak with OTA + hold cap (ports: inp out vdd vss vbn vcm reset)
5. **rms_crest_top** — Top level (ports: inp rms_out rms_ref peak_out vdd vss reset vbn vcm)

## Interface Compatibility

### What program.md expects:
- `rms.spice` with subckt `rms_converter`: ports `vout_pga vrms ibias_5u vdd vss`
- `crest.spice` with subckt `crest_detector`: ports `vout_pga vrms vcrest ibias_1u vdd vss`

### What actually exists:
- `design.cir` with subckt `rms_crest_top`: ports `inp rms_out rms_ref peak_out vdd vss reset vbn vcm`

### Mismatches:
1. **Single combined subcircuit** vs two separate (rms + crest)
2. **Port names** differ: inp vs vout_pga, rms_out vs vrms, etc.
3. **Bias type**: actual needs `vbn vcm` (voltage), program.md passes `ibias_5u` (current)
4. **Reset pin**: actual has reset, program.md doesn't mention it
5. **Crest factor**: NOT computed in analog — the subcircuit provides peak and RMS^2,
   crest = peak/RMS would be computed digitally

## Results Summary
```
{results_summary[:2000] if '[FILE NOT FOUND' not in results_summary else 'No results summary found'}
```

## Integration Approach

1. **Use rms_crest_top directly** in the top-level netlist
2. Create adapter wrappers:
   - `rms_converter` wrapper: takes ibias, generates vbn internally, maps rms_out
   - `crest_detector` wrapper: computes crest from peak/rms (or use behavioral)
3. The actual crest factor is peak_out / sqrt(rms_out - rms_ref), which needs
   analog division — in practice, both voltages go to the classifier as separate features
4. For integration, the 8 features can be remapped: use rms_out and peak_out directly

## Recommendation
The simplest integration path:
1. Include design.cir in the top netlist
2. Instantiate rms_crest_top with correct port mapping
3. Wire rms_out to classifier feature input (broadband_rms)
4. Wire peak_out / rms to crest factor feature (or approximate behaviorally)
5. Tie reset to a digital control signal or hardwire low
"""

with open(OUT, 'w') as f:
    f.write(report)
print(f"Expert 04 report written to {OUT}")
