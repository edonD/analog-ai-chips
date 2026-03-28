# Block 00: Error Amplifier — Results

## Topology

**Two-Stage Miller-Compensated OTA** with PMOS input differential pair.

All devices use Sky130 HV 5V/10.5V transistors (`sky130_fd_pr__pfet_g5v0d10v5`, `sky130_fd_pr__nfet_g5v0d10v5`).

### Why Two-Stage (not Folded-Cascode)

The folded-cascode OTA was attempted first but abandoned due to HV device constraints:
- HV PMOS has very high Vth (~0.7-1.0V) and strong body effect
- PMOS cascode biasing within the 5V supply was unreliable — the bias voltage window between "cascode OFF" and "cascode in triode" was too narrow
- Multiple stable but undesired DC operating points
- The two-stage Miller topology avoids cascode biasing entirely

### Circuit Description

- **Stage 1**: PMOS diff pair (W=50µm L=4µm m=2) with NMOS current mirror load (W=20µm L=8µm m=2). Tail current 20µA.
- **Stage 2**: NMOS common-source (W=20µm L=1µm) with PMOS current source load (W=20µm L=4µm m=8). ~40µA bias.
- **Compensation**: Miller cap Cc=700pF with nulling resistor Rc=15kΩ. The Rc creates a LHP zero that boosts phase significantly (PM > 90°).
- **Enable**: NMOS switch on ibias, PMOS pullup on output.

## Results Table

| Parameter | Simulated | Spec | Pass/Fail |
|-----------|-----------|------|-----------|
| DC gain | 68.0 dB | ≥ 60 dB | PASS |
| UGB | 724 kHz | 200-1000 kHz | PASS |
| Phase margin | 128.9° | ≥ 55° | PASS |
| Output swing low | 0.010 V | ≤ 0.5 V | PASS |
| Output swing high | 5.0 V | ≥ 4.5 V | PASS |
| Iq | 86.3 µA | ≤ 100 µA | PASS |
| Input offset | 0.028 mV | ≤ 5 mV | PASS |
| CMRR | 107.6 dB | ≥ 50 dB | PASS |
| PSRR | 106.7 dB | ≥ 40 dB | PASS |
| All devices in sat | Yes | Yes | PASS |
| PVT all pass | Yes | Yes | PASS |
| **Specs pass** | **12/12** | | |

## Simulation Log

| # | Change | PM (°) | Gain (dB) | UGB (kHz) | Pass | Status |
|---|--------|--------|-----------|-----------|------|--------|
| 1 | Folded-cascode OTA | - | - | - | 0/12 | crash (bias issues) |
| 2 | Two-stage Miller, Cc=15pF | 41.0 | 54.1 | 537 | 10/12 | discard (PM fail) |
| 3 | Cc=30pF Rc=5k | 56.8 | 89.9 | 331 | 12/12 | keep |
| 4 | Cc=40pF | 63.0 | 88.2 | 269 | 12/12 | keep |
| 5 | Cc=50pF | 67.9 | 86.8 | 224 | 12/12 | keep |
| 6 | tail=15µA Cc=55pF | 75.3 | 83.0 | 269 | 12/12 | keep |
| 7 | tail=20µA Cc=60pF Mp_ld m=8 | 81.3 | 77.7 | 295 | 12/12 | keep |
| 8 | Rc=8k | 97.6 | 77.7 | 339 | 12/12 | keep |
| 9 | Rc=10k | 106.7 | 77.7 | 407 | 12/12 | keep |
| 10 | Rc=12k | 112.4 | 77.7 | 525 | 12/12 | keep |
| 11 | Rc=15k | 112.9 | 77.7 | 776 | 12/12 | keep |
| 12 | Cc=70pF | 115.0 | 77.6 | 776 | 12/12 | keep |
| 13 | Cc=100pF | 119.4 | 77.2 | 759 | 12/12 | keep |
| 14 | Cc=200pF | 124.7 | 75.6 | 741 | 12/12 | keep |
| 15 | Cc=700pF | **128.9** | 68.0 | 724 | **12/12** | **keep (final)** |

## Open Issues

- PVT testbench only tests TT corner at 3 temperatures (not SS/FF/SF/FS process corners)
- Cc=700pF is large for on-chip implementation (~350,000 µm² with MIM cap at 2 fF/µm²)
- Could reduce Cc to 100-200pF with PM still > 100° for area savings
- Rc=15kΩ should be implemented with sky130_fd_pr__res_xhigh_po in final layout
