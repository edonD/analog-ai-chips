# Block 04: Envelope Detector — Requirements

## Software Required

| Tool | Version | Purpose |
|------|---------|---------|
| ngspice | >=42 | SPICE simulation (DC, AC, transient, noise) |
| Xschem | >=3.4 | Schematic capture |
| Magic | >=8.3 | Layout, DRC, parasitic extraction |
| KLayout | >=0.29 | Layout viewing, DRC cross-check |
| Netgen | >=1.5 | LVS |
| Python 3 | >=3.10 | Post-processing simulation results |
| matplotlib | >=3.7 | Plotting (rectification curves, transient waveforms, ripple) |
| numpy | >=1.24 | Numerical analysis (RMS error, ripple measurement) |

## PDK

SkyWater SKY130A — must be installed at a known path.
Model include: `.lib "<PDK_PATH>/libs.tech/ngspice/sky130.lib.spice" tt`

## Docker

All tools available via: `docker pull hpretl/iic-osic-tools:latest`

## Dependencies

Block 01 OTA (folded-cascode) provides the active rectifier element and the LPF integrator. Each envelope detector channel requires 2-3 OTA instances (rectifier + LPF), and there are 5 channels = 10-15 OTAs total.

For initial development, use the behavioral OTA model:

```spice
* Behavioral OTA for envelope detector development
.subckt ota_behavioral vip vim vout vdd vss
G1 vout vss cur='2.5e-6 * (v(vip) - v(vim))'
Rout vout vss 400Meg
Cout vout vss 50f
.ends
```

Replace with real OTA netlist from `../01_ota/ota_foldcasc.spice` when Block 01 completes. Report results for BOTH behavioral and real OTA models, flagging any degradation >10%.

## Outputs Produced

| File | Description |
|------|-------------|
| `envelope_det.sch` | Xschem schematic (single channel: rectifier + LPF) |
| `envelope_det.spice` | SPICE netlist (subcircuit, instantiated 5 times in full chain) |
| `tb_env_amp_sweep.spice` | Amplitude sweep testbench (5 mV to 500 mV) |
| `tb_env_am_track.spice` | AM-modulated signal tracking testbench |
| `tb_env_burst.spice` | Burst detection testbench (on/off transient) |
| `tb_env_ripple.spice` | Ripple measurement at various input frequencies |
| `tb_env_corners.spice` | 5-corner + 3-temperature sweep |
| `results.md` | All measured specs with PASS/FAIL per metric |
| `envelope_det.mag` | Magic layout |
