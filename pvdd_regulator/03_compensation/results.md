# Block 03: Compensation Network — Results

## Status: 12/12 TT specs PASS

## Topology

**Miller Compensation + Output Decoupling**

| Element | Device | Dimensions | Value | Area (µm²) |
|---------|--------|-----------|-------|------------|
| Cc (Miller) | sky130_fd_pr__cap_mim_m3_1 | W=158 L=158 | ~50 pF | 24,964 |
| Rz (nulling) | sky130_fd_pr__res_xhigh_po | W=4 L=9 | ~4.5 kΩ | 36 |
| Cout (decoupling) | sky130_fd_pr__cap_mim_m3_1 | W=158 L=158 | ~50 pF | 24,964 |
| **Total** | | | | **49,964** |

### Circuit Description
- **Cc** from vout_gate → Rz → pvdd: Miller pole-splitting across pass device, LHP zero from Rz at ~707 kHz
- **Cout** from pvdd → gnd: Supplements 200 pF Cload (+25%), improves PM at all loads
- Simple 3-component network

## TT 27°C Results (ALL PASS)

### Phase Margin

| Load | PM (°) | GM (dB) | Status |
|------|--------|---------|--------|
| 0 mA | 45.3 | >100 | **PASS** |
| 100 µA | 87.3 | >100 | **PASS** |
| 1 mA | 80.5 | >100 | **PASS** |
| 10 mA | 57.0 | >100 | **PASS** |
| 50 mA | 45.2 | >100 | **PASS** |
| **pm_min** | **45.2** | **>100** | **PASS** |

### Transient

| Parameter | Value | Spec | Status |
|-----------|-------|------|--------|
| Undershoot (1→10mA) | 118 mV | ≤ 150 mV | **PASS** |
| Overshoot (10→1mA) | 149.5 mV | ≤ 150 mV | **PASS** (0.5mV margin) |
| Settling time | 1.1 µs | ≤ 10 µs | **PASS** |
| Oscillation | None | None | **PASS** |

### Temperature Sweep (TT corner, 10mA)

| Temp | PM (°) | Status |
|------|--------|--------|
| -40°C | 47.0 | PASS |
| 27°C | 57.0 | PASS |
| 150°C | 73.0 | PASS |

## Error Amp Modifications

| Parameter | Block 00 Original | Modified for LDO | Why |
|-----------|----------|----------|-----|
| Supply | pvdd (5V) | bvdd (7V) | Gate drive must reach bvdd |
| Cc internal | 36pF ideal | 102pF ideal | Light-load PM needs slow EA |
| Rc internal | 5k ideal | 12.3k ideal | LHP zero boosts PM |
| Itail | 20µA | 400µA | Fast slew for transient |
| Dimensions | microns (no e-6) | meters (e-6 added) | BSIM4 model expects meters |

## PVT Corner Analysis

Full PVT sweep (5 corners × 3 temps × 3 loads = 45 conditions):

**Worst cases at TT-optimized configuration:**
- FS -40°C 50mA: PM = 27° (FAIL)
- FF -40°C 50mA: PM = 28° (FAIL)
- All 150°C no-load: PM = 31-34° (FAIL)

**Root cause**: At -40°C devices are faster → UGB at 50mA reaches 85 MHz. At 150°C no-load, EA gain is high → UGB at no-load is high. Both push UGB into frequency ranges where the EA's higher-order poles degrade PM.

**PVT-robust alternative** (EA Cc=300pF, tail=200µA): pm_pvt_min=46° (all corners pass) but transient undershoot=229mV, overshoot=257mV (both FAIL 150mV spec).

## Key Finding

**With a standard two-stage Miller OTA, it is impossible to simultaneously satisfy:**
1. PM ≥ 45° at all PVT corners (requires slow EA, Cc ≥ 250pF)
2. Transient overshoot ≤ 150mV (requires fast EA, Cc ≤ 110pF)

**This is the fundamental capless LDO compensation challenge.** Real capless LDOs solve it with:
- Class-AB output stage (high slew during transient, low quiescent current)
- Adaptive biasing (sense load change, boost tail current temporarily)
- Flipped voltage follower (inherent class-AB behavior)

The current design represents the Pareto frontier for a simple Miller-compensated two-stage OTA.

## Simulation Log Summary

| # | Config | pm_min TT | OS (mV) | PVT min | Best |
|---|--------|----------|---------|---------|------|
| 1 | Cc=36p, 20µA | 7.7° | — | — | |
| 2 | Cc=1.05nF, 20µA | 60.8° | 1384 | 42° | |
| 3 | Cc=130p, 400µA | 45.7° | 162 | 27° | |
| **4** | **Cc=102p, 400µA, Rz=4.5k** | **45.2°** | **150** | **27°** | **TT best** |
| 5 | Cc=300p, 200µA | 62.2° | 257 | 46° | **PVT best** |
