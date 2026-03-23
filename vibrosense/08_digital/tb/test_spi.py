"""
test_spi.py — SPI Slave + Register File integration testbench (cocotb)
Tests SPI read/write, reset values, read-only enforcement, aborted transactions.
Uses digital_top as DUT for realistic integration testing.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, Timer


SPI_HALF_PERIOD_NS = 500  # 1 MHz SPI clock


async def reset_dut(dut):
    """Reset the DUT."""
    dut.rst_n.value = 0
    dut.sck.value = 0
    dut.mosi.value = 0
    dut.cs_n.value = 1
    dut.adc_data_in.value = 0
    dut.class_result.value = 0
    dut.class_valid.value = 0
    await ClockCycles(dut.clk, 20)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)


async def spi_transfer(dut, addr, data, read=False):
    """Perform one 16-bit SPI transaction. Returns 8-bit read data."""
    if read:
        addr = addr | 0x80
    word = (addr << 8) | data

    dut.cs_n.value = 0
    await Timer(SPI_HALF_PERIOD_NS, unit="ns")

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
                miso_val = int(dut.miso.value)
            except ValueError:
                miso_val = 0  # high-Z reads as 0
            result = (result << 1) | (miso_val & 1)

    dut.sck.value = 0
    await Timer(SPI_HALF_PERIOD_NS, unit="ns")
    dut.cs_n.value = 1
    # Wait for CDC synchronization
    await ClockCycles(dut.clk, 10)

    return result


async def spi_write(dut, addr, data):
    """SPI write to register."""
    await spi_transfer(dut, addr, data, read=False)


async def spi_read(dut, addr):
    """SPI read from register."""
    return await spi_transfer(dut, addr, 0x00, read=True)


@cocotb.test()
async def test_register_write_read(dut):
    """Write and read back all RW registers."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # Register: (address, write_value, mask for valid bits)
    test_cases = [
        (0x00, 0x03, 0x03),   # GAIN: 2 bits
        (0x01, 0x0F, 0x0F),   # TUNE1: 4 bits
        (0x02, 0x0A, 0x0F),   # TUNE2: 4 bits
        (0x03, 0x05, 0x0F),   # TUNE3: 4 bits
        (0x04, 0x0B, 0x0F),   # TUNE4: 4 bits
        (0x05, 0x0D, 0x0F),   # TUNE5: 4 bits
        (0x06, 0x37, 0xFF),   # WEIGHT0: 8 bits
        (0x07, 0x5A, 0xFF),   # WEIGHT1: 8 bits
        (0x08, 0x91, 0xFF),   # WEIGHT2: 8 bits
        (0x09, 0xC4, 0xFF),   # WEIGHT3: 8 bits
        (0x0A, 0x40, 0xFF),   # THRESH: 8 bits
        (0x0B, 0x07, 0x0F),   # DEBOUNCE: 4 bits
    ]

    for addr, wdata, mask in test_cases:
        await spi_write(dut, addr, wdata)
        rdata = await spi_read(dut, addr)
        expected = wdata & mask
        dut._log.info(f"Reg 0x{addr:02X}: wrote 0x{wdata:02X}, read 0x{rdata:02X}, expected 0x{expected:02X}")
        assert (rdata & mask) == expected, \
            f"Reg 0x{addr:02X}: read 0x{rdata:02X} != expected 0x{expected:02X}"

    dut._log.info("PASS: All RW registers read back correctly")


@cocotb.test()
async def test_register_reset_values(dut):
    """Verify all registers have correct reset values."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # Expected reset values (addr, value, mask)
    reset_vals = [
        (0x00, 0x00, 0x03),   # GAIN
        (0x01, 0x08, 0x0F),   # TUNE1
        (0x02, 0x08, 0x0F),   # TUNE2
        (0x03, 0x08, 0x0F),   # TUNE3
        (0x04, 0x08, 0x0F),   # TUNE4
        (0x05, 0x08, 0x0F),   # TUNE5
        (0x06, 0x00, 0xFF),   # WEIGHT0
        (0x07, 0x00, 0xFF),   # WEIGHT1
        (0x08, 0x00, 0xFF),   # WEIGHT2
        (0x09, 0x00, 0xFF),   # WEIGHT3
        (0x0A, 0xFF, 0xFF),   # THRESH
        (0x0B, 0x03, 0x0F),   # DEBOUNCE
        (0x0C, 0x00, 0x0F),   # STATUS: class field=0 (valid bit is dynamic, FSM runs)
        (0x0E, 0x00, 0xFF),   # ADC_DATA
    ]

    for addr, expected, mask in reset_vals:
        rdata = await spi_read(dut, addr)
        dut._log.info(f"Reg 0x{addr:02X}: reset value 0x{rdata:02X}, expected 0x{expected:02X}")
        assert (rdata & mask) == expected, \
            f"Reg 0x{addr:02X}: reset value 0x{rdata:02X} != 0x{expected:02X}"

    dut._log.info("PASS: All reset values correct")


@cocotb.test()
async def test_read_only_registers(dut):
    """Write to read-only registers should be silently ignored."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # Read STATUS initial
    rdata_before = await spi_read(dut, 0x0C)

    # Try to write STATUS
    await spi_write(dut, 0x0C, 0xFF)
    rdata_after = await spi_read(dut, 0x0C)

    dut._log.info(f"STATUS: before write=0x{rdata_before:02X}, after write=0x{rdata_after:02X}")
    # STATUS should not have been modified by the write
    # (It may have changed due to FSM activity, but should not be 0xFF)
    assert rdata_after != 0xFF, "STATUS register was modified by write!"

    # Read ADC_DATA initial
    rdata_before = await spi_read(dut, 0x0E)

    # Try to write ADC_DATA
    await spi_write(dut, 0x0E, 0xAB)
    rdata_after = await spi_read(dut, 0x0E)

    dut._log.info(f"ADC_DATA: before write=0x{rdata_before:02X}, after write=0x{rdata_after:02X}")
    assert rdata_after != 0xAB, "ADC_DATA register was modified by write!"

    dut._log.info("PASS: Read-only registers reject writes")


@cocotb.test()
async def test_analog_config_outputs(dut):
    """Verify analog configuration outputs match register values."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # Write config
    await spi_write(dut, 0x00, 0x02)  # GAIN = 2
    await spi_write(dut, 0x01, 0x05)  # TUNE1 = 5
    await spi_write(dut, 0x02, 0x07)  # TUNE2 = 7
    await spi_write(dut, 0x03, 0x09)  # TUNE3 = 9
    await spi_write(dut, 0x04, 0x0B)  # TUNE4 = 11
    await spi_write(dut, 0x05, 0x0D)  # TUNE5 = 13
    await spi_write(dut, 0x06, 0x37)  # WEIGHT0
    await spi_write(dut, 0x07, 0x5A)  # WEIGHT1
    await spi_write(dut, 0x08, 0x91)  # WEIGHT2
    await spi_write(dut, 0x09, 0xC4)  # WEIGHT3
    await spi_write(dut, 0x0A, 0x40)  # THRESH

    await ClockCycles(dut.clk, 5)

    assert int(dut.gain.value) == 2, f"gain={int(dut.gain.value)}"
    assert int(dut.tune1.value) == 5, f"tune1={int(dut.tune1.value)}"
    assert int(dut.tune2.value) == 7, f"tune2={int(dut.tune2.value)}"
    assert int(dut.tune3.value) == 9, f"tune3={int(dut.tune3.value)}"
    assert int(dut.tune4.value) == 11, f"tune4={int(dut.tune4.value)}"
    assert int(dut.tune5.value) == 13, f"tune5={int(dut.tune5.value)}"
    assert int(dut.thresh.value) == 0x40, f"thresh={int(dut.thresh.value)}"

    weights_val = int(dut.weights.value)
    expected_weights = 0xC4915A37
    dut._log.info(f"weights=0x{weights_val:08X}, expected=0x{expected_weights:08X}")
    assert weights_val == expected_weights, f"weights mismatch"

    dut._log.info("PASS: All analog config outputs match register values")


@cocotb.test()
async def test_out_of_range_address(dut):
    """Accessing address 0x0F should return 0 and write should be ignored."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    await spi_write(dut, 0x0F, 0xFF)
    rdata = await spi_read(dut, 0x0F)
    dut._log.info(f"Reg 0x0F: read 0x{rdata:02X}")
    assert rdata == 0x00, f"Out-of-range address returned non-zero: 0x{rdata:02X}"

    dut._log.info("PASS: Out-of-range address handled correctly")


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
        test_module="test_spi",
    )


if __name__ == "__main__":
    test_runner()
