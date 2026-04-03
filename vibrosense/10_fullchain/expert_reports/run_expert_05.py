#!/usr/bin/env python3
"""Expert 05: Block 06 (Classifier MAC) Analysis"""
import os, glob, json

BASE = "/home/ubuntu/analog-ai-chips/vibrosense"
OUT = f"{BASE}/10_fullchain/expert_reports/expert_05_classifier.md"

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return f"[FILE NOT FOUND: {path}]"

design = read_file(f"{BASE}/06_classifier/design.cir")
readme = read_file(f"{BASE}/06_classifier/README.md")
results = read_file(f"{BASE}/06_classifier/full_results.json")
clkgen = read_file(f"{BASE}/06_classifier/clkgen_3ph.spice")

# List all spice files
spice_files = sorted(glob.glob(f"{BASE}/06_classifier/*.spice"))

# Check for classifier.spice
classifier_spice = os.path.exists(f"{BASE}/06_classifier/classifier.spice")

# Find subcircuit definitions in all spice files
all_subckts = []
for f in spice_files:
    content = read_file(f)
    for line in content.split('\n'):
        if line.strip().lower().startswith('.subckt'):
            all_subckts.append(f"{os.path.basename(f)}: {line.strip()}")

report = f"""# Expert 05: Block 06 (Classifier MAC) Analysis

## File Status
- `design.cir`: {'EXISTS ('+str(len(design))+' bytes)' if '[FILE NOT FOUND' not in design else 'EMPTY/MISSING'}
- `classifier.spice`: {'EXISTS' if classifier_spice else 'MISSING — program.md expects this'}
- `clkgen_3ph.spice`: {'EXISTS' if '[FILE NOT FOUND' not in clkgen else 'MISSING'}
- `full_results.json`: {'EXISTS' if '[FILE NOT FOUND' not in results else 'MISSING'}

## SPICE Files Available
{chr(10).join(['- ' + os.path.basename(f) for f in spice_files])}

## Subcircuit Definitions Found
```
{chr(10).join(all_subckts) if all_subckts else 'No subcircuits found in SPICE files'}
```

## design.cir Content
```
{design[:500] if '[FILE NOT FOUND' not in design else 'EMPTY'}
```

## Clock Generator (clkgen_3ph.spice)
```
{clkgen[:1000] if '[FILE NOT FOUND' not in clkgen else 'NOT FOUND'}
```

## Results
```
{results[:2000] if '[FILE NOT FOUND' not in results else 'No results found'}
```

## Integration Requirements (from program.md)
```
Xclass venv1 venv2 venv3 venv4 venv5 vrms vcrest vkurt
+       class_result[3:0] class_valid
+       weights[31:0] thresh[7:0]
+       fsm_sample fsm_evaluate fsm_compare
+       ibias_10u vdd vss classifier
```

## Key Observations
1. **design.cir is empty** — the classifier netlist may be in other files
2. The classifier needs:
   - 8 analog feature inputs
   - 4-class output (4 bits)
   - Weight loading interface (32 capacitors, programmable)
   - 3-phase FSM control (sample, evaluate, compare)
   - Bias current
3. The clkgen_3ph.spice provides the 3-phase clock for the charge-domain MAC
4. For integration, may need to create a behavioral classifier if no transistor-level exists

## Integration Approach
1. If classifier.spice exists and has correct subcircuit — use directly
2. If not, create a behavioral SPICE model that:
   - Samples 8 input voltages
   - Multiplies by weight capacitors (from trained_weights.json)
   - Produces 4-class comparison output
   - Uses switched-capacitor MAC principle
3. The behavioral model is acceptable for integration validation
"""

with open(OUT, 'w') as f:
    f.write(report)
print(f"Expert 05 report written to {OUT}")
