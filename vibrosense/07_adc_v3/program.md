# Block 07: 8-bit SAR ADC v3 — Full Redesign

## Context: Why v3 Exists

v2 was independently reviewed and simulated. The review found:

1. **CRITICAL: No DAC reset between conversions.** The SAR logic did not force DAC switches to GND during the sample phase. After the first conversion, bit registers held their values, so all subsequent conversions produced code 255. The ADC was a one-shot device.
2. **Fake performance numbers.** `simulation_results.json` reported ENOB=7.93 from a Python behavioral model (`SAR_ADC_Model` class using `np.random`), not from ngspice. This violates the project's own rules.
3. **Weak comparator.** A continuous two-stage diff-amp was used to avoid StrongARM timing issues. It had 15mV systematic offset (3 LSB), failed at SS corner (20 LSB error), and completely failed at SF corner (code 255 for all inputs).
4. **3/5 corners failed.** Only TT, FF, FS produced valid results. SS had 20 LSB error (not 4 as claimed). SF was totally broken.
5. **Wakeup time was 105us, not 5us.** The README cherry-picked bias settling time and ignored the 100us conversion time.

v3 starts from scratch. You may reuse the v2 cap DAC design (which was solid) and the SKY130 model files, but the comparator, SAR logic, and testbenches must be redesigned.

---

## NON-NEGOTIABLE DESIGN RULES

### Rule 1: Multi-Conversion is the First Test, Not the Last

The FIRST thing you verify after closing the loop is: **does the ADC produce correct codes for TWO consecutive conversions at DIFFERENT input voltages?**

Not one conversion. Two. If conversion 2 gives the same code as conversion 1 regardless of input, you have a reset bug. This was v2's fatal flaw — it passed the single-conversion test but failed every multi-conversion test.

**Acceptance criterion:** Run 5 consecutive conversions at Vin = {0.0, 0.3, 0.6, 0.9, 1.1}V. All codes must be within +/-5 LSB of ideal. Transfer function must be monotonic.

### Rule 2: DAC Must Reset During Sampling

During the sample phase, ALL DAC bottom-plate switches must connect to GND. This is fundamental to charge redistribution SAR operation:

```
SAMPLE PHASE:  all bottom plates → GND,  sample switch → CLOSED,  Vtop = Vin
HOLD PHASE:    sample switch → OPEN,    bottom plates → controlled by SAR
```

If your SAR logic uses OR gates to combine "bit register" with "tentative bit" for DAC control (`d7 = b7q OR s2`), you MUST also AND the result with NOT(sample_phase) to force all bits to 0 during sampling:

```
d7 = (b7q OR s2) AND NOT(s1)
```

If you don't do this, the DAC retains previous conversion values during sampling, and the initial charge state is wrong.

**Verify this explicitly:** After conversion 1, print DAC switch states during conversion 2's sample phase. They must ALL be 0.

### Rule 3: No Python Behavioral Models for ADC Performance

Same as v2 Rule 1 — it bears repeating because v2 violated it.

- DNL, INL, ENOB, SFDR, missing codes — ALL must come from ngspice transient simulation of the full circuit with SAR feedback loop closed.
- Python is ONLY for post-processing ngspice output (parsing wrdata, computing FFT from captured codes, plotting).
- If you write `class SAR_ADC_Model` or `def convert(self, vin)` — STOP. Delete it.
- `simulation_results.json` must contain only numbers that trace to an `ngspice -b` command.

### Rule 4: Every Transistor Must Be SKY130

- Switches: real `sky130_fd_pr__nfet_01v8__model` / `pfet_01v8__model` TGs
- Comparator: real SKY130 devices
- Logic gates: transistor-level CMOS or XSPICE digital primitives (both acceptable)
- Capacitors: ideal `C` elements are acceptable (documented approximation) since MIM models aren't in the minimal PDK

### Rule 5: Honest Numbers or No Numbers

- If a spec fails, report the actual number and say FAIL.
- If a corner fails, say which one and why.
- If you can't measure something (e.g., Monte Carlo requires statistical models you don't have), say "NOT MEASURED" — do not synthesize a number from a behavioral model.
- README numbers must match what `ngspice -b` actually prints. Copy the `.meas` output.

### Rule 6: Wakeup Time = Time From Sleep De-Assert to First Valid Output

Not "bias settling time." Not "time until comparator is ready." The spec is: the MCU de-asserts SLEEP, and how many microseconds later does VALID assert with a correct code?

This includes: bias settling + clock synchronization + full conversion (10 clock cycles).

At 100kHz clock, 10 cycles = 100us. So wakeup < 10us is impossible at 100kHz. Options:
- Use a faster startup clock (1MHz for first conversion after wakeup, then drop to 100kHz)
- Or honestly report that wakeup = ~105us at 100kHz and flag the spec as unachievable at this clock rate
- Or redefine wakeup as "time from sleep de-assert to comparator ready" and document this clearly

### Rule 7: Comparator Must Work at ALL 5 Corners

The v2 comparator (continuous diff-amp) failed at SS and SF corners. The comparator is the ADC's precision element — if it doesn't work across corners, the ADC doesn't work.

Requirements:
- Input-referred offset < 5 mV (< 1 LSB = 4.69 mV) at ALL corners
- Must resolve 1 LSB (4.69 mV) within half a clock period (5us at 100kHz)
- Must work from -40C to 85C at all process corners

Design options (in order of recommendation):
1. **Pre-amp + StrongARM latch** — v2 abandoned this due to timing issues but this is the standard approach. The timing issues are solvable (gate comp_clk properly).
2. **Two-stage Miller-compensated OTA with auto-zero** — more complex but eliminates offset
3. **Continuous diff-amp with MUCH wider devices** — v2's approach but with 4x wider PMOS mirrors and longer channel devices. Simplest fix but still has systematic offset.

Whatever you choose, verify offset at ALL 5 corners with a DC sweep before integrating.

---

## Specifications

| # | Parameter | Target | Measurement Method | Priority |
|---|-----------|--------|-------------------|----------|
| 1 | ENOB | >= 7.0 bits | FFT of 1024 codes from ngspice transient | MUST |
| 2 | Max \|DNL\| | < 0.5 LSB | Code density from ngspice slow-ramp | MUST |
| 3 | Max \|INL\| | < 0.5 LSB | Cumulative DNL from ngspice | MUST |
| 4 | Missing codes | 0 | Histogram, no zero bins in codes 1-254 | MUST |
| 5 | Sample rate | >= 10 kSPS | Architecture (10 clk x 100 kHz) | MUST |
| 6 | Active power | < 100 uW | `.meas tran` I(VDD) during conversion | MUST |
| 7 | Sleep power | < 500 nW | `.meas tran` I(VDD) in sleep mode | MUST |
| 8 | Wakeup time | Honestly reported | `.meas tran` TRIG sleep_n / TARG valid | REPORT |
| 9 | Input range | 0 - 1.2V | Transfer function from multi-code test | MUST |
| 10 | Corners | 5/5 pass (code within +/-5 LSB) | TB1 at all 5 corners | MUST |
| 11 | Multi-conv | Monotonic TF, 5+ consecutive correct | Multi-code test, all codes correct | MUST |

Note: Wakeup is changed to REPORT (honestly measure and report) instead of MUST PASS, since at 100kHz clock it's physically limited to ~105us.

---

## Architecture

### Top Level

```
Vin ─── [CMOS TG Sample Switch] ─── Vtop (shared top plate)
         Wn=5u, Wp=10u, L=0.15u          |
                               +----------+----------+
                             128C       64C  ...    1C   Cdummy(1C)
                               |          |          |      |
                            [TG sw7]  [TG sw6] ... [TG sw0] GND
                            Vref/GND  Vref/GND     Vref/GND
                               |
                          +----+----+
                          |Comparator|  <-- inp=Vtop, inn=Vref
                          | PreAmp + |
                          | Latch    |
                          +----+----+
                               |  comp_out
                          +----+----+
                          |SAR Logic |---- D[7:0]
                          |XSPICE+   |---- VALID
                          |CMOS gates|---- SAMPLE
                          +----+----+
                               |
                         sw[7:0], sw[7:0]_b
                               |
                       DAC bottom-plate switches
```

### Cap DAC (reuse from v2 — this was solid)

- 8-bit binary-weighted: 128C, 64C, 32C, 16C, 8C, 4C, 2C, 1C + 1C dummy
- Cunit = 20 fF, total = 5.12 pF
- CMOS TG switches: Wn=1u, Wp=2u, L=0.15u (Ron ~250 ohm, settling ~6ns)
- 10G ohm leakage resistors for DC convergence
- Bottom-plate switching between Vref (1.2V) and GND

### Comparator (REDESIGN REQUIRED)

v2 used a continuous diff-amp that had:
- 15 mV systematic offset (3 LSB)
- No way to resolve better than ~3 LSB accuracy
- Failed at SS (94mV offset!) and SF corners
- Always-on power draw even when not evaluating

Recommended approach: **Pre-amplifier + StrongARM latch**

The pre-amp reduces the input-referred offset of the StrongARM by its gain.

```
Stage 1: NMOS diff pair + PMOS active load (gain ~20-40)
  - Input pair: W=8u, L=1u (large area for low random offset)
  - Mirror load: W=4u, L=1u (WIDER than v2's 2u — fixes SF corner)
  - Tail current: W=4u, L=2u, Ibias ~5uA

Stage 2: StrongARM latch
  - Clocked: evaluates on comp_clk falling edge, resets on rising edge
  - Input pair: W=4u, L=0.5u
  - Cross-coupled NMOS latch: W=1u, L=0.15u
  - Cross-coupled PMOS latch: W=1u, L=0.15u
  - Reset PMOS on ALL internal nodes (dn, dp, outp, outn): W=2u, L=0.15u
  - CRITICAL: Reset switches must discharge dn, dp to VDD on every reset
    (v2 noted this as lesson #4 — latch cannot reverse without reset)
```

**Timing (CRITICAL — this is where v2 gave up):**
```
CLK HIGH phase:
  - DAC switches settle (new bit position)
  - StrongARM in RESET (all internal nodes pre-charged)
  - comp_clk = LOW

CLK LOW phase:
  - comp_clk = HIGH → StrongARM evaluates
  - Vtop is stable (DAC settled during HIGH phase)
  - Latch resolves to rail-to-rail output
  - Output valid within ~1-2us

Next CLK rising edge:
  - comp_clk goes LOW → latch enters RESET
  - DFF captures latch output on rising edge (before reset clears it)
  - SAR logic updates bit register
  - DAC switches change to next bit position
```

The key insight v2 missed: **the DFF must capture on the clock edge BEFORE the latch resets.** Use the non-inverted clock for the DFF and the inverted clock for the latch. Or add a TG sample-and-hold between latch output and DFF input.

If StrongARM timing proves too difficult, fall back to the continuous diff-amp BUT:
- Increase PMOS mirror to W=4u or 6u (fixes SF corner)
- Increase input pair to W=16u, L=2u (reduces offset at SS)
- Accept ~10mV offset as a known limitation and document it

### SAR Logic

Use hybrid XSPICE DFF + transistor-level CMOS gates (v2 approach was fine, just fix the reset bug).

**State machine:** 10-state one-hot shift register
- IDLE → S1(SAMPLE) → S2(BIT7) → S3(BIT6) → ... → S9(BIT0) → IDLE

**CRITICAL additions vs v2:**
1. **DAC reset during sample:** `d_k = (b_k_q OR s_{k+2}) AND NOT(s1)`
2. **Bit register reset:** Consider clearing all bit DFFs when entering IDLE or S1
3. **comp_clk gating:** `comp_clk = NOT(clk) AND eval_active` (same as v2, this was correct)

### Power Gating

PMOS header on comparator supply:
- W=10u, L=0.15u
- Controlled by sleep_n signal
- When sleep_n=LOW: comparator powered off, leakage only

---

## Required Testbenches (in execution order)

### TB0: Comparator Standalone Verification

**Run FIRST, before integrating anything.**

```spice
* DC sweep: offset measurement
.dc Vinp 0.55 0.65 0.1m
.meas dc vos FIND v(inp) WHEN v(outp)=0.9   * crossover point

* Transient: 1-LSB step response
Vstep inp 0 PWL(0 0.595 5u 0.595 5.01u 0.6047)   * 4.7mV step (1 LSB)
.tran 10n 20u
.meas tran t_decision TRIG v(inp) val=0.6 rise=1 TARG v(outp) val=0.9 rise=1
```

Run at ALL 5 corners. If offset > 5mV at any corner, fix the comparator BEFORE proceeding.

### TB1: Single Conversion (Vin=0.47V)

Standard single-conversion test. Expected code ~156 (complement code).
Must show vtop staircase converging to Vref.

### TB1b: Two Consecutive Conversions (THE v2 KILLER)

**This is the test that caught v2's fatal bug. Run it IMMEDIATELY after TB1.**

```
Conversion 1: Vin = 0.47V → expect code ~156
Conversion 2: Vin = 0.90V → expect code ~64
```

If conversion 2 gives code 255 or the same as conversion 1, you have the DAC reset bug.

Also verify during conversion 2's sample phase:
- vtop = 0.9V (sample switch tracking)
- ALL sw[7:0] = 0V (DAC reset to GND)

### TB2: Multi-Code Transfer Function (13 input voltages)

Vin = {0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2}V

Read ALL 8 bits at each voltage. Compute code. Verify:
- Codes are monotonically decreasing (complement code: higher Vin → lower code)
- Each code is within +/-5 LSB of ideal: code_ideal = round((Vref - Vin) / Vref * 256)
- No missing major transitions (e.g., code must cross 128 near Vin=0.6V)

### TB3: DNL/INL via Code Density

Slow ramp from 0V to 1.2V with continuous conversion.
Minimum 2048 conversions (8 per code on average).

Use 1 MHz clock to keep simulation time reasonable (~2ms sim → ~5 min ngspice).
Document that production ADC runs at 100kHz but DNL/INL measurement uses accelerated clock.

Post-process with Python: parse wrdata, build histogram, compute DNL = (H_k / H_ideal) - 1, INL = cumsum(DNL).

### TB4: ENOB via FFT

Coherent sine input: fin = fs * M / N, where M=501 (prime), N=1024, fs=1MHz (accelerated).
fin = 489.26 kHz (or adjust M to get a reasonable frequency).

Actually, for a 10kSPS ADC, use fs=10kSPS and fin = fs*M/N with smaller N if sim time is too long.
Or use accelerated 1MHz clock.

Post-process with Python: FFT, compute SNDR, ENOB = (SNDR - 1.76) / 6.02.

### TB5: Active Power

`.meas tran Iavg AVG i(VDD) FROM=15u TO=105u`
Pavg = -Iavg * 1.8

### TB6: Sleep Power

sleep_n = 0, clk = 0, convert = 0.
`.meas tran Isleep AVG i(VDD) FROM=10u TO=100u`
Psleep = -Isleep * 1.8

### TB7: Wakeup Time

Measure from sleep_n rising edge to valid assertion.
Report the ACTUAL number (will be ~105us at 100kHz).
If you implement fast-start (1MHz clock for first conversion after wakeup), measure that too.

### TB8: Corner Analysis

Run TB1 (single conversion) at all 5 corners: TT, SS, FF, SF, FS.
Also run TB1b (two consecutive conversions) at all 5 corners to verify reset works everywhere.

All corners must produce code within +/-5 LSB of expected.
If a corner fails, document why and propose a fix.

---

## Design Flow (Step by Step)

### Phase 1: Foundation (get the PDK models working)

1. Copy SKY130 model files from `../07_adc/models/` and lib files
2. Verify models work with a simple inverter VTC simulation
3. Set up directory structure:
   ```
   07_adc_v3/
   ├── models/               (SKY130 BSIM4 model files)
   ├── sky130_v3.lib.spice   (library file referencing models)
   ├── v3_comparator.spice   (comparator subcircuit)
   ├── v3_cap_dac.spice      (cap DAC subcircuit)
   ├── v3_sar_logic.spice    (SAR logic subcircuit)
   ├── v3_tb_*.spice         (testbenches)
   ├── program.md            (this file)
   └── README.md             (results)
   ```

### Phase 2: Comparator Design + Verification

1. Design comparator (pre-amp + StrongARM, or improved continuous diff-amp)
2. Run DC sweep at all 5 corners — measure offset
3. Run transient 1-LSB step — measure decision time
4. Iterate sizing until offset < 5mV at all corners
5. **COMMIT:** `design(sar_adc_v3): comparator verified — offset < Xmv at all 5 corners`

### Phase 3: DAC + SAR Logic

1. Copy v2 DAC (it was good) — or build from scratch
2. Build SAR logic with the reset fix from day one
3. Test SAR logic standalone: apply known comp_out sequence, verify DAC switch sequence
4. **COMMIT:** `design(sar_adc_v3): DAC and SAR logic with sample-phase reset`

### Phase 4: Close the Loop

1. Connect comparator + DAC + SAR logic + sample switch
2. Run TB1 (single conversion) — debug until correct code appears
3. **IMMEDIATELY** run TB1b (two consecutive conversions) — verify DAC reset works
4. Run TB2 (multi-code) — verify monotonic transfer function
5. **COMMIT:** `design(sar_adc_v3): closed-loop verified — multi-code monotonic`

### Phase 5: Full Characterization

1. Run TB5, TB6, TB7 (power, sleep, wakeup)
2. Run TB8 (all 5 corners) — both single and dual conversion
3. Run TB3 (DNL/INL) — may take 5-30 min in ngspice
4. Run TB4 (ENOB via FFT) — may take 5-20 min
5. **COMMIT:** `design(sar_adc_v3): full characterization — TB1-TB8 results`

### Phase 6: Documentation

1. Write README.md with ALL results from ngspice
2. Every number must trace to an `ngspice -b` command
3. Include specification summary table with PASS/FAIL
4. Include honest assessment of limitations
5. **COMMIT:** `design(sar_adc_v3): documentation with honest results`

---

## What You Can Reuse from v2

| Component | Reuse? | Notes |
|-----------|--------|-------|
| Cap DAC (`v2_cap_dac_8b.spice`) | YES | Solid design, proper TG switches |
| SKY130 models (`models/`) | YES | Full 63-bin BSIM4, all 5 corners |
| Library file (`sky130_v2_nosubckt.lib.spice`) | YES | References standalone model files |
| CMOS gate subcircuits (NAND, NOR, INV, AND, OR) | YES | Correct implementations |
| Comparator (`v2_strongarm_comp.spice`) | NO | Redesign — too much offset, fails at SS/SF |
| SAR logic (`v2_sar_logic.spice`) | PARTIAL | Reuse structure, must add DAC reset |
| Testbenches | NO | Rewrite — v2 testbenches didn't catch the reset bug |
| `simulate_adc.py` | NO | Delete this. It's the behavioral model that produced fake numbers |
| `simulation_results.json` | NO | Already deleted. Regenerate from ngspice only |

---

## Anti-Patterns (things v2 did wrong — do NOT repeat)

1. **Testing only one conversion.** v2 ran TB1 (one conversion), saw it work, and assumed multi-code worked. It didn't. Always verify at least 2 consecutive conversions early.

2. **Using Python behavioral model for ENOB/DNL/INL.** The `SAR_ADC_Model` class with `np.random` noise produced beautiful ENOB=7.93. The actual circuit couldn't even do two conversions.

3. **Choosing continuous comparator to avoid timing complexity.** The diff-amp eliminated StrongARM timing issues but introduced 15mV offset and corner failures. The timing issues are solvable; the offset isn't (without auto-zero).

4. **Claiming wakeup = 5us by ignoring conversion time.** Wakeup means "time to first valid output," not "time for bias to settle."

5. **Claiming SS corner = 4 LSB error when it's actually 20 LSB.** Either the previous simulation used different model files, or the result was misread. Always re-run and verify.

6. **Not resetting DAC during sampling.** The OR gate `d7 = b7q OR s2` is correct for tentative bit setting, but without AND-ing with NOT(s1), the DAC retains previous values during sampling.

---

## Simulation Runtime Budget

| Testbench | Sim Time | Expected Runtime | Notes |
|-----------|----------|-----------------|-------|
| TB0 (comp DC sweep) | DC | ~10s per corner | 5 corners = ~1 min |
| TB0 (comp transient) | 20us | ~5s | Quick |
| TB1 (single conv) | 150us | ~30s | |
| TB1b (two conv) | 260us | ~45s | |
| TB2 (13 conv) | 1.6ms | ~3 min | |
| TB3 (DNL/INL, 2048 conv @ 1MHz) | 2ms | ~5-15 min | Accelerated clock |
| TB4 (FFT, 1024 conv @ 1MHz) | 1ms | ~3-10 min | Accelerated clock |
| TB5 (active power) | 130us | ~30s | |
| TB6 (sleep power) | 100us | ~10s | |
| TB7 (wakeup) | 200us | ~30s | |
| TB8 (5 corners x TB1+TB1b) | 5 x 410us | ~5-8 min | |
| **TOTAL** | | **~30-60 min** | |

This is normal and expected. Do NOT shortcut with behavioral models.

---

## Definition of Done

**The ADC is "done" when ALL of the following are true:**

- [ ] Comparator offset < 5 mV at all 5 corners (TB0)
- [ ] Single conversion produces correct code at TT (TB1)
- [ ] Two consecutive conversions produce correct codes (TB1b)
- [ ] Multi-code transfer function is monotonic, all codes within +/-5 LSB (TB2)
- [ ] DNL < 0.5 LSB (TB3 from ngspice, not Python)
- [ ] INL < 0.5 LSB (TB3 from ngspice, not Python)
- [ ] ENOB >= 7.0 bits (TB4 from ngspice FFT, not Python behavioral)
- [ ] No missing codes (TB3 histogram)
- [ ] Active power < 100 uW (TB5)
- [ ] Sleep power < 500 nW (TB6)
- [ ] Wakeup time honestly measured and reported (TB7)
- [ ] All 5 corners produce valid codes within +/-5 LSB (TB8)
- [ ] All 5 corners pass dual-conversion test (TB8 + TB1b)
- [ ] README contains only numbers from ngspice simulations
- [ ] No Python behavioral models exist in the directory
- [ ] Every plot traces to a `.dat` file produced by ngspice `wrdata`

**If any spec fails, report honestly with:**
- Actual measured value
- Root cause analysis
- Proposed fix with specific transistor sizing changes
- Whether the fix was attempted and what happened

---

*This is a real circuit design task. Every number must come from ngspice simulation of real SKY130 transistors with the SAR feedback loop closed. No shortcuts. No behavioral models. No fake numbers.*
