# Block 01: OTA (Folded-Cascode) — Requirements

## Software Required

| Tool | Version | Purpose |
|------|---------|---------|
| ngspice | ≥42 | SPICE simulation (DC, AC, transient, noise, STB) |
| Xschem | ≥3.4 | Schematic capture |
| Magic | ≥8.3 | Layout, DRC, PEX |
| KLayout | ≥0.29 | Layout viewing |
| Netgen | ≥1.5 | LVS |
| Python 3 | ≥3.10 | Post-processing |
| matplotlib | ≥3.7 | Plotting (Bode plots, noise spectra) |
| numpy | ≥1.24 | Numerical analysis |

## PDK
SkyWater SKY130A

## Dependencies
Block 00 (bias generator) provides Iref=500nA. For initial development, use an ideal current source `Ibias 0 vbias 500n` and replace with Block 00 output later.

## Outputs Produced
| File | Description |
|------|-------------|
| `ota_foldcasc.sch` | Xschem schematic |
| `ota_foldcasc.spice` | SPICE netlist (subcircuit, reusable) |
| `tb_ota_ac.spice` | Open-loop AC analysis (gain, BW, PM) |
| `tb_ota_noise.spice` | Noise analysis |
| `tb_ota_dc.spice` | DC sweep (output swing, linearity) |
| `tb_ota_tran.spice` | Step response (slew, settling) |
| `tb_ota_psrr.spice` | PSRR measurement |
| `tb_ota_cmrr.spice` | CMRR measurement |
| `tb_ota_corners.spice` | 5-corner + 3-temperature sweep |
| `tb_ota_mc.spice` | Monte Carlo (200 runs) for offset |
| `results.md` | All specs, PASS/FAIL, operating points |
| `ota_foldcasc.mag` | Magic layout |
