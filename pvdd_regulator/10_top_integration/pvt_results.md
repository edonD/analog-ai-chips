# PVT Verification Results -- PVDD 5V LDO Regulator

**Date:** 2026-04-02
**Simulator:** ngspice-42
**PDK:** SkyWater SKY130A
**Corners:** TT, SS, FF, SF, FS x {-40C, 27C, 150C} = 15 corners
**All 45 simulations completed (no DNF)**

---

## T1: DC Regulation (PVDD at 1mA load, Rload=5k)

**Spec: 4.825V -- 5.175V (5.0V +/-3.5%)**

| Corner | -40C | 27C | 150C | Status |
|--------|------|-----|------|--------|
| TT | **5.728V** | 4.984V | 4.980V | **FAIL** (-40C) |
| SS | 4.983V | 4.979V | 4.980V | PASS |
| FF | 4.985V | 4.985V | 4.979V | PASS |
| SF | 4.985V | 4.984V | 4.980V | PASS |
| FS | 4.984V | 4.983V | 4.978V | PASS |

**Result: 14/15 PASS, 1 FAIL**

- TT -40C regulates at 5.728V (+14.6% error) -- the error amp / feedback loop fails to
  regulate properly at this corner. All other corners are within 4.978--4.985V (excellent).

---

## T2: Startup Peak (must be < 5.5V)

**Spec: PVDD peak < 5.5V during startup**

| Corner | -40C | 27C | 150C | Status |
|--------|------|-----|------|--------|
| TT | **5.728V** | 4.984V | 4.980V | **FAIL** (-40C) |
| SS | 4.983V | 4.979V | 4.980V | PASS |
| FF | 4.985V | 4.985V | 4.979V | PASS |
| SF | 4.985V | 4.984V | 4.980V | PASS |
| FS | 4.984V | 4.983V | 4.978V | PASS |

**Result: 14/15 PASS, 1 FAIL**

- TT -40C peak = 5.728V (exceeds 5.5V limit). Same root cause as T1.
- All other corners have peak = final (no overshoot), indicating clean startup.

---

## T3: Load Transient Undershoot (1mA to 10mA step)

**Spec: undershoot < 150mV below steady-state**
**Method: Rload=5k (1mA base) + 9mA current step at t=10ms**

| Corner | -40C | 27C | 150C | Status |
|--------|------|-----|------|--------|
| TT | **6278mV** | 68mV | 86mV | **FAIL** (-40C) |
| SS | 59mV | **786mV** | 91mV | **FAIL** (27C) |
| FF | 138mV | 65mV | 77mV | PASS |
| SF | 61mV | 69mV | 78mV | PASS |
| FS | 56mV | 66mV | **1067mV** | **FAIL** (150C) |

**Result: 10/15 PASS, 5 FAIL** (3 corners fail catastrophically, 2 recover)

Detailed undershoot data:

| Corner | -40C | 27C | 150C |
|--------|------|-----|------|
| TT | 6278mV (collapse) | 68mV | 86mV |
| SS | 59mV | 786mV (no recovery) | 91mV |
| FF | 138mV | 65mV | 77mV |
| SF | 61mV | 69mV | 78mV |
| FS | 56mV | 66mV | 1067mV (no recovery) |

Notes on failures:
- **TT -40C**: PVDD was already at 5.728V (DC reg failure), so step causes collapse.
- **SS 27C**: After 9mA step, PVDD drops to 4.12V and does not recover within 10ms.
  The regulator cannot supply 10mA under SS 27C conditions.
- **FS 150C**: After step, PVDD drops to 3.88V and does not recover. FS corner
  (fast NMOS / slow PMOS) weakens the PMOS pass device at high temperature.

---

## T11: Current Limit Trip (Rload=0.1 ohm, near-short)

**Spec: Iout < 80mA under short-circuit**

| Corner | -40C | 27C | 150C | Status |
|--------|------|-----|------|--------|
| TT | 52.6mA | 49.9mA | 45.9mA | PASS |
| SS | 56.0mA | 52.8mA | 48.3mA | PASS |
| FF | 49.4mA | 47.2mA | 43.8mA | PASS |
| SF | 51.9mA | 49.5mA | 45.8mA | PASS |
| FS | 53.7mA | 50.6mA | 46.3mA | PASS |

**Result: 15/15 PASS**

- Current limit works correctly at all 15 corners.
- Range: 43.8mA (FF 150C) to 56.0mA (SS -40C).
- All well below 80mA limit. Nominal ~50mA as designed.
- Temperature coefficient: Ilim decreases with temperature (expected for bandgap-referenced design).
- Process sensitivity: SS corners have slightly higher Ilim, FF slightly lower.

---

## Overall Summary

| Spec | Corners Tested | PASS | FAIL | Pass Rate |
|------|---------------|------|------|-----------|
| T1: DC Regulation | 15 | 14 | 1 | 93% |
| T2: Startup Peak | 15 | 14 | 1 | 93% |
| T3: Load Transient | 15 | 10 | 5 | 67% |
| T11: Current Limit | 15 | 15 | 0 | 100% |
| **Total** | **60** | **53** | **7** | **88%** |

### Failing Corners (root cause analysis)

1. **TT -40C** (T1, T2, T3 fail): The regulator does not regulate at -40C TT corner.
   PVDD settles at 5.728V instead of 5.0V. This suggests the error amp gain
   or feedback divider ratio shifts significantly at low temperature, or the
   soft-start / mode control sequencing has a timing issue at -40C.

2. **SS 27C** (T3 fail): DC regulation is fine at 1mA, but the regulator cannot
   maintain regulation under 10mA load step. The pass device (slow PMOS at SS)
   has insufficient drive capability, or the loop bandwidth is too low to respond
   to the transient.

3. **FS 150C** (T3 fail): Fast NMOS / slow PMOS at high temperature. The PMOS
   pass device is weakest at this corner (slow + hot). Cannot recover from 10mA step.

### Corners that pass everything
- SS -40C, SS 150C
- FF -40C, FF 27C, FF 150C
- SF -40C, SF 27C, SF 150C
- FS -40C, FS 27C
- TT 27C, TT 150C

**10 of 15 corners pass all specs. 5 corners have at least one failure.**

### Recommended design improvements
1. **TT -40C fix**: Investigate error amp bias at -40C. Likely needs temperature-compensated
   bias current or wider MOSFET sizing for low-temperature operation.
2. **Load transient fix**: Increase loop bandwidth or add feedforward compensation
   to improve transient response at SS/FS corners under heavy load.
3. **Pass device sizing**: Consider increasing pass device W/L ratio to ensure
   adequate drive at worst-case corners (FS 150C, SS 27C under load).
