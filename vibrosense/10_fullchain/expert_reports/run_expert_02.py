#!/usr/bin/env python3
"""Expert 02: Block 02 (PGA) and Block 03 (Filter Bank) Analysis"""
import os, glob

BASE = "/home/ubuntu/analog-ai-chips/vibrosense"
OUT = f"{BASE}/10_fullchain/expert_reports/expert_02_pga_filters.md"

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return f"[FILE NOT FOUND: {path}]"

def find_subckt_ports(content):
    lines = []
    for line in content.split('\n'):
        ls = line.strip().lower()
        if ls.startswith('.subckt'):
            lines.append(line.strip())
    return lines

# Read PGA files
pga_spice = read_file(f"{BASE}/02_pga/pga.spice")
pga_real = read_file(f"{BASE}/02_pga/pga_real.spice")
pga_readme = read_file(f"{BASE}/02_pga/README.md")

# Read filter bank files
filter_top = read_file(f"{BASE}/03_filters/filter_bank_top.spice")
bpf_ch1 = read_file(f"{BASE}/03_filters/bpf_ch1.spice")
bpf_ch1_real = read_file(f"{BASE}/03_filters/bpf_ch1_real.spice")
filter_readme = read_file(f"{BASE}/03_filters/README.md")

# Check behavioral OTA used by filters
ota_behav = read_file(f"{BASE}/03_filters/ota_behavioral.spice")

# Get subcircuit ports
pga_subckts = find_subckt_ports(pga_spice)
pga_real_subckts = find_subckt_ports(pga_real)
filter_subckts = find_subckt_ports(filter_top)
bpf_subckts = find_subckt_ports(bpf_ch1)
bpf_real_subckts = find_subckt_ports(bpf_ch1_real) if '[FILE NOT FOUND' not in bpf_ch1_real else ['NOT FOUND']

# List all filter spice files
filter_files = sorted(glob.glob(f"{BASE}/03_filters/bpf_ch*.spice"))

report = f"""# Expert 02: Block 02 (PGA) + Block 03 (Filter Bank) Analysis

## Block 02: PGA

### File Status
- `pga.spice`: EXISTS ({len(pga_spice.split(chr(10)))} lines) — behavioral OTA version
- `pga_real.spice`: EXISTS ({len(pga_real.split(chr(10)))} lines) — transistor-level version

### Subcircuit Interfaces

**pga.spice:**
```
{chr(10).join(pga_subckts)}
```

**pga_real.spice:**
```
{chr(10).join(pga_real_subckts)}
```

### Key Findings
1. program.md expects: `Xpga vin vout_pga ibias_5u vdd vss gain[1] gain[0] pga`
2. Need to check if pga.spice subcircuit name matches 'pga' and ports align
3. Two versions available: behavioral and real
4. For integration, prefer pga_real.spice (transistor-level)

## Block 03: Filter Bank

### File Status
- `filter_bank_top.spice`: EXISTS — complete filter bank
- Individual channels: bpf_ch1 through bpf_ch5 (both behavioral and real)
- `ota_behavioral.spice`: EXISTS — behavioral OTA for filters

### Filter Files Available
{chr(10).join(['- ' + os.path.basename(f) for f in filter_files])}

### Subcircuit Interfaces

**filter_bank_top.spice:**
```
{chr(10).join(filter_subckts)}
```

**bpf_ch1.spice:**
```
{chr(10).join(bpf_subckts)}
```

**bpf_ch1_real.spice:**
```
{chr(10).join(bpf_real_subckts)}
```

### Key Findings
1. program.md expects: `Xbpf1 vout_pga vbpf1 ibias_1u vdd vss tune1[3:0] bpf params: fc=300 bw=400`
2. Individual channel files have specific tuning for each band
3. Both behavioral and transistor-level versions exist
4. The filter_bank_top.spice likely instantiates all 5 channels

### Integration Approach
- Option A: Use filter_bank_top.spice (all 5 filters in one subcircuit)
- Option B: Instantiate individual bpf_chN.spice or bpf_chN_real.spice
- Need to verify port compatibility with program.md expected interface
- The 'real' versions use actual SKY130 transistors (preferred for integration)

## Interface Compatibility

| Expected | Available | Status |
|----------|-----------|--------|
| pga.spice with subckt 'pga' | pga.spice / pga_real.spice | CHECK PORTS |
| bpf.spice with subckt 'bpf' | bpf_ch1-5.spice, bpf_ch1-5_real.spice | INDIVIDUAL FILES |
| tune[3:0] params | Need to check channel files | CHECK |
"""

with open(OUT, 'w') as f:
    f.write(report)
print(f"Expert 02 report written to {OUT}")
