# OTA PGA v2 Redesign — Fixing Critical Issues

## Background

The current `ota_pga_v2.spice` is a two-stage Miller OTA (NMOS diff pair + PMOS CS) in SKY130.
It passes all 5 verification gates at the nominal TT/27C corner, but has serious issues
that would prevent tapeout. This program attacks each one.

## Issues to Fix (Priority Order)

### ISSUE 1: Corner/Temperature Verification is Fake

**Problem:** Gate 5 reports all corners (FF/FS/SF/SS/TT) and temperatures (-40/27/85C) as
"N/A" with status "OK". The gate passed because the simulations didn't crash, not because
gain, UGB, and phase margin were actually extracted and checked at each corner.

**Required fix:**
- Fix `verify_pga_v2.py` so Gate 5 actually extracts DC gain, UGB, and phase margin from
  each corner and temperature simulation
- Report real numbers in the verification table
- ALL corners and temps must meet: gain > 60 dB, UGB > 300 kHz, PM > 55 deg
- If any corner fails, resize devices until all corners pass

### ISSUE 2: Phase Margin Has Zero Headroom

**Problem:** PM = 60.9 deg vs 60 deg minimum. This WILL fail at SS or 85C corners.

**Required fix:**
- Target PM >= 65 deg at nominal (TT/27C) to give ~5 deg margin for PVT
- Increase Cc slightly (try 4-5 pF) and/or adjust Rz to push the RHP zero further left
- Verify PM stays above 55 deg at ALL corners and temperatures
- Do NOT sacrifice UGB below 350 kHz to get PM — find the right Cc/Rz tradeoff

### ISSUE 3: M11 Tail Source Has Marginal Vds (193 mV)

**Problem:** M11 Vds = 193 mV with Vov = 125.5 mV, so Vds - Vov = only 68 mV of
saturation margin. gds = 433 nS (highest in the circuit). This hurts CMRR and will
push M11 out of saturation at SS/hot corners.

**Required fix:**
- Increase L11 (currently 14u, try 16-20u) to reduce Vov at same current
- Or reduce W11 to increase Vov ratio while keeping current — need to check both
- Target Vds - Vov > 100 mV at nominal
- Monitor tail current stays at ~1.5 uA after resizing

### ISSUE 4: M5 Stage-2 PMOS Has Minimum Length (L=1)

**Problem:** L5 = 1u gives high gds = 111.7 nS. This limits DC gain and makes the
design sensitive to process variation. Stage 2 gain = gm5/gds_out where
gds_out = gds5 + gds7 = 111.7 + 306.8 = 418.5 nS, giving only 40.4 dB from stage 2.

**Required fix:**
- Increase L5 to at least 2u (match L3/L7 style)
- This will reduce gds5 significantly, boosting DC gain by several dB
- Adjust W5 to maintain the same gm5 (~44 uS) at the new length
- Verify total gain improves and PM is not degraded

### ISSUE 5: Power Budget is 2x Original Target

**Problem:** Original spec was <5 uW. Current design is 9.82 uW. The specs.json was
relaxed to <10 uW to pass.

**Required fix:**
- After fixing issues 1-4, attempt to reduce power:
  - Reduce stage 2 current (currently 3.8 uA) — try 2.5-3 uA if UGB can be maintained
    by adjusting Cc downward proportionally
  - The stage 1 tail at 1.6 uA is already reasonable
- Target: <8 uW total. If <5 uW is impossible with the two-stage topology at 400 kHz UGB,
  document why and set a realistic target
- Do NOT sacrifice PM or UGB to save power — those are higher priority

### ISSUE 6: Specs Were Loosened to Fit the Design

**Problem:** Multiple specs were relaxed from the original program.md targets:
- PSRR: 60 dB -> 50 dB
- Input noise: 300 -> 400 nV/rtHz
- Power: 8 -> 10 uW

**Required fix:**
- After addressing issues 1-5, re-evaluate against the ORIGINAL specs from program.md
- Update specs_pga_v2.json to reflect achievable but honest targets
- For any spec that genuinely cannot be met, document the physics reason (not just "it's hard")
- PSRR of 60 dB should be achievable now that the PSRR testbench is fixed

## Design Flow

1. First fix the verification script (Issue 1) so you have real corner data
2. Run verification with the CURRENT netlist to see where it actually fails
3. Fix M5 length (Issue 4) — this is a free gain improvement
4. Fix M11 headroom (Issue 3) — this improves robustness
5. Tune Cc/Rz for PM (Issue 2) — must be done after device resizing
6. Attempt power reduction (Issue 5)
7. Final full verification against original specs (Issue 6)
8. Iterate until all corners pass

## Success Criteria

ALL of these must be met at ALL corners (FF/FS/SF/SS/TT) and temperatures (-40/27/85C):

| Parameter | Target |
|-----------|--------|
| DC Gain | > 60 dB |
| UGB | > 300 kHz |
| Phase Margin | > 55 deg |
| CMRR @ DC | > 70 dB |
| PSRR @ 1 kHz | > 50 dB |
| Output Swing | > 1.0 Vpp |
| Slew Rate | > 50 mV/us |
| Power | < 8 uW |

Nominal (TT/27C) targets should be tighter:

| Parameter | Nominal Target |
|-----------|---------------|
| DC Gain | > 80 dB |
| UGB | > 400 kHz |
| Phase Margin | > 65 deg |
| PSRR @ 1 kHz | > 60 dB |
| Power | < 8 uW |

## Constraints

- Stay on SKY130 1.8V nfet_01v8 / pfet_01v8 devices
- Keep the same 9-pin subckt interface (vdd gnd inp inn out vbn vbcn vbp vbcp)
- Keep two-stage Miller topology — do not switch to folded cascode or three-stage
- Use ngspice for all simulations
- All device sizes in microns with `.option scale=1e-6`
