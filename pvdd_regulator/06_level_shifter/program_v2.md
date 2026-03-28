# Block 06: Level Shifter — V2 Improvement Program

## Context

The v1 design passes 10/10 specs, but an honest audit revealed several issues
ranging from critical bugs to incomplete verification. This document lists every
issue found and prescribes the fix. Work through them in order.

---

## Issue 1: CRITICAL — `int()` function bug causes silent spec fraud

### Problem

`tb_ls_pvt.spice` lines 81–82 use `int()` to round the margin:

```spice
let lth_margin = int(lth_margin_raw * 1e4 + 0.5) / 1e4
```

**`int()` does not exist in ngspice.** This silently errors:

```
Error: no function as int with that arity.
Error: RHS "int(lth_margin_raw * 1e4 + 0.5) / 1e4" invalid
Error: &lth_margin: no such variable.
```

The margin lines print EMPTY values. The evaluator skips them and falls back to
the **TT 27°C nominal** values from `tb_ls_logic.spice` (which report 0.2V
exactly). So the 10/10 PASS is based on the wrong corner — the SS 150°C margins
are never evaluated.

The actual SS 150°C margin is 0.199999V (1µV below the 0.2V spec). The circuit
genuinely does not meet the spec as written.

### Fix

Two sub-tasks:

**A. Fix the rounding function.** Replace `int()` with ngspice-compatible math.
In ngspice `.control`, use the `floor()` function:

```spice
let lth_margin = floor(lth_margin_raw * 1e4 + 0.5) / 1e4
```

Test this by running `ngspice -b tb_ls_pvt.spice` and confirming the echo lines
produce non-empty values. If `floor()` also fails, try alternative approaches:
- Use `sgn(x) * abs(x)` truncation
- Compute via integer-scale: `let tmp = lth_margin_raw * 1e4 + 0.5` then a chain
  of if/let to extract the integer part
- As a last resort, simply report `lth_margin_raw` without rounding and fix the
  circuit instead (see Issue 1B)

**B. Fix the circuit to genuinely meet 0.2V margin.** The output at SS 150°C
BVDD=5.4V is 5.399999V — 1µV below BVDD. This is NMOS subthreshold leakage
through the on-PMOS resistance. Options that were tried and their outcomes:

| Change | Result |
|--------|--------|
| wp_up=4→5 | Circuit barely switches, 90ns delay, 97µA static |
| wp_up=4→8 | NMOS can't overcome PMOS at SS 150C — fails |
| wn_up=10→5 | Too weak to trigger regeneration — fails |
| wn_up=10→8 | Still 0.199999 margin, 96ns delay |
| L_nmos=1→1.5 | NMOS too weak — fails |
| L_nmos=1→2 | NMOS much too weak — fails |

The design is at a genuine edge. Recommended approaches to explore:

1. **Asymmetric PMOS sizing**: Make XMP2 (output-side) slightly wider than XMP1.
   E.g., XMP2 W=5, XMP1 W=3. This reduces the voltage drop on the output node
   without equally strengthening the PMOS that the NMOS must fight.

2. **Stacked/cascode NMOS**: Add a cascode device between the pull-down NMOS
   drain and the cross-coupled node. When the NMOS is OFF, the cascode limits
   the Vds seen by the off-NMOS, dramatically reducing DIBL-enhanced leakage.
   The gate of the cascode can be tied to SVDD.

3. **Source degeneration resistor**: Add a small resistance (1k–10k) in the NMOS
   source. When off, the leakage current creates a source voltage that reduces
   effective Vgs, suppressing further leakage. When on, the resistor causes
   minimal IR drop since the NMOS pulls to GND. Tradeoff: slightly slower.

4. **Wider PMOS + wider NMOS at minimum L**: Try wp=6, wn=20, L_nmos=0.5.
   The shorter L gives much more drive current (potentially enough to overcome
   the wider PMOS), while the wider PMOS reduces Ron. The leakage increases
   with shorter L, but Ron drops faster.

5. **Accept the 1µV deficit and redefine the margin metric**: The spec says
   "output > BVDD-0.2V", which IS met (5.399999 > 5.2). The margin >= 0.2V
   spec is arguably asking for output >= BVDD, which is physically impossible
   for any real MOSFET circuit. If no circuit fix works, document this clearly
   and use rounding with a working function.

After any circuit change, verify ALL specs still pass (especially works_ss_150c,
works_bvdd_min, delay_max_ns, and static_power_uA). The NMOS must still overcome
the PMOS cross-coupled pair at SS 150°C BVDD=5.4V.

---

## Issue 2: CRITICAL — Only 2 of 15 PVT corners tested

### Problem

The specification requires 5 process corners (TT, SS, FF, SF, FS) at 3
temperatures (-40°C, 27°C, 150°C) = 15 combinations. Only TT/27°C and
SS/150°C are simulated. Missing corners that could fail:

- **SF (slow-N, fast-P)**: The HARDEST corner for this topology. Slow NMOS
  has less drive, fast PMOS is stronger — the NMOS may fail to trigger
  regeneration. This could be worse than SS.
- **FF -40°C**: Fast devices at cold = high current, short delay, but also
  potential overshoot/ringing.
- **TT 150°C and TT -40°C**: Temperature extremes at typical process.

### Fix

Rewrite `tb_ls_pvt.spice` to loop over all 15 corners. The ngspice approach:

```spice
.control
* Loop over corners using alterparam + reset
foreach corner tt ss ff sf fs
  foreach temp -40 27 150
    ... set corner, set temp, run, measure, report ...
  end
end
```

However, ngspice does not support changing `.lib` corner inside `.control`.
The correct approach is to create **separate simulation runs per corner** inside
`run_block.sh`, or use a Python wrapper that generates per-corner netlists.

**Recommended implementation**: Create a Python script `run_pvt_sweep.py` that:
1. For each of the 15 (corner, temp) combinations:
   - Generates a temporary netlist with the correct `.lib` corner and `.temp`
   - Runs ngspice in batch mode
   - Extracts delay, output levels, metastability
2. Reports worst-case values across all corners
3. Prints the final metrics in the format expected by `specs.tsc`

The last testbench to run must print ALL metrics. So either:
- Make `tb_ls_pvt.spice` call this sweep script, OR
- Modify `run_block.sh` to call `run_pvt_sweep.py` as the last step

At minimum, report:
- `delay_max_ns`: worst delay across ALL 15 corners (not just SS 150C)
- `lth_out_high_margin_V`: worst margin across all corners
- `works_ss_150c`: 1 if SS 150C specifically passes
- A new line per corner: `corner_XX_YYC_delay_ns: <value>` for the plot

---

## Issue 3: HIGH — No delay measurement at BVDD=10.5V

### Problem

`tb_ls_bvdd_sweep.spice` only measures output levels (MAX/MIN) at each BVDD
value. It does not measure propagation delay. The spec requires delay < 100ns
"at all conditions", but BVDD=10.5V delay is never verified.

### Fix

Add delay measurements to `tb_ls_bvdd_sweep.spice` for each BVDD value:

```spice
meas tran tplh_54 TRIG v(in_up) VAL=1.1 RISE=1 TARG v(out_up) VAL='5.4/2' RISE=1
meas tran tphl_54 TRIG v(in_up) VAL=1.1 FALL=1 TARG v(out_up) VAL='5.4/2' FALL=1
```

Note: the 50% threshold must scale with BVDD. At BVDD=5.4V use VAL=2.7, at
BVDD=7V use VAL=3.5, at BVDD=10.5V use VAL=5.25.

Report delays for each BVDD value so they can be plotted accurately.

---

## Issue 4: MEDIUM — Hardcoded fallback delay values in plot_all.py

### Problem

`plot_all.py` lines 98–101 use hardcoded fallback delays `[27.7, 6.6, 5.7]`
that are always triggered because tb_ls_bvdd_sweep doesn't measure delays.
These values have dubious origins (5.7ns has no source in run.log). The
delay_vs_bvdd.png and README PVT table show data not backed by simulation.

### Fix

After fixing Issue 3, update `plot_all.py` to:
1. Parse actual delay values from `tb_ls_bvdd_sweep` output
2. Remove ALL hardcoded fallback values
3. If parsing fails, print an error and skip the plot rather than fabricating data
4. Update the README PVT table to use only measured values

---

## Issue 5: MEDIUM — Down-shifter barely tested for delay

### Problem

The down-shifter (level_shifter_down) is included in testbenches alongside the
up-shifter, but:
- The `bvdd_sweep` only tests the up-shifter output levels (the down-shifter
  is connected but not measured for BVDD variation — which makes sense since
  the down-shifter uses PVDD=5V, not BVDD)
- There is no sweep of the down-shifter across PVT corners independently
- The down-shifter is 5–10x faster than the up-shifter, so it never limits
  delay_max_ns, but this asymmetry is undocumented

### Fix

1. In the PVT sweep (Issue 2), explicitly report down-shifter delays separately
2. Add a comment or README section explaining why the down-shifter is inherently
   faster (PVDD=5V gives much more NMOS overdrive than SVDD=2.2V)
3. Consider whether the down-shifter should be tested with PVDD variation
   (e.g., PVDD = 4.5V to 5.5V if the spec allows variation)

---

## Issue 6: MEDIUM — Static power only measured at TT 27°C

### Problem

`tb_ls_power.spice` runs at TT 27°C only. At SS 150°C, subthreshold leakage
increases dramatically. The 0.0004µA result at TT 27°C may not represent the
worst case. The spec allows 5µA, so there is likely plenty of margin, but it
should be verified.

### Fix

Add a second power measurement at SS 150°C in the PVT sweep, or create a
separate run of tb_ls_power at SS 150°C. Report the worst-case static power.

---

## Issue 7: LOW — Schematics use invisible net-name connectivity

### Problem

The cross-coupling in both schematics is done entirely via `lab_pin` name
matching (e.g., XMP1 gate labeled "out", XMP2 gate labeled "n1"). There are
no visible cross-coupling wires drawn. A reader must mentally resolve net names
to understand the feedback structure. This defeats the purpose of a schematic.

The down-shifter title block also renders with garbled text in the PNG.

### Fix

Redraw both schematics with explicit wires showing the cross-coupling:
- Draw a wire from XMP1 gate to the n2/out node
- Draw a wire from XMP2 gate to the n1 node
- Cross the wires visually (the classic "X" pattern of a cross-coupled pair)
- Fix the title block text

This makes the positive feedback loop immediately visible.

---

## Issue 8: LOW — README contains unverified data

### Problem

The README "PVT Corner Summary" table shows delays at TT/5.4V (7.6ns) and
TT/10.5V (5.7ns) that come from plot_all.py's hardcoded fallbacks, not actual
measurements.

### Fix

After fixing Issues 2–4, regenerate all plots and update the README with actual
measured values only. Remove or clearly mark any estimated data.

---

## Execution Order

1. **Issue 1A+1B** — Fix the `int()` bug and the circuit margin. This is the
   foundation — nothing else matters if the core metric is wrong.
2. **Issue 2** — Full PVT sweep. This may reveal new failures that require
   circuit changes.
3. **Issue 3** — Add delay measurements to BVDD sweep.
4. **Issue 4** — Fix plot_all.py to use real data only.
5. **Issue 6** — Add worst-case power measurement.
6. **Issue 5** — Down-shifter characterization.
7. **Issue 8** — Update README with verified data.
8. **Issue 7** — Redraw schematics (time permitting).

After each fix, run `bash run_block.sh > run.log 2>&1` and verify `python3
evaluate.py` still shows 10/10 PASS. Commit after each milestone.

---

## Absolute Rules (carried from program.md)

- Do NOT modify `specification.json`, `evaluate.py`, or `program.md`
- Every transistor must be a real Sky130 PDK device
- No behavioral models except testbench stimulus
- All simulations in ngspice
- Every spec verified by simulation at worst-case conditions
