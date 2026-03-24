# Block 06: Charge-Domain MAC Classifier — Design Program

**YOU MUST NEVER GIVE UP.** If one approach fails, try another. If SPICE won't converge, debug it. If a topology doesn't work, redesign from scratch. If caps don't match, try a different sizing. If the comparator has too much offset, try a different architecture. THERE IS ALWAYS ANOTHER WAY. Try 10 approaches if you have to. Try 50. Document every failed attempt — failures teach us what doesn't work.

**ANYTHING GOES** as long as it makes physical sense and simulates correctly in ngspice with SKY130 models. You are free to change the architecture, topology, sizing, number of bits, capacitor values — EVERYTHING. The only constraints are: (1) it must classify vibration patterns, (2) it must use real SKY130 transistors/caps, (3) it must simulate in ngspice, (4) it must be honest.

---

## WHAT EXISTS NOW (your starting point)

You have a working 4-input × 2-bit MAC unit with:
- Transmission-gate switches (W=0.84u/0.15u NMOS, W=1.68u/0.15u PMOS)
- Ideal 50 fF / 100 fF capacitors (NOT real MIM caps yet)
- StrongARM comparator (10 transistors)
- MAC linearity verified: 0.85% error
- Corner variation: ±0.5%
- Charge injection: 0.092 LSB

This is a proof-of-concept. You need to turn it into a tapeout-ready design.

---

## WHAT MUST BE DONE — IN ORDER OF PRIORITY

### PRIORITY 1: Scale to Full Size (8 inputs × 4-bit weights)

The current 4×2-bit MAC is a toy. The real system needs 8 inputs × 4-bit weights × 4 output classes.

- Build `mac_8in4b.spice` — full 8-input, 4-bit MAC unit
- Binary-weighted caps: Cunit, 2×Cunit, 4×Cunit, 8×Cunit
- Choose Cunit carefully — bigger = better matching but more area and energy
- You MUST simulate the full-scale version. Do NOT just claim "it scales linearly"
- Verify linearity, charge injection, and settling at full scale
- The bitline parasitic will be MUCH larger with 32 caps hanging off it — measure it

**If the full 8×4-bit is too big or too slow or has too much charge injection — REDESIGN.** Consider:
- Segmented bitlines (split into two halves, sum with a charge amplifier)
- Pipelined MAC (process 4 inputs at a time, accumulate)
- Current-mode summing instead of charge sharing
- Reduce to 3-bit weights if 4-bit matching is impossible
- ANYTHING that works. Be creative.

### PRIORITY 2: Real MIM Capacitor Models

Stop using ideal caps. Use `sky130_fd_pr__cap_mim_m3_1` or model the real MIM cap behavior:
- Bottom plate parasitic (~10% of cap value)
- Voltage coefficient (~50 ppm/V)
- If the PDK cap model isn't available in your library, at minimum add bottom-plate parasitic caps to model the real behavior

Simulate with realistic cap models and report the difference from ideal.

### PRIORITY 3: Full Winner-Take-All Circuit

Build the complete WTA:
- 4 MAC units (one per class: Normal, Imbalance, Bearing, Looseness)
- 3 StrongARM comparators in tree configuration, OR 6 comparators for full round-robin
- Priority encoder to produce 2-bit class output
- Simulate with realistic class separation (expect 20-100 mV between classes)

Test cases:
- Clear winner (one class 100 mV above others) — must always work
- Close race (two classes within 10 mV) — document what happens
- All classes equal — document the default behavior

### PRIORITY 4: Monte Carlo Mismatch Analysis

This is what kills real chips. You MUST do this:
- Cap mismatch: σ(ΔC/C) = 1% / √(C/fF) typical for MIM caps
- Add Gaussian random variation to every cap in the MAC
- Run 100+ Monte Carlo iterations
- Measure: MAC output σ, effective weight precision, classification accuracy
- Comparator offset MC: add threshold voltage mismatch to StrongARM input pair
  - σ(Vth) ≈ 5 mV for W=4u L=0.5u on SKY130

If Python-based MC is easier than ngspice MC, DO IT IN PYTHON but with physically realistic mismatch models. The numbers must be grounded in real Pelgrom coefficients.

**If mismatch kills accuracy — REDESIGN:**
- Bigger caps (better matching but more area/energy)
- Chopping/autozeroing for comparator offset
- Calibration scheme (trim caps digitally)
- Redundant MAC + averaging

### PRIORITY 5: Non-Overlapping Clock Generator

Design the actual clock generation circuit:
- Input: single master clock
- Outputs: phi_sample, phi_eval, phi_reset (non-overlapping)
- Non-overlap time > 5 ns (to prevent charge sharing between phases)
- Use standard NAND-gate based non-overlapping clock generator
- Simulate and verify no overlap in all corners

### PRIORITY 6: Weight Loading Interface

Design how weights get from SPI to the MAC:
- 32 bits per MAC unit × 4 MAC units = 128 bits total
- Latch/register to hold weight bits
- Level shifter if needed (digital 1.8V to analog switch control)
- This can be a simple shift register + parallel load

### PRIORITY 7: Power Analysis — REAL, NOT ESTIMATED

- Measure actual switching energy from SPICE transient (integrate Idd × Vdd over one classification cycle)
- Measure leakage current in idle state
- Calculate average power at 10 Hz classification rate
- Include clock generator power, weight register leakage, everything

### PRIORITY 8: Noise Analysis

- Thermal noise from switch resistance (kT/C noise on each cap)
- Clock feedthrough noise
- Supply noise rejection
- Run `.noise` if possible, or calculate analytically with SPICE-verified parameters

### PRIORITY 9: Full Classification Test

- Load CWRU-trained weights (or synthetic weights that separate 4 classes)
- Apply 100+ test vectors representing all 4 classes
- Measure classification accuracy in SPICE
- Compare to Python golden model
- Report confusion matrix

### PRIORITY 10: Temperature and Supply Variation

- Simulate at -40°C, 27°C, 85°C
- Simulate at Vdd = 1.6V, 1.8V, 2.0V
- Report MAC accuracy and WTA resolution at all conditions
- If it fails at any condition — FIX IT

---

## DESIGN FREEDOM — USE IT

You are NOT locked into the current architecture. If at any point the charge-domain MAC approach hits a wall, you may:

1. **Switch to current-mode MAC** — use current mirrors with binary-weighted W/L ratios as weights. Dot product becomes current summation on a wire. Simpler but has static power.

2. **Switch to switched-capacitor MAC** — use an op-amp integrator. More complex but better noise performance.

3. **Switch to time-domain classifier** — convert features to pulse widths, AND them with weight pulses, count overlapping time. Fully digital-compatible.

4. **Hybrid approach** — charge-domain MAC for computation + current-mode comparator for WTA.

5. **Simplify the problem** — if 4-bit weights are too hard to match, use 3-bit or even 2-bit. If 8 inputs create too much parasitic, reduce to 5 (just the BPF envelopes, drop RMS/crest/kurtosis). A simpler design that actually works beats a complex design that doesn't.

6. **Add redundancy** — use 2× or 4× the caps and average. Trade area for matching.

**The only rule: it must make physical sense and simulate correctly.**

---

## README.md — THIS IS YOUR DELIVERABLE

Every time you make progress, update README.md and commit. The README must contain:

1. **Architecture diagram** — ASCII art showing the full classifier
2. **Every transistor** — W/L, type, function, operating region
3. **Every capacitor** — value, type (ideal/MIM), what it does
4. **Every simulation result** — exact numbers from ngspice, not estimates
5. **Every plot** — embedded as PNG images in the plots/ directory
6. **Honest assessment** — what works, what doesn't, what's risky
7. **Failed approaches** — what you tried that didn't work and why
8. **PASS/FAIL table** — against the specs from the main program.md
9. **Next steps** — what remains to be done

**I read ONLY the README in the morning.** If it's not in the README, it doesn't exist.

---

## GIT WORKFLOW

```bash
# Set remote with token
git remote set-url origin https://<TOKEN>@github.com/edonD/analog-ai-chips.git

# Commit after every meaningful step
git add -A && git commit -m "design(classifier): <what you did>" && git push
```

Commit OFTEN. Every testbench that passes, every new subcircuit, every plot — commit it. If I wake up and there's only 1 commit, you didn't work hard enough.

---

## REFERENCE

Check this for README quality and detail level:
https://github.com/edonD/analog-ai-chips/blob/master/vibrosense/00_bias/README.md

---

## REMEMBER

- **NEVER GIVE UP.** A failed simulation is information, not a dead end.
- **NEVER fake results.** If ngspice says FAIL, report FAIL and fix it.
- **NEVER stop at "good enough."** Push until you hit a real physical limit.
- **ANYTHING GOES** as long as it's physically real and simulates.
- **Parametrise everything** — build optimizers if it helps.
- **The README is everything.** Make it detailed, honest, and complete.
- **THERE IS ALWAYS ANOTHER WAY.**
