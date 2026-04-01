# Design Review: PVDD 5V LDO Regulator — Honest Opinions

**Reviewer perspective:** Senior analog IC designer, 15+ years in automotive power management.
**Date:** 2026-04-01
**Scope:** All 11 blocks (00–10), system architecture, compensation strategy, PVT robustness.

This is a design review, not a congratulatory note. I will call out what is good, what is questionable, and what is broken.

---

## Block 00: Error Amplifier

### Purpose
The core OTA that compares the feedback voltage (vfb) to the bandgap reference (avbg) and drives the pass device gate. Must achieve sufficient gain for tight regulation while maintaining stability.

### Implementation
Two-stage OTA:
- **Stage 1:** PMOS differential pair (W=80µm L=4µm ×2) with NMOS current-mirror load (W=20µm L=8µm ×2), powered from BVDD. Tail current ~40µA from a 4× PMOS mirror.
- **Stage 2:** NFET common-source (W=20µm L=2µm) with PFET active load (W=20µm L=4µm ×4), also BVDD-powered.
- **Compensation:** Cc=2pF, Rc=5kΩ (Miller, from d2 to vout_gate).
- **Enable:** NFET gate on bias path + PFET pull-up to BVDD.

### What is good

1. **PMOS differential pair is the right choice for an LDO error amp.** The PMOS input allows the common-mode input range to include ground, which is essential since vfb and vref are both near 1.2V. This follows standard LDO practice (see Rincon-Mora, "Analog IC Design with Low-Dropout Regulators," 2nd ed., and virtually every published LDO from TI, Analog Devices, Maxim).

2. **BVDD-powered topology solves the startup chicken-and-egg problem.** Powering the EA from the input supply means it works from the moment BVDD is present — no separate startup circuit needed to bootstrap the amplifier supply. This is a legitimate architectural choice used in some industrial LDOs (e.g., TDK-Micronas HVCM, which this design references).

3. **Long-channel devices (L=4–8µm) for gain and matching.** The diff pair at L=4µm and mirror at L=8µm are well-chosen for high output impedance (high gain) and Pelgrom matching. This is textbook good practice for precision analog.

4. **Standalone performance is solid:** 78.4 dB gain, 513 kHz UGB, 67.5° PM at TT 27°C. These are reasonable numbers for a two-stage OTA standalone.

### What is questionable

1. **The design.cir has Cc=2pF, but the README claims 36pF (standalone) or 98pF (LDO integration).** The actual hardware is 2pF. This is an enormous discrepancy. The comment says "Miller comp minimized: 2pF + 5k (just enough for EA stability)" — but 2pF provides almost no Miller effect. At the system level, the 1µF external cap is doing all the work. This means the "standalone" characterization in the README (Cc=36pF, PM=67.5°, UGB=513kHz) does not reflect what is actually in the circuit.

2. **The header comments are misleading.** The block header describes a "cascode PFET" in Stage 2 that does not exist in the netlist. Lines 8–12 describe `XMcas_p: Cascode PFET, gate=cas_bias` and a resistive divider for `cas_bias = 0.8 × BVDD`, but none of these elements appear in the actual circuit. The real Stage 2 is a simple NFET CS + PFET load — no cascode. Comments that describe a different circuit than what exists are dangerous in a production design.

3. **Stage 2 has no cascode — output impedance and PSRR suffer.** A cascode on the PFET load (or an NFET cascode on the gain device) would significantly boost the second-stage gain and improve PSRR. The top-level README acknowledges this: "No cascode on Stage 2... relies on loop gain for rejection." This is acceptable only because the 1µF cap provides massive loop gain at DC.

4. **XMpu (pullup when disabled) is W=4µm L=2µm.** The README device table says W=20µm L=1µm. Another documentation mismatch. The actual device is small, which means the pullup may be slow to discharge Cgs of the pass device when the EA is disabled.

### What is concerning

1. **The EA enable (ea_en) is always tied to BVDD in the top-level integration.** The startup circuit ties ea_en to BVDD through a 100Ω resistor, making it permanently active. The mode control output `mc_ea_en` — which should disable the EA during POR and bypass modes — is floating. This means the error amplifier is fighting the pass device at all times, including during power-up when it should be off.

2. **The bias mirror chain is single-ended.** XMbn0 (W=2µm L=8µm, 1µA diode) mirrors to XMbn_pb (W=20µm L=8µm ×4, intended ~40µA). The mirror ratio is (20×4)/(2×1) = 40×. This is a large ratio — systematic mismatch from channel-length modulation will be significant at L=8µm. A cascode mirror or a regulated-cascode bias would be more robust.

3. **No common-mode feedback.** The two-stage topology relies on the Miller cap to set the DC bias of vout_gate. With only 2pF, the DC operating point of the output stage is weakly defined. The .op convergence issues reported at some corners may be related to this.

### Industry comparison

Published LDO error amplifiers overwhelmingly use either:
- **Folded-cascode OTA** (single stage, high gain) — preferred for capless LDOs where bandwidth matters (Leung et al., JSSC 2003; Al-Shyoukh et al., JSSC 2007)
- **Two-stage Miller OTA** — used when the load cap is large and provides the dominant pole (Rincon-Mora & Allen, JSSC 1998)

This design uses the two-stage topology but with a 1µF external cap providing the dominant pole. That's a valid combination — it's effectively the classic "cap-compensated LDO" architecture. However, the 2pF internal Miller cap is unusual. Most two-stage LDO amplifiers use 5–50pF for Miller compensation. Using 2pF essentially makes this a "degenerate" two-stage where the external cap does 99% of the compensation work.

### Recommendation

- **Fix the comments** to match the actual circuit. Remove all references to the non-existent cascode.
- **Add a cascode** to Stage 2 (either on XMcs_p or a folded cascode on XMcs_n). This is cheap (one device) and would improve both gain and PSRR by 15–20 dB.
- **Increase Cc to at least 5–10pF** to provide meaningful local feedback for the two-stage amplifier, rather than relying entirely on the external cap.
- **Connect mc_ea_en** from mode control to the actual ea_en input.

---

## Block 01: Pass Device

### Purpose
The PMOS pass transistor that regulates PVDD from BVDD. Must deliver 50mA with <400mV dropout across PVT.

### Implementation
10 parallel instances of `pfet_g5v0d10v5` at W=50µm L=0.5µm m=2 each. Total W = 1.0mm. Source=BVDD, Drain=PVDD, Bulk=BVDD.

### What is good

1. **Total width of 1mm for 50mA is compact and efficient.** The worst-case (SS 150°C) delivers 56.8mA at 400mV dropout — 13.6% margin. This is well-sized.

2. **L=0.5µm (minimum for HV device) is correct.** For a pass device, minimum length maximizes current per unit width and minimizes Cgs. There's no need for long-channel here since matching isn't critical.

3. **Cgs = 1.04 pF is very manageable.** This is a light load for the error amplifier — many published LDO pass devices have 10–100pF gate capacitance.

4. **Rds_on = 4.75Ω gives plenty of headroom.** At 50mA, the dropout is I×Rds_on = 237mV, well below the 400mV spec.

### What is questionable

1. **Using W=50µm m=2 instead of W=100µm m=1.** The README says "W=100um per instance" but the design.cir uses W=50µm m=2. The ngspice Sky130 PDK ignores the `mult` parameter according to the README, but `m=2` should work. This should be verified — if `m` is also ignored, each instance is only 50µm and total width is 500µm, halving the current capability. The 56.8mA worst-case measurement suggests m=2 is working, but this is a PDK landmine.

2. **No dummy devices at the edges of the array.** For 10 parallel instances, the edge devices will have different stress/matching than center devices. For a pass device this matters less than for a current mirror, but it's still good practice.

3. **All instances share the same gate node.** This is fine electrically but layout-dependent — long gate bus resistance can create non-uniform current sharing. A proper layout would use a comb or H-tree gate distribution.

### What is concerning

1. **SOA at sustained short circuit.** At BVDD=10.5V and Ishort=63mA (from top-level), the pass device dissipates 10.5V × 63mA = 662mW. At SS 150°C with the current limiter allowing 137mA, that's 1.44W. For a 1mm-wide device in 130nm, this is a significant concern. The thermal resistance of the die needs to be considered.

### Industry comparison

For a 50mA 5V LDO in 130nm CMOS, 1mm total PMOS width is on the lower end but reasonable. Published 130nm LDOs typically use 2–10mm for 50–100mA (e.g., Hazucha et al., JSSC 2005 uses 5mm/0.5µm for 100mA; various TI/ADI datasheets show similar). The compact size here is possible because the Sky130 HV PMOS has reasonable mobility.

### Recommendation

- Verify `m=2` is correctly handled by the simulator for this PDK device.
- Add SOA analysis for sustained short circuit at SS 150°C corners.
- Consider adding guard rings or dummy structures for layout robustness.

---

## Block 02: Feedback Network

### Purpose
Resistive voltage divider that scales PVDD (5.0V) down to vfb (1.226V) for comparison with the bandgap reference.

### Implementation
Two `res_xhigh_po` resistors: R_TOP (W=3µm L=536µm ≈ 364kΩ) and R_BOT (W=3µm L=174.3µm ≈ 118kΩ). Total R ≈ 482kΩ, divider ratio 0.2452.

### What is good

1. **Same resistor type for both legs — first-order TC cancellation.** Using `res_xhigh_po` for both R_TOP and R_BOT means the temperature coefficient of the ratio depends on the second-order TC mismatch, not the absolute TC. This is standard best practice (see Johns & Martin, "Analog Integrated Circuit Design," Chapter 4).

2. **W=3µm is good for matching.** Pelgrom matching improves with width. For xhigh_po (sheet ρ ≈ 2kΩ/sq), W=3µm is a reasonable choice that balances matching against area.

3. **Total resistance of 482kΩ keeps quiescent current at ~10µA.** This is a good trade-off between current consumption and noise. Lower resistance would be noisier in the thermal noise floor; higher resistance would increase Johnson noise contribution to the feedback node.

### What is questionable

1. **No filter capacitor across R_BOT.** A small cap (1–5pF) across R_BOT would filter high-frequency noise at the vfb node, preventing noise from coupling into the error amplifier input. Most production LDOs include this. The omission is understandable if bandwidth is already very low (which it is — 1.9 kHz UGB), but it's still good practice.

2. **The divider ratio accuracy depends entirely on resistor matching.** With no trimming, the ±3.5% output accuracy must come from the resistor ratio tolerance + bandgap accuracy + error amp offset. The Monte Carlo analysis should verify this, but I don't see MC results for the feedback network in isolation.

3. **482kΩ total impedance creates a high-impedance node at vfb.** Any parasitic capacitance at vfb (from routing, gate cap of EA input) forms a pole with 482kΩ. At Cpar=0.5pF, that's a pole at 660kHz. This is above the system UGB (1.9kHz) so it's fine, but if the design were ever modified to increase bandwidth, this would become a problem.

### Industry comparison

Typical LDO feedback dividers use 100kΩ–1MΩ total resistance. 482kΩ is in the sweet spot. TI's TPS7A series uses ~200kΩ; ADI's ADP150 uses ~400kΩ. The choice here is reasonable and industry-standard.

### Recommendation

- Add a 2–5pF cap across R_BOT for noise filtering.
- Run Monte Carlo on the divider ratio to verify ±3.5% PVDD accuracy is achievable.

---

## Block 03: Compensation Network

### Purpose
Frequency compensation to ensure loop stability (PM > 45°) across all load conditions (0–50mA).

### Implementation

**The subcircuit is completely empty.** All components have been removed:

```spice
.subckt compensation vout_gate pvdd gnd
* Miller comp REMOVED — inner EA Cc/Rc (30pF/25k) handles pole-splitting
* Outer Cc+Rz was redundant, killing bandwidth (UGB=170Hz with it)
* Output Cout REMOVED — 1µF external cap dominates; 70pF added load on EA for no benefit
.ends compensation
```

The actual compensation consists of:
- **Cc=2pF + Rc=5kΩ** inside the error amplifier (Block 00 design.cir)
- **Cout_ext=1µF** external bypass capacitor (Block 10 top integration)

### What is good

1. **The decision to remove redundant compensation is defensible.** If the 1µF external cap provides a dominant pole at ~1.6Hz and the inner EA Cc handles local two-stage stability, adding an outer Miller cap would indeed reduce UGB further for no benefit.

2. **The 1µF external cap gives massive phase margin (125–161°).** The system is unconditionally stable. There is no load condition where this design oscillates.

### What is questionable

1. **The README is deeply misleading.** The Block 03 README describes Cc=30pF + Rz=5kΩ + Cout=70pF with a total area of 49,901 µm² and detailed performance tables. None of these components exist in the actual circuit. The README describes a ghost circuit. The PM/UGB numbers in the README (45.8°–84.4° across loads, UGB up to 51MHz) describe a completely different design than what is built.

2. **The design.cir comments claim "inner EA Cc/Rc (30pF/25k) handles pole-splitting"** but the actual EA has Cc=2pF and Rc=5kΩ. Either the EA was modified after this comment was written, or the comment is wrong. This is a documentation disaster.

3. **An empty subcircuit is a code smell.** If the compensation block does nothing, it should be removed from the design hierarchy entirely rather than kept as a phantom block with misleading comments. Keeping it creates confusion about where compensation actually lives.

### What is concerning

1. **All stability depends on an external component.** The 1µF cap is essential — without it, PM would likely be negative (oscillation). The Block 03 README itself notes that "PVT corners fail PM ≥ 45° without output cap" and "Real capless LDOs solve this with class-AB output stages." This is an honest admission that the design cannot work without the external cap.

2. **The UGB of 1.9kHz is extremely low.** For context, most 50mA LDOs have UGB of 100kHz–1MHz. A 1.9kHz bandwidth means:
   - Load transient recovery is slow (the 1µF cap must absorb the initial charge/discharge)
   - Line transient rejection above 2kHz is limited to the open-loop PSRR of the pass device
   - The LDO cannot respond to fast load changes — it's essentially "open loop" above 2kHz

3. **PM of 125–161° is over-compensated.** Phase margin above 90° means the system is sluggish. The optimal target for a well-designed LDO is 55–70° — enough margin for PVT variation while maintaining good transient response. 161° means the loop is barely doing anything useful at frequencies above a few Hz.

### Industry comparison

Published LDO compensation strategies fall into three categories:

1. **External-cap LDOs** (this category): Use a large output cap (1–10µF) as the dominant pole. Simple, robust, but slow. This is the approach used by classic voltage regulators like the LM7805. Modern versions include TI TPS7A series, ADI ADP1740. Typical UGB: 50–500kHz with 1µF ceramic.

2. **Internally-compensated (capless) LDOs:** Use Miller compensation, nested Miller, or current-buffer compensation. No external cap needed. Faster transient response. Examples: Milliken et al. (JSSC 2007), Hazucha et al. (JSSC 2005). Typical UGB: 1–10MHz.

3. **Hybrid:** Small external cap (100pF–10nF) + internal compensation. Common in automotive. Examples: Infineon TLE4xxx, NXP MC33xxx.

This design is firmly in category 1, but with an unusually low UGB due to the very large cap (1µF) combined with minimal internal compensation. A well-designed external-cap LDO should achieve 100–500kHz UGB with 1µF, not 1.9kHz. The issue is that the internal compensation (2pF) provides almost no pole-splitting — the two EA poles are close together, and the 1µF cap must be large enough to push the UGB below both of them. A proper Miller cap (20–50pF) inside the EA would split the EA poles apart, allowing a much higher UGB with the same 1µF external cap.

### Recommendation

- **Restore meaningful inner compensation** to the EA: Cc=20–30pF, Rc as needed for RHP zero cancellation. This will split the EA poles and allow the UGB to move up to 100–500kHz.
- **Remove or honestly document** Block 03. An empty subcircuit with a misleading README is worse than no block at all.
- **If truly capless operation is desired,** the error amplifier needs a fundamentally different architecture: class-AB output stage with adaptive Miller compensation (Milliken topology) or a flipped voltage follower output (Hazucha topology). The current simple two-stage OTA cannot be made stable without a large external cap.

---

## Block 04: Current Limiter

### Purpose
Overcurrent protection that prevents pass device destruction during short-circuit or overload. Must be transparent during normal operation (0–50mA).

### Implementation
Sense-mirror brick-wall limiter:
- **XMs** (W=1µm L=0.5µm): Sense PMOS, mirrors 1/1000th of pass device current
- **XMcas** (W=10µm L=0.5µm): Cascode PMOS, gate tied to PVDD for Vds matching
- **XRs** (xhigh_po W=1µm L=7µm ≈ 14kΩ): Converts sense current to voltage
- **XMdet** (W=20µm L=1µm): Detection NMOS, turns on when Vsense > Vth
- **XRpu** (xhigh_po W=1µm L=500µm ≈ 1MΩ): Pull-up to BVDD
- **XMclamp** (4× W=50µm L=0.5µm m=2 = 400µm): Pulls gate toward BVDD
- **XMfp/XMfn**: Flag output inverter

### What is good

1. **The cascode for Vds matching (added in v4) is the right fix.** Without it, the sense PMOS operates at a very different Vds than the pass device, causing massive CLM (channel-length modulation) error. Tying the cascode gate to PVDD provides automatic tracking — when PVDD drops (heavy load), the cascode bias tracks. This moved the trip point from ~20mA to ~50mA, which is exactly the expected behavior.

2. **The 1/1000 mirror ratio is reasonable.** It keeps the sense current at ~50µA for 50mA load, which is manageable for the resistor-based detection.

3. **Brick-wall characteristic is appropriate for this current level.** At 50mA and 10.5V max, foldback isn't strictly necessary. The pass device power in short circuit is 10.5V × 63mA = 660mW — significant but manageable for short durations. (However, see concerns below about SS 150°C.)

4. **The README is brutally honest about the 3.1x PVT spread.** The designer clearly understands the limitation and documents it with root cause analysis. This is the right attitude.

### What is questionable

1. **Cas_bias tied to PVDD.** While this provides automatic tracking, PVDD during a short circuit is ~0V. That means Vgs_cas ≈ 0V – the cascode turns off during the exact condition it's supposed to help with. The cas_mid node floats, and the sense path degenerates to the pre-v4 behavior. A dedicated bias (e.g., a fraction of BVDD) would be more robust.

2. **Pull-up resistor (1MΩ) to BVDD wastes current.** At BVDD=10.5V, the steady-state current through XRpu when XMdet is OFF is 10.5V/1MΩ = 10.5µA. This is not negligible — it's ~4% of the total quiescent current budget. A PMOS pull-up controlled by a bias current would consume less.

3. **The sense resistor (XRs) is very small.** W=1µm L=7µm for xhigh_po. The matching of such a tiny resistor is poor. Pelgrom mismatch for poly resistors scales as 1/√(W×L), and W×L = 7µm² is small. However, since this is a single resistor (not a ratio), absolute accuracy is what matters, and that's dominated by process variation, not mismatch.

4. **Vth-based detection is inherently temperature-sensitive.** The trip condition is `I_sense × Rs ≈ Vth(XMdet)`. Both Rs and Vth have large temperature coefficients that compound rather than cancel: Rs drops at high temp (xhigh_po has TC1 = -1.47e-3/°C) while Vth also drops (~-1 to -2 mV/°C for NMOS). At 150°C, both effects push the trip point higher, explaining the 137mA at SS 150°C.

### What is concerning

1. **3.1x PVT spread (44mA to 137mA) is unacceptable for production.** At FF -40°C, the limiter trips at 44mA — only 6mA above the rated 50mA load. Normal load transients could false-trigger the limiter, causing output voltage dips. At SS 150°C, 137mA means 1.44W in the pass device during a sustained short — this is a thermal reliability risk.

2. **The clamp feedback loop is uncompensated.** When XMdet turns on, it pulls det_n low, which turns on XMclamp, which pulls the gate toward BVDD, which reduces pass device current, which reduces sense voltage, which turns off XMdet... This is a negative feedback loop. Without compensation, it could ring or oscillate. The README says "no oscillation" at TT 27°C, but has this been verified at all PVT corners? The 100µs response time suggests it might be sluggish rather than properly damped.

3. **The flag output inverter (XMfp/XMfn) drives ilim_flag, but ilim_flag is not connected to anything in the top-level integration.** The `ilim_en` signal from mode control (which should gate the current limiter) is also floating. The current limiter is always active, with no ability to disable it during bypass or retention modes.

### Industry comparison

Production current limiters in automotive LDOs typically use:
- **Proportional (analog) current limiting:** A current mirror comparator with a reference derived from a temperature-compensated source (PTAT or bandgap). This gives 10–20% PVT variation, not 300%. Examples: TI TPS7A4700, Infineon TLE4275.
- **Foldback current limiting:** Reduces current in short circuit below the trip point. Standard for high-power LDOs. Not strictly necessary at 50mA.
- **Thermal shutdown** as a backup: If the current limiter allows too much current at hot corners, thermal shutdown prevents destruction. This design has no thermal protection.

The Vth-based detection used here is a "freshman" topology — simple to understand, but its PVT sensitivity makes it unsuitable for production automotive parts. The designer's own README recommends replacing it with a "current mirror comparator where the reference current is derived from a temperature-compensated source." That is correct.

### Recommendation

- **Replace Vth-based detection** with a bandgap-referenced current comparator. Use the IREF (1µA) from the chip's bandgap — mirror it through a ratio to set the detection threshold. This replaces the poly resistor TC and NMOS Vth TC with the bandgap current TC (±2%), reducing PVT spread to ~20%.
- **Use a dedicated cascode bias** (e.g., BVDD – 2V from a resistive divider, not PVDD) so the cascode works during short circuit.
- **Add thermal shutdown** as a second line of defense.
- **Connect ilim_en** from mode control to actually gate the limiter.

---

## Block 05: UV/OV Comparators

### Purpose
Monitor PVDD and assert flags when the output voltage goes below the undervoltage threshold (~4.3V) or above the overvoltage threshold (~5.5V). Used by the system for fault detection and mode transitions.

### Implementation
Two separate comparators (UV and OV), each with:
- Resistive divider from PVDD to ground, scaling to vref (1.226V) at the trip point
- NMOS differential pair with PMOS current-mirror load, powered from vdd_comp (1.8V)
- ~1µA bias from a diode-connected NMOS + 800kΩ resistor
- Resistive hysteresis feedback
- NOR output gate with enable gating

### What is good

1. **Running from a separate 1.8V supply domain is correct.** UV/OV comparators should operate independently of the supply they're monitoring. Using vdd_comp (1.8V, presumably SVDD) ensures they work even when PVDD is out of range.

2. **NMOS differential pair is the right choice.** With inputs near 1.2V, an NMOS pair keeps the tail current source in saturation with adequate headroom (1.8V – Vgs_nmos – Vds_tail ≈ 1.8 – 0.5 – 0.2 = 1.1V). A PMOS pair would struggle with 1.8V supply.

3. **NOR gate output with enable is a clean logic interface.** When disabled (en_bar=HIGH), the flag is forced LOW regardless of comparator state. This prevents false flags during startup.

4. **Separate comparators for UV and OV is simpler than a window comparator.** Two independent comparators are easier to design, test, and debug. Standard practice.

### What is questionable

1. **Ideal resistors throughout.** R_top, R_bot, R_hyst, and R_bias are all ideal SPICE resistors (`R name node1 node2 value`), not PDK devices. In a production design, these would be poly or diffusion resistors with temperature coefficients, mismatches, and process variation. The trip points measured in simulation are optimistic — real silicon will show more spread.

2. **R_bias = 800kΩ to generate ~1µA.** This is (1.8V – Vgs)/800kΩ ≈ (1.8 – 0.5)/0.8M ≈ 1.6µA. The bias current depends on the supply voltage and the NMOS Vgs, which varies with process and temperature. A proper current reference (mirrored from the chip's IREF) would be more accurate.

3. **Asymmetric hysteresis feedback.** The UV comparator feeds back from `out_n` (internal) to `mid_uv`, while the OV comparator feeds back from `ov_flag` (output) to `mid_ov`. This creates different hysteresis dynamics — the OV hysteresis depends on the NOR gate delay, while the UV hysteresis is purely analog. This inconsistency seems accidental rather than intentional.

4. **R_hyst values differ significantly.** UV uses 2.5MΩ, OV uses 8MΩ. Combined with the divider impedances (~700kΩ UV, ~650kΩ OV), the hysteresis will be very different between the two. This should be justified.

### What is concerning

1. **The comparators use 1.8V (01v8) devices but the input dividers go up to PVDD=5V.** The R_top and R_bot form a divider from PVDD (up to 5.7V for OV testing) to ground. Since these are ideal resistors, there's no voltage rating issue. But in a real implementation, if these were poly resistors, the voltage across R_top (5.7V × 500k/650k ≈ 4.4V) would exceed the 1.8V device voltage rating. This is fine for xhigh_po (which handles high voltage), but the design should specify this explicitly.

2. **Enable inverter uses minimum-length devices (L=0.15µm).** XMen_n (W=0.42µm L=0.15µm) and XMen_p (W=0.84µm L=0.15µm) are 1.8V devices at minimum length. These will have significant leakage and poor matching. For a simple enable inverter this is probably fine, but the NOR gate also uses L=0.15µm. At 150°C, sub-threshold leakage through these devices could affect the output logic levels.

3. **No offset cancellation or trimming.** The comparator offset depends on NMOS pair matching (W=2µm L=1µm). With Avt ≈ 5–10 mV·µm for 130nm NMOS, the 1σ offset is Avt/√(W×L) ≈ 5/√2 ≈ 3.5mV referred to the comparator input. Multiplied by the divider gain (×4 for UV, ×4.5 for OV), this is ~15mV on PVDD — acceptable for the ±200mV spec window, but tight across 3σ.

### Industry comparison

Production UV/OV comparators in automotive LDOs typically use:
- **Dedicated bandgap-referenced thresholds** rather than resistive dividers from the monitored supply
- **Chopper-stabilized or auto-zeroed** comparators for precision thresholds
- **Digital trimming** for threshold accuracy (±1% typical)
- **PDK resistors** with characterized matching and TC

This implementation is functional for a prototype but would need significant work for production: real resistors, current-reference bias, offset trimming, and PVT characterization.

### Recommendation

- Replace ideal resistors with PDK xhigh_po devices.
- Use the chip's 1µA IREF for biasing instead of R_bias + diode.
- Make the hysteresis feedback consistent between UV and OV.
- Add PVT Monte Carlo analysis.

---

## Block 06: Level Shifter

### Purpose
Translates control signals between the SVDD domain (~2.2V) and the BVDD domain (5.4–10.5V) or PVDD domain.

### Implementation
Two subcircuits using cross-coupled PMOS topology:
- **level_shifter_up:** SVDD → BVDD (input inverter + NMOS pull-downs W=15µm + cross-coupled PMOS in BVDD domain)
- **level_shifter_down:** PVDD → SVDD (similar, with NMOS pull-downs W=2µm + cross-coupled PMOS in SVDD domain)

### What is good

1. **Cross-coupled PMOS is the standard topology for voltage level shifting.** This is textbook design, used in virtually every mixed-voltage IC. (See Weste & Harris, "CMOS VLSI Design," Chapter 1.)

2. **Zero static current.** In steady state, one NMOS is ON pulling one side low, and the corresponding cross-coupled PMOS is ON pulling the other side high. No DC path from supply to ground. Good for low-Iq automotive design.

3. **Asymmetric sizing in level_shifter_up (XMP1=4µm, XMP2=5µm).** This ensures the output side switches faster by making the output PMOS slightly stronger. A minor but thoughtful optimization.

4. **L=1µm on NMOS pull-downs.** Longer channel reduces sub-threshold leakage when the NMOS is OFF, preventing false switching at high temperatures. This is good practice for automotive.

### What is questionable

1. **Only one level shifter is used in the top-level integration.** XLS_EN shifts the external enable signal from SVDD to BVDD. But the level_shifter_down is not instantiated anywhere. If UV/OV flags (in SVDD domain) need to reach BVDD-domain logic, more shifters would be needed.

2. **The up-shifter NMOS pull-downs are very wide (W=15µm).** At SVDD=2.2V, these devices must overpower the cross-coupled PMOS (W=4–5µm) to flip the latch. The ratio 15:5 = 3:1 should work, but it's aggressive. At low SVDD (<2V) or high BVDD (>8V), the PMOS becomes stronger (larger Vsg) and the NMOS becomes weaker (smaller Vgs), potentially causing the shifter to fail. The minimum operating SVDD should be characterized.

3. **No buffering on the output.** The output is the raw cross-coupled node. Adding an inverter buffer would clean up the edges and provide drive strength.

### Industry comparison

Cross-coupled PMOS level shifters are universal in mixed-voltage designs. The topology here is standard. Some advanced designs use "current-mirror" level shifters for wider voltage range (Kuo & Ker, TCAS-I 2007), but for the 2.2V–10.5V range here, the basic cross-coupled topology is adequate.

### Recommendation

- Characterize minimum SVDD for reliable operation at maximum BVDD.
- Add output buffers if driving capacitive loads.
- Consider whether more level shifters are needed for the integration.

---

## Block 07: Zener Clamp

### Purpose
Overvoltage protection for PVDD. Clamps PVDD during load dump and transient overvoltage events. Also provides protection in HTOL (high-temperature operating life) test mode at 6.5V.

### Implementation
Hybrid clamp using MOS devices (no actual Zener diodes — Sky130 has none):
- **Precision stack:** N-P-N-P-N diode-connected MOSFETs (5 devices, L=4µm) for DC onset control
- **Fast diode stack:** 7× NFET (L=0.5µm W=10µm, body=GND) for transient response
- **Clamp NMOS:** W=100µm m=4 = 200µm, L=0.5µm, controlled by precision stack voltage
- **Rpd = 500kΩ:** Gate pull-down

### What is good

1. **Using L=4µm for the precision stack is clever.** Long-channel devices have a higher Vth (~1.07V vs ~0.7V at L=0.5µm) and a lower TC (~-0.6 mV/°C vs ~-1.1 mV/°C). This is a real insight — the designer clearly fought the TC problem and found a creative solution. At 5 devices, the stack voltage is ~5.35V with ~-3 mV/°C total TC.

2. **The mixed N-P-N-P-N stack alternates NMOS and PMOS devices.** This exploits the different Vth values and TCs of NMOS vs PMOS to fine-tune the onset voltage and reduce total TC. This is more sophisticated than a simple NMOS-only stack.

3. **The parallel fast diode stack (7× NFET) provides fast transient clamping.** The precision stack with Rpd=500kΩ has a slow time constant. The fast stack conducts immediately during a transient, buying time for the precision stack to respond.

4. **Honest documentation of PVT failures.** 6/15 PVT corners fail — the designer acknowledges this and explains why.

### What is questionable

1. **The name "Zener Clamp" is misleading.** There are no Zener diodes in this circuit. It's a MOSFET threshold-voltage clamp. The name will confuse anyone reading the design for the first time. Call it what it is: "MOS Voltage Clamp" or "Active Clamp."

2. **The fast stack uses body=GND for all 7 NFETs.** This means each NFET has body effect — the source-to-body voltage increases up the stack, raising the effective Vth of upper devices. The total stack voltage will be significantly higher than 7×Vth0. By contrast, the precision stack uses body=source (requiring deep N-well), eliminating body effect. The inconsistency suggests these were designed independently.

3. **6/15 PVT points fail.** This is a 40% failure rate. For automotive (AEC-Q100), the design must work across all corners. Requiring post-fab trimming (Rpd adjustment) adds test cost and complexity. At SF/FS corners, the onset shifts by >500mV — this is a fundamental limitation of Vth-based clamping.

4. **Rpd = 500kΩ is an ideal resistor.** In the actual design.cir, Rpd is a simple `500k` resistor, not a PDK device. If implemented as xhigh_po, it would have a temperature coefficient that further shifts the onset.

### What is concerning

1. **Onset at 150°C drops to 5.28V (TT) — only 280mV above the regulated PVDD of 5.0V.** This means the clamp starts conducting at normal operating voltage at high temperature, drawing 256µA of leakage. At FF 150°C, onset drops to 4.86V — below the regulated output. The clamp would fight the regulator, potentially preventing it from reaching 5.0V.

2. **The clamp NMOS (200µm total) has significant parasitic Cgs.** The v17 notes mention reducing the clamp from 2000µm to 400µm due to Cgs interaction with startup. The current 200µm still adds parasitic capacitance to PVDD (estimated ~0.5pF from Cgs alone). During fast transients, the Cgs feedthrough from the clamp gate can couple to PVDD.

3. **No ESD protection.** The README title mentions "ESD and transient protection" but this circuit provides no ESD protection. ESD events inject charge in nanoseconds — the MOS diode stacks and 500kΩ Rpd are far too slow. Proper ESD protection requires dedicated ESD clamp cells (e.g., GGNMOS, SCR, or dedicated ESD diodes).

### Industry comparison

Production overvoltage clamps in automotive ICs use:
- **True Zener diodes** (available in BCD processes like TSMC BCD, GF130BCD) — accurate, well-characterized, reliable
- **Bandgap-referenced active clamps** — a comparator monitors the output and engages a shunt regulator when OV is detected. More accurate than threshold-based clamps.
- **ESD-rated clamp cells** — separate dedicated structures for ESD, not shared with functional OV clamping

Sky130 lacks true Zener diodes, making this a process limitation rather than a design error. The MOS-based approach is the best available option, but it inherently has wider PVT variation than a true Zener.

### Recommendation

- Rename to "MOS Voltage Clamp."
- Accept that this block requires trimming for production and budget for it.
- Add a separate ESD protection structure (GGNMOS or snapback clamp) — do not rely on this circuit for ESD.
- Consider a bandgap-referenced active clamp if tighter onset accuracy is needed.
- Fix Rpd to be a PDK resistor device.

---

## Block 08: Mode Control

### Purpose
Sequences the regulator through POR → retention bypass → retention regulate → power-up bypass → active regulate modes based on BVDD voltage thresholds.

### Implementation
- **Resistor ladder:** 5 xhigh_po segments (total ~400kΩ, ~17µA Iq at 7V) from BVDD to GND, creating 4 tap points
- **Comparators:** 4 PVDD-powered CMOS inverter pairs with Schmitt trigger hysteresis (feedback NFETs with L=100µm)
- **Logic:** CMOS combinational gates (AOI22, AOI21, NAND+INV, buffers) generating bypass_en, ea_en, ref_sel, uvov_en, ilim_en, pass_off

### What is good

1. **Shared resistor ladder is area-efficient.** One ladder for four thresholds, rather than four separate dividers, saves area and current. Standard practice in multi-threshold detectors.

2. **Schmitt trigger hysteresis via feedback NFETs is clever.** The L=100µm NFETs provide very weak pull-down (nanoamps of current), creating a small but meaningful shift in the inverter trip point. This avoids the cross-talk problem that plagued the v12 design (PFET-to-tap hysteresis injecting current into the ladder). The approach is documented in some literature (e.g., Allen & Holberg, "CMOS Analog Circuit Design," on Schmitt triggers).

3. **Logic is purely combinational — no clock, no flip-flops.** For a power management controller that must work from DC, combinational logic is the right choice. There's no clock domain to worry about, and the outputs settle as soon as the comparators switch.

4. **16/16 specs pass at TT 27°C with 3.34% max threshold error.** The design works well at the nominal corner.

### What is questionable

1. **All logic is PVDD-powered, but PVDD doesn't exist during POR.** When BVDD is ramping from 0V and PVDD=0V, the CMOS logic has no supply. The inverter trip points are undefined. The comparators need PVDD to function, but PVDD is produced by the pass device, which is controlled by the mode logic output. This is a second chicken-and-egg problem (separate from the EA bootstrap). The design relies on the PFET pull-ups defaulting to a known state when PVDD=0V (all outputs LOW or HIGH depending on topology), but this is not guaranteed with floating supplies.

2. **L=100µm feedback NFETs.** These are extraordinarily long-channel devices — 100µm is unusual even for precision analog. The purpose is to make them very weak (essentially a resistor). But the channel resistance of such a long device will have enormous process variation. It would be simpler and more predictable to use an actual resistor.

3. **Only TT 27°C tested.** The README admits "Only TT 27°C tested. The inverter trip point (~1.93V) varies with corner and temperature, which will shift all thresholds." For an automotive design, this is a critical gap. The inverter trip point could shift ±300mV across PVT, shifting all four thresholds by a proportional amount divided by the tap ratio.

4. **The `vref` pin is declared but unused.** The mode_control subcircuit has `vref` in its port list (connected to `avbg` in the top level), but the internal circuit never references it. Dead pins are a source of confusion and potential ERC (electrical rule check) violations.

### What is concerning

1. **None of the mode control outputs are connected in the top-level integration.** As verified above:
   - `pass_off` → floating (should disable pass device during POR)
   - `bypass_en` → floating (should enable bypass switch)
   - `mc_ea_en` → floating (should enable/disable error amp)
   - `ref_sel` → floating (should select retention vs active reference)
   - `uvov_en` → connected to UV/OV comparator enable (this one IS used)
   - `ilim_en` → floating (should enable/disable current limiter)

   This means the entire mode control state machine — the block that sequences POR, retention, bypass, and active modes — **has no effect on the circuit behavior**. The error amp is always on, the pass device is never force-off, bypass mode doesn't exist, and the current limiter is always active. The LDO operates in "always active" mode regardless of BVDD voltage.

2. **This is arguably the most critical integration bug in the design.** The mode control exists, works correctly in isolation, but is simply not wired up. Without it:
   - POR behavior is undefined (no pass_off)
   - Retention and bypass modes don't exist
   - The EA is always active, potentially fighting PVDD during low-BVDD conditions
   - The system cannot handle cold-crank (BVDD dropping below regulation threshold) gracefully

### Industry comparison

Automotive LDOs universally implement power-up sequencing. TI's TPS7A series, Infineon's TLE4xxx, NXP's MC33xxx all have fully integrated mode control that gates the error amplifier, bypass switches, and protection circuits. A mode control block that exists but isn't connected is unprecedented — this is clearly an integration oversight, not an architectural decision.

### Recommendation

- **Wire up all mode control outputs** in the top-level integration. This is the single highest-priority fix.
- **Add PVT characterization** for all threshold voltages.
- **Replace L=100µm feedback NFETs** with resistors for predictability.
- Remove the unused `vref` pin.
- Address the PVDD-powered-logic-during-POR issue with a dedicated POR circuit or supply bootstrapping.

---

## Block 09: Startup Circuit

### Purpose
Bootstrap the regulator from a cold start. Solve the chicken-and-egg problem where the EA needs PVDD to operate but PVDD is produced by the EA-controlled pass device.

### Implementation (actual design.cir, v40)
Extremely simplified:
- **Rgate = 1kΩ:** Series resistor between EA output and pass device gate (isolation/damping)
- **ea_en = BVDD via 100Ω:** Error amplifier always enabled
- **Startup_done detector:** Resistive divider (788kΩ/212kΩ xhigh_po) + NFET + inverter — asserts HIGH when PVDD > ~3.3V
- **No active startup assistance.** The XMsu_pd gate pulldown was disabled (commented out) due to causing overshoot.

### What is good

1. **Simplicity.** The startup circuit does very little — the heavy lifting is done by the BVDD-powered error amplifier, which operates from the moment BVDD appears. With a BVDD-powered EA, the traditional startup problem is largely eliminated.

2. **Rgate = 1kΩ provides useful isolation.** It limits the gate charge/discharge rate, preventing the EA from slamming the pass device on or off. Combined with Cgs ≈ 1pF, the gate pole is at 1/(2π × 1kΩ × 1pF) ≈ 159MHz — well above the loop bandwidth, so it doesn't affect stability.

3. **The soft-start (Rss + Css in the top level) is the real startup mechanism.** The 100kΩ/22nF RC filter on the reference creates a 2.2ms ramp that prevents PVDD overshoot. This is simple, robust, and well-proven.

### What is questionable

1. **The README describes a completely different circuit than what is built.** The README talks about R_top + R_bot = 4.1MΩ + 900kΩ, MN_gate (gate pulldown switch), R_gate = 102kΩ, MN_pu (BVDD regulation assist), and 11 total components. The actual design.cir has 5 components (Rgate, Ren, two resistors, one NFET, two inverter MOSFETs, one pull-up resistor). The README describes a previous version (pre-v40) that was abandoned. This documentation mismatch is pervasive throughout the project.

2. **The startup_done signal is not used anywhere.** It's generated but goes to the top-level port and is not connected to any other block. Originally, it would have gated the handoff from startup to EA control, but since the EA is always on, startup_done serves no purpose.

3. **ea_en is permanently tied to BVDD.** Combined with the mode control mc_ea_en being disconnected, the error amplifier can never be disabled. This might cause issues when BVDD is very low (<3V) and the EA is trying to regulate with insufficient headroom.

### What is concerning

1. **2V overshoot (reported in Block 09 README, Spec T4).** At no-load, PVDD overshoots to 7V because the EA output is limited to PVDD (its supply rail) and can't turn the pass device fully off. The README explains this is a system-level limitation: "min pass device Vsg = BVDD − PVDD + headroom ≈ 2.7V → 80mA at no load → PVDD settles at ~5.96V." This is correct at the 50mA load condition (where it regulates to 5.02V), but the no-load overshoot is a real problem for applications that may have zero load at startup.

   Wait — the EA is powered from BVDD (not PVDD as the README states). Looking at the EA design.cir, the output stage (XMcs_n, XMcs_p) is powered from BVDD. So vout_gate can swing from 0V to ~BVDD. At BVDD=7V with PVDD at 5V, the gate should be able to reach 7V (turning the PFET off, since Vsg=0). Let me reconsider: if the EA output can reach BVDD, then it *can* turn off the pass device. The overshoot might be transient — during the ramp, the EA hasn't settled yet. The soft-start tau=2.2ms should handle this.

   Actually, the top-level README reports startup peak of 5.25V for 1V/µs ramp, which is within spec (<5.5V). The 2V overshoot reported in Block 09 README might be from an older version. This inconsistency is confusing.

2. **Pull-up resistor for det_n is 2MΩ xhigh_po.** The startup_done detector uses XR_pu (W=1µm L=2000µm ≈ 4MΩ). At BVDD=7V, this draws 7V/4MΩ = 1.75µA — a small but unnecessary constant drain since startup_done isn't used.

### Industry comparison

Most LDOs with input-powered error amplifiers don't need a separate startup circuit at all — the EA comes alive as soon as the input supply ramps. The soft-start RC on the reference is the standard mechanism for controlling output ramp rate. This is what TI, ADI, and Infineon do in their datasheets.

The v40 design effectively acknowledges this by stripping the startup circuit down to almost nothing. The remaining components (Rgate and startup_done detector) are ancillary.

### Recommendation

- Remove the startup_done detector if it's not used — it wastes current and area.
- Fix the README to match the actual circuit.
- If overshoot at no-load is truly 2V, the soft-start time constant may need to be increased, or a load-independent startup sequence is needed.

---

## Block 10: Top-Level Integration

### Purpose
Wire all 11 blocks together into a complete LDO regulator.

### Implementation
The top-level netlist connects:
- Pass device, error amp, feedback network, compensation (empty), current limiter, UV/OV comparators, zener clamp, mode control, startup circuit, and one level shifter (for external enable)
- Adds soft-start RC (Rss=100kΩ, Css=22nF, tau=2.2ms)
- Adds output capacitors (200pF internal + 1µF external)

### What is good

1. **The soft-start RC is clean and effective.** Rss=100kΩ in series with Css=22nF on the reference input creates a smooth ramp. This is simple, robust, and PVT-independent (RC product is constant if both are the same material).

2. **19/19 specs pass at TT 27°C.** The regulator regulates. Output accuracy is excellent (5.000V). Load regulation is outstanding (0.008 mV/mA). Line regulation is good (0.92 mV/V). PSRR is excellent (-67.5dB DC). The design works.

3. **The 1µF external cap provides rock-solid stability.** PM > 125° at all loads. No oscillation risk whatsoever.

### What is questionable

1. **Css = 22nF in design.cir, but the README says 10nF in some places and 22nF in others.** The design.cir is ground truth: Css=22nF, so tau=2.2ms. The README's first mention says "Css=10nF (tau=1ms)" but the architecture section says "Rss=100k, Css=22nF → tau=2.2ms." Yet another documentation inconsistency.

2. **The 1µF external cap makes this NOT a "capless" LDO.** The README and Block 03 documentation discuss capless LDO techniques, but this design absolutely requires the external cap. Without it, stability would collapse (PM → negative) and transient performance would be unacceptable (ΔV = 10mA × 1µs / 200pF = 50V — obviously clipped, but the point stands). The design should be honestly characterized as an "external capacitor LDO."

3. **UGB of 1.9kHz is extremely low for a 50mA LDO.** For comparison:
   - TI TPS7A4700: UGB ~300kHz with 1µF
   - ADI ADP150: UGB ~200kHz with 1µF
   - Literature (Rincon-Mora): UGB should be >100kHz for acceptable transient response

   The 1.9kHz UGB means the loop can only suppress disturbances below ~2kHz. Above that, the LDO is essentially open-loop. The excellent transient results (27mV undershoot for 1→10mA) are almost entirely due to the 1µF cap absorbing the charge, not the loop responding.

4. **Phase margin of 125–161° is far from optimal.** In control theory, optimal transient response occurs at PM ≈ 60–70°. At 161°, the step response is aperiodic but extremely slow — the loop is so over-damped that it barely responds. This is "stable" in the way that a car going 5 mph is "safe" — technically true, but not useful.

### What is concerning

1. **Mode control outputs are disconnected (covered in Block 08 section).** This is the most critical integration bug. The regulator has no POR protection, no bypass mode, no retention mode, and no ability to disable the error amp or current limiter.

2. **BVDD domain coupling.** The error amp Stage 1 (diff pair) is powered from BVDD. Any noise on BVDD directly modulates the tail current and common-mode of the diff pair. The loop gain provides -67.5dB PSRR at DC, but at frequencies above the 1.9kHz UGB, PSRR degrades rapidly. At 10kHz it's -51dB, at 100kHz it's probably -30dB or worse. For an automotive supply with significant switching noise (alternator, DC-DC converters), this could be problematic.

3. **Quiescent current of 269µA is high for a 50mA LDO.** For comparison:
   - TI TPS7A20: 1µA Iq
   - ADI ADP150: 9µA Iq
   - Maxim MAX38902: 20µA Iq
   - This design: 269µA Iq

   269µA is acceptable for an automotive LDO (where battery capacity is large), but it's 10–100x higher than state-of-the-art. The main contributors are: EA bias (~86µA), feedback divider (~10µA), mode control ladder (~17µA), and the pass device leakage/bias currents.

4. **No Monte Carlo results at the system level.** The 19/19 pass is at TT 27°C nominal. Real silicon has mismatch and process variation. The ±3.5% output accuracy spec requires MC verification with at least 500 runs. The Block 00 README mentions "MC 500 runs, sigma x2" for phase margin, but I see no system-level MC for output voltage accuracy.

5. **The EA is instantiated with pvdd as a port, but the EA actually uses bvdd for power.** Looking at the EA subcircuit: `XEA vref_ss vfb ea_out pvdd gnd ibias ea_en bvdd error_amp`. The port mapping is: vref=vref_ss, vfb=vfb, vout_gate=ea_out, pvdd=pvdd, gnd=gnd, ibias=ibias, en=ea_en, bvdd=bvdd. Inside the EA, pvdd is used only for the diff pair source — wait, looking at the EA subcircuit again, pvdd is not used internally at all! The diff pair and tail are connected to `bvdd`. The `pvdd` pin in the error_amp subcircuit is declared but unused in the v7 design.cir. This is a vestige of the old PVDD-powered topology.

---

## System-Level Topics

### Overall Architecture: Is BVDD-Powered EA the Right Choice?

**The case for BVDD-powered EA:**
- Eliminates startup deadlock (EA works from the moment BVDD exists)
- Allows the EA output to swing up to BVDD, fully turning off the pass device
- Simplifies the startup circuit (no separate bootstrap path needed)

**The case against:**
- BVDD noise couples directly into the EA — PSRR depends entirely on loop gain
- The EA must operate across the full BVDD range (5.4–10.5V for Sky130), requiring HV devices with lower gm and higher noise
- Power consumption scales with BVDD (the EA draws current from the high-voltage rail)

**What does the literature say?**
Most published LDO architectures power the error amplifier from the regulated output (PVDD) or from a separate low-voltage supply, NOT from the input supply. The reason is PSRR — an EA powered from the input supply acts as a common-mode-to-differential-mode converter for input noise. However, some automotive LDOs (TDK-Micronas, some Infineon designs) do use input-powered EAs for exactly the startup robustness reason cited here.

**Verdict:** The BVDD-powered EA is a pragmatic choice for an automotive LDO where startup robustness matters more than PSRR. It's not the standard approach, but it's defensible. The PSRR numbers (-67.5dB DC) confirm that the loop gain is sufficient to suppress BVDD noise at low frequencies. The weakness is high-frequency PSRR, which is inherently limited.

### Compensation Strategy: Inner Miller + 1µF External Cap

**What is actually implemented:** 2pF inner Miller + 1µF external cap. The outer Miller (Block 03) is removed.

**Is this standard?** No. Standard external-cap LDOs use 20–50pF Miller compensation inside the EA to split the internal poles, then the external cap provides the dominant pole. The 2pF here provides almost no pole-splitting. The system works because the 1µF cap pushes the UGB so low (1.9kHz) that both internal EA poles are well above UGB and don't affect phase margin. But this makes the loop extremely sluggish.

**The Block 03 README mentions "inner + outer Miller" as the intended strategy, but this was abandoned.** The design tried outer Miller (30pF Cc + 5kΩ Rz from ea_out to pvdd) but found it redundant because "UGB=170Hz with it." That's true — adding outer Miller on top of 1µF further reduces bandwidth. But the solution should have been to reduce the 1µF cap or increase the inner Miller, not to remove all compensation and rely on the external cap alone.

**Recommendation:** Increase inner EA Cc to 20–30pF, reduce external cap to 100nF–470nF, and target UGB of 100–500kHz. This would dramatically improve transient response while maintaining adequate phase margin (55–70°).

### PVT Robustness: The .op Bi-stable Issue

**The problem:** ngspice's .op solver finds a bi-stable equilibrium where the pass device is fully ON and PVDD ≈ BVDD at some PVT corners (SS, FF, SF). Transient simulation from zero initial conditions correctly finds the regulated operating point.

**Is this a real concern?** Yes and no:
- **In simulation:** It's a known ngspice limitation. The .op solver doesn't handle feedback loops with multiple equilibria well. Transient simulation with realistic initial conditions (PVDD=0, BVDD ramping) always converges to the correct state.
- **In silicon:** The physical circuit starts from PVDD=0V and ramps up. It will always find the regulated equilibrium if the loop is designed correctly. The bi-stable point (PVDD≈BVDD) is unstable — any perturbation pushes the system back to regulation.
- **However:** If the mode control is not wired (which it isn't), there's no mechanism to force the pass device off during POR. The EA is always on, which should prevent bi-stability, but if the EA output saturates at an unfortunate level during power-up, the system could latch in the wrong state.

**Verdict:** The .op bi-stable issue is primarily a simulation artifact, not a silicon risk — PROVIDED the startup and mode control are properly implemented. Since mode control is disconnected, the risk is slightly elevated.

### The 1µF External Cap Dependency

**Can this be a capless LDO?**
No, not with the current architecture. Here's why:

1. **The error amplifier is a simple two-stage OTA.** Capless LDOs require either class-AB output stages (Milliken et al., JSSC 2007), flipped voltage followers (Hazucha et al., JSSC 2005), or current-buffer compensation (Leung et al., JSSC 2003). These topologies create a dominant pole at the gate of the pass device rather than at the output, allowing stability without an external cap.

2. **The pass device gm at light load is very low.** At Iload=100µA, gm_pass ≈ 50µA/V. The output pole without external cap is at gm_pass / (2π × 200pF) ≈ 40kHz. With the EA two-stage poles also in the tens-of-kHz range, the system would have three poles close together — inherently unstable.

3. **The 200pF internal Cload is marginal.** For a capless LDO, internal Cload of 200pF is on the low side. Published capless designs typically use 100pF–6nF internal caps (Milliken: 6nF; Hazucha: 600pF).

**What does the literature say about capless LDO bandwidth?**
Capless LDOs need UGB > 1MHz to handle load transients with only internal capacitance. The current design's 1.9kHz UGB is 500x too low for capless operation.

**Verdict:** The 1µF external cap is non-negotiable with the current architecture. If capless operation is ever required, the EA must be redesigned from scratch.

### Current Limiter Cascode: Is Tying cas_bias to PVDD Standard?

**No.** Tying the cascode gate to the output being regulated means:
- During normal regulation (PVDD ≈ 5V): Works fine. Vgs_cas ≈ PVDD – cas_mid ≈ 5V – 5.7V = -0.7V (just at threshold).
- During short circuit (PVDD ≈ 0V): Vgs_cas ≈ 0V. The cascode turns off. The sense path reverts to un-cascoded behavior, losing the Vds matching that the cascode was supposed to provide.

**Standard practice** is to bias the cascode from a fixed reference (e.g., a fraction of BVDD derived from a resistive divider or bias generator). This ensures the cascode operates correctly under all conditions, including fault conditions.

### Area Estimation

Based on the devices and component values:

| Block | Dominant Component | Estimated Area |
|-------|-------------------|---------------|
| 00 Error Amp | 2pF MIM cap (~10µm × 10µm), diff pair (80µm × 4µm × 2 × 2 sides) | ~5,000 µm² |
| 01 Pass Device | 10 × 50µm × 0.5µm m=2 (with guard rings) | ~15,000 µm² |
| 02 Feedback | 536µm × 3µm + 174µm × 3µm poly resistors | ~2,200 µm² |
| 03 Compensation | EMPTY | 0 µm² |
| 04 Current Limiter | 4× clamp PMOS (50µm × 0.5µm × m=2), sense chain | ~3,000 µm² |
| 05 UV/OV | Ideal resistors (need PDK conversion), comparators | ~2,000 µm² |
| 06 Level Shifter | Small CMOS devices | ~500 µm² |
| 07 Zener Clamp | 200µm clamp NFET, diode stacks | ~5,000 µm² |
| 08 Mode Control | 400kΩ ladder, 64 devices | ~8,000 µm² |
| 09 Startup | Rgate + 1MΩ resistors | ~3,000 µm² |
| 10 Top Level | Cload 200pF MIM + Css 22nF | ~120,000 µm² |
| | **External 1µF** | **Off-chip** |
| | **TOTAL** | **~165,000 µm² ≈ 0.165 mm²** |

The 22nF soft-start cap (Css) dominates the on-chip area. At ~500 µm²/pF for MIM caps in Sky130, 22nF would require 11,000,000 µm² = 11 mm² — which is obviously unrealizable on-chip. **Css must be an off-chip component** or must be replaced with a current-source-based soft-start (which uses no cap). The spec says total area ~0.065 mm², which is only achievable if Css is off-chip or replaced.

Similarly, the 200pF Cload requires ~100,000 µm² = 0.1 mm². The spec says total area including pass device is 0.065 mm². **This does not add up.** Either the area spec is wrong, or the 200pF is also off-chip, or the MIM cap density is much higher than I estimated.

---

## Summary of Critical Findings

### Showstoppers (must fix)

1. **Mode control outputs are disconnected.** The regulator has no POR protection, no bypass mode, no retention mode. This defeats the purpose of having mode control. (Block 08 / Block 10)

2. **Documentation is pervasively inconsistent with design.cir files.** READMEs describe circuits that don't exist, with numbers from old versions. Component values cited in documentation (Cc=98pF, Css=10nF) don't match actual netlists (Cc=2pF, Css=22nF). Comments in design.cir describe features (cascodes, level shifters) that were removed. Any engineer trying to review or modify this design based on the documentation will be misled.

3. **Compensation subcircuit is empty with a misleading README.** Block 03 has a 150-line README with detailed performance tables describing components that don't exist.

### Significant Issues

4. **Current limiter has 3.1x PVT spread** (44–137mA). At SS 150°C, it allows 137mA — potential SOA violation. At FF -40°C, it trips at 44mA — may interfere with rated 50mA load. (Block 04)

5. **Zener clamp fails 40% of PVT corners.** Requires trimming for production. At FF 150°C, onset drops below PVDD, fighting the regulator. (Block 07)

6. **UGB of 1.9kHz is 100x lower than industry practice** for a 50mA LDO. Transient performance relies entirely on the 1µF external cap. (Block 03 / Block 10)

7. **UV/OV comparators use ideal resistors** instead of PDK devices. Results are optimistic. (Block 05)

8. **22nF soft-start cap is unrealizable on-chip.** Must be off-chip or replaced with a current-source-based approach. (Block 10)

### Minor Issues

9. Error amp comments describe a non-existent cascode (Block 00)
10. Startup_done signal is generated but unused (Block 09)
11. EA pvdd pin is declared but unused (Block 00 / Block 10)
12. No filter cap on feedback node (Block 02)
13. Quiescent current (269µA) is 10–100x higher than state-of-the-art (Block 10)
14. No ESD protection (Block 07)

### What is Genuinely Good

- BVDD-powered EA architecture for startup robustness — pragmatic choice
- PMOS diff pair with long-channel devices — correct and well-sized
- Pass device sizing — compact and efficient for the spec
- Feedback network — proper matched poly resistors at W=3µm
- Soft-start concept — simple RC works across PVT
- Schmitt trigger hysteresis in mode control — clever approach
- Long-channel MOS clamp stack — creative solution to TC problem
- Honest documentation of known limitations (current limiter PVT, zener corners)

### Overall Verdict

This is a **functional prototype** that regulates correctly at the nominal corner. The fundamental architecture (BVDD-powered EA + external cap + sense-mirror current limiter) is sound. However, it has significant integration issues (disconnected mode control, inconsistent documentation) and relies entirely on a large external capacitor for stability and transient performance.

For a learning project or proof-of-concept, it demonstrates competent analog design fundamentals. For a production automotive IC, it would need: mode control integration, proper compensation tuning, temperature-compensated current limiting, PDK-accurate components throughout, and comprehensive PVT/MC verification.

The single most impactful improvement would be to **wire up the mode control outputs** and **increase the inner EA Miller cap to 20-30pF while reducing the external cap to 100nF**. This would transform the LDO from a sluggish external-cap-dependent prototype into a responsive, properly compensated regulator.
