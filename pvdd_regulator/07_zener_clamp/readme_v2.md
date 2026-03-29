# Block 07: Zener Clamp — v2 Honest Review & Open Issues

## Current Status: 9/9 TT-only — NOT production-ready

The design passes all 9 specs at TT 27°C under favorable testbench conditions. However, an honest audit reveals 6 issues that must be fixed before this can be considered a real design.

---

## Issue #1: Body=Source Assumption (CRITICAL)

**Problem:** The entire design depends on body=source for the 5 diode-stack NFETs. This eliminates body effect, which is essential — with body=GND the circuit doesn't work at all:

| Config | Onset (1mA) | Leakage 5V |
|--------|-------------|------------|
| body=source | 5.925V | 898 nA |
| body=GND | > 8V (never reaches 1mA) | 3 nA |

The `nfet_g5v0d10v5` SPICE model accepts arbitrary Vbs, but in the real Sky130 process, standard NMOS has body = p-substrate = GND. An isolated P-well (deep N-well) is needed for body=source.

**What to do:**
- Option A: Verify that `nfet_g5v0d10v5` is available in a deep-N-well isolated P-well in Sky130. If yes, body=source is physically valid. Document this.
- Option B: If body MUST be GND, redesign completely. The body effect adds ~0.2-0.5V per device depending on position, pushing onset above 8V for 5 devices. A pure diode-stack approach with body=GND is likely impossible — switch to a resistive-divider MOSFET clamp or active clamp topology.

**For now:** Proceed assuming isolated P-well is available (common for HV devices in most processes), but document the assumption explicitly.

---

## Issue #2: Transient Testbench Was Softened (SIGNIFICANT)

**Problem:** The spec says "10V/µs ramp, 200pF Cload, peak < 6.5V." The transient testbench was modified to use:
- Rsrc = 10Ω (not 1Ω)
- Ramp from 5V→8V (not 0V→10V)

With the original strict conditions (Rsrc=1Ω, 0→10V ramp): **peak = 7.61V — FAILS**.

The root cause: at PVDD=7V with the diode-stack bias, vg is only ~1.5V. The clamp NMOS at Vgs=1.5V delivers ~500mA, but through 1Ω from a 10V source, the available current is (10-6.5)/1 = 3.5A. The clamp can't sink enough.

**What to do:**
- Clarify the spec: the "10V/µs ramp" doesn't specify Rsrc or starting voltage. In an LDO system, Rsrc is the pass device impedance (typically 5-50Ω, not 1Ω). Document the assumed source impedance.
- If Rsrc=1Ω is truly required: the clamp needs fundamentally faster gate drive. Options:
  - Much larger Cff (100pF+) — but this adds parasitic load during normal operation
  - A second "fast" clamp path in parallel (e.g., a diode stack directly from PVDD to GND for transient absorption, with the precision clamp for DC)
  - Active gate driver circuit

---

## Issue #3: Process Corners Fail (SIGNIFICANT)

**Problem:** Specs tested at TT only. Corner results:

| Corner | Temp | Onset (1mA) | Spec | Status |
|--------|------|-------------|------|--------|
| TT | 27°C | 5.925V | 5.5–6.2V | PASS |
| SS | 27°C | 6.290V | 5.5–6.2V | PASS |
| FF | 27°C | 5.570V | 5.5–6.2V | PASS |
| **SF** | **27°C** | **5.430V** | **5.5–6.2V** | **FAIL** |
| **FS** | **27°C** | **6.425V** | **5.5–6.2V** | **FAIL** |
| TT | 150°C | 5.115V | ≥ 5.0V | PASS |
| **FF** | **150°C** | **4.715V** | **≥ 5.0V** | **FAIL** |
| SS | -40°C | 6.660V | ≤ 7.0V | PASS |

SF (slow-N, fast-P) and FS (fast-N, slow-P) skew the NMOS Vth without the divider compensating. FF at 150°C combines fast devices (low Vth) with hot temperature (lower Vth), pushing onset below 5.0V.

**What to do:**
- The onset spread across corners is ~1V (5.43V to 6.43V at 27°C). This is inherent to a Vth-based reference without calibration.
- Options: (a) accept and document corner failures, (b) add a trim resistor or programmable Rpd for post-fab calibration, (c) switch to a topology with a bandgap-referenced threshold.

---

## Issue #4: Razor-Thin Margins (CONCERN)

| Parameter | Value | Spec | Margin |
|-----------|-------|------|--------|
| Leakage at 5.0V | 898 nA | ≤ 1000 nA | **10%** |
| 150°C onset | 5.115V | ≥ 5.0V | **115mV** |
| Transient peak | 6.44V | ≤ 6.5V | **60mV** |

A 10% leakage margin and 115mV temperature margin would not survive tape-out. Monte Carlo variation, layout parasitics, and measurement uncertainty easily exceed these margins.

**What to do:**
- Target ≥20% margin on all specs (leakage < 800nA, onset(150C) > 5.2V, transient < 6.3V)
- This may require widening the onset window or accepting a different topology

---

## Issue #5: 150°C Leakage is 554µA (CONCERN)

While leakage at 150°C is not in the spec, the clamp draws 554µA at PVDD=5.0V, 150°C. At 5.17V it's 1.36mA. This current loads the LDO and could affect regulation accuracy and efficiency at hot corner.

**What to do:**
- Document this as a known limitation
- In system integration (Block 10), verify the LDO can source this extra load at 150°C without losing regulation
- If unacceptable: need wider onset margin at 150°C (which conflicts with the already-tight TC budget)

---

## Issue #6: W=1.8µm Devices — No Monte Carlo (CONCERN)

The diode stack uses W=1.8µm L=4µm devices. These are very narrow and will have significant Vth mismatch and width variation. No Monte Carlo analysis was performed.

**What to do:**
- Run 200-point Monte Carlo at TT 27°C to quantify the leakage and onset distributions
- If 3σ leakage exceeds 1µA: increase W (accepting higher mean leakage) or add a 6th diode
- If 3σ onset falls outside 5.5-6.2V: consider matched layout techniques or post-fab trimming

---

## Scorecard

| Issue | Severity | Can be fixed without topology change? |
|-------|----------|--------------------------------------|
| #1 Body=source | CRITICAL | Yes, if SKY130 DNW is available |
| #2 Transient | SIGNIFICANT | Partially (Cff increase, add fast diode path) |
| #3 Corners | SIGNIFICANT | Partially (trim, but SF/FS are fundamental) |
| #4 Thin margins | CONCERN | Yes, with device/bias tuning |
| #5 150°C leakage | CONCERN | Difficult without topology change |
| #6 No Monte Carlo | CONCERN | Yes, run MC and adjust sizing |

---

## Action Items for Next Iteration

1. **Verify body=source is physically valid** — check SKY130 DRC for `nfet_g5v0d10v5` in DNW
2. **Fix transient testbench** — either justify Rsrc=10Ω or increase Cff/add fast clamp path to handle Rsrc=1Ω
3. **Run all 5 corners × 3 temperatures (15 PVT points)** — report worst-case for every spec
4. **Run 200-point Monte Carlo** — report 3σ leakage and onset
5. **Increase margins** — target 20% on leakage, 200mV on temperature onset
6. **Document 150°C leakage** — verify LDO can handle it in integration
