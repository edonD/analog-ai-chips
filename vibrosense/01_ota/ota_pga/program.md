# Block 01 Extension: PGA OTA Variant — Program

## 1. Mission

The existing `../ota_foldcasc.spice` was designed for the Gm-C filter blocks. It
runs at 500 nA tail current and achieves 33.7 kHz unity-gain bandwidth at 10 pF.
That is correct and sufficient for Gm-C integrators, where bandwidth is set by Gm/C,
not by closed-loop gain.

The PGA (Block 02) is different. It uses the OTA in closed-loop feedback with
resistive or switched-capacitor gain networks. The closed-loop bandwidth of a
feedback amplifier is approximately UGB / closed-loop-gain. At 33.7 kHz UGB and
64x closed-loop gain, the PGA bandwidth would be only ~530 Hz. That is usable only
for the lowest vibration band (100-500 Hz). At 16x gain it would be ~2.1 kHz. The
PGA needs to cover vibration bands up to 10 kHz at its intermediate gain settings.

Your mission is to design `ota_pga.spice`, a higher-current variant of the
folded-cascode OTA, targeting 50 kHz UGB at 10 pF load. The topology is identical
to `ota_foldcasc`. Only the bias point changes. The subcircuit pin interface is
identical to `ota_foldcasc` — nine pins in the same order — so Block 02 can
instantiate either OTA by changing only the subcircuit name.

### The bandwidth requirement per gain setting

With 50 kHz UGB the PGA closed-loop bandwidths become:

| PGA gain | Closed-loop BW | Vibration bands covered |
|----------|---------------|------------------------|
| 1x       | ~50 kHz       | All bands (full signal) |
| 4x       | ~12.5 kHz     | Bands 1-4 (100 Hz-10 kHz) |
| 16x      | ~3.1 kHz      | Bands 1-3 (100 Hz-2 kHz) |
| 64x      | ~780 Hz        | Band 1 only (100-500 Hz) |

This is acceptable: high gain is only needed for small signals in the low-frequency
bands where bearing fault fundamentals dominate. At 5-20 kHz the signal is large
enough that 1x or 4x gain is sufficient.

### What "done" means

1. `ota_pga.spice` exists containing subcircuit `ota_pga` with the same 9-pin
   interface as `ota_foldcasc`: `vdd gnd inp inn out vbn vbcn vbp vbcp`
2. All 5 gates of `verify_pga.py` pass at TT 27C.
3. UGB > 45 kHz at 10 pF across all 5 corners and 3 temperatures.
4. Phase margin > 60 degrees from 2 pF to 50 pF load (unconditional stability).
5. All transistors in saturation with Vov > 100 mV at TT 27C.
6. `ota_foldcasc.spice` has not been modified in any way.

---

## 2. What Exists — Read Before Writing Anything

### 2.1 `../ota_foldcasc.spice` — FROZEN

This is the filter OTA. It is finished, verified through 16 iterations, and will
be used by Blocks 03, 04, and 05. Do not touch it. Add this line to the top if not
already present:

    ** FROZEN v11 — filter OTA. PGA variant in ota_pga/ota_pga.spice

### 2.2 The filter OTA operating point (from ../README.md and ../verification_report_v2.txt)

At TT 27C 1.8V with 10 pF load:
- Tail current (M11): 501 nA, W=3.8u L=14u
- PMOS fold current per branch (M3/M4): ~250 nA, 20 parallel instances W=0.42u L=20u
- Input pair (M1/M2): W=5u L=14u, Vov > 50 mV
- NMOS cascode (M7/M8): W=2u L=14u
- NMOS current sources (M9/M10): W=2.15u L=14u
- DC gain: 65.4 dB
- UGB: 33.7 kHz
- Phase margin: 89.2 degrees
- Supply current: 1.02 uA total
- Noise: 287 nV/sqrt(Hz) at 10 kHz, 1/f corner at ~417 Hz

### 2.3 Why the filter OTA cannot simply be re-biased

The filter OTA was pushed to its limits at 500 nA. When tail current (Vbn) was
increased during verification, the PMOS fold current did not scale because Vbp
is set independently. The excess tail current had nowhere to go and drove the
output into the rail. This was documented in the verification report (Runs #1-6).

The fix: both the tail current and the PMOS fold current must scale together.
This requires sizing three things simultaneously:
1. The tail (M11) to carry 1.5 uA
2. The PMOS fold (M3/M4) to carry 750 nA per branch (half of 1.5 uA)
3. The PMOS bias mirrors (M12/M13) to set the correct Vbp for 750 nA per fold device

Everything else (cascode devices, input pair) can stay the same or be scaled
conservatively.

### 2.4 The bias voltages

The four bias voltages come from `../../00_bias/bias_distribution/design_full.cir`
(subcircuit `bias_generator_full`). In testbenches for this block you must use
the real bias generator, not ideal voltage sources.

At TT 27C: vbn=0.65V, vbcn=0.88V, vbp=1.07V, vbcp=0.475V.

Important: vbn is fixed by the bias generator (0.65V). You cannot change vbn to
get more tail current — the bias generator produces a fixed voltage that was
set to give 500 nA through a W=3.8u L=14u device. To get 1.5 uA at the same
vbn, you must scale M11's width to 3x: W = 11.4u L = 14u.

Similarly, vbp is fixed. To get 750 nA per fold branch at the same vbp, you must
increase the number of parallel PMOS instances from 20 to 30.

---

## 3. Circuit Approach

### 3.1 Start from a copy of `../ota_foldcasc.spice`

Copy the entire file into `ota_pga/ota_pga.spice`. Change only the subcircuit name
on the first line:

    ** OLD: .subckt ota_foldcasc vdd gnd inp inn out vbn vbcn vbp vbcp
    ** NEW: .subckt ota_pga      vdd gnd inp inn out vbn vbcn vbp vbcp

Pin order is identical. This is the only acceptable starting point — do not write
a new netlist from scratch.

### 3.2 Scale M11 tail current source (3x width)

The tail current source M11 carries half the total supply current. At vbn = 0.65V,
drain current scales with W/L for a given Vgs. To triple the current:

    ** OLD: XM11 otail vbn gnd gnd sky130_fd_pr__nfet_01v8 w=3.8 l=14
    ** NEW: XM11 otail vbn gnd gnd sky130_fd_pr__nfet_01v8 w=11.4 l=14

Keep L=14u. Long channel is required for high output impedance and low noise.
The new tail current will be approximately 501 nA × (11.4/3.8) = 1.503 uA.

Verify in simulation: measure I(XM11) in the .op output. Must be 1.4 uA to 1.6 uA.

### 3.3 Scale PMOS fold current (20 → 30 parallel instances)

Each of the 20 existing parallel PMOS instances (M3a through M3t, and M4a through
M4t) carries approximately 12.5 nA. Together they conduct 250 nA per fold branch.
To match the new 750 nA per branch you need 30 parallel instances (30 × 25 nA).

In the netlist, add 10 more instances to each set. Name them M3u through M3ad and
M4u through M4ad, following the same pattern:

    XM3u  fold_p inp   vdd  vdd  sky130_fd_pr__pfet_01v8 w=0.42 l=20
    XM3v  fold_p inp   vdd  vdd  sky130_fd_pr__pfet_01v8 w=0.42 l=20
    ... (continue through XM3ad, 10 new instances)
    XM4u  out    inn   vdd  vdd  sky130_fd_pr__pfet_01v8 w=0.42 l=20
    ... (continue through XM4ad, 10 new instances)

Keep W=0.42u L=20u. Do not change these dimensions. The minimum width is critical
for SKY130's high PMOS Vth (~1.0V) — it produces the narrow-channel Vth reduction
that keeps Vov above 150 mV at the bias point. If you widen the device, Vth drops
and the device enters triode.

Effective total width per branch: 30 × 0.42u = 12.6u (was 20 × 0.42u = 8.4u).
Current per instance at the new operating point: ~25 nA per device at vbp = 1.07V.

### 3.4 Scale PMOS bias mirrors M12 and M13

M12 and M13 set the Vbp that drives the fold devices. At the new operating point,
each must carry enough current to properly mirror to the 30-instance fold. With
vbp coming from the bias generator (fixed at 1.07V), the mirror devices themselves
need to carry proportionally more current to maintain the correct operating point.

    ** OLD: XM12 vbp vbp vdd vdd sky130_fd_pr__pfet_01v8 w=0.42 l=20
    ** NEW: XM12 vbp vbp vdd vdd sky130_fd_pr__pfet_01v8 w=1.26 l=20   (3x width)
    ** OLD: XM13 fold_ctrl vbp vdd vdd sky130_fd_pr__pfet_01v8 w=0.42 l=20
    ** NEW: XM13 fold_ctrl vbp vdd vdd sky130_fd_pr__pfet_01v8 w=1.26 l=20

Check this in operating point simulation: the Vov of M12/M13 must match M3a/M3t
within 20 mV, confirming the mirror is accurate.

### 3.5 Input pair, cascode devices, NMOS current sources — unchanged

Leave M1/M2 (W=5u L=14u), M7/M8 (W=2u L=14u), M9/M10 (W=2.15u L=14u) at their
existing sizes. The input pair gm scales with sqrt(Id) — at 1.5 uA tail, each
input device carries 750 nA instead of 250 nA, increasing gm by sqrt(3) ≈ 1.73x.
This directly increases UGB by the same factor: 33.7 × 1.73 ≈ 58 kHz. Target met.

The cascode devices (M5/M6, M7/M8) operate at the same current density as before
since their current scales with the fold — they do not need resizing. Verify their
Vov stays > 100 mV after the current increase.

---

## 4. Expected Operating Point After Changes

Based on scaling analysis (verify all values in simulation):

| Device/Parameter | Filter OTA | PGA OTA | Change |
|-----------------|-----------|---------|--------|
| M11 tail | 501 nA | ~1.5 uA | 3x width |
| M3/M4 per branch | 250 nA | 750 nA | 20→30 instances |
| Input pair Id | 250 nA | 750 nA | unchanged device |
| gm1 (input pair) | ~5 uS | ~8.7 uS | scales as sqrt(3x Id) |
| UGB | 33.7 kHz | ~50 kHz | gm1 / (2pi × 10pF) |
| Phase margin | 89.2 deg | >70 deg | should stay high |
| Supply current | 1.02 uA | ~3.0 uA | 3x |
| Power | 0.97 uW | ~5.4 uW | acceptable (budget: 20 uW for PGA) |
| Noise @ 10kHz | 287 nV/√Hz | ~190 nV/√Hz | improves as 1/sqrt(3x Id) |

Noise improvement note: thermal noise decreases as gm increases. At 3x current,
gm increases by sqrt(3), so input-referred noise decreases by 1/sqrt(sqrt(3)) ≈
0.76x. Expected noise: 287 × 0.76 ≈ 218 nV/√Hz. This is close to the 200 nV/√Hz
original spec. The PGA OTA may actually meet the noise spec that the filter OTA missed.

---

## 5. File Organization Rules

### Files you will create (inside this folder: `01_ota/ota_pga/`)

```
ota_pga.spice                ← subckt ota_pga, same 9-pin interface
specs_pga.json               ← PGA OTA specs with measured values
verify_pga.py                ← 5-gate verification (copy of verify_design.py, updated thresholds)
tb_pga_ac.spice              ← AC open-loop: gain, UGB, phase margin
tb_pga_dc.spice              ← DC sweep: output swing
tb_pga_tran.spice            ← transient step: slew rate
tb_pga_psrr.spice            ← power supply rejection
tb_pga_cmrr.spice            ← common-mode rejection
tb_pga_corner_tt.spice       ← TT corner
tb_pga_corner_ss.spice       ← SS corner
tb_pga_corner_ff.spice       ← FF corner
tb_pga_corner_sf.spice       ← SF corner
tb_pga_corner_fs.spice       ← FS corner
tb_pga_temp_m40.spice        ← -40C
tb_pga_temp_27.spice         ← 27C
tb_pga_temp_85.spice         ← 85C
generate_plots.py            ← Bode, corner summary, dashboard
README.md                    ← design report
```

### Files you will NOT touch under any circumstances

```
../ota_foldcasc.spice        ← frozen v11
../verify_design.py          ← frozen
../specs.json                ← frozen
../README.md                 ← frozen
../tb_*.spice (all 15)       ← frozen
../report_*.png (all 9)      ← frozen
```

### Testbench naming convention

Every new testbench has `_pga_` in its name. If you create a file named `tb_ac.spice`
without the `_pga_` infix you may accidentally overwrite or confuse a filter OTA testbench.
The naming convention is not optional.

---

## 6. Testbenches

Each testbench is a direct copy of the corresponding filter OTA testbench with two
substitutions:
1. `ota_foldcasc` → `ota_pga` (subcircuit name)
2. Ideal voltage sources for bias → instantiation of `bias_generator_full` from
   `../../00_bias/bias_distribution/design_full.cir`

The bias instantiation block to use in every testbench:

```spice
.include "../../00_bias/bias_distribution/design_full.cir"
Xbias vdd gnd iref_out vbn vbp vbcn vbcp  bias_generator_full
Riref iref_out gnd 3560
** vbn, vbp, vbcn, vbcp are now available as net names
** Pass them directly to ota_pga pins
```

### 6.1 `tb_pga_ac.spice` — AC performance (run second, after .op)

Use a loop-breaking inductor (L=1H) to open the feedback loop for AC measurement.
Sweep: .ac dec 100 0.1 10G
Measure: DC gain (from v(out) at 0.1 Hz), UGB (where |A| crosses 0 dB),
phase at UGB (phase margin = 180 + phase(A) at UGB).

PASS thresholds:
- DC gain > 65 dB
- UGB: 45 kHz to 300 kHz
- Phase margin > 60 degrees

### 6.2 `tb_pga_dc.spice` — output swing

Sweep Vinp from 0.1V to 1.7V in unity-gain configuration (out connected to inn).
Measure output swing: the voltage range over which gain > 0.9 V/V.
PASS: swing > 1.0 Vpp

### 6.3 `tb_pga_tran.spice` — slew rate

100 mV step at 10 us, 10 pF load, unity-gain configuration.
Measure: slew rate on rising and falling edges.
PASS: slew rate > 30 mV/us (scales with current vs filter OTA's 20.5 mV/us)

### 6.4 `tb_pga_psrr.spice` and `tb_pga_cmrr.spice`

Identical structure to filter OTA testbenches. AC sweep of supply rejection and
common-mode rejection.
PASS: PSRR > 60 dB at 1 kHz, CMRR > 70 dB at DC

### 6.5 Corner testbenches (5 files)

Each corner testbench runs the AC sweep at the given process corner.
All corners must achieve UGB > 30 kHz (relaxed from 45 kHz — worst corner allowed
to be slower) and phase margin > 55 degrees.

### 6.6 Temperature testbenches (3 files)

AC sweep at -40C, 27C, 85C with TT corner models.
All temperatures must achieve UGB > 30 kHz and phase margin > 55 degrees.

---

## 7. `verify_pga.py` — 5-Gate Verification Script

Copy `../verify_design.py` to `verify_pga.py`. Update the following constants only.
Do not change the gate structure, the measurement extraction logic, or the reporting format.

```python
# ── Identity ──────────────────────────────────────────────
NETLIST   = "ota_pga.spice"
SUBCKT    = "ota_pga"
LOGFILE   = "verification_report_pga.txt"

# ── Gate 1: Operating Point ───────────────────────────────
ITAIL_TARGET_NA  = 1500      # was 500
ITAIL_TOL_PCT    = 10        # ±10%
VOV_MIN_MV       = 100       # was 150 — relaxed, higher current gives more headroom

# ── Gate 2: AC Performance ────────────────────────────────
GAIN_MIN_DB      = 65        # unchanged
UGB_MIN_HZ       = 45_000    # was 30_000
UGB_MAX_HZ       = 300_000   # was 150_000 — raised for higher-current design
PM_MIN_DEG       = 60        # unchanged

# ── Gate 3: Transient ─────────────────────────────────────
SLEW_MIN_MV_US   = 30        # was 10 — scales with current
SWING_MIN_VPP    = 1.0       # unchanged

# ── Gate 4: Rejection ─────────────────────────────────────
PSRR_MIN_DB      = 60        # was 50 — raised expectation
CMRR_MIN_DB      = 70        # was 60 — raised expectation

# ── Gate 5: Corners + Temperature ────────────────────────
CORNER_UGB_MIN_HZ = 30_000   # was 20_000
CORNER_PM_MIN_DEG = 55       # unchanged
```

Gates remain sequential: Gate N does not run if Gate N-1 fails. Exit code indicates
which gate failed, same convention as `verify_design.py`.

---

## 8. `specs_pga.json`

```json
{
  "name": "VibroSense PGA OTA (high-current variant)",
  "description": "Folded-cascode OTA scaled for PGA closed-loop use. Same topology as ota_foldcasc, 3x tail current for 50 kHz UGB. Used exclusively by Block 02 PGA.",
  "supply_v": 1.8,
  "tail_current_ua": 1.5,
  "measurements": {
    "dc_gain_db":               {"target": ">65",            "weight": 20},
    "ugb_hz":                   {"target": "45000 to 300000","weight": 25},
    "phase_margin_deg":         {"target": ">60",            "weight": 20},
    "input_noise_nv_sqrthz_1k": {"target": "<300",           "weight": 10,
                                 "note": "Relaxed from 200. Thermal noise improves with gm at higher current."},
    "cmrr_db":                  {"target": ">70",            "weight": 10},
    "psrr_db":                  {"target": ">60",            "weight": 10},
    "power_uw":                 {"target": "<8",             "weight": 5,
                                 "note": "1.5uA x 1.8V = 2.7uW typ. Budget 8uW including mirrors."}
  }
}
```

---

## 9. PASS / FAIL Criteria

All of the following must be true before declaring this task complete.

### 9.1 Operating point gate (Gate 1)
- [ ] All transistors in saturation (Vds > Vgs - Vth for NMOS, Vsd > Vsg - |Vtp| for PMOS)
- [ ] All Vov > 100 mV (critical: M5/M6 PMOS cascode and M7/M8 NMOS cascode)
- [ ] Tail current 1.35 uA to 1.65 uA (1.5 uA ± 10%)
- [ ] Current balance: I(fold_p_branch) ≈ I(fold_n_branch) within 5%
- [ ] Output quiescent voltage: 0.8V to 1.0V (near VDD/2)

### 9.2 AC performance gate (Gate 2)
- [ ] DC gain > 65 dB
- [ ] UGB: 45 kHz to 300 kHz at 10 pF load
- [ ] Phase margin > 60 degrees

### 9.3 Transient gate (Gate 3)
- [ ] Output swing > 1.0 Vpp
- [ ] Slew rate > 30 mV/us (rising and falling)

### 9.4 Rejection gate (Gate 4)
- [ ] PSRR > 60 dB at 1 kHz
- [ ] CMRR > 70 dB at DC

### 9.5 Corners and temperature gate (Gate 5)
- [ ] UGB > 30 kHz at all 5 corners × 3 temperatures (15 conditions)
- [ ] Phase margin > 55 degrees at all 15 conditions
- [ ] All transistors remain in saturation at all 15 conditions

### 9.6 Stability across load capacitance
- [ ] Phase margin > 60 degrees at CL = 2 pF
- [ ] Phase margin > 60 degrees at CL = 50 pF
- [ ] No gain peaking (AC magnitude monotonically decreasing above UGB)

### 9.7 File integrity
- [ ] `../ota_foldcasc.spice` is byte-for-byte identical to what it was before this task
- [ ] All 15 existing `../tb_*.spice` files are untouched
- [ ] All 9 existing `../report_*.png` files are untouched
- [ ] New subcircuit is named `ota_pga` in all files (never `ota_foldcasc`)

---

## 10. Deliverables

When this task is complete the following files must exist in `ota_pga/`:

```
ota_pga.spice                 ← verified subcircuit, 9-pin interface
specs_pga.json                ← with measured values filled in
verify_pga.py                 ← all 5 gates green
tb_pga_ac.spice               ← green
tb_pga_dc.spice               ← green
tb_pga_tran.spice             ← green
tb_pga_psrr.spice             ← green
tb_pga_cmrr.spice             ← green
tb_pga_corner_[tt,ss,ff,sf,fs].spice  ← all green
tb_pga_temp_[m40,27,85].spice ← all green
generate_plots.py             ← produces Bode, corner, dashboard plots
README.md                     ← design report with filled spec table
verification_report_pga.txt   ← gate-by-gate pass record
```

The README.md must include at the top:

| Spec             | Target          | Measured (TT 27C) | Worst corner |
|------------------|-----------------|--------------------|--------------|
| DC Gain          | >65 dB          | ...                | ...          |
| UGB              | 45-300 kHz      | ...                | ...          |
| Phase Margin     | >60 deg         | ...                | ...          |
| Noise @ 1 kHz    | <300 nV/√Hz     | ...                | —            |
| PSRR @ 1 kHz     | >60 dB          | ...                | ...          |
| CMRR @ DC        | >70 dB          | ...                | ...          |
| Supply current   | <4.5 uA         | ...                | ...          |
| Power            | <8 uW           | ...                | ...          |

---

## 11. Interface Contract (for Block 02)

When this task is complete, Block 02 (PGA) receives:

    File:    01_ota/ota_pga/ota_pga.spice
    Subckt:  ota_pga vdd gnd inp inn out vbn vbcn vbp vbcp
    UGB:     ~50 kHz at 10 pF (measured value in README.md)
    PM:      >60 deg, unconditionally stable 2 pF to 50 pF

    Companion filter OTA (for reference, not for PGA use):
    File:    01_ota/ota_foldcasc.spice
    Subckt:  ota_foldcasc vdd gnd inp inn out vbn vbcn vbp vbcp
    UGB:     33.7 kHz at 10 pF

    Both OTAs are biased by:
    File:    00_bias/bias_distribution/design_full.cir
    Subckt:  bias_generator_full vdd gnd iref_out vbn vbp vbcn vbcp

Block 02 must use ota_pga (not ota_foldcasc) and must use bias_generator_full
(not ideal voltage sources). These are the only acceptable instantiations.
