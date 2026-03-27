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
| Id dropout TT 27C | 84.2 mA | >= 50 mA | PASS |
| Id dropout SS 150C | 56.8 mA | >= 50 mA | PASS |
| Total width | 1.0 mm | <= 20 mm | PASS |
| Rds_on | 4.75 ohm | <= 20 ohm | PASS |
| Leakage (off) | 0.02 uA | <= 1 uA | PASS |
| Cgs | 1.04 pF | measured | INFO |
| gm at 10mA | measured | measured | INFO |

## Simulation Log

| Run | Change | Result |
|-----|--------|--------|
| 1 | W=100u L=0.5u, 10 parallel, total 1mm | 7/7 PASS, 84mA TT, 57mA SS |

## Open Issues

- None - all specs pass with good margin
- Total width of 1mm is very compact (spec allows 20mm)
