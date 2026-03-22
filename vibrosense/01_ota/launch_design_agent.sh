#!/bin/bash
# Launch Claude Code OTA design agent with logging
# Logs to: /home/ubuntu/analog-ai-chips/vibrosense/01_ota/agent.log

cd /home/ubuntu/analog-ai-chips/vibrosense/01_ota

LOG="/home/ubuntu/analog-ai-chips/vibrosense/01_ota/agent.log"
echo "=== OTA Design Agent started at $(date) ===" > "$LOG"

PROMPT='You are an analog IC design engineer. Your mission is to design the folded-cascode OTA defined in program.md for the VibroSense project using the SkyWater SKY130A PDK.

## CRITICAL RULES
- NEVER modify program.md, specs.json, or requirements.md
- The SKY130 PDK lib path is: /home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/ngspice/sky130.lib.spice
- ngspice 42 is installed at /usr/bin/ngspice
- Python 3 with matplotlib and numpy are available
- You MUST commit all work with git (git add -A && git commit -m "design: <description>" && git push)
- Today is 2026-03-22

## YOUR MISSION - DO NOT STOP UNTIL COMPLETE

Follow this exact sequence. Be honest in your analysis - if specs fail, iterate the design.

### Phase 1: SPICE Subcircuit
1. Read program.md thoroughly (all sections, especially Section 3 topology and sizing)
2. Create ota_foldcasc.spice - the subcircuit netlist with all 13 transistors per Section 3.3-3.4
3. Use .param statements for all device sizes so the design is parameterizable (Section 10.3)

### Phase 2: Operating Point Verification (MOST IMPORTANT - Section 7)
4. Create tb_ota_op.spice per Section 6.7
5. Run it and extract Vgs, Vth, Vds, Vdsat, Id, gm, gds, region for ALL 13 transistors
6. Verify EVERY check in Section 7.1:
   - ALL PMOS: Vsg - |Vth| > 150mV (sky130 PMOS unreliable below this)
   - Signal NMOS (M1,M2,M7,M8): Vgs - Vth > 50mV
   - All cascodes: Vds > Vdsat + 50mV
   - Tail current: |Id_M11 - 500nA| < 50nA
   - Current balance: |Id_M1 - Id_M2| < 10nA
   - Output: 0.6V < Vout < 1.2V
7. If ANY check fails, resize transistors and re-simulate. DO NOT proceed until clean.
8. Produce the operating point table per Section 7.3 format

### Phase 3: AC Analysis
9. Create tb_ota_ac.spice per Section 6.1 (open-loop with AC stimulus)
10. Run and measure DC gain, UGB, phase margin, gain margin
11. Targets: gain >= 65dB, UGB 30-150kHz, PM >= 60deg, GM >= 10dB
12. If specs fail, iterate sizing per Section 9 troubleshooting

### Phase 4: All Other Testbenches
13. Create and run tb_ota_dc.spice (Section 6.2) - output swing >= 1.0 Vpp
14. Create and run tb_ota_tran.spice (Section 6.3) - slew rate >= 10 mV/us
15. Create and run tb_ota_noise.spice (Section 6.4) - noise <= 200 nV/rtHz @ 1kHz
16. Create and run tb_ota_psrr.spice (Section 6.5) - PSRR >= 50dB @ 1kHz
17. Create and run tb_ota_cmrr.spice (Section 6.6) - CMRR >= 60dB at DC

### Phase 5: Corner and Monte Carlo
18. Create and run tb_ota_corners.spice (Section 6.8) - all specs across TT/SS/FF/SF/FS
19. Create and run temperature sweep (Section 6.9) - -40C/27C/85C
20. Create and run tb_ota_mc.spice (Section 6.10) - 200 runs, offset 3-sigma < 10mV

### Phase 6: Analysis and Plots
21. Create Python scripts to generate publication-quality plots:
    - Bode plot (magnitude and phase)
    - Noise spectral density
    - DC transfer characteristic and output swing
    - Step response (transient)
    - Corner comparison plots
    - Monte Carlo offset histogram
22. Save all plots as PNG files

### Phase 7: Results Documentation
23. Create results.md with ALL specs, measured values, PASS/FAIL for every parameter
24. Include the full operating point table
25. Include corner and temperature results
26. Include Monte Carlo statistics

### Phase 8: Design Optimization (if needed)
- If you find that specs are marginal or failing, you MAY create an optimizer script
- The optimizer should sweep W/L parameters systematically to find the best sizing
- Always re-verify operating points after any sizing change

### ITERATION PROTOCOL
- After each simulation, honestly assess: does it meet spec?
- If not, diagnose using Section 9 troubleshooting guide
- Resize, re-simulate, repeat
- NEVER declare success if any spec fails
- Commit progress regularly with descriptive messages

### GIT PROTOCOL
- Commit after each major milestone (subcircuit done, OP verified, each testbench passing, etc.)
- Use message format: "design: <what was accomplished>"
- Push after each commit

NEVER STOP until ALL specs in Section 5 pass across all corners and temperatures. Be honest. Do great work.'

exec claude --dangerously-skip-permissions --verbose --output-format stream-json -p "$PROMPT" 2>&1 | tee -a "$LOG"
