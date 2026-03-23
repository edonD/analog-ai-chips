#!/bin/bash
cd /home/ubuntu/analog-ai-chips/vibrosense/01_ota
LOG="agent.log"
echo "=== OTA Design Agent v3 started at $(date) ===" > "$LOG"

PROMPT='You are an analog IC design engineer completing the VibroSense folded-cascode OTA design in SKY130A.

TODAY IS 2026-03-23.

## ENVIRONMENT
- SKY130 PDK: /home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/ngspice/sky130.lib.spice
- ngspice 42: /usr/bin/ngspice
- Python 3 with matplotlib/numpy
- Working dir: /home/ubuntu/analog-ai-chips/vibrosense/01_ota

## CURRENT STATE — GATES 1 AND 2 ALREADY PASS
The previous run achieved:
- Gate 1 (OP): ALL 13 transistors verified, all in saturation, all Vov specs met
- Gate 2 (AC): DC gain=63.5dB, UGB=32.8kHz, PM=90deg — all pass
- Gate 3 (DC/Tran): DC swing=1.009Vpp PASSES, but slew rate was stuck at 6.87 mV/us

The existing files are solid: ota_foldcasc.spice, tb_ota_op.spice, tb_ota_ac.spice, tb_ota_dc.spice, tb_ota_tran.spice, sky130_minimal.lib.spice, models/

## WHAT CHANGED: THE VERIFIER IS UPDATED (v2)

verify_design.py has been updated with:
1. **Fixed slew rate measurement**: Now accepts multiple measurement methods:
   - "sr_meas": direct derivative measurement (preferred — output from testbench in V/s)
   - "t_low"/"t_high": two voltage crossings during slewing phase
   - "t10"/"t90": 10-90% (fallback, but use a LARGE step like 500mV)

   The KEY FIX: use a 500mV step (e.g., 0.5V to 1.0V) so the OTA actually slews
   (current-limited), not just settles (bandwidth-limited). The theoretical SR is
   Itail/CL = 548nA/10pF = 55 mV/us. A proper large-signal testbench will measure this.

2. **Gate 4 (Noise/Rejection)**: NEW — checks tb_ota_noise.spice, tb_ota_psrr.spice, tb_ota_cmrr.spice
   - Expects "noise_1k" and "noise_10k" measurements (input-referred, V/rtHz)
   - Expects "psrr_1k" measurement (dB)
   - Expects "cmrr_dc" measurement (dB)

3. **Gate 5 (Corners/Temperature)**: NEW — checks tb_corner_XX.spice and tb_temp_XX.spice
   - Expects individual files: tb_corner_tt.spice, tb_corner_ss.spice, etc.
   - Expects "gain_peak" or "gain_db" and "ugb" measurements
   - Has SANITY CHECK: if gain varies < 2dB across corners, measurement is broken

## IMMUTABLE FILES — DO NOT MODIFY
- program.md, specs.json, requirements.md, verify_design.py

## YOUR MISSION: PASS ALL 5 GATES

### Step 1: Fix tb_ota_tran.spice for proper slew rate measurement
The transient testbench must:
- Apply a LARGE step (500mV, e.g., Vinp from 0.5V to 1.0V) to force current-limited slewing
- The OTA is in unity-gain feedback
- Measure the slew rate using one of these methods:
  a) PREFERRED: Use ngspice DERIV to measure dV/dt at the steepest point, output as "sr_meas" in V/s
  b) ALTERNATIVE: Measure time between two voltage crossings during slew phase, output "t_low", "t_high", "v_low", "v_high"
  c) FALLBACK: 10-90% method with "t10", "t90" — but only works if step is large enough to cause slewing

Run verify_design.py after fixing. Gate 3 should now pass.

### Step 2: Create tb_ota_noise.spice (Gate 4)
Per program.md Section 6.4:
- Use .noise analysis from 1Hz to 1MHz
- Output input-referred noise spectral density
- Testbench must output measurements named "noise_1k" and "noise_10k" (in V/rtHz)
- Specs: noise_1k <= 200 nV/rtHz, noise_10k <= 100 nV/rtHz

### Step 3: Create tb_ota_psrr.spice (Gate 4)
Per program.md Section 6.5:
- Apply AC stimulus on VDD, measure output
- PSRR = differential_gain_dB - vdd_to_output_gain_dB
- Testbench must output measurement named "psrr_1k" (in dB)
- Spec: >= 50 dB at 1kHz

### Step 4: Create tb_ota_cmrr.spice (Gate 4)
Per program.md Section 6.6:
- Tie both inputs together, apply AC stimulus
- CMRR = differential_gain_dB - common_mode_gain_dB
- IMPORTANT: the OTA needs DC feedback to set the output point! Use inductor or resistor.
  Do NOT leave the output floating (it will rail and invalidate the measurement).
- Testbench must output measurement named "cmrr_dc" (in dB)
- Spec: >= 60 dB at DC

### Step 5: Create corner testbenches (Gate 5)
Create tb_corner_tt.spice, tb_corner_ss.spice, tb_corner_ff.spice, tb_corner_sf.spice, tb_corner_fs.spice
Each is essentially tb_ota_ac.spice but with the .lib line changed to the appropriate corner.
Each must output "gain_peak" (or "gain_db") and "ugb" measurements.
Spec: gain >= 60 dB in ALL corners. Results MUST vary across corners.

### Step 6: Create temperature testbenches (Gate 5)
Create tb_temp_-40.spice, tb_temp_27.spice, tb_temp_85.spice
Same as tb_ota_ac.spice but with .temp set appropriately.
Each must output "gain_peak" (or "gain_db") and "ugb" measurements.
Spec: gain >= 55 dB, UGB in 20-200 kHz at all temperatures.

### Step 7: Run verify_design.py and iterate
After creating all testbenches, run the verifier. Fix any failures. Iterate.

### Step 8: Results and plots
Only after ALL 5 gates pass. Write results.md with ONLY verifier-confirmed numbers.
Generate plots from simulation data files (NOT hardcoded numbers).

## HONESTY PROTOCOL (same as before)
- verify_design.py is the ONLY source of truth
- If stuck after 15 attempts at same gate, write STUCK_REPORT.md
- Honest failure >> fake success
- No hardcoded data in plots or results
- No junk files — use exact filenames from requirements.md

## GIT PROTOCOL
- Commit after each gate passes: "design: gate N passed — <details>"
- Push after each commit

## CRITICAL: NEVER GIVE UP
- If a gate fails, diagnose WHY using the verifier output
- Try at least 15 different approaches before declaring stuck
- Read program.md Section 9 for troubleshooting every failure mode
- You have a solid foundation — Gates 1 and 2 already pass
- The slew rate fix is straightforward — just use a bigger step
- KEEP GOING until all 5 gates pass or you have genuinely exhausted all options'

exec claude --dangerously-skip-permissions --verbose --output-format stream-json -p "$PROMPT" 2>&1 | tee -a "$LOG"
