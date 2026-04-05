# CAD Expert Review #2: Testbench Quality

**Reviewer:** CAD Expert 2 (Testbench Quality)
**Date:** 2026-04-05

---

## Stimulus Quality (`scripts/generate_stimuli.py`)

### Positive
- Bearing fault physics is correctly modeled: BPFI=162.2 Hz, BPFO=107.4 Hz, BSF=70.6 Hz
  match real 6205-2RS bearing at 1797 RPM.
- Fault signals use impulse trains convolved with decaying resonance -- physically realistic.
- Inner race has shaft-frequency AM (correct: inner race rotates with shaft).
- Outer race has no AM (correct: outer race is stationary in housing).
- Ball fault uses 2x BSF (correct: ball contacts both races per revolution).
- 12 kHz sample rate matches CWRU dataset standard.

### Issues
1. **Fixed random seed (42).** All training stimuli use the same noise realization.
   Classifier could be fitting to this specific noise pattern.
   **Impact: Medium** -- variant stimuli use different seeds (100-303), which tests this.

2. **Simplistic resonance model.** Real bearings have multiple resonance modes at
   different frequencies. The stimuli use a single resonance per fault type (3 kHz
   for inner race, 2.5 kHz for outer, 3.5 kHz for ball). This means the BPF channels
   see very specific spectral patterns rather than broadband fault energy.
   **Impact: Medium** -- classifier may rely on the specific resonance frequency
   rather than the general spectral envelope shape.

3. **No sensor noise model.** Real MEMS accelerometers have Johnson noise, 1/f noise,
   and quantization noise. PWL stimuli are noiseless (signal-only plus filtered white noise).
   **Impact: Low** -- the BPF bank provides inherent noise filtering.

4. **V_SCALE=0.1 V/g.** This means the input signal amplitude is ~0.1V peak for
   normal and up to ~0.3V for fault conditions. At 4x PGA gain, fault signals reach
   ~1.2V swing. This is within the 1.8V supply but leaves limited headroom.
   **Impact: Low** -- adequate for proof-of-concept.

## Simulation Parameters

### `.tran 10u 200m UIC`
- **Step size (10 us):** At 6 kHz max signal frequency, Nyquist requires <83 us.
  10 us gives 100 kHz effective sampling -- adequate with 10x margin.
- **Duration (200 ms):** Allows 5+ BPF settling time constants and ~30 shaft rotations.
  Adequate for steady-state analysis.
- **UIC:** Correct -- initial conditions set `v(venv*)=0.9` to skip envelope settling.
  Without this, envelope LPF would need ~100ms to charge to VCM.

### `.option` Settings
- `method=gear`: Good for circuits with large capacitors (Gear is better than trap for
  stiff circuits with diodes/switches).
- `reltol=1e-3`: Standard. Could be tighter (1e-4) for precision but would slow sim.
- `abstol=1e-12, vntol=1e-6`: Standard.
- `gmin=1e-12`: Standard.
- `itl1=500, itl2=200, itl4=100`: Generous iteration limits. Good for convergence.

### Issues
1. **No `.option RSHUNT`.** For circuits with very high impedance nodes (10G pseudo-resistors
   in PGA), adding `RSHUNT=1e12` can help convergence without affecting accuracy.
   **Impact: Low** -- sims converge without it.

2. **No `.savetime` or `.tran` maxstep.** ngspice auto-selects timestep. This means
   the sim may take very small steps during transients (e.g., when impulses arrive),
   explaining the 45-72 minute runtimes.
   **Impact: Medium** -- adding `.tran 10u 200m 0 50u UIC` (max step 50us) could
   speed up sims significantly.

## Analysis Methodology (`scripts/analyze_peak_results.py`)

### Positive
- Uses last 50ms (or last 25%) for steady-state analysis -- correct.
- Majority vote at 1ms intervals over the analysis window -- reasonable.
- Extracts mean, median, min, max, std for all features.
- Power measurement via current through sense resistors -- correct methodology.
- Class boundaries at 0.225V, 0.675V, 1.125V (midpoints between 0, 0.45, 0.9, 1.35V).

### Issues
1. **Power sign convention issue.** Results JSON shows negative power values
   (e.g., `v_vdd_bpf1: -4.60 uW`). The code uses `-np.mean(current)` but some
   blocks may have different current direction conventions.
   **Impact: Low** -- the total matches expected values.

2. **No confidence interval.** Analysis reports point estimates without uncertainty.
   With signal fluctuation (e.g., ENV4 std = 5 mV on a 95 mV spread), a confidence
   interval would better characterize reliability.
   **Impact: Low** -- not needed for proof-of-concept.

---

## Verdict: GOOD with minor improvements possible

The testbench is well-designed for a proof-of-concept. Stimulus generation is
physically grounded in real bearing fault mechanics. Simulation parameters are
appropriate. Analysis methodology is sound. The main risk is overfit to fixed
stimuli, which the variant test plan addresses.
