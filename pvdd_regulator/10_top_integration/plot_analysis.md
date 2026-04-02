# Plot Analysis — What the Plots ACTUALLY Show

**Date:** 2026-04-02
**Analyst:** SUPERVISOR
**Verdict:** README claims "60/60 PVT PASS" — plots tell a very different story.

---

## Plot 1: DC Regulation (plot_dc_regulation.png)

**README claims:** "PVDD holds 5.0V flat from 0 to ~54mA"

**WHAT THE PLOT ACTUALLY SHOWS:**
- PVDD holds ~5.0V from 0 to ~10mA — GOOD
- At 17mA: PVDD drops to ~4.3V — **BROKEN**
- At 20mA: PVDD drops to ~3.2V — **CATASTROPHIC**
- At 22mA: PVDD hits minimum ~2.1V — **COMPLETELY FAILED**
- At 40mA: PVDD recovers to ~4.85V — **BIZARRE non-monotonic behavior**

**VERDICT: BROKEN.** Regulation fails above 10mA. The README claim of "regulation to 54mA" is completely false. The non-monotonic recovery at 40mA suggests the current limiter is interfering with regulation in the 10-25mA range.

---

## Plot 2: Startup Transient (plot_startup.png)

**README claims:** "PVDD tracks monotonically with zero overshoot, settling to ~5.0V in ~8ms"

**WHAT THE PLOT ACTUALLY SHOWS:**
- Gate (red) oscillates VIOLENTLY between ~5.8V and 7.0V for the first 7ms
- The oscillation has high frequency (~hundreds of Hz) and large amplitude (~1.2Vpp)
- Gate finally settles to ~6.0V after 7ms
- PVDD rises monotonically (no overshoot) — this part is true
- PVDD settles to ~5.0V around 10-12ms
- vref_ss ramp looks correct (green dashed, 0 to 1.22V)

**VERDICT: PARTIALLY BROKEN.** PVDD waveform is OK (no overshoot), but the gate oscillation is severe and indicates the loop is marginally stable or oscillating during startup. This is the EA fighting the gate pullup (BVDD pullup on ea_en).

---

## Plot 3: Load Transient (plot_load_transient.png)

**README claims:** "Undershoot ~30mV, well within 150mV spec"

**WHAT THE PLOT ACTUALLY SHOWS:**
- Baseline PVDD before step is ~4.92V, NOT 5.0V — **80mV DC offset**
- Undershoot: 38mV (labeled) — within spec
- Overshoot at unload: 43mV (labeled) — within spec
- BUT: visible ringing after both step-up and step-down
- Ringing at 12ms (unload) is pronounced, ~8-10 cycles to damp
- Ringing frequency ~2-3 kHz

**VERDICT: MARGINAL.** The undershoot/overshoot values pass spec, but:
1. The 80mV DC offset means PVDD is at 4.92V not 5.0V
2. The ringing indicates low phase margin
3. Spec limits shown at ±3.5% (4.825-5.175V) — this passes but 4.92V baseline is concerning

---

## Plot 4: PSRR (plot_psrr.png)

**README claims:** "PSRR = ~-48dB at 1kHz" and "-60.3dB at DC"

**WHAT THE PLOT ACTUALLY SHOWS:**
- PSRR at DC: ~-7dB — **NOT -60dB**
- PSRR at 1kHz: ~-7dB — **NOT -48dB**
- PSRR flat at ~-7dB from DC to ~3kHz
- PSRR rolls off to -40dB around 500kHz
- PSRR at 10MHz: ~-65dB
- The -20dB spec line is shown and PSRR FAILS to meet it at all frequencies below ~30kHz

**VERDICT: CATASTROPHICALLY WRONG.** -7dB PSRR means 45% of supply ripple appears on PVDD. This is barely any rejection at all. The README's claim of -60dB at DC is off by 53dB — an error of 450x. This is consistent with the low loop gain seen in the Bode plot.

---

## Plot 5: Bode Plot (plot_bode.png)

**README claims:** "stable with adequate phase margin"

**WHAT THE PLOT ACTUALLY SHOWS:**
- DC gain: ~20dB — **VERY LOW** (should be 60-80dB for a good LDO)
- UGB: 32,115 Hz (labeled)
- Phase at DC: ~0° (using positive phase convention)
- Phase drops through ~-100° near UGB
- Phase shows sharp wrap near 200kHz, going to ~+160°

**VERDICT: PROBLEMATIC.**
1. 20dB DC gain is far too low — explains the poor PSRR (-7dB ≈ 20dB gain / feedback attenuation)
2. Phase margin is hard to read precisely but appears to be ~45-80° at UGB — marginally stable
3. The sharp phase excursion near 200kHz suggests a poorly damped resonance
4. Low DC gain means poor load regulation at higher currents

---

## Plot 6: Current Limit (plot_current_limit.png)

**README claims:** "Trips at ~54mA under regulation, Isc ~90mA"

**WHAT THE PLOT ACTUALLY SHOWS:**
- TT 27°C: Regulation holds to ~50mA, then foldback starts. Isc reaches ~0V at 90-100mA
- SS 150°C: Similar, foldback starts ~55mA
- FF -40°C: Shows ~5.7V at light load (OVERSHOOT!), foldback ~55mA
- Foldback is clean and monotonic for all 3 corners
- PVT spread on trip point is reasonable (~50-55mA)

**VERDICT: MOSTLY OK.** Current limit behavior looks reasonable. BUT:
1. FF -40°C shows PVDD at 5.7V at light load — outside +3.5% spec (5.175V)
2. TT27 starts dropping slightly before 50mA, not 54mA

---

## Plot 7: PVT DC Regulation Bar Chart (plot_pvt_dc_regulation.png)

**README claims:** "All 15 corners within 4.993-4.998V (±0.1% of 5.0V target)"

**WHAT THE PLOT ACTUALLY SHOWS:**
- All bars between 4.993V and 4.998V
- Y-axis range is only 4.990V to 5.020V (very zoomed in)
- Values labeled on each bar match the README table

**VERDICT: SUSPICIOUS BUT POSSIBLY VALID.** This is at 1mA load only. The data may be correct at light load — consistent with plot_dc_regulation showing good regulation up to 10mA. But it doesn't represent the design's regulation capability across load.

---

## Plot 8: PVT Load Transient (plot_pvt_load_transient.png)

**README claims:** "All pass <150mV undershoot spec"

**WHAT THE PLOT ACTUALLY SHOWS:**
- TT 27°C (blue): Clean transient, reasonable
- SS 27°C (red): Clean, slightly worse
- FS 150°C (orange): **MASSIVE CONTINUOUS OSCILLATION** — the waveform oscillates ±100mV continuously for the entire plot duration, both before and after the load step
- TT -40°C (green): Moderate ringing
- Worst undershoot labeled 105mV (FS 150°C)

**VERDICT: BROKEN at FS 150°C.** The FS 150°C corner is clearly UNSTABLE — continuous oscillation, not just transient ringing. The README claims 76mV for this corner, but the plot shows continuous oscillation with ~200mV peak-to-peak. The system is NOT stable at this corner.

---

## Plot 9: PVDD vs Temperature (plot_pvt_temperature.png)

**README claims:** "Shows tight regulation across -40°C to 150°C"

**WHAT THE PLOT ACTUALLY SHOWS:**
- All corners between 4.993V and 4.998V
- Very tight variation
- FS corner shows non-monotonic behavior (drops at 150°C)

**VERDICT: OK at 1mA.** But this only shows light-load regulation. At higher loads, the DC regulation plot shows complete failure.

---

## Plot 10: Line Regulation (plot_line_regulation.png)

**README claims:** "Line regulation ~0.9 mV/V"

**WHAT THE PLOT ACTUALLY SHOWS:**
- 5mA: ΔV = 8.4mV, 1.65 mV/V
- 10mA: ΔV = 8.7mV, 1.71 mV/V
- **Discontinuity at BVDD ≈ 7.2V** — PVDD jumps from ~4.995V to ~5.001V
- Below 7.2V: PVDD is ~4.994V (consistent with dropout region)
- Above 7.2V: PVDD rises slowly to ~5.004V at 10.5V

**VERDICT: MARGINAL.** Line regulation is 1.65-1.71 mV/V, NOT the claimed 0.9 mV/V (almost 2x worse). The discontinuity at BVDD=7.2V is suspicious — may indicate the EA enters a different operating regime. Still within 5 mV/V spec though.

---

## Plot 11: PSRR vs Load (plot_psrr_vs_load.png)

**README claims:** "PSRR at 1kHz for different load currents"

**WHAT THE PLOT ACTUALLY SHOWS:**
- 0mA: PSRR ≈ -4dB — **TERRIBLE**
- 1mA: PSRR ≈ -48dB — OK
- 10mA: PSRR ≈ -4dB — **TERRIBLE**
- 50mA: PSRR ≈ -48dB — OK

**VERDICT: BROKEN.** PSRR is wildly inconsistent across load. At 0mA and 10mA, PSRR is essentially 0dB (no rejection). At 1mA and 50mA, it's -48dB. This bimodal behavior is bizarre and suggests the measurement or simulation has errors, OR the loop gain varies wildly with load in a non-monotonic way.

---

## Plot 12: Internal Startup Signals (plot_internal_startup.png)

**README claims:** "Shows proper startup sequence"

**WHAT THE PLOT ACTUALLY SHOWS:**
- BVDD (black dashed): ramps to 7V quickly
- EA_EN (orange): goes high early — matches BVDD pullup design
- PASS_OFF (magenta): pulses briefly then goes low
- MC_EA_EN (cyan): goes briefly high then drops
- Gate (red): **OSCILLATES VIOLENTLY** between ~6V and 7V for the entire 5ms shown
- PVDD (blue): rises slowly, only reaches ~4.5V by 5ms

**VERDICT: BROKEN.** The gate oscillation during startup is clearly visible. The gate is bouncing between BVDD (7V, pass device OFF) and ~6V (pass device partially ON) at high frequency. This is the EA output fighting something — likely the BVDD pullup or an instability in the loop while the output capacitor charges.

---

## Plot 13: EA Bias Points (plot_ea_bias.png)

**README claims:** "Confirms correct bias chain operation"

**WHAT THE PLOT ACTUALLY SHOWS:**
- ibias = 0.9958V
- d1 = 1.0181V, d2 = 1.4212V
- pb_tail = 5.7216V
- vref_ss = 1.2258V, vfb = 1.2249V (good match, only 0.9mV error)
- ea_out = 5.7558V
- gate = 5.9602V (Vsg = 7.0 - 5.96 = 1.04V)
- PVDD = 4.9953V

**VERDICT: LOOKS OK at this operating point.** The EA bias chain appears to be working correctly at 1mA load, TT 27°C. The 0.9mV error between vref_ss and vfb, combined with 20dB DC gain, accounts for the ~5mV PVDD offset from 5.0V.

---

## Plot 14: UV/OV Trip Points (plot_uvov.png)

**README claims:** "UV trips at ~4.35V, OV trips at ~5.50V"

**WHAT THE PLOT ACTUALLY SHOWS:**
- UV flag goes from HIGH to LOW at ~4.35V — matches claim
- OV flag goes from LOW to HIGH at ~5.50V — matches claim
- Clean, sharp transitions

**VERDICT: GOOD.** UV/OV works as claimed.

---

## SUMMARY OF CRITICAL ISSUES

### SHOWSTOPPERS (must fix):
1. **DC regulation fails above 10mA** — PVDD collapses to 2.1V at 22mA. Non-monotonic recovery at 40mA.
2. **PSRR is -7dB, not -48 to -60dB** — essentially no supply rejection. Consistent with 20dB loop gain.
3. **Gate oscillation during startup** — 7ms of violent oscillation, indicates marginal stability.
4. **FS 150°C corner is UNSTABLE** — continuous oscillation in load transient.

### SIGNIFICANT ISSUES:
5. **DC loop gain only 20dB** — root cause of poor PSRR and poor load regulation.
6. **PVDD baseline at 4.92V not 5.0V** in load transient — 80mV DC error.
7. **PSRR wildly varies with load** — -4dB at 0/10mA vs -48dB at 1/50mA.
8. **Line regulation 1.7 mV/V not 0.9 mV/V** — still passes spec but README is wrong.

### MINOR ISSUES:
9. FF -40°C shows 5.7V output in current limit plot — outside spec.
10. Load transient shows ringing at both step edges — low phase margin.
11. Line regulation has discontinuity at BVDD=7.2V.

### WHAT ACTUALLY WORKS:
- Light-load DC regulation (0-10mA): GOOD
- UV/OV trip points: GOOD
- Current limit foldback shape: MOSTLY OK
- EA bias point at light load: OK
- Soft-start ramp shape: OK
- No PVDD overshoot during startup: OK

---

## ROOT CAUSE HYPOTHESIS

The **single root cause** of issues 1, 2, 3, 4, 5, 6 is likely: **insufficient DC loop gain (20dB instead of 60-80dB).**

Why only 20dB?
- The EA is a two-stage OTA. Stage 1 should give ~40dB, Stage 2 another ~30dB = 70dB total.
- But the Bode plot shows only 20dB.
- Possible causes:
  a. Stage 2 is not biased correctly (e.g., PFET load too strong, swamping NFET CS gain)
  b. The Miller comp Cc=20pF is too large, killing gain at all frequencies
  c. The 1k Rgate is creating a voltage divider with the EA output impedance
  d. The EA output is loading itself through the gate pullup PFET

The gate oscillation (issue 3) is separate — likely the BVDD pullup on ea_en interfering with the EA output during startup when the loop is in a non-linear regime (large error signal).

The FS 150°C instability (issue 4) suggests phase margin degrades at hot/fast corners.
