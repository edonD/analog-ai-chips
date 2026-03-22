# Block 08 — Digital Control: Program

## Overview

Digital control block for the VibroSense-1 analog ML vibration classifier.
Implements SPI slave + register file + classifier timing FSM + debounce logic
+ clock divider. This is the only digital block in the chip — everything else
is analog. Its job is to configure the analog signal chain, orchestrate the
classifier computation, and report results to an external MCU via SPI.

---

## SOTA Context and Design Philosophy

This is a **simple peripheral controller**, not a complex digital design.
The key metrics are **correctness** and **low power**, not performance.

| Reference Design | Gates | Power | Notes |
|------------------|-------|-------|-------|
| ARM Cortex-M0 | ~12,000 | ~10 uW/MHz | Full 32-bit CPU |
| TI MSP430 core | ~8,000 | ~5 uW/MHz | 16-bit ultra-low-power |
| Simple SPI slave | ~500 | <1 uW/MHz | Shift register + control |
| Our target | <5,000 | <10 uW/MHz | SPI + regs + FSM + debounce |

Our digital block is intentionally minimal. It does NOT contain a CPU, ALU,
or instruction decoder. It is a state machine that configures analog registers
and sequences the classifier. If it exceeds 10,000 gates, something is wrong
with the design — simplify.

---

## Architecture

```
                        +------------------------------------------+
                        |           digital_top                    |
  SCK  ----+----------->|                                          |
  MOSI ----+----------->|  +------------+    +-----------+         |
  CS_N ----+----------->|  | spi_slave  |--->| reg_file  |---> config buses
  MISO <---+------------|  |            |<---|           |         |
                        |  +------------+    +-----------+         |
                        |                         |                |
  CLK  --------------->|  +------------+    +-----------+         |
  RST_N -------------->|  | clk_divider|    |  debounce |---> IRQ_N
                        |  +------------+    +-----------+         |
                        |       |                 ^                |
                        |       v                 |                |
                        |  +-----------------------------+        |
                        |  |     fsm_classifier          |        |
                        |  |  (sample/eval/compare)      |---> ctrl signals
                        |  +-----------------------------+        |
                        +------------------------------------------+
```

### Signal List (Top-Level Ports)

| Signal | Dir | Width | Description |
|--------|-----|-------|-------------|
| clk | in | 1 | System clock (1-10 MHz) |
| rst_n | in | 1 | Active-low async reset |
| sck | in | 1 | SPI clock (mode 0) |
| mosi | in | 1 | SPI master-out-slave-in |
| cs_n | in | 1 | SPI chip select (active low) |
| miso | out | 1 | SPI master-in-slave-out |
| irq_n | out | 1 | Interrupt (open-drain, active low) |
| gain | out | 2 | PGA gain select |
| tune1 | out | 4 | BPF1 tuning DAC |
| tune2 | out | 4 | BPF2 tuning DAC |
| tune3 | out | 4 | BPF3 tuning DAC |
| tune4 | out | 4 | BPF4 tuning DAC |
| tune5 | out | 4 | BPF5 tuning DAC |
| weights | out | 32 | Classifier weights (8 x 4-bit) |
| thresh | out | 8 | Anomaly threshold |
| debounce_val | out | 4 | Debounce count setting |
| adc_chan | out | 2 | ADC channel select |
| adc_start | out | 1 | ADC conversion start pulse |
| adc_data_in | in | 8 | ADC result (from analog ADC) |
| class_result | in | 4 | Classification result (from analog MAC) |
| class_valid | in | 1 | Classification result valid strobe |
| fsm_sample | out | 1 | Classifier FSM: sample phase |
| fsm_evaluate | out | 1 | Classifier FSM: evaluate (MAC active) |
| fsm_compare | out | 1 | Classifier FSM: compare phase |

---

## Sub-Block Specifications

### 1. SPI Slave (`spi_slave.v`)

**Protocol: SPI Mode 0 (CPOL=0, CPHA=0)**

- Data sampled on rising edge of SCK
- Data shifted out on falling edge of SCK
- CS_N active low — all state resets when CS_N goes high mid-transaction
- 16-bit transaction: 8-bit address + 8-bit data
- Bit 7 of address byte = R/W flag (1=read, 0=write)
- Address bits [6:0] = register address (0x00–0x0E, others ignored)

**Timing:**

```
CS_N  \_________________________________________________/
SCK    _/‾\_/‾\_/‾\_/‾\_/‾\_/‾\_/‾\_/‾\_/‾\_/‾\_/‾\_/‾\_/‾\_/‾\_/‾\_/‾\
MOSI   |A7 |A6 |A5 |A4 |A3 |A2 |A1 |A0 |D7 |D6 |D5 |D4 |D3 |D2 |D1 |D0 |
MISO   |---|---|---|---|---|---|---|---|R7 |R6 |R5 |R4 |R3 |R2 |R1 |R0 |
       |<--- address byte ----------->|<--- data byte ------------------>|
```

**Implementation details:**

- Shift register clocked by SCK (external clock domain)
- Use a 4-bit counter to track bit position (0–15)
- At bit count = 8, latch address byte, determine R/W, load read data
- At bit count = 16, if write: assert write strobe to register file
- MISO driven only during bits 8–15 of a read transaction
- MISO is high-Z when CS_N is high (directly connected to pad with tristate)
- All outputs to register file are synchronized to clk domain via 2-FF synchronizer

**Clock domain crossing:**

- SCK and clk are asynchronous
- Write data and address cross from SCK domain to clk domain via:
  - Handshake protocol: spi sets req, clk domain samples and sets ack
  - OR: 2-FF synchronizer on write strobe (simpler, adequate at <10 MHz)
- Read data: register file is in clk domain, SPI reads a snapshot latched at
  the start of the transaction (at CS_N falling edge, latch all read-eligible
  registers into SCK domain shadow registers)

**Edge cases:**

- CS_N deasserted mid-transaction: abort, no write occurs
- Back-to-back transactions: 1 SCK cycle gap minimum between CS_N assertions
- MISO contention: MISO must be high-Z within 1 ns of CS_N going high

**Gate estimate:** ~400-600 gates (shift register + counter + synchronizers)

---

### 2. Register File (`reg_file.v`)

**14 registers, addressed 0x00–0x0E:**

| Addr | Name | R/W | Width | Reset | Description |
|------|------|-----|-------|-------|-------------|
| 0x00 | GAIN | RW | 2 | 0x0 | PGA gain (0=1x, 1=4x, 2=16x, 3=64x) |
| 0x01 | TUNE1 | RW | 4 | 0x8 | BPF1 freq tuning DAC (100-500 Hz) |
| 0x02 | TUNE2 | RW | 4 | 0x8 | BPF2 freq tuning DAC (500-2000 Hz) |
| 0x03 | TUNE3 | RW | 4 | 0x8 | BPF3 freq tuning DAC (2000-5000 Hz) |
| 0x04 | TUNE4 | RW | 4 | 0x8 | BPF4 freq tuning DAC (5000-10000 Hz) |
| 0x05 | TUNE5 | RW | 4 | 0x8 | BPF5 freq tuning DAC (10000+ Hz) |
| 0x06 | WEIGHT0 | RW | 8 | 0x00 | Classifier weights 0-1 (2 x 4-bit) |
| 0x07 | WEIGHT1 | RW | 8 | 0x00 | Classifier weights 2-3 (2 x 4-bit) |
| 0x08 | WEIGHT2 | RW | 8 | 0x00 | Classifier weights 4-5 (2 x 4-bit) |
| 0x09 | WEIGHT3 | RW | 8 | 0x00 | Classifier weights 6-7 (2 x 4-bit) |
| 0x0A | THRESH | RW | 8 | 0xFF | Anomaly threshold (default = max = never trigger) |
| 0x0B | DEBOUNCE | RW | 4 | 0x3 | Consecutive detections before IRQ (default = 3) |
| 0x0C | STATUS | R | 8 | 0x00 | Classification result [3:0]=class, [7]=valid |
| 0x0D | ADC_CTRL | RW | 4 | 0x0 | [1:0]=chan, [2]=start, [3]=busy (read-only) |
| 0x0E | ADC_DATA | R | 8 | 0x00 | Last ADC conversion result |

**Implementation details:**

- Synchronous write on clk rising edge when wr_en asserted and addr matches
- Combinational read: read data available same cycle as addr (for SPI latching)
- Read-only registers (STATUS, ADC_DATA): writes are silently ignored
- ADC_CTRL[2] (start bit): self-clearing — automatically clears after 1 clk cycle
- ADC_CTRL[3] (busy bit): set by ADC interface, cleared when adc_data_in valid
- STATUS register updated from class_result input when class_valid pulses
- All RW registers have defined reset values (see table above)
- Unused bits in sub-8-bit registers read as 0

**Special behaviors:**

- Writing GAIN triggers no immediate action; PGA reads gain bus continuously
- Writing TUNE1-5 triggers no immediate action; DACs read tune bus continuously
- Writing WEIGHT0-3 takes effect on next classifier evaluation cycle
- Writing THRESH takes effect on next compare phase
- Writing DEBOUNCE resets the debounce counter to 0 (prevent stale state)
- Reading STATUS clears the valid bit (read-to-clear on bit 7)

**Gate estimate:** ~800-1200 gates (14 registers + mux + decode)

---

### 3. Classifier Timing FSM (`fsm_classifier.v`)

**Purpose:** Generate timing signals for the analog multiply-accumulate (MAC)
block. The classifier needs three phases: sample (acquire feature values),
evaluate (run MACs), and compare (check against threshold).

**State machine:**

```
         +-------+
  reset->| IDLE  |<--------------------------+
         +---+---+                            |
             | (class_enable from reg)        |
             v                                |
         +-------+                            |
         |SAMPLE |  (hold for SAMPLE_CYCLES)  |
         +---+---+                            |
             |                                |
             v                                |
         +--------+                           |
         |EVALUATE|  (hold for EVAL_CYCLES)   |
         +---+----+                           |
             |                                |
             v                                |
         +--------+                           |
         |COMPARE |  (hold for COMP_CYCLES)   |
         +---+----+                           |
             |                                |
             v                                |
         +-------+                            |
         | WAIT  |  (hold for WAIT_CYCLES)    |
         +---+---+                            |
             |                                |
             +--------------------------------+
```

**Parameters (compile-time, not runtime configurable):**

| Parameter | Default | Description |
|-----------|---------|-------------|
| SAMPLE_CYCLES | 64 | Time for analog S/H to settle (~64 us at 1 MHz) |
| EVAL_CYCLES | 128 | Time for MAC: 8 weights x 16 clocks per multiply |
| COMP_CYCLES | 4 | Time for comparator to resolve |
| WAIT_CYCLES | 804 | Remaining time to fill 1000 cycles = 1 ms period |

**Total period: 1000 clocks = 1 ms at 1 MHz = 1000 evaluations/second.**

This is much faster than the vibration phenomena we detect (bearing faults
produce signatures in the 100-10000 Hz range, but the classification rate
only needs to be ~10-100 Hz). The fast rate is intentional: it gives the
debounce filter plenty of samples to work with.

**Output signals:**

| Signal | Active during | Purpose |
|--------|---------------|---------|
| fsm_sample | SAMPLE state | Close S/H switches, acquire features |
| fsm_evaluate | EVALUATE state | Enable MAC current mirrors |
| fsm_compare | COMPARE state | Enable threshold comparator |
| fsm_done | 1 clk pulse at COMPARE->WAIT transition | Strobe to latch result |

**Implementation details:**

- Single counter (10-bit, counts 0-999) free-running when enabled
- Combinational decode of counter value into state signals
- No actual state register needed — counter IS the state
- Reset: counter = 0, all outputs low
- Enable: controlled by a bit in a register (or always-on after reset release)

**Power optimization:**

- During WAIT state, all analog control signals are low — analog blocks can
  power down their dynamic circuits (static bias remains on)
- Clock gating: fsm_evaluate and fsm_compare could gate clocks to unused
  digital logic, but at <5000 gates, clock gating overhead may exceed savings

**Gate estimate:** ~200-300 gates (10-bit counter + comparators + decode)

---

### 4. Debounce and IRQ Logic (`debounce.v`)

**Purpose:** Prevent false alarms. The analog classifier may occasionally
misclassify a single cycle due to noise. The debounce logic requires N
consecutive anomaly detections before asserting IRQ.

**Algorithm:**

```
On each fsm_done pulse:
  if class_result != 0 (anomaly detected):
    if detect_count < debounce_val:
      detect_count <= detect_count + 1
    if detect_count == debounce_val:
      irq_assert <= 1
  else (normal):
    detect_count <= 0
    irq_assert <= 0
```

**Detailed behavior:**

- `class_result` is a 4-bit classification output from the analog MAC
  - 0x0 = normal (no fault)
  - 0x1 = inner race fault
  - 0x2 = outer race fault
  - 0x3 = ball fault
  - 0x4-0xF = reserved
- `debounce_val` is a 4-bit register (0-15), value from register 0x0B
  - 0 = no debounce, IRQ on first detection
  - 1 = require 2 consecutive detections
  - N = require N+1 consecutive detections
- `irq_assert` remains asserted as long as consecutive anomaly detections
  continue. It deasserts when a normal classification occurs.
- When `irq_assert` transitions 0->1, the STATUS register captures the
  class_result value that triggered the IRQ.

**IRQ output:**

- Open-drain: irq_n is driven low when asserted, high-Z when deasserted
- External pull-up resistor on the pad (not modeled in digital RTL)
- In RTL: `assign irq_n = irq_assert ? 1'b0 : 1'bz;`
- For synthesis: use a tristate buffer cell or model as active-low push-pull
  (tristate decided at pad level)

**Edge cases:**

- Writing DEBOUNCE register resets detect_count to 0
- Reset (rst_n=0) clears detect_count and deasserts IRQ
- If debounce_val = 0, IRQ asserts on the very first anomaly detection
- If debounce_val changes while detect_count > 0: if new value < detect_count,
  IRQ asserts immediately on the next anomaly detection
- CLASS_CHANGE: if class_result changes from one non-zero value to another
  (e.g., inner race to ball fault), detect_count resets to 1. This prevents
  conflating different fault types.

**Status register update:**

- On each fsm_done: STATUS[3:0] <= class_result, STATUS[7] <= class_valid
- STATUS[7] (valid bit) is read-to-clear (cleared by SPI read of 0x0C)

**Gate estimate:** ~200-400 gates (4-bit counter + comparator + control)

---

### 5. Clock Divider (`clk_divider.v`)

**Purpose:** Generate slower clocks from the system clock for power management
and analog timing. Not all analog blocks need the full system clock rate.

**Outputs:**

| Signal | Frequency (at 1 MHz clk) | Used by |
|--------|--------------------------|---------|
| clk_div2 | 500 kHz | General slow logic |
| clk_div4 | 250 kHz | ADC timing |
| clk_div8 | 125 kHz | Not currently used (reserved) |
| clk_div16 | 62.5 kHz | Not currently used (reserved) |

**Implementation:**

- Simple ripple counter (4-bit)
- Synchronous reset
- All outputs 50% duty cycle
- No glitch protection needed (these are free-running divided clocks)

**Note:** For synthesis, these divided clocks must be declared as clock signals
in the SDC constraints file. The synthesizer must not treat them as regular
data signals or it will insert unnecessary buffers.

**Gate estimate:** ~20-40 gates (4 flip-flops)

---

### 6. Top-Level Wrapper (`digital_top.v`)

**Purpose:** Instantiate all sub-blocks and connect them.

**Implementation notes:**

- All analog interface signals directly wired to register outputs
- SPI interface: SCK used as clock for spi_slave, all other logic on clk
- Clock domain crossing between SPI and system clock handled in spi_slave
- IRQ_N directly driven by debounce block
- No internal bus — all connections are point-to-point wires
- No FIFOs, no DMA, no interrupts besides IRQ_N

---

## Synthesis Flow

### Yosys Script (`synth/synth.ys`)

```tcl
# Read all RTL
read_verilog rtl/spi_slave.v
read_verilog rtl/reg_file.v
read_verilog rtl/fsm_classifier.v
read_verilog rtl/debounce.v
read_verilog rtl/clk_divider.v
read_verilog rtl/digital_top.v

# Synthesize
synth -top digital_top

# Technology mapping to SkyWater 130nm
dfflibmap -liberty sky130_fd_sc_hd__tt_025C_1v80.lib
abc -liberty sky130_fd_sc_hd__tt_025C_1v80.lib

# Write outputs
write_verilog synth/digital_top_synth.v
stat
```

### Expected Synthesis Results

| Metric | Target | Acceptable |
|--------|--------|------------|
| Total cells | <3000 | <5000 |
| Total area | <15,000 um^2 | <25,000 um^2 |
| Max frequency | >10 MHz | >5 MHz |
| Flip-flops | ~100-150 | <200 |
| Combinational cells | ~500-800 | <1500 |

### Power Estimation

At 130nm SkyWater, rough power model:

- Dynamic: P = alpha * C * V^2 * f
- For sky130_fd_sc_hd at 1.8V, 1 MHz:
  - Per flip-flop: ~0.5 nW (alpha=0.1 typical for control logic)
  - Per combinational cell: ~0.2 nW
  - 150 FFs + 800 comb = 75 + 160 = 235 nW dynamic
- Leakage at 25C: ~1 nW per cell typical
  - 950 cells * 1 nW = 950 nW
- **Total estimated: ~1.2 uW** at 1 MHz, 25C

This is well under the 10 uW target. The digital block is NOT the power
bottleneck — the analog OTAs and bias circuits dominate power.

---

## Testbench Specifications

All testbenches use cocotb (Python). The cocotb Makefile selects Icarus Verilog
as the simulator. VCD waveforms are dumped for debugging with GTKWave.

### Test 1: SPI Register Read/Write (`tb/test_spi.py`)

**Purpose:** Verify that every register can be written and read back correctly.

**Test sequence:**

```
1. Reset DUT (rst_n=0 for 10 clocks, then release)
2. For each RW register (0x00-0x0B, 0x0D):
   a. SPI write: send address byte (bit7=0) + data byte (all 1s in valid bits)
   b. SPI read: send address byte (bit7=1) + dummy data byte
   c. Assert: read data matches written data (masked to valid bits)
3. For each RW register:
   a. SPI write: data = 0x00
   b. SPI read: verify 0x00
4. For read-only registers (0x0C, 0x0E):
   a. SPI write: data = 0xFF
   b. SPI read: verify data is NOT 0xFF (write was ignored)
5. Verify register reset values:
   a. Assert rst_n=0, release
   b. Read all registers, compare to reset value table
6. Verify out-of-range address:
   a. SPI write to 0x0F: should be silently ignored
   b. SPI read from 0x0F: should return 0x00
7. Verify CS_N abort:
   a. Start SPI write, deassert CS_N after 8 bits (mid-transaction)
   b. Read the register: verify it was NOT modified
```

**SPI bit-bang helper function:**

```python
async def spi_transfer(dut, addr, data, read=False):
    """Perform one 16-bit SPI transaction."""
    if read:
        addr |= 0x80  # set R/W bit
    word = (addr << 8) | data
    dut.cs_n.value = 0
    await ClockCycles(dut.sck, 1)  # setup time
    result = 0
    for i in range(16):
        bit = (word >> (15 - i)) & 1
        dut.mosi.value = bit
        dut.sck.value = 1
        await Timer(500, units='ns')  # half period
        if i >= 8:  # capture MISO during data phase
            result = (result << 1) | dut.miso.value.integer
        dut.sck.value = 0
        await Timer(500, units='ns')
    dut.cs_n.value = 1
    await Timer(1, units='us')  # inter-transaction gap
    return result
```

**Pass criteria:**

- All 14 registers read back correctly after write
- All reset values correct
- Read-only registers reject writes
- Aborted transactions do not modify registers
- No X or Z values on any output after reset

---

### Test 2: Classifier Timing FSM (`tb/test_fsm.py`)

**Purpose:** Verify the FSM generates correct timing for the analog classifier.

**Test sequence:**

```
1. Reset DUT
2. Wait for FSM to start cycling
3. Capture timestamps of fsm_sample, fsm_evaluate, fsm_compare, fsm_done
4. Verify:
   a. fsm_sample asserts first, held for SAMPLE_CYCLES clocks
   b. fsm_evaluate asserts next, held for EVAL_CYCLES clocks
   c. fsm_compare asserts next, held for COMP_CYCLES clocks
   d. fsm_done pulses for exactly 1 clock at end of COMPARE
   e. Total period = SAMPLE_CYCLES + EVAL_CYCLES + COMP_CYCLES + WAIT_CYCLES
   f. No overlap between sample/evaluate/compare
   g. Cycle repeats identically
5. Run for 10 full cycles, verify all 10 are identical
6. Verify reset behavior: assert rst_n mid-cycle, verify all outputs go low
7. Verify phase durations with +-0 tolerance (must be exact)
```

**Measurements to report:**

- Exact duration of each phase in clock cycles
- Total FSM period in clock cycles
- Any glitches on phase signals (check for >1 transition per phase)

**Pass criteria:**

- All phase durations match parameters exactly
- Total period = 1000 cycles
- No overlapping phases
- fsm_done is exactly 1 clock wide
- Clean reset behavior

---

### Test 3: Debounce and IRQ (`tb/test_debounce.py`)

**Purpose:** Verify the debounce logic and IRQ assertion/deassertion.

**Test sequence:**

```
1. Reset DUT
2. Configure DEBOUNCE register to 3 (require 4 consecutive detections)
3. Stimulus sequence:
   a. Inject class_result = 0 for 10 cycles — verify IRQ_N stays high
   b. Inject class_result = 1 for 3 cycles — verify IRQ_N stays high
      (only 3 detections, need 4)
   c. Inject class_result = 0 for 1 cycle — verify counter resets
   d. Inject class_result = 2 for 4 cycles — verify IRQ_N goes low on 4th
   e. Inject class_result = 2 for 5 more cycles — verify IRQ_N stays low
   f. Inject class_result = 0 for 1 cycle — verify IRQ_N goes high
4. Verify debounce_val = 0:
   a. Set DEBOUNCE register to 0
   b. Inject class_result = 1 — IRQ_N should go low immediately
5. Verify class change resets counter:
   a. Set DEBOUNCE register to 2 (need 3 consecutive)
   b. Inject class_result = 1 for 2 cycles
   c. Inject class_result = 2 for 1 cycle — counter resets
   d. Inject class_result = 2 for 2 more cycles — IRQ still not asserted
   e. Inject class_result = 2 for 1 more cycle — NOW IRQ asserts
6. Verify STATUS register captures class_result:
   a. After IRQ asserts with class_result = 2
   b. SPI read STATUS — should return 0x82 (valid + class 2)
   c. SPI read STATUS again — should return 0x02 (valid bit cleared)
7. Verify IRQ timing:
   a. IRQ must assert within 1 clk cycle of debounce threshold being met
   b. IRQ must deassert within 1 clk cycle of normal classification
```

**Pass criteria:**

- IRQ_N asserts after exactly DEBOUNCE+1 consecutive anomaly detections
  (since debounce_val=N means require N+1 detections when counting from 0)
  Wait — clarification: debounce_val=3 means require 3 consecutive. The
  register value IS the count. So detect_count must reach debounce_val.
  With debounce_val=3: first detection sets count=1, second=2, third=3=threshold, IRQ.
  With debounce_val=0: IRQ on first detection (count goes from 0 to 0, already met).
  Implementation: IRQ when detect_count >= debounce_val AND class_result != 0.
- IRQ_N deasserts within 1 clock of normal classification
- STATUS register correctly captures and clears
- Class change correctly resets counter

---

### Test 4: Integrated Top-Level (`tb/test_top.py`)

**Purpose:** End-to-end test with realistic stimulus.

**Test sequence:**

```
1. Reset DUT
2. Configure via SPI:
   a. Write GAIN = 2 (16x)
   b. Write TUNE1-5 = {0x5, 0x7, 0x9, 0xB, 0xD}
   c. Write WEIGHT0-3 = {0x37, 0x5A, 0x91, 0xC4}
   d. Write THRESH = 0x40
   e. Write DEBOUNCE = 2
3. Read back all registers, verify correct
4. Verify analog config outputs:
   a. gain == 2'b10
   b. tune1 == 4'b0101
   c. weights == 32'hC4_91_5A_37
   d. thresh == 8'h40
5. Run classifier FSM for 100 cycles with class_result = 0:
   a. Verify IRQ_N stays high entire time
   b. Verify STATUS reads 0x00 (or 0x80 if valid bit set, then clears)
6. Inject fault:
   a. Set class_result = 3 (ball fault)
   b. Wait for debounce (2 consecutive detections)
   c. Verify IRQ_N goes low
   d. Read STATUS via SPI: expect 0x83 first read, 0x03 second read
7. Clear fault:
   a. Set class_result = 0
   b. Verify IRQ_N goes high within 1 cycle
8. ADC control:
   a. Write ADC_CTRL = 0x05 (channel 1, start=1)
   b. Verify adc_start pulses for 1 clock
   c. Verify adc_chan = 1
   d. Write adc_data_in = 0xAB
   e. Read ADC_DATA via SPI: expect 0xAB
9. Stress test:
   a. Run SPI at maximum rate (back-to-back transactions)
   b. Verify no data corruption
   c. Run 1000 classifier cycles with alternating fault/normal
   d. Verify IRQ behavior is always correct
```

**Pass criteria:**

- All SPI reads return correct data
- All analog config outputs match register values
- IRQ timing is correct in all scenarios
- ADC handshake works
- No metastability or X values after reset
- Stress test passes without errors

---

## Cocotb Makefile (`tb/Makefile`)

```makefile
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES = $(PWD)/../rtl/spi_slave.v
VERILOG_SOURCES += $(PWD)/../rtl/reg_file.v
VERILOG_SOURCES += $(PWD)/../rtl/fsm_classifier.v
VERILOG_SOURCES += $(PWD)/../rtl/debounce.v
VERILOG_SOURCES += $(PWD)/../rtl/clk_divider.v
VERILOG_SOURCES += $(PWD)/../rtl/digital_top.v

TOPLEVEL = digital_top
MODULE = test_top

include $(shell cocotb-config --makefiles)/Makefile.sim
```

---

## Implementation Order

1. **reg_file.v** — simplest, foundation for everything else
2. **spi_slave.v** — needs reg_file interface defined
3. **clk_divider.v** — trivial
4. **fsm_classifier.v** — independent of SPI
5. **debounce.v** — needs fsm_done signal
6. **digital_top.v** — wire everything together
7. **Testbenches** — in order: test_spi, test_fsm, test_debounce, test_top
8. **Synthesis** — after all tests pass

---

## Coding Style Requirements

- Verilog-2005 (not SystemVerilog — Icarus Verilog and Yosys compatibility)
- No latches — all storage must be flip-flops (use `always @(posedge clk)`)
- No initial blocks (not synthesizable)
- No tri-state internal signals (only at top-level pads)
- All signals must have explicit widths (no implicit 1-bit)
- Reset: asynchronous active-low (`always @(posedge clk or negedge rst_n)`)
- Naming: lowercase_with_underscores for signals, UPPERCASE for parameters
- One module per file
- File name matches module name

---

## PASS/FAIL Summary

| Criterion | Target | Hard Fail |
|-----------|--------|-----------|
| SPI read/write all registers | correct | any mismatch |
| SPI read-only enforcement | writes ignored | write modifies read-only reg |
| FSM phase durations | exact match | off by even 1 clock |
| IRQ assertion timing | within 1 clk of threshold | >1 clk delay |
| IRQ deassertion timing | within 1 clk of normal | >1 clk delay |
| Debounce counter behavior | matches spec | any miscounting |
| Gate count (synthesized) | <5000 | >10000 |
| Power at 1 MHz | <10 uW | >10 uW |
| Max frequency | >5 MHz | <1 MHz |
| No X/Z after reset | none | any X/Z on outputs |
| No latches in synthesis | zero | any latch inferred |
