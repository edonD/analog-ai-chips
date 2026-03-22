# Block 02: Programmable Gain Amplifier (PGA) — Requirements

## Software Required

| Tool | Version | Purpose |
|------|---------|---------|
| ngspice | >=42 | SPICE simulation (AC, transient, noise, FFT) |
| Xschem | >=3.4 | Schematic capture |
| Magic | >=8.3 | Layout, DRC, parasitic extraction |
| KLayout | >=0.29 | Layout viewing, DRC cross-check |
| Netgen | >=1.5 | LVS |
| Python 3 | >=3.10 | Post-processing simulation results |
| matplotlib | >=3.7 | Plotting (gain curves, THD spectra, transients) |
| numpy | >=1.24 | Numerical analysis (FFT, gain error calculation) |

## PDK

SkyWater SKY130A — must be installed at a known path.
Model include: `.lib "<PDK_PATH>/libs.tech/ngspice/sky130.lib.spice" tt`

## Docker

All tools available via: `docker pull hpretl/iic-osic-tools:latest`

## Dependencies

Block 01 OTA (folded-cascode) provides the gain element. For initial development, use the behavioral OTA model from the README interface contract:

```spice
* Behavioral OTA for PGA development
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
| `pga.sch` | Xschem schematic (capacitive-feedback PGA with 4 gain settings) |
| `pga.spice` | SPICE netlist (subcircuit, reusable by downstream blocks) |
| `tb_pga_ac_1x.spice` | AC analysis at gain = 1x |
| `tb_pga_ac_4x.spice` | AC analysis at gain = 4x |
| `tb_pga_ac_16x.spice` | AC analysis at gain = 16x |
| `tb_pga_ac_64x.spice` | AC analysis at gain = 64x |
| `tb_pga_thd.spice` | THD measurement (transient + FFT) at each gain |
| `tb_pga_switching.spice` | Gain switching transient response |
| `tb_pga_noise.spice` | Input-referred noise analysis across gains |
| `tb_pga_corners.spice` | 5-corner + 3-temperature sweep |
| `results.md` | All measured specs with PASS/FAIL per gain setting |
| `pga.mag` | Magic layout |
