# Block 03: Gm-C Band-Pass Filter Bank — Requirements

## Software Required

| Tool | Version | Purpose |
|------|---------|---------|
| ngspice | >=42 | SPICE simulation (AC, transient, noise, Monte Carlo, PVT corners) |
| Xschem | >=3.4 | Schematic capture |
| Magic | >=8.3 | Layout, DRC, parasitic extraction |
| KLayout | >=0.29 | Layout viewing, DRC cross-check |
| Netgen | >=1.5 | LVS |
| Python 3 | >=3.10 | Post-processing simulation results |
| matplotlib | >=3.7 | Plotting (Bode plots, filter responses, tuning curves) |
| numpy | >=1.24 | Numerical analysis (frequency extraction, Q measurement) |

## PDK

SkyWater SKY130A — must be installed at a known path.
Model include: `.lib "<PDK_PATH>/libs.tech/ngspice/sky130.lib.spice" tt`

## Docker

All tools available via: `docker pull hpretl/iic-osic-tools:latest`

## Dependencies

Block 01 OTA (folded-cascode) provides the transconductor (Gm element) in each filter stage. Each Tow-Thomas biquad requires 3 OTA instances, and there are 5 channels = 15 OTAs total.

For initial development, use the behavioral OTA model:

```spice
* Behavioral OTA — programmable gm via bias current
* gm = 2.5uS at Ibias=500nA; scales linearly with Ibias
.subckt ota_behavioral vip vim vout vdd vss ibias
G1 vout vss cur='5.0 * i(vibias) * (v(vip) - v(vim))'
Vibias ibias ibias_int DC 0
Rout vout vss 400Meg
Cout vout vss 50f
.ends
```

Replace with real OTA netlist from `../01_ota/ota_foldcasc.spice` when Block 01 completes. Report results for BOTH models, flagging any degradation >10%.

## Outputs Produced

| File | Description |
|------|-------------|
| `bpf_ch1.sch` | Xschem schematic — Channel 1 (100-500 Hz) |
| `bpf_ch2.sch` | Xschem schematic — Channel 2 (500-2000 Hz) |
| `bpf_ch3.sch` | Xschem schematic — Channel 3 (2-5 kHz) |
| `bpf_ch4.sch` | Xschem schematic — Channel 4 (5-10 kHz) |
| `bpf_ch5.sch` | Xschem schematic — Channel 5 (10-20 kHz) |
| `bpf_ch1.spice` | SPICE netlist — Channel 1 |
| `bpf_ch2.spice` | SPICE netlist — Channel 2 |
| `bpf_ch3.spice` | SPICE netlist — Channel 3 |
| `bpf_ch4.spice` | SPICE netlist — Channel 4 |
| `bpf_ch5.spice` | SPICE netlist — Channel 5 |
| `bias_dac.sch` | Xschem schematic — 4-bit tuning DAC |
| `bias_dac.spice` | SPICE netlist — tuning DAC |
| `tb_bpf_ac_ch1-5.spice` | AC sweep testbench for each channel |
| `tb_bpf_thd.spice` | THD measurement per channel |
| `tb_bpf_intermod.spice` | Multi-tone intermodulation test |
| `tb_bpf_tuning.spice` | Tuning range verification across PVT |
| `tb_bpf_corners.spice` | 5-corner + 3-temperature sweep |
| `tb_bpf_noise.spice` | Noise analysis per channel |
| `results.md` | All measured specs with PASS/FAIL per channel |
| `bpf_ch1-5.mag` | Magic layouts |
