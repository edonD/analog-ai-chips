# Block 07: Zener Clamp — v4 Audit & Mandatory Fix List

## Status: 9/9 TT — BUT 4 REAL PROBLEMS REMAIN UNFIXED

The previous "resolution" was lazy — it documented problems instead of fixing them.
This document defines **hard engineering tasks** that require circuit changes, not writeups.

---

## PROBLEM A: Transient Peak Fails at Rsrc < 10 ohm (MUST FIX)

**The problem:** The spec says "10V/us ramp, 200pF Cload, peak < 6.5V." The current
transient testbench uses Rsrc=10 ohm. At Rsrc=5 ohm (a realistic pass-device
impedance for a large PMOS), the peak is **6.70V — FAIL**. At Rsrc=1 ohm: **7.3V**.

The previous "fix" was to write a paragraph justifying why 10 ohm is OK. That is
not a fix. The circuit must handle Rsrc=5 ohm or lower.

**Root cause:** The Cff=20pF feedforward cap is the only fast path to the gate.
During a fast ramp, Cff couples PVDD to vg. But the clamp NMOS at moderate vg
(~1.5V) can only sink ~500mA. Through 5 ohm from 8V source: (8-6.5)/5 = 300mA
is needed. This seems possible, but the gate drive isn't fast/strong enough.

**What to try:**
1. **Increase Cff to 50-100pF.** Larger Cff couples more of the ramp to vg,
   giving higher gate drive during transients. Check that this doesn't cause
   startup problems (Cff couples during power-up too — see Problem D).
2. **Add a parallel fast diode stack** (body=GND, short-channel L=0.5u) in
   parallel with the precision clamp. The diode stack handles the first ~100ns
   of the transient; the precision clamp takes over for steady-state clamping.
   This is the "hybrid" approach from program.md.
3. **Increase clamp NMOS width** (m=40 or m=60 instead of m=20). More gm at
   lower vg means the clamp can sink more current with less gate drive.

**Pass criterion:** transient_peak_V < 6.5V with Rsrc=5 ohm. Test with Rsrc=1
as a stretch goal.

**IMPORTANT: do NOT "solve" this by writing documentation. Change the circuit.**

---

## PROBLEM B: 6/15 PVT Corners Fail (MUST IMPROVE)

**The problem:** Full PVT sweep shows 6/15 FAIL:
- SS 27C: onset=6.465V (> 6.2V max) — leakage OK
- FF 27C: leakage=2588nA (> 1000nA max) — onset OK
- SF 27C: leakage=6723nA (>> 1000nA max) — onset borderline
- FF 150C: onset=4.855V (< 5.0V min)
- SF 150C: onset=4.690V (< 5.0V min)
- FS 27C: onset=6.605V (> 6.2V max) — leakage OK

The previous "fix" was to call this a "fundamental limitation" and recommend
trimming. That is giving up, not engineering. The topology may have limitations,
but you should still try to improve corner coverage.

**Root cause analysis:**
- SS/FS fail HIGH onset: NMOS Vth is high → each diode drops more → onset rises
- FF/SF fail LOW onset + HIGH leakage: NMOS Vth is low → diodes conduct at lower V

**What to try:**
1. **Center the design.** The current TT onset is 6.075V, biased toward the upper
   end of the 5.5-6.2V window. If you can center it at ~5.85V (midpoint), you
   gain 190mV of headroom on the high side, which might bring SS and FS into spec.
   To lower onset: increase W slightly (e.g., W=2u instead of 1.5u) and increase
   Rpd to compensate leakage.
2. **Try a PMOS+NMOS hybrid stack** where some devices are PMOS and some NMOS.
   PMOS Vth shifts in the OPPOSITE direction from NMOS in SF/FS corners (that's
   what SF/FS means — one is slow, the other fast). A mixed stack could cancel
   the skew-corner shift. This is a topology change worth exploring.
3. **Add a body-bias trim** to fine-tune Vth post-fab (if body=source allows
   a small offset voltage).

**Pass criterion:** Improve from 9/15 to at least 12/15 PVT pass. 15/15 is the
stretch goal. At minimum, get FF/SF 27C leakage under control.

**IMPORTANT: do NOT "solve" this by saying trimming is needed. Try to fix it.**

---

## PROBLEM C: Clamp Impedance at Onset is 107 ohm (SHOULD FIX)

**The problem:** The spec table in program.md says "Clamp impedance above threshold:
max 50 ohm." At the onset (1mA), the measured dynamic impedance is 107 ohm.
It drops to 16 ohm at 10mA and 2.4 ohm at 7V. So the clamp is "soft" at onset
and only becomes sharp at higher currents.

**Root cause:** The diode stack is the impedance bottleneck. At onset current,
the stack devices are in subthreshold/moderate inversion with low gm. The clamp
NMOS has high gm but its gate drive is limited by the stack.

**What to try:**
1. **Wider diode stack devices** give lower impedance per device (higher gm at
   same current). But wider = more leakage. Trade-off.
2. **Add a feedback path** where the clamp NMOS drain current bootstraps the
   gate drive higher. E.g., a current mirror from the clamp current that injects
   additional current into the vg node.
3. **Accept and document** if the impedance spec is met at 10mA but not at 1mA.
   The 1mA onset point is where the clamp barely turns on — high impedance there
   is physically inevitable for a passive clamp.

**Pass criterion:** Z < 50 ohm at 5mA or better. Document the Z vs I curve.

---

## PROBLEM D: Cff Causes 1A Startup Surge (SHOULD FIX)

**The problem:** During a fast power-up (0 to 5V in 1us), Cff=20pF couples the
entire ramp to the clamp gate. The clamp draws **1.0A peak** and holds PVDD at
4.7V instead of 5.0V. It settles in ~12us (Rpd*Cff time constant).

During a slow startup (100us): only 67uA peak — OK.

**Root cause:** Cff has no directionality. It couples ALL dV/dt to the gate,
including the desired startup ramp. The Rpd discharge time constant (500k * 20p
= 10us) is too slow to bleed the charge before the clamp activates.

**What to try:**
1. **Add a diode in series with Cff** — a diode-connected NFET from Cff to vg.
   This makes Cff only couple POSITIVE dV/dt (overshoot) but blocks the DC
   bias from holding vg high during startup. After the transient, the diode
   cuts off and vg settles via Rpd.
2. **Reduce Cff and increase clamp W instead.** Less Cff means less startup
   coupling but also less transient response. Compensate by making the clamp
   NMOS even wider so it needs less gate drive.
3. **Add an RC delay on Cff** — a small series resistor (1-10k) that limits the
   Cff charging rate and allows Rpd to compete during startup.

**Pass criterion:** During 0→5V startup in 1us, clamp surge current < 10mA,
PVDD reaches 5.0V within 20us. Normal transient clamping still works.

---

## RULES

1. **Do NOT "resolve" a problem by documenting it.** Change the circuit.
2. Keep 9/9 TT specs passing at all times. Never regress.
3. For each circuit change: commit, run, extract metrics, keep or discard.
4. The evaluator is `python3 evaluate.py` reading from `run.log`. Do not modify it.
5. Test transient with BOTH Rsrc=10 and Rsrc=5. Report both.
6. Run `python3 run_pvt_sweep.py` after any design change to check corners.
7. Test startup: 0→5V in 1us through 1 ohm into 200pF. Report peak clamp current.
8. All devices must be real Sky130 PDK. No ideal Zener or behavioral sources.
9. Update this file after each problem is addressed with SIMULATION DATA.

## EXPERIMENT LOOP

```
1. Pick one problem (A, B, C, or D)
2. Form a hypothesis for a circuit change
3. Modify design.cir
4. git commit -m "exp(07): <what you changed>"
5. Run: bash run_block.sh > run.log 2>&1
6. Check: python3 evaluate.py (must stay 9/9)
7. Test transient at Rsrc=5: run custom testbench
8. Run PVT: python3 run_pvt_sweep.py
9. Test startup: run custom testbench
10. If improved AND 9/9 still passes → KEEP
11. If 9/9 regressed → git checkout design.cir (DISCARD)
12. Log results below
13. Go to step 1. NEVER STOP until all 4 problems are improved.
```

---

## Experiment Log

| # | Change | 9/9 TT? | Trans Rsrc=5 | PVT pass | Startup surge | Status |
|---|--------|---------|-------------|----------|---------------|--------|
| v9 (baseline) | W=1.5u L=4u Rpd=500k Cff=20p | 9/9 | 6.70V FAIL | 9/15 | 1.0A FAIL | current |

---

## Current Design (v9 baseline)

```
Diode stack: 5x nfet_g5v0d10v5 W=1.5u L=4u (body=source, requires DNW)
Pulldown:    Rpd = 500k
Feedforward: Cff = 20 pF
Clamp NMOS:  nfet_g5v0d10v5 W=100u L=0.5u m=20 (body=GND, total 2000um)
```
