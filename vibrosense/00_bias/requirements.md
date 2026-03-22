# Block 00: Bias Generator — Requirements

## Software Required

| Tool | Version | Purpose |
|------|---------|---------|
| ngspice | ≥42 | SPICE simulation (DC, AC, transient, Monte Carlo) |
| Xschem | ≥3.4 | Schematic capture |
| Magic | ≥8.3 | Layout, DRC, parasitic extraction |
| KLayout | ≥0.29 | Layout viewing, DRC cross-check |
| Netgen | ≥1.5 | LVS |
| Python 3 | ≥3.10 | Post-processing simulation results |
| matplotlib | ≥3.7 | Plotting |
| numpy | ≥1.24 | Numerical analysis |

## PDK

SkyWater SKY130A — must be installed at a known path.
Model include: `.lib "<PDK_PATH>/libs.tech/ngspice/sky130.lib.spice" tt`

## Docker

All tools available via: `docker pull hpretl/iic-osic-tools:latest`

## This Block Has No Dependencies

Block 00 can run in complete isolation. It produces bias currents consumed by all other analog blocks.

## Outputs Produced

| File | Description |
|------|-------------|
| `bias_generator.sch` | Xschem schematic |
| `bias_generator.spice` | Extracted SPICE netlist |
| `tb_bias_dc.spice` | DC operating point testbench |
| `tb_bias_temp.spice` | Temperature sweep testbench |
| `tb_bias_supply.spice` | Supply sensitivity testbench |
| `tb_bias_startup.spice` | Power-on transient testbench |
| `tb_bias_corners.spice` | 5-corner analysis |
| `tb_bias_mc.spice` | Monte Carlo (200 runs) |
| `results.md` | All measured specs with PASS/FAIL |
| `bias_generator.mag` | Magic layout |
