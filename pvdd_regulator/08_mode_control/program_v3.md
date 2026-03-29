# Block 08: Mode Control — Fix Program v3

## Status

16/16 specs pass but 2 are broken. The circuit and hysteresis are solid. Only testbench fixes remain.

## Defect 1: Glitch Detection Passes by Accident

**File:** `tb_mc_ramp_normal.spice`

The `.meas` commands that look for extra edges (3rd rising edge of bypass_en, etc.) FAIL because no such edge exists. When `.meas` fails in ngspice, the variable is undefined. The subsequent `if g_by3 > 0.1` is a no-op on an undefined variable, so `gf` stays 1. This is an accidental pass, not a real check.

**Fix:** After each `.meas`, check if the variable exists. If it does NOT exist, that means no extra edge was found, which is GOOD (no glitch). If it DOES exist, a glitch was found. Reverse the logic:

```spice
* Try to find a 3rd rising edge of bypass_en (should NOT exist)
meas tran g_by3 FIND v(bvdd) WHEN v(bypass_en)=2.5 RISE=3 TD=2u

* In ngspice, failed meas returns 0 or leaves variable undefined.
* A successful meas (found the edge) means there IS a glitch.
* Use: if the measurement succeeded AND returned a positive value, flag glitch.
```

The simplest reliable approach: use Python (`extract_metrics.py`) to count zero-crossings in the wrdata output file. For each output signal, count how many times it crosses 50% of its max value. Compare to expected count. If more → glitch.

Or simpler: just use the `.meas` approach but with FALL instead of RISE for signals that should only fall once, and test both directions. The key fix is the logic inversion — a failed `.meas` means NO glitch (good), a successful one means glitch (bad).

## Defect 2: PVT Corners Not Tested

**File:** `tb_mc_pvt.spice`

Currently hardcoded to `.lib "../sky130.lib.spice" tt` and runs at 27°C only. The spec requires thresholds within ±15% across SS/FF/SF/FS corners.

**Fix:** Run at least the 5 process corners at 27°C. The simplest ngspice approach:

Option A: Create 5 separate testbench files (tb_mc_pvt_tt.spice, tb_mc_pvt_ss.spice, etc.) and run them sequentially. Pick the worst-case `thresh_max_error_pct`.

Option B (preferred): Use a single testbench with `.lib` switching. Since ngspice doesn't support looping over corners natively in batch mode, create a wrapper:

1. In `tb_mc_pvt.spice`, use a `.param corner_id = 0` and `.if` blocks, OR
2. Create a Python wrapper `run_pvt.py` that:
   - Generates 5 temp spice files, each with a different `.lib` line
   - Runs each with ngspice
   - Parses all results
   - Prints the worst-case metrics

The metrics to print from tb_mc_pvt.spice (or the wrapper):
```
thresh_por_V: <worst case>
thresh_ret_V: <worst case>
thresh_pup_V: <worst case>
thresh_act_V: <worst case>
thresh_max_error_pct: <worst across all corners>
```

**Important:** `run_block.sh` calls `tb_mc_pvt.spice` directly. So either fix that file to handle corners internally, or have it call the wrapper. Do NOT modify `run_block.sh`.

## Constraints

- Do NOT modify `specification.json`, `evaluate.py`, `program.md`, `specs.tsc`, or `run_block.sh`
- Do NOT break the existing 14 passing specs — only fix the 2 broken ones
- The circuit (`design.cir`) is DONE — do not change it unless a PVT corner fails
- Commit when done: `git add pvdd_regulator/08_mode_control/ && git commit -m "exp(08): fix glitch detection + PVT corners"`

## Execution

1. Fix `tb_mc_ramp_normal.spice` glitch detection logic
2. Fix `tb_mc_pvt.spice` to run 5 corners
3. Run `bash run_block.sh > run.log 2>&1`
4. Run `python3 evaluate.py`
5. If all 16/16 pass → commit and stop
6. If PVT corners fail → adjust ladder in design.cir, re-run
