"""
test_debounce.py — Debounce and IRQ logic testbench (cocotb)
Tests: threshold behavior, class change reset, immediate mode, IRQ deassertion.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles


async def reset_dut(dut):
    dut.rst_n.value = 0
    dut.fsm_done.value = 0
    dut.class_result.value = 0
    dut.class_valid.value = 0
    dut.debounce_val.value = 3
    dut.debounce_wr.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)


async def inject_classification(dut, result, n_cycles=1):
    """Inject n classification results via fsm_done pulses."""
    for _ in range(n_cycles):
        dut.class_result.value = result
        dut.fsm_done.value = 1
        await RisingEdge(dut.clk)
        dut.fsm_done.value = 0
        await RisingEdge(dut.clk)


@cocotb.test()
async def test_no_irq_on_normal(dut):
    """IRQ should never assert when class_result=0 (normal)."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    for _ in range(20):
        await inject_classification(dut, 0)

    assert int(dut.irq_n.value) == 1, "IRQ asserted on normal classification!"
    dut._log.info("PASS: No IRQ on normal classifications")


@cocotb.test()
async def test_debounce_threshold(dut):
    """With debounce_val=3, IRQ should assert after 3 consecutive anomalies."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)
    dut.debounce_val.value = 3

    # 2 anomaly detections — not enough
    await inject_classification(dut, 1, 2)
    assert int(dut.irq_n.value) == 1, "IRQ asserted too early (after 2)"

    # 3rd detection — should trigger
    await inject_classification(dut, 1, 1)
    irq_val = int(dut.irq_n.value)
    dut._log.info(f"After 3 detections: irq_n = {irq_val}")
    assert irq_val == 0, "IRQ not asserted after 3 consecutive detections"

    dut._log.info("PASS: Debounce threshold works correctly")


@cocotb.test()
async def test_irq_deasserts_on_normal(dut):
    """IRQ should deassert when normal classification occurs."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)
    dut.debounce_val.value = 1

    # Trigger IRQ
    await inject_classification(dut, 2, 1)
    assert int(dut.irq_n.value) == 0, "IRQ didn't assert"

    # Normal classification should deassert
    await inject_classification(dut, 0, 1)
    assert int(dut.irq_n.value) == 1, "IRQ didn't deassert on normal"

    dut._log.info("PASS: IRQ deasserts on normal classification")


@cocotb.test()
async def test_debounce_zero_immediate(dut):
    """With debounce_val=0, IRQ should assert on first anomaly."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)
    dut.debounce_val.value = 0

    await inject_classification(dut, 3, 1)
    assert int(dut.irq_n.value) == 0, "IRQ not asserted immediately with debounce=0"

    dut._log.info("PASS: Immediate IRQ with debounce_val=0")


@cocotb.test()
async def test_normal_resets_counter(dut):
    """A normal result mid-sequence should reset the counter."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)
    dut.debounce_val.value = 3

    # 2 anomaly detections
    await inject_classification(dut, 1, 2)
    assert int(dut.irq_n.value) == 1, "IRQ should not be asserted yet"

    # 1 normal — resets counter
    await inject_classification(dut, 0, 1)

    # 2 more anomaly detections — not enough (counter was reset)
    await inject_classification(dut, 1, 2)
    assert int(dut.irq_n.value) == 1, "IRQ asserted despite counter reset"

    # 1 more — now 3 consecutive
    await inject_classification(dut, 1, 1)
    assert int(dut.irq_n.value) == 0, "IRQ should be asserted after 3 consecutive"

    dut._log.info("PASS: Normal classification resets counter")


@cocotb.test()
async def test_class_change_resets(dut):
    """Changing fault class resets the debounce counter."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)
    dut.debounce_val.value = 3

    # 2 detections of class 1
    await inject_classification(dut, 1, 2)
    assert int(dut.irq_n.value) == 1

    # Switch to class 2 — counter resets
    await inject_classification(dut, 2, 2)
    assert int(dut.irq_n.value) == 1, "IRQ asserted despite class change"

    # 1 more of class 2 — now 3 consecutive of class 2
    await inject_classification(dut, 2, 1)
    assert int(dut.irq_n.value) == 0, "IRQ should assert after 3 of same class"

    dut._log.info("PASS: Class change resets counter")


@cocotb.test()
async def test_debounce_wr_resets(dut):
    """Writing DEBOUNCE register resets the detection counter."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)
    dut.debounce_val.value = 3

    # Build up counter
    await inject_classification(dut, 1, 2)

    # Write to debounce register
    dut.debounce_wr.value = 1
    await RisingEdge(dut.clk)
    dut.debounce_wr.value = 0
    await RisingEdge(dut.clk)

    # 2 more detections — not enough (counter was reset)
    await inject_classification(dut, 1, 2)
    assert int(dut.irq_n.value) == 1, "IRQ asserted despite debounce_wr reset"

    dut._log.info("PASS: debounce_wr resets counter")


def test_runner():
    import os
    from cocotb_tools.runner import get_runner

    sim = os.environ.get("SIM", "icarus")
    runner = get_runner(sim)

    rtl_dir = os.path.join(os.path.dirname(__file__), "..", "rtl")
    runner.build(
        verilog_sources=[os.path.join(rtl_dir, "debounce.v")],
        hdl_toplevel="debounce",
        always=True,
    )
    runner.test(
        hdl_toplevel="debounce",
        test_module="test_debounce",
    )


if __name__ == "__main__":
    test_runner()
