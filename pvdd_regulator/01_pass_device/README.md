# Block 01: Pass Device

## Summary

HV PMOS pass device for PVDD 5V LDO Regulator using SkyWater SKY130A PDK.

**Device:** `sky130_fd_pr__pfet_g5v0d10v5` (10.5V rated HV PMOS)

| Parameter | Value |
|-----------|-------|
| W per instance | 100 um |
| L | 0.5 um |
| Instances | 10 parallel |
| Total W | 1.0 mm |
| Id @ TT 27C, Vds=400mV | 84.2 mA |
| Id @ SS 150C, Vds=400mV | 56.8 mA |
| Rds_on | 4.75 ohm |
| Cgs | 1.04 pF |
| Leakage (off) | 0.02 uA |

**Specs: 7/7 PASS**

## Plots

### Id vs Vds Family Curves
![Id vs Vds](idvds_family.png)

### Id vs Vgs at Dropout
![Id vs Vgs](idvgs_dropout.png)

### Gate Capacitance
![Cgs](cgs_vs_vgs.png)

### Transconductance
![gm](gm_vs_id.png)

### Safe Operating Area
![SOA](soa_overlay.png)

## Design Notes

- The HV PMOS `pfet_g5v0d10v5` has model bins covering L=0.5um and W up to 100um.
- Using W=100um per instance with 10 parallel instances gives 1mm total width.
- At TT 27C with Vds=-0.4V and full gate drive (Vgs=-5.4V), the device delivers 84.2mA.
- At worst case SS 150C, it delivers 56.8mA, 13.6% above the 50mA specification.
- Total width of 1mm is very compact compared to the 20mm maximum.
- Cgs of 1.04pF is low, which is favorable for error amplifier loading.
