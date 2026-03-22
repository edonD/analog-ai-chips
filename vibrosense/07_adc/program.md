# Block 07: 8-bit SAR ADC Adapted from JKU 12-bit Design

## 1. Objective

Design an 8-bit successive approximation register (SAR) ADC for on-demand digitization
of analog feature voltages. This ADC is shared (via analog mux) among all feature
extraction blocks and converts their outputs for MCU processing.

Key requirement: This is an ON-DEMAND ADC. It sleeps at <0.5 uW and activates only
when the MCU wakes and requests a conversion. It is NOT always-on. The MCU wakes at
10 Hz, requests ~8 conversions (one per feature), then both MCU and ADC go back to
sleep.

Starting point: JKU 12-bit SAR ADC for SKY130 (github.com/iic-jku/SKY130_SAR-ADC1).
We simplify from 12-bit to 8-bit to reduce power, area, and design complexity.

---

## 2. State of the Art

### 2.1 The JKU 12-bit SAR ADC (Our Starting Point)

**Published specs:**
- Resolution: 12 bits
- Sample rate: 1.44 MS/s
- Power: 703 uW at 1.44 MS/s
- Area: 0.175 mm^2 in SKY130
- Architecture: Charge-redistribution SAR with binary-weighted cap DAC
- Comparator: StrongARM latch with pre-amplifier
- SAR logic: Asynchronous (self-timed) for maximum speed
- Cap DAC: 12-bit binary-weighted, Cunit = ~5 fF (estimated)
  Total cap: (2^12 - 1) × 5 fF = 20.475 pF per side (differential)
- Published on GitHub with full Xschem schematics, Magic layout, ngspice testbenches

**Why adapt rather than design from scratch?**
The JKU design is a proven, silicon-verified SAR ADC in the exact same PDK we use.
Adapting it (removing 4 LSB bits) is lower risk than designing from scratch. The
comparator, bootstrapped switches, and layout methodology are already debugged.

**What changes for 8-bit:**
1. Cap DAC: Remove C, 2C, 4C, 8C (the 4 LSBs). Smallest cap becomes 16C (was bit 4).
   Actually, re-anchor: 8-bit means 8 binary-weighted caps from C to 128C.
   Total: (2^8 - 1) × Cunit = 255 × Cunit.
   With Cunit = 5 fF: 1.275 pF per side. ~16x smaller than 12-bit.
2. SAR logic: 8 cycles instead of 12. Simpler counter/sequencer.
3. Clock: Reduce from ~17 MHz internal (1.44M × 12) to ~100 kHz (10k × 10 cycles).
   Massive power reduction from dynamic power scaling.
4. Comparator: Can be smaller/slower. Relaxed kickback and offset requirements
   (8-bit LSB is 16x larger than 12-bit LSB).

### 2.2 Published 8-bit SAR ADCs on 130nm-class Processes

**Chang et al. (TCAS-II 2013)**
- Process: 130nm CMOS
- Resolution: 8-bit
- Sample rate: 200 kS/s
- Power: 3.2 uW at 200 kS/s
- FOM: 100 fJ/conv-step (Walden FOM)
- Architecture: Monotonic switching (set-and-down), saves 50% switching energy
- Relevance: Very close to our target. Shows 8-bit SAR at single-digit uW is feasible.

**Verma et al., Princeton (JSSC 2007)**
- Process: 130nm CMOS
- Resolution: 8-bit
- Sample rate: 100 kS/s
- Power: 1.9 uW
- FOM: 75 fJ/conv-step
- Architecture: Ultra-low-power SAR with custom comparator optimized for low Vdd
- Relevance: Demonstrates the extreme low-power end. Our 10 kS/s target should
  be even lower power since P scales linearly with fs.

**Liu et al. (JSSC 2010)**
- Process: 130nm CMOS
- Resolution: 10-bit (we can compare the 8-bit equivalent)
- Sample rate: 1 MS/s
- Power: 2.5 uW (extrapolated to 8-bit at 10 kS/s: ~0.05 uW active)
- Key innovation: Asynchronous SAR (no external clock needed, self-timed)
- Relevance: Asynchronous operation is beneficial for on-demand conversion

**Our target: 8-bit, 10 kS/s, <50 uW active, <0.5 uW sleep.**
Based on SOTA, even 50 uW seems generous. We may achieve <10 uW active.
But we set 50 uW as the relaxed target to account for unoptimized design.

### 2.3 Walden FOM Comparison

FOM = Power / (2^ENOB × fs)

| Design | ENOB | fs | Power | FOM |
|--------|------|-----|-------|-----|
| JKU 12-bit | ~10.5 | 1.44 MS/s | 703 uW | 337 fJ/conv |
| Chang 8-bit | 7.5 | 200 kS/s | 3.2 uW | 89 fJ/conv |
| Verma 8-bit | 7.2 | 100 kS/s | 1.9 uW | 129 fJ/conv |
| **Ours (target)** | **≥7** | **10 kS/s** | **<50 uW** | **<39 pJ/conv** |

Our FOM looks bad because we're not optimizing for it — we're optimizing for
sleep power and simplicity. The active power will likely be much less than 50 uW
once designed, giving a better FOM.

---

## 3. Architecture

### 3.1 Top-Level Block Diagram

```
                    Vin (from analog mux)
                         │
                    ┌────┴────┐
                    │ Bootstrap│
                    │ Switch   │ (S/H)
                    └────┬────┘
                         │
                    ┌────┴────┐
            Vrefp ──┤ Cap DAC  │
            Vrefn ──┤ 8-bit    │
                    │ binary   │
                    └────┬────┘
                         │
                    ┌────┴────┐
                    │Comparator│
                    │StrongARM │
                    └────┬────┘
                         │
                    ┌────┴────┐
                    │SAR Logic │
                    │8-bit reg │──── D[7:0] output
                    │+ control │
                    └────┬────┘
                         │
                    CLK ──┘

        SLEEP ─────── Power gate (cuts bias to comparator, disables clock)
```

### 3.2 Cap DAC

Binary-weighted capacitor array (single-ended for simplicity; differential if
adapting JKU design directly):

```
Vin ─── S_sample ─── Top plate (shared)
                         │
        ┌────────────────┼────────────────┐
        │                │                │
       128C             64C    ...       1C     (C_dummy)
        │                │                │        │
      S_128            S_64    ...      S_1     GND
     (Vref/GND)      (Vref/GND)     (Vref/GND)
```

- Cunit = 20 fF (larger than JKU's ~5 fF because we have fewer caps and want
  better matching at 8-bit level).
- Total cap: 255 × 20 fF + 20 fF (dummy) = 5.12 pF + 0.02 pF = 5.14 pF.
- Dummy cap: 1 Cunit connected to ground, completes the charge redistribution.
- Vref = 1.2V (bandgap reference or divided VDD). Vrefp = 1.2V, Vrefn = 0V.
  Input range: 0V to 1.2V (or 0.6V ± 0.6V differential).

**Alternative: Monotonic switching (Chang TCAS-II 2013)**
Instead of conventional binary switching (switch each cap to Vref or GND),
use set-and-down: start with all caps at Vref, successively switch caps to GND.
Saves 50% switching energy. But more complex for initial implementation.
**Decision**: Start with conventional switching. Optimize to monotonic if power
budget is tight.

### 3.3 Comparator

StrongARM latch (directly from JKU design, possibly simplified):
- Input NMOS pair: W/L = 4u/0.5u (relaxed from JKU's larger devices — 8-bit
  LSB = 1.2V/256 = 4.7 mV, so comparator offset must be < 2 mV for <0.5 LSB).
- Actually, sigma_os for W/L = 4u/0.5u ≈ 4-5 mV. Marginal.
  Increase to W/L = 8u/1u: sigma_os ≈ 2-3 mV. Acceptable.
- Regeneration latch: cross-coupled inverters, minimum size.
- Pre-amplifier: One stage of NMOS diff pair with diode loads, gain ~10x.
  Reduces effective input-referred offset by 10x. With pre-amp: sigma_os_eff ≈ 0.3 mV.
  Well below 1 LSB.

Power: Comparator fires 8 times per conversion, 10k conversions/s = 80k comparisons/s.
Energy per comparison: ~100 fJ (estimated from Cload × VDD^2).
Pcomp = 80k × 100 fJ = 8 nW. Negligible.

But: bias current for pre-amplifier. If pre-amp is always on during conversion:
Ibias = 5 uA, power = 9 uW for 8 clock cycles at 100 kHz = 80 us per conversion.
Active 0.08% of time (10k × 80u = 0.8 ms per second). P_avg = 9u × 0.8m = 7.2 nW.

### 3.4 SAR Logic

Options:
1. **Synchronous SAR**: External clock drives an 8-bit shift register. Each clock
   cycle, one bit is resolved.
   - Clock frequency: 8 × 10 kS/s × ~1.2 (overhead) = 96 kHz ≈ 100 kHz.
   - Simple to implement and debug.

2. **Asynchronous SAR**: Comparator "ready" signal triggers the next bit.
   Self-timed, no external clock needed.
   - Faster (each bit resolves as soon as comparator decides).
   - More complex control logic.
   - Better power efficiency (no wasted clock cycles).

**Decision**: Synchronous SAR for simplicity. Clock provided by Block 08 MCU or
a simple ring oscillator gated by the CONVERT signal.

SAR logic in Verilog (for mixed-signal simulation):
```verilog
module sar_logic (
    input  wire       clk,
    input  wire       start,    // begin conversion
    input  wire       comp_out, // comparator result
    output reg  [7:0] dac_sw,   // cap DAC switch control
    output reg  [7:0] result,   // final digital output
    output reg        done,     // conversion complete
    output reg        sample    // sample switch control
);
```

State machine:
1. IDLE: Wait for START. SAMPLE = 1 (track input).
2. SAMPLE: Hold for 1 clock cycle. SAMPLE = 0 (hold input).
3. BIT7: Set DAC_SW[7] = 1 (try MSB). Wait for comparator.
   If COMP_OUT = 1: keep DAC_SW[7] = 1 (Vin > Vdac).
   If COMP_OUT = 0: clear DAC_SW[7] = 0 (Vin < Vdac).
4. BIT6 through BIT0: Same process for each successive bit.
5. DONE: Assert DONE, output RESULT[7:0]. Return to IDLE.

Total: 10 clock cycles per conversion (1 sample + 8 bits + 1 done).
At 100 kHz clock: 100 us per conversion. 10 kS/s. Matches spec.

### 3.5 Sleep Mode

Power gating strategy:
- **Sleep signal** (active low) from MCU cuts power to:
  1. Comparator bias (via PMOS header switch).
  2. SAR clock (AND gate: CLK_internal = CLK & ~SLEEP).
  3. Pre-amplifier bias.
- SAR logic flip-flops: retain state (leakage only, ~pA per FF).
- Cap DAC: passive (no power). Charge leaks away during sleep — irrelevant
  because DAC is reset at start of each conversion.

Sleep power:
- 8-bit SAR logic: 10 FFs × ~1 pA leakage = 10 pA.
- Comparator (power-gated): ~100 pA (subthreshold leakage through header).
- Total sleep: ~110 pA × 1.8V = 0.2 nW. Well below 0.5 uW target.

Wakeup time:
- Comparator bias settling: ~1 us (bias current source needs to stabilize).
- Pre-amplifier: ~2 us.
- SAR logic: instant (combinational).
- Total: ~3-5 us. Well below 10 us target (with margin).

---

## 4. Adapting the JKU Design

### 4.1 What to Keep from JKU

1. **Comparator**: StrongARM latch topology. Proven in silicon. May need resizing
   for 8-bit (can use smaller devices since offset budget is 16x relaxed).
2. **Bootstrapped sample switch**: Critical for linearity. The bootstrap circuit
   ensures constant Vgs regardless of input level, giving uniform Ron and thus
   uniform sampling bandwidth.
3. **Layout methodology**: JKU's binary-weighted cap layout with common-centroid
   placement. Directly applicable to our 8-bit array (just fewer caps).
4. **Testbench infrastructure**: Their ngspice testbenches for DNL/INL, FFT can
   be adapted with parameter changes.

### 4.2 What to Change

1. **Cap DAC**: Remove 4 LSB pairs (C, 2C, 4C, 8C). Re-anchor binary weights.
   Old: 12 pairs from C to 2048C. New: 8 pairs from C to 128C.
   Old total: ~20 pF/side. New total: ~5 pF/side.
   Impact: Smaller kT/C noise (actually worse — but 8-bit only needs kT/C noise
   < 1 LSB = 4.7 mV. For C_total = 5 pF: sqrt(kT/C) = sqrt(4.14e-21/5e-12) = 28.8 uV.
   Way below 4.7 mV. No problem).

2. **SAR logic**: Change from 12-bit to 8-bit shift register. If JKU uses
   asynchronous SAR, simplify to synchronous 8-bit for initial design.

3. **Clock frequency**: Reduce from ~17 MHz to ~100 kHz. This is the main power
   saver. Dynamic power P = C × V^2 × f scales linearly with f.
   Power reduction: ~170x from clock scaling alone.

4. **Differential to single-ended**: JKU design is fully differential. For 8-bit,
   single-ended is sufficient (and halves the cap array). But differential
   rejects common-mode noise and supply ripple. Decision: Keep differential if
   adapting JKU layout directly. Go single-ended only if designing from scratch.

5. **Power gating**: JKU design is always-on. Add PMOS header switches on bias
   currents, controlled by SLEEP signal. Add clock gating.

### 4.3 Fallback: Design from Scratch

If adapting JKU is too complex (their design may have many interdependencies that
make partial modification harder than expected), design a simple 8-bit SAR:

**Minimal 8-bit SAR components:**
1. Binary-weighted cap array: 1C, 2C, 4C, 8C, 16C, 32C, 64C, 128C, 1C(dummy).
   Cunit = 20 fF. Total: 256 × 20 fF = 5.12 pF.
2. CMOS transmission gate sample switch (or bootstrapped if linearity matters).
3. StrongARM latch comparator (textbook design).
4. 8-bit SAR logic in Verilog (synthesize with sky130_fd_sc_hd standard cells)
   or hand-design with DFFs and a shift register.
5. Power gating: PMOS header + clock gate.

This from-scratch approach takes ~2 weeks for schematic + simulation, vs ~1 week
for JKU adaptation. But it's fully understood and easier to debug.

**Decision**: Try JKU adaptation first. If blocked after 3 days, switch to from-scratch.

---

## 5. Detailed Design Procedure

### Step 1: Clone and Analyze JKU Design

```bash
git clone https://github.com/iic-jku/SKY130_SAR-ADC1.git
# Examine:
# - Top-level schematic structure
# - Cap DAC sizing and layout
# - Comparator schematic
# - SAR logic implementation
# - Testbench structure
```

Identify which sub-blocks can be reused directly and which need modification.
Document the interface signals and their timing.

### Step 2: Modify Cap DAC

Option A (modify JKU):
- Open cap DAC schematic in Xschem.
- Remove 4 LSB cap pairs.
- Reconnect the remaining 8 pairs to SAR logic outputs.
- Update any parasitic extraction models.

Option B (from scratch):
```spice
* Binary-weighted cap DAC, 8-bit, single-ended
* Top plate is common (sampling node)
* Bottom plates switched between Vref and GND

.subckt cap_dac_8b top sw7 sw6 sw5 sw4 sw3 sw2 sw1 sw0 vref gnd
C128 top n7 {128*Cunit}
C64  top n6 {64*Cunit}
C32  top n5 {32*Cunit}
C16  top n4 {16*Cunit}
C8   top n3 {8*Cunit}
C4   top n2 {4*Cunit}
C2   top n1 {2*Cunit}
C1   top n0 {1*Cunit}
Cdummy top gnd {1*Cunit}

* Switches: each bottom plate to Vref (sw=1) or GND (sw=0)
S7 vref n7 sw7 gnd SMOD
S7b gnd n7 sw7b gnd SMOD
* ... (repeat for all 8 bits)
.param Cunit=20f
.model SMOD SW Ron=500 Roff=1G Vt=0.9
.ends
```

### Step 3: Design/Adapt Comparator

StrongARM latch for 8-bit:
```
         VDD
          │
    ┌─────┴─────┐
    M5(P)       M6(P)    (reset switches)
    │           │
    ├───┐   ┌───┤
    │   │   │   │
    M3(P)   M4(P)        (cross-coupled latch)
    │   │   │   │
    ├───┘   └───┤
    │           │
    OUTN       OUTP
    │           │
    M1(N)       M2(N)    (input diff pair)
    │           │
    └─────┬─────┘
          │
         M0(N)           (tail current / clock switch)
          │
         GND

    INP ── gate M1
    INN ── gate M2
    CLK ── gate M0, M5, M6
```

Sizing for 8-bit (sigma_os < 2 mV):
- M1, M2 (input pair): W/L = 8u/1u. gm/Id ≈ 20 V^-1 in moderate inversion.
  AVT(NMOS, SKY130) ≈ 5 mV·um. sigma_os = AVT / sqrt(W×L) = 5/sqrt(8) = 1.77 mV.
  Acceptable for 1 LSB = 4.7 mV (offset < 0.5 LSB at 1-sigma).
- M3, M4 (latch): W/L = 2u/0.15u. Fast regeneration.
- M5, M6 (reset): W/L = 2u/0.15u. Pull outputs to VDD during reset.
- M0 (tail): W/L = 4u/0.5u. Provides adequate current during evaluate.

Add pre-amplifier if offset is marginal:
- Single-stage NMOS diff pair with diode-connected PMOS loads.
- Gain ~10x. Effective offset: 1.77 mV / 10 = 0.18 mV. Excellent.
- Bias: 2 uA. Power: 3.6 uW (only during conversion).

### Step 4: Implement SAR Logic

Verilog RTL for mixed-signal co-simulation with ngspice (via Verilog-A interface
or d_cosim):

```verilog
module sar_8bit (
    input  wire       clk,
    input  wire       convert,   // start conversion
    input  wire       comp_out,  // from comparator
    output reg  [7:0] dac_ctrl,  // to cap DAC switches
    output reg  [7:0] result,
    output reg        sample_n,  // active-low sample switch
    output reg        valid
);

    reg [3:0] state; // 0=idle, 1=sample, 2-9=bit7..bit0, 10=done

    always @(posedge clk) begin
        case (state)
            4'd0: begin // IDLE
                valid <= 0;
                sample_n <= 0; // sampling
                if (convert) state <= 4'd1;
            end
            4'd1: begin // SAMPLE
                sample_n <= 1; // hold
                dac_ctrl <= 8'b1000_0000; // try MSB
                state <= 4'd2;
            end
            4'd2: begin // BIT7
                if (comp_out) result[7] <= 1;
                else begin result[7] <= 0; dac_ctrl[7] <= 0; end
                dac_ctrl[6] <= 1; // try next bit
                state <= 4'd3;
            end
            // ... BIT6 through BIT0 ...
            4'd9: begin // BIT0
                if (comp_out) result[0] <= 1;
                else begin result[0] <= 0; dac_ctrl[0] <= 0; end
                state <= 4'd10;
            end
            4'd10: begin // DONE
                valid <= 1;
                state <= 4'd0;
            end
        endcase
    end
endmodule
```

For ngspice simulation without Verilog cosimulation, implement SAR logic as
behavioral SPICE (using `A` analog behavioral elements or `Bd` digital elements
with d_cosim). Alternatively, use XSPICE digital models.

### Step 5: Testbench — DNL/INL

```spice
* tb_dnl_inl.spice
* Code density test: apply slow ramp (or sine) input
* Capture all 256 output codes
* Compute histogram, derive DNL and INL

* Slow ramp input: 0V to 1.2V in 25.6ms (100us per code at 10kS/s)
Vramp inp gnd PWL(0 0 25.6m 1.2)

* Run 256 conversions, record output codes
* Post-process in Python:
*   - Histogram of codes
*   - DNL[k] = (count[k] / ideal_count) - 1
*   - INL[k] = sum(DNL[0:k])
*   - PASS: |DNL| < 0.5 LSB, |INL| < 0.5 LSB for all codes

.tran 1u 25.6m
```

### Step 6: Testbench — ENOB (FFT)

```spice
* tb_enob.spice
* Apply near-Nyquist sine input, capture 1024 samples, FFT

* Input: sine at fin = 4.883 kHz (coherent with 10kS/s, 1024 points)
*   fin = fs × M / N = 10k × 501 / 1024 ≈ 4893 Hz (prime M for coherent sampling)
Vsin inp gnd SIN(0.6 0.59 4893)  ; 0.6V DC + 0.59V amplitude (nearly full scale)

.tran 0.1m 102.4m  ; 1024 samples at 10kS/s

* Post-process: FFT of 1024 output codes
* ENOB = (SNDR - 1.76) / 6.02
* Target: ENOB >= 7 bits (SNDR >= 43.9 dB)
```

### Step 7: Testbench — Power

```spice
* tb_power_active.spice
* Measure VDD current during active conversion

.meas tran Iavg_active AVG I(VDD) FROM=0 TO=100u  ; one conversion
.meas tran P_active PARAM='Iavg_active * 1.8'

* tb_power_sleep.spice
* Assert SLEEP, measure leakage
.meas tran Iavg_sleep AVG I(VDD) FROM=1m TO=10m
.meas tran P_sleep PARAM='Iavg_sleep * 1.8'
```

### Step 8: Testbench — Wakeup Time

```spice
* tb_wakeup.spice
* De-assert SLEEP, then immediately start conversion
* Measure time from SLEEP de-assertion to first valid conversion

Vsleep sleep gnd PWL(0 1.8 0 1.8 1u 0)  ; wake up at t=0
Vconvert convert gnd PULSE(0 1.8 2u 1n 1n 10u 200u)  ; first convert at 2us

* Measure: is the first conversion accurate?
* If not, try convert at 5us, 10us, etc.
* Wakeup time = minimum delay between SLEEP de-assertion and valid conversion
```

---

## 6. PASS/FAIL Criteria

| Parameter | Target | Test Method |
|-----------|--------|-------------|
| ENOB | ≥7 bits | FFT of coherent sine, compute SNDR |
| DNL | <0.5 LSB (all codes) | Code density histogram from ramp |
| INL | <0.5 LSB (all codes) | Cumulative sum of DNL |
| Sample rate | ≥10 kS/s | Measure conversion time |
| Active power | <100 uW | IDD measurement during conversion |
| Sleep power | <0.5 uW | IDD measurement with SLEEP asserted |
| Wakeup time | <10 us | First valid conversion after wake |
| Input range | 0 – 1.2V (or Vcm ± 0.6V) | Ramp sweep |
| Missing codes | Zero | Code density histogram |
| Monotonicity | Strictly monotonic | DNL > -1 LSB everywhere |

Note: Active power target is 100 uW (relaxed from initial 50 uW) to account for
unoptimized first design. Optimization target: <50 uW.

---

## 7. Corner and Monte Carlo Strategy

### 7.1 Process Corners

| Corner | Key Concern |
|--------|-------------|
| TT/27C | Baseline performance |
| FF/-40C | Comparator may oscillate (too fast regeneration); check stability |
| SS/85C | Comparator may be too slow; check that it resolves within clock period |
| SF/27C | Cap DAC switch asymmetry; check DNL |
| FS/27C | Same as SF but mirrored |

Critical check: At SS/85C, comparator decision time. With 100 kHz clock (10 us
period), comparator has ~5 us to decide. Even SS comparator decides in <100 ns.
No risk here.

Real risk: Cap DAC settling at SS corner. Switch Ron_SS ≈ 1 kohm.
Worst-case RC: 1k × 5.12 pF = 5.12 ns. 5*tau = 25.6 ns. With 10 us per bit
cycle, this is 0.0003% of the available time. No problem.

### 7.2 Monte Carlo (100 runs)

**Cap mismatch**: This is the dominant error source for SAR ADC.
- Cunit = 20 fF. sigma(dC/C) = 0.5% / sqrt(A).
  For 20 fF cap (3.2 um × 3.2 um): sigma = 0.5% / 3.2 = 0.156%.
- MSB cap = 128 × Cunit. Implemented as 128 unit elements.
  Mismatch of MSB aggregate: 0.156% / sqrt(128) = 0.014%. Excellent.
- Critical ratio: MSB vs sum of all lower bits (127C vs 128C).
  Mismatch: sqrt(2) × 0.156% / sqrt(128) = 0.019%.
  At 8-bit level (1 LSB = 0.39%): mismatch is 0.019/0.39 = 0.05 LSB. Negligible.

**Comparator offset**: sigma_os = 1.77 mV (without pre-amp) or 0.18 mV (with pre-amp).
- 1 LSB = 4.7 mV. Offset < 0.5 LSB at 1-sigma without pre-amp. Acceptable.
- With pre-amp: offset is negligible.

**Switch charge injection mismatch**: Different Vth per switch causes different
charge injection. With 8 switches, worst-case is MSB switch.
- Charge injection on MSB node: Qinj = 0.5 × W × L × Cox × delta_Vth.
  delta_Vth ~ 5 mV (1-sigma). Qinj = 0.5 × 2 × 0.15 × 8.8f × 5m = 6.6 aC.
  On 128C = 2.56 pF: dV = 6.6a / 2.56p = 2.6 uV. Negligible.

**Conclusion**: 8-bit SAR in SKY130 is dominated by systematic errors (layout
parasitics, comparator offset), not random mismatch. Monte Carlo will likely show
all 100 runs passing. The real challenge is good layout.

---

## 8. Power Analysis (Detailed)

### Active Mode (during conversion)

| Component | Power | Duty |
|-----------|-------|------|
| Comparator (8 decisions) | 8 × 100 fJ / 100 us = 8 nW | per conversion |
| Pre-amplifier bias (2 uA) | 3.6 uW × 100 us/100 ms = 3.6 nW avg | 0.1% |
| SAR logic (8 clock edges) | 8 × 50 fJ / 100 us = 4 nW | per conversion |
| Cap DAC switching | ~8 × 0.5 × Cunit × Vref^2 = 8 × 14.4 fJ = 115 fJ | per conversion |
| Bootstrap switch | ~50 fJ per sample | per conversion |
| **Total per conversion** | **~400 fJ** | |
| **At 80 conv/s (8 features × 10 Hz)** | **32 pW average** | |

But this ignores bias currents that must be on during the full conversion window.
Comparator pre-amp: 2 uA × 1.8V = 3.6 uW for 100 us = 360 pJ per conversion.
At 80 conv/s: 28.8 nW average. Still negligible.

**Realistic active power**: ~10-50 uW during the 100 us conversion window.
Averaged over 10 Hz wake cycle: <500 nW.

### Sleep Mode

| Component | Leakage |
|-----------|---------|
| SAR logic (10 FFs) | ~10 pA |
| Comparator (power-gated) | ~100 pA |
| Cap DAC switches (all off) | ~50 pA |
| Pre-amp (power-gated) | ~50 pA |
| **Total** | **~210 pA × 1.8V = 0.38 nW** |

0.38 nW << 500 nW target. Excellent margin.

---

## 9. Layout Considerations

### Cap DAC Layout
- Binary-weighted caps using unit-element (20 fF) tiling.
- Common-centroid arrangement to cancel linear gradients:
  - MSB (128C): 128 unit caps spread across the array.
  - LSB (1C): 1 unit cap at the geometric center.
- Top-plate (sampling node) routing: thick metal, short, minimal parasitic.
- Bottom-plate routing: to switches, keep balanced between Vref and GND paths.
- Guard ring around entire cap DAC.

### Comparator Layout
- Input pair: interdigitated (M1a, M2a, M2b, M1b) for matching.
- Latch: symmetric cross-coupled layout.
- Keep comparator close to cap DAC to minimize parasitic on comparison node.

### Area Estimate

| Block | Area |
|-------|------|
| Cap DAC (5.14 pF total) | ~2600 um^2 = 51 um × 51 um |
| Comparator + pre-amp | ~30 um × 20 um = 600 um^2 |
| SAR logic (std cells) | ~50 um × 10 um = 500 um^2 |
| Bootstrap switch | ~10 um × 10 um = 100 um^2 |
| Routing + decoupling | ~0.005 mm^2 |
| **Total** | **~0.01 mm^2** |

Compare to JKU 12-bit: 0.175 mm^2. Our 8-bit is ~17x smaller. Reasonable
(cap array is 16x smaller, logic slightly simpler).

---

## 10. From-Scratch Design (Fallback)

If JKU adaptation proves too entangled, here is the from-scratch design plan:

### 10.1 Minimal Component List

1. **Sample switch**: Single NMOS (sky130_fd_pr__nfet_01v8, W/L = 5u/0.15u).
   No bootstrap for simplicity. Linearity will suffer at high Vin (Ron increases).
   Acceptable for 8-bit if input range is limited to mid-supply (0.3V to 0.9V).
   Or: use CMOS TG for rail-to-rail.

2. **Cap DAC**: 8 binary-weighted MIM caps + 1 dummy. Cunit = 20 fF.
   Use `sky130_fd_pr__cap_mim_m3_1` parametric cell.

3. **Comparator**: Standard StrongARM. Schematic from Razavi textbook.
   12 transistors total.

4. **SAR logic**: 8 DFFs + combinational logic. Use `sky130_fd_sc_hd__dfxtp_1`
   standard cells. Or design at transistor level (8 × 28 transistors = 224 MOSFETS
   for the DFFs alone — manageable).

5. **Power gate**: Single PMOS header (W = 10u) on comparator VDD.

### 10.2 Simulation Strategy (From-Scratch)

1. Build comparator, verify offset and speed standalone.
2. Build cap DAC, verify monotonicity with ideal switch and ideal comparator.
3. Combine: SAR loop with behavioral SAR logic (XSPICE state machine).
4. Replace behavioral SAR with transistor/standard-cell SAR.
5. Full DNL/INL and ENOB characterization.
6. Add power gating, verify sleep/wake.

### 10.3 Timeline

| Week | Task |
|------|------|
| 1 | Comparator design + standalone verification |
| 2 | Cap DAC design + verification with ideal comparator |
| 3 | SAR logic + full ADC integration + DNL/INL |
| 4 | ENOB, power, corners, Monte Carlo, layout start |

---

## 11. Integration with System

### Inputs
- `VIN`: Analog input from analog mux (Block 08 controls mux). Range: 0 – 1.2V.
  Sources: Block 04 band energies, Block 05 RMS and peak, Block 06 class scores.
- `CONVERT`: Start conversion pulse from MCU (Block 08).
- `CLK`: 100 kHz clock from MCU or local oscillator.
- `SLEEP`: Power-down control from MCU.
- `VDD` = 1.8V, `VSS` = 0V, `VREF` = 1.2V (from bandgap or resistive divider).

### Outputs
- `D[7:0]`: 8-bit digital output to MCU.
- `VALID`: Conversion complete flag.

### Conversion Sequence
1. MCU de-asserts SLEEP (wakeup ~5 us).
2. MCU selects analog mux channel (settling ~1 us).
3. MCU asserts CONVERT.
4. ADC samples input, runs 8 SAR cycles (100 us total).
5. ADC asserts VALID. MCU reads D[7:0].
6. Repeat for next channel (8 channels × 100 us = 800 us total).
7. MCU asserts SLEEP. ADC enters low-power mode.

Total wake time per 10 Hz cycle: ~1 ms (including MCU overhead).
ADC active time: 800 us per 100 ms cycle = 0.8% duty cycle.

---

## 12. References

1. JKU SKY130 SAR ADC, https://github.com/iic-jku/SKY130_SAR-ADC1
2. S.-W. M. Chen and R. W. Brodersen, "A 6-bit 600-MS/s 5.3-mW Asynchronous ADC
   in 0.13-um CMOS," JSSC 2006.
3. M. van Elzakker et al., "A 10-bit Charge-Redistribution ADC Consuming 1.9 uW
   at 1 MS/s," JSSC 2010.
4. C.-C. Liu et al., "A 10-bit 50-MS/s SAR ADC With a Monotonic Capacitor Switching
   Procedure," JSSC 2010.
5. S.-E. Chang et al., "An 8-bit 200-kS/s 3.2-uW SAR ADC," TCAS-II 2013.
6. N. Verma and A. P. Chandrakasan, "An Ultra Low Energy 12-bit Rate-Resolution
   Scalable SAR ADC for Wireless Sensor Nodes," JSSC 2007.
7. B. Razavi, "The StrongARM Latch," IEEE SSC Magazine, 2015.
8. P. Harpe et al., "A 2.2/2.7 fJ/conversion-step 10/12b 40 kS/s SAR ADC with
   Data-Driven Noise Reduction," ISSCC 2013.
9. SkyWater SKY130A PDK documentation, https://skywater-pdk.readthedocs.io

---

## 13. Comparison: Our ADC vs. Published Works

| Parameter | JKU 12b | Chang 8b | Verma 8b | **Ours (target)** |
|-----------|---------|----------|----------|-------------------|
| Process | SKY130 | 130nm | 130nm | **SKY130** |
| Resolution | 12 bit | 8 bit | 8 bit | **8 bit** |
| ENOB | ~10.5 | 7.5 | 7.2 | **≥7** |
| Sample rate | 1.44 MS/s | 200 kS/s | 100 kS/s | **10 kS/s** |
| Active power | 703 uW | 3.2 uW | 1.9 uW | **<100 uW** |
| Sleep power | N/A | N/A | N/A | **<0.5 uW** |
| FOM (Walden) | 337 fJ | 89 fJ | 129 fJ | **<78 pJ** |
| Area | 0.175 mm^2 | N/R | N/R | **~0.01 mm^2** |
| Differential | Yes | No | No | **TBD** |

Our FOM is poor because we optimize for sleep power and simplicity, not
throughput. At 10 kS/s, the per-conversion energy will likely be similar to
Chang/Verma, giving a competitive FOM if we achieve <10 uW active.

---

## 14. Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| JKU adaptation too entangled | MEDIUM | Fallback: from-scratch 8-bit SAR |
| Comparator offset > 0.5 LSB | MEDIUM | Pre-amplifier stage, or offset calibration |
| Cap DAC parasitics degrade linearity | MEDIUM | Careful layout, PEX, post-layout simulation |
| Sleep mode leakage too high | LOW | SKY130 leakage is low; add power gating header |
| Wakeup time > 10 us | LOW | Comparator bias designed for fast settling |
| ENOB < 7 bits | MEDIUM | Likely due to layout — iterate layout and PEX |
| Missing codes | LOW | Unlikely at 8-bit with proper cap matching |

---

## 15. Checklist

- [ ] JKU design cloned and analyzed (or from-scratch design started)
- [ ] Cap DAC schematic: 8-bit binary-weighted, Cunit = 20 fF
- [ ] Comparator standalone: offset < 2 mV, decision time < 100 ns
- [ ] SAR logic: functional simulation shows correct bit-trial sequence
- [ ] Full ADC integration: ramp input produces monotonic output codes
- [ ] DNL measured: < 0.5 LSB for all 256 codes
- [ ] INL measured: < 0.5 LSB for all 256 codes
- [ ] ENOB measured: ≥ 7 bits via FFT
- [ ] Active power: < 100 uW (goal: < 50 uW)
- [ ] Sleep power: < 0.5 uW
- [ ] Wakeup time: < 10 us to first valid conversion
- [ ] Monte Carlo 100 runs: DNL < 0.5 LSB at 3-sigma
- [ ] Corner simulations: all specs pass at 5 corners × 3 temperatures
- [ ] Layout started (cap DAC common-centroid, comparator matched)
- [ ] Post-layout simulation: ENOB degradation < 0.5 bits from schematic
