# Block 08: Mode Control — Autonomous Design Task

You are designing Block 08 (Mode Control) for the PVDD 5V LDO Regulator on SkyWater SKY130A.

## READ FIRST
- Read `program.md` in this directory completely — it defines everything.
- Read `specification.json` and `specs.tsc` for pass/fail criteria.
- Read `evaluate.py` and `run_block.sh` — do NOT modify these.
- Read `../06_level_shifter/design.cir` — dependency for domain crossing.
- Read `../program.md` — global rules (real PDK only, no behavioral models, ngspice only).
- Read `../00_error_amp/error_amp.sch` — reference for xschem schematic style.

## SPICEINIT
A `.spiceinit` with `set ngbehavior=hs` exists in this directory. This means W/L values in subcircuit instantiations are in MICRONS when using the PDK models directly. Use the local `sky130.lib.spice` approach — copy/symlink the PDK lib to this directory like Block 04 does, or use the one at `../sky130.lib.spice`.

## YOUR TASK

### Phase 1: Design the Circuit (design.cir)
Build the mode control circuit in `design.cir`. Architecture per program.md:
- Single resistor ladder (BVDD → R5 → tap4 → R4 → tap3 → R3 → tap2 → R2 → tap1 → R1 → GND)
- Four comparators using HV diff pairs (sky130_fd_pr__nfet_g5v0d10v5 or pfet), each comparing a tap to vref (1.226V)
- SR latches or positive feedback for ~200mV hysteresis
- Combinational logic to decode the 4 comparator outputs into: bypass_en, ea_en, ref_sel, uvov_en, ilim_en, pass_off
- All devices must be real Sky130 PDK devices (HV: g5v0d10v5)
- Quiescent current < 20µA total from BVDD

Threshold targets (set by resistor ladder ratios):
- TH1 = 2.5V (POR exit): tap1 = vref when BVDD = 2.5V → R1/(R1+R2+R3+R4+R5) = 1.226/2.5
- TH2 = 4.2V: tap2 = vref when BVDD = 4.2V
- TH3 = 4.5V: tap3 = vref when BVDD = 4.5V
- TH4 = 5.6V: tap4 = vref when BVDD = 5.6V

Subcircuit: `.subckt mode_control bvdd pvdd svdd gnd vref en_ret bypass_en ea_en ref_sel uvov_en ilim_en pass_off`

Mode truth table:
| Mode | comp1 | comp2 | comp3 | comp4 | bypass_en | ea_en | ref_sel | uvov_en | ilim_en | pass_off |
|------|-------|-------|-------|-------|-----------|-------|---------|---------|---------|----------|
| POR (BVDD<2.5V) | 0 | 0 | 0 | 0 | 0 | 0 | X | 0 | 0 | 1 |
| Ret bypass | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| Ret regulate | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| PU bypass | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| Active | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 0 |

### Phase 2: Write All Testbenches
Create all testbenches listed in program.md deliverables:
- `tb_mc_ramp_normal.spice` — BVDD ramp 0→10.5V at 1V/µs, measure all thresholds and outputs
- `tb_mc_fast_ramp.spice` — 12 V/µs ramp
- `tb_mc_slow_ramp.spice` — 0.1 V/µs ramp
- `tb_mc_power_down.spice` — BVDD 10.5V→0, reverse transitions
- `tb_mc_hysteresis.spice` — up/down threshold measurement
- `tb_mc_iq.spice` — quiescent current at BVDD=7V active mode
- `tb_mc_pvt.spice` — all corners

Each testbench must print results in the format:
```
thresh_max_error_pct: <value>
thresh_por_V: <value>
thresh_ret_V: <value>
...
```

Use `.lib "../sky130.lib.spice" tt` for PDK models.

### Phase 3: Experiment Loop
Follow the experiment loop from program.md section 4:
1. Build initial design.cir with one comparator (TH4) first
2. Run: `ngspice -b tb_mc_ramp_normal.spice` to test
3. If crashes, debug with `tail -50 run.log`
4. Add comparators incrementally (TH1, TH2, TH3)
5. Add logic decoding
6. Run full suite: `bash run_block.sh > run.log 2>&1`
7. Check: `grep "^thresh_max_error_pct:\|^monotonic:\|^glitch_free:" run.log`
8. Iterate — tune ladder resistors, fix glitches, improve thresholds
9. Commit working improvements: `git add pvdd_regulator/08_mode_control/ && git commit -m "exp(08): <what changed>"`
10. If regression, revert: `git checkout pvdd_regulator/08_mode_control/design.cir`
11. NEVER STOP — keep improving until all 16 specs pass, then optimize Iq

### Phase 4: Plots and README
After specs pass:
1. Write `plot_all.py` to generate PNGs from simulation data
2. Write `README.md` with all required plots embedded
3. Commit

### Phase 5: Xschem Schematic
After the design is finalized and all specs pass, create an xschem schematic:
1. Study `../00_error_amp/error_amp.sch` for the exact xschem file format, symbol paths, coordinate system, and annotation style
2. Create `mode_control.sch` following the same conventions:
   - Use real Sky130 PDK symbols from `/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/`
   - pfet_g5v0d10v5.sym, nfet_g5v0d10v5.sym for transistors
   - Standard xschem resistor/capacitor symbols where needed
   - Organize into clear sections: RESISTOR LADDER, COMPARATOR 1-4, LOGIC, ENABLE
   - Add characterization text block with all measured results
   - Add title, subtitle, port labels
3. Export to PNG: `xschem --no_x --netlist --png mode_control.png mode_control.sch`
4. Commit the .sch and .png

## CONSTRAINTS
- Do NOT modify `specification.json`, `evaluate.py`, `program.md`, or `specs.tsc`
- All devices must be real Sky130 PDK (no behavioral, no Verilog-A, no ideal switches)
- Only testbench stimulus sources can be ideal
- ngspice only
- Push through convergence issues with .option settings
- Build incrementally — get one comparator working before adding the next
