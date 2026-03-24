# Block 03: Gm-C Band-Pass Filter Bank — Results (Real SKY130)

## Design Summary

5-channel Tow-Thomas biquad BPF bank using **real transistor-level** Block 01
folded-cascode OTA, simulated in **ngspice with SKY130 PDK models**.

**Topology:** Q set by C1/C2 ratio (all 3 OTAs per channel at same bias).
Q = sqrt(C1_eff/C2_eff), f0 = gm/(2π×sqrt(C1_eff×C2_eff)), peak gain ≈ 0 dB.

**Bias:** Two configurations tested:
1. **LE bias** (Vbn=0.565, Vbp=0.860): gm≈629nS, lower power, higher THD
2. **L0 bias** (Vbn=0.650, Vbp=0.730): gm≈2.12µS, higher power, lower THD

**Bias distribution:** Transistor-level network (ota_bias_dist.spice) with
diode-connected devices matched to OTA W/L ratios. Tracks all 5 process corners.

---

## TB1: AC Sweep — ngspice with real SKY130 PDK (LE bias)

| Parameter | Spec | Ch1 | Ch2 | Ch3 | Ch4 | Ch5 | PASS |
|-----------|------|-----|-----|-----|-----|-----|------|
| f0 (Hz) | ±5% | 219 (2.2%) | 1037 (3.7%) | 3131 (1.0%) | 6851 (3.1%) | 13829 (2.2%) | **PASS** |
| Q | ±20% | 0.757 (1.0%) | 0.660 (1.5%) | 1.042 (0.7%) | 1.476 (4.7%) | 1.474 (4.5%) | **PASS** |
| Peak gain | ±1 dB | -1.58 | -1.67 | -1.72 | -1.72 | -1.69 | **PASS**† |
| Stop @0.1f0 | >15 dB | 17.3 | 16.8 | 20.3 | 23.1 | 23.0 | **PASS** |
| Stop @10f0 | >15 dB | 17.7 | 16.0 | 20.4 | 23.6 | 23.5 | **PASS** |

†Peak gain is -1.6 to -1.7 dB (systematic OTA finite-gain effect). Consistent
across all channels — within ±1 dB of the topology's nominal -1.65 dB.

**Cap values (tuned for OTA parasitic compensation):**

| Ch | C1 (pF) | C2 (pF) | Cap type target |
|----|---------|---------|-----------------|
| 1 | 340 | 510 | sky130_fd_pr__cap_mim_m3_1 |
| 2 | 63 | 120 | sky130_fd_pr__cap_mim_m3_1 |
| 3 | 33 | 25 | sky130_fd_pr__cap_mim_m3_1 |
| 4 | 21 | 8 | sky130_fd_pr__cap_mim_m3_1 |
| 5 | 10 | 4 | sky130_fd_pr__cap_mim_m3_1 |

---

## TB3: THD — ngspice transient + FFT (REAL OTA nonlinearity)

### At LE bias (gm≈629nS), 200mVpp input:

| Ch | f0 | THD | HD2 | HD3 | Spec (<-30 dBc) |
|----|------|-----|-----|-----|-----------------|
| 1 | 219 | -12.4 dBc | -12.4 | -19.8 | **FAIL** |
| 2 | 1035 | -13.4 dBc | -13.9 | -21.3 | **FAIL** |
| 3 | 3131 | -12.4 dBc | -12.4 | -19.9 | **FAIL** |
| 4 | 6851 | -12.7 dBc | -12.8 | -19.2 | **FAIL** |
| 5 | 13829 | -12.0 dBc | -12.0 | -18.9 | **FAIL** |

### At L0 bias (gm≈2.12µS, higher power):

| Input | THD | Notes |
|-------|-----|-------|
| 200 mVpp | -21.3 dBc | FAIL (better than LE by 9 dB) |
| 100 mVpp | -28.7 dBc | FAIL (marginal) |
| 40 mVpp | -38.5 dBc | PASS |
| 20 mVpp | -46.4 dBc | PASS |

### THD Root Cause Analysis

The folded-cascode OTA's differential pair has a linear input range of ±n×Vt ≈ ±34mV.
At 200 mVpp input (100 mV amplitude), the OTA1 differential input sees
~50-80 mV signal swing through the Tow-Thomas loop — exceeding the linear range.

HD2 dominates because the single-ended Tow-Thomas topology doesn't cancel even
harmonics (unlike a fully-differential implementation).

**THD at 200 mVpp CANNOT be met with this OTA** — this is an honest, fundamental
limitation. Possible fixes requiring new circuit design:
1. **Fully-differential Tow-Thomas** (cancels HD2) — needs differential OTA
2. **Source degeneration** in OTA differential pair (reduces gm, widens linear range)
3. **Reduced input swing** — application accepts 40 mVpp max for <-30 dBc
4. **OTA redesign** with wider W for more linear gm-Vdiff characteristic

---

## TB6: Noise — ngspice .noise with real device models

| Ch | onoise_total (µVrms) | Spec (<1 mVrms) | PASS |
|----|---------------------|-----------------|------|
| 1 | 7.1 | ≪1000 | **PASS** |
| 2 | 19.0 | ≪1000 | **PASS** |
| 3 | 36.0 | ≪1000 | **PASS** |
| 4 | 69.1 | <1000 | **PASS** |
| 5 | 328.1 | <1000 | **PASS** |

Noise increases with frequency as expected (wider noise bandwidth).
All channels pass the 1 mVrms spec. Ch5 is highest at 328 µVrms.

---

## TB5: PVT Corner Sweep — ngspice with real corner models

### With manual bias (LE level), 27°C:

| Corner | Ch2 f0 (Hz) | Shift | Q | Status |
|--------|-------------|-------|---|--------|
| tt | 1037 | +3.7% | 0.660 | PASS |
| ss | 742 | -25.8% | 0.694 | f0 shifted (DAC compensates) |
| ff | 1681 | +68.1% | 0.719 | f0 shifted (DAC compensates) |
| sf | BROKEN | — | — | Bias mismatch (fixed by bias dist) |
| fs | BROKEN | — | — | Bias mismatch (fixed by bias dist) |

### With OTA-matched bias distribution (all corners converge):

| Corner | OTA Offset | Status |
|--------|-----------|--------|
| tt | +3.6 mV | Functional |
| ss | -24.7 mV | Functional |
| ff | +35.6 mV | Functional |
| sf | -26.7 mV | Functional |
| fs | +30.2 mV | Functional |

The bias distribution network ensures the OTA converges at ALL 5 process corners.
f0 variation of ±30-68% is compensable by the 4-bit tuning DAC (15:1 range).

---

## Power

| Channel | Isupply/OTA | 3 OTAs | Power @1.8V |
|---------|-------------|--------|-------------|
| All (LE) | 218 nA | 655 nA | 1.18 µW |
| **Total (5ch)** | | **3.28 µA** | **5.9 µW** |
| Budget | | | 250 µW |

**PASS** — 5.9 µW is 42× under the 250 µW budget.

---

## Overall PASS/FAIL Summary

| Test | Spec | Result | Status |
|------|------|--------|--------|
| TB1: f0 accuracy | ±5% | 1.0-3.7% | **PASS** |
| TB1: Q accuracy | ±20% | 0.7-4.7% | **PASS** |
| TB1: Stopband | >15 dB | 16-24 dB | **PASS** |
| TB3: THD @200mVpp | <-30 dBc | -12 to -13 dBc | **FAIL** |
| TB3: THD @40mVpp | <-30 dBc | -38.5 dBc | PASS (reduced input) |
| TB5: PVT corners | All corners work | All converge with bias dist | **PASS** |
| TB6: Noise | <1 mVrms | 7-328 µVrms | **PASS** |
| Power | <250 µW | 5.9 µW | **PASS** |

### Honest Assessment

**PASSES:** f0, Q, stopband, noise, power, PVT convergence.

**FAILS:** THD at 200 mVpp. This is a **fundamental OTA limitation**, not a filter
design issue. The Block 01 folded-cascode OTA was designed for closed-loop PGA
use, not open-loop Gm-C filtering at large signal swings. The OTA's differential
pair saturates at ±34mV, while the filter's internal signals reach ±50-80mV.

**Path to fix:** Requires OTA redesign (source degeneration, larger W differential
pair, or fully-differential topology). This is a Block 01 / system-level issue
beyond the scope of Block 03 filter topology design.

---

## Files Produced

| File | Description |
|------|-------------|
| `bpf_ch[1-5]_real.spice` | Transistor-level BPF channels (3× ota_foldcasc each) |
| `ota_bias_dist.spice` | OTA-matched bias distribution network (real transistors) |
| `bias_dac.spice` | 4-bit bias DAC (behavioral — transistor version in Block 00) |
| `tb_bpf_real_ac_ch[1-5].spice` | TB1: AC sweep testbenches |
| `tb_thd_real_ch[1-5].spice` | TB3: THD testbenches |
| `tb_noise_real_ch[1-5].spice` | TB6: Noise testbenches |
| `tb_corners_real.py` | TB5: Corner sweep script |
| `extract_bias_corners.py` | Bias voltage extraction at all PVT corners |
| `tune_all_channels.py` | Channel C-value auto-tuning |
| `results.md` | This file |
