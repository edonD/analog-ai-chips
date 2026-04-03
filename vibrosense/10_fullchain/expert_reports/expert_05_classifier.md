# Expert 05: Block 06 (Classifier MAC) Analysis

## File Status
- `design.cir`: EXISTS (0 bytes)
- `classifier.spice`: MISSING — program.md expects this
- `clkgen_3ph.spice`: EXISTS
- `full_results.json`: EXISTS

## SPICE Files Available
- _tmp_diag.spice
- _tmp_test_w0.spice
- _tmp_test_w15.spice
- _tmp_test_w5.spice
- clkgen_3ph.spice
- mac_8in4b.spice
- mac_unit.spice
- sky130_fd_pr__cap_mim_m3_1.spice
- sky130_minimal.lib.spice
- strongarm_comp.spice
- tb_8in4b_linearity.spice
- tb_8in4b_mim.spice
- tb_8in4b_multiinput.spice
- tb_charge_inject.spice
- tb_classify_cwru.spice
- tb_mac_linearity.spice
- tb_mac_linearity_base.spice
- tb_mac_timing.spice
- tb_mac_transient.spice
- test_quick.spice
- test_sw.spice
- wta_circuit.spice

## Subcircuit Definitions Found
```
clkgen_3ph.spice: .subckt clkgen_3ph clk_in phi_s phi_sb phi_e phi_eb phi_r vdd vss
mac_8in4b.spice: .subckt mac_8in4b
mac_unit.spice: .subckt mac_4in2b bl vss vdd
sky130_fd_pr__cap_mim_m3_1.spice: .subckt sky130_fd_pr__cap_mim_m3_1 c0 c1
strongarm_comp.spice: .subckt strongarm_comp vinp vinn voutp voutn clk vdd vss
wta_circuit.spice: .subckt wta_2input vinp vinn voutp voutn clk vdd vss
```

## design.cir Content
```

```

## Clock Generator (clkgen_3ph.spice)
```
* VibroSense Block 06: Non-Overlapping Clock Generator
* Input: clk_in (master clock)
* Outputs: phi_s/phi_sb (sample), phi_e/phi_eb (eval), phi_r (reset)
* Uses cross-coupled NAND gates for guaranteed non-overlap
* Process: SKY130A

* Simple 3-phase generator using delayed inverter chains
* Phase timing derived from master clock period

.subckt clkgen_3ph clk_in phi_s phi_sb phi_e phi_eb phi_r vdd vss

* --- Delay elements (inverter chains) ---
* Each inverter: NMOS W=0.42u L=0.15u, PMOS W=0.84u L=0.15u
* 2 inverters ≈ 200ps delay at SKY130

* Master clock buffer
XN_buf1 clk_buf1 clk_in vss vss sky130_fd_pr__nfet_01v8 W=0.84u L=0.15u
XP_buf1 clk_buf1 clk_in vdd vdd sky130_fd_pr__pfet_01v8 W=1.68u L=0.15u
XN_buf2 clk_buf clk_buf1 vss vss sky130_fd_pr__nfet_01v8 W=0.84u L=0.15u
XP_buf2 clk_buf clk_buf1 vdd vdd sky130_fd_pr__pfet_01v8 W=1.68u L=0.15u

* Phase generation using NAND-based non-overlapping generator
* For simplicity: phi_s = clk_buf, phi_e = delayed clk_buf_bar,
* phi_r = fu
```

## Results
```
{
  "p1": {
    "linearity_max_err_mV": 1.4993346468353541,
    "linearity_max_err_lsb": 0.101571325490018,
    "charge_injection_mV": 5.29202,
    "multi_vbl_sim": 0.44883,
    "multi_vbl_ideal": 0.4472249950960999,
    "multi_err_pct": 0.35888085896344024,
    "ci_full_mV": 5.044479999999999,
    "ci_full_lsb": 0.3417345961352624
  },
  "p3": {
    "winner": "Normal",
    "margin_mV": 19.25699999999997,
    "comp_correct": true,
    "comp_vdiff": -1.79985
  },
  "p4": {
    "n_mc": 200,
    "accuracy_pct": 99.5,
    "ideal_winner": "Normal",
    "vbl_mean": [
      543.1013391063295,
      524.7037967461365,
      515.6917599410045,
      451.6091830989291
    ],
    "vbl_std": [
      0.05080724052632674,
      0.04772114248874247,
      0.052069805888334306,
      0.05128238570031306
    ],
    "enob_class0": 4,
    "enob_class1": 4,
    "enob_class2": 4,
    "enob_class3": 4,
    "mean_enob": 4.0
  },
  "p5": {
    "phi_s_max": 1.826,
    "phi_e_max": 1.87166,
    "phi_r_max": 1.81663
  },
  "p7": {
    "pwr_at_10Hz_uW": 0.0
  },
  "p10": {
    "tt": 0.44883,
    "ss": 0.44831,
    "ff": 0.44916,
    "sf": 0.448816,
    "fs": 0.44833,
    "max_var_pct": 0.11585678319185892
  }
}
```

## Integration Requirements (from program.md)
```
Xclass venv1 venv2 venv3 venv4 venv5 vrms vcrest vkurt
+       class_result[3:0] class_valid
+       weights[31:0] thresh[7:0]
+       fsm_sample fsm_evaluate fsm_compare
+       ibias_10u vdd vss classifier
```

## Key Observations
1. **design.cir is empty** — the classifier netlist may be in other files
2. The classifier needs:
   - 8 analog feature inputs
   - 4-class output (4 bits)
   - Weight loading interface (32 capacitors, programmable)
   - 3-phase FSM control (sample, evaluate, compare)
   - Bias current
3. The clkgen_3ph.spice provides the 3-phase clock for the charge-domain MAC
4. For integration, may need to create a behavioral classifier if no transistor-level exists

## Integration Approach
1. If classifier.spice exists and has correct subcircuit — use directly
2. If not, create a behavioral SPICE model that:
   - Samples 8 input voltages
   - Multiplies by weight capacitors (from trained_weights.json)
   - Produces 4-class comparison output
   - Uses switched-capacitor MAC principle
3. The behavioral model is acceptable for integration validation
