# Block 02: Feedback Network

**Resistive voltage divider scaling PVDD (5.0V) to the bandgap reference level (1.226V).**

| Parameter | Value | Spec |
|-----------|-------|------|
| VFB at 5.0V, TT 27°C | **1.22600 V** (error 0.004 mV) | 1.226 ± 1 mV |
| Temp drift (-40→150°C) | **0.07 mV** | ≤ 5 mV |
| Corner drift (SS/FF) | **0 mV** | ≤ 10 mV |
| Divider current | **10.35 µA** | 10–15 µA |
| Noise (1Hz–1MHz) | **38.5 µVrms** | ≤ 50 µVrms |
| MC 3σ (200 runs) | **5.21 mV** | ≤ 10 mV |
| Parasitic cap at VFB | **~0.14 pF** | ≤ 2 pF |

**Result: 6/6 specs PASS + MC PASS.**

---

## Circuit

```
PVDD (5.0V) ──── XR_TOP ──┬── XR_BOT ──── GND
                           │
                          VFB (~1.226V)
                           │
                     → error amp (−)
```

| Resistor | Device | W (µm) | L (µm) | R (kΩ) |
|----------|--------|--------|--------|--------|
| R_TOP | sky130_fd_pr__res_xhigh_po | 3.0 | 536 | 364 |
| R_BOT | sky130_fd_pr__res_xhigh_po | 3.0 | 174.30 | 118 |
| **Total** | | | | **482** |

Ratio = R_BOT/(R_TOP+R_BOT) = 0.24520. Same resistor type for first-order TC cancellation. Width = 3.0 µm for optimal Pelgrom matching.

---

## VFB vs Temperature

![VFB vs Temperature](vfb_vs_temp.png)

Total drift across -40 to 150°C: **0.07 mV**. Matched TC coefficients make the ratio self-compensating.

---

## VFB at PVT Corners

![VFB at PVT Corners](vfb_corners.png)

15 PVT conditions (5 corners × 3 temperatures). VFB is invariant across process corners — the divider ratio is ratiometric. Only temperature causes variation (0.07 mV total).

---

## Monte Carlo Mismatch (200 runs)

![MC VFB Histogram](mc_vfb_histogram.png)

| Statistic | Value |
|-----------|-------|
| Mean | 1.2259 V |
| σ | 1.74 mV |
| 3σ | 5.21 mV |

3σ < 10 mV spec → **PASS**.

---

## Noise Spectral Density

![Noise at VFB](noise_vfb.png)

Flat thermal noise at 38.5 nV/√Hz. Integrated (1 Hz – 1 MHz): **38.5 µVrms** < 50 µVrms spec.

*Note: Noise is analytical (ngspice behavioral resistors do not generate thermal noise).*

---

## Design Iterations

| # | W (µm) | vfb_error | I_div | MC 3σ |
|---|--------|-----------|-------|-------|
| 1 | 1.0 | 8.68 mV | 11.96 µA | — |
| 2 | 1.0 | 0.068 mV | 11.94 µA | 15.7 mV |
| 3 | 2.0 | 0.039 mV | 11.93 µA | 7.72 mV |
| 4 | 2.0 | 0.054 mV | 10.37 µA | 6.66 mV |
| **5** | **3.0** | **0.004 mV** | **10.35 µA** | **5.21 mV** |
