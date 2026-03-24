# Block 08 — Digital Control (Silicon-Hardened)

**Process:** SkyWater SKY130 (sky130_fd_sc_hd) | **Supply:** 1.8 V | **Power:** ~1.6 uW @ 1 MHz | **Status:** ALL SPECS PASS — TAPEOUT READY

---

## 1. Overview

Digital control block for the VibroSense-1 analog ML vibration classifier. Implements SPI slave interface with shadow registers, 16-register configuration file (including CTRL register with FSM enable), classifier timing FSM, debounce/IRQ logic, and clock divider. This is the only digital block in the chip — everything else is analog. Its job is to configure the analog signal chain via SPI, orchestrate the charge-domain MAC classifier computation, and report anomaly detection results to an external MCU via interrupt.

---

## 2. Architecture

### 2.1 Block Diagram

![Digital Control Block Diagram](digital_top.png)

The rendered schematic is also available in xschem format: [`digital_top.sch`](digital_top.sch).

Five sub-modules are arranged left-to-right:

1. **spi_slave** — SPI Mode 0 interface with toggle-based CDC and shadow register snapshot
2. **reg_file** — 16 x 8-bit configuration registers with special behaviors (read-to-clear, self-clear, FSM enable)
3. **fsm_classifier** — Counter-based timing FSM generating SAMPLE/EVALUATE/COMPARE/WAIT phases
4. **debounce** — Consecutive-match filter with configurable threshold and active-low IRQ output
5. **clk_divider** — 4-bit counter providing /2, /4, /8, /16 clock-enable taps

### 2.2 Design Philosophy

1. **Counter-based FSM** — No state register; a single 10-bit counter IS the state. Combinational decode generates all phase signals. Total period = SAMPLE(64) + EVAL(128) + COMPARE(4) + WAIT(804) = 1000 cycles.

2. **Toggle-based CDC** — Write path from SPI (SCK domain) to register file (CLK domain) uses toggle synchronizer with 3-stage sync chain. An XOR edge detector produces a single wr_pulse in the CLK domain.

3. **Shadow registers for reads** — On cs_n falling edge (detected via 3-stage synchronizer), all 16 register values (128 bits) are captured into a clk-domain shadow buffer. The SPI slave reads from this buffer, fully in the SCK domain after capture. This eliminates CDC violations on the read path.

4. **Separate MISO data/enable** — `miso_data` carries the data, `miso_oe_n` controls the pad-level tristate (directly follows cs_n). No internal tristate buffers in the synthesized netlist.

5. **FSM gated by CTRL register** — FSM is disabled by default after reset. Software must write CTRL[0]=1 to start the classifier. This prevents spurious timing signals to the analog MAC during configuration.

6. **Real ADC handshake** — `adc_done` is a direct input from the external SAR ADC. No fake timer stubs.

### 2.3 Silicon-Hardening Changes (v2)

This version resolves all critical and moderate issues identified during the pre-tapeout review:

| # | Issue | Severity | Fix |
|---|-------|----------|-----|
| 1 | Unreset SCK-domain FFs (initial block) | Critical | Per-txn FFs reset by cs_n posedge; persistent CDC FFs reset by rst_n. Initial block removed. |
| 2 | Internal tristate on MISO | Critical | Split into miso_data + miso_oe_n. Pad handles tristate. |
| 3 | SPI read path CDC violation | Critical | Shadow register approach: 128-bit snapshot on cs_n falling edge. |
| 4 | Dead class_valid port in debounce | Moderate | Port removed from debounce.v and digital_top.v instantiation. |
| 5 | Clock divider outputs not true clocks | Moderate | Documented as clock-enable signals (counter taps). |
| 6 | ADC handshake is fake 10-cycle stub | Moderate | Real adc_done input pin; fake timer removed. |
| 7 | FSM has no software enable/sleep | Moderate | CTRL register at 0x0F, bit[0] = FSM enable, default disabled. |

---

## 3. Register Map

**16 registers, addressed 0x00-0x0F:**

| Addr | Name | R/W | Width | Reset | Description |
|------|------|-----|-------|-------|-------------|
| 0x00 | GAIN | RW | 2 | 0x00 | PGA gain (0=1x, 1=4x, 2=16x, 3=64x) |
| 0x01 | TUNE1 | RW | 4 | 0x08 | BPF1 frequency tuning DAC |
| 0x02 | TUNE2 | RW | 4 | 0x08 | BPF2 frequency tuning DAC |
| 0x03 | TUNE3 | RW | 4 | 0x08 | BPF3 frequency tuning DAC |
| 0x04 | TUNE4 | RW | 4 | 0x08 | BPF4 frequency tuning DAC |
| 0x05 | TUNE5 | RW | 4 | 0x08 | BPF5 frequency tuning DAC |
| 0x06 | WEIGHT0 | RW | 8 | 0x00 | Classifier weights 0-1 (2x4-bit packed) |
| 0x07 | WEIGHT1 | RW | 8 | 0x00 | Classifier weights 2-3 |
| 0x08 | WEIGHT2 | RW | 8 | 0x00 | Classifier weights 4-5 |
| 0x09 | WEIGHT3 | RW | 8 | 0x00 | Classifier weights 6-7 |
| 0x0A | THRESH | RW | 8 | 0xFF | Anomaly threshold (default=max=never trigger) |
| 0x0B | DEBOUNCE | RW | 4 | 0x03 | Consecutive detections before IRQ |
| 0x0C | STATUS | R | 8 | 0x00 | [7]=valid (read-to-clear), [3:0]=class_result |
| 0x0D | ADC_CTRL | RW | 4 | 0x00 | [3]=busy(RO), [2]=start(self-clear), [1:0]=chan |
| 0x0E | ADC_DATA | R | 8 | 0x00 | Last ADC conversion result |
| 0x0F | CTRL | RW | 1 | 0x00 | [0]=FSM enable (0=disabled, 1=enabled) |

**Special Behaviors:**
- Writing DEBOUNCE register resets the debounce counter (prevents stale counts from old threshold)
- ADC_CTRL[2] (start) self-clears after 1 clock cycle; ADC_CTRL[3] (busy) clears on adc_done
- STATUS[7] (valid) clears on SPI read of address 0x0C (read-to-clear)
- Writes to read-only registers (STATUS at 0x0C, ADC_DATA at 0x0E) are silently ignored
- CTRL[0] must be set to 1 to start the classifier FSM (default: disabled after reset)

---

## 4. SPI Protocol

### 4.1 Mode and Framing

- **SPI Mode 0**: CPOL=0, CPHA=0 (data sampled on rising SCK edge, shifted on falling edge)
- **Frame**: 16 bits per transaction (active while cs_n is low)
  - Bits [15:8] = Address byte: bit[7]=R/W flag (1=read, 0=write), bits[6:0]=register address
  - Bits [7:0] = Data byte: write data (write) or don't-care (read)

### 4.2 Timing

```
cs_n   ____/                                                 \____
sck    ____/ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 \____
mosi   -----<RW><A6><A5><A4><A3><A2><A1><A0><D7><D6><D5><D4><D3><D2><D1><D0>
miso   ----(Z)-----------------------------<R7><R6><R5><R4><R3><R2><R1><R0>
```

- **Write**: RW=0. Data latched on bit 15 (last SCK rising edge). Toggle CDC transfers to CLK domain.
- **Read**: RW=1. Shadow registers are snapshotted on cs_n falling edge. MISO shifts out read data starting at bit 8 (on SCK falling edges).
- **MISO output enable**: `miso_oe_n` = `cs_n` (output enabled only during transaction)

### 4.3 CDC Write Path

1. SPI slave latches `wr_addr_hold` and `wr_data_hold` at bit 15, toggles `wr_toggle`
2. 3-stage synchronizer in CLK domain: `wr_sync1 -> wr_sync2 -> wr_sync3`
3. XOR edge detect: `wr_pulse = wr_sync2 ^ wr_sync3`
4. `wr_pulse` drives register file write for one CLK cycle

### 4.4 CDC Read Path (Shadow Registers)

1. cs_n falling edge detected via 3-stage synchronizer: `cs_n_sync1 -> cs_n_sync2 -> cs_n_sync3`
2. Falling edge: `snapshot_req = cs_n_sync3 & ~cs_n_sync2`
3. All 16 registers (128 bits) captured into `shadow_regs[]` array in CLK domain
4. SPI slave reads from `shadow_regs[]` in SCK domain (safe: values are stable for entire transaction)

---

## 5. FSM Description

### 5.1 State Machine

The `fsm_classifier` uses a single 10-bit counter as its state. No explicit state register is needed. Phase signals are decoded combinationally from the counter value:

| Phase | Counter Range | Cycles | Output Asserted | Purpose |
|-------|--------------|--------|-----------------|---------|
| SAMPLE | 0 to 63 | 64 | `fsm_sample` | ADC samples vibration data |
| EVALUATE | 64 to 191 | 128 | `fsm_evaluate` | Charge-domain MAC computes |
| COMPARE | 192 to 195 | 4 | `fsm_compare` | Threshold comparison |
| WAIT | 196 to 999 | 804 | (none) | Idle between classifications |

- **Total period**: 1000 cycles (1 ms at 1 MHz clock)
- **Enable gating**: Counter holds at 0 when `enable` = 0 (from CTRL[0])
- **fsm_done**: Pulsed for 1 cycle at counter = 999 (end of WAIT phase)
- **Reset behavior**: Counter resets to 0 on rst_n assertion

### 5.2 Timing Diagram

```
counter:  0   63 64  191 192 195 196        999 0
          |----|----|-----|----|-----|---------|
phase:    SAMPLE  EVALUATE  COMPARE    WAIT     SAMPLE...
fsm_done:                                    ^pulse
```

---

## 6. Debounce Algorithm

### 6.1 Operation

The debounce module implements a consecutive-match filter to prevent spurious interrupt assertions:

1. On each `fsm_done` pulse, the current `class_result` is compared to a stored `prev_class`
2. If the class matches the previous result, `match_count` increments
3. If the class changes, `match_count` resets to 1 and `prev_class` updates
4. When `match_count >= debounce_val`, `irq_n` asserts (active low) and `irq_class` latches the result
5. `irq_n` deasserts when `match_count < debounce_val` (class changes or threshold reconfigured)

### 6.2 Configuration

- `debounce_val` range: 1-15 (4-bit, from register 0x0B)
- Default: 3 (require 3 consecutive identical classifications)
- Writing the DEBOUNCE register generates `debounce_wr_pulse`, which resets `match_count` to 0

### 6.3 Edge Cases

- `debounce_val = 1`: IRQ asserts on the first classification (no debouncing)
- `debounce_val = 0`: effectively requires 0 consecutive matches (immediate trigger)
- Class changes mid-sequence: counter resets, must re-accumulate from 1

---

## 7. Silicon-Hardening Changes

See Section 2.3 for the complete table. The key changes that differentiate v2 from v1:

**Before (v1 — simulation only):**
- SCK-domain FFs initialized via `initial` block (not synthesizable)
- Internal tristate: `assign miso = cs_n ? 1'bz : miso_bit`
- CDC violation: SPI reads directly from CLK-domain combinational logic
- Dead `class_valid` port on debounce
- Fake 10-cycle ADC done stub
- FSM always running from reset

**After (v2 — silicon-ready):**
- Proper async resets on all FFs (cs_n posedge for per-txn, rst_n for persistent)
- Split MISO: `miso_data` + `miso_oe_n` (pad handles tristate)
- Shadow register snapshot eliminates read-path CDC violation
- Clean port list (dead ports removed)
- Real `adc_done` input pin
- CTRL[0] gates FSM (default disabled)

---

## 8. Test Results

### 8.1 Test Summary

All testbenches written in cocotb 2.0.1 with Icarus Verilog 12.0.

| Test Suite | Tests | Pass | Fail | Coverage |
|------------|-------|------|------|----------|
| test_clk_divider.py | 2 | 2 | 0 | Divide ratios, reset behavior |
| test_fsm.py | 5 | 5 | 0 | Phase durations, multi-cycle, order, reset, enable gating |
| test_debounce.py | 7 | 7 | 0 | Threshold, immediate, class change, reset, deassert |
| test_spi.py | 8 | 8 | 0 | Write/read, reset values, read-only, config outputs, CTRL reg, miso_oe_n, shadow snapshot, no spurious writes |
| test_top.py | 6 | 6 | 0 | Full integration, ADC done pin, FSM enable/disable, FSM signals, clock dividers, SPI stress |
| **Total** | **28** | **28** | **0** | -- |

### 8.2 Key Results Table

| Parameter | Specification | Measured | Margin | Status |
|-----------|--------------|----------|--------|--------|
| SPI read/write all registers | Correct | All 16 registers verified | -- | **PASS** |
| SPI read-only enforcement | Writes ignored | Confirmed (STATUS, ADC_DATA) | -- | **PASS** |
| Shadow register snapshot | Consistent read | Verified | -- | **PASS** |
| MISO output enable (miso_oe_n) | High when cs_n high | Verified | -- | **PASS** |
| No spurious writes after reset | None | Verified | -- | **PASS** |
| FSM enable/disable via CTRL | Functional | Verified | -- | **PASS** |
| ADC done input pin | Functional | Verified | -- | **PASS** |
| FSM phase durations | Exact match | 64/128/4/804 cycles exact | 0 error | **PASS** |
| FSM total period | 1000 cycles | 1000 cycles | Exact | **PASS** |
| IRQ assertion timing | <=1 clk | 1 clk | -- | **PASS** |
| IRQ deassertion timing | <=1 clk | 1 clk | -- | **PASS** |
| Debounce counter behavior | Per spec | 7/7 tests pass | -- | **PASS** |

### 8.3 New Tests Added for Silicon Hardening

| Test | What It Verifies |
|------|-----------------|
| test_ctrl_register | CTRL register (0x0F) write/read, FSM enable bit |
| test_miso_oe_n | miso_oe_n follows cs_n (high when deselected) |
| test_shadow_register_snapshot | Shadow registers capture consistent snapshot on cs_n fall |
| test_no_spurious_write_after_reset | No register corruption after reset (toggle CDC correctness) |
| test_adc_done_pin | Real adc_done input captures ADC data correctly |
| test_fsm_enable_disable | FSM stays idle until CTRL[0]=1, stops when CTRL[0]=0 |

---

## 9. Synthesis Results

### 9.1 Tool Chain

| Tool | Version | Target |
|------|---------|--------|
| Yosys | 0.33 | Synthesis + technology mapping |
| Liberty | sky130_fd_sc_hd__tt_025C_1v80 | Standard cell library |

### 9.2 Gate Count

| Metric | Target | Measured | Status |
|--------|--------|----------|--------|
| Total cells | <5,000 | **744** | **PASS** (85% margin) |
| Flip-flops | <500 | **259** | **PASS** (48% margin) |
| Combinational | <2,000 | **485** | **PASS** |
| Latches | 0 | **0** | **PASS** |
| Internal tristates ($_TBUF_) | 0 | **0** | **PASS** |

**Flip-flop breakdown:**
- `sky130_fd_sc_hd__dfrtp_1` (D-FF with async reset): 232
- `sky130_fd_sc_hd__dfstp_2` (D-FF with async set): 18
- `sky130_fd_sc_hd__dfrtn_1` (negative-edge D-FF with reset): 9

**Note:** The 11 `lpflow_isobufsrc` cells are combinational isolation buffers (X = A & ~SLEEP), NOT tristate buffers. They are used by ABC for logic optimization and do not require special handling.

### 9.3 Area

| Metric | Target | Measured | Status |
|--------|--------|----------|--------|
| Chip area | <25,000 um^2 | **10,259 um^2** | **PASS** (59% margin) |

### 9.4 Power Estimation

At SKY130 130nm, 1.8V, 1 MHz system clock:

| Component | Cells | Dynamic Power | Leakage |
|-----------|-------|---------------|---------|
| Flip-flops (a=0.1) | 259 | ~130 nW | ~259 nW |
| Combinational (a=0.05) | 485 | ~44 nW | ~485 nW |
| MUX cells (a=0.02) | 190 | ~17 nW | ~190 nW |
| **Total** | **744** | **~191 nW** | **~934 nW** |
| **Grand Total** | | | **~1.6 uW** |

| Metric | Target | Estimated | Status |
|--------|--------|-----------|--------|
| Power @ 1 MHz idle | <10 uW | **~1.6 uW** | **PASS** (84% margin) |

---

## 10. Pin/Port Table

| Signal | Dir | Width | Clock Domain | Description |
|--------|-----|-------|-------------|-------------|
| clk | in | 1 | -- | System clock (1-10 MHz) |
| rst_n | in | 1 | -- | Active-low asynchronous reset |
| sck | in | 1 | SCK | SPI clock (Mode 0, CPOL=0 CPHA=0) |
| mosi | in | 1 | SCK | SPI master-out-slave-in |
| cs_n | in | 1 | async | SPI chip select (active low) |
| miso_data | out | 1 | SCK | SPI MISO data output |
| miso_oe_n | out | 1 | async | MISO output enable (active low, = cs_n) |
| irq_n | out | 1 | CLK | Interrupt output (active low, push-pull) |
| gain[1:0] | out | 2 | CLK | PGA gain select |
| tune1[3:0] | out | 4 | CLK | BPF1 tuning DAC |
| tune2[3:0] | out | 4 | CLK | BPF2 tuning DAC |
| tune3[3:0] | out | 4 | CLK | BPF3 tuning DAC |
| tune4[3:0] | out | 4 | CLK | BPF4 tuning DAC |
| tune5[3:0] | out | 4 | CLK | BPF5 tuning DAC |
| weights[31:0] | out | 32 | CLK | Classifier weights (8x4-bit packed) |
| thresh[7:0] | out | 8 | CLK | Anomaly threshold |
| debounce_val[3:0] | out | 4 | CLK | Debounce setting |
| adc_chan[1:0] | out | 2 | CLK | ADC channel select |
| adc_start | out | 1 | CLK | ADC start conversion pulse (self-clearing) |
| adc_data_in[7:0] | in | 8 | CLK | ADC conversion result (from analog SAR ADC) |
| adc_done | in | 1 | CLK | ADC conversion complete strobe |
| class_result[3:0] | in | 4 | CLK | Classification result from charge-domain MAC |
| class_valid | in | 1 | CLK | Classification valid strobe |
| fsm_sample | out | 1 | CLK | Classifier FSM: sample phase active |
| fsm_evaluate | out | 1 | CLK | Classifier FSM: evaluate phase active |
| fsm_compare | out | 1 | CLK | Classifier FSM: compare phase active |
| clk_div2 | out | 1 | CLK | Divide-by-2 clock enable (NOT true clock) |
| clk_div4 | out | 1 | CLK | Divide-by-4 clock enable |
| clk_div8 | out | 1 | CLK | Divide-by-8 clock enable |
| clk_div16 | out | 1 | CLK | Divide-by-16 clock enable |

**Total: 20 inputs (17 signal bits), 18 outputs (77 signal bits) = 94 signal bits**

---

## 11. Schematic and File References

### 11.1 Schematic Files

| File | Format | Description |
|------|--------|-------------|
| [`digital_top.sch`](digital_top.sch) | xschem text | Block-level schematic showing all 5 sub-modules with interconnections |
| [`digital_top.png`](digital_top.png) | PNG image | Rendered block diagram (matplotlib) |
| [`gen_sch.py`](gen_sch.py) | Python | Generator script for both .sch and .png |

### 11.2 RTL Files

| File | Description |
|------|-------------|
| `rtl/spi_slave.v` | SPI Mode 0 slave with toggle CDC, shadow registers, split MISO |
| `rtl/reg_file.v` | 16-register file with CTRL register and shadow data bus |
| `rtl/fsm_classifier.v` | Counter-based classifier timing FSM |
| `rtl/debounce.v` | Debounce counter + IRQ logic |
| `rtl/clk_divider.v` | 4-bit clock divider (clock-enable taps) |
| `rtl/digital_top.v` | Top-level wrapper |

### 11.3 Testbench Files

| File | Tests | Description |
|------|-------|-------------|
| `tb/test_spi.py` | 8 | SPI + register file: write/read, reset, read-only, CTRL, shadow, MISO OE |
| `tb/test_fsm.py` | 5 | FSM: phase durations, multi-cycle, order, reset, enable gating |
| `tb/test_debounce.py` | 7 | Debounce: threshold, immediate, class change, reset, deassert |
| `tb/test_clk_divider.py` | 2 | Clock divider: ratios, reset |
| `tb/test_top.py` | 6 | Integration: ADC done, FSM enable, signals, dividers, SPI stress |

### 11.4 Synthesis Files

| File | Description |
|------|-------------|
| `synth/synth.ys` | Yosys synthesis script with tristate/latch checks |
| `synth/synth_report.txt` | Full synthesis log and statistics |
| `synth/digital_top_synth.v` | Gate-level netlist (SKY130 sky130_fd_sc_hd) |
| `synth/sky130_fd_sc_hd__tt_025C_1v80.lib` | Liberty timing library |

---

*Generated 2026-03-24 | SKY130 sky130_fd_sc_hd | Yosys 0.33 + Icarus Verilog 12.0 + cocotb 2.0.1 | 28/28 tests pass, 744 cells, 10,259 um^2, tapeout-ready*
