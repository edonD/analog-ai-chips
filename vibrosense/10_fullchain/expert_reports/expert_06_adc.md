# Expert 06: Block 07 (ADC) Analysis

## File Status

### 07_adc (original)
- `design.cir`: EXISTS (0 bytes, possibly empty)
- `adc.spice`: MISSING

### 07_adc_v3 (latest version)
- `v3_sar_adc.spice`: EXISTS
- `v3_comparator.spice`: EXISTS
- `v3_cap_dac.spice`: EXISTS

## V3 ADC Subcircuits
```
.subckt v3_sar_adc vin vref clk convert sleep_n
.subckt v3_comparator inp inn outp outn vdd vss comp_clk sleep_n
.subckt bit_sw bp vref gnd_node ctrl ctrl_b vdd vss
.subckt v2_cap_dac_8b top vref gnd_node
```

## V3 SAR ADC Content (first 500 chars)
```
* ============================================================================
* 8-bit SAR ADC v3 — Top Level
* VibroSense Block 07 — Full Redesign
* Process: SkyWater SKY130A (130 nm CMOS), Supply: 1.8V, Vref: 1.2V
* ============================================================================
*
* Changes from v2:
*   1. New comparator: Pre-amp + StrongARM latch (offset < 1mV all corners)
*   2. DAC reset fix: AND NOT(sample) gates all DAC outputs during sampling
*   3. Honest testbench ordering
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
