# Block 10 — Full-Chain Integration: Requirements

## Software Tools (ALL tools from ALL blocks)

### Analog Simulation
| Tool | Version | Purpose |
|------|---------|---------|
| ngspice | >= 42 | SPICE simulation of full analog chain |
| Xschem | >= 3.4 | Schematic capture and netlist generation |
| Magic | >= 8.3.460 | Layout editor and DRC/LVS |
| KLayout | >= 0.28 | Layout viewer, DRC, GDS export |
| Netgen | >= 1.5 | LVS (layout vs. schematic) |

### Digital Simulation and Synthesis
| Tool | Version | Purpose |
|------|---------|---------|
| Yosys | >= 0.38 | Verilog synthesis to gate-level netlist |
| Icarus Verilog | >= 12 | Mixed-signal co-simulation (digital side) |
| cocotb | >= 1.8 | Testbench orchestration |
| Verilator | >= 5 | Alternative RTL simulator |

### Software / Analysis
| Tool | Version | Purpose |
|------|---------|---------|
| Python 3 | >= 3.10 | Orchestration, analysis, plotting |
| numpy | >= 1.24 | Numerical computation |
| scipy | >= 1.11 | Signal processing, .mat file loading |
| scikit-learn | >= 1.3 | Golden model comparison |
| matplotlib | >= 3.7 | Result visualization |
| pandas | >= 2.0 | Data aggregation and reporting |

### PDK
| Library | Purpose |
|---------|---------|
| SkyWater SKY130A PDK | All transistor models, standard cells |
| sky130_fd_sc_hd | Digital standard cell library |
| sky130_fd_pr | Primitive devices (resistors, capacitors, MOSFETs) |

## Block Dependencies (ALL must be complete)

| Block | Required Output | Purpose in Full Chain |
|-------|----------------|----------------------|
| 00_bias | bias_generator.spice | Bias currents for all analog blocks |
| 01_ota | ota.spice | OTA subcircuit for filters/PGA/envelope |
| 02_pga | pga.spice | Programmable gain amplifier |
| 03_filters | bpf1-5.spice | 5 band-pass filters |
| 04_envelope | envelope1-5.spice | 5 envelope detectors |
| 05_rms_crest | rms.spice, crest.spice | RMS and crest factor |
| 06_classifier | classifier.spice | Analog MAC + comparator |
| 07_adc | adc.spice | ADC for debug/monitoring |
| 08_digital | digital_top_synth.v | Synthesized digital control |
| 09_training | weights_spice.txt, feature_vectors_spice.txt | Trained weights + test vectors |

**This block CANNOT run until all other blocks (00-09) are complete.**

## File Structure (expected output)

```
10_fullchain/
  requirements.md              # this file
  program.md                   # integration specification
  netlists/
    vibrosense1_top.spice      # top-level SPICE netlist
    digital_wrapper.spice      # Verilog-A or behavioral model of digital block
  stimuli/
    normal_stimulus.pwl        # time-domain normal vibration
    inner_race_stimulus.pwl    # time-domain inner race fault
    outer_race_stimulus.pwl    # time-domain outer race fault
    ball_stimulus.pwl          # time-domain ball fault
  scripts/
    run_fullchain.py           # orchestrate simulation + analysis
    generate_stimuli.py        # convert CWRU data to analog waveforms
    analyze_results.py         # parse SPICE output, compute metrics
    compare_golden.py          # compare to Python golden model
    plot_results.py            # generate all figures
  results/
    fullchain_normal.raw       # ngspice output: normal case
    fullchain_inner.raw        # ngspice output: inner race fault
    fullchain_outer.raw        # ngspice output: outer race fault
    fullchain_ball.raw          # ngspice output: ball fault
    power_breakdown.txt        # per-block power measurement
    timing_report.txt          # detection latency measurements
    accuracy_report.txt        # classification accuracy summary
    comparison_table.txt       # vs POLYN, Aspinity, MCU+FFT
    final_specifications.txt   # proven chip specs for top-level README
    waveforms/                 # saved waveform plots
```
