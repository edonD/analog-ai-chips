# Expert 07: Block 08 (Digital Block) Analysis

## File Status

### RTL Files
- clk_divider.v
- debounce.v
- digital_top.v
- fsm_classifier.v
- reg_file.v
- spi_slave.v

### Synthesis
- `digital_top_synth.v`: EXISTS (117698 chars)
- `synth_report.txt`: EXISTS
- `synth.ys`: EXISTS

### Verification
- `verification_report.txt`: EXISTS

## Module Definitions
```
module digital_top #(
```

## Digital Top Port Summary (from RTL)
```
`timescale 1ns / 1ps
// =============================================================================
// digital_top.v — Top-Level Digital Control for VibroSense-1
// =============================================================================
// Instantiates: spi_slave, reg_file, fsm_classifier, debounce, clk_divider.
// All analog interface signals wired to register file outputs.
//
// Silicon-ready: no internal tristates, proper CDC with shadow registers,
// real adc_done input, FSM gated by CTRL register enable bit.
// =============================================================================

module digital_top #(
    // FSM timing parameters
    parameter SAMPLE_CYCLES = 64,
    parameter EVAL_CYCLES   = 128,
    parameter COMP_CYCLES   = 4,
    parameter WAIT_CYCLES   = 804,
    parameter FSM_CNT_WIDTH = 10
) (
    // System
    input  wire        clk,
    input  wire        rst_n,

    // SPI interface (miso split into data + output-enable for pad-level tristate)
    input  wire        sck,
    input  wire        mosi,
    input  wire        cs_n,
    output wire        miso_data,
    output wire        miso_oe_n,

    // Interrupt
    output wire        irq_n,

    // PGA configuration
    output wire [1:0]  gain,

    // BPF tuning DACs
    output wire [3:0]  tune1,
    output wire [3:0]  tune2,
    output wire [3:0]  tune3,
    output wire [3:0]  tune4,
    output wire [3:0]  tune5,

    // Classifier weights and threshold
    output wire [31:0] weights,
    output wire [7:0]  thresh,

    // Debounce setting
    output wire [3:0]  debounce_val,

    // ADC interface
    output wire [1:0]  adc_chan,
    output wire        adc_start,
    input  wire [7:0]  adc_data_in,
    input  wire        adc_done,       // real ADC done signal from analog

    // Analog classifier interface
    input  wire [3:0]  class_result,
    input  wire        class_valid,

    // Classifier FSM outputs (to analog MAC)
    output wire        fsm_sample,
    output wire       
```

## Synthesis Report
```

 /----------------------------------------------------------------------------\
 |                                                                            |
 |  yosys -- Yosys Open SYnthesis Suite                                       |
 |                                                                            |
 |  Copyright (C) 2012 - 2020  Claire Xenia Wolf <claire@yosyshq.com>         |
 |                                                                            |
 |  Permission to use, copy, modify, and/or distribute this software for any  |
 |  purpose with or without fee is hereby granted, provided that the above    |
 |  copyright notice and this permission notice appear in all copies.         |
 |                                                                            |
 |  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES  |
 |  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF          |
 |  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR   |
 |  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES    |
 |  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN     |
 |  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF   |
 |  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.            |
 |                                                                            |
 \----------------------------------------------------------------------------/

 Yosys 0.33 (git sha1 2584903a060)


-- Executing script file `synth.ys' --

1. Executing Verilog-2005 frontend: ../rtl/spi_slave.v
Parsing Verilog input from `../rtl/spi_slave.v' to AST representation.
Generating RTLIL representation for module `\spi_slave'.
Warning: Replacing memory \shadow_regs with list of registers. See ../rtl/spi_slave.v:84
Successfully finished Verilog frontend.

2. Executing Verilog-2005 frontend: ../rtl/reg_file.v
Parsing Verilog input from `../rtl
```

## Verification Report
```
VibroSense-1 Block 08 — Digital Control Block
Verification Report
===============================================================
Date:       2026-03-23
Tool:       Python 3.12 behavioral simulation (cycle-accurate RTL models)
Platform:   Windows 11 (no Icarus Verilog / cocotb available on this host)
Simulator:  Python behavioral models in tb/sim_models.py mirror the Verilog
            RTL logic exactly (same clock-cycle semantics, same reset values,
            same self-clearing/read-to-clear behavior).
RTL files:  rtl/clk_divider.v, rtl/fsm_classifier.v, rtl/reg_file.v,
            rtl/debounce.v, rtl/spi_slave.v, rtl/digital_top.v
Testbenches: tb/test_spi.py, tb/test_fsm.py, tb/test_debounce.py, tb/test_top.py
Synthesis:  synth/synth.ys provided; results ESTIMATED (Yosys not installed)

===============================================================
OVERALL RESULT: PASS — 121/121 test cases passed
===============================================================

───────────────────────────────────────────────────────────────
Test Suite 1: SPI Register Read/Write  (tb/test_spi.py)
Result: PASS  48/48
───────────────────────────────────────────────────────────────

  Sub-test 1a: Write all-1s (valid bits) to all RW registers, read back
    All 13 RW registers pass  (addr 0x00-0x0B, 0x0D)       PASS

  Sub-test 1b: Write 0x00 to all RW registers, read back zero
    All 13 RW registers pass                                 PASS

  Sub-test 2: Reset values after rst_n release
    All 15 registers hold correct reset values               PASS
    0x00 GAIN=0x00, 0x01-0x05 TUNE=0x08, 0x06-0x09 WEIGHT=0x00
    0x0A THRESH=0xFF, 0x0B DEBOUNCE=0x03, 0x0C STATUS=0x00
    0x0D ADC_CTRL=0x00, 0x0E ADC_DATA=0x00

  Sub-test 3: Read-only register enforcement
    0x0C STATUS write ignored                                 PASS
    0x0E ADC_DATA write ignored                               PASS

  Sub-test 4: Out-of-range address 0x0F
    Write ignored, read returns 0x00             
```

## Integration Requirements
The digital block needs a SPICE behavioral wrapper. program.md specifies:
```
Xdigital sck mosi cs_n miso irq_n
+         gain[1:0] tune1[3:0] tune2[3:0] tune3[3:0] tune4[3:0] tune5[3:0]
+         weights[31:0] thresh[7:0] debounce[3:0]
+         class_result[3:0] class_valid
+         fsm_sample fsm_evaluate fsm_compare
+         clk rst_n vdd vss digital_wrapper
```

## Key Findings
1. The digital block has both RTL and synthesized versions
2. For SPICE integration, we need a **behavioral SPICE wrapper** (Verilog-A or PWL)
3. The wrapper translates between digital signals and analog voltages
4. Key functions: SPI config, weight register loading, FSM control, debounce, IRQ

## Integration Approach
For the full-chain simulation, the digital block can be:

1. **Simplified behavioral model** (recommended):
   - Pre-load weights at t=0 (no SPI stimulus needed)
   - Generate 3-phase FSM signals (sample/evaluate/compare) at 1kHz
   - Debounce classifier output and drive IRQ
   - Use voltage-controlled sources in SPICE

2. **Co-simulation** (complex):
   - Use ngspice + Icarus Verilog co-simulation
   - More accurate but much harder to set up

3. **Pure SPICE behavioral** (simplest):
   - PWL sources for FSM clocks
   - Weight values as .param (already in weights_spice.txt)
   - Simple comparator for class output -> IRQ
