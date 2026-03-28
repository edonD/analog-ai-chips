# Agent Instructions for Block 06: Level Shifter

## Working Directory
`/home/ubuntu/analog-ai-chips/pvdd_regulator/06_level_shifter/`

## Sky130 PDK Path
`/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/ngspice/sky130.lib.spice`

ngspice is installed at `/usr/bin/ngspice`. xschem is installed at `/usr/bin/xschem`.

## Phase 1: Read Everything First
Read these files to understand the full context:
- `program.md` — design rules, topology guidance, experiment loop, absolute rules
- `specification.json` — machine-readable pass/fail criteria
- `specs.tsc` — spec tracker with grep patterns and thresholds
- `design.cir` — empty subcircuit stubs to fill in
- `run_block.sh` — simulation runner
- `evaluate.py` — automated evaluator (DO NOT MODIFY)

## Phase 2: Design the Circuits
Implement both subcircuits in `design.cir`:
1. `level_shifter_up` (SVDD 2.2V → BVDD 5.4-10.5V) — cross-coupled PMOS topology
2. `level_shifter_down` (PVDD 5.0V → SVDD 2.2V) — voltage-clamped inverter

## Phase 3: Create All Testbenches
Create these testbench files:
- `tb_ls_logic.spice` — logic function, output levels, metastability
- `tb_ls_delay.spice` — propagation delay measurement
- `tb_ls_bvdd_sweep.spice` — function across BVDD = 5.4V, 7V, 10.5V
- `tb_ls_power.spice` — static power in both stable states
- `tb_ls_pvt.spice` — all criteria at all PVT corners

**CRITICAL:** Every testbench must print metrics in EXACTLY the format expected by specs.tsc:
```
delay_max_ns: <value>
lth_out_high_margin_V: <value>
lth_out_low_V: <value>
htl_out_high_margin_V: <value>
htl_out_low_V: <value>
static_power_uA: <value>
works_bvdd_min: 1
works_bvdd_max: 1
works_ss_150c: 1
no_metastable: 1
```

The LAST testbench that runs (tb_ls_pvt.spice) should print ALL metrics as the final summary since evaluate.py reads run.log and takes the LAST occurrence of each pattern.

## Phase 4: Experiment Loop
Follow the loop from program.md section 4:
1. Create branch: `git checkout -b autoresearch/level-shifter-mar27`
2. Iterate: modify design.cir → commit → run `bash run_block.sh > run.log 2>&1` → evaluate → keep/discard
3. Keep if delay_max_ns improves and all specs pass; discard otherwise

## Phase 5: Xschem Schematics (VERY IMPORTANT)

After the design passes all specs, create professional xschem schematics for BOTH subcircuits. This is critical — the schematics must be publication-quality.

### Schematic Requirements:
- Create `level_shifter_up.sch` and `level_shifter_down.sch` as xschem schematic files
- Use proper Sky130 PDK symbols from the xschem library
- **Layout must be extremely well-organized:**
  - Clear left-to-right or top-to-bottom signal flow
  - Supply rails (BVDD/SVDD/GND) clearly labeled at top and bottom
  - All internal nodes labeled with meaningful names
  - Wide margins on all sides (at least 200 units)
  - Title block with: block name, subcircuit name, designer "Claude AI", date, revision
  - No overlapping wires or components
  - Components spaced generously — readability over compactness
  - Input on the left, output on the right
  - Power supply connections at the top, ground at the bottom
  - Complementary devices (cross-coupled pair) should be symmetrically placed
  - Wire labels for every named net
- **Export to PNG:**
  ```bash
  xvfb-run -a xschem --png --plotfile level_shifter_up.png level_shifter_up.sch
  xvfb-run -a xschem --png --plotfile level_shifter_down.png level_shifter_down.sch
  ```
  If that doesn't work, try:
  ```bash
  xvfb-run -a xschem -n -s -q --png --plotfile level_shifter_up.png level_shifter_up.sch
  ```
  The `-n` flag means no-readline, `-s` means no-splash, `-q` means quit after.

## Phase 6: Update README.md

Create/update `README.md` with:
1. Block title and description
2. Architecture overview — both topologies explained
3. Device sizing table with W/L for every transistor
4. Schematic images embedded: `![Level Shifter Up](level_shifter_up.png)` and `![Level Shifter Down](level_shifter_down.png)`
5. Simulation results table: parameter | value | spec | pass/fail
6. Waveform plots embedded (from plot_all.py if available, or from testbench .dat files)
7. PVT corner summary
8. Design notes and trade-offs

## Phase 7: Commit and Push

After everything is complete:
```bash
cd /home/ubuntu/analog-ai-chips
git add pvdd_regulator/06_level_shifter/
git commit -m "design(06): level shifter — both directions verified, schematics generated

- level_shifter_up: cross-coupled PMOS, SVDD(2.2V) to BVDD(5.4-10.5V)
- level_shifter_down: clamped inverter, PVDD(5V) to SVDD(2.2V)
- All 10 specs passing across PVT corners
- Xschem schematics with PNG exports
- Full README with results and embedded schematics"
git push origin HEAD
```

## ABSOLUTE RULES
- Do NOT modify `specification.json`, `evaluate.py`, or `program.md`
- Every transistor must be a real Sky130 PDK device
- No behavioral models except testbench stimulus
- All simulations in ngspice
- Every spec verified by simulation
- NEVER STOP iterating until all specs pass
- The schematics MUST be clean, well-organized, and professional
