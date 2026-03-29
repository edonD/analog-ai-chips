# Block 03: Compensation Network — Results

## Topology

**Miller Compensation + Output Decoupling**
- Cc (50 pF MIM cap) from vout_gate → Rz → pvdd (Miller pole-splitting + LHP zero)
- Rz (4.5 kΩ xhigh poly) nulling resistor (creates zero at ~707 kHz)
- Cout (50 pF MIM cap) from pvdd → gnd (supplements Cload for PM improvement)

### Why This Topology
- Miller Cc provides pole-splitting across the pass device at mid/high loads
- At light loads (gm_pass near zero), Cc acts as a gate cap to AC ground through Cload
- Rz creates a LHP zero for phase boost near UGB
- Cout adds ~25% more output capacitance, improving PM at all loads
- Total area: ~50k µm² (within 50k budget)
- Simple: only 3 components

## Component Values

| Element | Device | Dimensions | Value | Area (µm²) |
|---------|--------|-----------|-------|------------|
| Cc | sky130_fd_pr__cap_mim_m3_1 | W=158 L=158 | ~50 pF | 24,964 |
| Rz | sky130_fd_pr__res_xhigh_po | W=4 L=9 | ~4.5 kΩ | 36 |
| Cout | sky130_fd_pr__cap_mim_m3_1 | W=158 L=158 | ~50 pF | 24,964 |
| **Total** | | | | **49,964** |

## Phase Margin Table (TT 27°C, BVDD=7V)

| Load | PM (°) | GM (dB) | UGB (kHz) | Status |
|------|--------|---------|-----------|--------|
| 0 mA | 45.3 | >100 | 202 | **PASS** |
| 100 µA | 87.3 | >100 | 1567 | **PASS** |
| 1 mA | 80.5 | >100 | 11749 | **PASS** |
| 10 mA | 57.0 | >100 | 36308 | **PASS** |
| 50 mA | 45.2 | >100 | 56234 | **PASS** |
| **pm_min** | **45.2** | **>100** | | **PASS** |

## Transient Performance (TT 27°C)

| Parameter | Value | Spec | Status |
|-----------|-------|------|--------|
| Undershoot (1→10mA, 1µs) | 118 mV | ≤ 150 mV | **PASS** |
| Overshoot (10→1mA, 1µs) | 149.5 mV | ≤ 150 mV | **PASS** (0.5mV margin) |
| Settling time | 1.1 µs | ≤ 10 µs | **PASS** |
| Oscillation | None | None | **PASS** |

## Error Amp Parameters (modified from Block 00 for LDO context)

| Parameter | Original | Modified | Why |
|-----------|----------|----------|-----|
| Cc internal | 36pF (ideal) | 102pF (ideal) | Light-load PM |
| Rc internal | 5k (ideal) | 12.3k (ideal) | LHP zero boosts PM |
| Itail | 20µA | 400µA | Fast slew for <150mV transient |
| Supply | pvdd | bvdd | Gate drive must reach bvdd range |
| Stage 2 load | m=8 | m=8 | Unchanged |

## Evaluation Summary

| Spec | Value | Pass? |
|------|-------|-------|
| pm_min ≥ 45° | 45.24° | **PASS** |
| pm_0mA ≥ 45° | 45.29° | **PASS** |
| pm_100uA ≥ 45° | 87.35° | **PASS** |
| pm_1mA ≥ 45° | 80.51° | **PASS** |
| pm_10mA ≥ 45° | 56.98° | **PASS** |
| pm_50mA ≥ 45° | 45.24° | **PASS** |
| gm ≥ 10 dB | >100 dB | **PASS** |
| undershoot ≤ 150mV | 118.2 mV | **PASS** |
| overshoot ≤ 150mV | 149.5 mV | **PASS** |
| settling ≤ 10µs | 1.085 µs | **PASS** |
| no oscillation | true | **PASS** |
| **PVT PM ≥ 45°** | **not tested** | **MISSING** |
| **Total** | | **11/12** |

## Simulation Log

| # | EA Cc | EA Rc | Tail | Ext Cc | Rz | Cout | pm_min | US/OS (mV) | Status |
|---|-------|-------|------|--------|-----|------|--------|-----------|--------|
| 1 | 36p | 5k | 20µA | 10pF | 1k | — | 7.7° | — | FAIL |
| 2 | 1.05nF | 11.4k | 20µA | 50pF | 2k | — | 60.8° | 1387/1384 | PM OK, trans FAIL |
| 3 | 200p | 10k | 700µA | 50pF | 3k | — | 55.5° | 150/185 | OS FAIL |
| 4 | 130p | 12k | 400µA | 50pF | 3k | — | 45.7° | 132/162 | OS FAIL |
| 5 | 130p | 12k | 400µA | 50pF | 3k | 50pF | 48.9° | 132/162 | OS FAIL |
| 6 | 106p | 12.3k | 400µA | 50pF | 3k | 50pF | 45.1° | 120/151 | OS 1.2mV over |
| 7 | 106p | 12.3k | 400µA | 50pF | 4.5k | 50pF | 45.7° | 120/151 | OS 1mV over |
| **8** | **102p** | **12.3k** | **400µA** | **50pF** | **4.5k** | **50pF** | **45.2°** | **118/150** | **ALL PASS** |

## Open Issues

1. **PVT corners not yet tested** — margins are thin (0.24° PM, 0.5mV overshoot). PVT will likely cause failures.
2. **EA internal Cc/Rc are ideal components** — need PDK device conversion.
3. **UGB at heavy loads is 36-56 MHz** — exceeds 1 MHz nominal spec but PM passes.
4. **Need to add PM margin** — current 0.24° margin at 50mA is razor-thin for PVT. May need architectural changes (adaptive biasing) for robust PVT compliance.
