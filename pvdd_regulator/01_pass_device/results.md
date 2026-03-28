# Block 01: Pass Device — Results

## Device Configuration

| Parameter | Value |
|-----------|-------|
| Device | sky130_fd_pr__pfet_g5v0d10v5 |
| W per instance | 100 um |
| L | 0.5 um |
| Parallel instances | 10 |
| Total W | 1.0 mm |
| Topology | 10 parallel subcircuit instances |

## Characterization Table

| Parameter | Simulated | Spec | Status |
|-----------|-----------|------|--------|
| Id dropout TT 27C | 84.23 mA | >= 50 mA | PASS |
| Id dropout SS 150C | 56.83 mA | >= 50 mA | PASS |
| Total width | 1.0 mm | <= 20 mm | PASS |
| Rds_on | 4.75 ohm | <= 20 ohm | PASS |
| Leakage (off) | 2.06e-5 uA | <= 1 uA | PASS |
| Cgs | 1.037 pF | -- | INFO |
| gm at 10mA | 5.4 mA/V | -- | INFO |

## PVT Corner Results

| Corner | -40C | 27C | 150C |
|--------|------|-----|------|
| TT | 103.2 mA | 84.2 mA | 64.3 mA |
| SS | 92.7 mA | 75.2 mA | 56.8 mA |
| FF | 113.6 mA | 93.4 mA | 71.9 mA |

All corners exceed 50 mA spec. Worst case: SS 150C = 56.8 mA (13.6% margin).

## SOA Check

| Parameter | Value |
|-----------|-------|
| Max Vds tested | 5.5V |
| Id at max Vds | 877 mA |
| Max power | 4825 mW |
| Status | PASS |

## Simulation Log

| Run | Change | Result |
|-----|--------|--------|
| 1 | W=100u L=0.5u, 10 parallel, total 1mm | 7/7 PASS, 84mA TT, 57mA SS |

## Open Issues

- None - all specs pass with good margin
- Total width of 1mm is very compact (spec allows 20mm)
- Could reduce to ~9 instances but margin would be tight at SS 150C
