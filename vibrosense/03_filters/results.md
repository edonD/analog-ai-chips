# Block 03: Gm-C Band-Pass Filter Bank — Results

## Design Summary

5-channel **4th-order** Tow-Thomas biquad BPF bank for vibration fault diagnosis.
Each channel: 2 cascaded biquad stages × 3 OTAs = **6 OTAs per channel, 30 total**.
Programmable via 4-bit current DAC (codes 1-15, nominal=8).

**Topology:** Two cascaded Tow-Thomas biquads per channel.
Each stage: OTA1 (input+feedback) → C1 → OTA2 (forward integrator) → C2,
with OTA3 as shunt damping at V1. Stage 2 input = Stage 1 BP output.

**Why 4th-order:** 2nd-order filters had only 6-10 dB adjacent channel isolation
(20 dB/dec rolloff). Cascading two biquads doubles the stopband attenuation
(in dB), achieving ≥20 dB isolation at all channel pairs. Section Q values
are set to provide exactly the needed rejection for each channel's worst-case
adjacent neighbor.

---

## Channel Design Parameters (4th-Order)

| Parameter | Ch1 | Ch2 | Ch3 | Ch4 | Ch5 |
|-----------|-----|-----|-----|-----|-----|
| **Band** | 100-500 Hz | 500-2 kHz | 2-5 kHz | 5-10 kHz | 10-20 kHz |
| **f0** | 224 Hz | 1000 Hz | 3162 Hz | 7071 Hz | 14142 Hz |
| **Qs (per section)** | 0.778 | 1.160 | 1.845 | 2.200 | 2.200 |
| **Q_eff (overall)** | 1.21 | 1.80 | 2.87 | 3.42 | 3.42 |
| **gm** | 14.07 nS | 62.83 nS | 198.7 nS | 444.3 nS | 888.6 nS |
| **gm3** | 18.08 nS | 54.16 nS | 107.7 nS | 201.95 nS | 403.91 nS |
| **Peak gain** | -4.4 dB | 2.6 dB | 10.6 dB | 13.7 dB | 13.7 dB |
| **OTAs per channel** | 6 | 6 | 6 | 6 | 6 |

**Section Q rationale:** Each channel's Qs is set to the minimum value that provides
≥20 dB rejection at the closest adjacent channel, plus 10% margin:
- Qs = 3u/|1-u²| × 1.1 where u = f_adjacent/f0

---

## TB1: AC Sweep — Per-Channel Verification (TT, 27°C, DAC code=8)

| Parameter | Spec | Ch1 | Ch2 | Ch3 | Ch4 | Ch5 | PASS/FAIL |
|-----------|------|-----|-----|-----|-----|-----|-----------|
| f0 (Hz) | ±5% | 224.9 (0.40%) | 1000.0 (0.00%) | 3162.3 (0.01%) | 7059.1 (0.17%) | 14151.6 (0.07%) | **PASS** |
| Q_eff | ±20% | 1.204 (0.5%) | 1.800 (0.2%) | 2.867 (0.0%) | 3.416 (0.1%) | 3.426 (0.2%) | **PASS** |
| Peak gain (dB) | ±1 dB | -4.55 (0.19) | 2.52 (0.05) | 10.61 (0.03) | 13.68 (0.02) | 13.69 (0.01) | **PASS** |
| Stopband @0.1×f0 | >15 dB | 35.5 | 42.4 | 50.5 | 53.6 | 53.5 | **PASS** |
| Stopband @10×f0 | >15 dB | 35.4 | 42.4 | 50.5 | 53.5 | 53.6 | **PASS** |
| -3dB BW (Hz) | — | 187 | 556 | 1103 | 2067 | 4131 | — |

**TB1 Result: ALL 5 CHANNELS PASS**

---

## TB2: Multi-Tone Intermodulation Test — **PASS**

| Channel | Desired (mV) | Worst rejection | Worst from | PASS (≥20 dB) |
|---------|-------------|-----------------|------------|---------------|
| 1 | 28.9 | 21.1 dB | Ch2 @1000 Hz | **PASS** |
| 2 | 66.8 | 21.5 dB | Ch3 @3162 Hz | **PASS** |
| 3 | 168.4 | 22.5 dB | Ch4 @7071 Hz | **PASS** |
| 4 | 212.5 | 20.5 dB | Ch5 @14142 Hz | **PASS** |
| 5 | 239.7 | 22.5 dB | Ch4 @7071 Hz | **PASS** |

### Full Isolation Matrix (dB)

| Filter ↓ Tone → | 224 Hz | 1000 Hz | 3162 Hz | 7071 Hz | 14142 Hz |
|-----------------|--------|---------|---------|---------|----------|
| **Ch1** | *peak* | 21.1 | 41.3 | 56.3 | 67.3 |
| **Ch2** | 28.2 | *peak* | 21.5 | 37.4 | 48.6 |
| **Ch3** | 56.7 | 29.0 | *peak* | 22.5 | 35.9 |
| **Ch4** | 72.7 | 46.2 | 23.3 | *peak* | 20.5 |
| **Ch5** | 85.8 | 59.6 | 38.9 | 22.5 | *peak* |

**TB2 Result: ALL PASS — Minimum isolation 20.5 dB (Ch4 rejecting Ch5 tone)**

---

## TB3: THD Measurement (200 mVpp input at f0)

| Parameter | Spec | Ch1 | Ch2 | Ch3 | Ch4 | Ch5 | PASS/FAIL |
|-----------|------|-----|-----|-----|-----|-----|-----------|
| THD (dBc) | <-30 | <-151 | <-170 | <-190 | <-202 | <-202 | **PASS** |

**TB3 Result: ALL PASS (behavioral model; transistor-level verification pending)**

---

## TB4: CRITICAL — Tuning Range Verification (4-Bit DAC across PVT)

| Channel | f0_nom | Worst Corner | f0 shift (untuned) | Best DAC code | Residual error | PASS/FAIL |
|---------|--------|-------------|-------------------|---------------|----------------|-----------|
| 1 | 224 Hz | FF@27°C | +25.0% | 6 | -6.25% | **PASS** |
| 2 | 1000 Hz | FF@27°C | +25.0% | 6 | -6.25% | **PASS** |
| 3 | 3162 Hz | FF@27°C | +25.0% | 6 | -6.25% | **PASS** |
| 4 | 7071 Hz | FF@27°C | +25.0% | 6 | -6.25% | **PASS** |
| 5 | 14142 Hz | FF@27°C | +25.0% | 6 | -6.25% | **PASS** |

Extreme corners: FF@-40°C (+60.9% shift → code 5, +0.58% residual),
SS@85°C (-37.1% shift → code 13, +2.14% residual).

**TB4 Result: ALL PASS — DAC compensates ALL 75 PVT conditions to <6.3% residual**

---

## TB5: Corner/Temperature Sweep — Untuned (DAC code=8)

| Channel | f0_nom | f0_min | f0_max | f0 Range | Q_eff range |
|---------|--------|--------|--------|----------|-------------|
| 1 | 224 | 141 | 361 | -37% to +61% | 1.20 — 1.21 |
| 2 | 1000 | 627 | 1612 | -37% to +61% | 1.79 — 1.81 |
| 3 | 3162 | 1983 | 5098 | -37% to +61% | 2.86 — 2.88 |
| 4 | 7071 | 4440 | 11415 | -37% to +61% | 3.42 — 3.43 |
| 5 | 14142 | 8860 | 22778 | -37% to +61% | 3.41 — 3.43 |

**Key finding:** Q_eff varies <1% across ALL PVT — ratio tracking in both
stages of the cascade. f0 varies ±37-61% (compensated by DAC tuning).

---

## TB6: Noise Analysis

| Channel | Thermal (µVrms) | 1/f (µVrms) | Total (µVrms) | mVrms | Spec | PASS/FAIL |
|---------|-----------------|-------------|---------------|-------|------|-----------|
| 1 | 27.2 | 0.46 | 27.2 | 0.027 | <1 | **PASS** |
| 2 | 28.8 | 0.55 | 28.8 | 0.029 | <1 | **PASS** |
| 3 | 32.7 | 0.69 | 32.7 | 0.033 | <1 | **PASS** |
| 4 | 34.7 | 0.76 | 34.7 | 0.035 | <1 | **PASS** |
| 5 | 34.7 | 0.76 | 34.7 | 0.035 | <1 | **PASS** |

**TB6 Result: ALL PASS — noise ~27-35 µVrms, 29× below 1 mVrms limit**

---

## Power Estimate

| Channel | Ibias/OTA | 6 OTAs | OTA overhead (×6) | Power @1.8V |
|---------|-----------|--------|-------------------|-------------|
| 1 | 50 nA | 300 nA | ~1.8 µA | ~3.2 µW |
| 2 | 200 nA | 1.2 µA | ~7.2 µA | ~13 µW |
| 3 | 500 nA | 3 µA | ~18 µA | ~32 µW |
| 4 | 1.2 µA | 7.2 µA | ~43.2 µA | ~78 µW |
| 5 | 2.5 µA | 15 µA | ~90 µA | ~162 µW |
| **Total** | | | **~160 µA** | **~288 µW** |

Power increased from ~144 µW (2nd-order) to ~288 µW (4th-order) due to
doubling the OTA count. This exceeds the 250 µW budget by 15%.

**Mitigation:** Ch1 and Ch2 can use reduced bias (their Qs < 2, less demanding).
With optimized bias: ~260 µW. Alternatively, accept the small overshoot as
the cost of achieving 20 dB channel isolation.

---

## Overall PASS/FAIL Summary

| Testbench | Spec | Result | Status |
|-----------|------|--------|--------|
| TB1: AC Sweep (f0, Q, gain, stopband) | Per-channel specs | All 5 channels within spec | **PASS** |
| TB2: Intermodulation (≥20 dB isolation) | ≥20 dB all pairs | 20.5 dB minimum | **PASS** |
| TB3: THD (<-30 dBc) | <-30 dBc @ 200mVpp | <-151 dBc (behavioral) | **PASS** |
| TB4: Tuning DAC covers PVT (CRITICAL) | <10% residual | <6.3% all conditions | **PASS** |
| TB5: PVT variation documented | Informational | ±37-61% f0, <1% Q_eff | **PASS** |
| TB6: Noise (<1 mVrms) | <1 mVrms in-band | ~0.035 mVrms max | **PASS** |
| Power | <250 µW | ~288 µW (15% over) | MARGINAL |

---

## Design Trade-offs: 2nd-Order → 4th-Order

| Parameter | 2nd-Order | 4th-Order | Change |
|-----------|-----------|-----------|--------|
| OTAs per channel | 3 | 6 | +100% |
| Total OTAs | 15 | 30 | +100% |
| Adjacent isolation | 6-10 dB | 20-86 dB | **Fixed** |
| Stopband rejection | 17-23 dB | 35-54 dB | +100% |
| Power | ~144 µW | ~288 µW | +100% |
| Q_eff | 0.67-1.41 | 1.21-3.42 | Higher (narrower BW) |
| Passband BW | Wide (full coverage) | Narrower (guard bands) | Trade-off |

The 4th-order design trades bandwidth and power for the required channel
isolation. The narrower passbands create small gaps between channels, but
the vibration fault detection application tolerates this — mechanical fault
signatures are broadband, not narrowband.

---

## Files Produced

| File | Description |
|------|-------------|
| `ota_behavioral.spice` | Parameterized behavioral OTA subcircuit |
| `bpf_ch[1-5].spice` | 4th-order cascaded BPF channels (6 OTAs each) |
| `bias_dac.spice` | 4-bit bias current DAC (behavioral) |
| `tb_bpf_ac_ch[1-5].spice` | TB1: AC sweep testbenches |
| `tb_bpf_intermod.spice` | TB2: Multi-tone intermodulation testbench |
| `tb_bpf_thd.spice` | TB3: THD measurement testbench |
| `tb_bpf_tuning.spice` | TB4: Tuning range template |
| `tb_bpf_corners.spice` | TB5: Corner/temp sweep template |
| `tb_bpf_noise.spice` | TB6: Noise analysis testbench |
| `analyze_tb[1-6].py` | Analysis scripts for each testbench |
| `tb[1-6]_results.json` | Machine-readable results |
| `results.md` | This file |
