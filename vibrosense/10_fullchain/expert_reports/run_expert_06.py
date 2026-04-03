#!/usr/bin/env python3
"""Expert 06: Block 07 (ADC v3) Analysis"""
import os, glob

BASE = "/home/ubuntu/analog-ai-chips/vibrosense"
OUT = f"{BASE}/10_fullchain/expert_reports/expert_06_adc.md"

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return f"[FILE NOT FOUND: {path}]"

# Check both ADC directories
adc_design = read_file(f"{BASE}/07_adc/design.cir")
adc_readme = read_file(f"{BASE}/07_adc/README.md")

adc_v3_spice = read_file(f"{BASE}/07_adc_v3/v3_sar_adc.spice")
adc_v3_readme = read_file(f"{BASE}/07_adc_v3/README.md")
adc_v3_comp = read_file(f"{BASE}/07_adc_v3/v3_comparator.spice")
adc_v3_cap = read_file(f"{BASE}/07_adc_v3/v3_cap_dac.spice")

# Check for adc.spice
adc_spice = os.path.exists(f"{BASE}/07_adc/adc.spice")

# Find subcircuits
subckts_v3 = []
for content in [adc_v3_spice, adc_v3_comp, adc_v3_cap]:
    if '[FILE NOT FOUND' not in content:
        for line in content.split('\n'):
            if line.strip().lower().startswith('.subckt'):
                subckts_v3.append(line.strip())

report = f"""# Expert 06: Block 07 (ADC) Analysis

## File Status

### 07_adc (original)
- `design.cir`: {'EXISTS ('+str(len(adc_design))+' bytes, possibly empty)' if '[FILE NOT FOUND' not in adc_design else 'MISSING'}
- `adc.spice`: {'EXISTS' if adc_spice else 'MISSING'}

### 07_adc_v3 (latest version)
- `v3_sar_adc.spice`: {'EXISTS' if '[FILE NOT FOUND' not in adc_v3_spice else 'MISSING'}
- `v3_comparator.spice`: {'EXISTS' if '[FILE NOT FOUND' not in adc_v3_comp else 'MISSING'}
- `v3_cap_dac.spice`: {'EXISTS' if '[FILE NOT FOUND' not in adc_v3_cap else 'MISSING'}

## V3 ADC Subcircuits
```
{chr(10).join(subckts_v3) if subckts_v3 else 'No subcircuits found'}
```

## V3 SAR ADC Content (first 500 chars)
```
{adc_v3_spice[:500] if '[FILE NOT FOUND' not in adc_v3_spice else 'NOT FOUND'}
```

## Integration Requirements
program.md expects: `.include ../07_adc/adc.spice`
The ADC is for debug/monitoring only — not in the critical signal path.

## Key Findings
1. The ADC is NOT in the critical classification path — it's for debug
2. Two versions exist: 07_adc (original, may be empty) and 07_adc_v3 (latest)
3. For integration, the ADC can be:
   - Included if a working netlist exists
   - Replaced with a behavioral model
   - Omitted entirely (with a dummy interface) for initial integration

## Integration Recommendation
1. Use v3_sar_adc.spice from 07_adc_v3 as the ADC
2. Create adc.spice wrapper in 07_adc that includes the v3 version
3. OR: create minimal behavioral ADC for integration
4. ADC is lowest priority — focus on analog signal chain + classifier first
"""

with open(OUT, 'w') as f:
    f.write(report)
print(f"Expert 06 report written to {OUT}")
