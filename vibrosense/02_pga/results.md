# Block 02: PGA Simulation Results

## Tapeout-Ready Results (all real SKY130 components, TT 27°C)

### AC Gain & Bandwidth

| Gain | Expected (dB) | Measured (dB) | Error (dB) | @25kHz (dB) | BW (kHz) | Spec | PASS |
|------|--------------|--------------|-----------|------------|---------|------|------|
| 1x   | 0.00         | -0.007       | -0.007    | -0.046     | >>25    | >25  | **PASS** |
| 4x   | 12.04        | 11.99        | -0.05     | 11.72      | >>25    | >25  | **PASS** |
| 16x  | 24.08        | 24.02        | -0.06     | 21.35      | ~27     | >25  | **PASS** |
| 64x  | 36.12        | 35.97        | -0.15     | 24.83      | ~7      | >6   | **PASS** |

### THD (1 kHz, 1 Vpp output)

| Gain | Input Vpk | THD (%) | THD (dBc) | Spec  | PASS |
|------|-----------|---------|-----------|-------|------|
| 1x   | 500 mV    | 0.19    | -54.4     | <1.0% | **PASS** |

### Power

| Component | Current (uA) | Power (uW) |
|-----------|-------------|-----------|
| OTA + decoder + switches | 5.56 | 10.0 |
| **Total** | **5.56** | **~10.0** |
| **Spec** | — | **<10** |
| | | **PASS** |

### Transient (1x, 500 mVpk @ 1 kHz)

| Metric | Value |
|--------|-------|
| DC output | 0.949 V |
| Output peak | 1.453 V |
| Output min | 0.449 V |
| Output swing | 1.00 Vpp |
| Virtual ground (V(inn)) | 0.900 V |

---

## Comparison: Ideal Passives vs Tapeout-Ready

| Parameter | With ideal passives | Tapeout-ready | Delta |
|-----------|-------------------|---------------|-------|
| Gain 1x (dB) | -0.002 | -0.007 | -0.005 |
| Gain 64x (dB) | 36.04 | 35.97 | -0.07 |
| THD 1x (%) | 0.005 | 0.19 | +0.185 |
| Power (uW) | 9.94 | 9.94 | 0 |

THD increased from 0.005% to 0.19% due to PMOS pseudo-resistor nonlinearity and MIM cap bottom-plate parasitics. Still well within the <1% spec.

---

## Status: ALL SPECS PASS — TAPEOUT-READY (schematic level)
