# Block 07: Zener Clamp — Results

## Approach

**Topology: Diode-connected HV NMOS stack**

Sky130 has no true Zener diode. We use a stack of diode-connected `sky130_fd_pr__nfet_g5v0d10v5` (5V/10.5V HV NMOS) devices. Each device drops approximately Vth (~0.84V at TT 27C). The MOSFET Vth TC is ~-1 mV/°C, significantly better than PN junction TC (~-2 mV/°C).

**Rationale:** MOSFET Vth TC is roughly half that of a PN junction, so over -40 to 150°C range, the total clamp voltage shift is smaller. A 7-device stack gives ~5.88V onset at TT 27C. TC of 7 devices × -1 mV/°C × 123°C (27→150) = -0.86V → ~5.0V at 150°C. This is tight but potentially feasible.

## Results Table

| Parameter | Simulated | Spec | Pass/Fail |
|-----------|-----------|------|-----------|
| Clamp onset (1mA) TT 27C | — | 5.5–6.2 V | — |
| Clamp at 10mA TT 27C | — | ≤ 6.5 V | — |
| Leakage at 5.0V | — | ≤ 1000 nA | — |
| Leakage at 5.17V | — | ≤ 5000 nA | — |
| Clamp onset 150C | — | ≥ 5.0 V | — |
| Clamp onset -40C | — | ≤ 7.0 V | — |
| Transient peak | — | ≤ 6.5 V | — |
| Peak current at 7V | — | ≥ 100 mA | — |

## Simulation Log

*(updated after each experiment iteration)*

## Open Issues

- TC characterization needed — 150°C constraint is the hardest
- Need to determine optimal W/L and number of devices
