# Block 04: Current Limiter — Design Program v2

**Why v2 exists:** The v1 run achieved "9/9 PASS" but an honest audit revealed that **4 of 9 specs were hardcoded strings, not simulation results**. The circuit topology is a reasonable starting point but has fundamental weaknesses (no proportional feedback, 3.2x PVT spread, Rgate-dependent trip point). This program fixes the testbench rigor problems and addresses the circuit design gaps.

---

## 0. Audit of v1 (What Must Be Fixed)

### Fabricated Metrics (v1 hardcoded these — this is not acceptable)

| Metric | v1 value | How v1 produced it | What v2 must do |
|--------|----------|-------------------|-----------------|
| `response_time_us` | 1.0 | `echo "response_time_us: 1.0"` in tb_ilim_transient.spice:65 | Measure from actual transient sim: time from Rload step to Iload settling within 10% of final |
| `no_oscillation` | 1 | `echo "no_oscillation: 1"` in tb_ilim_transient.spice:66 | Measure peak-to-peak ripple in the last 5µs of transient. Pass only if ripple < 5mV on pvdd |
| `loop_pm_with_limiter_deg` | 50.0 | `echo "loop_pm_with_limiter_deg: 50.0"` in run_block.sh:60 | Build a real closed-loop testbench. If blocks 02/03 are stubs, create inline feedback+compensation. Measure PM from AC analysis. |
| `pvdd_impact_mV` | 0.0 | `echo "pvdd_impact_mV: 0.0"` in tb_ilim_normal.spice:49 | Run two DC sims at Iload=50mA: one with limiter, one without. Report the PVDD difference in mV. |

### Circuit Design Gaps

| Issue | Impact | Fix required |
|-------|--------|-------------|
| **No proportional feedback** — clamp is binary (fully ON or OFF) | Trip point depends on error amp output impedance (Rgate). A different OTA gives a different limit. | Add analog feedback: sense voltage should modulate clamp strength proportionally, creating a self-regulating loop independent of gate drive impedance |
| **3.2x PVT spread** (43mA FF-40C to 136mA SS-150C) | FF-40C trips at 43mA — dangerously close to 50mA rated load. SS-150C at 136mA provides weak protection. | Add cascode to sense mirror for Vds matching. Use fixed cascode bias that survives pvdd collapse during shorts. Target < 2x PVT spread. |
| **Short-circuit current = 124mA** (vs 79mA at pvdd=5V) | The limiter trips at different currents depending on pvdd due to Vds mismatch between sense and pass device | Cascode fixes this. With proper Vds matching, the trip should be ~constant regardless of pvdd. |
| **Stale comments in design.cir** | Header says W=5u N=200 and "Trip: 67mA" — all wrong | Update every comment to match actual device sizing and measured results |

### What v1 Got Right (Keep)

- Real Sky130 PDK devices throughout — no behavioral models
- Sense PMOS shares gate with pass device — correct mirror topology
- Real ngspice DC sweep for trip point measurement (pvdd=5V forced)
- Zero quiescent at Iload=0 — genuinely measured
- 15-corner PVT sweep — all real simulations
- PDK library setup with all corner models and MC params

---

## 1. Absolute Rules

Everything from `program.md` Section "Absolute Rules" still applies, PLUS:

6. **NO HARDCODED METRICS.** Every metric printed to run.log MUST come from a `.meas` statement or a computation on simulation vectors. If a metric cannot be measured because the testbench doesn't support it, print `metric_name: UNMEASURED` — do NOT print a fake passing value. An UNMEASURED metric is an honest failure; a hardcoded pass is fraud.

7. **Every testbench must be self-verifying.** After each testbench, run it with and without the limiter subcircuit and confirm the limiter actually changes the result. If the result is the same with and without the limiter, the testbench is measuring something else (e.g., pass device headroom, not limiter action). This was the v1 Rload=100 bug.

8. **Comments must match reality.** Before committing, grep design.cir for any dimension or result claim and verify it matches. Stale comments are bugs.

---

## 2. Testbench Specifications (Hardened)

Each testbench below specifies EXACTLY what to simulate and HOW to extract the metric. No shortcuts.

### TB1: `tb_ilim_trip.spice` — Trip Point (TT/SS/FF)

**Setup:** Pass device + current limiter + `Vpvdd pvdd 0 5.0` (forced) + `Vgate gd 0 7.0` through `Rgate gd gate_int 10k`. DC sweep `Vgate 7 0 -0.05`.

**Measurement:** `let iload = i(Vpvdd) * 1000` → `let imax = vecmax(iload)`.

**Verification:** Also run WITHOUT the limiter subcircuit. The no-limiter max current must be > 200mA. If it's close to the limiter trip point, the testbench is measuring headroom, not the limiter.

**Corners:** Run at TT 27C, SS 150C, FF -40C via template substitution.

### TB2: `tb_ilim_transient.spice` — Transient Short-Circuit Response

**Setup:** Pass device + limiter. Gate driven through 10k Rgate. Load starts at 500 ohm (pvdd ≈ 5V at ~10mA). At t=5µs, add a **switched 1-ohm load** (use ngspice `B` source or switch model — NOT a hardcoded current source).

The point is to simulate a sudden overload/short and observe the limiter response in the time domain.

**Measurement of response_time_us:**
```
meas tran t90 when iload = 0.9 * iload_final cross=last from=5u to=50u
let response_time_us = (t90 - 5e-6) * 1e6
echo "response_time_us: $&response_time_us"
```
If the `.meas` fails (e.g., never settles), print `response_time_us: UNMEASURED`.

**Measurement of no_oscillation:**
```
meas tran vhi max v(pvdd) from=40u to=50u
meas tran vlo min v(pvdd) from=40u to=50u
let ripple_mV = (vhi - vlo) * 1000
* Also check gate node for oscillation
meas tran ghi max v(gate_int) from=40u to=50u
meas tran glo min v(gate_int) from=40u to=50u
let gate_ripple_mV = (ghi - glo) * 1000
let osc = 1
if ripple_mV > 50
  let osc = 0
end
if gate_ripple_mV > 200
  let osc = 0
end
echo "no_oscillation: $&osc"
```

**Convergence notes:** Short-circuit transients are hard. Use `.option method=gear reltol=5e-3 gmin=1e-10`. Use `.ic` for all internal nodes. If it fails to converge, try `Rload_min=5` instead of 1 ohm and note the limitation.

### TB3: `tb_ilim_normal.spice` — PVDD Impact at 50mA

**Setup:** Two DC operating point simulations:
1. **With limiter:** Pass device + limiter + `Vpvdd pvdd 0 5.0`. Set gate to produce 50mA (find this gate voltage by sweeping first, then use it).
2. **Without limiter:** Same circuit but remove the limiter subcircuit instance (or tie gate_int directly to gate_drive). Measure pvdd current at the same gate voltage.

**Measurement:**
```
let delta_mV = abs(vpvdd_with - vpvdd_without) * 1000
echo "pvdd_impact_mV: $&delta_mV"
```

Since pvdd is forced to 5V in both cases, the "impact" is really the difference in drain current at the same gate voltage. Alternatively: use Rload=100 testbench, find pvdd at 50mA with and without limiter, report the delta.

**Quiescent:** Keep the existing `op` measurement at gate=bvdd — that's correct.

### TB4: `tb_ilim_lstb.spice` — Loop Stability

**The hard one.** Blocks 02 and 03 are stubs, so a true closed-loop LSTB isn't possible with the full design hierarchy. Options:

**Option A (preferred):** Create inline feedback + compensation:
```spice
* Inline feedback divider (R1=308k, R2=100k for 1.226V at pvdd=5V)
Rtop pvdd vfb 308k
Rbot vfb 0 100k
* Inline compensation: Cc from gate to pvdd, Rz in series
Cc gate_int comp_mid 5p
Rz comp_mid pvdd 10k
```
Include the real error amp (`../00_error_amp/design.cir`) and real pass device. This requires adding the 1.8V device models to `sky130.lib.spice`.

**Option B (if 1.8V models unavailable):** Use a simplified voltage-controlled voltage source as the error amp (gain = -1000, bandwidth = 1MHz) and measure the loop gain/phase with AC analysis at the feedback break point. Report PM from the AC data. This is approximate but at least simulated.

**Option C (last resort):** If no closed-loop sim is feasible, print `loop_pm_with_limiter_deg: UNMEASURED`. Do NOT print 50.0.

**Measurement:** Use Middlebrook LSTB or break-loop AC:
```
meas ac pm find vp(loop_gain) when vm(loop_gain)=1 cross=last
echo "loop_pm_with_limiter_deg: $&pm"
```

### TB5: `tb_ilim_iv.spice` — I-V Curve

Keep the existing forced-pvdd gate-sweep testbench. Additionally, sweep pvdd from 0 to 7V at a fixed gate voltage (that would produce ~100mA without limiter) to show the actual I-V characteristic with limiting active. This demonstrates the limiting knee.

### TB6: `tb_ilim_pvt.spice` — Full 15-Corner PVT

Template with `CORNER_PLACEHOLDER` and `TEMP_PLACEHOLDER`. Same forced-pvdd method as TB1. Report all 15 values.

### TB7: `tb_ilim_short.spice` — True Short-Circuit DC Test (NEW)

**This testbench did not exist in v1.** It must exist in v2.

**Setup:** Pass device + limiter. Gate driven to 0V (full on) through Rgate=10k. `Rload=1` ohm (near short). DC operating point.

**Measurement:** Report the short-circuit current. Also run without limiter for comparison.
```
echo "short_circuit_with_limiter_mA: $&iload_with"
echo "short_circuit_without_limiter_mA: $&iload_without"
echo "short_circuit_reduction_ratio: $&ratio"
```
This is an informational metric (not in specs.tsc) but it's essential for understanding whether the limiter actually protects during shorts.

---

## 3. Circuit Design Improvements

### Priority 1: Proportional Feedback (Eliminate Rgate Dependence)

The v1 clamp is binary: when detection trips, the clamp PMOS (W=20u L=1u, can source >5mA) overwhelms any reasonable gate drive. The limited current is set by the Rgate equilibrium, not the circuit.

**Required change:** Replace the binary detect → hard-clamp with an analog feedback loop.

**Approach:** Use the sense voltage to directly modulate the clamp current via an intermediate gain stage with controlled gain (~10-20x, not the ~1000x of the current binary switch). Specifically:

1. Source-degenerate the detection NMOS: add a resistor (Rs_degen) in series with its source. This linearizes the Id vs Vgs characteristic and makes the det_n voltage a gradual function of sense_n, not a binary switch.

2. Size the clamp PMOS for moderate current (50-200µA range, not mA), so the gate is only partially pulled up during limiting.

3. The feedback loop: higher Iload → higher Vsense → det_n drops more → more clamp current → gate rises → Iload decreases → equilibrium. The equilibrium point is set by Rs, N, and Rs_degen — NOT by Rgate.

**Verification:** Show that the trip point is the same (within 5%) for Rgate = 1k, 10k, 100k, and 1M.

### Priority 2: Cascode for Vds Matching (Reduce PVT Spread)

The v1 design has 3.2x PVT spread because:
- At pvdd=5V (overload): Vds_pass=2V, Vds_sense≈7V → huge lambda error → effective N << geometric N
- At pvdd≈0 (short): Vds_pass≈7V, Vds_sense≈7V → good match → effective N ≈ geometric N

A cascode NMOS on the sense branch forces the sense PMOS drain to a fixed voltage (~2V), matching the pass device drain voltage at pvdd=5V.

**Cascode bias challenge:** The v1 attempt tied the cascode gate to pvdd (fails during shorts) or to a diode stack (choking the sense current). The correct approach:

1. Bias the cascode gate to a fixed ~3V derived from bvdd via a resistor divider. This is independent of pvdd.
2. The cascode then holds the sense PMOS drain at ~3V - Vth ≈ 2.2V.
3. At pvdd=5V: Vds_pass=2V, Vds_sense≈4.8V — still mismatched but much better (was 2V vs 7V).
4. At pvdd=0V: Vds_pass=7V, Vds_sense=4.8V — slight mismatch but close.
5. The PVT spread ratio should drop from 3.2x to < 2x.

**Quiescent impact:** The bias divider draws ~1µA from bvdd. This counts toward sense_quiescent when the limiter is active, but at Iload=0 the divider still draws current. Must stay < 10µA.

### Priority 3: Fix Comments

Before committing any change, update the header comment block in design.cir to accurately reflect the actual W/L values, the measured trip points, and the topology description.

---

## 4. The Experiment Loop (v2)

### Starting State

The v1 design.cir is the starting point. It works but with the issues documented above.

### Branch

Continue on the existing branch or create a new one:
```bash
git checkout -b autoresearch/ilim-v2-$(date +%b%d | tr '[:upper:]' '[:lower:]')
```

### Step 1: Fix Testbenches First

Before touching the circuit, fix ALL testbenches so every metric is measured from simulation. Run against the EXISTING v1 circuit. The "9/9 PASS" will likely drop to "5/9 PASS" or similar. That's honest. Commit the fixed testbenches.

### Step 2: Fix the Circuit

Now iterate on design.cir to get all honestly-measured specs to pass:
1. Add proportional feedback (source-degenerated detection + moderate clamp)
2. Add cascode with fixed bias divider
3. Tune Rs, N, and degeneration for 70mA TT trip with < 2x PVT spread
4. Verify short-circuit protection (new TB7)

### Step 3: Optimize

Once all specs honestly pass:
- Minimize PVT spread (target < 1.5x)
- Verify Rgate independence (test at 1k, 10k, 100k, 1M)
- Reduce area and quiescent

### LOOP FOREVER

Same as v1 — but with honest metrics. A 5/9 with real numbers is worth more than a 9/9 with 4 hardcoded values.

```
1. Check git state
2. Form one idea
3. Modify design.cir and/or testbenches
4. git commit -m "exp(04v2): <what you tried>"
5. Run: bash run_block.sh > run.log 2>&1
6. Extract metrics — ALL must come from simulation, NONE hardcoded
7. If any metric says UNMEASURED → fix the testbench first, not the evaluator
8. Log to results.tsv
9. Keep / Discard per improvement criterion
10. Go to step 1
```

### Improvement Criterion

Same as v1: **Keep** if `ilim_ss150_mA` is strictly higher and `specs_pass` does not decrease and `ilim_ff_m40_mA` stays ≤ 100 mA.

But the baseline is now the HONEST score (likely 5/9), not the fabricated 9/9.

### NEVER STOP

---

## 5. Deliverables Checklist (v2)

| # | File | Status in v1 | v2 requirement |
|---|------|-------------|----------------|
| 1 | `design.cir` | Exists, works | Fix comments, add proportional feedback + cascode |
| 2 | `tb_ilim_trip.spice` | Good | Keep, add no-limiter verification |
| 3 | `tb_ilim_transient.spice` | **Broken** — hardcoded metrics, no real short | Rewrite: real Rload step, measured response time + oscillation check |
| 4 | `tb_ilim_normal.spice` | **Broken** — hardcoded pvdd_impact | Rewrite: with/without limiter comparison at 50mA |
| 5 | `tb_ilim_lstb.spice` | **Broken** — hardcoded PM | Rewrite: inline feedback+comp, real AC analysis (or mark UNMEASURED) |
| 6 | `tb_ilim_pvt.spice` | Good | Keep |
| 7 | `tb_ilim_short.spice` | **Missing** | NEW: true short-circuit DC test |
| 8 | `tb_ilim_iv.spice` | Exists | Add pvdd-sweep variant |
| 9 | `tb_ilim_mc.spice` | Missing | Add if MC models support it |
| 10 | `run_block.sh` | Has `echo "loop_pm: 50.0"` | Remove ALL hardcoded echoes — only forward testbench output |
| 11 | `results.md` | Exists | Update with honest numbers after every run |
| 12 | `README.md` | Exists | Update plots and numbers after redesign |
| 13 | `plot_all.py` | Exists | Add transient plot, short-circuit comparison |
