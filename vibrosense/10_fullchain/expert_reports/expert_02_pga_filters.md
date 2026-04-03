# Expert 02: Block 02 (PGA) + Block 03 (Filter Bank) Analysis

## Block 02: PGA

### File Status
- `pga.spice`: EXISTS (81 lines) — behavioral OTA version
- `pga_real.spice`: EXISTS (158 lines) — transistor-level version

### Subcircuit Interfaces

**pga.spice:**
```
.subckt pga vin vout vcm vdd vss g1 g0
```

**pga_real.spice:**
```
.subckt decoder_2to4 g1 g0 sel0 sel1 sel2 sel3 vdd vss
.subckt pga_real vin vout vcm vdd vss vbn vbcn vbp vbcp g1 g0
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
- bpf_ch1.spice
- bpf_ch1_real.spice
- bpf_ch2.spice
- bpf_ch2_real.spice
- bpf_ch3.spice
- bpf_ch3_real.spice
- bpf_ch4.spice
- bpf_ch4_real.spice
- bpf_ch5.spice
- bpf_ch5_real.spice

### Subcircuit Interfaces

**filter_bank_top.spice:**
```
.subckt filter_bank_top vinp vinn
```

**bpf_ch1.spice:**
```
.subckt bpf_ch1 vin bp_out vdd vss vcm
```

**bpf_ch1_real.spice:**
```
.subckt bpf_ch1_real vinp vinn bp_outp bp_outn vdd vss vcm vbn vbcn vbp vbcp
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
