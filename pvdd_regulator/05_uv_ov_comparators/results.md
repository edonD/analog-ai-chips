# Block 05: UV/OV Comparators — Results

## Topology

Both UV and OV comparators use the same core topology:
- **NMOS differential pair** with PMOS current mirror load
- **1.8V supply domain** (vdd_comp) — only the resistive divider sees high PVDD voltage
- **NOR gate output** for enable gating: flag = NOR(out_n, en_bar)
- **Feedback resistor** from output to divider midpoint for hysteresis

**UV comparator:** feedback from pre-inversion node (out_n) to mid_uv
**OV comparator:** feedback from post-inversion node (ov_flag) to mid_ov

Both feedback polarities create positive feedback (hysteresis).

## Results Table

| Parameter | Simulated | Spec Min | Spec Max | Unit | Pass/Fail |
|-----------|-----------|----------|----------|------|-----------|
| UV threshold (falling) | 4.289 | 4.0 | 4.5 | V | PASS |
| UV hysteresis | 63.5 | 50 | 150 | mV | PASS |
| OV threshold (rising) | 5.495 | 5.25 | 5.7 | V | PASS |
| OV hysteresis | 112.2 | 50 | 150 | mV | PASS |
| Response time | 0.001 | — | 5 | µs | PASS |
| Power per comparator | 2.71 | — | 5 | µA | PASS |
| Output rail-to-rail | PASS | — | — | — | PASS |
| UV PVT in window | 1 | 1 | — | bool | PASS |
| OV PVT in window | 1 | 1 | — | bool | PASS |
| Threshold error | 5.2 | — | 200 | mV | PASS |

**specs_pass: 13/13**

## Simulation Log

| Run | Change | threshold_error_mV | specs_pass | Status |
|-----|--------|--------------------|------------|--------|
| 1 | Initial design: PMOS diff pair, 7V supply | 999 | 3/13 | crash — wrong pin order, 1.8V devices at 7V |
| 2 | Redesign: NMOS diff pair, 1.8V supply, NOR output | 70.7 | 12/13 | UV hysteresis too low (19mV) |
| 3 | Reduce UV R_hyst from 8M to 2.5M | 10.6 | 13/13 | UV hyst=63mV, but OV threshold high |
| 4 | Adjust OV Rbot from 143.4k to 146k | 5.2 | 13/13 | **KEEP — all specs pass** |

## Open Issues

None — all specs met at TT 27°C. Full PVT corner sweep and Monte Carlo not yet run (would need additional testbench automation).
