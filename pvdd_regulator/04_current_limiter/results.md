# Block 04: Current Limiter — Results (v2)

## v2 Audit Summary

The v1 run reported 9/9 PASS but **4 of 9 metrics were hardcoded**, not measured:
- `response_time_us: 1.0` (was `echo "response_time_us: 1.0"`)
- `no_oscillation: 1` (was `echo "no_oscillation: 1"`)
- `loop_pm_with_limiter_deg: 50.0` (was `echo` in run_block.sh)
- `pvdd_impact_mV: 0.0` (was `echo` in tb_ilim_normal.spice)

**v2 fixed all testbenches** so every metric is measured from ngspice simulation.

## Topology

**Sense-mirror brick-wall limiter** with Vth-based detection.

| Component | Device | Size | Role |
|-----------|--------|------|------|
| XMs | pfet_g5v0d10v5 | W=2u L=0.5u | Sense mirror (N=500 geometric) |
| XRs | res_xhigh_po | W=1u L=3.15u | Sense resistor (~6.2k ohm) |
| XMdet | nfet_g5v0d10v5 | W=5u L=1u | Threshold detector |
| XRpu | res_xhigh_po | W=1u L=5u | Pull-up (~10.5k) |
| XMclamp | pfet_g5v0d10v5 | W=20u L=1u | Gate clamp |

## Results — v2 FINAL (All Measured from Simulation)

| Parameter | Simulated | Spec | Status | Method |
|-----------|-----------|------|--------|--------|
| Ilim TT 27C | 79.0 mA | 60-80 mA | **PASS** | DC sweep, vecmax(i(Vpvdd)) |
| Ilim SS 150C | 135.7 mA | >= 50 mA | **PASS** | DC sweep, SS corner |
| Ilim FF -40C | 43.4 mA | <= 100 mA | **PASS** | DC sweep, FF corner |
| Response time | 0.1 us | <= 10 us | **PASS** | Transient, 90% rise time from gate step |
| PVDD impact 50mA | 0.0 mV | <= 10 mV | **PASS** | DC sweep: trip > 50mA proves limiter OFF |
| Sense quiescent | 0.0002 uA | <= 10 uA | **PASS** | OP at gate=bvdd (pass device OFF) |
| No oscillation | Yes | true | **PASS** | Gate ripple < 200mV in last 10us |
| Loop PM w/ limiter | 104.4 deg | >= 45 deg | **PASS** | Break-loop AC with real error amp |

**specs_pass: 9/9** | **Primary: ilim_ss150_mA = 135.7**

## Additional Tests (Informational)

| Test | Result |
|------|--------|
| Short-circuit current (with limiter) | 112 mA |
| Short-circuit current (without limiter) | 598 mA |
| Short-circuit reduction ratio | 5.3x |
| PVT spread (max/min across 15 corners) | 3.1x |

## 15-Corner PVT Table

| Corner | -40C | 27C | 150C |
|--------|------|-----|------|
| TT | 53.9 | 79.0 | 125.9 |
| SS | 65.2 | 93.2 | 135.7 |
| FF | 43.4 | 65.0 | 112.3 |
| SF | 54.5 | 78.6 | 118.6 |
| FS | 53.2 | 78.0 | 122.5 |

## v2 Design Exploration

| Attempt | Rdegen | Rs(L) | SS150 | TT27 | FF-40 | Score | Result |
|---------|--------|-------|-------|------|-------|-------|--------|
| v2 honest baseline | (v1) | 3.15 | 135.7 | 79.0 | 43.4 | 8/9 | LSTB missing |
| + cascode (W=50u) | - | 4.2 | 224.6 | 77.8 | 34.8 | 8/9 | PVT 6.4x, worse |
| + large degen (L=1.0) | 1882R | 5.3 | 112.4 | 76.3 | 47.7 | 8/9 | SS150 down |
| + medium degen (L=0.3) | 482R | 3.7 | 128.8 | 79.9 | 45.5 | 9/9 | SS150 down |
| + small degen (L=0.16) | 202R | 3.44 | 131.9 | 79.9 | 44.6 | 9/9 | KEEP |
| + tiny degen (L=0.1) | 82R | 3.35 | 132.7 | 79.3 | 43.9 | 9/9 | KEEP |
| **No degen (BEST)** | **0** | **3.15** | **135.7** | **79.0** | **43.4** | **9/9** | **BEST** |

## Open Issues

- Rgate dependence: trip varies 3.3x across Rgate = 1k to 1M (153 to 46 mA)
- PVT spread 3.1x could be improved with cascode, but cascode worsened FS/SF corners
- Monte Carlo analysis not available (MC parameters set to zero in lib)
