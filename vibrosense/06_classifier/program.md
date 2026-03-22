# Block 06: Charge-Domain MAC Classifier Using MIM Capacitors

## 1. Objective

Design a 4-class vibration classifier using charge-domain multiply-accumulate (MAC)
computation with binary-weighted MIM capacitors. This block takes 8 analog feature
voltages (from Blocks 04/05: spectral band energies, RMS, crest factor) and computes
4 weighted sums (one per class) using capacitive charge sharing. A winner-take-all
(WTA) circuit selects the class with highest score.

This is the computational heart of the VibroSense system — a tiny but functional
compute-in-memory (CIM) classifier, directly inspired by academic and commercial
charge-domain CIM architectures.

Total power budget: <5 uW averaged (mostly off; operates only during classification).

---

## 2. State of the Art

### 2.1 Charge-Domain CIM — The Big Players

**EnCharge AI (Princeton spinoff, 2023-2025)**
- Topology: Capacitor-based CIM using Q = C × V. Binary-weighted caps store weights,
  input voltages are sampled onto them, charge redistribution computes MAC.
- Scale: 200 TOPS at chip level (massive arrays, 256×256 and larger).
- Precision: 4-8 bit weights, 8-bit inputs.
- Power efficiency: Claimed 100+ TOPS/W (charge-domain is inherently efficient because
  energy per MAC = 0.5*C*V^2, and with C = 1 fF, V = 0.5V: E = 0.125 fJ/MAC).
- Key innovation: Charge-domain avoids current-based summation (which has IR drop and
  static power). Charge sharing is passive — no amplifier needed for the MAC itself.
- Relevance: Direct inspiration for our design. We use the same Q = C × V principle
  but at microscopic scale (128 caps vs their millions).

**KAIST charge-domain CIM macro (ISSCC 2023)**
- Topology: 256×256 capacitor array, 4-bit weights, charge redistribution.
- Performance: 4.1 TOPS, 12.4 TOPS/W.
- Key detail: Uses ping-pong architecture (two arrays alternating sample/evaluate)
  to hide latency. We don't need this — our classification rate is only 10 Hz.
- Cap unit: ~10 fF in 28nm. Our 50 fF in SKY130 is larger (older process) but
  still small enough.

**Samsung charge-domain CIM (JSSC 2022)**
- Topology: Capacitor-based CIM with 8-bit inputs, 4-bit weights.
- Performance: 5.4 TOPS/W in 28nm.
- Key insight: Charge injection from switches is the dominant error source, not
  cap mismatch. They use dummy switch compensation and bottom-plate sampling.
  We must address the same issue.

**Verma group, Princeton (multiple papers 2018-2024)**
- The academic group behind EnCharge. Foundational papers:
  - Valavi et al., "A mixed-signal charge-domain CIM," JSSC 2019.
  - Gonugondla et al., "Fundamental limits of charge-domain CIM," JSSC 2020.
  - Bankman et al., "Analog compute-in-memory for ML inference," Nature Electronics 2023.
- Key theoretical result: Charge-domain MAC SNR = 6.02*N + 1.76 + 10*log10(M) dB,
  where N = weight bits and M = number of inputs being accumulated. More inputs
  actually improve SNR (averaging effect). For our case: N=4, M=8:
  SNR = 24.08 + 1.76 + 9.03 = 34.87 dB ≈ 5.5 ENOB. Adequate for 4-class
  classification.

### 2.2 Why Charge-Domain for VibroSense?

Alternative approaches for a tiny 8×4 classifier:
1. **Digital MAC in MCU**: Block 08 MCU could compute 8×4 MACs in software.
   Cost: ~32 multiply-accumulates per classification. At 1 MHz clock, takes ~32 us.
   Power: ~50 uW for 32 us = 1.6 nJ per classification. At 10 Hz: 16 nW average.
   THIS IS CHEAPER than analog. So why do analog?

   **Answer**: The analog classifier is a technology demonstrator. We are proving
   that charge-domain CIM works in SKY130 at ultra-low power. The classifier
   itself is trivially small, but the architecture scales — the same cap cell
   could be tiled to 256×256 for neural network inference at orders of magnitude
   better efficiency than digital.

2. **Current-domain CIM (SRAM-based)**: Well-explored (TSMC, Samsung, Intel papers).
   But requires SRAM bitcells, sense amplifiers, and significant static current.
   Overkill for 8×4. Also, SKY130 SRAM is not well-characterized for CIM.

3. **Resistive CIM (RRAM/memristor)**: Not available in SKY130.

**Decision**: Charge-domain CIM with MIM capacitors. Simple, passive, and directly
demonstrates the principle that EnCharge commercialized at scale.

---

## 3. Architecture

### 3.1 Top-Level Block Diagram

```
  8 Feature Inputs (V0-V7)     32-bit Shift Register (from SPI)
         │                              │
         ▼                              ▼
  ┌──────────────────────────────────────────────┐
  │           4 × MAC Units (one per class)      │
  │                                              │
  │  MAC_0: W[0][0..7] × V[0..7] → Score_0      │
  │  MAC_1: W[1][0..7] × V[0..7] → Score_1      │
  │  MAC_2: W[2][0..7] × V[0..7] → Score_2      │
  │  MAC_3: W[3][0..7] × V[0..7] → Score_3      │
  │                                              │
  └────────────┬───────────┬──────────┬──────────┘
               │           │          │
               ▼           ▼          ▼
  ┌─────────────────────────────────────────┐
  │         Winner-Take-All (WTA)           │
  │  4 comparators + priority encoder       │
  │  Output: 2-bit class label (0-3)        │
  └─────────────────────────────────────────┘
```

### 3.2 Single MAC Unit Detail

Each MAC unit has 8 input positions, each with a 4-bit binary-weighted cap bank:

```
  V_in[j] ──── S_sample ──── ┬─── Cunit (50fF)  ── S_eval ──┐
                              ├─── 2×Cunit (100fF) ── S_eval ──┤
                              ├─── 4×Cunit (200fF) ── S_eval ──┤
                              └─── 8×Cunit (400fF) ── S_eval ──┤
                                                                │
                                        Bitline (Cbl ~ 1pF) ◄──┘
                                              │
                                         To comparator
```

Weight bits (w3,w2,w1,w0) control which caps are connected to the eval switches.
If weight bit = 1, that cap participates in charge sharing. If 0, that cap is
grounded (discharged) during sample phase.

### 3.3 Operation Phases

**Phase 1: Reset**
- All bitlines precharged to Vcm = 0.9V (or VDD/2).
- All weight caps discharged to ground.
- Duration: ~100 ns.

**Phase 2: Sample**
- S_sample switches close. Each input voltage V[j] charges the weight caps
  that have their weight bit = 1.
- Charge stored: Q[j] = W[j] × Cunit × V[j], where W[j] is the 4-bit weight
  (0 to 15) and Cunit = 50 fF.
- Duration: ~200 ns (RC settling through switch + cap).

**Phase 3: Evaluate**
- S_sample switches open. S_eval switches close.
- All charged caps share charge onto bitline capacitance Cbl.
- Bitline voltage:
  V_bl = Vcm + (Sum_j W[j] × Cunit × (V[j] - Vcm)) / (Cbl + Sum_j W[j] × Cunit)
- This is the MAC result, scaled by capacitor ratios.
- Duration: ~200 ns.

**Phase 4: Compare**
- Comparators compare Score_0..Score_3 against each other.
- WTA selects the highest score.
- Duration: ~100 ns (StrongARM latch comparator).

**Total computation time: ~600 ns < 1 us. Meets spec.**

### 3.4 Capacitor Array Sizing

Binary-weighted MIM caps per input position:
- Cunit = 50 fF (sky130_fd_pr__cap_mim_m3_1, minimum reliable size for matching)
- 1C = 50 fF (bit 0, LSB)
- 2C = 100 fF (bit 1)
- 4C = 200 fF (bit 2)
- 8C = 400 fF (bit 3, MSB)
- Total per input position: 15C = 750 fF
- Total per MAC unit: 8 inputs × 750 fF = 6 pF
- Total for 4 MAC units: 24 pF

MIM cap density in SKY130: ~2 fF/um^2.
Area for 24 pF: 12,000 um^2 = ~110 um × 110 um. Very small.

### 3.5 Bitline Capacitance

Cbl determines the voltage scaling and SNR. Larger Cbl means smaller signal swing
(worse SNR) but better linearity and less sensitivity to parasitic variation.

Design choice: Cbl = 1 pF (explicit MIM cap).
- Maximum signal: all 8 inputs at max (1.2V), all weights = 15.
  Total charge cap = 8 × 15 × 50 fF = 6 pF.
  V_bl_max = Vcm + 6 pF × (1.2 - 0.9) / (1 pF + 6 pF) = 0.9 + 0.257 V = 1.157 V.
  Within supply range. Good.
- 1 LSB equivalent on bitline: Cunit × (Vmax - Vcm) / (Cbl + 6p) = 50f × 0.3 / 7p
  = 2.14 mV. Comparator needs to resolve ~2 mV. Achievable with StrongARM latch.

### 3.6 Winner-Take-All

Four parallel StrongARM latch comparators in round-robin tournament:
- Compare Score_0 vs Score_1 → Winner_A
- Compare Score_2 vs Score_3 → Winner_B
- Compare Winner_A vs Winner_B → Final winner

Actually, simpler: use 4 comparators comparing each score against a swept threshold
(analog search). But this is slow.

**Simplest approach**: 6 comparators for all pairs (C(4,2) = 6), plus voting logic.
But 6 comparators × ~1 uW each = 6 uW. Too much.

**Revised approach**: Sequential comparison using a single comparator + analog mux.
- Mux selects Score_0 onto comparator input A.
- Compare against Score_1, Score_2, Score_3 sequentially.
- If Score_0 wins all 3 comparisons, class = 0.
- Else, try Score_1 against remaining, etc.
- Worst case: 6 comparisons × 100 ns = 600 ns. Total: ~1.2 us. Still < 10 us.
- Power: 1 comparator = ~1 uW. Acceptable.

**Final decision**: Single StrongARM comparator + 4:1 analog mux on each input.
2-bit counter drives mux select. Simple digital control (included in Block 08 or
local FSM).

---

## 4. Detailed Design Procedure

### Step 1: Unit Capacitor Design

The 50 fF MIM cap in SKY130:
- sky130_fd_pr__cap_mim_m3_1: Metal3-Metal4 MIM capacitor.
- Density: ~2 fF/um^2. For 50 fF: area = 25 um^2, i.e., 5 um × 5 um.
- Matching: sigma(dC/C) ≈ 0.1% / sqrt(area_in_um^2) = 0.1% / 5 = 0.02%.
  For 50 fF cap: sigma = 0.02% × 50 fF = 0.01 fF. Negligible.
- Binary-weighted caps: 2C = two unit caps in parallel (not one 100 fF cap).
  This ensures matching through unit-element design.
- Layout: common-centroid arrangement for each 4-bit bank:
  ```
  8C 4C 2C 1C 1C 2C 4C 8C
  ```
  (mirror symmetry to cancel gradients)

### Step 2: Switch Design

CMOS transmission gate for each sample/eval switch:
- NMOS: sky130_fd_pr__nfet_01v8, W/L = 2u/0.15u (minimum Ron ~ 500 ohm).
- PMOS: sky130_fd_pr__pfet_01v8, W/L = 4u/0.15u.
- Ron × C = 500 × 400 fF = 0.2 ns. RC settling in 5*tau = 1 ns. Fast enough.

**Charge injection analysis** (CRITICAL):
- When S_sample opens, channel charge is injected onto the cap.
- For NMOS: Qinj = 0.5 × W × L × Cox × (Vgs - Vth).
  Cox = 8.8 fF/um^2 (SKY130). W = 2u, L = 0.15u.
  Qinj = 0.5 × 2 × 0.15 × 8.8f × (1.8 - 0.5) = 0.5 × 0.264f × 1.3 = 0.172 fC.
  On 50 fF cap: dV = 0.172 fC / 50 fF = 3.4 mV.
  1 LSB on bitline = 2.14 mV. So charge injection = 1.6 LSB. TOO MUCH.

**Mitigation strategies**:
1. **Bottom-plate sampling**: Sample input on top plate of cap; bottom plate is the
   switch side. When switch opens, charge injection goes to low-impedance input
   source, not to the cap. Standard technique, used in all SAR ADCs.
2. **Dummy switch**: Half-sized NMOS (W/2) driven by inverted clock, absorbs charge
   from main switch.
3. **Complementary switches**: CMOS TG has partial cancellation (NMOS injects
   positive charge, PMOS injects negative). Not perfect but helps.
4. **Slow clock edges**: Reduces dV/dt-induced injection. Use 10 ns rise/fall.

**Decision**: Use bottom-plate sampling (primary) + complementary TG (secondary).
Residual charge injection target: <0.5 LSB = <1 mV on bitline.

### Step 3: Weight Shift Register

32-bit shift register (8 weights × 4 bits) loaded via SPI:
- 32 D-flip-flops (sky130_fd_sc_hd__dfxtp_1).
- Serial data in (SDI), serial clock (SCK), latch enable (LE).
- On LE rising edge, shift register contents transferred to weight latches
  that control the cap bank switches.
- SPI clock: 1 MHz (from Block 08 MCU). Load time: 32 us. Negligible.
- Power: Shift register is static CMOS. Leakage only when not clocking. ~10 nW.

For 4 MAC units with different weights: 4 × 32 = 128 flip-flops total.
Or: load sequentially (4 × 32 us = 128 us) with a 7-bit address (which MAC unit).
Decision: 128 FFs. Area: 128 × ~10 um^2 = 1280 um^2. Negligible.

### Step 4: StrongARM Comparator

Standard StrongARM latch (Razavi topology):
- Input diff pair: NMOS, W/L = 2u/0.5u. Gm enough for ~1 mV resolution.
- Cross-coupled inverter latch: regeneration to full digital levels.
- Clock: single-phase. CLK high = reset (both outputs low). CLK falling = evaluate.
- Power: dynamic only. E = Cload × VDD^2 per comparison.
  Cload ~ 20 fF. E = 20f × 1.8^2 = 64.8 fJ per comparison.
  At 10 Hz classification with 6 comparisons: P = 6 × 64.8f × 10 = 3.9 pW. Negligible.
- Offset: sigma_os ≈ 5-10 mV with minimum-sized devices. Our LSB = 2.14 mV.
  Need sigma_os < 1 mV for reliable comparison.
  Upsize input pair: W/L = 10u/1u. sigma_os ≈ 2-3 mV. Marginal.
  Add calibration: offset-cancel comparator with pre-amplifier stage.
  Or: accept that classification may have 1-2 bit uncertainty and rely on
  software majority voting across multiple classifications. For 10 Hz rate,
  majority-vote over 5 readings = 2 Hz effective rate. Acceptable.

### Step 5: Charge Injection Testbench (CRITICAL)

```spice
* tb_charge_inject.spice
* Zero-input charge injection test
* All inputs at Vcm, toggle all switches, measure residual Vbl

* Setup: all weight caps connected (W=15 for all inputs)
* Input: all V[j] = Vcm = 0.9V
* Expected Vbl after eval = Vcm (since all inputs = Vcm)
* Any deviation = charge injection error

V0 inp0 gnd 0.9
V1 inp1 gnd 0.9
* ... (all 8 inputs at 0.9V)

* Clock: sample phase (100ns), then eval phase (100ns)
Vclk_sample clk_s gnd PULSE(0 1.8 0 1n 1n 100n 400n)
Vclk_eval   clk_e gnd PULSE(0 1.8 150n 1n 1n 100n 400n)

* Measure: Vbl at end of eval phase
.meas tran V_inject FIND V(bitline) AT=300n
.meas tran V_error PARAM='V_inject - 0.9'

* PASS: |V_error| < 1 LSB = 2.14 mV
* PASS: |V_error| < Cunit × Vref / 15 / Cbl = 50f × 0.3 / 15 / 1p = 1 mV
```

### Step 6: MAC Linearity Testbench (CRITICAL — ALL 16 WEIGHT CODES)

```spice
* tb_mac_linearity.spice
* Single input (V0), sweep weight from 0 to 15, measure Vbl
* Other 7 inputs grounded (at Vcm with W=0)

.param WEIGHT=0  ; swept 0..15 in Python wrapper

V0 inp0 gnd 1.05  ; Vcm + 150mV = moderate input

* Weight configuration: only inp0 active
* W[0] = WEIGHT (parameterized), W[1..7] = 0

* Expected: Vbl = Vcm + WEIGHT * Cunit * (1.05 - 0.9) / (Cbl + WEIGHT * Cunit)
* For WEIGHT=0: Vbl = 0.9V
* For WEIGHT=15: Vbl = 0.9 + 15*50f*0.15 / (1p+750f) = 0.9 + 112.5f/1.75p = 0.9 + 64.3mV

* Sweep WEIGHT 0..15, verify:
* 1. Monotonically increasing
* 2. DNL < 2 LSB (= 2 × 64.3/15 = 8.6 mV)
* 3. INL < 2 LSB
```

### Step 7: Full Classification Testbench

```spice
* tb_classify_cwru.spice
* Load trained weights from Block 09
* Apply CWRU test vectors (8 features each)
* Run 4 MAC units, check WTA output
* Must correctly classify: Normal, Inner Race, Outer Race, Ball fault

* Test vectors (from Block 09 training):
* V_normal  = [0.95, 0.91, 0.92, 0.90, 0.93, 0.91, 0.90, 0.92]
* V_inner   = [1.10, 1.05, 0.95, 0.92, 1.08, 0.90, 0.91, 1.15]
* V_outer   = [0.95, 1.10, 1.08, 0.90, 0.92, 1.05, 0.90, 0.91]
* V_ball    = [0.93, 0.92, 1.05, 1.08, 0.91, 0.92, 1.10, 0.95]

* For each test vector, run full sample-eval-compare cycle
* Check: WTA output matches expected class label
```

---

## 5. PASS/FAIL Criteria

| Parameter | Target | Test Method |
|-----------|--------|-------------|
| MAC linearity | ±2 LSB (DNL and INL) | 16-code weight sweep on single input |
| MAC monotonicity | Strictly monotonic for 0-15 weights | Same sweep, check no inversions |
| Computation time | <1 us | Measure from sample rising edge to valid WTA output |
| Weight precision | ≥4 bits effective | ENOB from linearity measurement |
| Charge injection | <1 LSB on bitline | Zero-input switch toggle test |
| Classification rate | ≥10 Hz | Timing analysis of full cycle |
| Average power | <5 uW | Current measurement over full classify cycle |
| Cap mismatch impact | <1 class error in 100 MC runs | Monte Carlo classification |
| Weight loading | All 128 bits correct via SPI | Shift register functional test |
| WTA accuracy | Correct winner for >10 mV score difference | Sweep score differences |

---

## 6. Monte Carlo Strategy (100 Runs)

### Cap Mismatch Model
SKY130 MIM cap matching: sigma(dC/C) = 0.5% / sqrt(A_um^2) for M3-M4 MIM.
For Cunit = 50 fF (5 um × 5 um = 25 um^2): sigma = 0.5% / 5 = 0.1%.
For 8C = 400 fF (effective 8 parallel 50 fF): sigma = 0.1% / sqrt(8) = 0.035%.

Apply Gaussian mismatch to each cap independently. Measure:
1. MAC output for fixed input/weight: distribution of Vbl.
2. Classification accuracy: run all 4 CWRU test vectors, count misclassifications.

**Expected result**: With 0.1% cap mismatch, MAC error is ~0.1% of full scale
= 0.064 mV on bitline. This is 0.03 LSB. Cap mismatch is NOT the problem.

### Switch Mismatch Model
Vth mismatch in TG switches causes different charge injection per switch.
sigma(Vth) ≈ 5 mV for W/L = 2u/0.15u in SKY130.
This modulates charge injection differently per path.
Expected impact: ~0.5 mV spread on bitline. ~0.25 LSB. Acceptable.

### Comparator Offset
sigma_os = 3 mV for input pair W/L = 10u/1u.
LSB on bitline = 2.14 mV. Offset > 1 LSB is possible.
**This is the dominant error source.**
Mitigation: offset calibration during startup (store offset, subtract digitally).

---

## 7. Corner Analysis

| Corner | Key Concern | Expected Impact |
|--------|-------------|-----------------|
| TT/27C | Nominal | Baseline |
| FF/-40C | Fast switches, less charge injection | Better accuracy |
| SS/85C | Slow switches, more leakage on bitline | Possible droop during eval phase |
| SF/27C | NMOS slow, PMOS fast: TG asymmetry | Worse charge injection cancellation |
| FS/27C | NMOS fast, PMOS slow: TG asymmetry | Worse charge injection cancellation |

Key risk: At SS/85C, switch Ron increases. Need to verify that RC settling during
200 ns sample phase is still adequate. Ron_SS ≈ 2× Ron_TT = 1 kohm.
Worst case: 1k × 400 fF = 0.4 ns. 5*tau = 2 ns. Still fine.

Leakage at 85C on bitline during evaluate phase:
Junction leakage ≈ 100 pA at 85C. On 1 pF bitline: dV/dt = 100 pA / 1 pF = 100 mV/s.
In 200 ns evaluate: dV = 20 nV. Negligible.

---

## 8. Power Analysis

| State | Duration | Current | Energy |
|-------|----------|---------|--------|
| Idle (weights loaded, waiting) | 99.99% of time | ~10 nA (leakage) | — |
| Sample phase | 200 ns | ~50 uA (switch charging) | 10 fJ |
| Evaluate phase | 200 ns | ~5 uA (charge redistribution) | 1 fJ |
| Compare phase | 100 ns | ~50 uA (comparator) | 5 fJ |
| WTA logic | 100 ns | ~10 uA | 1 fJ |
| **Per classification** | **~600 ns** | — | **~17 fJ** |
| **At 10 Hz** | — | — | **170 fJ/s = 170 fW** |

The classifier itself is essentially free in terms of power. The dominant power
cost is the bias current for the comparator if it's kept always-on. At 1 uA bias:
P = 1.8 uW. Well within 5 uW budget.

With duty cycling (comparator on only during classification): P_avg = 170 fW.
Negligible compared to other blocks.

---

## 9. Layout Considerations

### Capacitor Array
- 128 unit caps (50 fF each) organized in 4 MAC units × 8 inputs × 4 bit-weights.
- Common-centroid layout within each 4-bit bank.
- Each MAC unit's caps in a row, 4 rows for 4 MAC units.
- Total cap area: 128 × 25 um^2 = 3200 um^2 = ~57 um × 57 um.
- Add 2x for routing: ~115 um × 115 um = 0.013 mm^2.

### Switches
- 128 sample switches + 128 eval switches = 256 TGs.
- Each TG: ~2 um × 1 um = 2 um^2. Total: 512 um^2. Negligible.
- Place switches adjacent to their respective caps.

### Shift Register
- 128 DFFs. Area: ~1300 um^2 = ~36 um × 36 um.
- Place at edge of classifier block, near SPI pads.

### Comparator
- 1 StrongARM latch + 2 analog muxes. Area: ~20 um × 20 um.

### Total Area
~0.015 mm^2. Very compact. Dominated by the cap array.

---

## 10. Weight Encoding

### 4-Bit Weight Representation

Unsigned 4-bit weights: 0 to 15.
- Weight = 0: All 4 caps disconnected. No contribution from this input.
- Weight = 15: All 4 caps connected. Maximum contribution.
- Weight = 8: Only MSB cap (8C = 400 fF) connected.

For signed weights (needed for some classifiers), use offset binary:
- Actual_weight = Code - 8. Range: -8 to +7.
- Negative weights: subtract contribution by connecting cap to Vcm instead of Vin
  during sample phase (requires additional switch per cap, driven by sign bit).
- Decision: Use unsigned weights initially. If Block 09 training requires signed
  weights, add sign-inversion switches. This adds 32 switches (8 per MAC, sign
  bit per input). Manageable.

### Weight Loading Protocol

SPI frame format (MSB first):
```
| MAC_addr[1:0] | Input_addr[2:0] | Weight[3:0] | (unused) |
|    2 bits     |     3 bits      |   4 bits    |  (pad)   |
```

Or bulk load: 128 bits serial stream, loaded into one long shift register.
Clock at 1 MHz: 128 us load time. At 10 Hz classification: 0.13% duty cycle.

---

## 11. Integration with System

### Inputs
- `V[0..7]`: 8 analog feature voltages from Blocks 04/05, range 0.7V–1.2V
  (centered on Vcm = 0.9V).
  - V[0..3]: Spectral band energies from Block 04 (4 frequency bands).
  - V[4]: Broadband RMS from Block 05.
  - V[5]: Crest factor (analog representation, or digitized and re-DAC'd).
  - V[6..7]: Reserved / additional features.
- `SDI, SCK, LE`: SPI interface for weight loading from Block 08.
- `CLK_classify`: Classification trigger from Block 08 (10 Hz).
- `VDD` = 1.8V, `VSS` = 0V.

### Outputs
- `CLASS[1:0]`: 2-bit class label (0 = normal, 1 = inner race, 2 = outer race,
  3 = ball fault).
- `VALID`: Classification valid strobe.
- `SCORE[0..3]`: 4 analog score voltages (optional, for debugging via ADC).

### Timing Sequence
1. Block 08 MCU loads weights via SPI (128 us, done once at startup).
2. Feature extraction blocks (04/05) produce stable feature voltages.
3. MCU asserts CLK_classify.
4. Classifier runs: reset (100 ns) → sample (200 ns) → evaluate (200 ns) →
   compare (6 × 100 ns for sequential WTA) → total ~1.1 us.
5. CLASS[1:0] and VALID go high.
6. MCU reads CLASS, logs result, goes back to sleep.

---

## 12. Comparison: Our Design vs. SOTA

| Parameter | EnCharge AI | KAIST ISSCC23 | Samsung JSSC22 | **VibroSense B06** |
|-----------|-------------|---------------|-----------------|-------------------|
| Process | 16nm | 28nm | 28nm | **130nm (SKY130)** |
| Array size | 256×256+ | 256×256 | 128×128 | **8×4** |
| Weight bits | 4-8 | 4 | 4 | **4** |
| Throughput | 200 TOPS | 4.1 TOPS | 1.2 TOPS | **80 kOPS** |
| Efficiency | 100+ TOPS/W | 12.4 TOPS/W | 5.4 TOPS/W | **~470 TOPS/W** * |
| Cap unit | ~1 fF | ~10 fF | ~5 fF | **50 fF** |
| Area | ~10 mm^2 | 0.78 mm^2 | 1.2 mm^2 | **0.015 mm^2** |

*470 TOPS/W is misleading — it only accounts for the MAC energy (17 fJ per
32 MACs = 0.53 fJ/MAC = 1/0.53f = 1.9 TOPS/W equivalent). At chip level with
all overhead, efficiency is much lower. The point is not to compete on throughput
but to demonstrate the principle.

---

## 13. Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Charge injection > 1 LSB | HIGH | Bottom-plate sampling, dummy switches, slow clocks |
| Comparator offset > score difference | HIGH | Offset calibration, majority voting |
| Cap mismatch degrades weight precision | LOW | Unit-element design, common-centroid layout |
| Signed weights needed but not implemented | MEDIUM | Add sign-inversion switches if Block 09 requires |
| Bitline leakage during evaluate | LOW | Short evaluate phase (200 ns), adequate at all corners |
| SPI loading errors | LOW | Read-back verification (shift out and compare) |

---

## 14. References

1. H. Valavi et al., "A 64-Tile 2.4-Mb In-Memory-Computing CNN Accelerator Employing
   Charge-Domain Compute," JSSC 2019.
2. S. Gonugondla et al., "Fundamental Limits on Energy-Efficient Charge-Domain CIM,"
   JSSC 2020.
3. D. Bankman et al., "An Analog-to-Information Converter for ML Inference,"
   Nature Electronics 2023.
4. KAIST, "A 4-bit Charge-Domain CIM Macro," ISSCC 2023.
5. Samsung, "A 5.4-TOPS/W Charge-Domain CIM," JSSC 2022.
6. EnCharge AI, "200 TOPS Analog In-Memory Compute," Hot Chips 2023.
7. B. Razavi, "The StrongARM Latch," IEEE SSC Magazine, 2015.

---

## 15. Checklist

- [ ] Unit cap (50 fF) designed and characterized: C value, matching, parasitics
- [ ] Binary-weighted bank (1C/2C/4C/8C) verified: monotonic, DNL < 0.5 LSB
- [ ] Switch charge injection measured: < 1 LSB with bottom-plate sampling
- [ ] Single MAC linearity: all 16 weight codes swept, monotonic, INL < 2 LSB
- [ ] Multi-input MAC: 8 inputs active, summation matches ideal within 2 LSB
- [ ] Weight shift register: all 128 bits load and read back correctly via SPI
- [ ] StrongARM comparator: resolves 2 mV in < 50 ns
- [ ] WTA: correctly identifies highest score for all 4-class combinations
- [ ] Full classification: CWRU test vectors correctly classified (all 4 classes)
- [ ] Charge injection test: zero-input residual < 1 LSB on bitline
- [ ] Monte Carlo 100 runs: < 5% misclassification rate due to mismatch
- [ ] Corner analysis: classification correct at all 5 process corners
- [ ] Power measurement: < 5 uW average at 10 Hz classification rate
- [ ] Layout: cap array with common-centroid, guard rings, shielded bitlines
