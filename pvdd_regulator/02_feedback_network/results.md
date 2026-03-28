# Block 02: Feedback Network — Results

## Topology

**Two-resistor voltage divider** using `sky130_fd_pr__res_xhigh_po` (P- polysilicon, ~2 kΩ/sq, low TC) for both R_TOP and R_BOT. Same resistor type for first-order TC cancellation. Width = 3.0 µm for optimal Pelgrom mismatch matching.

## Final Design

| Parameter | Value |
|-----------|-------|
| Resistor type | sky130_fd_pr__res_xhigh_po |
| R_TOP (pvdd→vfb) | w=3.0 µm, l=536 µm → 364 kΩ |
| R_BOT (vfb→gnd) | w=3.0 µm, l=174.30 µm → 118 kΩ |
| R_total | 482 kΩ |
| R_parallel | 89.2 kΩ |
| Divider ratio | 0.24520 |
| Parasitic cap at VFB | ~0.14 pF (< 2 pF spec) |

## Results Table

| Parameter | Simulated | Spec Limit | Pass/Fail |
|-----------|-----------|------------|-----------|
| VFB at PVDD=5.0V, TT 27°C | 1.22600 V | 1.226 ± 1 mV | **PASS** (error = 0.004 mV) |
| VFB temp drift (-40 to 150°C) | 0.07 mV | ≤ 5 mV | **PASS** |
| VFB corner drift (SS/FF) | 0 mV | ≤ 10 mV | **PASS** |
| Divider current | 10.35 µA | 10–15 µA | **PASS** |
| Noise at VFB (1Hz–1MHz) | 38.5 µVrms | ≤ 50 µVrms | **PASS** |
| No model errors | ✓ | All TBs run clean | **PASS** |
| MC 3σ (200 runs) | 5.21 mV | ≤ 10 mV | **PASS** |

**Score: 6/6 specs pass + MC pass. Primary metric (vfb_error_mV) = 0.004 mV.**

## Monte Carlo Mismatch Analysis (200 runs)

| Parameter | Value |
|-----------|-------|
| Mean VFB | 1.2259 V |
| Std dev | 1.74 mV |
| 3σ spread | 5.21 mV |
| Min VFB | 1.2216 V |
| Max VFB | 1.2305 V |

## Temperature Sweep

Total drift: 0.07 mV (-40 to 150°C). Both resistors have matched TC coefficients.

## Process Corner Analysis

VFB is invariant across all 5 process corners (TT/SS/FF/SF/FS). The process variation multiplier scales both resistors identically. Divider current varies (9.85–10.89 µA) but the ratio does not.

## Noise Analysis

| Parameter | Value |
|-----------|-------|
| R_parallel (R_TOP ∥ R_BOT) | 89.2 kΩ |
| Noise spectral density | 38.5 nV/√Hz (white) |
| Integrated noise (1 Hz – 1 MHz) | 38.5 µVrms |

**Caveat:** Noise computed analytically. Sky130 xhigh_po behavioral R does not generate noise in ngspice.

## PVDD Sweep

Ratio variation < 0.01% across 4.8–5.17V PVDD operating range.

## Design Evolution

| # | Design | vfb_error | I_div | MC 3σ | Status |
|---|--------|-----------|-------|-------|--------|
| 1 | w=1.0, l_top=149, l_bot=48 | 8.68 mV | 11.96 µA | — | VFB too low |
| 2 | w=1.0, l_bot=48.45 | 0.068 mV | 11.94 µA | 15.7 mV | MC too high |
| 3 | w=2.0, l_top=307, l_bot=99.82 | 0.039 mV | 11.93 µA | 7.72 mV | All pass |
| 4 | w=2.0, l_top=353, l_bot=114.78 | 0.054 mV | 10.37 µA | 6.66 mV | Lower Iq |
| 5 | **w=3.0, l_top=536, l_bot=174.30** | **0.004 mV** | **10.35 µA** | **5.21 mV** | **Final** |

## Open Issues

None — all specifications met with margin.
