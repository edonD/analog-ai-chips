#!/bin/bash
cd /home/ubuntu/analog-ai-chips/vibrosense/01_ota/schematic
LOG="agent.log"
echo "=== Schematic Agent started at $(date) ===" > "$LOG"

PROMPT='You are an analog IC layout engineer. Your mission is to create a high-quality xschem schematic (.sch) for the VibroSense folded-cascode OTA.

TODAY IS 2026-03-23.

## ENVIRONMENT
- xschem 3.4.4 at /usr/bin/xschem
- Xvfb for headless rendering
- Python 3 with openai package installed
- puppeteer available globally via node
- Working dir: /home/ubuntu/analog-ai-chips/vibrosense/01_ota/schematic
- SKY130 PDK: /home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A

## THE NETLIST (IMMUTABLE — DO NOT MODIFY)
The SPICE netlist is at: /home/ubuntu/analog-ai-chips/vibrosense/01_ota/ota_foldcasc.spice
It contains 13 transistors (7 NFET, 6 PFET) in a folded-cascode topology.
Read it carefully — every device, every net, every W/L must match exactly in the schematic.

## THE INFERENCE API
There is a model at http://18.232.161.171:8000/v1 (OpenAI-compatible) that converts SPICE to xschem.
- Model ID: cir2sch-fft-4b
- Use the helper: python3 cir2sch.py /path/to/netlist.spice output.sch
- Or call the API directly via the openai Python package

## YOUR WORKFLOW

### Step 1: Generate initial schematic via API
Read the netlist, call the inference API via cir2sch.py, get the initial .sch file.
Save as ota_foldcasc_raw.sch

### Step 2: Validate the raw output
Run: python3 validate_sch.py ota_foldcasc_raw.sch
This checks:
- All 13 transistors present with correct SKY130 models
- All 9 ports present (vinp, vinn, vout, vdd, vss, vbn, vbcn, vbp, vbcp)
- Net connectivity
- Generates a PNG for visual inspection

### Step 3: Fix the schematic
The API output will likely need fixes. You must:

a) Ensure correct xschem symbol paths for SKY130:
   - NFET: {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym}
   - PFET: {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym}
   - Or shorter if xschem knows the PDK path: {sky130_fd_pr/nfet_01v8.sym}

b) Ensure every transistor has the correct W, L, nf parameters as attributes

c) Ensure proper pin connections match the netlist exactly:
   - M1: drain=fold_p, gate=vinp, source=tail, body=vss
   - M2: drain=fold_n, gate=vinn, source=tail, body=vss
   - M3: drain=fold_p, gate=vbp, source=vdd, body=vdd
   - M4: drain=fold_n, gate=vbp, source=vdd, body=vdd
   - M5: drain=cas_p, gate=vbcp, source=fold_p, body=vdd
   - M6: drain=vout, gate=vbcp, source=fold_n, body=vdd
   - M7: drain=cas_p, gate=vbcn, source=src7, body=vss
   - M8: drain=vout, gate=vbcn, source=src8, body=vss
   - M9: drain=src7, gate=vbn, source=vss, body=vss
   - M10: drain=src8, gate=vbn, source=vss, body=vss
   - M11: drain=tail, gate=vbn, source=vss, body=vss
   - M12: drain=fold_p, gate=vbp, source=vdd, body=vdd
   - M13: drain=fold_n, gate=vbp, source=vdd, body=vdd

d) Follow analog layout conventions:
   - VDD rail at top, VSS rail at bottom
   - PMOS devices in upper half, NMOS in lower half
   - Input pair (M1/M2) centered, symmetric
   - Output node (vout) clearly labeled on the right
   - Bias inputs (vbn, vbcn, vbp, vbcp) on the left side
   - Signal inputs (vinp, vinn) on the left
   - Clean, non-overlapping wires

### Step 4: Visual quality check
Use xschem + Xvfb to export a PNG:
    xvfb-run --auto-servernum xschem --plotfile ota_foldcasc.png -q ota_foldcasc.sch

Or write a tcl script for xschem to export. Check the PNG visually (read it with the Read tool).
Fix any overlapping components, crossed wires, or poor placement.

### Step 5: Netlist round-trip verification
Extract a SPICE netlist from the schematic:
    xvfb-run --auto-servernum xschem -n -q ota_foldcasc.sch

Compare the extracted netlist with the original. Every device, net, and parameter must match.

### Step 6: If the API output is unusable, BUILD IT MANUALLY
The xschem .sch format is text-based. You can construct it directly:
- v { ... } header block
- G { ... } global attributes
- C { symbol_path } x y rotation mirror { attributes } for each component
- N x1 y1 x2 y2 { ... } for wires
- T { text } x y for labels

If the API gives garbage, write the .sch file yourself using the xschem format specification.
The topology is well-defined — 13 transistors, known connections. You can do this.

### Step 7: Final deliverables
- ota_foldcasc.sch — the clean, validated schematic
- ota_foldcasc.png — screenshot of the schematic
- validation_report.txt — output of validate_sch.py showing all checks pass

## IMMUTABLE CONSTRAINT
The SPICE netlist ota_foldcasc.spice must NOT be modified. The schematic must match it exactly.
Do not simplify, rename, or change any device parameters to make drawing easier.

## GIT
Commit when done: git add -A && git commit -m "schematic: xschem schematic for folded-cascode OTA" && git push

NEVER STOP until you have a valid .sch file with all 13 transistors correctly placed and connected.'

exec claude --dangerously-skip-permissions --verbose --output-format stream-json -p "$PROMPT" 2>&1 | tee -a "$LOG"
