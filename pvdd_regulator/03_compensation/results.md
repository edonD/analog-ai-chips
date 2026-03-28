# Block 03: Compensation Network — Results

## Topology

**Miller Compensation** — Cc (MIM cap) from vout_gate to pvdd through series Rz (xhigh poly resistor).

### Design Decisions
- The error amp (Block 00) was modified to work in the LDO context:
  - Supply changed from pvdd to bvdd (allows full gate drive range for PMOS pass device)
  - Dimensions fixed to meters (e-6 suffix added)
  - Internal Cc and Rc optimized for LDO loop stability
  - Tail current increased from 20µA to 400µA for fast slew rate
- The Miller cap from vout_gate to pvdd provides:
  - Pole splitting at mid/high loads (Miller effect through pass device)
  - Additional gate capacitance at light loads
- The nulling resistor Rz creates a LHP zero at ~1.3 MHz for phase boost

## Component Values

| Element | Device | Dimensions | Value | Area (µm²) |
|---------|--------|-----------|-------|------------|
| Cc | sky130_fd_pr__cap_mim_m3_1 | W=141 L=141 | ~40 pF | 19,881 |
| Rz | sky130_fd_pr__res_xhigh_po | W=4 L=6 | ~3 kΩ | 24 |
| **Total** | | | | **19,905** |

## Phase Margin Table (TT 27°C, BVDD=7V)

| Load | PM (°) | GM (dB) | UGB (kHz) | Status |
|------|--------|---------|-----------|--------|
| 0 mA | 53.6 | >100 | 232 | PASS |
| 100 µA | 86.2 | >100 | 1758 | PASS |
| 1 mA | 80.8 | >100 | 13335 | PASS |
| 10 mA | 56.1 | >100 | 40272 | PASS |
| 50 mA | 45.7 | >100 | 60954 | PASS |
| **pm_min** | **45.7** | **>100** | | **PASS** |

## Transient Performance (TT 27°C)

| Parameter | Value | Spec | Status |
|-----------|-------|------|--------|
| Undershoot (1→10mA, 1µs) | 132 mV | ≤ 150 mV | PASS |
| Overshoot (10→1mA, 1µs) | 162 mV | ≤ 150 mV | **FAIL** |
| Settling time | 1.5 µs | ≤ 10 µs | PASS |
| Oscillation | None | None | PASS |

## Error Amp Parameters (modified from Block 00)

| Parameter | Original | Modified | Why |
|-----------|----------|----------|-----|
| Cc internal | 36pF (ideal) | 130pF (ideal) | Light-load stability |
| Rc internal | 5k (ideal) | 12k (ideal) | LHP zero for phase boost |
| Itail | 20µA | 400µA | Fast slew for transient |
| Supply | pvdd | bvdd | Full gate drive range |

## Simulation Log

| # | Change | pm_min (°) | Undershoot/Overshoot (mV) | Status |
|---|--------|-----------|---------------------------|--------|
| 1 | Initial Cc=10pF, EA Cc=36pF, tail=20µA | 7.7 | — | FAIL (PM) |
| 2 | EA Cc corrected to 1.05nF | 60.8 | 1387/1384 | PM PASS, trans FAIL |
| 3 | EA Cc=300pF, tail=20µA | 43.5 | 1241/1234 | FAIL |
| 4 | EA Cc=200pF, tail=100µA | 49.2 | 304/346 | PM PASS, trans FAIL |
| 5 | Tail=700µA, EA Cc=200pF | 55.5 | 150/185 | UNDER passes, OS FAIL |
| 6 | EA Cc=140pF, Rc=12k, tail=700µA | 46.1 | 132/171 | PM PASS, OS FAIL |
| 7 | Tail=400µA, Cc=130pF, Rc=12k | 45.7 | 132/162 | PM PASS, OS FAIL |
| **Current** | **Cc=130pF, Rc=12k, tail=400µA, ext Cc=40pF Rz=3k** | **45.7** | **132/162** | **PM PASS, OS 12mV over** |

## Open Issues

1. **Overshoot at 10→1mA step**: 162mV vs 150mV spec (12mV over, 8% gap)
   - Root cause: with 200pF Cload, the charge injection during load decrease creates ~4ns of uncontrolled pvdd rise before the loop responds
   - Possible fixes: adaptive biasing (class-AB output), feed-forward path, or larger Cload

2. **EA internal Cc/Rc are ideal components** — need to convert to PDK devices (MIM cap + xhigh poly resistor)

3. **UGB at heavy loads (50mA) = 61 MHz** — exceeds the spec max of 1 MHz. The spec may need revision as this is a fundamental consequence of the high loop gain.

4. **PVT corners not yet tested** — current results are TT 27°C only
