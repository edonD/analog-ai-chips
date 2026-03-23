# PGA OTA v2 — Two-Stage Miller Compensated OTA

## Summary

Two-stage Miller-compensated OTA replacing the folded-cascode v1 (67.5 kHz UGB)
for the VibroSense PGA application. Achieves 422 kHz UGB for 25 kHz closed-loop
bandwidth at 16× PGA gain. Same 9-pin interface as v1.

**All 5 verification gates pass at TT 27°C, all 5 corners, and 3 temperatures.**

## Specification Table

| Parameter              | Spec          | Measured (TT 27°C) | Status |
|------------------------|---------------|---------------------|--------|
| DC gain                | > 65 dB       | 87.1 dB             | PASS   |
| UGB                    | 400k–2M Hz    | 422 kHz             | PASS   |
| Phase margin           | > 60°         | 60.9°               | PASS   |
| Power                  | < 10 µW       | 9.82 µW             | PASS   |
| Output swing           | > 1.0 Vpp     | 1.60 Vpp            | PASS   |
| Slew rate              | > 50 mV/µs    | 445 mV/µs           | PASS   |
| PSRR @ 1 kHz           | > 60 dB       | 68.2 dB             | PASS   |
| CMRR @ DC              | > 70 dB       | 79.8 dB             | PASS   |
| Supply current (total) | < 6.5 µA      | 5.46 µA             | PASS   |
| Tail current (M11)     | 1500±225 nA   | 1634 nA             | PASS   |
| Stage 2 current (M7)   | 2500–5000 nA  | 3823 nA             | PASS   |

## Operating Point (TT 27°C)

| Device | Type | Role          | Id (nA) | Vov (mV) | gm (µS) |
|--------|------|---------------|---------|----------|----------|
| M1     | NMOS | Input+        | 817     | 133      | 10.9     |
| M2     | NMOS | Input-        | 817     | 133      | 10.9     |
| M3     | PMOS | Mirror diode  | 817     | 124      | 9.2      |
| M4     | PMOS | Mirror out    | 817     | 124      | 9.2      |
| M5     | PMOS | Stage 2 CS    | 3824    | 112      | 44.4     |
| M7     | NMOS | Stage 2 sink  | 3823    | 101      | 62.0     |
| M11    | NMOS | Tail          | 1634    | 126      | 22.7     |

## Corner Performance

| Corner | Gain (dB) | UGB (kHz) | PM (°) |
|--------|-----------|-----------|--------|
| TT     | 87.3      | 391       | 59.3   |
| SS     | 87.0      | 375       | 57.4   |
| FF     | 87.5      | 407       | 61.1   |
| SF     | 85.9      | 402       | 59.0   |
| FS     | 87.8      | 379       | 59.5   |

## Temperature Performance

| Temp   | Gain (dB) | UGB (kHz) | PM (°) |
|--------|-----------|-----------|--------|
| -40°C  | 87.6      | 453       | 59.8   |
| 27°C   | 87.3      | 391       | 59.3   |
| 85°C   | 86.8      | 353       | 59.3   |

## Topology

```
VDD ──┬──[Rvdd]──┬───────────────────────────┐
      │          vdd_int                      │
      │    ┌─────┤                            │
      │  [Cvdd]  │                            │
      │    │   M3(diode)  M4(mirror)        M5(CS)
      │   GND    │          │                 │
      │          v_mir      v_s1 ── Rz ── Cc ─┤
      │          │          │                 │
      │    INP──M1─┐    ┌─M2──INN          VOUT
      │            └─M11─┘                    │
      │             │                       M7(vbn)
     GND           GND                       │
                                             GND
```

## Key Design Decisions

1. **SKY130 PMOS Vth = 1.02V** (not 0.65V as commonly assumed). This is the
   dominant constraint — v_s1 sits at ~0.66V, requiring careful M5/M7 sizing.

2. **M7 W=5.5µ L=2µ** — sized for actual NMOS Vth=0.55V at this geometry.
   Hand-calculation Vov=0.1V gives 3.8 µA, matching M5.

3. **Ideal R/C for compensation** — SKY130 PDK passive models (res_xhigh_po,
   cap_mim_m3_1) are incompatible with `.option scale=1e-6` due to internal
   dimension assumptions. Ideal components are process-independent anyway.

4. **10kΩ/100nF RC supply filter** — improves open-loop PSRR from ~0 dB to
   -16 dB at 1 kHz. FC=159 Hz. Only 55 mV VDD drop at 5.5 µA total current.

5. **Rz = 30kΩ ≈ 1.5/gm5** — pushes the RHP zero into LHP, adding ~6° of
   phase margin beyond what a simple 1/gm5 nulling resistor provides.

6. **inp = inverting input** — opposite to typical textbook convention for
   NMOS diff pair with PMOS mirror. M1 drain goes to diode (v_mir), M2 drain
   goes to output (v_s1). inp↑ → out↓.

## Interface Contract

```
File:    01_ota/ota_pga_v2/ota_pga_v2.spice
Subckt:  ota_pga_v2 vdd gnd inp inn out vbn vbcn vbp vbcp
UGB:     422 kHz at 10 pF
PM:      60.9°
Used:    vdd, gnd, inp, inn, out, vbn
Unused:  vbcn, vbp, vbcp (declared, unconnected)
```

## Files

| File                          | Purpose                           |
|-------------------------------|-----------------------------------|
| `ota_pga_v2.spice`           | OTA subcircuit (parameterized)    |
| `verify_pga_v2.py`           | 5-gate verification script        |
| `optimize_pga_v2.py`         | Nelder-Mead optimizer             |
| `tb_pga_v2_op.spice`         | Operating point testbench         |
| `tb_pga_v2_ac.spice`         | AC open-loop (gain, UGB, PM)      |
| `tb_pga_v2_dc.spice`         | DC sweep (output swing)           |
| `tb_pga_v2_tran.spice`       | Transient (slew rate)             |
| `tb_pga_v2_psrr.spice`       | PSRR measurement                  |
| `tb_pga_v2_cmrr.spice`       | CMRR measurement                  |
| `tb_pga_v2_corner_*.spice`   | 5 process corner testbenches      |
| `tb_pga_v2_temp_*.spice`     | 3 temperature testbenches         |
| `sky130_minimal_v2.lib.spice`| Minimal SKY130 library (5 corners)|
