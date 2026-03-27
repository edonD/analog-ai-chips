# PVDD 5V LDO Regulator — Design Program

## Absolute Rules

**READ THESE BEFORE DOING ANYTHING. VIOLATIONS WILL INVALIDATE THE ENTIRE DESIGN.**

1. **USE THE REAL SKY130 PDK MODELS. ALWAYS.** Every transistor, resistor, and capacitor must be an instantiated Sky130 device (`sky130_fd_pr__nfet_01v8`, `sky130_fd_pr__pfet_01v8`, `sky130_fd_pr__nfet_g5v0d10v5`, `sky130_fd_pr__pfet_g5v0d10v5`, `sky130_fd_pr__res_*`, `sky130_fd_pr__cap_mim_m3_1`, etc.). No exceptions.

2. **NO BEHAVIORAL MODELS, NO PYTHON APPROXIMATIONS, NO IDEAL COMPONENTS IN THE DESIGN.** When a circuit is difficult to converge or simulate, you fix the circuit or the testbench — you do NOT replace real devices with ideal sources, behavioral VerilogA models, or Python/numpy stand-ins. The ONLY ideal components allowed are:
   - `V_AVBG` (bandgap reference, 1.226V DC source) — this is an external chip block
   - `I_BIAS` (current reference, 1uA DC source) — this is an external chip block
   - `V_BVDD` (battery supply source for testbenches)
   - `V_SVDD` (2.2V supply for testbenches)
   - Testbench stimulus sources (pulse, sine, PWL for transient tests)
   - Load resistors/capacitors in testbenches

3. **ALL SIMULATIONS IN NGSPICE.** No HSPICE, no Spectre, no Xyce. The design must simulate correctly in ngspice with the Sky130 PDK `.lib.spice` models. If ngspice has convergence issues, fix them with `.option` settings (reltol, abstol, gmin, etc.) — do not switch simulators or replace devices.

4. **EVERY SPEC MUST BE VERIFIED BY SIMULATION, NOT BY CALCULATION.** Hand calculations are for initial sizing only. The final claimed performance must come from an ngspice `.spice` testbench that anyone can re-run. If you cannot simulate it, you cannot claim it.

5. **WHEN THINGS GET HARD, YOU PUSH THROUGH.** LDO design is hard. The loop will oscillate. The startup will latch. The pass device will not have enough headroom. The compensation will be wrong. Convergence will fail. NONE of these are reasons to simplify the circuit, replace devices with behavioral models, or skip verification. Iterate on the real circuit until it works.

---

## Process: SkyWater SKY130A

### PDK Setup

```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
* Corner options: tt, ss, ff, sf, fs
* Temperature: .temp 27 (sweep -40 to 150)
```

### Available Devices

**Standard 1.8V devices (for error amp, feedback, compensation, UV/OV):**
- `sky130_fd_pr__nfet_01v8` — NMOS, Vds_max = 1.8V
- `sky130_fd_pr__pfet_01v8` — PMOS, Vds_max = 1.8V

**5V / 10.5V high-voltage devices (for pass device, level shifter, protection):**
- `sky130_fd_pr__nfet_g5v0d10v5` — HV NMOS, Vds_max = 10.5V
- `sky130_fd_pr__pfet_g5v0d10v5` — HV PMOS, Vds_max = 10.5V
- `sky130_fd_pr__nfet_05v0` — 5V NMOS (thick oxide)
- `sky130_fd_pr__pfet_05v0` — 5V PMOS (thick oxide)

**Resistors:**
- `sky130_fd_pr__res_xhigh_po` — high-R polysilicon (~2 kohm/sq, low TC)
- `sky130_fd_pr__res_high_po` — medium-R polysilicon
- `sky130_fd_pr__res_generic_nd` — N-diffusion resistor
- `sky130_fd_pr__res_generic_pd` — P-diffusion resistor
- `sky130_fd_pr__res_iso_pw` — isolated P-well (~3.5 kohm/sq, high TC)

**Capacitors:**
- `sky130_fd_pr__cap_mim_m3_1` — MIM cap (~2 fF/um^2)
- `sky130_fd_pr__cap_mim_m3_2` — MIM cap (second layer)
- MOS cap (gate cap of large MOSFET) — for large values

**Diodes:**
- `sky130_fd_pr__diode_pw2nd_05v5` — P-well to N-diffusion
- `sky130_fd_pr__diode_pd2nw_05v5` — P-diff to N-well

### Sky130 Constraints to Remember

| Constraint | Value | Impact |
|-----------|-------|--------|
| Max VDS (HV devices) | 10.5V | Input range limited to ~10.5V |
| Max VGS (1.8V devices) | 1.8V | Error amp must run from regulated domain or use cascode protection |
| NMOS Vth (1.8V) | ~0.5-0.7V | Affects input common-mode range |
| PMOS Vth (1.8V) | ~0.7-1.0V | High Vth limits headroom |
| NMOS Vth (5V/10.5V) | ~0.6-0.9V | Higher than 1.8V devices |
| No native 40V devices | -- | Cannot replicate GF130BCD 40V PDMOS directly |
| MIM cap density | ~2 fF/um^2 | 200 pF internal load = ~100,000 um^2 (large) |

---

## Target Specifications

These specs come from the TDK-Micronas HVCM PVDD regulator concept documentation. Adapt input voltage range for Sky130 HV device limits.

| Parameter | Symbol | Min | Typ | Max | Unit | Notes |
|-----------|--------|-----|-----|-----|------|-------|
| Input voltage (BVDD) | V_BVDD | 5.4 | 7.0 | 10.5 | V | Sky130 HV limit; original was 5.4-40V |
| Output voltage (PVDD) | V_PVDD | 4.8 | 5.0 | 5.17 | V | +/-3.5% over PVT and load |
| Dropout voltage | V_DO | -- | 400 | -- | mV | At BVDD=5.4V, full load |
| Load current (active) | I_LOAD | 0 | -- | 50 | mA | Active mode |
| Load current (retention) | I_RET | 0 | -- | 0.5 | mA | Retention / sleep mode |
| Load transient undershoot | dV_US | -- | -- | 150 | mV | 1mA to 10mA step in 1us |
| Load transient overshoot | dV_OS | -- | -- | 150 | mV | 10mA to 1mA step in 1us |
| Internal load cap | C_LOAD | -- | 200 | -- | pF | On-chip, no external cap |
| Line regulation | LNR | -- | -- | 5 | mV/V | dVPVDD/dVBVDD at fixed load |
| Load regulation | LDR | -- | -- | 2 | mV/mA | dVPVDD/dILOAD at fixed BVDD |
| Quiescent current (active) | I_Q | -- | -- | 300 | uA | From BVDD, no load |
| Quiescent current (retention) | I_QRET | -- | -- | 10 | uA | Retention mode |
| UV threshold | V_UV | 4.0 | 4.3 | 4.5 | V | PVDD undervoltage flag |
| OV threshold | V_OV | 5.25 | 5.5 | 5.7 | V | PVDD overvoltage flag |
| Phase margin | PM | 45 | -- | -- | deg | All conditions (PVT, load) |
| Gain margin | GM | 10 | -- | -- | dB | All conditions |
| PSRR @ DC | PSRR_DC | 40 | -- | -- | dB | |
| PSRR @ 10kHz | PSRR_10k | 20 | -- | -- | dB | |
| Reference voltage | V_REF | -- | 1.226 | -- | V | Ideal AVBG source |
| Bias current | I_BIAS | -- | 1.0 | -- | uA | Ideal IREF source |
| Temperature range | T_J | -40 | 27 | 150 | C | Automotive (derated from 175C for Sky130) |

---

## Architecture

### LDO Block Diagram

```
    BVDD (5.4-10.5V)
     |
     |     ┌─────────────────┐
     +─────┤ Pass Device      ├─────────┬──── PVDD (5.0V)
     |     │ HV PMOS          │         |
     |     │ sky130 pfet_g5v0 │         |
     |     └────────┬─────────┘    C_LOAD (200pF)
     |              |gate               |
     |         ┌────┴────┐             GND
     |         │  Error   │
     |         │Amplifier │◄──── V_FB (from feedback divider)
     |         │  (OTA)   │
     |         └────┬────┘
     |              |
     |         V_REF (1.226V ideal)
     |
     |     ┌─────────────┐
     +─────┤Level Shifter │◄──── SVDD domain control signals
     |     └─────────────┘
     |
     |     ┌─────────────┐
     +─────┤ Zener Clamp  │──── GND (transient protection)
           └─────────────┘

    PVDD ──┬──[R_TOP]──┬──[R_BOT]── GND
           |           |
           |          V_FB ──► Error Amp (-)
           |
           ├──► UV comparator (threshold ~4.3V)
           ├──► OV comparator (threshold ~5.5V)
           └──► Current sense ──► Current limiter
```

### Pass Device Selection

The pass device is the most critical component. In Sky130:

**Option A: HV PMOS (`sky130_fd_pr__pfet_g5v0d10v5`)**
- Source = BVDD, Drain = PVDD, Gate driven by error amp
- PMOS LDO: low dropout (Vdo = Vds_sat), gate can be pulled to GND
- VDS_max = 10.5V — sufficient for BVDD up to 10.5V
- Challenge: high Vth (~1V), large gate capacitance for W=11mm equivalent

**Option B: HV NMOS (`sky130_fd_pr__nfet_g5v0d10v5`) as source follower**
- Drain = BVDD, Source = PVDD, Gate driven by error amp
- NMOS LDO: higher dropout (Vdo = Vgs > Vth + Vdsat), but faster response
- Needs gate voltage above PVDD by Vgs — requires charge pump or bootstrap
- Not recommended for this design (adds complexity)

**Decision: Use Option A — HV PMOS pass device.** This matches the original GF130BCD PDMOS topology.

### Feedback Divider Ratio

```
V_FB = V_PVDD * R_BOT / (R_TOP + R_BOT) = V_REF = 1.226V

For V_PVDD = 5.0V:
R_BOT / (R_TOP + R_BOT) = 1.226 / 5.0 = 0.2452

If R_BOT = 100 kohm:
R_TOP = R_BOT * (5.0/1.226 - 1) = 100k * 3.078 = 307.8 kohm

Total divider current: 5.0V / (307.8k + 100k) = 12.3 uA
```

Use `sky130_fd_pr__res_xhigh_po` for both resistors (low TC, high R/sq).

---

## Block-by-Block Design Procedure

### Block 00: Error Amplifier

**What it does:** Compares V_FB to V_REF and drives the pass device gate. This is the gain stage that sets regulation accuracy, PSRR, and transient response.

**Topology options to explore:**
1. **Folded-cascode OTA** — high gain (>60 dB) in one stage, wide input range. Same as VibroSense Block 01 but adapted for 5V supply domain.
2. **Two-stage Miller OTA** — higher gain (>80 dB), needs compensation cap. Better load regulation but stability is harder.
3. **Single-stage differential pair with cascode** — simplest, may not achieve enough gain.

**Design targets:**
| Parameter | Target | Why |
|-----------|--------|-----|
| DC gain | >60 dB | For <2 mV/mA load regulation |
| UGB | 200 kHz - 1 MHz | Fast enough for load transient, slow enough for stability |
| Phase margin | >55 deg | With pass device + 200pF Cload in the loop |
| Input offset | <5 mV | Contributes directly to output voltage error |
| Supply | PVDD (5V) or BVDD via LDO | Error amp can run from regulated 5V domain |
| Bias current | 10-50 uA | From IREF via current mirrors |
| Input CM range | Must include 1.226V | Both inputs near bandgap voltage |
| Output swing | Must reach BVDD - Vth_pass | To fully turn on/off the pass device |

**Critical consideration:** The error amp output drives the gate of the HV PMOS pass device. The gate voltage must swing from ~0V (pass device fully ON, PVDD regulated) to ~BVDD (pass device OFF). If the error amp runs from PVDD (5V), its output can swing 0-5V — sufficient since the pass device gate needs to go below BVDD - |Vth| to turn on. BUT during startup, PVDD is not yet established. The error amp needs a bootstrap or must initially run from BVDD through a cascode.

**Procedure:**
1. Choose topology. Start with folded-cascode — it worked for VibroSense.
2. Size the differential pair for offset and noise. W*L > 50 um^2 for each input device.
3. Size tail current for UGB target: GBW = gm / (2*pi*Cload_equiv). The load seen by the error amp is the pass device gate cap (large, ~50-200 pF for W=several mm).
4. Simulate: DC operating point, AC open-loop gain/phase, input offset (Monte Carlo).
5. ALL IN NGSPICE WITH SKY130 MODELS.

**Testbenches to write:**
- `tb_ea_dc.spice` — DC operating point, verify all devices in saturation
- `tb_ea_ac.spice` — Open-loop gain and phase (use ideal feedback break)
- `tb_ea_offset.spice` — Monte Carlo offset (if PDK MC models available)
- `tb_ea_cmrr.spice` — Common-mode rejection
- `tb_ea_psrr.spice` — Power supply rejection

### Block 01: Pass Device

**What it does:** The power MOSFET that drops BVDD down to PVDD. All load current flows through it.

**Device:** `sky130_fd_pr__pfet_g5v0d10v5`

**Sizing procedure:**
1. Look up the device model parameters: Vth, Cox, mobility, lambda.
2. For 50 mA at Vds = 400 mV (dropout), calculate required W/L.
3. In Sky130, the HV PMOS has lower mobility than standard PMOS — expect W to be large (several mm).
4. Simulate: sweep Vgs at Vds = 0.4V, find the W/L that gives 50 mA.
5. Characterize: Id vs Vds family, Cgs vs Vgs, gm vs Id.
6. Extract Rds_on at full gate drive for bypass mode.

**Key concern:** The pass device gate capacitance is the dominant load for the error amplifier. A W=5mm device might have Cgs > 100 pF. This sets the second pole in the LDO loop and directly impacts stability. You MUST characterize Cgs before designing compensation.

**Testbenches:**
- `tb_pass_iv.spice` — Id vs Vds family curves at multiple Vgs
- `tb_pass_cgs.spice` — Gate capacitance vs bias point
- `tb_pass_dropout.spice` — Vout vs Vin at 50 mA to find actual dropout
- `tb_pass_corners.spice` — Repeat above at SS/FF/SF/FS corners and -40/27/150C

### Block 02: Feedback Network

**What it does:** Resistive divider that scales PVDD (5V) to V_REF (1.226V).

**Design:**
- Use `sky130_fd_pr__res_xhigh_po` (low TC polysilicon)
- R_TOP ~ 308 kohm, R_BOT ~ 100 kohm
- Divider current ~ 12 uA (acceptable quiescent current)
- Matching matters — use same resistor type, matched layout (series connection of unit resistors)

**Testbenches:**
- `tb_fb_ratio.spice` — DC ratio accuracy across corners
- `tb_fb_tc.spice` — Temperature coefficient of the ratio (should be near-zero if matched)
- `tb_fb_noise.spice` — Resistor thermal noise contribution

### Block 03: Compensation

**What it does:** Ensures the LDO feedback loop is stable (PM > 45 deg) across all load currents (0 to 50 mA), all temperatures, and all process corners.

**This is the hardest block. Do not shortcut it.**

**LDO pole/zero structure:**
1. **Output pole (dominant):** f_out = 1 / (2*pi * Rload * Cload). At no-load (Rload=100kohm), this is ~8 kHz. At full-load (100 ohm), it moves to ~8 MHz. This pole MOVES by 1000x with load — this is what makes LDO compensation hard.
2. **Gate pole:** f_gate = 1 / (2*pi * Rout_ea * Cgs_pass). Rout_ea is the error amp output impedance, Cgs_pass is the pass device gate cap. Typically 10-500 kHz.
3. **ESR zero (if external cap):** Not applicable here — internal cap only, negligible ESR.

**Compensation strategies to explore:**
1. **Miller compensation** — cap from error amp output to pass device drain (PVDD). Creates pole-splitting. Standard approach.
2. **Dominant-pole at gate** — make the gate pole dominant by adding cap at error amp output. Simple but limits bandwidth.
3. **Adaptive biasing** — increase error amp bias current at high load (when output pole moves to high frequency). Improves transient response.
4. **Nested Miller** — if using a two-stage error amp.

**Procedure:**
1. First, close the loop with just error amp + pass device + feedback divider + 200 pF Cload. NO compensation.
2. Run loop stability (LSTB or break-loop AC analysis). Measure gain, phase margin, gain margin.
3. Identify the pole locations. You will see the problem.
4. Add compensation. Re-simulate.
5. Sweep load from 0 to 50 mA. Phase margin must be >45 deg at EVERY load point.
6. Sweep temperature -40 to 150C. Still stable?
7. Sweep corners SS/FF/SF/FS. Still stable?
8. Monte Carlo (if models support it). PM > 45 deg at 2-sigma?

**Testbenches:**
- `tb_comp_lstb.spice` — Loop stability (break loop at feedback node, AC analysis)
- `tb_comp_load_sweep.spice` — PM vs load current (parametric sweep)
- `tb_comp_pvt.spice` — PM across all 5 corners and 3 temperatures
- `tb_comp_transient.spice` — Step response (complement to AC analysis)

### Block 04: Current Limiter

**What it does:** Prevents pass device destruction if output is shorted or overloaded.

**Topology:** Sense the current through the pass device using a scaled mirror (1:N ratio — small sense device mirrors a fraction of the main pass device current). Compare sense current to a reference. When exceeded, clamp the error amp output to limit gate drive.

**Design targets:**
| Parameter | Target |
|-----------|--------|
| Current limit threshold | 60-80 mA (20-60% above 50 mA max load) |
| Accuracy | +/-20% over PVT (acceptable for protection) |
| Response time | < 10 us |
| Power overhead | < 10 uA (sense transistor leakage) |

**Testbenches:**
- `tb_ilim_dc.spice` — Iout vs Vout curve showing current limiting
- `tb_ilim_short.spice` — Transient response to output short-circuit
- `tb_ilim_corners.spice` — Limit threshold across PVT

### Block 05: UV/OV Comparators

**What it does:** Monitors PVDD output and flags undervoltage (<4.3V) or overvoltage (>5.5V) conditions.

**Topology:** Two continuous-time comparators with hysteresis, referenced to scaled versions of V_REF.

**Design targets:**
| Parameter | UV | OV |
|-----------|----|----|
| Threshold | 4.3V +/-0.3V | 5.5V +/-0.2V |
| Hysteresis | 50-100 mV | 50-100 mV |
| Response time | < 5 us | < 5 us |
| Power | < 5 uA each | < 5 uA each |

**Testbenches:**
- `tb_uv_threshold.spice` — Sweep PVDD, find UV trip point
- `tb_ov_threshold.spice` — Sweep PVDD, find OV trip point
- `tb_uvov_hyst.spice` — Verify hysteresis on both comparators
- `tb_uvov_corners.spice` — Threshold accuracy across PVT

### Block 06: Level Shifter

**What it does:** Translates digital control signals from SVDD domain (2.2V) to BVDD/PVDD domain (5-10.5V) and vice versa.

**Topology:** Cross-coupled PMOS level shifter (standard). Input: 0/2.2V SVDD logic. Output: 0/BVDD or 0/PVDD logic.

**Key signals to shift:**
- Enable (SVDD → BVDD domain)
- Mode control bits (SVDD → BVDD)
- UV/OV flags (PVDD domain → SVDD)

Use `sky130_fd_pr__pfet_g5v0d10v5` and `sky130_fd_pr__nfet_g5v0d10v5` for the high-side.

**Testbenches:**
- `tb_ls_function.spice` — Verify logic level translation
- `tb_ls_delay.spice` — Propagation delay
- `tb_ls_supply.spice` — Function across BVDD range 5.4-10.5V

### Block 07: Zener Clamp

**What it does:** Protects PVDD output from voltage transients. Clamps overshoot during load dump or fast BVDD ramps.

**Sky130 implementation:** Use reverse-biased diode stacks (`sky130_fd_pr__diode_pw2nd_05v5`) to create a clamp at ~5.5-6V. Or use a thick-oxide NMOS with gate-drain clamp configuration.

**Testbenches:**
- `tb_zener_iv.spice` — I-V characteristic of the clamp
- `tb_zener_transient.spice` — Clamping behavior during voltage spike

### Block 08: Mode Control

**What it does:** Manages transitions between operating modes (POR → retention → power-up → active) based on BVDD voltage thresholds.

**Implementation:** Comparators sensing BVDD voltage + combinational logic generating:
- Bypass switch enable (shorts pass device ON for bypass mode)
- Error amp enable
- Reference select (4.1V target in retention regulate vs 5.0V in active)
- UV/OV comparator enable

**Testbenches:**
- `tb_mode_transitions.spice` — BVDD ramp from 0 to 10.5V, verify all mode transitions
- `tb_mode_fast_ramp.spice` — 10V/us BVDD ramp (automotive cold-crank)
- `tb_mode_slow_ramp.spice` — 0.1V/us BVDD ramp

### Block 09: Startup

**What it does:** Ensures the LDO starts correctly from a de-energized state. The error amplifier cannot function until its own supply (PVDD or a pre-regulated voltage) is established — this creates a chicken-and-egg problem.

**Startup strategies:**
1. **Bootstrap from BVDD:** Initially power the error amp from BVDD through a resistor/diode. As PVDD ramps up, switch to PVDD supply.
2. **Current-limited pulldown on pass gate:** A weak pulldown turns the pass device partially ON to bootstrap PVDD.
3. **Dedicated startup amplifier:** A simple, low-power amplifier that operates from BVDD directly (using HV devices) and hands off to the main error amp once PVDD is established.

**Testbenches:**
- `tb_startup_ramp.spice` — BVDD ramp from 0 to 10.5V at various slew rates
- `tb_startup_pvt.spice` — Startup across all corners and temperatures
- `tb_startup_loaded.spice` — Startup with 50 mA load applied immediately

### Block 10: Top Integration

**What it does:** Connects all blocks into the complete PVDD regulator and runs full verification.

**Full verification plan (ALL IN NGSPICE, ALL WITH SKY130 PDK):**

| # | Test | Stimulus | Pass Criteria |
|---|------|----------|---------------|
| 1 | DC regulation | BVDD=7V, sweep Iload 0-50mA | VPVDD = 5.0V +/-3.5% |
| 2 | Line regulation | Iload=10mA, sweep BVDD 5.4-10.5V | dVPVDD < 5 mV/V |
| 3 | Load regulation | BVDD=7V, sweep Iload 0-50mA | dVPVDD < 2 mV/mA |
| 4 | Load transient | 1mA→10mA step, 1us rise | Undershoot < 150 mV |
| 5 | Load transient | 10mA→1mA step, 1us fall | Overshoot < 150 mV |
| 6 | Loop stability | LSTB at Iload=0, 1mA, 10mA, 50mA | PM > 45 deg, GM > 10 dB |
| 7 | PSRR | AC on BVDD, measure at PVDD | >40 dB @ DC, >20 dB @ 10kHz |
| 8 | Startup | BVDD ramp 0→10.5V at 1V/us | Monotonic, no oscillation, settle <100us |
| 9 | Startup (fast) | BVDD ramp 0→10.5V at 10V/us | No overshoot >5.5V |
| 10 | Dropout | Iload=50mA, sweep BVDD 4.5→6V | VPVDD within 100mV of BVDD until regulation |
| 11 | Current limit | Rload=0.1 ohm (near short) | Iout clamped < 80 mA |
| 12 | UV threshold | Sweep PVDD externally (HiZ mode) | Trip at 4.3V +/-0.3V |
| 13 | OV threshold | Sweep PVDD externally (HiZ mode) | Trip at 5.5V +/-0.2V |
| 14 | Mode transitions | BVDD ramp through all thresholds | Clean transitions, no glitches |
| 15 | PVT corners | Tests 1-8 at SS/FF/SF/FS, -40/27/150C | All specs met |
| 16 | Quiescent current | BVDD=7V, no load | Iq < 300 uA |
| 17 | Retention mode | BVDD=3.5V, Iload=0.5mA | PVDD tracks BVDD (bypass) |
| 18 | Power consumption | All modes | Report total from BVDD |

---

## Design Flow

### Phase 1: Pass Device Characterization (Block 01)

Start here because everything depends on the pass device.

1. Instantiate `sky130_fd_pr__pfet_g5v0d10v5` with W=1mm, L=minimum (0.5um or process min for HV).
2. Sweep Vgs, measure Id at Vds=0.4V. Find the W needed for 50 mA.
3. If W is unreasonably large (>20mm), consider NMOS source-follower topology instead.
4. Measure Cgs vs Vgs at the operating point. This number drives everything downstream.
5. Document: W/L, Id(Vgs), gm, Cgs, Rds_on.

### Phase 2: Error Amplifier (Block 00)

Design the error amp knowing the pass device load (Cgs, gm_pass).

1. Choose topology (folded-cascode recommended).
2. Target UGB = gm_ea / (2*pi*Cgs_pass) — this should be in the 100kHz-1MHz range.
3. Size for gain > 60 dB, offset < 5 mV.
4. The error amp runs from PVDD (5V) using 1.8V devices. Use cascode stacking if needed to protect from PVDD overshoot during transients. OR use 5V thick-oxide devices (`sky130_fd_pr__nfet_05v0`) for the entire error amp.
5. Simulate open-loop gain/phase. Does NOT need to be stable alone — it will be stabilized by the LDO loop.

### Phase 3: Close the Loop (Blocks 02 + 03)

1. Connect: V_REF → Error Amp (+) → Pass Device gate → PVDD → Feedback divider → Error Amp (-)
2. Add 200 pF load cap.
3. Run loop stability analysis. It WILL be unstable initially.
4. Add compensation. Iterate until PM > 45 deg at all loads.
5. Run transient step response to confirm stability in time domain.

### Phase 4: Protection (Blocks 04, 05, 07)

Add current limiter, UV/OV comparators, and zener clamp. These should not affect the main regulation loop under normal conditions.

### Phase 5: Mode Control and Startup (Blocks 06, 08, 09)

Add level shifters, mode control logic, and startup circuit. Verify power-up from zero.

### Phase 6: Top Integration (Block 10)

Connect everything. Run the full 18-point verification plan. Iterate until all specs pass.

---

## File Naming Convention

Each block directory should contain:
- `design.cir` — Final SPICE subcircuit (the deliverable)
- `tb_*.spice` — Testbench files
- `README.md` — Block-level design report with results
- `specs.json` — Machine-readable spec file
- `*.png` — Simulation result plots

## What Success Looks Like

A complete `pvdd_regulator/10_top_integration/design.cir` that:
1. Contains ONLY Sky130 PDK device instantiations (no ideal/behavioral components)
2. Simulates in ngspice without errors
3. Passes all 18 verification tests across PVT corners
4. Has a documented design report with every number backed by a re-runnable testbench
5. Can be handed to a layout engineer for physical implementation in Sky130

---

*This program was created 2026-03-27. All specifications derived from TDK-Micronas HVCM PVDD regulator concept documentation, adapted for SkyWater SKY130A process.*
