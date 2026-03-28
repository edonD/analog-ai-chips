# Block 02: Feedback Network — Results

## Topology

**Two-resistor voltage divider** using `sky130_fd_pr__res_xhigh_po` (P- polysilicon, ~2 kΩ/sq, low TC) for both R_TOP and R_BOT. Same resistor type for first-order TC cancellation. Width = 2.0 µm for Pelgrom mismatch matching.

## Final Design

| Parameter | Value |
|-----------|-------|
| Resistor type | sky130_fd_pr__res_xhigh_po |
| R_TOP (pvdd→vfb) | w=2.0 µm, l=353 µm → 363.8 kΩ |
| R_BOT (vfb→gnd) | w=2.0 µm, l=114.78 µm → 118.2 kΩ |
| R_total | 482.0 kΩ |
| R_parallel | 89.2 kΩ |
| Divider ratio | 0.24519 |
| Parasitic cap at VFB | ~0.094 pF (< 2 pF spec) |

## Results Table

| Parameter | Simulated | Spec Limit | Pass/Fail |
|-----------|-----------|------------|-----------|
| VFB at PVDD=5.0V, TT 27°C | 1.22595 V | 1.226 ± 1 mV | **PASS** (error = 0.054 mV) |
| VFB temp drift (-40 to 150°C) | 0.08 mV | ≤ 5 mV | **PASS** |
| VFB corner drift (SS/FF) | ~0 mV | ≤ 10 mV | **PASS** |
| Divider current | 10.37 µA | 10–15 µA | **PASS** |
| Noise at VFB (1Hz–1MHz) | 38.4 µVrms | ≤ 50 µVrms | **PASS** |
| No model errors | ✓ | All TBs run clean | **PASS** |
| MC 3σ (200 runs) | 6.66 mV | ≤ 10 mV | **PASS** |

**Score: 6/6 specs pass + MC pass. Primary metric (vfb_error_mV) = 0.054 mV.**

## Monte Carlo Mismatch Analysis (200 runs)

| Parameter | Value |
|-----------|-------|
| Mean VFB | 1.2260 V |
| Std dev | 2.22 mV |
| 3σ spread | 6.66 mV |
| Min VFB | 1.2197 V |
| Max VFB | 1.2319 V |

**3σ = 6.66 mV < 10 mV target → PASS**

## Temperature Sweep

Total drift: 0.08 mV (-40 to 150°C). Both R_TOP and R_BOT have matched TC coefficients (tc1 = -1.47e-3, tc2 = 2.7e-6). The ratio is self-compensating to first order.

## Process Corner Analysis

Corner drift is essentially zero. The process variation multiplier scales both resistors identically. Only mismatch (random) affects the ratio, not global process shifts.

## Noise Analysis

| Parameter | Value |
|-----------|-------|
| R_parallel (R_TOP ∥ R_BOT) | 89.2 kΩ |
| Noise spectral density | 38.4 nV/√Hz (white) |
| Integrated noise (1 Hz – 1 MHz) | 38.4 µVrms |

**Caveat:** Noise computed analytically. Sky130 xhigh_po uses behavioral R expressions that don't generate thermal noise in ngspice. Analytical √(4kTR·BW) is exact for resistor thermal noise.

## PVDD Sweep (Line Regulation)

| PVDD | VFB | Ratio |
|------|-----|-------|
| 4.8 V | 1.177 V | 0.24520 |
| 5.0 V | 1.226 V | 0.24519 |
| 5.17 V | 1.268 V | 0.24518 |

Ratio variation < 0.01% across PVDD operating range. Excellent linearity from the xhigh_po model.

## Design Evolution

| # | Design | vfb_error | I_div | MC 3σ | Status |
|---|--------|-----------|-------|-------|--------|
| 1 | w=1.0, l_top=149, l_bot=48 | 8.68 mV | 11.96 µA | — | VFB too low |
| 2 | w=1.0, l_bot=48.45 | 0.068 mV | 11.94 µA | 15.7 mV | MC too high |
| 3 | w=2.0, l_top=307, l_bot=99.82 | 0.039 mV | 11.93 µA | 7.72 mV | All pass |
| 4 | **w=2.0, l_top=353, l_bot=114.78** | **0.054 mV** | **10.37 µA** | **6.66 mV** | **Final: lower Iq** |

## Open Issues

None — all specifications met.
