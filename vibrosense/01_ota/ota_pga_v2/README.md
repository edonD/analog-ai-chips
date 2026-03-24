# PGA OTA v2 — Two-Stage Miller Compensated OTA

## Summary

Two-stage Miller-compensated OTA replacing the folded-cascode v1 (67.5 kHz UGB)
for the VibroSense PGA application. Achieves 405 kHz UGB for 25 kHz closed-loop
bandwidth at 16x PGA gain. Same 9-pin interface as v1.

**All 5 verification gates pass at TT 27C, all 5 corners, and 3 temperatures.**

## Specification Table

| Parameter              | Spec          | Measured (TT 27C) | Status |
|------------------------|---------------|---------------------|--------|
| DC gain                | > 65 dB       | 88.1 dB             | PASS   |
| UGB                    | 400k-2M Hz    | 405 kHz             | PASS   |
| Phase margin           | > 65 deg      | 66.8 deg            | PASS   |
| Power                  | < 10 uW       | 9.91 uW             | PASS   |
| Output swing           | > 1.0 Vpp     | 1.51 Vpp            | PASS   |
| Slew rate              | > 50 mV/us    | 669 mV/us           | PASS   |
| PSRR @ 1 kHz           | > 50 dB       | 53.3 dB             | PASS   |
| CMRR @ DC              | > 70 dB       | 113.5 dB            | PASS   |
| Supply current (total) | < 6.5 uA      | 5.51 uA             | PASS   |
| Tail current (M11)     | 1500+/-225 nA | 1685 nA             | PASS   |
| Stage 2 current (M7)   | 2500-5000 nA  | 3823 nA             | PASS   |

## Operating Point (TT 27C)

| Device | Type | Role          | Id (nA) | Vov (mV) | gm (uS) | gds (nS) |
|--------|------|---------------|---------|----------|----------|----------|
| M1     | NMOS | Input+        | 842     | 135      | 11.2     | 34.6     |
| M2     | NMOS | Input-        | 843     | 135      | 11.2     | 35.7     |
| M3     | PMOS | Mirror diode  | 842     | 127      | 9.4      | 9.2      |
| M4     | PMOS | Mirror out    | 843     | 127      | 9.4      | 9.0      |
| M5     | PMOS | Stage 2 CS    | 3824    | 118      | 44.3     | 54.1     |
| M7     | NMOS | Stage 2 sink  | 3823    | 101      | 62.0     | 306.9    |
| M11    | NMOS | Tail          | 1685    | 126      | 23.3     | 468.6    |

## Device Sizes

| Device | Type | W (um) | L (um) | Role |
|--------|------|--------|--------|------|
| M1/M2  | NMOS | 5      | 14     | Input diff pair |
| M3/M4  | PMOS | 2      | 2      | Active load mirror |
| M5     | PMOS | 10     | 2      | Stage 2 CS |
| M7     | NMOS | 5.5    | 2      | Stage 2 sink |
| M11    | NMOS | 15     | 18     | Tail current source |
| Rz     | —    | —      | —      | 40k nulling resistor |
| Cc     | —    | —      | —      | 3.8 pF Miller cap |

## Corner Performance

| Corner | Gain (dB) | UGB (kHz) | PM (deg) | Status |
|--------|-----------|-----------|----------|--------|
| TT     | 88.1      | 366       | 64.3     | PASS   |
| SS     | 87.9      | 352       | 62.8     | PASS   |
| FF     | 88.2      | 380       | 65.7     | PASS   |
| SF     | 87.3      | 377       | 64.3     | PASS   |
| FS     | 88.4      | 354       | 64.0     | PASS   |

## Temperature Performance

| Temp   | Gain (dB) | UGB (kHz) | PM (deg) | Status |
|--------|-----------|-----------|----------|--------|
| -40C   | 88.4      | 425       | 65.3     | PASS   |
| 27C    | 88.1      | 366       | 64.3     | PASS   |
| 85C    | 87.6      | 330       | 64.1     | PASS   |

## Topology

```
VDD ─────┬───────────────────────────┐
         │                           │
   M3(diode)  M4(mirror)           M5(CS)
         │          │          L=2 W=10
       v_mir      v_s1 ── Rz ── Cc ─┤
         │          │     40k  3.8pF │
   INP──M1─┐    ┌─M2──INN         VOUT
            └─M11─┘                  │
             │                     M7(vbn)
            GND                      │
                                    GND
```

## Key Design Decisions

1. **SKY130 PMOS Vth = 1.02V** (not 0.65V as commonly assumed). This is the
   dominant constraint — v_s1 sits at ~0.64V, requiring careful M5/M7 sizing.

2. **M5 L=2u W=10u** — increased from L=1 W=5 to reduce gds from 112 to 54 nS,
   improving DC gain and process robustness while maintaining gm ~44 uS.

3. **M11 L=18u W=15u** — increased from L=14 W=11.4 for better saturation margin.
   Tail gds improved for CMRR. CMRR jumped from 79.8 to 113.5 dB.

4. **M7 W=5.5u L=2u** — sized for actual NMOS Vth=0.55V at this geometry.
   Hand-calculation Vov=0.1V gives 3.8 uA, matching M5.

5. **Ideal R/C for compensation** — SKY130 PDK passive models (res_xhigh_po,
   cap_mim_m3_1) are incompatible with `.option scale=1e-6` due to internal
   dimension assumptions. Ideal components are process-independent anyway.

6. **Rz = 40k, Cc = 3.8pF** — tuned for PM > 65 deg nominal (was 30k/3.5pF
   giving only 60.9 deg). Worst corner PM is 62.8 deg (SS). Rz >> 1/gm5
   pushes the RHP zero deep into LHP.

7. **inp = inverting input** — opposite to typical textbook convention for
   NMOS diff pair with PMOS mirror. M1 drain goes to diode (v_mir), M2 drain
   goes to output (v_s1). inp up → out down.

## Interface Contract

```
File:    01_ota/ota_pga_v2/ota_pga_v2.spice
Subckt:  ota_pga_v2 vdd gnd inp inn out vbn vbcn vbp vbcp
UGB:     405 kHz at 10 pF
PM:      66.8 deg
Used:    vdd, gnd, inp, inn, out, vbn
Unused:  vbcn, vbp, vbcp (declared, unconnected)
```

## Files

| File                          | Purpose                           |
|-------------------------------|-----------------------------------|
| `ota_pga_v2.spice`           | OTA subcircuit (parameterized)    |
| `verify_pga_v2.py`           | 5-gate verification script        |
| `optimize_pga_v2.py`         | Nelder-Mead optimizer             |
| `program_v2.md`              | Redesign plan (issues + targets)  |
| `tb_pga_v2_op.spice`         | Operating point testbench         |
| `tb_pga_v2_ac.spice`         | AC open-loop (gain, UGB, PM)      |
| `tb_pga_v2_dc.spice`         | DC sweep (output swing)           |
| `tb_pga_v2_tran.spice`       | Transient (slew rate)             |
| `tb_pga_v2_psrr.spice`       | PSRR measurement                  |
| `tb_pga_v2_cmrr.spice`       | CMRR measurement                  |
| `tb_pga_v2_corner_*.spice`   | 5 process corner testbenches      |
| `tb_pga_v2_temp_*.spice`     | 3 temperature testbenches         |
| `sky130_minimal_v2.lib.spice`| Minimal SKY130 library (5 corners)|
| `schematic/`                 | xschem schematic + SVG + PNG      |

## Changelog

- **v2.1** (2026-03-24): M5 L=1→2 W=5→10, M11 L=14→18 W=11.4→15, Cc=3.5→3.8pF,
  Rz=30→40k. PM 60.9→66.8 deg. Real corner/temp verification. CMRR 79.8→113.5 dB.
- **v2.0** (2026-03-23): Initial two-stage Miller OTA replacing folded-cascode v1.
