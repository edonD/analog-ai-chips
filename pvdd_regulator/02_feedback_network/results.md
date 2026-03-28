# Block 02: Feedback Network — Results

## Topology

**Two-resistor voltage divider** using `sky130_fd_pr__res_xhigh_po` (P- polysilicon, ~2 kΩ/sq, low TC) for both R_TOP and R_BOT. Same resistor type for first-order TC cancellation.

## Final Design

| Parameter | Value |
|-----------|-------|
| Resistor type | sky130_fd_pr__res_xhigh_po |
| R_TOP (pvdd→vfb) | w=1.0 µm, l=149 µm → 316.2 kΩ |
| R_BOT (vfb→gnd) | w=1.0 µm, l=48.45 µm → 102.7 kΩ |
| R_total | 418.9 kΩ |
| Divider ratio | 0.24521 |

## Results Table

| Parameter | Simulated | Spec Limit | Pass/Fail |
|-----------|-----------|------------|-----------|
| VFB at PVDD=5.0V, TT 27°C | 1.22607 V | 1.226 ± 1 mV | **PASS** (error = 0.068 mV) |
| VFB temp drift (-40 to 150°C) | 0.15 mV | ≤ 5 mV | **PASS** |
| VFB corner drift (SS/FF) | ~0 mV | ≤ 10 mV | **PASS** |
| Divider current | 11.94 µA | 10–15 µA | **PASS** |
| Noise at VFB (1Hz–1MHz) | 35.8 µVrms | ≤ 50 µVrms | **PASS** |
| No model errors | ✓ | All TBs run clean | **PASS** |

**Score: 6/6 specs pass. Primary metric (vfb_error_mV) = 0.068 mV.**

## Temperature Sweep

| Temperature | VFB (V) |
|-------------|---------|
| -40°C | 1.22486 |
| 27°C | 1.22607 |
| 150°C | 1.22471 |

Total drift: 0.15 mV (-40 to 150°C). Extremely low because both R_TOP and R_BOT use the same resistor type with matched TC coefficients (tc1 = -1.47e-3, tc2 = 2.7e-6). The ratio is self-compensating.

## Process Corner Analysis

| Corner | VFB (V) | Drift from TT |
|--------|---------|---------------|
| TT | 1.22607 | 0 |
| SS (+5%) | 1.22607 | ~0 |
| FF (-5%) | 1.22607 | ~0 |

Corner drift is essentially zero because the process variation parameter (`var_mult`) scales both resistors identically. The only second-order effect is end resistance (`rhead`) having a different variation coefficient than body resistance — negligible for long resistors.

## Noise Analysis

| Parameter | Value |
|-----------|-------|
| R_parallel (R_TOP ∥ R_BOT) | 77.5 kΩ |
| Noise spectral density | 35.8 nV/√Hz |
| Integrated noise (1 Hz – 1 MHz) | 35.8 µVrms |

**Caveat:** Noise computed analytically from measured resistance values. The sky130 xhigh_po model uses behavioral R expressions which do not generate thermal noise in ngspice. The analytical computation (sqrt(4kTR·BW)) is exact for thermal noise of a resistor.

## Simulation Log

| # | Change | vfb_error_mV | specs_pass | Status |
|---|--------|-------------|------------|--------|
| 1 | Initial: l_top=149, l_bot=48 | 8.68 | 2/6 | VFB too low, testbench bugs |
| 2 | l_bot=48.4, fix temp/corner/noise TBs | 1.02 | 5/6 | Noise integration wrong |
| 3 | l_bot=48.45, fix noise (square before integ) | 0.068 | 5/6 | Noise sim unreliable |
| 4 | Analytical noise from R_parallel | 0.068 | 6/6 | **ALL PASS** |

## Open Issues

- Monte Carlo mismatch analysis not yet run (need MC testbench)
- Corner analysis currently uses scalar `var_mult` — should verify with separate SS/FF model files if available
- Noise is analytical only (ngspice limitation with behavioral resistors)
