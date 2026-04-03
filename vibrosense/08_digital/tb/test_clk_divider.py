"""
test_clk_divider.py — Clock Divider testbench (cocotb)
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles


async def reset_dut(dut):
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)


@cocotb.test()
async def test_divide_ratios(dut):
    """Verify /2, /4, /8, /16 divide ratios by counting transitions."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    cycles = 256
    div2_transitions = 0
    div4_transitions = 0
    div8_transitions = 0
    div16_transitions = 0

    prev_div2 = int(dut.clk_div2.value)
    prev_div4 = int(dut.clk_div4.value)
    prev_div8 = int(dut.clk_div8.value)
    prev_div16 = int(dut.clk_div16.value)

    for _ in range(cycles):
        await RisingEdge(dut.clk)
        d2 = int(dut.clk_div2.value)
        d4 = int(dut.clk_div4.value)
        d8 = int(dut.clk_div8.value)
        d16 = int(dut.clk_div16.value)

        if d2 != prev_div2:
            div2_transitions += 1
        if d4 != prev_div4:
            div4_transitions += 1
        if d8 != prev_div8:
            div8_transitions += 1
        if d16 != prev_div16:
            div16_transitions += 1

        prev_div2 = d2
        prev_div4 = d4
        prev_div8 = d8
        prev_div16 = d16

    # Each transition = half period, so transitions = cycles/ratio * 2 / 2 = cycles/ratio
    dut._log.info(f"div2 transitions: {div2_transitions} (expected {cycles})")
    dut._log.info(f"div4 transitions: {div4_transitions} (expected {cycles//2})")
    dut._log.info(f"div8 transitions: {div8_transitions} (expected {cycles//4})")
    dut._log.info(f"div16 transitions: {div16_transitions} (expected {cycles//8})")

    assert div2_transitions == cycles, f"div2: {div2_transitions}"
    assert div4_transitions == cycles // 2, f"div4: {div4_transitions}"
    assert div8_transitions == cycles // 4, f"div8: {div8_transitions}"
    assert div16_transitions == cycles // 8, f"div16: {div16_transitions}"

    dut._log.info("PASS: All divide ratios correct")


@cocotb.test()
async def test_reset_clears(dut):
    """Verify reset clears all divider outputs."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Run for a while
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 50)

    # Assert reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 3)

    assert int(dut.clk_div2.value) == 0
    assert int(dut.clk_div4.value) == 0
    assert int(dut.clk_div8.value) == 0
    assert int(dut.clk_div16.value) == 0

    dut._log.info("PASS: Reset clears all outputs")


def test_runner():
    import os
    from cocotb_tools.runner import get_runner

    sim = os.environ.get("SIM", "icarus")
    runner = get_runner(sim)

    rtl_dir = os.path.join(os.path.dirname(__file__), "..", "rtl")
    runner.build(
        verilog_sources=[os.path.join(rtl_dir, "clk_divider.v")],
        hdl_toplevel="clk_divider",
        always=True,
    )
    runner.test(
        hdl_toplevel="clk_divider",
        test_module="test_clk_divider",
    )


if __name__ == "__main__":
    test_runner()
