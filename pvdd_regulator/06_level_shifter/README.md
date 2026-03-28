# Block 06: Level Shifter

## Overview

Bidirectional level shifters for the PVDD 5V LDO regulator, translating digital signals between voltage domains:

- **level_shifter_up**: SVDD (2.2V) to BVDD (5.4--10.5V) -- for enable, mode, and bypass signals
- **level_shifter_down**: PVDD (5.0V) to SVDD (2.2V) -- for UV/OV status flags

Both use the **cross-coupled PMOS** topology with an input inverter, providing rail-to-rail output swing and zero static power in either stable state.

## Architecture

### Cross-Coupled PMOS Level Shifter

Both directions use the same topology (6 transistors):

1. **Input inverter** -- generates complementary drive signals in the input domain
2. **NMOS pull-down pair** -- driven by complementary input-domain signals, pulls cross-coupled nodes to GND
3. **Cross-coupled PMOS pair** -- connected to the output-domain supply, provides positive feedback for full rail swing

The cross-coupling ensures:
- Zero static current (one side always fully ON, the other fully OFF)
- Full rail-to-rail output swing
- No metastable states -- positive feedback resolves any intermediate voltage

### Key Design Decisions

- **NMOS L=1um** (vs minimum 0.5um): Doubles channel length to reduce subthreshold leakage at 150C, ensuring output reaches within 1uV of the supply rail
- **Asymmetric PMOS sizing (up-shifter)**: XMP2 (output side) W=5um, XMP1 W=4um — lower Ron on output node without equally strengthening the PMOS the NMOS must fight
- **Wide NMOS pull-downs (up-shifter W=15um)**: Ensures fast switching across all 15 PVT corners including cold (-40C) where Vth is highest. Down-shifter uses W=2um (PVDD=5V provides ample overdrive)
- **All HV devices** (g5v0d10v5): Safe for up to 10.5V BVDD operation

## Device Sizing

### level_shifter_up (SVDD 2.2V to BVDD)

| Device | Type | W (um) | L (um) | Function |
|--------|------|--------|--------|----------|
| XMN_INV | nfet_g5v0d10v5 | 2 | 0.5 | Input inverter NMOS |
| XMP_INV | pfet_g5v0d10v5 | 4 | 0.5 | Input inverter PMOS |
| XMN1 | nfet_g5v0d10v5 | 15 | 1.0 | Pull-down (gate=in) |
| XMN2 | nfet_g5v0d10v5 | 15 | 1.0 | Pull-down (gate=in_b) |
| XMP1 | pfet_g5v0d10v5 | 4 | 0.5 | Cross-coupled PMOS (internal) |
| XMP2 | pfet_g5v0d10v5 | 5 | 0.5 | Cross-coupled PMOS (output, wider) |

### level_shifter_down (PVDD 5V to SVDD 2.2V)

| Device | Type | W (um) | L (um) | Function |
|--------|------|--------|--------|----------|
| XMN_INV | nfet_g5v0d10v5 | 2 | 0.5 | Input inverter NMOS |
| XMP_INV | pfet_g5v0d10v5 | 4 | 0.5 | Input inverter PMOS |
| XMN1 | nfet_g5v0d10v5 | 2 | 1.0 | Pull-down (gate=in) |
| XMN2 | nfet_g5v0d10v5 | 2 | 1.0 | Pull-down (gate=in_b) |
| XMP1 | pfet_g5v0d10v5 | 4 | 0.5 | Cross-coupled PMOS |
| XMP2 | pfet_g5v0d10v5 | 4 | 0.5 | Cross-coupled PMOS |

## Schematics

### Level Shifter UP (SVDD to BVDD)

![Level Shifter Up](level_shifter_up.png)

### Level Shifter DOWN (PVDD to SVDD)

![Level Shifter Down](level_shifter_down.png)

## Simulation Results

All 10 specs passing. Verified across **all 15 PVT corners** (5 process x 3 temperatures).

| Parameter | Value | Spec | Pass/Fail |
|-----------|-------|------|-----------|
| Propagation delay (worst case) | 8.98 ns | <= 100 ns | PASS |
| LTH output HIGH margin | 0.20 V | >= 0.2 V | PASS |
| LTH output LOW | 0.22 uV | <= 0.2 V | PASS |
| HTL output HIGH margin | 0.20 V | >= 0.2 V | PASS |
| HTL output LOW | 0.52 uV | <= 0.2 V | PASS |
| Static power (worst case) | 0.0021 uA | <= 5 uA | PASS |
| Works at BVDD=5.4V | Yes | Yes | PASS |
| Works at BVDD=10.5V | Yes | Yes | PASS |
| Works at SS 150C | Yes | Yes | PASS |
| No metastable states | Yes | Yes | PASS |

### Switching Waveforms

![Switching Waveforms](switching_waveforms.png)

### Delay vs BVDD

![Delay vs BVDD](delay_vs_bvdd.png)

### Delay at PVT Corners

![Delay PVT](delay_pvt.png)

## PVT Corner Summary (all 15 corners, BVDD=5.4V)

| Corner | -40C | 27C | 150C |
|--------|------|-----|------|
| TT | 5.56 ns | 6.31 ns | 7.65 ns |
| SS | 6.68 ns | 7.52 ns | **8.98 ns** (worst) |
| FF | 4.72 ns | 5.39 ns | 6.61 ns |
| SF | 6.71 ns | 7.43 ns | 8.52 ns |
| FS | 4.89 ns | 5.71 ns | 7.39 ns |

### BVDD Sweep Delays (TT 27C)

| BVDD | tpLH (ns) | tpHL (ns) |
|------|-----------|-----------|
| 5.4V | 3.27 | 4.31 |
| 7.0V | 7.92 | 4.38 |
| 10.5V | 3.82 | 2.79 |

The worst-case corner is SS 150C at BVDD=5.4V, where:
- NMOS Vth is highest (~0.9V), leaving only 1.3V overdrive from SVDD=2.2V
- PMOS pull-up is weakest at minimum BVDD
- Temperature increases subthreshold leakage

The down-shifter (PVDD→SVDD) is consistently faster than the up-shifter because PVDD=5V provides much more NMOS gate overdrive than SVDD=2.2V. The down-shifter never limits the worst-case delay.

## Design Notes and Trade-offs

1. **NMOS pull-down sizing (W=15um for up-shifter)**: The up-shifter faces the toughest challenge — SVDD=2.2V must drive HV NMOS with Vth~0.9V at SS 150C. The wide W=15um ensures enough current to trigger cross-coupled regeneration across all 15 PVT corners, including cold (-40C) where Vth is highest.

2. **Asymmetric PMOS (up-shifter)**: XMP2 (output side) is W=5um vs XMP1 W=4um. The wider output PMOS reduces Ron on the output node for lower voltage drop, without equally strengthening the PMOS that the NMOS must fight during switching.

3. **NMOS channel length (L=1um)**: Using L=1um instead of minimum L=0.5um reduces subthreshold leakage by ~10x at 150C. This ensures the output reaches within 1uV of the supply rail in steady state, at the cost of slower switching (still well within spec at 8.98ns worst case).

4. **Shared topology**: Both directions use the same cross-coupled PMOS structure, differing only in NMOS pull-down width and supply connections. This simplifies verification and layout.

5. **Zero static power**: The cross-coupled PMOS latch ensures one branch is always fully OFF, drawing essentially zero DC current in either stable state (worst case 0.0021 uA across all 15 PVT corners).

6. **Full BVDD range**: Verified at BVDD = 5.4V (minimum, weak PMOS), 7.0V (nominal), and 10.5V (maximum). All HV devices are rated for 10.5V, so no oxide stress concerns.
