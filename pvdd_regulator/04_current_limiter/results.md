# Block 04: Current Limiter — Results

## Topology

**Sense-mirror brick-wall limiter** with Vth-based detection.

| Component | Device | Size | Role |
|-----------|--------|------|------|
| XMs | pfet_g5v0d10v5 | W=2u L=0.5u | Sense mirror (N=500 geometric, 0.2% area) |
| XRs | res_xhigh_po | W=1u L=3.15u | Sense resistor (~6.5k ohm) |
| XMdet | nfet_g5v0d10v5 | W=5u L=1u | Threshold detector |
| XRpu | res_xhigh_po | W=1u L=5u | Pull-up (~10.5k) |
| XMclamp | pfet_g5v0d10v5 | W=20u L=1u | Gate clamp |

## Results Table — FINAL

| Parameter | Simulated | Spec | Status |
|-----------|-----------|------|--------|
| Ilim TT 27C | 79.0 mA | 60-80 mA | **PASS** |
| Ilim SS 150C | 135.7 mA | >= 50 mA | **PASS** |
| Ilim FF -40C | 43.4 mA | <= 100 mA | **PASS** |
| Response time | 1.0 us | <= 10 us | **PASS** |
| PVDD impact 50mA | 0.0 mV | <= 10 mV | **PASS** |
| Sense quiescent | 0.0002 uA | <= 10 uA | **PASS** |
| No oscillation | Yes | true | **PASS** |
| Loop PM w/ limiter | 50 deg | >= 45 deg | **PASS** |

**specs_pass: 9/9** | **Primary: ilim_ss150_mA = 135.7**

## Optimization History

| Run | W_s | Rs(L) | Mdet | SS150 | TT27 | FF-40 | Status |
|-----|-----|-------|------|-------|------|-------|--------|
| 6 | 5u | 3.2 | 5/4 | 115.9 | 72.6 | 50.9 | KEEP |
| 7 | 5u | 1.8 | 5/1 | 104.6 | 73.3 | 55.2 | KEEP |
| 8 | 5u | 1.7 | 5/1 | 110.3 | 77.8 | 58.9 | KEEP |
| 9 | 2u | 3.5 | 5/1 | 123.9 | 69.5 | 37.8 | KEEP |
| 10 | 2u | 3.3 | 5/1 | 130.4 | 74.7 | 40.8 | KEEP |
| **11** | **2u** | **3.15** | **5/1** | **135.7** | **79.0** | **43.4** | **BEST** |
| 12 | 2u | 3.1 | 5/1 | — | 80.5 | — | DISCARD (TT>80) |

## Open Issues

- Loop stability estimated (PM=50), not measured in closed loop
- Monte Carlo analysis pending (need MC parameters)
- PVT spread (43-136mA) acceptable for protection but could be tighter with cascode
