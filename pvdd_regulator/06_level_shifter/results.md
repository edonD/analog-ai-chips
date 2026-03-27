# Block 06: Level Shifter — Results

## Topology

**Both directions** use the classic **cross-coupled PMOS** level shifter (4 core transistors + input inverter = 6 devices each). This is the simplest topology with zero static current in both stable states.

- **Low-to-high (level_shifter_up):** SVDD → BVDD. NMOS pull-downs driven by SVDD-domain input. PMOS cross-coupled from BVDD. Wn=10u, Wp=1u (NMOS wide to overcome PMOS at SS 150C).
- **High-to-low (level_shifter_down):** PVDD → SVDD. Same topology with PVDD-domain drive. Wn=2u, Wp=1u (PVDD drive is strong, less NMOS width needed).

## Results Table

| Parameter | Simulated | Spec | Pass/Fail |
|-----------|-----------|------|-----------|
| delay_max_ns | — | ≤ 100 ns | — |
| lth_out_high_margin_V | — | ≥ 0.2 V | — |
| lth_out_low_V | — | ≤ 0.2 V | — |
| htl_out_high_margin_V | — | ≥ 0.2 V | — |
| htl_out_low_V | — | ≤ 0.2 V | — |
| static_power_uA | — | ≤ 5 uA | — |
| works_bvdd_min | — | 1 | — |
| works_bvdd_max | — | 1 | — |
| works_ss_150c | — | 1 | — |
| no_metastable | — | 1 | — |

## Simulation Log

- **Run 0:** Initial design. Cross-coupled PMOS both directions. Wn_up=10u, Wp_up=1u, Wn_dn=2u, Wp_dn=1u. Awaiting first simulation.

## Open Issues

- First simulation not yet run.
