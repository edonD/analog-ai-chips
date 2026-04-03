# Block 05: RMS / Crest Factor Detector — Requirements

## Software Required

| Tool | Version | Purpose |
|------|---------|---------|
| ngspice | ≥42 | SPICE simulation (DC, AC, transient, Monte Carlo) |
| Xschem | ≥3.4 | Schematic capture |
| Magic | ≥8.3 | Layout, DRC, PEX |
| KLayout | ≥0.29 | Layout viewing |
| Netgen | ≥1.5 | LVS |
| Python 3 | ≥3.10 | Post-processing, crest factor computation |
| matplotlib | ≥3.7 | Plotting (RMS linearity, peak hold decay) |
| numpy | ≥1.24 | Numerical analysis, RMS reference calculation |

## PDK
SkyWater SKY130A

## Dependencies
Block 01 OTA (folded-cascode). For initial development, use a behavioral OTA model (VCCS with Gm=10uA/V, Rout=10Mohm, GBW=50kHz). Replace with Block 01 extracted netlist for final verification.

## Outputs Produced

| File | Description |
|------|-------------|
| `rms_crest.sch` | Xschem schematic (RMS detector + peak detector) |
| `rms_crest.spice` | SPICE netlist (subcircuit, reusable) |
| `tb_rms_linearity.spice` | RMS linearity sweep (10mVrms–500mVrms) |
| `tb_rms_freq.spice` | RMS frequency response (10Hz–10kHz) |
| `tb_peak_hold.spice` | Peak hold time measurement |
| `tb_peak_accuracy.spice` | Peak detector accuracy vs frequency |
| `tb_crest_known.spice` | Crest factor vs known waveforms (sine, square, impulse) |
| `tb_rms_noise.spice` | Output noise floor of RMS detector |
| `tb_rms_corners.spice` | 5-corner + 3-temperature sweep |
| `tb_rms_mc.spice` | Monte Carlo (100 runs) for mismatch effects |
| `results.md` | All specs, PASS/FAIL, comparison to ideal RMS |
