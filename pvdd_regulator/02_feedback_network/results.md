# Block 02: Feedback Network — Results

## Topology

**Two-resistor voltage divider** using `sky130_fd_pr__res_xhigh_po` (P- polysilicon, ~2 kΩ/sq, low TC) for both R_TOP and R_BOT. Same resistor type for first-order TC cancellation. Width = 3.0 µm for optimal Pelgrom mismatch matching.

## Final Design

| Parameter | Value |
|-----------|-------|
| Resistor type | sky130_fd_pr__res_xhigh_po |
| R_TOP (pvdd→vfb) | w=3.0 µm, l=536 µm → 365 kΩ |
| R_BOT (vfb→gnd) | w=3.0 µm, l=174.30 µm → 118 kΩ |
| R_total | 483 kΩ |
| R_parallel | 89.4 kΩ |
| Divider ratio | 0.24520 |

## Results Table

| Parameter | Simulated | Spec Limit | Pass/Fail | Notes |
|-----------|-----------|------------|-----------|-------|
| VFB at PVDD=5.0V, TT 27°C | 1.22600 V | 1.226 ± 1 mV | **PASS** (error = 0.004 mV) | Real ngspice sim |
| VFB temp drift (-40 to 150°C) | 0.06 mV | ≤ 5 mV | **PASS** | Real ngspice sim at 7 temps |
| VFB corner drift (SS/FF) | 0 mV | ≤ 10 mV | **PASS** | See caveat below |
| Divider current | 10.35 µA | 10–15 µA | **PASS** | Real ngspice sim |
| Noise at VFB (1Hz–1MHz) | 38.5 µVrms | ≤ 50 µVrms | **PASS** | Analytical, not simulated |
| No model errors | ✓ | All TBs run clean | **PASS** | |
| MC 3σ (500 runs) | 4.69 mV | ≤ 10 mV | **PASS** | Real ngspice MC |

**Score: 6/6 specs pass + MC pass. Primary metric (vfb_error_mV) = 0.004 mV.**

## Caveats and Honest Assessment

### What is trustworthy
- **DC ratio accuracy** (0.004 mV): simulated with real PDK resistor model including end effects, voltage coefficients, and body/head resistance partitioning.
- **Temperature drift** (0.06 mV): simulated at 7 temperatures using `set temp` in ngspice. Both resistors share tc1=-1.47e-3 (body) and tc1=-4.3e-4 (head), so the ratio TC cancels to first order. The residual 0.06 mV comes from different body/head TC weighting between R_TOP and R_BOT.
- **Monte Carlo** (3σ = 4.69 mV): uses the AGAUSS mismatch terms built into the PDK model (body_pelgrom=0.0347, plus head mismatch). Each run generates independent random variations for each resistor instance.
- **Divider current** (10.35 µA): directly measured from simulation.

### What is weak or incomplete
1. **Corner drift = 0 is trivially true by model construction.** The `var_mult` parameter multiplies both `rhead` and `rbody` by the same factor. Both R_TOP and R_BOT use the same subcircuit, so the ratio is algebraically invariant to `var_mult`. This is a property of the model, not necessarily of real silicon. Real process corners could shift different-length resistors differently through mechanisms not captured in this model (line-edge roughness, end-cap variation, doping gradients). Verified via proper combined PVT test (separate files per corner, .param AFTER .include) that VFB is identical across TT/SS/FF at each temperature. The divider current varies correctly (8.87–12.66 µA), confirming the corner parameter is taking effect.

2. **Noise is analytical, not simulated.** The xhigh_po model uses behavioral `r={expression}` with voltage-dependent terms. ngspice does not generate thermal noise for behavioral resistors. The reported 38.5 µVrms is `sqrt(4kTR_par*BW)` with R_par derived from the simulated divider current. This is exact for white thermal noise but omits 1/f noise contribution from the poly resistor. For a resistor divider, 1/f noise is typically negligible above ~100 Hz, so the thermal-only estimate is reasonable.

3. **Parasitic capacitance model is placeholder.** The `sky130_fd_pr__model__parasitic__res_po` subcircuit uses a dummy `0.1 fF/µm²` plate capacitance. The real PDK parasitic model was not available (incomplete PDK installation). The estimated 0.14 pF at VFB is based on this placeholder. Real parasitic caps would come from post-layout extraction.

4. **No full PDK `.lib` corner files for resistors.** The full sky130 `.lib` (from `libs.tech/ngspice/`) was not installed. Instead, we use the `libs.ref` individual model file with manual `var_mult` parameter variation. This misses any corner-specific adjustments to sheet resistance, TC coefficients, or end resistance that the full corner models might include.

## Monte Carlo Mismatch Analysis (500 runs)

| Parameter | Value |
|-----------|-------|
| Mean VFB | 1.2260 V |
| Std dev | 1.56 mV |
| 3σ spread | 4.69 mV |
| Min VFB | 1.2204 V |
| Max VFB | 1.2301 V |
| Runs | 500 |

## Full PVT Verification (proper, separate files per corner)

| Corner | -40°C | 27°C | 150°C | I_div range |
|--------|-------|------|-------|-------------|
| TT | 1.22595 | 1.22600 | 1.22594 | 9.32–12.03 µA |
| SS | 1.22595 | 1.22600 | 1.22594 | 8.87–11.46 µA |
| FF | 1.22595 | 1.22600 | 1.22594 | 9.81–12.66 µA |

Total PVT drift: 0.06 mV. VFB is identical across corners (expected for matched divider with single `var_mult` model).

## Noise Analysis

| Parameter | Value |
|-----------|-------|
| R_parallel (R_TOP ∥ R_BOT) | 89.4 kΩ |
| Noise spectral density (thermal) | 38.5 nV/√Hz (white, analytical) |
| Integrated noise (1 Hz – 1 MHz) | 38.5 µVrms (analytical) |

**Not simulated.** Behavioral resistors in the PDK model do not generate noise in ngspice. Value is sqrt(4kTR_par*BW).

## Design Evolution

| # | Design | vfb_error | I_div | MC 3σ | Status |
|---|--------|-----------|-------|-------|--------|
| 1 | w=1.0, l_top=149, l_bot=48 | 8.68 mV | 11.96 µA | — | VFB too low |
| 2 | w=1.0, l_bot=48.45 | 0.068 mV | 11.94 µA | 15.7 mV | MC too high |
| 3 | w=2.0, l_top=307, l_bot=99.82 | 0.039 mV | 11.93 µA | 7.72 mV | All pass |
| 4 | w=2.0, l_top=353, l_bot=114.78 | 0.054 mV | 10.37 µA | 6.66 mV | Lower Iq |
| 5 | **w=3.0, l_top=536, l_bot=174.30** | **0.004 mV** | **10.35 µA** | **4.69 mV** | **Final** |

## Sensitivity Analysis

| Perturbation | VFB Change | Sensitivity |
|-------------|------------|-------------|
| l_top ± 1 µm | ± 1.73 mV | 1.73 mV/µm |
| l_bot ± 1 µm | ± 5.31 mV | 5.31 mV/µm |

## Pareto Analysis: Area vs MC Matching

| W (µm) | Area (µm²) | MC 3σ (mV) | Status |
|---------|-----------|-----------|--------|
| 1.0 | 228 | 12.7 | FAIL |
| 1.5 | 522 | 8.5 | PASS (min area) |
| 2.0 | 937 | 6.8 | PASS |
| **3.0** | **2,130** | **4.9** | **PASS (chosen)** |
| 4.0 | 3,804 | 3.8 | PASS |

## Open Issues

1. Noise is analytical only — need behavioral-R noise fix or post-layout extraction
2. Parasitic cap model is placeholder — need real PDK parasitic extraction
3. Corner model is single-parameter (`var_mult`) — may miss real corner effects on ratio
4. No post-layout verification yet
