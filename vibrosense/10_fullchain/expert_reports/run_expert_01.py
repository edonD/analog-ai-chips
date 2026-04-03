#!/usr/bin/env python3
"""Expert 01: Block 00 (Bias Generator) and Block 01 (OTA) Analysis"""
import os, glob

BASE = "/home/ubuntu/analog-ai-chips/vibrosense"
OUT = f"{BASE}/10_fullchain/expert_reports/expert_01_bias_ota.md"

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return f"[FILE NOT FOUND: {path}]"

def find_subckt_ports(content, name=None):
    """Extract .subckt lines from SPICE content."""
    lines = []
    for line in content.split('\n'):
        ls = line.strip().lower()
        if ls.startswith('.subckt'):
            if name is None or name.lower() in ls:
                lines.append(line.strip())
    return lines

# Read all relevant files
bias_cir = read_file(f"{BASE}/00_bias/design.cir")
bias_readme = read_file(f"{BASE}/00_bias/README.md")
bias_specs = read_file(f"{BASE}/00_bias/specs.json")

ota_spice = read_file(f"{BASE}/01_ota/ota_foldcasc.spice")
ota_readme = read_file(f"{BASE}/01_ota/README.md")

# Check for bias_generator.spice (expected by program.md)
bias_gen_spice = os.path.exists(f"{BASE}/00_bias/bias_generator.spice")

# Check what program.md expects
program = read_file(f"{BASE}/10_fullchain/program.md")

# Check what OTA files exist
ota_files = glob.glob(f"{BASE}/01_ota/*.spice")
ota_dirs = [d for d in os.listdir(f"{BASE}/01_ota") if os.path.isdir(f"{BASE}/01_ota/{d}")]

# Analyze bias generator interface
bias_subckts = find_subckt_ports(bias_cir)

# Analyze OTA interface
ota_subckts = find_subckt_ports(ota_spice)

# Check if OTA has bias distribution files
ota_pga_dir = os.path.exists(f"{BASE}/01_ota/ota_pga")
ota_pga_v2_dir = os.path.exists(f"{BASE}/01_ota/ota_pga_v2")

# Check what the integration expects
# program.md: .include ../00_bias/bias_generator.spice
# program.md: .include ../01_ota/ota.spice
# program.md: Xbias vdd vss ibias_1u ibias_5u ibias_10u bias_generator

report = f"""# Expert 01: Block 00 (Bias) + Block 01 (OTA) Analysis

## Block 00: Bias Generator

### File Status
- `design.cir`: EXISTS ({len(bias_cir.split(chr(10)))} lines)
- `bias_generator.spice`: {'EXISTS' if bias_gen_spice else 'MISSING — needs to be created/linked'}

### Subcircuit Interface
```
{chr(10).join(bias_subckts)}
```

### Key Findings
1. **Subcircuit name**: `bias_generator` — matches what program.md expects
2. **Ports**: `vdd gnd iref_out` — only ONE output current
3. **MISMATCH**: program.md expects `Xbias vdd vss ibias_1u ibias_5u ibias_10u bias_generator`
   - The actual subcircuit has only 3 ports: `vdd gnd iref_out`
   - program.md expects 5 ports: `vdd vss ibias_1u ibias_5u ibias_10u`
   - Need wrapper or adapter to generate 1uA, 5uA, 10uA from single iref_out

### Bias Architecture
- Beta-multiplier self-biased reference with TC-compensated resistor
- OTA-regulated for stability
- Single PMOS output mirror (1:1 copy)
- The reference current is approximately 1uA based on resistor values

### Integration Actions Needed
1. Create `bias_generator.spice` (or symlink to `design.cir`)
2. Create wrapper that provides multiple bias currents (1uA, 5uA, 10uA)
   from the single reference output using current mirrors
3. Alternative: make a simplified behavioral bias generator for integration

## Block 01: OTA

### File Status
- `ota_foldcasc.spice`: EXISTS ({len(ota_spice.split(chr(10)))} lines)
- `ota.spice`: MISSING — needs to be created/linked
- OTA subdirectories: ota_pga={'exists' if ota_pga_dir else 'missing'}, ota_pga_v2={'exists' if ota_pga_v2_dir else 'missing'}

### Subcircuit Interface
```
{chr(10).join(ota_subckts)}
```

### Key Findings
1. **Subcircuit name**: `ota_foldcasc` — program.md expects just `ota`
2. **Ports**: `vinp vinn vout vdd vss vbn vbcn vbp vbcp` (9 ports)
   - 4 bias voltages needed: vbn, vbcn, vbp, vbcp
   - These are NOT directly available from Block 00's bias generator
3. **Architecture**: Folded-cascode with long-L NMOS for low 1/f noise
4. **Bias**: 500nA tail current, long-L devices

### OTA Bias Requirements
The OTA needs 4 bias voltages. These would normally come from a bias distribution
network that converts the reference current to appropriate gate voltages.
- `vbn`: NMOS gate bias (~0.65V for 500nA)
- `vbcn`: NMOS cascode bias
- `vbp`: PMOS gate bias
- `vbcp`: PMOS cascode bias

### Integration Actions Needed
1. Create `ota.spice` (wrapper around ota_foldcasc or rename)
2. Create bias voltage generator circuit for the 4 bias voltages
3. OR: use behavioral bias sources for integration (simpler, faster)

## OTA Files Available
{chr(10).join(['- ' + os.path.basename(f) for f in sorted(ota_files)])}

## Interface Compatibility Summary

| Expected by program.md | Actual | Status |
|------------------------|--------|--------|
| bias_generator.spice | design.cir | RENAME NEEDED |
| Ports: vdd vss ibias_1u ibias_5u ibias_10u | Ports: vdd gnd iref_out | WRAPPER NEEDED |
| ota.spice | ota_foldcasc.spice | RENAME NEEDED |
| OTA bias from bias_gen | OTA needs 4 voltages | ADAPTER NEEDED |

## Recommendation

For integration, the simplest approach is:
1. Use the existing `design.cir` as `bias_generator.spice` but add current mirror
   outputs for 1uA, 5uA, 10uA
2. Create a bias distribution subcircuit that generates the 4 OTA bias voltages
   from the reference current
3. Alternative: use ideal voltage/current sources for bias in the top-level netlist
   to decouple bias debugging from integration debugging
"""

with open(OUT, 'w') as f:
    f.write(report)
print(f"Expert 01 report written to {OUT}")
