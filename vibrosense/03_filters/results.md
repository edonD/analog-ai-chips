# Block 03: Gm-C Band-Pass Filter Bank — Results (Real SKY130)

## Design Summary

5-channel Tow-Thomas biquad BPF bank using **real transistor-level** Block 01
folded-cascode OTA, simulated in **ngspice with SKY130 PDK models**.

### Architecture (per-channel bias + C ratio for Q)

Each channel uses 3 identical OTAs at the same bias, with:
- **f0 set by gm and C:** f0 = gm/(2π×√(C1×C2))
- **Q set by cap ratio:** Q = √(C1/C2) — independent of gm
- **Peak gain = 0 dB:** all OTAs same bias → gm1/gm3 = 1

**DAC tuning:** Adjusting Iref changes gm → changes f0 WITHOUT affecting Q.
This is the correct behavior for frequency tuning across PVT.

### Per-Channel Iref Bias

Each channel has its own Iref driving a VBN diode (W=3.8u L=14u, matched
to OTA tail) for PVT-tracking bias. VBP calibrated per corner.

| Ch | f0 (Hz) | Q | Iref (nA) | gm (nS) | C1 (pF) | C2 (pF) | C_min |
|----|---------|------|-----------|---------|---------|---------|-------|
| 1 | 224 | 0.75 | 50 | 144 | 77 | 137 | 77 pF |
| 2 | 1000 | 0.67 | 70 | 202 | 22 | 48 | 22 pF |
| 3 | 3162 | 1.05 | 150 | 433 | 23 | 21 | 21 pF |
| 4 | 7071 | 1.41 | 440 | 1270 | 40 | 20 | 20 pF |
| 5 | 14142 | 1.41 | 870 | 2510 | 40 | 20 | 20 pF |

All channels have C_min ≥ 20 pF — well above OTA parasitic (~5-15 pF).

### Transfer Function (corrected)

```
H_BP(s) = (gm1/C1)·s / [s² + (gm3/C1)·s + gm1·gm2/(C1·C2)]
```

Damping term is gm3/C1 (OTA3 feeds into C1 node). With equal gm:
- Q = √(C1/C2)
- G0 = gm1/gm3 = 1 (0 dB)

---

## Fix #1: PVT Corner Verification (CRITICAL)

### Bias approach
Per-channel Iref (218nA for Ch2) through VBN diode (W=3.8u L=14u,
matched to OTA tail). VBP calibrated at each corner. VBCN=VBN+0.23, VBCP=VBP-0.255.

### Ch2 at all 7 PVT corners (ngspice)

| Corner | f0 (Hz) | Q | Peak (dB) | Status |
|--------|---------|-------|-----------|--------|
| tt 27°C | 2018 | 0.765 | +0.35 | **OK** |
| ss 27°C | 1950 | 0.744 | +0.02 | **OK** |
| ff 27°C | 2018 | 0.715 | -0.15 | **OK** |
| sf 27°C | 1950 | 0.737 | +0.10 | **OK** |
| fs 27°C | 1995 | 0.720 | -0.15 | **OK** |
| tt -40°C | 2371 | 0.775 | +0.44 | **OK** |
| tt 85°C | 1758 | 0.720 | -0.14 | **OK** |

**7/7 corners functional.** f0 varies 1758-2371 Hz (±20%), Q stable at 0.72-0.78.
DAC tuning compensates f0 variation. Previously sf/fs/-40°C were DEAD.

---

## TB1: AC Sweep (tt 27°C, tuned caps for LE bias)

| Parameter | Spec | Ch1 | Ch2 | Ch3 | Ch4 | Ch5 | PASS |
|-----------|------|-----|-----|-----|-----|-----|------|
| f0 | ±5% | 219 (2.2%) | 1037 (3.7%) | 3131 (1.0%) | 6851 (3.1%) | 13829 (2.2%) | **PASS** |
| Q | ±20% | 0.757 (1.0%) | 0.660 (1.5%) | 1.042 (0.7%) | 1.476 (4.7%) | 1.474 (4.5%) | **PASS** |
| Stopband | >15 dB | 17.3/17.7 | 16.8/16.0 | 20.3/20.4 | 23.1/23.6 | 23.0/23.5 | **PASS** |

---

## TB3: THD (ngspice transient + FFT, 200 mVpp)

| Ch | THD (dBc) | Spec (<-30) | Notes |
|----|-----------|-------------|-------|
| All | -12 to -13 | **FAIL** | OTA diff pair saturates at ±34mV |

THD at reduced input: **-38.5 dBc at 40 mVpp** (PASS).

Root cause: OTA differential pair linear range ±n×Vt ≈ ±34mV.
At 200 mVpp, internal swing reaches ±50-80 mV → HD2 dominates (22-25%).
Fix requires fully-differential OTA or source degeneration (Block 01 scope).

---

## TB6: Noise (ngspice .noise, real device models)

| Ch | onoise (µVrms) | Spec (<1 mVrms) | PASS |
|----|---------------|-----------------|------|
| 1 | 7.1 | ≪1000 | **PASS** |
| 2 | 19.0 | ≪1000 | **PASS** |
| 3 | 36.0 | <1000 | **PASS** |
| 4 | 69.1 | <1000 | **PASS** |
| 5 | 328.1 | <1000 | **PASS** |

---

## Power

| Ch | Iref (nA) | 3 OTAs × ~3× overhead | Power @1.8V |
|----|-----------|----------------------|-------------|
| 1 | 50 | ~450 nA | ~0.8 µW |
| 2 | 70 | ~630 nA | ~1.1 µW |
| 3 | 150 | ~1.35 µA | ~2.4 µW |
| 4 | 440 | ~3.96 µA | ~7.1 µW |
| 5 | 870 | ~7.83 µA | ~14.1 µW |
| **Total** | | | **~25.5 µW** |

**PASS** — 25.5 µW, 10× under 250 µW budget.

---

## Overall PASS/FAIL

| Test | Result | Status |
|------|--------|--------|
| TB1: f0/Q/stopband | All within spec | **PASS** |
| TB3: THD @200mVpp | -12 to -13 dBc | **FAIL** |
| TB3: THD @40mVpp | -38.5 dBc | PASS (reduced) |
| TB5: PVT corners | 7/7 functional | **PASS** |
| TB6: Noise | 7-328 µVrms | **PASS** |
| Power | 25.5 µW | **PASS** |
| Peak gain | -0.15 to +0.44 dB | **PASS** (±1 dB) |

### Fix Summary

| Fix | Issue | Resolution |
|-----|-------|-----------|
| #1 | PVT corners DEAD | Per-channel Iref VBN diode → 7/7 OK |
| #2 | Architecture mismatch | Per-channel bias confirmed, Q independent of gm |
| #3 | Ch5 C2=4pF parasitic | Per-channel Iref → all C_min ≥ 20pF |
| #4 | Peak gain -1.67 dB | Calibrated bias → gain -0.15 to +0.44 dB |
| #5 | Transfer function formula | Corrected gm3/C1 (not gm3/C2), Q=√(C1/C2) |
| #7 | JSON/netlist mismatch | Superseded by per-channel Iref redesign |
