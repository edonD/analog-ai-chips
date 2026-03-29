# Block 04: Current Limiter — Design Program v3

**Why v3 exists:** v2 fixed the 4 hardcoded metrics from v1 and achieved honest 9/9. An independent audit of v2 found 3 remaining testbench methodology weaknesses plus 2 design fragilities. This program fixes every one of them.

---

## 0. v2 Audit Findings (What v3 Must Fix)

### Testbench Methodology Issues

#### Issue 1: `pvdd_impact_mV` is a logic gate, not a measurement

**Current code (tb_ilim_normal.spice lines 62-68):**
```spice
if trip_mA > 50
  let pvdd_impact = 0    ← asserted, never measured
else
  let pvdd_impact = (50 - trip_mA)   ← wrong units (mA, not mV)
end
```

This says "if the limiter trips above 50mA, assume zero impact." That's a reasonable *argument* but not a *measurement*. The spec asks for the PVDD voltage difference due to the limiter at 50mA load. The limiter adds a sense PMOS to the gate node, a detection NMOS drawing subthreshold current, and a pull-up resistor from bvdd — these have real (if small) effects even below the trip point.

**v3 fix:** Two separate DC simulations at the exact same operating point:

```spice
* Simulation A: WITH limiter — sweep gate, find Vgate that produces 50mA
dc Vgate 7 0 -0.02
meas dc vgate_50 find gate_drive when i(Vpvdd)=50e-3 cross=1
* Record the current at this gate voltage
let ipvdd_with = 50    * (by construction)

* Simulation B: WITHOUT limiter — use same Vgate, measure current
* Remove limiter influence by disconnecting clamp: set det_n = bvdd (clamp OFF)
* OR: run a second netlist without the limiter subcircuit

* Delta = |Ipvdd_with - Ipvdd_without| at same Vgate → convert to mV via load impedance
* OR: at fixed Iload=50mA, measure Vpvdd with and without → delta in mV
```

The cleanest approach: **run two separate ngspice invocations** — one with the limiter subcircuit, one with just a wire from gate_drive to gate_int. Compare the drain current at the same gate voltage. If the currents differ, compute the equivalent PVDD impact as `delta_I * Rload`.

Alternatively (simpler, same result): the testbench already forces Vpvdd=5V, so "PVDD impact" means the current difference at the same gate voltage. If limiter draws current from the gate node (even below trip), it shifts the gate voltage slightly, changing Id. Measure this by:
1. Sweep gate WITH limiter → find Iload at each Vgate
2. Sweep gate WITHOUT limiter → find Iload at each Vgate
3. At the Vgate that gives 50mA without limiter, read the with-limiter current
4. Delta_mA = 50 - Iwith. Convert: delta_mV = delta_mA * (Vpvdd/Iload) = delta_mA * 100 ohm

**Implementation:** Create two spice files (or use `alter` to disconnect the limiter). The "without" case can be achieved by adding a second voltage source that forces det_n = bvdd (disabling the clamp), or by instantiating a second copy of the pass device without the limiter and comparing.

The simplest robust approach:
1. `tb_ilim_normal_with.spice` — full circuit, DC sweep, wrdata of i(Vpvdd) vs Vgate
2. `tb_ilim_normal_without.spice` — same circuit but Xlim removed (pass device gate driven directly), DC sweep, wrdata
3. In ngspice control block of the "with" file: load both data files, interpolate, find delta at 50mA
4. Print `pvdd_impact_mV: <measured value>`

If this is too complex for a single testbench, create a Python wrapper that runs both and computes the delta.

#### Issue 2: Short-circuit test uses wrong conditions and unfair comparison

**Current problems:**
- `Vpvdd pvdd 0 DC 1.0` — pvdd forced to 1V is not a realistic short. A real short has pvdd ≈ 0V. And in a real LDO, pvdd isn't forced — it collapses under the load.
- "Without limiter" test changes Rgate from 10k to 1 ohm. This tests "what if the gate driver were infinitely stiff" not "what if the limiter weren't there." The clamp PMOS can't overcome 1 ohm, so of course the current is higher.

**v3 fix:**

Test condition A (near-short with limiter): Keep the limiter. Use `Vpvdd pvdd 0 DC 0.1` (100mV — realistic near-short, pass device has Vds ≈ 6.9V). Gate driven to 0V through 10k.

Test condition B (near-short without limiter): **Remove the limiter subcircuit entirely.** Do NOT change Rgate. Create a separate spice file `tb_ilim_short_nolim.spice` that is identical to `tb_ilim_short.spice` except:
- Remove `.include "design.cir"` and `Xlim ...` line
- Connect gate_int directly: wire from Rgate to gate_int, no limiter on gate_int

Then both tests use the same 10k Rgate, same pvdd, same everything — only difference is limiter present vs absent. This is a fair A/B comparison.

Additionally: run the short-circuit test at pvdd=0V (true dead-short). If convergence fails, use pvdd=0.1V and note the limitation. Try pvdd=5V too (overload near regulation — this is where the trip point test already operates).

**Report:**
```
short_circuit_pvdd0p1_with_mA: <value>
short_circuit_pvdd0p1_without_mA: <value>
short_circuit_reduction_x: <ratio>
```

#### Issue 3: Oscillation check window misses the critical period

**Current code (tb_ilim_transient.spice lines 79-86):**
```spice
meas tran ghi max v(gate_int) from=40u to=50u    ← only last 10µs
meas tran glo min v(gate_int) from=40u to=50u
```

Oscillation/ringing is most likely to occur right after the gate step (t=5-20µs), not at t=40-50µs when the circuit has fully settled. The current window only catches sustained oscillation, not decaying ringing.

**v3 fix:** Three measurement windows:

```spice
* Window 1: Early response (5-15us) — catches initial ringing
meas tran ghi_early max v(gate_int) from=5u to=15u
meas tran glo_early min v(gate_int) from=5u to=15u
let early_ripple_mV = (ghi_early - glo_early) * 1000

* Window 2: Mid settling (15-30us) — catches sustained oscillation
meas tran ghi_mid max v(gate_int) from=15u to=30u
meas tran glo_mid min v(gate_int) from=15u to=30u
let mid_ripple_mV = (ghi_mid - glo_mid) * 1000

* Window 3: Steady state (40-50us) — confirms final stability
meas tran ghi_late max v(gate_int) from=40u to=50u
meas tran glo_late min v(gate_int) from=40u to=50u
let late_ripple_mV = (ghi_late - glo_late) * 1000

echo "early_gate_ripple_mV: $&early_ripple_mV"
echo "mid_gate_ripple_mV: $&mid_ripple_mV"
echo "late_gate_ripple_mV: $&late_ripple_mV"
```

Same for current ripple. The `no_oscillation` pass condition:
- Early window: gate ripple < 2V (large transient OK during step)
- Mid window: gate ripple < 500mV (should be settling)
- Late window: gate ripple < 200mV AND current ripple < 5mA (must be stable)

Additionally: report ALL three windows in run.log. The late window determines the spec pass, but early/mid windows are logged for visibility.

### Design Fragilities (Characterize Even If Not Fixed)

#### Issue 4: Rgate dependence — trip point changes with error amp impedance

**Current state:** Noted in results.md as "3.3x variation across Rgate 1k-1M" but never measured in a testbench.

**v3 fix:** Create `tb_ilim_rgate_sweep.spice` that runs the trip-point DC sweep at Rgate = 1k, 3k, 10k, 30k, 100k, 300k, 1M. Report the trip current at each. This is informational (not a spec), but it quantifies the design's dependence on the error amp.

```
rgate_dependence_1k_mA: <value>
rgate_dependence_10k_mA: <value>
rgate_dependence_100k_mA: <value>
rgate_dependence_1M_mA: <value>
```

If the ratio of max/min trip across Rgate is > 2x, flag it as a design weakness in results.md.

#### Issue 5: PVT spread is 3.1x

**Current state:** 44mA (FF-40C) to 137mA (SS-150C). This is within the generous spec window (50-100mA for corner limits) but FF-40C at 44mA is only 6mA above the 50mA rated load — a thin margin.

**v3 action:** This is a known circuit limitation of the Vth-based detection without cascode. v2 attempted a cascode and source degeneration — both made SS150 worse. Document the tradeoff clearly:

- The PVT spread is dominated by the detection NMOS Vth temperature coefficient
- A cascode would fix Vds matching but introduces a new failure mode (cascode turns off during shorts)
- Source degeneration reduces gain → requires more sense current → raises trip but reduces SS150 margin

For v3: characterize and document, don't attempt to fix unless a new topology idea emerges. The current design passes all specs. Focus on testbench integrity, not chasing an architectural change that was already tried and failed.

---

## 1. Absolute Rules (Inherited from v2, Extended)

Everything from v2 rules 1-8, plus:

9. **A/B comparisons must change ONE variable.** When measuring "with vs without limiter," the ONLY difference between the two simulations must be the presence of the limiter. Do not change Rgate, pvdd, bvdd, or any other parameter simultaneously. If you can't run without the limiter in the same netlist, create a second netlist.

10. **Oscillation checks must cover the entire transient, not just the tail.** Ringing at t=5-20µs is more dangerous than ringing at t=40-50µs because it represents instability during the actual limiting event.

11. **results.md numbers must be auto-extracted from run.log, not hand-typed.** Any discrepancy between results.md and run.log is a documentation bug. Create a script or use grep to populate the table.

---

## 2. Testbench Fix Specifications

### Fix 1: `tb_ilim_normal.spice` — Real PVDD Impact Measurement

**Delete the current if/else logic gate.** Replace with actual measurement.

**Method:** Two DC sweeps in the same ngspice run.

Sweep 1 (WITH limiter — already in circuit):
```spice
dc Vg 7 0 -0.02
wrdata ilim_normal_with i(Vpvdd)
```

Sweep 2 (WITHOUT limiter — disable clamp by forcing det_n = bvdd):
To disable the limiter without restructuring the netlist, inject a voltage source that holds det_n at bvdd:
```spice
* After first sweep, force det_n to bvdd to disable clamp
* V_disable xlim.det_n 0 DC 7.0   ← can't do this inside subckt
```

Since we can't probe into the subcircuit easily, the cleanest approach is to run a separate ngspice invocation. Create `tb_ilim_normal_nolim.spice` — identical pass device, identical Vpvdd, identical Rgate, but **no limiter subcircuit** (gate_drive → Rgate → gate_int directly to pass device gates).

Then in run_block.sh:
```bash
with_data=$(ngspice -b tb_ilim_normal.spice 2>&1)
nolim_data=$(ngspice -b tb_ilim_normal_nolim.spice 2>&1)
# Extract current at 50mA operating point from both
# Compare and compute delta
```

Or use a Python helper:
```python
# parse_pvdd_impact.py
# Read both wrdata files, find gate voltage for 50mA, compare currents
```

**Expected result:** The impact should be very small (< 1mV) since the limiter is OFF below trip. But measure it, don't assume it.

### Fix 2: `tb_ilim_short.spice` — Fair A/B Short-Circuit Test

**Delete the `alter Rgate = 1` hack.** Replace with a proper A/B comparison.

Create TWO files:

**`tb_ilim_short.spice`** (with limiter):
```spice
* pvdd=0.1V (near dead-short), gate=0V through 10k, limiter present
Vpvdd pvdd 0 DC 0.1
Vg gate_drive 0 DC 0.0
Rgate gate_drive gate_int 10k
.include "design.cir"
Xlim gate_int bvdd pvdd 0 ilim_flag current_limiter
```

**`tb_ilim_short_nolim.spice`** (without limiter):
```spice
* IDENTICAL except no limiter — gate_int connects directly
Vpvdd pvdd 0 DC 0.1
Vg gate_drive 0 DC 0.0
Rgate gate_drive gate_int 10k
* NO .include "design.cir", NO Xlim line
```

run_block.sh runs both, extracts currents, computes ratio. This is a fair comparison — same Rgate, same pvdd, only limiter differs.

### Fix 3: `tb_ilim_transient.spice` — Full-Window Oscillation Check

**Keep existing measurements. Add early and mid windows.**

Add before the existing window check:
```spice
* Early response window (5-15us)
meas tran ghi_early max v(gate_int) from=5u to=15u
meas tran glo_early min v(gate_int) from=5u to=15u
let early_gate_ripple_mV = (ghi_early - glo_early) * 1000

meas tran ihi_early max i(Vpvdd) from=5u to=15u
meas tran ilo_early min i(Vpvdd) from=5u to=15u
let early_current_ripple_mA = (ihi_early - ilo_early) * 1000

* Mid window (15-30us)
meas tran ghi_mid max v(gate_int) from=15u to=30u
meas tran glo_mid min v(gate_int) from=15u to=30u
let mid_gate_ripple_mV = (ghi_mid - glo_mid) * 1000

echo "early_gate_ripple_mV: $&early_gate_ripple_mV"
echo "mid_gate_ripple_mV: $&mid_gate_ripple_mV"
```

Keep existing late window (40-50µs) for the spec pass/fail. Log early/mid for visibility.

**For `no_oscillation` determination:** Use the late window (same as v2) for the binary pass/fail, but if early/mid ripple is extreme (gate > 3V, current > 50mA), flag a warning in run.log.

### New TB: `tb_ilim_rgate_sweep.spice` — Rgate Dependence Characterization

**Informational, not spec.** Sweep Rgate from 1k to 1M and measure trip at each.

```spice
.param rg_val = 10k
Rgate gate_drive gate_int {rg_val}

.control
* Cannot sweep .param directly in ngspice. Use multiple alter+dc sequences.
foreach rg 1000 3000 10000 30000 100000 300000 1000000
  alter Rgate = $rg
  dc Vgate 7 0 -0.05
  let il = i(Vpvdd) * 1000
  let mx = vecmax(il)
  echo "rgate_${rg}_trip_mA: $&mx"
end
```

Report in run.log. Not parsed by evaluate.py — just logged for engineering visibility.

---

## 3. run_block.sh Updates

### Remove Rgate=1 short-circuit hack
Replace the single `tb_ilim_short.spice` call with two calls:
```bash
echo "--- Running tb_ilim_short.spice (with limiter) ---"
short_with=$(ngspice -b tb_ilim_short.spice 2>&1 | grep "^short_circuit_mA:" | awk '{print $2}')
echo "short_circuit_with_limiter_mA: $short_with"

echo "--- Running tb_ilim_short_nolim.spice (without limiter) ---"
short_without=$(ngspice -b tb_ilim_short_nolim.spice 2>&1 | grep "^short_circuit_mA:" | awk '{print $2}')
echo "short_circuit_without_limiter_mA: $short_without"
```

### Add pvdd_impact from real comparison
```bash
echo "--- Running tb_ilim_normal.spice ---"
# ... extract sense_quiescent_uA as before ...
# ... extract pvdd_impact_mV from actual with/without comparison ...
```

### Add Rgate sweep (informational)
```bash
echo "--- Running tb_ilim_rgate_sweep.spice ---"
ngspice -b tb_ilim_rgate_sweep.spice 2>&1 | grep "^rgate_" || true
```

---

## 4. results.md Auto-Update

**After each run, results.md must be regenerated from run.log.**

Create `update_results.py`:
```python
# Reads run.log, extracts all metrics, writes results.md with exact values
# No hand-rounding — values copied verbatim from simulation
```

Or at minimum: run_block.sh appends a `--- Machine-extracted ---` section to results.md with grep output from run.log.

---

## 5. Execution Order

### Step 1: Fix tb_ilim_normal.spice (PVDD impact)
1. Create `tb_ilim_normal_nolim.spice` (no limiter variant)
2. Rewrite the pvdd_impact measurement to do a real with/without comparison
3. Run both, extract delta, print `pvdd_impact_mV: <measured>`
4. Commit

### Step 2: Fix tb_ilim_short.spice (fair A/B)
1. Change `Vpvdd` from 1.0V to 0.1V
2. Create `tb_ilim_short_nolim.spice` (identical but no limiter)
3. Remove the `alter Rgate = 1` hack
4. Update run_block.sh to run both files
5. Commit

### Step 3: Fix tb_ilim_transient.spice (oscillation windows)
1. Add early (5-15µs) and mid (15-30µs) ripple measurements
2. Log all three windows
3. Keep late window for spec pass/fail
4. Commit

### Step 4: Add Rgate characterization
1. Create `tb_ilim_rgate_sweep.spice`
2. Add to run_block.sh (informational section)
3. Document findings in results.md
4. Commit

### Step 5: Sync results.md to run.log
1. After full run, verify every number in results.md matches run.log exactly
2. Fix any discrepancies
3. Commit

### Step 6: Run full suite, verify 9/9
If any metric drops to UNMEASURED or FAIL, fix the testbench or circuit. Do not revert to logic-gate shortcuts.

### LOOP FOREVER
Continue optimizing circuit parameters. Same improvement criterion as v2.

---

## 6. What v3 Does NOT Attempt

- **Cascode on sense mirror** — tried in v2, made SS150 worse. Don't retry unless new topology idea.
- **Source degeneration** — tried in v2, reduced primary metric. Don't retry.
- **Fixing PVT spread** — 3.1x is within spec. The fix requires architectural change (current mirror comparator with tracking reference), which is a v4 effort.
- **Fixing Rgate dependence** — requires proportional feedback redesign, also a v4 effort. v3 characterizes it; v4 would fix it.

v3 scope is **testbench integrity only** — make every measurement bulletproof. The circuit stays the same unless a spec fails under honest measurement.
