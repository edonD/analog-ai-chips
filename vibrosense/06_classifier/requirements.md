# Block 06: Charge-Domain MAC Classifier — Requirements

## Software Required

| Tool | Version | Purpose |
|------|---------|---------|
| ngspice | ≥42 | SPICE simulation (transient, Monte Carlo, noise) |
| Xschem | ≥3.4 | Schematic capture |
| Magic | ≥8.3 | Layout, DRC, PEX |
| KLayout | ≥0.29 | Layout viewing |
| Netgen | ≥1.5 | LVS |
| Python 3 | ≥3.10 | Post-processing, weight generation, test vector injection |
| matplotlib | ≥3.7 | Plotting (MAC linearity, charge injection, classification) |
| numpy | ≥1.24 | Numerical analysis, ideal MAC reference |

## PDK
SkyWater SKY130A

## Dependencies
- Block 09 (training/weights): Provides trained 4-bit weight values for 4-class vibration classification. For initial development, use hand-coded test weights (all-zeros, all-ones, ramp, known patterns). Replace with Block 09 trained weights for final classification validation.
- NO dependency on Block 01 OTA. This block is purely capacitors + switches + comparators.

## Outputs Produced

| File | Description |
|------|-------------|
| `mac_classifier.sch` | Xschem schematic (4× MAC units + WTA + shift register) |
| `mac_classifier.spice` | SPICE netlist (subcircuit, reusable) |
| `tb_mac_linearity.spice` | Single MAC: sweep 1 input, all 16 weight codes, verify monotonic |
| `tb_mac_multi.spice` | All 8 inputs active, verify MAC summation |
| `tb_charge_inject.spice` | Charge injection: toggle switches with zero input |
| `tb_weight_load.spice` | SPI weight loading into shift register |
| `tb_classify_cwru.spice` | Full classification with trained weights + CWRU test vectors |
| `tb_wta.spice` | Winner-take-all comparator verification |
| `tb_mac_corners.spice` | 5-corner + 3-temperature sweep |
| `tb_mac_mc.spice` | Monte Carlo (100 runs) for cap mismatch impact |
| `tb_mac_power.spice` | Power measurement (active + idle) |
| `results.md` | All specs, PASS/FAIL, classification accuracy |
