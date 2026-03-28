#!/usr/bin/env bash
# This script launches a second Claude agent to finalize the block
# after the optimization loop agent finishes.

cd /home/ubuntu/analog-ai-chips/pvdd_regulator/00_error_amp

claude --dangerously-skip-permissions -p "You are in /home/ubuntu/analog-ai-chips/pvdd_regulator/00_error_amp/ on branch autoresearch/error-amp-mar27. The error amplifier optimization loop has completed. You must now finalize this block. Do ALL of the following:

1. READ the current state: read design.cir, run.log, results.tsv, and program.md to understand the final design and results.

2. UPDATE README.md: Create a comprehensive README.md for this block with:
   - Block title and purpose
   - Topology description (two-stage Miller OTA)
   - Complete device table (every transistor with W/L/multiplier/type)
   - Operating point summary (all node voltages, branch currents)
   - Full specification results table (parameter | simulated | spec | pass/fail)
   - All plots embedded inline (bode_gain_phase.png, output_swing.png, noise_spectral.png, psrr_vs_freq.png, pvt_gain.png, pvt_pm.png)
   - Run plot_all.py if it exists, or create it to generate all required plots from .dat files

3. CREATE AN XSCHEM SCHEMATIC — THIS IS CRITICAL AND MUST BE DONE WITH EXTREME CARE:
   - Create error_amp.sch in xschem format
   - The schematic must be VERY well organized:
     * Clear left-to-right signal flow: inputs (vref, vfb) on the LEFT, output (vout_gate) on the RIGHT
     * Power supplies (pvdd) at TOP, ground (gnd) at BOTTOM
     * Input differential pair grouped together in the center-left
     * Current mirrors grouped logically
     * Output/second stage on the right
     * Compensation network clearly visible
     * Every node must have a proper net label
     * Use wire connections, not overlapping symbols
     * GENEROUS spacing between components — no cramped layout, minimum 200 units between devices
     * Title block in bottom-right corner with: 'Block 00: Error Amplifier', 'PVDD 5V LDO — SkyWater SKY130A', date
     * Margins of at least 500 units on all sides
     * Component values (W/L) annotated next to each device
     * Pin labels for the subcircuit ports must be clearly visible at the edges
   - Use xschem symbol primitives for MOSFETs, voltage sources, current sources, capacitors, resistors
   - After creating the .sch file, export to PNG:
     xschem --no_x --netlist_type spice --export error_amp.png error_amp.sch
     OR if that doesn't work try:
     xschem -n -s -q --export error_amp.png error_amp.sch
     OR try using xschem batch mode to export
   - If xschem export fails, try alternative approaches to get the PNG
   - The PNG must be high resolution (at least 1920x1080)
   - Embed the schematic PNG in README.md

4. GENERATE ALL REQUIRED PLOTS using matplotlib:
   - Create/update plot_all.py to read simulation .dat files and produce:
     * bode_gain_phase.png — gain and phase vs frequency
     * output_swing.png — Vout vs differential input
     * noise_spectral.png — input-referred noise vs frequency
     * psrr_vs_freq.png — PSRR vs frequency
     * pvt_gain.png — DC gain across PVT corners
     * pvt_pm.png — phase margin across PVT corners
   - Run: python3 plot_all.py

5. COMMIT AND PUSH EVERYTHING:
   git add pvdd_regulator/00_error_amp/
   git commit -m 'feat(pvdd/00): error amp final — schematic, README, plots, all specs passing'
   git push origin autoresearch/error-amp-mar27

Do NOT skip any step. Do NOT stop until the push succeeds. Check that xschem is installed (which xschem). If xschem is not available, install it or use an alternative method to create the schematic visualization."
