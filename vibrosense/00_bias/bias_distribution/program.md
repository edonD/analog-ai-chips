# Block 00 Extension: Bias Distribution — Program

## 1. Mission

The existing `../design.cir` produces a single output: `iref_out`, a 507 nA current
source. Every downstream OTA in the VibroSense chip needs four specific bias voltages
to set its operating point. Currently those voltages are ideal voltage sources hardcoded
in every OTA testbench. That is a simulation shortcut, not a real design.

Your mission is to extend Block 00 so that it generates and distributes all four OTA
bias voltages from the same 500 nA reference current, with no external ideal sources
anywhere downstream. You will produce a new subcircuit `bias_generator_full` in a new
file `design_full.cir`. When you are done, every other block in the chip can be verified
using only real circuits.

The four voltages required:

| Signal | Value (TT, 27C) | Type | OTA device it biases |
|--------|----------------|------|----------------------|
| vbn    | 0.65 V         | Ground-referred | M11 tail, M9/M10 NMOS sources |
| vbcn   | 0.88 V         | Ground-referred | M7/M8 NMOS cascode gates |
| vbp    | VDD - 0.73 V = 1.07 V | VDD-tracking | M3/M4/M12/M13 PMOS mirrors |
| vbcp   | VDD - 1.325 V = 0.475 V | VDD-tracking | M5/M6 PMOS cascode gates |

VDD-tracking means the voltage moves with VDD rail by rail. This is critical: if vbp
and vbcp are generated as fixed ground-referenced voltages instead of VDD-tracking,
the OTA PSRR degrades from 70 dB to approximately 30-40 dB.

### What "done" means

1. `design_full.cir` exists containing subcircuit `bias_generator_full` with 7 pins:
   `vdd gnd iref_out vbn vbcn vbp vbcp`
2. A regression testbench proves `iref_out` from `bias_generator_full` matches
   `bias_generator` to within 2% at TT 27C — the new devices must not disturb
   the core beta-multiplier operating point.
3. All four bias voltages hit their targets across 5 corners and 3 temperatures.
4. vbp and vbcp are confirmed VDD-tracking: when VDD moves from 1.6 V to 2.0 V,
   vbp moves by the same amount (delta_vbp / delta_VDD > 0.9 V/V).
5. `design.cir` has not been modified in any way.

---

## 2. What Exists — Read Before Writing Anything

Before creating any file, read the following. Do not skip this.

### 2.1 `../design.cir` — FROZEN

This file contains `.subckt bias_generator vdd gnd iref_out`. It is finished,
verified, and used by 53 existing testbenches. You must not modify it in any way.
Not a single character. Add this comment to the top if it is not already there:

    ** FROZEN v1 — do not modify. Extended version in bias_distribution/design_full.cir

### 2.2 The existing operating point (from ../README.md)

At TT 27C 1.8V:
- Iref = 507 nA
- vbias (internal node) = VDD - 0.73 V = 1.07 V  ← this is vbp
- nbias (internal node) = 0.65 V                  ← this is vbn
- OTA tail (otail) = ~0.15 V
- Quiescent power = 0.97 uW

The internal node `vbias` is the PMOS mirror gate, set by the OTA feedback loop.
Because M3/M4 are PMOS with source at VDD, `vbias` tracks VDD by construction —
it is always approximately VDD - |Vgs_pmos|, regardless of absolute VDD. This
is why vbp has good PSRR. Your job is to expose this node and derive vbcp from it.

The internal node `nbias` is the NMOS mirror gate, set by M1's diode connection.
It is ground-referred. vbcn must be derived by stacking one more Vgs above it.

### 2.3 The OTA sizing context (from ../ota_foldcasc.spice)

The OTA was designed around these bias voltages:
- vbn = 0.65 V  → sets Vgs of M11 (W=3.8u L=14u) to carry 501 nA
- vbcn = 0.88 V → sets M7/M8 NMOS cascode (W=2u L=14u) gate
- vbp = 1.07 V  → sets M3a-M3t PMOS fold (W=0.42u L=20u, 20 parallel)
- vbcp = 0.475V → sets M5/M6 PMOS cascode (W=0.42u L=2u) gate

Your bias generation circuit must reproduce these values. If you miss by more than
±50 mV on any voltage, the OTA will have transistors leaving saturation.

---

## 3. Circuit Approach

### 3.1 Expose vbn and vbp (zero new devices needed)

In `design_full.cir`, copy the entire contents of `design.cir` and rename the
subcircuit to `bias_generator_full` with the extended port list. Then rename every
occurrence of the internal node `nbias` to `vbn` and every occurrence of `vbias`
to `vbp`. The nodes now have the same names as the output pins, so they connect
automatically. No new wires, no new devices, no change to any values.

After this rename the circuit is electrically identical to `bias_generator`. Verify
this by running the regression testbench (Section 6.1) before proceeding further.

### 3.2 Generate vbcn (one new device)

vbcn must be approximately vbn + Vgs_nmos at 500 nA. With the same device sizing
as M1 (W=2u L=4u), Vgs at 500 nA is approximately 0.23 V, giving vbcn ≈ 0.88 V.

Circuit: add a diode-connected NMOS (Mbcn) with drain and gate tied together at
vbcn, source at vbn. Current must flow through Mbcn to set the voltage. Provide
this current by adding one additional PMOS output mirror leg (XM8, identical to
XM7: W=4u L=4u, gate=vbp, source=vdd) whose drain connects to vbcn.

    XM8    vbcn vbp vdd vdd  sky130_fd_pr__pfet_01v8  w=4 l=4
    XMbcn  vbcn vbcn vbn gnd sky130_fd_pr__nfet_01v8  w=2 l=4

Current path: VDD → XM8 (500 nA) → vbcn node → XMbcn (diode) → vbn → gnd.
XM8 mirrors the same current as XM7 (500 nA). XMbcn drops one Vgs ≈ 0.23 V.
Result: vbcn ≈ vbn + 0.23 V ≈ 0.88 V.

### 3.3 Generate vbcp (one new device)

vbcp must be approximately vbp - |Vgs_pmos| at 500 nA. With W=0.42u L=20u (same
as the OTA's PMOS fold devices), |Vgs| at 500 nA is approximately 0.595 V, giving
vbcp ≈ 1.07 - 0.595 = 0.475 V.

Because vbp is VDD-referred, vbcp will automatically be VDD-referred too — this
is the VDD-tracking property you need.

Circuit: add a diode-connected PMOS (Mbcp) with drain and gate tied at vbcp, source
at vbp. Add a matched NMOS (Mbcp_sink, same as M1: W=2u L=4u, gate=vbn) to sink
the current and set a stable operating point.

    XMbcp      vbcp vbcp vbp vdd  sky130_fd_pr__pfet_01v8  w=0.42 l=20
    XMbcp_sink vbcp vbn  gnd gnd  sky130_fd_pr__nfet_01v8  w=2    l=4

Current path: vbp → XMbcp (diode, ~500 nA) → vbcp → XMbcp_sink → gnd.
XMbcp_sink gate is at vbn = 0.65 V, same as M1 and M2. It carries ~500 nA.
XMbcp drops one |Vgs| ≈ 0.595 V below vbp.
Result: vbcp ≈ vbp - 0.595 ≈ 0.475 V. VDD-tracking because vbp is VDD-tracking.

### 3.4 Total power addition

Four new mirror legs (XM8 draws 500 nA, XMbcp_sink draws ~500 nA) add approximately
1.8 V × 1.0 uA = 1.8 uW to the existing 0.97 uW. Total ≈ 2.8 uW. Still well inside
the 15 uW system budget for this block.

---

## 4. Device Sizing Rationale

| Device | W (um) | L (um) | Why |
|--------|--------|--------|-----|
| XM8 (mirror leg) | 4 | 4 | Identical to XM7 — same Vgs, same current density, matched mirror |
| XMbcn | 2 | 4 | Same as M1 — produces same Vgs at same current, gives vbcn = vbn + Vgs_M1 |
| XMbcp | 0.42 | 20 | Identical to OTA PMOS fold devices — produces exactly the Vgs the OTA expects |
| XMbcp_sink | 2 | 4 | Same as M1/M2 — sinks ~500 nA at vbn gate bias without disturbing vbn |

Do not change these sizes. They are chosen to produce bias voltages that exactly match
what the OTA was designed for. If you resize them, the OTA operating point will shift.

---

## 5. File Organization Rules

### Files you will create (inside this folder: `00_bias/bias_distribution/`)

```
design_full.cir              ← new subckt bias_generator_full (7 pins)
specs_full.json              ← specs for the 4 bias voltages
tb_regression_iref.spice     ← proves iref unchanged vs design.cir
tb_biasdist_dc.spice         ← measures all 4 voltages at TT 27C
tb_biasdist_corners.spice    ← all 4 voltages at 5 corners × 3 temps
tb_biasdist_psrr.spice       ← VDD-tracking verification for vbp and vbcp
generate_plots.py            ← plots for all measurements
README.md                    ← design report (same structure as ../README.md)
```

### Files you will NOT touch under any circumstances

```
../design.cir                ← frozen
../specs.json                ← frozen
../requirements.md           ← frozen
../README.md                 ← frozen
../tb_*.spice (all 53)       ← frozen
```

All new work lives in `bias_distribution/`. The parent directory (`00_bias/`) is
read-only from this task's perspective.

---

## 6. Testbenches

### 6.1 `tb_regression_iref.spice` — must run first

Purpose: prove that `bias_generator_full` produces the same Iref as the frozen
`bias_generator`. If this fails, you introduced a bug in the node rename step.

```spice
** Regression: iref from both subcircuits must match within 2%
.include "../design.cir"
.include "design_full.cir"

Xold vdd gnd iref_old              bias_generator
Xnew vdd gnd iref_new vbn vbp vbcn vbcp  bias_generator_full

Vdd vdd gnd 1.8
Rold iref_old gnd 3560
Rnew iref_new gnd 3560

.op
.meas op iref_old_nA  find  i(Rold)*1e9
.meas op iref_new_nA  find  i(Rnew)*1e9
.meas op delta_pct    param 'abs(iref_old_nA - iref_new_nA) / iref_old_nA * 100'
** PASS: delta_pct < 2.0
** FAIL: delta_pct >= 2.0 → the node rename introduced a circuit change. Debug first.
```

Do not proceed to any other testbench until this passes.

### 6.2 `tb_biasdist_dc.spice` — TT 27C operating point

```spice
.include "design_full.cir"
.lib "PATH_TO_SKY130/sky130.lib.spice" tt

Xbias vdd gnd iref_out vbn vbp vbcn vbcp  bias_generator_full
Vdd vdd gnd 1.8
Riref iref_out gnd 3560

.op
.meas op m_iref_nA   find  i(Riref)*1e9
.meas op m_vbn       find  v(vbn)
.meas op m_vbcn      find  v(vbcn)
.meas op m_vbp       find  v(vbp)
.meas op m_vbcp      find  v(vbcp)
.meas op m_vbcn_diff param 'v(vbcn) - v(vbn)'
.meas op m_vbcp_diff param 'v(vbp)  - v(vbcp)'

** Expected results:
** m_iref_nA:   480 to 530 nA
** m_vbn:       0.60 to 0.70 V
** m_vbcn:      0.82 to 0.95 V
** m_vbp:       1.00 to 1.15 V
** m_vbcp:      0.42 to 0.53 V
** m_vbcn_diff: 0.18 to 0.28 V  (one Vgs drop)
** m_vbcp_diff: 0.52 to 0.65 V  (one |Vgs| drop)
```

### 6.3 `tb_biasdist_corners.spice` — 5 corners × 3 temperatures

Run the same .op measurements as 6.2 with .lib corner substitution and .temp statements.
Corners: tt, ss, ff, sf, fs. Temperatures: -40, 27, 85.
Total: 15 simulation conditions.

For each condition record all four voltage values. The pass criterion is that no
voltage deviates by more than ±100 mV from its TT 27C value. Pay special attention
to vbcn at the ss corner (Vgs increases, vbcn could rise above 0.95 V) and vbcp
at ff corner (|Vgs| decreases, vbcp could rise above 0.53 V).

### 6.4 `tb_biasdist_psrr.spice` — VDD-tracking verification

This testbench sweeps VDD from 1.6 V to 2.0 V in DC and measures how vbp and vbcp
track it.

```spice
.include "design_full.cir"
.lib "PATH_TO_SKY130/sky130.lib.spice" tt

Xbias vdd gnd iref_out vbn vbp vbcn vbcp  bias_generator_full
Vdd vdd gnd 1.8
Riref iref_out gnd 3560

.dc Vdd 1.6 2.0 0.01

.meas dc track_vbp  find  deriv(v(vbp))  at=1.8
.meas dc track_vbcp find  deriv(v(vbcp)) at=1.8

** PASS: track_vbp  > 0.85 V/V  (vbp moves with VDD)
** PASS: track_vbcp > 0.85 V/V  (vbcp moves with VDD)
** FAIL: track < 0.5 → voltage is ground-referenced, not VDD-tracking → OTA PSRR destroyed

** Also verify: track_vbn  < 0.15 V/V  (vbn should NOT track VDD — it is ground-referred)
** Also verify: track_vbcn < 0.15 V/V  (vbcn should NOT track VDD)
```

---

## 7. PASS / FAIL Criteria

All of the following must be true before declaring this task complete.

### 7.1 Regression (non-negotiable first gate)
- [ ] `tb_regression_iref`: iref_old vs iref_new within 2% at TT 27C 1.8V

### 7.2 Bias voltages at TT 27C 1.8V
- [ ] vbn:  0.60 V to 0.70 V
- [ ] vbcn: 0.82 V to 0.95 V
- [ ] vbp:  1.00 V to 1.15 V
- [ ] vbcp: 0.42 V to 0.53 V
- [ ] Iref: 480 nA to 530 nA (unchanged from frozen design)

### 7.3 Bias voltages across 5 corners × 3 temperatures
- [ ] All four voltages within ±100 mV of TT 27C values at every condition
- [ ] vbp and vbcp remain VDD-tracking at all corners (confirmed by operating point analysis)

### 7.4 VDD-tracking
- [ ] dvbp/dVDD > 0.85 V/V at TT 27C
- [ ] dvbcp/dVDD > 0.85 V/V at TT 27C
- [ ] dvbn/dVDD < 0.15 V/V  (must NOT track — ground-referred)
- [ ] dvbcn/dVDD < 0.15 V/V (must NOT track — ground-referred)

### 7.5 File integrity
- [ ] `../design.cir` is byte-for-byte identical to what it was before this task started
- [ ] All 53 existing `../tb_*.spice` files are untouched
- [ ] New subcircuit is named `bias_generator_full` (not `bias_generator`) in all files

---

## 8. Deliverables

When this task is complete the following files must exist in `bias_distribution/`:

```
design_full.cir          ← subckt bias_generator_full, 7 pins, verified
specs_full.json          ← formal spec record with measured values filled in
tb_regression_iref.spice ← green
tb_biasdist_dc.spice     ← green
tb_biasdist_corners.spice← green, all 15 conditions
tb_biasdist_psrr.spice   ← green
generate_plots.py        ← produces corner summary and VDD-tracking plots
README.md                ← documents what was built, measured values, known margins
```

The README.md must include a filled-in version of this table at the top:

| Signal | Target      | Measured (TT) | Worst corner | VDD-tracking |
|--------|-------------|---------------|--------------|--------------|
| vbn    | 0.60-0.70 V | ...           | ...          | No (correct) |
| vbcn   | 0.82-0.95 V | ...           | ...          | No (correct) |
| vbp    | 1.00-1.15 V | ...           | ...          | Yes (>0.85)  |
| vbcp   | 0.42-0.53 V | ...           | ...          | Yes (>0.85)  |

---

## 9. Interface Contract (for downstream blocks)

When this block is complete, every downstream block (02 through 06) must use
`bias_generator_full` from this file. They must not use `bias_generator` and
must not use any ideal voltage sources for OTA biasing. The include path is:

    .include "../../00_bias/bias_distribution/design_full.cir"

Instantiation:

    Xbias vdd gnd iref_out vbn vbp vbcn vbcp  bias_generator_full

The four bias voltage nodes (vbn, vbp, vbcn, vbcp) are then available as net
names in the top-level testbench and are passed directly to OTA subcircuit pins.
