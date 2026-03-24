# Digital Control Block — Silicon-Ready Hardening Program

## Context

The current RTL (6 modules, 565 cells, all 23 tests passing) is functionally correct
in simulation but has several issues that would prevent it from working in real silicon.
This program defines the fixes required to make it tapeout-ready.

---

## CRITICAL FIXES (must be resolved)

### 1. Unreset SCK-domain flip-flops in `spi_slave.v`

**Problem:** `wr_toggle`, `rd_toggle`, `addr_latched`, `wr_addr_hold`, `wr_data_hold`,
`shift_in`, `shift_out`, `rd_is_status` are initialized only via an `initial` block
(lines 187-192), which does NOT synthesize. In real silicon, these power up to random values.

If `wr_toggle` powers up at `1` while the CLK-domain `wr_sync1/2/3` are reset to `0`,
the XOR pulse generator produces a spurious `wr_pulse`, causing a garbage write to a
random register on the first clock after reset.

**Fix:** Add proper reset to all SCK-domain registers. Use `cs_n` posedge (already used
as async reset for `bit_cnt` and `rw_flag`) to also reset `wr_toggle`, `rd_toggle`,
`addr_latched`, `wr_addr_hold`, `wr_data_hold`, `shift_in`, `shift_out`, `rd_is_status`.
Alternatively, add a synchronized power-on-reset in the SCK domain. Remove the `initial`
block entirely.

### 2. Internal tristate on MISO in `spi_slave.v`

**Problem:** Line 55: `assign miso = cs_n ? 1'bz : miso_bit;` infers an internal tristate
buffer. Modern ASICs (including sky130) do not support internal tristate buses. Yosys mapped
this to `lpflow_isobufsrc` isolation cells — not proper I/O pad tristates.

**Fix:** Replace the tristate with a separate `miso_data` and `miso_oe_n` output pair.
The top-level module should export both signals, and the I/O pad handles the actual tristate.
Update `digital_top.v` ports accordingly.

### 3. SPI read path CDC violation in `spi_slave.v`

**Problem:** `rd_addr = addr_latched` (SCK domain) drives `reg_file.rd_data` which is
combinational from CLK-domain registers. The data is sampled on `negedge sck`. If a
CLK-domain register changes at the exact moment the SPI read occurs, metastability results.
This violates CDC rules and would fail Spyglass/CDC-lint.

**Fix:** Implement a shadow-register approach: on `cs_n` falling edge (start of SPI
transaction), snapshot all readable registers into a SCK-domain shadow buffer. SPI reads
then come from the shadow buffer (fully in SCK domain), eliminating the CDC crossing.
This costs ~120 FFs but is well within the 5,000-cell budget (currently at 565).

---

## MODERATE FIXES (should be resolved)

### 4. Dead `class_valid` port in `debounce.v`

**Problem:** `class_valid` is declared as an input (line 23) but never referenced in the
always block. The debounce module triggers entirely on `fsm_done`. Wasted wiring and
confusing to reviewers.

**Fix:** Remove the `class_valid` port from `debounce.v` and update the instantiation in
`digital_top.v`.

### 5. Clock divider outputs are data signals, not clocks

**Problem:** `clk_divider.v` outputs `cnt[0]` through `cnt[3]` as `clk_div2` through
`clk_div16`. These are data-path signals, not clock-tree signals. If any downstream analog
block uses them as clock inputs, they won't have proper clock tree buffering.

**Fix:** Add a comment documenting that these are clock-enable signals, not clocks. If any
downstream usage requires actual divided clocks, add proper clock gating cells
(`sky130_fd_sc_hd__dlclkp`) instead of counter taps. At minimum, document the intended
usage clearly.

### 6. ADC handshake is a 10-cycle stub in `digital_top.v`

**Problem:** Lines 114-133 fake the ADC done signal with a fixed 10-cycle timer. The
comment block (lines 92-112) is rambling and shows design uncertainty. A real SAR ADC
provides its own done signal.

**Fix:** Add a proper `adc_done` input pin to `digital_top.v`. Remove the fake timer.
Wire `adc_done` directly to the register file's `adc_done` input. Clean up the rambling
comments.

### 7. FSM has no software enable/sleep mode

**Problem:** `digital_top.v` line 136: `assign fsm_enable = 1'b1;` — the FSM runs
continuously from reset, driving sample/evaluate/compare signals to the analog MAC even
before the chip is configured.

**Fix:** Add an FSM_ENABLE bit to a control register (e.g., add a CTRL register at address
0x0F with bit 0 = FSM enable). Default to 0 (disabled). Software must explicitly enable
the FSM after configuring gains, weights, and threshold. This prevents the analog MAC from
receiving spurious timing signals during configuration.

---

## VERIFICATION REQUIREMENTS

After all fixes:

1. All existing 23 tests must still pass (no regressions)
2. Add new tests for:
   - Shadow register read consistency (SPI read returns snapshot, not live value)
   - MISO output enable behavior (`miso_oe_n` high when `cs_n` high)
   - FSM enable/disable via new CTRL register
   - ADC done input pin functionality
   - Verify no spurious writes after reset (toggle-based CDC reset correctness)
3. Re-run Yosys synthesis on sky130:
   - Gate count must remain < 5,000 (expect ~700-800 after shadow registers)
   - Zero latches
   - Zero internal tristates (verify no `lpflow_isobufsrc` in netlist)
4. Update README.md with new architecture, test results, and synthesis numbers

---

## DELIVERABLES

- [x] Fixed `spi_slave.v` — proper resets, no tristate, shadow registers
- [x] Fixed `debounce.v` — removed dead port
- [x] Fixed `digital_top.v` — real ADC done pin, FSM enable register, clean ports
- [x] New/updated testbenches covering all new functionality
- [x] Updated synthesis run with clean reports
- [x] Updated README.md documenting all changes and new results
- [x] All tests passing, committed and pushed
