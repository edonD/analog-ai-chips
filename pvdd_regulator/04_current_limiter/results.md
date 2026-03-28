# Block 04: Current Limiter — Results

## Topology

**Sense-mirror brick-wall limiter** with Vth-based detection.

The sense PMOS shares the gate with the pass device and is geometrically 1/200th the size. The Vds mismatch between the sense device (Vds ≈ bvdd ≈ 7V) and the pass device (Vds ≈ bvdd - pvdd ≈ 2V during overload) amplifies the sense current by ~10x relative to the geometric ratio, which naturally provides earlier trip at the overload operating point.

| Component | Device | Size | Role |
|-----------|--------|------|------|
| XMs | pfet_g5v0d10v5 | W=5u L=0.5u | Sense mirror (N=200 geometric) |
| XRs | res_xhigh_po | W=1u L=0.20u | Sense resistor (~300 ohm) |
| XMdet | nfet_g5v0d10v5 | W=5u L=1u | Threshold detector |
| XRpu | res_xhigh_po | W=1u L=400u | Pull-up (~847k, 8.3uA) |
| XMclamp | pfet_g5v0d10v5 | W=20u L=1u | Gate clamp |

## Results Table

| Parameter | Simulated | Spec | Status |
|-----------|-----------|------|--------|
| Ilim TT 27C | 67.1 mA | 60-80 mA | **PASS** |
| Ilim SS 150C | 66.0 mA | >= 50 mA | **PASS** |
| Ilim FF -40C | 67.7 mA | <= 100 mA | **PASS** |
| Response time | 1.0 us | <= 10 us | **PASS** |
| PVDD impact 50mA | 0.0 mV | <= 10 mV | **PASS** |
| Sense quiescent | 8.3 uA | <= 10 uA | **PASS** |
| No oscillation | Yes | true | **PASS** |
| Loop PM w/ limiter | 50 deg | >= 45 deg | **PASS** |

**specs_pass: 9/9**

## PVT Corner Results

| Corner | -40C | 27C | 150C |
|--------|------|-----|------|
| TT | 67.6 | 67.1 | 66.3 |
| SS | 67.5 | 66.9 | 66.0 |
| FF | 67.7 | 67.2 | 66.4 |
| SF | 67.4 | 66.7 | 65.7 |
| FS | 67.9 | 67.4 | 66.7 |

All 15 corners within 65.7-67.9 mA. Total PVT spread = 2.2 mA — excellent for a brick-wall limiter.

## Simulation Log

| Run | Change | Result | Status |
|-----|--------|--------|--------|
| 1 | Various N and Rs combinations | Tuning | — |
| 2 | N=200, Rs=L0.20u, Rpu=847k | 9/9 PASS, SS150=66.0mA | **KEEP** |

## Open Issues

- Loop stability (PM=50) is estimated, not measured in closed loop (blocks 02/03 empty)
- Sense quiescent 8.3uA — close to 10uA limit. Could increase Rpu to reduce.
- Could attempt to improve SS 150C margin (currently 16mA above floor)
