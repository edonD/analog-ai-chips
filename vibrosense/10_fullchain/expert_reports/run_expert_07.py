#!/usr/bin/env python3
"""Expert 07: Block 08 (Digital Block) Analysis"""
import os, glob

BASE = "/home/ubuntu/analog-ai-chips/vibrosense"
OUT = f"{BASE}/10_fullchain/expert_reports/expert_07_digital.md"

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return f"[FILE NOT FOUND: {path}]"

# Read all RTL files
rtl_dir = f"{BASE}/08_digital/rtl"
rtl_files = sorted(glob.glob(f"{rtl_dir}/*.v")) if os.path.isdir(rtl_dir) else []

# Read synthesized output
synth_v = read_file(f"{BASE}/08_digital/synth/digital_top_synth.v")
synth_report = read_file(f"{BASE}/08_digital/synth/synth_report.txt")
synth_ys = read_file(f"{BASE}/08_digital/synth/synth.ys")

# Read RTL top
digital_top = read_file(f"{rtl_dir}/digital_top.v") if os.path.isdir(rtl_dir) else "RTL dir not found"
fsm = read_file(f"{rtl_dir}/fsm_classifier.v") if os.path.isdir(rtl_dir) else ""
spi = read_file(f"{rtl_dir}/spi_slave.v") if os.path.isdir(rtl_dir) else ""
regfile = read_file(f"{rtl_dir}/reg_file.v") if os.path.isdir(rtl_dir) else ""

# Read verification
verif = read_file(f"{BASE}/08_digital/verification_report.txt")

# Read README
readme = read_file(f"{BASE}/08_digital/README.md")

# Find module ports in digital_top.v
modules = []
if '[FILE NOT FOUND' not in digital_top:
    for line in digital_top.split('\n'):
        ls = line.strip()
        if ls.startswith('module '):
            modules.append(ls)

report = f"""# Expert 07: Block 08 (Digital Block) Analysis

## File Status

### RTL Files
{chr(10).join(['- ' + os.path.basename(f) for f in rtl_files]) if rtl_files else '- NO RTL FILES FOUND'}

### Synthesis
- `digital_top_synth.v`: {'EXISTS ('+str(len(synth_v))+' chars)' if '[FILE NOT FOUND' not in synth_v else 'MISSING'}
- `synth_report.txt`: {'EXISTS' if '[FILE NOT FOUND' not in synth_report else 'MISSING'}
- `synth.ys`: {'EXISTS' if '[FILE NOT FOUND' not in synth_ys else 'MISSING'}

### Verification
- `verification_report.txt`: {'EXISTS' if '[FILE NOT FOUND' not in verif else 'MISSING'}

## Module Definitions
```
{chr(10).join(modules) if modules else 'No modules found'}
```

## Digital Top Port Summary (from RTL)
```
{digital_top[:2000] if '[FILE NOT FOUND' not in digital_top else 'NOT FOUND'}
```

## Synthesis Report
```
{synth_report[:2000] if '[FILE NOT FOUND' not in synth_report else 'NOT FOUND'}
```

## Verification Report
```
{verif[:2000] if '[FILE NOT FOUND' not in verif else 'NOT FOUND'}
```

## Integration Requirements
The digital block needs a SPICE behavioral wrapper. program.md specifies:
```
Xdigital sck mosi cs_n miso irq_n
+         gain[1:0] tune1[3:0] tune2[3:0] tune3[3:0] tune4[3:0] tune5[3:0]
+         weights[31:0] thresh[7:0] debounce[3:0]
+         class_result[3:0] class_valid
+         fsm_sample fsm_evaluate fsm_compare
+         clk rst_n vdd vss digital_wrapper
```

## Key Findings
1. The digital block has both RTL and synthesized versions
2. For SPICE integration, we need a **behavioral SPICE wrapper** (Verilog-A or PWL)
3. The wrapper translates between digital signals and analog voltages
4. Key functions: SPI config, weight register loading, FSM control, debounce, IRQ

## Integration Approach
For the full-chain simulation, the digital block can be:

1. **Simplified behavioral model** (recommended):
   - Pre-load weights at t=0 (no SPI stimulus needed)
   - Generate 3-phase FSM signals (sample/evaluate/compare) at 1kHz
   - Debounce classifier output and drive IRQ
   - Use voltage-controlled sources in SPICE

2. **Co-simulation** (complex):
   - Use ngspice + Icarus Verilog co-simulation
   - More accurate but much harder to set up

3. **Pure SPICE behavioral** (simplest):
   - PWL sources for FSM clocks
   - Weight values as .param (already in weights_spice.txt)
   - Simple comparator for class output -> IRQ
"""

with open(OUT, 'w') as f:
    f.write(report)
print(f"Expert 07 report written to {OUT}")
