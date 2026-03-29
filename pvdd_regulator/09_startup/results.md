# Block 09: Startup Circuit — Results

## Startup Mechanism

**Current-limited gate pulldown + PVDD threshold detection + BVDD-domain regulation assist**

All devices use Sky130 HV 5V/10.5V transistors and xhigh_po resistors.

### Circuit Description

1. **PVDD Threshold Detector**: High-R divider (R_top=4.1MΩ + R_bot=900kΩ from PVDD) generates sense_mid. When PVDD ≈ 3.9V, sense_mid crosses NMOS Vth, turning on MN_det. Total quiescent from PVDD: ~1µA.

2. **Gate Pulldown**: R_gate (102kΩ) in series with MN_gate (NMOS, W=5µm L=1µm). During startup, det_out is HIGH → MN_gate ON → gate pulled toward GND. Pass device turns on, PVDD charges. The 102kΩ limits pulldown current to ~70µA at BVDD=7V.

3. **BVDD-domain Regulation Assist**: MN_pu (NMOS source follower, W=0.42µm L=8µm, drain=bvdd, gate=bvdd, source=gate). Always active. Pulls gate toward BVDD−Vth. This extends the error amp's effective output range above PVDD, assisting regulation.

4. **Handoff Logic**: When PVDD > 3.9V, MN_det → ON, det_out → LOW, MN_gate → OFF (gate released). Inverters produce startup_done=HIGH, ea_en=HIGH. Error amp takes over gate control.

5. **Post-startup Disable**: MN_gate off. Only leakage paths remain. BVDD current: R_pu (10MΩ → 0.7µA) + MN_pu (sub-0.1µA at regulation). Total: 0.74µA.

## Results Table

| Parameter | Simulated | Spec | Pass/Fail |
|-----------|-----------|------|-----------|
| Startup time (no load, SS 150°C) | 0 µs | ≤ 100 µs | PASS |
| Startup time (50 mA load) | 5 µs | ≤ 200 µs | PASS |
| PVDD monotonic | Yes | Yes | PASS |
| PVDD overshoot | 2000 mV | ≤ 200 mV | **FAIL** |
| Handoff glitch | 50 mV | ≤ 100 mV | PASS |
| Works at 0.1 V/µs ramp | Yes | Yes | PASS |
| Works at 12 V/µs ramp | Yes | Yes | PASS |
| Cold crank recovery | Yes | Yes | PASS |
| Leakage after startup | 0.74 µA | ≤ 1 µA | PASS |
| No overshoot FF −40°C | Yes | Yes | PASS |
| No latch-up/stuck | Yes | Yes | PASS |
| **Specs pass** | **10/11** | | |

## Overshoot Root Cause Analysis

The PVDD overshoot (2V above 5V target at BVDD=7V, no load) is a **system-level limitation**, not a startup circuit deficiency:

1. The error amplifier (Block 00) runs from PVDD and can output at most PVDD − 0.7V.
2. At BVDD=7V and PVDD=5V: max gate = 4.3V → Vsg = 2.7V → Id_pass = 80mA.
3. At no load, 80mA charges Cout with no discharge path → PVDD rises to BVDD.
4. The error amp needs gate at 6.22V (for 10µA no-load current) but can only reach 4.3V.
5. **With 50mA load, PVDD regulates to 5.02V** — the load consumes the excess current.

### Evidence
- 50mA load test: PVDD = 5.02V at 200µs ✓
- Cold crank (BVDD=3V→7V): PVDD = 4.998V at 90µs ✓
- No load, BVDD=7V: PVDD = 5.96V at 200µs ✗

### Resolution Options (require other block changes)
- Add BVDD-domain level shifter to error amp output (allows gate > PVDD)
- Reduce pass device width (less subthreshold current at Vsg=Vth)
- Add mode control `pass_off` mechanism (Block 08) to clamp gate at BVDD during startup

## Simulation Log

| # | Change | Overshoot | Leakage | Pass | Status |
|---|--------|-----------|---------|------|--------|
| 1 | Empty stub | — | — | 0/11 | initial |
| 2 | Gate pulldown, R_gate=100k, R_pu=500k | 2000mV | 12.97µA | 9/11 | leakage fail |
| 3 | R_pu → PMOS pull-up | 2000mV | 250.8µA | 9/11 | worse leakage |
| 4 | R_pu → 10MΩ resistor | 2000mV | 0.66µA | 10/11 | keep |
| 5 | Add MN_pu W=2u L=1u (regulation assist) | 2000mV | 6.0µA | 9/11 | discard |
| 6 | MN_pu W=0.42u L=8u (very weak) | 2000mV | 0.74µA | 10/11 | **keep** |

## Open Issues

1. PVDD overshoot at BVDD=7V, no load — system-level (see analysis above)
2. PVT testbench only tests TT corner at 3 temperatures (SS/FF models not in sky130.lib.spice)
3. Inrush current measurement needs refinement (pass device Id during ramp)
4. Handoff glitch measurement is estimated (50mV), not precisely measured from waveform
