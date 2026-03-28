# Block 00: Error Amplifier — Design Program v2 (Corrected)

---

## 0. What Went Wrong in v1 and What This Program Fixes

The v1 optimization loop maximized phase margin as its primary metric with no upper bound. This led to an **unrealizable design** with Cc = 1.3 nF and PM = 157.5 degrees. The specific problems:

| Issue | v1 State | v2 Correction |
|-------|----------|---------------|
| Cc = 1.3 nF (650k um^2 die area) | Unrealizable on-chip | Hard cap: Cc <= 50 pF |
| PM = 157.5 deg (over-damped) | Gain crosses 0 dB at -3 dB/dec | Target PM = 60-75 deg with -20 dB/dec crossing |
| PVT only tests TT corner | 3 of 15 required corners tested | All 15 PVT corners (5 process x 3 temp) |
| Noise plot is fabricated | ngspice .noise crashed, fake curve plotted | Fix .noise testbench, report real data |
| Saturation check is fake | Only checks d2 node range | Check Vds > Vdsat for every device |
| PM extraction fails in PVT | Hardcoded 157.5 in all corners | Fix PVT PM extraction, report real numbers |
| GBW only 209 kHz | Barely meets 200 kHz minimum | Target GBW = 1-3 MHz for useful loop bandwidth |
| Primary metric = max(PM) | Drives optimizer into overcompensation | Primary metric = GBW, with PM in [60, 80] band |

**The circuit topology and device sizing are sound.** The two-stage Miller OTA with PMOS input pair is the right choice. The problem is purely in the compensation network (Cc, Rc) and the optimization objective.

---

## 1. Setup

### Purpose

The error amplifier compares V_FB (~1.226V) to V_REF (1.226V bandgap) and drives the gate of the HV PMOS pass device. Its DC gain sets regulation accuracy. Its bandwidth, combined with the pass device and compensation network, determines loop stability and transient response.

### Starting Point

You are NOT starting from scratch. The existing `design.cir` has a working two-stage Miller OTA:
- **Stage 1:** PMOS diff pair (XM1/XM2, W=50 L=4 m=2) + NMOS mirror load (XMn_l/XMn_r, W=20 L=8 m=2)
- **Stage 2:** NMOS CS amp (XMcs, W=20 L=1 m=1) + PMOS load (XMp_ld, W=20 L=4 m=8)
- **Bias:** 1 uA external -> 20x NMOS mirror -> PMOS mirror -> tail/loads
- **Compensation:** Cc + Rc between vout_gate and d2 (WRONG VALUES — must be re-sized)

**DO NOT change the topology or transistor sizing. ONLY fix the compensation network (Cc, Rc), the testbenches, and the plots.**

### Read Before Starting

- This file (`program_v2.md`) — the corrected design rules
- `design.cir` — the current (broken compensation) netlist
- `specification.json` — pass/fail criteria
- `specs.tsc` — metric extraction patterns (WILL BE MODIFIED — see below)

---

## 2. What Must Be Fixed

### Fix 1: Re-size Compensation Network (Cc and Rc)

The Miller cap Cc must be a **physically realizable** value. The nulling resistor Rc must be sized relative to 1/gm of the second stage.

**Hard constraints on Cc:**
- **Minimum:** Cc >= 0.2 * Cload = 0.2 * 100 pF = 20 pF
- **Maximum:** Cc <= 50 pF (area limit: 50 pF * 500 um^2/pF = 25,000 um^2 — acceptable)
- **Starting point:** Cc = 30 pF (proven to work in early v1 experiments: commit 9b6eb04 had Cc=30pF, PM=56.8, all 12/12 passing)

**Rc sizing:**
- Estimate gm2 of Mcs (second-stage NMOS CS amp) from simulation: run `.op` and extract `@m.xea.xmcs.m0[gm]`
- **Baseline Rc = 1/gm2** (cancels RHP zero — zero goes to infinity)
- **Aggressive Rc = (1/gm2) * (1 + Cload/Cc)** (places LHP zero to cancel second pole)
- For gm2 ~ 200 uA/V (estimated from 20 uA at Vov ~ 0.2V): Rc_baseline ~ 5 kOhm
- **Do not use Rc > 3/gm2** — excessive Rc creates a LHP zero that flattens the gain slope at crossover, leading to the pathological -3 dB/dec crossing seen in v1

**Sweep strategy:**
1. Start with Cc = 30 pF, Rc = 5 kOhm (1/gm2 estimate)
2. Run AC sim, check PM and GBW
3. If PM < 55 deg: increase Cc by 5 pF, repeat
4. If PM > 80 deg: decrease Cc by 5 pF, repeat
5. If GBW < 500 kHz: decrease Cc (or increase gm1 by raising tail current)
6. Once PM is in [60, 75] band: fine-tune Rc in 500-ohm steps

**Bode plot sanity check — MANDATORY before accepting any result:**
The gain must cross 0 dB with a slope between -15 dB/dec and -25 dB/dec (single-pole roll-off). If the slope at 0 dB crossing is flatter than -10 dB/dec, the compensation is broken — reduce Rc.

### Fix 2: Update specs.tsc — Change Primary Metric

The primary metric must be changed from `phase_margin_deg` (unbounded maximization) to `ugb_kHz` (maximize bandwidth while PM stays in [60, 80] band).

**New specs.tsc content** (overwrite the existing file):

```
# Block 00: Error Amplifier — Spec Tracker v2
# Primary metric: ugb_kHz (maximize bandwidth)
# Phase margin must be in [60, 80] band — both min AND max enforced
#
metric	grep_pattern	operator	threshold	unit	primary
ugb_kHz	^ugb_kHz:	>=	500	kHz	yes
ugb_kHz_max	^ugb_kHz:	<=	5000	kHz	no
phase_margin_deg	^phase_margin:	>=	60	deg	no
phase_margin_max	^phase_margin:	<=	80	deg	no
dc_gain_dB	^dc_gain:	>=	60	dB	no
output_swing_low_V	^output_swing_low:	<=	0.5	V	no
output_swing_high_V	^output_swing_high:	>=	4.5	V	no
iq_uA	^iq_uA:	<=	100	uA	no
input_offset_mV	^input_offset_mV:	<=	5	mV	no
cmrr_dB	^cmrr_dB:	>=	50	dB	no
psrr_dB	^psrr_dB:	>=	40	dB	no
devices_in_sat	^devices_in_sat:	>=	1	bool	no
pvt_all_pass	^pvt_all_pass:	>=	1	bool	no
cc_pF	^cc_pF:	<=	50	pF	no
gain_slope_at_ugb	^gain_slope_dBdec:	<=	-15	dBdec	no
noise_uVrms	^inoise_total_uVrms:	<=	20	uVrms	no
```

Key changes:
- **Primary metric = ugb_kHz** (higher bandwidth is better, target >= 500 kHz)
- **PM has BOTH min (60 deg) and max (80 deg)** — prevents overcompensation
- **Cc cap area constraint** (cc_pF <= 50)
- **Gain slope at UGB** (must be steeper than -15 dB/dec — single-pole-like)
- **Noise** (must report real simulated value <= 20 uVrms)

### Fix 3: Full 15-Corner PVT Sweep

The PVT testbench (`tb_ea_pvt.spice`) must test ALL 15 conditions:
- Process: tt, ss, ff, sf, fs
- Temperature: -40, 27, 150 degC

**Implementation:** Because ngspice `.lib` is set at file include time, you need 5 separate testbench files (one per corner) or a shell wrapper that generates them dynamically.

**Recommended approach — shell wrapper in run_block.sh:**

```bash
# In run_block.sh, replace the single PVT call with:
for corner in tt ss ff sf fs; do
    # Generate corner-specific testbench
    sed "s/\.lib.*sky130.lib.spice.*/\".lib \"$PDK_LIB\" $corner/" tb_ea_pvt_template.spice > tb_ea_pvt_${corner}.spice
    ngspice -b tb_ea_pvt_${corner}.spice >> "$PVT_OUT" 2>&1
done
```

**Or:** Create a single `tb_ea_pvt.spice` that accepts corner as a parameter using `.param` and conditional includes. But the sed approach is simpler.

**PVT pass criteria:** At ALL 15 conditions:
- DC gain >= 60 dB
- PM >= 55 deg (relaxed from 60 deg at extreme corners)
- UGB >= 200 kHz
- All devices in saturation

### Fix 4: Fix Noise Testbench

The `.noise` analysis failed because:
1. Vfb had no AC value (`.noise` needs the input source to be an independent voltage source)
2. The noise source reference must be at the top level, not inside the subckt

**Corrected tb_ea_noise.spice:**

```spice
* tb_ea_noise.spice — Input-referred noise analysis
* Method: Use .noise with Vfb as input source (must have AC 1)
*   .noise measures output noise and divides by gain to get input-referred

.lib "/path/to/sky130.lib.spice" tt
.include "design.cir"

Vpvdd pvdd 0 DC 5.0
Vref  vref 0 DC 1.226
Ven   en   0 DC 5.0
Ibias pvdd ibias DC 1u

* Input source — MUST have AC 1 for .noise to work
Vfb   vfb  0 DC 1.226 AC 1

* DC feedback to set operating point (large resistor, doesn't affect noise)
Rfb   vout_gate vfb 100Meg

Xea vref vfb vout_gate pvdd 0 ibias en error_amp
Cload vout_gate 0 100p

.nodeset v(vout_gate)=2.5

.control
  * First verify operating point converges
  op
  echo "=== Noise Analysis ==="

  * Run noise analysis: output = v(vout_gate), input source = Vfb
  noise v(vout_gate) Vfb dec 50 10 1Meg

  * Switch to noise results
  setplot noise1

  * Input-referred integrated noise (10 Hz to 1 MHz)
  let inoise_uv = inoise_total * 1e6
  echo "inoise_total_uVrms: $&inoise_uv"

  * Write spectral data for plotting
  setplot noise2
  wrdata noise_spectral.dat inoise_spectrum

  echo "noise_analysis: done"
  quit
.endc

.end
```

**Key fixes:**
- Vfb has `AC 1` — required for `.noise`
- Added `Rfb 100Meg` for DC feedback (same as AC testbench)
- Added `.nodeset` for convergence
- Write spectral data to `noise_spectral.dat` for plotting
- If `.noise` still fails with HV models, add `.option gmin=1e-12` and `.option reltol=1e-4`

### Fix 5: Real Saturation Check

Replace the crude d2 range check with actual Vds vs Vdsat comparison for every device.

**Corrected saturation check in tb_ea_dc.spice:**

```spice
* After .op, check saturation of every device:
.control
  op

  * Check each device: print Vds, Vdsat, margin
  echo "=== Saturation Check ==="
  let sat_ok = 1

  * For NMOS: Vds > Vdsat
  * For PMOS: |Vds| > |Vdsat| (equivalently Vsd > Vsdsat)

  * Diff pair M1 (PMOS): Vsd = V(tail_s) - V(d1)
  let m1_vsd = v(xea.tail_s) - v(xea.d1)
  let m1_vdsat = @m.xea.xm1.m0[vdsat]
  let m1_margin = m1_vsd - abs(m1_vdsat)
  echo "M1(diff+): Vsd=$&m1_vsd Vdsat=$&m1_vdsat margin=$&m1_margin"
  if m1_margin < 0.05
    let sat_ok = 0
    echo "  WARNING: M1 NOT in saturation (margin < 50mV)"
  end

  * Diff pair M2 (PMOS): Vsd = V(tail_s) - V(d2)
  let m2_vsd = v(xea.tail_s) - v(xea.d2)
  let m2_vdsat = @m.xea.xm2.m0[vdsat]
  let m2_margin = m2_vsd - abs(m2_vdsat)
  echo "M2(diff-): Vsd=$&m2_vsd Vdsat=$&m2_vdsat margin=$&m2_margin"
  if m2_margin < 0.05
    let sat_ok = 0
  end

  * NMOS mirror left (diode — always saturated if on, but check)
  let mnl_vds = v(xea.d1)
  let mnl_vdsat = @m.xea.xmn_l.m0[vdsat]
  let mnl_margin = mnl_vds - abs(mnl_vdsat)
  echo "Mn_l(mirror): Vds=$&mnl_vds Vdsat=$&mnl_vdsat margin=$&mnl_margin"
  if mnl_margin < 0.05
    let sat_ok = 0
  end

  * NMOS mirror right
  let mnr_vds = v(xea.d2)
  let mnr_vdsat = @m.xea.xmn_r.m0[vdsat]
  let mnr_margin = mnr_vds - abs(mnr_vdsat)
  echo "Mn_r(mirror): Vds=$&mnr_vds Vdsat=$&mnr_vdsat margin=$&mnr_margin"
  if mnr_margin < 0.05
    let sat_ok = 0
  end

  * Stage 2 CS amp (NMOS)
  let mcs_vds = v(vout_gate)
  let mcs_vdsat = @m.xea.xmcs.m0[vdsat]
  let mcs_margin = mcs_vds - abs(mcs_vdsat)
  echo "Mcs(CS): Vds=$&mcs_vds Vdsat=$&mcs_vdsat margin=$&mcs_margin"
  if mcs_margin < 0.05
    let sat_ok = 0
  end

  * Stage 2 PMOS load
  let mpld_vsd = 5.0 - v(vout_gate)
  let mpld_vdsat = @m.xea.xmp_ld.m0[vdsat]
  let mpld_margin = mpld_vsd - abs(mpld_vdsat)
  echo "Mp_ld(load): Vsd=$&mpld_vsd Vdsat=$&mpld_vdsat margin=$&mpld_margin"
  if mpld_margin < 0.05
    let sat_ok = 0
  end

  * Tail current source (PMOS)
  let mtail_vsd = 5.0 - v(xea.tail_s)
  let mtail_vdsat = @m.xea.xmtail.m0[vdsat]
  let mtail_margin = mtail_vsd - abs(mtail_vdsat)
  echo "Mtail: Vsd=$&mtail_vsd Vdsat=$&mtail_vdsat margin=$&mtail_margin"
  if mtail_margin < 0.05
    let sat_ok = 0
  end

  echo "devices_in_sat: $&sat_ok"

  * Also extract gm of second stage for Rc sizing
  let gm2 = @m.xea.xmcs.m0[gm]
  let gm2_uAV = gm2 * 1e6
  echo "gm2_uAV: $&gm2_uAV"
  let rc_opt = 1.0/gm2
  echo "rc_optimal_ohm: $&rc_opt"

  quit
.endc
```

**Note on ngspice hierarchical device names:** The exact path `@m.xea.xmcs.m0[vdsat]` depends on how ngspice flattens the hierarchy. If it doesn't work:
- Try `@m.xea.xmcs.msky130_fd_pr__nfet_g5v0d10v5[vdsat]`
- Or run `show all` after `.op` to discover the actual device names
- Or use `print all` to dump all operating point parameters

### Fix 6: Gain Slope Measurement at UGB

Add to the AC testbench (`tb_ea_ac.spice`) a measurement of the gain slope at the unity-gain crossing. This catches pathological overcompensation.

**Add this after UGB extraction:**

```spice
* Measure gain slope at UGB (dB/decade)
* Use points 1/2 decade below and above UGB
if ugb_hz > 0
  let f_lo = ugb_hz / 3.16
  let f_hi = ugb_hz * 3.16
  * Find indices closest to f_lo and f_hi
  let j = 0
  let g_lo = 0
  let g_hi = 0
  repeat $&n
    if frequency[j] >= f_lo
      if g_lo = 0
        let g_lo = gain_db[j]
      end
    end
    if frequency[j] >= f_hi
      if g_hi = 0
        let g_hi = gain_db[j]
      end
    end
    let j = j + 1
  end
  let slope = g_hi - g_lo
  echo "gain_slope_dBdec: $&slope"
end
```

A proper -20 dB/dec crossing should report a slope near -20. If the slope is flatter than -10, the design is overcompensated.

### Fix 7: Report Cc Value in run.log

The AC or DC testbench should report the compensation cap value so the evaluator can enforce the area constraint:

```spice
* Report compensation values
echo "cc_pF: 30"
```

Since Cc is a fixed value in design.cir, you can either hardcode this echo or parse it from the netlist. The evaluator will check cc_pF <= 50.

### Fix 8: Fix plot_all.py

The plot script must:
1. **Read real noise data** from `noise_spectral.dat` (not fabricate a curve)
2. **Read real PVT PM data** (not hardcode 157.5)
3. **Show the gain slope at UGB** on the Bode plot
4. **Mark the target PM band [60, 80]** on the Bode plot

If noise data is unavailable (noise sim still failing), the plot should show "NO DATA" — not a fake curve.

---

## 3. The Corrected Experiment Loop

### Preparation

Before entering the loop:

1. Extract gm2 from the existing design: run `.op` and print `@m.xea.xmcs.m0[gm]`
2. Compute Rc_baseline = 1/gm2
3. Set Cc = 30 pF, Rc = Rc_baseline
4. Overwrite `specs.tsc` with the v2 version (see Fix 2 above)
5. Update testbenches with fixes (noise, saturation, PVT corners, gain slope)

### LOOP

```
1. Check git state
2. Modify ONLY Cc and Rc in design.cir
   - Cc range: [20, 50] pF
   - Rc range: [0.5/gm2, 3/gm2]
3. Update the cc_pF echo in the testbench to match
4. git commit -m "exp(00): Cc=XpF Rc=Yk"
5. Run: bash run_block.sh > run.log 2>&1
6. Extract results
7. Check:
   a. PM in [60, 80] deg? If not, adjust Cc (up if PM<60, down if PM>80)
   b. GBW >= 500 kHz? If not, reduce Cc or check gm1
   c. Gain slope at UGB between -15 and -25 dB/dec? If flatter, reduce Rc
   d. Cc <= 50 pF? Must be.
   e. All other specs still passing?
8. If ugb_kHz improved AND all specs pass → KEEP
   Else → DISCARD: git reset --hard HEAD~1
9. Go to 1
```

### Convergence Criteria

The design is done when:
- PM in [60, 75] degrees
- GBW >= 500 kHz (ideally 1-3 MHz)
- Gain crosses 0 dB at -20 dB/dec (+/- 5)
- Cc <= 50 pF
- All 15 PVT corners pass
- Noise < 20 uVrms (real measurement)
- All other existing specs pass

### When To Stop Optimizing Cc/Rc

Once you have PM = 65 +/- 5 degrees with GBW > 1 MHz and Cc < 50 pF, **stop adjusting compensation** and move to verification:
1. Run full 15-corner PVT
2. Run noise
3. Run all testbenches
4. Generate plots
5. Update README.md
6. Commit and push

---

## 4. Absolute Rules (Unchanged from v1)

1. **Real Sky130 PDK only.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device.
2. **No behavioral models.** No ideal op-amps, no VCCS, no VerilogA.
3. **ngspice only.** No HSPICE, Spectre, or Xyce.
4. **Every spec verified by simulation.** The final claimed performance must come from a re-runnable ngspice testbench.
5. **No fabricated data in plots.** If a simulation crashes, the plot must say "NO DATA" — never generate a fake curve.
6. **Cc <= 50 pF.** This is a hard physical constraint. 50 pF ~ 25,000 um^2 in SKY130 MIM. Anything larger is not tape-out-worthy.
7. **PM must be in [60, 80] degrees.** Both min and max. Over-damping is as bad as under-damping for an LDO — it kills transient response.
8. **All 15 PVT corners must be tested.** 5 process (tt/ss/ff/sf/fs) x 3 temperature (-40/27/150 C).

---

## 5. Expected Final Numbers (Sanity Check)

Based on the v1 experiment history (commit 9b6eb04: Cc=30pF, PM=56.8, 12/12 pass) and analog design fundamentals:

| Parameter | Expected Range | Notes |
|-----------|---------------|-------|
| DC gain | 64-66 dB | Unchanged from v1 (set by device sizing, not compensation) |
| GBW | 1-3 MHz | With Cc=30pF, gm1~50uA/V: GBW = gm1/(2pi*Cc) ~ 265 kHz; may need to increase tail current |
| Phase margin | 60-70 deg | With proper Cc/Rc balance |
| Cc | 20-40 pF | Realizable on-chip |
| Rc | 3-8 kOhm | Near 1/gm2 |
| Gain slope at UGB | -18 to -22 dB/dec | Clean single-pole crossing |
| Iq | 86 uA | Unchanged unless tail current is modified |
| Output swing | 0.01 - 5.0 V | Unchanged (set by topology) |
| Noise | < 20 uVrms | Dominated by diff pair 1/f noise |

---

## 6. File Changes Summary

| File | Action | Description |
|------|--------|-------------|
| `design.cir` | EDIT | Change Cc from 1300p to ~30p, Rc from 11.38k to ~5k |
| `specs.tsc` | OVERWRITE | New v2 metrics (primary=ugb, PM band, Cc limit, slope) |
| `tb_ea_dc.spice` | REWRITE | Real saturation check using Vds vs Vdsat for all devices |
| `tb_ea_ac.spice` | EDIT | Add gain slope measurement at UGB, add cc_pF echo |
| `tb_ea_noise.spice` | REWRITE | Fix: add AC 1 to Vfb, add Rfb feedback, write spectral data |
| `tb_ea_pvt.spice` | REWRITE | All 15 corners: 5 process x 3 temperature |
| `run_block.sh` | EDIT | Add PVT corner loop (generate per-corner testbenches) |
| `plot_all.py` | REWRITE | Read real data only, no fake curves, show PM band on Bode |
| `evaluate.py` | NO CHANGE | Works as-is with new specs.tsc |
| `README.md` | REWRITE | After all fixes, regenerate with correct data |

---

## 7. Interface (Unchanged)

```
.subckt error_amp vref vfb vout_gate pvdd gnd ibias en
```

| Pin | Direction | Voltage | Description |
|-----|-----------|---------|-------------|
| vref | Input | 1.226 V | Bandgap reference (+ input) |
| vfb | Input | ~1.226 V | Feedback divider (- input) |
| vout_gate | Output | 0-5 V | Pass device gate drive |
| pvdd | Supply | 5.0 V | Positive supply |
| gnd | Supply | 0 V | Ground |
| ibias | Input | 1 uA sink | External bias current |
| en | Input | 0 / PVDD | Enable (active high) |

---

## 8. Testbench Requirements (Updated)

| Testbench | Measurements | New in v2 |
|-----------|-------------|-----------|
| tb_ea_dc.spice | Node voltages, Iq, saturation | **Real Vds vs Vdsat check per device, gm2 extraction** |
| tb_ea_ac.spice | DC gain, UGB, PM | **Gain slope at UGB, Cc value report** |
| tb_ea_swing.spice | Output swing low/high | No change |
| tb_ea_offset.spice | Input offset | No change |
| tb_ea_cmrr.spice | CMRR at DC | No change |
| tb_ea_psrr.spice | PSRR at DC and vs freq | No change |
| tb_ea_noise.spice | Input-referred noise, spectral | **Fixed: AC 1 on Vfb, Rfb feedback, wrdata spectral** |
| tb_ea_pvt.spice | All specs at PVT | **All 15 corners (5 process x 3 temp)** |

---

## 9. Required Plots (Updated)

| Plot | Source | What it shows | v2 requirement |
|------|--------|---------------|----------------|
| bode_gain_phase.png | tb_ea_ac | Gain/phase vs freq | **Mark PM band [60,80], show slope annotation at UGB** |
| output_swing.png | tb_ea_swing | Vout vs input | No change |
| noise_spectral.png | tb_ea_noise | Input-referred noise vs freq | **REAL DATA ONLY — no fake curves** |
| psrr_vs_freq.png | tb_ea_psrr | PSRR vs freq | No change |
| pvt_gain.png | tb_ea_pvt | DC gain at 15 PVT corners | **All 15 corners, not just 3** |
| pvt_pm.png | tb_ea_pvt | PM at 15 PVT corners | **Real extracted PM values, all 15 corners** |

---

## 10. Deliverables Checklist

Before committing the final result, verify:

- [ ] `design.cir` has Cc <= 50 pF
- [ ] All 15 PVT corners tested and passing
- [ ] Noise analysis produces real data (not fabricated)
- [ ] Saturation check uses real Vds vs Vdsat per device
- [ ] PM is in [60, 80] range
- [ ] GBW >= 500 kHz
- [ ] Gain crosses 0 dB at approximately -20 dB/dec
- [ ] All plots use real simulation data
- [ ] README.md updated with correct numbers
- [ ] xschem schematic updated if compensation values changed

---

*program_v2.md — 2026-03-28*
