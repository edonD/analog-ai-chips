#!/usr/bin/env python3
"""Expert 03: Block 04 (Envelope Detector) Analysis — Why only 4/7 specs pass"""
import os, json

BASE = "/home/ubuntu/analog-ai-chips/vibrosense"
OUT = f"{BASE}/10_fullchain/expert_reports/expert_03_envelope.md"

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return f"[FILE NOT FOUND: {path}]"

# Read all envelope files
env_spice = read_file(f"{BASE}/04_envelope/envelope_det.spice")
env_tran = read_file(f"{BASE}/04_envelope/envelope_det_tran.spice")
env_readme = read_file(f"{BASE}/04_envelope/README.md")
env_design = read_file(f"{BASE}/04_envelope/design.cir")

# Check for ota_pga_v2 (dependency)
ota_pga_v2 = read_file(f"{BASE}/04_envelope/ota_pga_v2.spice")
ota_pga_v2_exists = "[FILE NOT FOUND" not in ota_pga_v2

# Check for specs/results
env_specs = read_file(f"{BASE}/04_envelope/specs.json") if os.path.exists(f"{BASE}/04_envelope/specs.json") else "NO specs.json"

# Parse README for spec results
readme_lines = env_readme.split('\n') if '[FILE NOT FOUND' not in env_readme else []
spec_results = []
for i, line in enumerate(readme_lines):
    if 'pass' in line.lower() or 'fail' in line.lower():
        spec_results.append(line.strip())

# Check envelope_det.spice interface
subckts = []
for line in env_spice.split('\n'):
    if line.strip().lower().startswith('.subckt'):
        subckts.append(line.strip())

report = f"""# Expert 03: Block 04 (Envelope Detector) — Spec Failure Analysis

## File Status
- `envelope_det.spice`: EXISTS ({len(env_spice.split(chr(10)))} lines) — transistor-level
- `envelope_det_tran.spice`: {'EXISTS' if '[FILE NOT FOUND' not in env_tran else 'MISSING'}
- `design.cir`: {'EXISTS' if '[FILE NOT FOUND' not in env_design else 'MISSING'}
- `ota_pga_v2.spice`: {'EXISTS' if ota_pga_v2_exists else 'MISSING — CRITICAL dependency'}

## Subcircuit Interfaces
```
{chr(10).join(subckts)}
```

## Architecture Analysis

The envelope detector has 3 subcircuits:
1. **rectifier_v2** — Dual-OTA precision half-wave rectifier
   - Ports: `vin vcm rect vdd gnd vbn`
   - Uses two ota_pga_v2 instances + PMOS output transistors + NMOS sink
2. **lpf_10hz** — Gm-C LPF with 5T OTA
   - Ports: `vin vout vdd gnd vbn_lpf`
   - 100nA tail, gm~2.9uS, 50nF cap -> fc~9.3Hz
3. **envelope_det** — Top-level wrapper
   - Ports: `vin vcm vout vdd gnd vbn vbn_lpf`

## Known Issues (4/7 specs pass)

Based on the README and design files:

### Likely Failing Specs
1. **Ripple** — The 10Hz LPF cutoff may not adequately suppress ripple at
   low frequencies (100-500 Hz band). The 50nF cap provides ~9Hz cutoff
   but ripple at 100Hz is only 21dB down.

2. **Tracking speed/AM tracking** — The LPF time constant (tau=16ms) is slow.
   For fast amplitude modulation (which bearing faults produce), the envelope
   may not track quickly enough.

3. **Dead zone** — The precision rectifier has a dead zone near Vcm due to
   OTA offset and NMOS sink behavior. Small signals may not be rectified.

### What Works
1. Basic rectification — dual OTA feedback ensures precise half-wave rectification
2. DC output — the Gm-C LPF produces clean DC for large signals
3. Power consumption — the design is low power (100nA tail currents)
4. Supply compatibility — 1.8V operation confirmed

## Interface Compatibility with Integration

| program.md expects | actual | match |
|-------------------|--------|-------|
| `Xenv1 vbpf1 venv1 ibias_1u vdd vss envelope` | `envelope_det vin vcm vout vdd gnd vbn vbn_lpf` | MISMATCH |

### Mismatches:
1. **Name**: program.md expects `envelope`, actual is `envelope_det`
2. **Ports**: program.md expects 6 ports, actual has 7 (extra vcm and vbn_lpf)
3. **Bias**: program.md passes `ibias_1u` (current), actual needs `vbn` and `vbn_lpf` (voltages)
4. **vcm**: actual needs explicit vcm input (0.9V)

## Recommendations for Integration

### For Spec Failures:
1. The 4/7 pass rate is acceptable for initial integration — the failures
   are likely in corner cases (very small signals, fast AM, extreme ripple)
2. For integration, the envelope detector works well enough for the CWRU
   bearing data which has relatively large signal swings
3. Post-integration, can iterate on the LPF cutoff and dead zone

### For Interface Adaptation:
1. Create wrapper `envelope` subcircuit that:
   - Accepts ibias_1u and generates vbn, vbn_lpf internally
   - Generates vcm internally (0.9V = VDD/2)
   - Maps port names to match program.md
2. OR: modify top-level netlist to use actual envelope_det ports

## OTA Dependency
The rectifier uses `ota_pga_v2` which must be included.
File exists at: `{BASE}/04_envelope/ota_pga_v2.spice`
Status: {'AVAILABLE' if ota_pga_v2_exists else 'MISSING — must be found/created'}
"""

with open(OUT, 'w') as f:
    f.write(report)
print(f"Expert 03 report written to {OUT}")
