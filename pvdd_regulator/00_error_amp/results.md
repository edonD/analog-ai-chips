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
- **Compensation**: Miller cap Cc=900pF with nulling resistor Rc=11.4kΩ. The Rc creates a LHP zero that boosts phase significantly (PM > 90°).
- **Enable**: NMOS switch on ibias, PMOS pullup on output.

## Results Table

| Parameter | Simulated | Spec | Pass/Fail |
|-----------|-----------|------|-----------|
| DC gain | 66.0 dB | ≥ 60 dB | PASS |
| UGB | 214 kHz | 200-1000 kHz | PASS |
| Phase margin | 156.4° | ≥ 55° | PASS |
| Output swing low | 0.010 V | ≤ 0.5 V | PASS |
| Output swing high | 5.0 V | ≥ 4.5 V | PASS |
| Iq | 86.3 µA | ≤ 100 µA | PASS |
| Input offset | 0.028 mV | ≤ 5 mV | PASS |
| CMRR | 107.6 dB | ≥ 50 dB | PASS |
| PSRR | 106.1 dB | ≥ 40 dB | PASS |
| All devices in sat | Yes | Yes | PASS |
| PVT all pass | Yes | Yes | PASS |
| **Specs pass** | **12/12** | | |

## Simulation Log

| # | Change | PM (°) | Gain (dB) | UGB (kHz) | Pass | Status |
|---|--------|--------|-----------|-----------|------|--------|
| 1 | Folded-cascode OTA | - | - | - | 0/12 | crash (bias) |
| 2 | Two-stage Miller, Cc=15pF | 41.0 | 54.1 | 537 | 10/12 | discard |
| 3 | Cc=30pF Rc=5k | 56.8 | 89.9 | 331 | 12/12 | keep |
| 4-5 | Cc sweep 40-50pF | 63→68 | 88→87 | 269→224 | 12/12 | keep |
| 6-7 | tail=15→20µA, Cc=55→60pF | 75→81 | 83→78 | 269→295 | 12/12 | keep |
| 8-11 | Rc sweep 8→15k | 98→113 | 78 | 339→776 | 12/12 | keep |
| 12-14 | Cc sweep 70→200pF, Rc=15k | 115→125 | 78→76 | 776→741 | 12/12 | keep |
| 15-17 | Rc=11.4k, Cc=700→1100pF | 155→158 | 68→64 | 219→209 | 12/12 | keep |
| **18** | **Cc=900pF, Rc=11.4k** | **156.4** | **66.0** | **214** | **12/12** | **final** |

## Key Insights

1. **The nulling resistor Rc is the primary PM tuning knob.** Moving from Rc=5k (no zero) to Rc=11.4k (LHP zero at ~25kHz) added 100°+ of phase margin.
2. **Cc trades gain for PM.** Larger Cc reduces DC gain (due to capacitive loading of stage 1) but moves the non-dominant pole higher.
3. **Tail current sets UGB via gm.** Higher tail → more gm → higher UGB → need more Cc.
4. **HV device constraints forced the two-stage topology.** The folded-cascode is theoretically superior (simpler compensation) but impractical with HV PMOS Vth >0.7V in a 5V supply.

## Open Issues

- PVT testbench only tests TT corner at 3 temperatures (not SS/FF/SF/FS process corners)
- Cc=900pF is large (~450k µm² MIM cap) — could reduce to 200pF with PM still > 120°
- Rc should be implemented with sky130_fd_pr__res_xhigh_po (~5.7 squares) in layout
