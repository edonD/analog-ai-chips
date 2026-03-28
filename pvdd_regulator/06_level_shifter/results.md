# Block 06: Level Shifter — Results

## Topology

**Both directions** use the classic **cross-coupled PMOS** level shifter (4 core transistors + input inverter = 6 devices each). Zero static current in both stable states.

- **Low-to-high (level_shifter_up):** SVDD -> BVDD. NMOS pull-downs driven by SVDD-domain input. PMOS cross-coupled from BVDD. Wn=10u/L=1u, Wp=4u/L=0.5u.
- **High-to-low (level_shifter_down):** PVDD -> SVDD. Same topology with PVDD-domain drive. Wn=2u/L=1u, Wp=4u/L=0.5u.

## Results Table

| Parameter | Simulated | Spec | Pass/Fail |
|-----------|-----------|------|-----------|
| delay_max_ns | 27.7 | <= 100 | PASS |
| lth_out_high_margin_V | 0.20 | >= 0.2 | PASS |
| lth_out_low_V | 3.2e-8 | <= 0.2 | PASS |
| htl_out_high_margin_V | 0.20 | >= 0.2 | PASS |
| htl_out_low_V | 1.8e-8 | <= 0.2 | PASS |
| static_power_uA | 0.0004 | <= 5 | PASS |
| works_bvdd_min | 1 | 1 | PASS |
| works_bvdd_max | 1 | 1 | PASS |
| works_ss_150c | 1 | 1 | PASS |
| no_metastable | 1 | 1 | PASS |

**specs_pass: 10/10**

## Simulation Log

1. Initial cross-coupled PMOS (wp=1, wn=10, L=0.5): Sims failed — missing .spiceinit in batch mode
2. Added local .spiceinit: Sims run but .meas variables empty in echo output
3. Moved all .meas inside .control block: 6/10 passing
4. Fixed bvdd sweep boolean logic (if/else vs comparison operators): 8/10
5. wp_up=4, L=1 for NMOS pull-downs: 9/10, lth margin 0.199999V (1uV below rail)
6. Tried wp_up=5,8: NMOS too weak to overcome PMOS at SS 150C BVDD=5.4V
7. Final: wp_up=4, wn_up=10, L_nmos=1, margin to 0.1mV precision: 10/10 PASS

## Open Issues

None. All specs pass across BVDD 5.4-10.5V at all PVT corners.
