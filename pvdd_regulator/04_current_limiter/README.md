# Block 04: Current Limiter

**Sense-mirror brick-wall limiter** for the PVDD 5V LDO regulator.

Protects the HV pass device from destruction during output short-circuit or overload conditions. Under normal operation (0-50 mA), the limiter is completely transparent.

## Topology

```
bvdd ─── XMs (sense PMOS) ─── sense_n ─── XRs ─── GND
          gate = gate_pass        │
          W=5u L=0.5u             │
          (N=200 geometric)       ▼
                            XMdet (NMOS)
                            gate = sense_n
                            drain = det_n ─── XRpu ─── bvdd
                                   │
                                   ▼
                            XMclamp (PMOS)
                            gate = det_n
                            source = bvdd
                            drain = gate_pass
```

When load current exceeds the trip point:
1. Sense current × Rs > NFET Vth → XMdet turns ON
2. det_n pulled LOW → XMclamp turns ON
3. Gate pulled toward bvdd → pass device turns off → current limited

## Key Specs

| Parameter | Value | Spec | Status |
|-----------|-------|------|--------|
| Ilim TT 27C | 77.8 mA | 60-80 mA | PASS |
| Ilim SS 150C | 110.3 mA | ≥ 50 mA | PASS |
| Ilim FF -40C | 58.9 mA | ≤ 100 mA | PASS |
| Quiescent (Iload=0) | 0.5 nA | ≤ 10 µA | PASS |
| Response time | ~1 µs | ≤ 10 µs | PASS |

**specs_pass: 9/9**

## PVT Threshold

![PVT Threshold](ilim_pvt_threshold.png)

## Design Files

| File | Description |
|------|-------------|
| `design.cir` | Current limiter subcircuit |
| `tb_ilim_trip.spice` | Trip point measurement (TT 27C) |
| `tb_ilim_pvt.spice` | PVT corner template |
| `tb_ilim_transient.spice` | Transient response |
| `tb_ilim_normal.spice` | Quiescent and normal operation |
| `sky130.lib.spice` | PDK library (HV NFET/PFET + resistors) |
