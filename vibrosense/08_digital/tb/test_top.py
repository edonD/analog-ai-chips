"""
test_top.py — Integrated top-level testbench (cocotb)
End-to-end test: SPI config -> FSM enable -> fault injection -> IRQ -> ADC done pin.
Tests: full integration, FSM signals, clock dividers, SPI stress,
       FSM enable/disable via CTRL register, ADC done pin functionality.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, Timer


SPI_HALF_PERIOD_NS = 500


async def reset_dut(dut):
    dut.rst_n.value = 0
    dut.sck.value = 0
    dut.mosi.value = 0
    dut.cs_n.value = 1
    dut.adc_data_in.value = 0
    dut.adc_done.value = 0
    dut.class_result.value = 0
    dut.class_valid.value = 0
    await ClockCycles(dut.clk, 20)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)


async def spi_transfer(dut, addr, data, read=False):
    if read:
        addr = addr | 0x80
    word = (addr << 8) | data

    dut.cs_n.value = 0
    await Timer(SPI_HALF_PERIOD_NS, unit="ns")
    await ClockCycles(dut.clk, 5)  # shadow snapshot

    result = 0
    for i in range(16):
        bit = (word >> (15 - i)) & 1
        dut.mosi.value = bit
        dut.sck.value = 0
        await Timer(SPI_HALF_PERIOD_NS, unit="ns")
        dut.sck.value = 1
        await Timer(SPI_HALF_PERIOD_NS, unit="ns")
        if i >= 8:
            try:
                miso_val = int(dut.miso_data.value)
            except ValueError:
                miso_val = 0
            result = (result << 1) | (miso_val & 1)

    dut.sck.value = 0
    await Timer(SPI_HALF_PERIOD_NS, unit="ns")
    dut.cs_n.value = 1
    await ClockCycles(dut.clk, 10)
    return result


async def spi_write(dut, addr, data):
    await spi_transfer(dut, addr, data, read=False)


async def spi_read(dut, addr):
    return await spi_transfer(dut, addr, 0x00, read=True)


@cocotb.test()
async def test_full_integration(dut):
    """Full integration test: config -> enable FSM -> run -> fault -> IRQ -> clear."""
    clock = Clock(dut.clk, 10, unit="ns")  # 100 MHz
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # Step 1: Configure via SPI
    dut._log.info("Step 1: Configure via SPI")
    await spi_write(dut, 0x00, 0x02)   # GAIN = 16x
    await spi_write(dut, 0x01, 0x05)   # TUNE1
    await spi_write(dut, 0x02, 0x07)   # TUNE2
    await spi_write(dut, 0x03, 0x09)   # TUNE3
    await spi_write(dut, 0x04, 0x0B)   # TUNE4
    await spi_write(dut, 0x05, 0x0D)   # TUNE5
    await spi_write(dut, 0x06, 0x37)   # WEIGHT0
    await spi_write(dut, 0x07, 0x5A)   # WEIGHT1
    await spi_write(dut, 0x08, 0x91)   # WEIGHT2
    await spi_write(dut, 0x09, 0xC4)   # WEIGHT3
    await spi_write(dut, 0x0A, 0x40)   # THRESH
    await spi_write(dut, 0x0B, 0x02)   # DEBOUNCE = 2

    # Step 2: Enable FSM via CTRL register
    dut._log.info("Step 2: Enable FSM")
    await spi_write(dut, 0x0F, 0x01)

    # Step 3: Read back and verify
    dut._log.info("Step 3: Read back configuration")
    assert await spi_read(dut, 0x00) == 0x02
    assert await spi_read(dut, 0x01) == 0x05
    assert await spi_read(dut, 0x06) == 0x37
    assert await spi_read(dut, 0x0A) == 0x40
    assert await spi_read(dut, 0x0B) == 0x02
    assert (await spi_read(dut, 0x0F) & 0x01) == 1

    # Step 4: Verify analog outputs
    dut._log.info("Step 4: Verify analog config outputs")
    assert int(dut.gain.value) == 2
    assert int(dut.tune1.value) == 5
    assert int(dut.thresh.value) == 0x40

    # Step 5: Run classifier FSM — watch for fsm_done pulses
    dut._log.info("Step 5: Run classifier FSM with normal input")
    dut.class_result.value = 0  # normal

    done_count = 0
    for _ in range(2000):
        await RisingEdge(dut.clk)
        if int(dut.fsm_done.value) == 1:
            done_count += 1

    dut._log.info(f"  FSM done pulses in 2000 clocks: {done_count}")
    assert done_count >= 1, "FSM not generating done pulses"
    assert int(dut.irq_n.value) == 1, "IRQ asserted with normal input"

    # Step 6: Inject fault
    dut._log.info("Step 6: Inject ball fault (class=3)")
    dut.class_result.value = 3

    # Wait for debounce (need 2 consecutive detections with debounce=2)
    irq_asserted = False
    for _ in range(3000):
        await RisingEdge(dut.clk)
        if int(dut.irq_n.value) == 0:
            irq_asserted = True
            break

    assert irq_asserted, "IRQ never asserted after fault injection"
    dut._log.info("  IRQ asserted after fault injection")

    # Step 7: Read STATUS
    dut._log.info("Step 7: Read STATUS register")
    status = await spi_read(dut, 0x0C)
    dut._log.info(f"  STATUS = 0x{status:02X}")
    assert (status & 0x0F) == 3, f"STATUS class field wrong: {status & 0x0F}"

    # Step 8: Clear fault
    dut._log.info("Step 8: Clear fault")
    dut.class_result.value = 0

    # Wait for IRQ to deassert
    irq_cleared = False
    for _ in range(2000):
        await RisingEdge(dut.clk)
        if int(dut.irq_n.value) == 1:
            irq_cleared = True
            break

    assert irq_cleared, "IRQ didn't deassert after normal"
    dut._log.info("  IRQ deasserted")

    dut._log.info("PASS: Full integration test complete")


@cocotb.test()
async def test_adc_done_pin(dut):
    """Test ADC with real adc_done input pin."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # Set ADC data
    dut.adc_data_in.value = 0xAB

    # Trigger ADC start via SPI
    await spi_write(dut, 0x0D, 0x05)  # channel=1, start=1
    await ClockCycles(dut.clk, 5)

    # ADC_DATA should still be 0 (no adc_done yet)
    adc_data = await spi_read(dut, 0x0E)
    dut._log.info(f"ADC_DATA before done: 0x{adc_data:02X}")
    assert adc_data == 0x00, f"ADC_DATA captured before adc_done: 0x{adc_data:02X}"

    # Pulse adc_done
    dut.adc_done.value = 1
    await RisingEdge(dut.clk)
    dut.adc_done.value = 0
    await ClockCycles(dut.clk, 5)

    # Now ADC_DATA should be 0xAB
    adc_data = await spi_read(dut, 0x0E)
    dut._log.info(f"ADC_DATA after done: 0x{adc_data:02X}")
    assert adc_data == 0xAB, f"ADC_DATA mismatch: 0x{adc_data:02X}"

    # Verify ADC channel output
    assert int(dut.adc_chan.value) == 1, f"adc_chan={int(dut.adc_chan.value)}"

    dut._log.info("PASS: ADC done pin test complete")


@cocotb.test()
async def test_fsm_enable_disable(dut):
    """Verify FSM does not run until CTRL[0] enables it."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # FSM should be disabled by default
    saw_sample = False
    for _ in range(200):
        await RisingEdge(dut.clk)
        if int(dut.fsm_sample.value) == 1:
            saw_sample = True
            break

    assert not saw_sample, "FSM ran without CTRL enable!"
    dut._log.info("  FSM correctly idle when CTRL[0]=0")

    # Enable FSM
    await spi_write(dut, 0x0F, 0x01)

    # Need to wait up to a full FSM cycle (1000 clk) to see fsm_sample,
    # since the counter may already be past the SAMPLE phase when enable takes effect.
    saw_sample = False
    for _ in range(1100):
        await RisingEdge(dut.clk)
        if int(dut.fsm_sample.value) == 1:
            saw_sample = True
            break

    assert saw_sample, "FSM didn't start after CTRL enable"
    dut._log.info("  FSM started after CTRL[0]=1")

    # Disable FSM
    await spi_write(dut, 0x0F, 0x00)
    await ClockCycles(dut.clk, 5)

    # After disable, counter resets to 0. Check that no sample signal appears.
    saw_sample = False
    for _ in range(200):
        await RisingEdge(dut.clk)
        if int(dut.fsm_sample.value) == 1:
            saw_sample = True
            break

    assert not saw_sample, "FSM still running after CTRL disable"
    dut._log.info("PASS: FSM enable/disable via CTRL register works")


@cocotb.test()
async def test_fsm_phase_signals(dut):
    """Verify FSM sample/evaluate/compare signals are generated when enabled."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # Enable FSM
    await spi_write(dut, 0x0F, 0x01)

    saw_sample = False
    saw_evaluate = False
    saw_compare = False
    saw_done = False

    for _ in range(1100):
        await RisingEdge(dut.clk)
        if int(dut.fsm_sample.value) == 1:
            saw_sample = True
        if int(dut.fsm_evaluate.value) == 1:
            saw_evaluate = True
        if int(dut.fsm_compare.value) == 1:
            saw_compare = True
        if int(dut.fsm_done.value) == 1:
            saw_done = True

    assert saw_sample, "Never saw fsm_sample"
    assert saw_evaluate, "Never saw fsm_evaluate"
    assert saw_compare, "Never saw fsm_compare"
    assert saw_done, "Never saw fsm_done"

    dut._log.info("PASS: All FSM phase signals observed")


@cocotb.test()
async def test_clock_dividers(dut):
    """Verify divided clock outputs toggle."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    prev2 = int(dut.clk_div2.value)
    toggled = False
    for _ in range(10):
        await RisingEdge(dut.clk)
        if int(dut.clk_div2.value) != prev2:
            toggled = True
            break
        prev2 = int(dut.clk_div2.value)

    assert toggled, "clk_div2 not toggling"
    dut._log.info("PASS: Clock dividers active")


@cocotb.test()
async def test_stress_spi(dut):
    """Back-to-back SPI transactions stress test."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # Write various patterns to WEIGHT registers and read back
    patterns = [0x00, 0xFF, 0x55, 0xAA, 0x0F, 0xF0, 0x12, 0xED]
    for i, pat in enumerate(patterns):
        addr = 0x06 + (i % 4)
        await spi_write(dut, addr, pat)
        rdata = await spi_read(dut, addr)
        assert rdata == pat, f"Stress: addr=0x{addr:02X} wrote=0x{pat:02X} read=0x{rdata:02X}"

    dut._log.info("PASS: SPI stress test passed")


def test_runner():
    import os
    from cocotb_tools.runner import get_runner

    sim = os.environ.get("SIM", "icarus")
    runner = get_runner(sim)

    rtl_dir = os.path.join(os.path.dirname(__file__), "..", "rtl")
    runner.build(
        verilog_sources=[
            os.path.join(rtl_dir, "spi_slave.v"),
            os.path.join(rtl_dir, "reg_file.v"),
            os.path.join(rtl_dir, "fsm_classifier.v"),
            os.path.join(rtl_dir, "debounce.v"),
            os.path.join(rtl_dir, "clk_divider.v"),
            os.path.join(rtl_dir, "digital_top.v"),
        ],
        hdl_toplevel="digital_top",
        always=True,
    )
    runner.test(
        hdl_toplevel="digital_top",
        test_module="test_top",
    )


if __name__ == "__main__":
    test_runner()
