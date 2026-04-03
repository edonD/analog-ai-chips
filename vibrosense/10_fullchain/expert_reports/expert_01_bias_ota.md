# Expert 01: Block 00 (Bias) + Block 01 (OTA) Analysis

## Block 00: Bias Generator

### File Status
- `design.cir`: EXISTS (65 lines)
- `bias_generator.spice`: MISSING — needs to be created/linked

### Subcircuit Interface
```
.subckt bias_generator vdd gnd iref_out
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
- `ota_foldcasc.spice`: EXISTS (73 lines)
- `ota.spice`: MISSING — needs to be created/linked
- OTA subdirectories: ota_pga=exists, ota_pga_v2=exists

### Subcircuit Interface
```
.subckt ota_foldcasc vinp vinn vout vdd vss vbn vbcn vbp vbcp
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
- debug.spice
- ota_foldcasc.spice
- sky130_minimal.lib.spice
- tb_closed_loop.spice
- tb_corner_ff.spice
- tb_corner_fs.spice
- tb_corner_sf.spice
- tb_corner_ss.spice
- tb_corner_tt.spice
- tb_investigate.spice
- tb_itail.spice
- tb_load_sweep.spice
- tb_ota_ac.spice
- tb_ota_cmrr.spice
- tb_ota_dc.spice
- tb_ota_op.spice
- tb_ota_psrr.spice
- tb_ota_tran.spice
- tb_temp_-40.spice
- tb_temp_27.spice
- tb_temp_85.spice
- tb_ugb_sweep.spice

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
