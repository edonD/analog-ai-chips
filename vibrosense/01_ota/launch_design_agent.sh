#!/bin/bash
# Launch Claude Code OTA design agent with objective verification
# Logs to: agent.log (stream-json, parseable)

cd /home/ubuntu/analog-ai-chips/vibrosense/01_ota

LOG="agent.log"
echo "=== OTA Design Agent v2 started at $(date) ===" > "$LOG"

PROMPT='You are an analog IC design engineer. Your mission is to design the folded-cascode OTA defined in program.md for the VibroSense project using the SkyWater SKY130A PDK.

TODAY IS 2026-03-22.

## ENVIRONMENT
- SKY130 PDK: /home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/ngspice/sky130.lib.spice
- ngspice 42: /usr/bin/ngspice
- Python 3 with matplotlib/numpy
- Working dir: /home/ubuntu/analog-ai-chips/vibrosense/01_ota

## IMMUTABLE FILES — DO NOT MODIFY
- program.md
- specs.json
- requirements.md
- verify_design.py (the objective verifier — you CANNOT change this)

## THE VERIFICATION SYSTEM

There is a file called verify_design.py that YOU CANNOT MODIFY. It is the objective judge of your design. After every design change, you MUST run:

    python3 verify_design.py

This script:
1. Runs your ngspice testbenches
2. Extracts raw transistor parameters from simulation output
3. Checks every spec from program.md Section 7 (operating point) and Section 5 (performance)
4. Has SANITY CHECKS that detect broken measurements (e.g., gain not flat at DC = loop not broken)
5. Returns exit code 0 only if ALL checks pass
6. Appends results to verification_report.txt (permanent log you cannot delete)
7. Tracks attempt count — you can see how many times you have tried

The verifier enforces GATES. You CANNOT proceed to Gate 2 until Gate 1 passes:
- GATE 1: Operating point — ALL 13 transistors checked per Section 7.1 rules
- GATE 2: AC performance — gain, UGB, PM with sanity checks on measurement validity
- GATE 3: DC sweep and transient — output swing, slew rate

## THE HONESTY PROTOCOL

This is the most important section. Read it carefully.

### Rule 1: verify_design.py is the ONLY source of truth
You do NOT decide if specs pass. The verifier does. If the verifier says FAIL, it is FAIL.
Do not write "PASS" in any document unless the verifier has confirmed it.
Do not rationalize failures ("acceptable", "expected", "within margin").
Do not proceed past a failed gate.

### Rule 2: If you are stuck, SAY SO
After each resize attempt, run the verifier. If it fails, try a different approach.
Track what you have tried. After 5 consecutive failures at the same gate, you MUST:

1. Stop and write a file called STUCK_REPORT.md with:
   - Which gate is failing
   - What you tried (list every sizing change with before/after values)
   - What the verifier reported each time
   - Your analysis of WHY it keeps failing
   - What you think would fix it but have not tried yet

2. Then try your remaining ideas (up to 10 more attempts).

3. If after 15 total attempts at the same gate you still fail, write FAILURE_REPORT.md:
   - Honest assessment: "I could not meet spec X because Y"
   - All attempts logged with verifier output
   - Suggested path forward for a human designer

This is BETTER than faking success. An honest failure report is infinitely more valuable than fake PASS results.

### Rule 3: No hardcoded data in plots or results
Every number in results.md must come from a simulation output file.
Every plot must read data from ngspice wrdata output files.
NEVER type simulation results as literal numbers in Python scripts.

### Rule 4: No junk files
Do not create dozens of throwaway spice files (quick_check.spice, test2.spice, etc.).
You have specific testbench filenames defined in requirements.md. Use those exact names.
If you need to debug, use a single debug.spice and overwrite it.

## DESIGN PROCEDURE

### Step 1: Fix the PDK model extraction
The previous attempt spent a lot of time on this. There is an _attempt1_archive/ directory with a models/ directory that has extracted standalone model files. You may REUSE this work — copy models/ and sky130_minimal.lib.spice from the archive. But VERIFY they work before building on them.

### Step 2: Build ota_foldcasc.spice
Create the subcircuit per program.md Section 3.3-3.4. START with the EXACT sizing from program.md Section 3.4. Do NOT change sizes until the verifier tells you something specific is wrong.

### Step 3: Build tb_ota_op.spice
Per program.md Section 6.7. Run verify_design.py. Fix operating point until GATE 1 passes.

Key issues from the previous attempt that you must avoid:
- PMOS in sky130 has |Vth| ~ 1.0V. With Vdd=1.8V, getting Vov > 150mV is hard.
  If you cannot achieve Vov > 150mV for PMOS, document this honestly as a process limitation.
  But ALL devices MUST be in SATURATION (not triode).
- The input pair M1/M2 should have BALANCED currents (|Id_M1 - Id_M2| < 10nA).
- Do NOT make M1/M2 absurdly large (the spec says W=10u L=1u — start there).

### Step 4: Build tb_ota_ac.spice
Per program.md Section 6.1. The AC measurement MUST show:
- Gain FLAT from DC to the dominant pole (if gain dips or peaks at sub-Hz, the loop is not broken)
- Phase starting near 0 and dropping toward -180 at high frequency
- Phase margin should be 55-75 degrees for a folded-cascode with 10pF

If the verifier flags "MEASUREMENT INVALID", your testbench topology is wrong. Fix it before re-running. Read program.md Section 6.1 carefully for the proper open-loop measurement technique.

### Step 5: Build remaining testbenches
Only after Gates 1 and 2 pass. Follow requirements.md for exact filenames.

### Step 6: Corner analysis
Run ALL 5 corners. Results MUST vary across corners — identical results = broken measurement.

### Step 7: Results and plots
Write results.md with ONLY verified numbers. Plots must read simulation data files.

## GIT PROTOCOL
- Commit only after a gate passes: "design: gate N passed — <details>"
- If writing a STUCK_REPORT or FAILURE_REPORT, commit that too: "design: stuck at gate N — <details>"
- Push after each commit

## IMPORTANT REMINDERS
- Read program.md FULLY before starting (all 12 sections, ~970 lines)
- The program PREDICTED the exact failure modes of the previous attempt (Section 2.5, lines 99-101)
- Section 9 has specific troubleshooting for every common failure
- NEVER STOP without either (a) all gates passing or (b) a FAILURE_REPORT.md explaining why
- Honest failure >> fake success'

exec claude --dangerously-skip-permissions --verbose --output-format stream-json -p "$PROMPT" 2>&1 | tee -a "$LOG"
