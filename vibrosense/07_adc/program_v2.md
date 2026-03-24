# Block 07: 8-bit SAR ADC — Program v2 (Tape-Out Quality)

## ABSOLUTE RULES — READ BEFORE ANYTHING ELSE

### Rule 1: NO PYTHON BEHAVIORAL MODELS FOR ADC PERFORMANCE
**NEVER use Python, numpy, or any scripting language to model the SAR conversion algorithm.**
- DNL, INL, ENOB, SFDR, missing codes — ALL must come from ngspice transient simulation
  of the full transistor-level netlist with the SAR feedback loop closed.
- Python/matplotlib is ONLY allowed for post-processing ngspice output data files
  (parsing `.raw` or `wrdata` text, computing FFT from captured digital codes, plotting).
- If you find yourself writing `class SAR_ADC_Model` or simulating charge redistribution
  in Python — STOP. You are cheating. Delete it and go back to SPICE.
- A "behavioral model that implements the exact SAR algorithm" is worthless. We know the
  algorithm works. We need to know if the CIRCUIT works.

### Rule 2: EVERY TRANSISTOR MUST BE A SKY130 DEVICE
- Every switch in the cap DAC must be a real `sky130_fd_pr__nfet_01v8` or `pfet_01v8`
  transmission gate — NOT a `.model SWMOD SW` ideal switch.
- The sample-and-hold switch must be a bootstrapped NMOS or CMOS TG with real devices.
- All capacitors must use `sky130_fd_pr__cap_mim_m3_1` or `sky130_fd_pr__cap_mim_m3_2`
  — NOT ideal `C` elements. If MIM cap models are unavailable, use `C` elements BUT
  document this explicitly as a known approximation and explain the parasitic impact.
- All logic gates (inverters, NANDs, NORs, flip-flops) must be either:
  (a) Transistor-level (hand-designed CMOS gates), OR
  (b) XSPICE `d_dff`, `d_and`, `d_or` digital primitives with proper timing, OR
  (c) ngspice `adevice` Verilog-A co-simulation.
  They must NOT be ideal `E` voltage-controlled voltage sources or `B` arbitrary sources
  pretending to be logic.

### Rule 3: CLOSED-LOOP SIMULATION OR IT DIDN'T HAPPEN
The following signal path MUST exist in ONE ngspice netlist, simultaneously:
```
Vin → sample switch → top plate → cap DAC → comparator input
                                                    ↓
                                              comparator output
                                                    ↓
                                              SAR logic (XSPICE or transistor)
                                                    ↓
                                              DAC switch control → cap DAC bottom plates
```
If the SAR logic is not driving the DAC switches based on comparator output in the same
simulation, you do NOT have a working ADC. You have disconnected sub-blocks.

### Rule 4: HONEST PLOTS OR NO PLOTS
- Every plot in the README must come from actual simulation data files.
- The README must state the exact ngspice command and source data file for each plot.
- If a simulation fails or a spec fails, say so. Do NOT fall back to a behavioral model
  to produce a "passing" result. A failing real simulation is worth more than a passing
  fake one.
- If the ENOB is 5.3 bits, report 5.3 bits. Then explain what limits it and how to fix it.

### Rule 5: NO FAKE CORNERS OR MONTE CARLO
- Corner simulations must use the actual SKY130 corner model files (tt, ss, ff, sf, fs)
  via `.lib "sky130.lib.spice" ss` etc. — NOT by hand-adjusting offset parameters in Python.
- Monte Carlo must use ngspice `.param` with `agauss()` or `aunif()` on device parameters,
  OR use the SKY130 `mc_mm_switch=1` mismatch models.
- If you cannot run real Monte Carlo, say "Monte Carlo not implemented — requires SKY130
  statistical models" and move on. Do NOT fake it with `np.random.normal`.

### Rule 6: USE THE REAL PDK
- You MUST use the SkyWater SKY130 PDK models. The PDK is typically at:
  `$PDK_ROOT/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice`
- If the PDK is not installed, install it:
  ```bash
  pip install volare
  volare enable --pdk sky130 6d4d11780c40b20ee63cc98e645307a9bf2b2ab8
  ```
  Or clone from: https://github.com/google/skywater-pdk-libs-sky130_fd_pr
- Do NOT write your own "minimal" model files with hand-typed BSIM4 parameters.
  These will be wrong and produce meaningless results.
- If the full PDK model is too slow, you may extract individual corner files, but they
  must be the ACTUAL files from the PDK, not hand-written approximations.

---

## 1. Objective

Design an 8-bit successive approximation register (SAR) ADC for on-demand digitization
of analog feature voltages. The ADC must be tape-out quality: every node, every device,
every timing relationship must be verified in transistor-level SPICE simulation with the
SAR feedback loop closed.

Key requirement: ON-DEMAND ADC. Sleeps at <0.5 uW, activates only when MCU requests
a conversion at 10 Hz. 10 clock cycles per conversion at 100 kHz = 10 kS/s.

---

## 2. Specifications (ALL must be verified in ngspice)

| # | Parameter | Spec | How to Measure | Gate |
|---|-----------|------|----------------|------|
| 1 | ENOB | >= 7.0 bits | FFT of 1024 coherent-sampled codes from ngspice transient | MUST PASS |
| 2 | Max \|DNL\| | < 0.5 LSB | Code density histogram from ngspice slow-ramp transient | MUST PASS |
| 3 | Max \|INL\| | < 0.5 LSB | Cumulative sum of DNL from ngspice | MUST PASS |
| 4 | Missing codes | 0 | Histogram — no zero bins in codes 1-254 | MUST PASS |
| 5 | Sample rate | >= 10 kSPS | 10 clock cycles × 100 kHz clock | MUST PASS |
| 6 | Active power | < 100 uW | `.meas tran` I(VDD) during conversion, ngspice | MUST PASS |
| 7 | Sleep power | < 0.5 uW | `.meas tran` I(VDD) with SLEEP asserted, ngspice | MUST PASS |
| 8 | Wakeup time | < 10 us | `.meas tran` TRIG/TARG from sleep de-assert to valid output | MUST PASS |
| 9 | Input range | 0 – 1.2V | Transfer function from ngspice ramp test | MUST PASS |
| 10 | Corners pass | All 5 | ENOB >= 7.0 at TT/SS/FF/SF/FS with real model files | SHOULD PASS |

---

## 3. Architecture

### 3.1 Top-Level

```
Vin ─── [Bootstrap/TG Switch] ─── Vtop (shared top plate)
                                        │
                    ┌───────────────────┤────────────────────┐
                   128C               64C    ...           1C   Cdummy
                    │                  │                     │      │
                [TG sw7]          [TG sw6]    ...       [TG sw0]  GND
                Vref/GND          Vref/GND              Vref/GND
                                        │
                                   ┌────┴────┐
                                   │Comparator│
                                   │Pre-Amp + │
                                   │StrongARM │
                                   └────┬────┘
                                        │ comp_out
                                   ┌────┴────┐
                                   │SAR Logic │──── D[7:0]
                                   │(XSPICE)  │──── VALID
                                   └────┬────┘
                                        │
                              sw[7:0] → DAC switches
```

### 3.2 Cap DAC — MUST use real switch transistors

Each bit switch is a CMOS transmission gate:
```spice
* Bit k switch — connects bottom plate to Vref or GND
.subckt bit_switch in_vref in_gnd out ctrl ctrl_n vdd vss
* When ctrl=HIGH: connect to Vref
XM_vref_n in_vref out ctrl  vss sky130_fd_pr__nfet_01v8 w=1u l=0.15u
XM_vref_p in_vref out ctrl_n vdd sky130_fd_pr__pfet_01v8 w=2u l=0.15u
* When ctrl=LOW: connect to GND (inverted control)
XM_gnd_n  in_gnd  out ctrl_n vss sky130_fd_pr__nfet_01v8 w=1u l=0.15u
XM_gnd_p  in_gnd  out ctrl  vdd sky130_fd_pr__pfet_01v8 w=2u l=0.15u
.ends
```
This is the MINIMUM acceptable switch implementation. Ideal `S` switches are NOT acceptable.

Note: The switch sizing above is a starting point. You may need to adjust W/L for:
- Charge injection matching (make NMOS and PMOS inject equal and opposite charge)
- Ron < 1k to settle within 1 clock period (Ron × Ctotal < Tclk / 10)
- Leakage in sleep mode

### 3.3 Comparator — StrongARM with pre-amplifier

Same topology as program.md v1. The comparator design from v1 was actually good
(real transistors, real SKY130 models, real ngspice). Keep it.

**Mandatory verification:**
1. Input-referred offset: DC sweep, measure crossover point
2. Decision speed: Apply 1-LSB step (4.7 mV), measure time to valid output
3. Minimum resolvable input: Find smallest Vdiff that produces correct output in 5 us
4. Power: `.meas` I(VDD) averaged over one clock cycle

### 3.4 SAR Logic — MUST be in SPICE, not external

**Option A (recommended): XSPICE digital primitives**

ngspice has built-in digital primitives. Use them:
```spice
* D flip-flop
aff1 d1 clk null null q1 qb1 dflop1
.model dflop1 d_dff rise_delay=1n fall_delay=1n

* AND gate
aand1 [a1 a2] out1 and1
.model and1 d_and rise_delay=0.5n fall_delay=0.5n

* Inverter
ainv1 in1 out1 inv1
.model inv1 d_inverter rise_delay=0.5n fall_delay=0.5n
```

Build the SAR state machine from these primitives:
- 10-state counter (shift register or decoded)
- 8-bit result register (D flip-flops)
- Comparator output sampling logic
- DAC switch drivers

The digital outputs drive analog transmission gate switches via `adc_bridge` and
`dac_bridge` XSPICE elements:
```spice
* Bridge from analog comparator output to digital SAR input
abridge_comp [comp_outp] [comp_digital] adc_buf
.model adc_buf adc_bridge in_low=0.6 in_high=1.2

* Bridge from digital SAR output to analog DAC switch control
abridge_dac [d7 d6 d5 d4 d3 d2 d1 d0] [sw7 sw6 sw5 sw4 sw3 sw2 sw1 sw0] dac_buf
.model dac_buf dac_bridge out_low=0 out_high=1.8 t_rise=1n t_fall=1n
```

**Option B: Full transistor-level logic**

Design CMOS gates from sky130 transistors:
- CMOS inverter: 1 NMOS + 1 PFET
- NAND2: 2 NMOS series + 2 PMOS parallel
- DFF: Two transmission-gate latches (master-slave), ~16 transistors each
- Total: ~200 transistors for the SAR logic

This is more work but eliminates any digital model approximations.

**Option C: ngspice Verilog-A co-simulation**

If ngspice is compiled with `--enable-cider` or has Verilog-A support:
```spice
.hdl "sar_logic.va"
XSAR clk comp_out d7 d6 d5 d4 d3 d2 d1 d0 sample valid sar_logic
```

**What is NOT acceptable:**
- `E` or `B` sources that output pre-computed DAC codes
- Python scripts that inject control signals between simulation steps
- Any approach where the SAR logic is not part of the ngspice simulation

### 3.5 Power Gating

PMOS header on comparator VDD. Same as v1 — that part was fine.

---

## 4. Required Testbenches (ALL must run in ngspice)

### TB1: Single Conversion Verification (`tb_single_conv.spice`)

The MOST IMPORTANT testbench. Must demonstrate ONE complete conversion:
- Apply DC input (e.g., Vin = 0.47V, expected code ~ 100)
- Assert CONVERT
- Watch SAR logic step through 8 bits
- See each DAC switch toggle in sequence
- See comparator make 8 decisions
- See correct output code on D[7:0]

**Plot required:** Time-domain waveform showing:
- Vin (DC)
- Vtop (top plate — should show staircase as DAC switches toggle)
- CLK
- comp_out
- D[7], D[6], ..., D[0] (all 8 bits)
- VALID

This is the proof that the ADC works. Without this plot, nothing else matters.

### TB2: Multi-Code Verification (`tb_multi_code.spice`)

Run 8-16 conversions at different input voltages (0V, 0.15V, 0.3V, ... 1.2V).
Verify that the output codes are correct (within ±1 LSB of ideal).

This can be a single long transient with stepped input:
```spice
Vin inp 0 PWL(0 0.0  200u 0.0  200.1u 0.15  400u 0.15  400.1u 0.3 ...)
```

### TB3: DNL/INL via Code Density (`tb_dnl_inl.spice`)

Slow ramp input covering 0V to 1.2V. The ADC must convert continuously.
Need at least 256 × 16 = 4096 conversions for statistical significance.
At 10 kS/s, this is a 0.41-second simulation — may be slow. Options:
- Increase clock to 1 MHz for this test (100x faster, same circuit behavior
  if settling is fast enough)
- Accept 10-minute ngspice runtime
- Use fewer conversions (256 × 4 = 1024 minimum) with wider error bars

**Post-processing (Python allowed here):**
Read the D[7:0] outputs from ngspice wrdata. Build histogram. Compute DNL/INL.
Plot. This is legitimate use of Python — processing SPICE output, not replacing SPICE.

### TB4: ENOB via FFT (`tb_enob.spice`)

Coherent sine input, 1024 conversions. Same rules as TB3 — may need faster clock.
```
fin = fs × M / N,  M = 501 (prime),  N = 1024
```

**Post-processing (Python allowed):** FFT of captured codes, compute SNDR, ENOB.

### TB5: Active Power (`tb_power_active.spice`)

`.meas tran Iavg AVG I(VDD)` over one full conversion. Multiply by VDD.

### TB6: Sleep Power (`tb_power_sleep.spice`)

Assert SLEEP, wait 10 us for settling, measure average VDD current.
`.meas tran Isleep AVG I(VDD) FROM=10u TO=100u`

### TB7: Wakeup Time (`tb_wakeup.spice`)

De-assert SLEEP, start clocking, measure time to first valid output.

### TB8: Corner Simulations (`tb_corner_*.spice`)

Run TB1 (single conversion) at all 5 corners with real PDK model files:
```spice
.lib "$PDK_ROOT/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice" ss
```
Verify correct output code at each corner.

If TB3/TB4 are too slow per corner, at minimum run TB2 (multi-code) at each corner.

### TB9: Monte Carlo — OPTIONAL but honest

If you implement Monte Carlo:
- Use `agauss()` on cap values: `C128 = {128 * Cunit * (1 + agauss(0, 0.00156, 3))}`
- Use `agauss()` on comparator pair Vth: `.param vos = agauss(0, 1.77m, 3)`
- Run 20-50 iterations minimum
- Report yield: fraction of runs where all specs pass

If you cannot implement it properly, state: "Monte Carlo deferred — requires parametric
sweep infrastructure. Analytical mismatch budget provided instead." Then show the math.

---

## 5. Design Flow

### Step 1: Install PDK and verify models
```bash
# Verify SKY130 models exist
ls $PDK_ROOT/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice
# If not, install via volare or clone
```
Run a simple inverter simulation to confirm models work.

### Step 2: Comparator standalone verification
Already done in v1. Re-verify with correct PDK models if v1 used hand-written models.

### Step 3: Build DAC with real switches
Replace ideal `S` switches with CMOS TG subcircuits. Verify:
- Switching time (step response, measure 10-90% settling)
- Charge injection (switch with no input, measure voltage glitch on top plate)
- Leakage (hold mode, measure voltage droop over 100 us)

### Step 4: Build SAR logic in XSPICE
Implement the state machine. Test standalone:
- Apply a known sequence of comp_out values, verify DAC switch sequence
- Verify timing (all state transitions on clock edges)

### Step 5: Connect everything — closed-loop single conversion
THIS IS THE CRITICAL STEP. Connect comparator + DAC + SAR + sample switch.
Apply a known DC input. Run transient. Verify correct output code.
Debug until it works. This may take many iterations.

Common failure modes:
- Comparator polarity wrong (outputs inverted)
- DAC switch control polarity wrong (sets bit when it should clear)
- Timing race (comparator not settled before SAR samples its output)
- Charge injection from switches corrupting top plate voltage
- Missing reset/initialization at start of conversion

### Step 6: Run all testbenches
Once TB1 passes, run TB2-TB9 sequentially. Fix any failures.

### Step 7: Write README with real results
Every number in the README must have a source ngspice simulation behind it.
Every plot must come from ngspice data. State which testbench produced each result.

---

## 6. Simulation Performance Expectations

Be realistic about ngspice runtime:
- TB1 (single conversion, 100 us): ~2-10 seconds
- TB2 (16 conversions, 1.6 ms): ~30-60 seconds
- TB3 (4096 conversions at 10 kS/s, 410 ms): ~30-60 MINUTES
  - Mitigation: run at 1 MHz clock → 4.1 ms sim time → ~2-5 minutes
  - Or reduce to 1024 conversions → ~10 minutes
- TB4 (1024 conversions): ~10-20 minutes at 10 kS/s, ~1-2 minutes at 1 MHz
- TB5-TB7: < 30 seconds each
- TB8 (5 corners × TB1): ~5-10 minutes total

Total: expect 1-2 hours of simulation time. This is NORMAL for a real ADC design.
Do not try to shortcut by replacing SPICE with Python.

If simulations are too slow, acceptable mitigations:
1. Run DNL/INL with faster clock (1 MHz instead of 100 kHz) — same circuit,
   just faster. Document this and note that the real ADC runs at 100 kHz.
2. Reduce FFT size to 256 or 512 points — lower frequency resolution but valid ENOB.
3. Run corners on TB1 only (single conversion) instead of full DNL/INL per corner.

NOT acceptable mitigations:
- Replacing the circuit with a Python model
- Using ideal switches "to speed up simulation"
- Skipping the closed-loop simulation entirely

---

## 7. README Requirements

The README.md must contain:

### Section 1: Architecture
- Block diagram
- Sub-block descriptions
- All transistor sizes in a table (W, L, multiplier, role)
- All capacitor values

### Section 2: Closed-Loop Verification
- **THE plot**: TB1 single conversion waveform showing the SAR algorithm
  operating on the real circuit (Vtop staircase, bit decisions, final code)
- TB2 multi-code transfer function

### Section 3: Static Performance
- DNL/INL plots from TB3
- Exact command used to run TB3
- Data file referenced

### Section 4: Dynamic Performance
- FFT spectrum plot from TB4
- ENOB, SNDR, SFDR numbers
- Exact command used

### Section 5: Power
- Active power from TB5
- Sleep power from TB6
- Wakeup time from TB7

### Section 6: Corner Analysis
- Table of results per corner from TB8
- Which corners pass/fail

### Section 7: Monte Carlo (if implemented)
- Distribution plots
- Yield numbers
- Or explicit statement that MC was not implemented and why

### Section 8: Spec Summary Table
- All 10 specs with PASS/FAIL
- Source testbench for each measurement

### Section 9: Honest Assessment
- What works, what doesn't
- What would break at tape-out
- What the design margin is
- Known risks and mitigations

---

## 8. What "Done" Looks Like

**Minimum viable (all MUST PASS):**
- [ ] TB1: Single conversion produces correct code — proven in ngspice with full
      closed-loop (comparator + DAC + SAR logic + sample switch)
- [ ] TB2: Transfer function is monotonic across 0-1.2V range
- [ ] TB5: Active power < 100 uW measured in ngspice
- [ ] TB6: Sleep power < 0.5 uW measured in ngspice
- [ ] TB7: Wakeup < 10 us measured in ngspice
- [ ] README documents all results with plots from real SPICE data

**Full qualification (add these if time permits):**
- [ ] TB3: DNL < 0.5 LSB, INL < 0.5 LSB from code density
- [ ] TB4: ENOB >= 7.0 bits from FFT
- [ ] TB8: All 5 corners pass
- [ ] TB9: Monte Carlo yield > 95%
- [ ] SAR logic Verilog file for digital synthesis

**If specs fail, the design is still valuable IF:**
- The failure is honestly reported with root cause analysis
- A concrete fix is proposed (e.g., "increase input pair W to 16u to fix offset")
- The closed-loop simulation demonstrably works (correct conversion sequence)
- Only the MAGNITUDE of a parameter is off, not the fundamental operation

---

## 9. Common Pitfalls — Avoid These

1. **"The behavioral model shows ENOB = 7.93"** — This is testing the SAR algorithm,
   not the circuit. Delete the behavioral model.

2. **"Corner analysis with offset = 0.5 mV"** — This is making up numbers, not running
   real corners. Use actual PDK corner files or don't claim corner analysis.

3. **"Monte Carlo with np.random.normal"** — This is not Monte Carlo. This is random
   number generation. Use ngspice parametric sweep or don't claim MC.

4. **"ENOB is constant across all corners"** — Impossible in a real circuit. If your
   corners show identical ENOB, your corner analysis is fake.

5. **"Max DNL = 0.063 LSB"** — Suspiciously close to 1/16 = 0.0625. This is likely
   from an ideal model with exactly 64 samples per code. Real circuits show DNL
   patterns correlated with bit transitions (especially at major carries like code 128).

6. **"Sleep power = 0.37 nW"** — This might be real for just the comparator, but the
   full ADC includes DAC switches, sample switch, and SAR logic leakage. Measure the
   COMPLETE circuit in sleep mode.

7. **Plotting the wrong columns from wrdata** — ngspice `wrdata` interleaves variables.
   For 4 variables: rows 0..N are var1, N+1..2N are var2, etc. Parse carefully.

---

## 10. Git Commit Guidelines

Commit after each milestone:
1. After comparator re-verification with real PDK: `design(sar_adc_v2): comparator verified with SKY130 PDK`
2. After DAC with real switches: `design(sar_adc_v2): cap DAC with transistor-level TG switches`
3. After SAR logic in XSPICE: `design(sar_adc_v2): SAR logic implemented in XSPICE digital`
4. After first closed-loop conversion: `design(sar_adc_v2): first closed-loop conversion verified`
5. After full qualification: `design(sar_adc_v2): full ADC qualification — TB1-TB8 results`

Each commit message must be honest about what was actually verified.

---

*This program demands real circuit design, not algorithm verification.*
*Every number in the final README must trace back to an ngspice simulation.*
*If it can't be simulated in SPICE, it can't be taped out.*
