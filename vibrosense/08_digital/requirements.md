# Block 08 — Digital Control: Requirements

## Software Tools

| Tool | Version | Purpose |
|------|---------|---------|
| Yosys | >= 0.38 | Verilog synthesis to gate-level netlist |
| OpenROAD / OpenLane2 / LibreLane | latest | Place and route (optional, for area/timing) |
| Icarus Verilog | >= 12 | RTL simulation (alternative: Verilator >= 5) |
| Verilator | >= 5 | Fast RTL simulation (alternative to Icarus) |
| cocotb | >= 1.8 | Python-based testbench framework |
| Python 3 | >= 3.10 | cocotb runtime, scripting |
| GTKWave | latest | Waveform viewer for VCD/FST files |

## PDK / Cell Library

| Library | Purpose |
|---------|---------|
| SkyWater SKY130A PDK | Target technology node |
| sky130_fd_sc_hd | Standard cell library (high density) |

## Analog Dependencies

**None.** This is a pure digital block.

No SPICE simulator required. No analog models required. The digital block
interfaces with analog blocks only through clean digital signals (SPI bus,
register values, IRQ output, classifier control signals).

## Installation (Ubuntu/Debian)

```bash
# Yosys
sudo apt install yosys

# Icarus Verilog
sudo apt install iverilog

# GTKWave
sudo apt install gtkwave

# Python + cocotb
pip install cocotb>=1.8

# SkyWater PDK (for synthesis target)
# Clone sky130_fd_sc_hd liberty/verilog from:
# https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hd
```

## File Structure (expected output)

```
08_digital/
  requirements.md          # this file
  program.md               # design specification
  rtl/
    spi_slave.v            # SPI slave interface
    reg_file.v             # register file (14 registers)
    fsm_classifier.v       # classifier timing FSM
    debounce.v             # debounce + IRQ logic
    clk_divider.v          # clock divider
    digital_top.v          # top-level wrapper
  tb/
    test_spi.py            # cocotb: SPI read/write all registers
    test_fsm.py            # cocotb: classifier timing verification
    test_debounce.py       # cocotb: debounce + IRQ logic
    test_top.py            # cocotb: integrated top-level test
    Makefile               # cocotb Makefile
  synth/
    synth.ys               # Yosys synthesis script
    synth_report.txt       # gate count, timing, area
    digital_top_synth.v    # synthesized gate-level netlist
```
