# Block 02: Feedback Network

**Resistive voltage divider scaling PVDD (5.0V) to the bandgap reference level (1.226V).**

| Parameter | Value | Spec |
|-----------|-------|------|
| VFB at 5.0V, TT 27°C | **1.22596 V** (error 0.039 mV) | 1.226 ± 1 mV |
| Temp drift (-40→150°C) | **0.10 mV** | ≤ 5 mV |
| Corner drift (SS/FF) | **~0 mV** | ≤ 10 mV |
| Divider current | **11.93 µA** | 10–15 µA |
| Noise (1Hz–1MHz) | **35.9 µVrms** | ≤ 50 µVrms |
| MC 3σ (200 runs) | **7.72 mV** | ≤ 10 mV |

**Result: 6/6 specs PASS.**

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
| R_TOP | sky130_fd_pr__res_xhigh_po | 2.0 | 307 | 316.1 |
| R_BOT | sky130_fd_pr__res_xhigh_po | 2.0 | 99.82 | 102.8 |
| **Total** | | | | **418.9** |

Ratio = R_BOT/(R_TOP+R_BOT) = 0.24521. Same resistor type for first-order TC cancellation. Width = 2.0 µm for Pelgrom mismatch matching (3σ < 10 mV).

---

## VFB vs Temperature

![VFB vs Temperature](vfb_vs_temp.png)

Total drift across -40 to 150°C: **0.10 mV**. The matched resistor types have identical TC coefficients, so the ratio is self-compensating.

---

## VFB at PVT Corners

![VFB at PVT Corners](vfb_corners.png)

15 PVT conditions (5 corners × 3 temperatures). Corner drift is essentially zero — the divider ratio is ratiometric and insensitive to global process shifts.

---

## Monte Carlo Mismatch (200 runs)

![MC VFB Histogram](mc_vfb_histogram.png)

| Statistic | Value |
|-----------|-------|
| Mean | 1.2262 V |
| σ | 2.57 mV |
| 3σ | 7.72 mV |
| Min | 1.2197 V |
| Max | 1.2358 V |

3σ < 10 mV spec → **PASS**. Width = 2.0 µm gives sufficient area for Pelgrom matching.

---

## Noise Spectral Density

![Noise at VFB](noise_vfb.png)

Flat thermal noise at 35.9 nV/√Hz. Integrated (1 Hz – 1 MHz): **35.9 µVrms** < 50 µVrms spec.

*Note: Noise is analytical (ngspice behavioral resistors do not generate thermal noise).*
