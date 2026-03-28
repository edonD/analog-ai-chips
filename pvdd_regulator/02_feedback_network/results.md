# Block 02: Feedback Network — Results

## Topology

**Two-resistor voltage divider** using `sky130_fd_pr__res_xhigh_po` (P- polysilicon, ~2 kΩ/sq, low TC) for both R_TOP and R_BOT. Same resistor type for first-order TC cancellation. Width = 2.0 µm for improved Pelgrom mismatch matching.

## Final Design

| Parameter | Value |
|-----------|-------|
| Resistor type | sky130_fd_pr__res_xhigh_po |
| R_TOP (pvdd→vfb) | w=2.0 µm, l=307 µm → 316.1 kΩ |
| R_BOT (vfb→gnd) | w=2.0 µm, l=99.82 µm → 102.8 kΩ |
| R_total | 418.9 kΩ |
| Divider ratio | 0.24521 |

## Results Table

| Parameter | Simulated | Spec Limit | Pass/Fail |
|-----------|-----------|------------|-----------|
| VFB at PVDD=5.0V, TT 27°C | 1.22596 V | 1.226 ± 1 mV | **PASS** (error = 0.039 mV) |
| VFB temp drift (-40 to 150°C) | 0.10 mV | ≤ 5 mV | **PASS** |
| VFB corner drift (SS/FF) | ~0 mV | ≤ 10 mV | **PASS** |
| Divider current | 11.93 µA | 10–15 µA | **PASS** |
| Noise at VFB (1Hz–1MHz) | 35.9 µVrms | ≤ 50 µVrms | **PASS** |
| No model errors | ✓ | All TBs run clean | **PASS** |

**Score: 6/6 specs pass. Primary metric (vfb_error_mV) = 0.039 mV.**

## Monte Carlo Mismatch Analysis (200 runs)

| Parameter | Value |
|-----------|-------|
| Mean VFB | 1.2262 V |
| Std dev | 2.57 mV |
| 3σ spread | 7.72 mV |
| Min VFB | 1.2197 V |
| Max VFB | 1.2358 V |

**3σ = 7.72 mV < 10 mV target → PASS**

Pelgrom coefficient body_pelgrom = 0.0347 for xhigh_po. At w=2.0 µm:
- R_BOT mismatch: σ = 0.0347/√(2×99.82) = 0.245%
- R_TOP mismatch: σ = 0.0347/√(2×307) = 0.140%

## Temperature Sweep

| Temperature | VFB (V) |
|-------------|---------|
| -40°C | 1.22571 |
| 27°C | 1.22596 |
| 150°C | 1.22586 |

Total drift: 0.10 mV (-40 to 150°C). Extremely low because both R_TOP and R_BOT use the same resistor type with matched TC coefficients (tc1 = -1.47e-3, tc2 = 2.7e-6 for body, tc1 = -4.3e-4 for end resistance). The ratio is self-compensating to first order.

## Process Corner Analysis

| Corner | VFB (V) | Drift from TT |
|--------|---------|---------------|
| TT | 1.22596 | 0 |
| SS (+5%) | 1.22596 | ~0 |
| FF (-5%) | 1.22596 | ~0 |
| SF (+2.5%) | 1.22596 | ~0 |
| FS (-2.5%) | 1.22596 | ~0 |

Corner drift is essentially zero because the process variation multiplier scales both resistors identically. The divider ratio is a ratiometric quantity — only mismatch (random) affects it, not global process shift.

## Noise Analysis

| Parameter | Value |
|-----------|-------|
| R_parallel (R_TOP ∥ R_BOT) | 77.6 kΩ |
| Noise spectral density | 35.9 nV/√Hz (white) |
| Integrated noise (1 Hz – 1 MHz) | 35.9 µVrms |

**Caveat:** Noise computed analytically from measured resistance values. The sky130 xhigh_po model uses behavioral R expressions which do not generate thermal noise in ngspice. The analytical computation (√(4kTR·BW)) is exact for resistor thermal noise.

## Simulation Log

| # | Change | vfb_error_mV | specs_pass | MC 3σ (mV) | Status |
|---|--------|-------------|------------|------------|--------|
| 1 | w=1.0, l_top=149, l_bot=48 | 8.68 | 2/6 | — | VFB too low |
| 2 | w=1.0, l_bot=48.4 | 1.02 | 5/6 | — | Close but >1mV |
| 3 | w=1.0, l_bot=48.45 | 0.068 | 6/6 | 15.7 | MC too high |
| 4 | **w=2.0, l_top=307, l_bot=99.82** | **0.039** | **6/6** | **7.72** | **ALL PASS** |

## Open Issues

None — all specifications met including Monte Carlo mismatch.
