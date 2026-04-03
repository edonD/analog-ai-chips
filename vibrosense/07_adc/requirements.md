# Block 07: 8-bit SAR ADC — Requirements

## Software Required

| Tool | Version | Purpose |
|------|---------|---------|
| ngspice | ≥42 | SPICE simulation (transient, FFT, Monte Carlo) |
| Xschem | ≥3.4 | Schematic capture |
| Magic | ≥8.3 | Layout, DRC, PEX |
| KLayout | ≥0.29 | Layout viewing |
| Netgen | ≥1.5 | LVS |
| Python 3 | ≥3.10 | Post-processing, FFT, DNL/INL computation |
| matplotlib | ≥3.7 | Plotting (DNL/INL, FFT spectrum, power) |
| numpy | ≥1.24 | Numerical analysis |

## PDK
SkyWater SKY130A

## Dependencies
Independent block — no dependency on other VibroSense blocks. Adapted from JKU 12-bit SAR ADC design (github.com/iic-jku/SKY130_SAR-ADC1).

## Outputs Produced

| File | Description |
|------|-------------|
| `sar_adc_8b.sch` | Xschem schematic (8-bit SAR ADC) |
| `sar_adc_8b.spice` | SPICE netlist (subcircuit, reusable) |
| `sar_logic.v` | SAR control logic (Verilog, for mixed-signal sim) |
| `comparator.sch` | StrongARM latch comparator schematic |
| `cap_dac.sch` | Binary-weighted capacitor DAC schematic |
| `tb_dnl_inl.spice` | Code density test (slow ramp input, histogram) |
| `tb_enob.spice` | ENOB measurement (FFT of near-Nyquist sine) |
| `tb_power_active.spice` | Active power measurement at 10kS/s |
| `tb_power_sleep.spice` | Sleep mode leakage measurement |
| `tb_wakeup.spice` | Sleep-to-active wakeup transient |
| `tb_adc_corners.spice` | 5-corner + 3-temperature sweep |
| `tb_adc_mc.spice` | Monte Carlo (100 runs) for cap mismatch |
| `results.md` | All specs, PASS/FAIL, ENOB/DNL/INL plots |
