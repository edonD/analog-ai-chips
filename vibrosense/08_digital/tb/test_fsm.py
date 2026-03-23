"""
test_fsm.py — Classifier Timing FSM testbench (cocotb)
Verifies phase durations, total period, no overlap, fsm_done pulse width.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, Timer

SAMPLE_CYCLES = 64
EVAL_CYCLES   = 128
COMP_CYCLES   = 4
WAIT_CYCLES   = 804
TOTAL_CYCLES  = SAMPLE_CYCLES + EVAL_CYCLES + COMP_CYCLES + WAIT_CYCLES  # 1000


async def reset_dut(dut):
    dut.rst_n.value = 0
    dut.enable.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)


@cocotb.test()
async def test_phase_durations(dut):
    """Verify each phase lasts exactly the specified number of cycles."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # Enable FSM
    dut.enable.value = 1
    await RisingEdge(dut.clk)

    # Count cycles in each phase
    sample_count = 0
    eval_count = 0
    comp_count = 0
    wait_count = 0
    done_count = 0

    for i in range(TOTAL_CYCLES):
        await RisingEdge(dut.clk)
        s = int(dut.fsm_sample.value)
        e = int(dut.fsm_evaluate.value)
        c = int(dut.fsm_compare.value)
        d = int(dut.fsm_done.value)

        sample_count += s
        eval_count += e
        comp_count += c
        done_count += d

        if not s and not e and not c:
            wait_count += 1

        # No overlap check
        active = s + e + c
        assert active <= 1, f"Cycle {i}: overlap detected (sample={s}, eval={e}, comp={c})"

    dut._log.info(f"SAMPLE cycles: {sample_count} (expected {SAMPLE_CYCLES})")
    dut._log.info(f"EVALUATE cycles: {eval_count} (expected {EVAL_CYCLES})")
    dut._log.info(f"COMPARE cycles: {comp_count} (expected {COMP_CYCLES})")
    dut._log.info(f"WAIT cycles: {wait_count} (expected {WAIT_CYCLES})")
    dut._log.info(f"DONE pulses: {done_count} (expected 1)")

    assert sample_count == SAMPLE_CYCLES, f"SAMPLE: {sample_count} != {SAMPLE_CYCLES}"
    assert eval_count == EVAL_CYCLES, f"EVALUATE: {eval_count} != {EVAL_CYCLES}"
    assert comp_count == COMP_CYCLES, f"COMPARE: {comp_count} != {COMP_CYCLES}"
    assert wait_count == WAIT_CYCLES, f"WAIT: {wait_count} != {WAIT_CYCLES}"
    assert done_count == 1, f"DONE pulses: {done_count} != 1"

    dut._log.info("PASS: All phase durations correct")


@cocotb.test()
async def test_multiple_cycles(dut):
    """Verify FSM repeats identically for 5 cycles."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)
    dut.enable.value = 1
    await RisingEdge(dut.clk)

    done_times = []
    cycle_count = 0

    for i in range(5 * TOTAL_CYCLES):
        await RisingEdge(dut.clk)
        if int(dut.fsm_done.value) == 1:
            done_times.append(i)
            cycle_count += 1

    assert cycle_count == 5, f"Expected 5 done pulses, got {cycle_count}"

    # Check period between done pulses
    for j in range(1, len(done_times)):
        period = done_times[j] - done_times[j-1]
        assert period == TOTAL_CYCLES, f"Period {j}: {period} != {TOTAL_CYCLES}"
        dut._log.info(f"Cycle {j}: period = {period} clocks (correct)")

    dut._log.info("PASS: 5 identical cycles verified")


@cocotb.test()
async def test_phase_order(dut):
    """Verify phases occur in correct order: SAMPLE → EVALUATE → COMPARE → WAIT."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)
    dut.enable.value = 1
    await RisingEdge(dut.clk)

    last_phase = "none"
    transitions = []

    for i in range(TOTAL_CYCLES + 10):
        await RisingEdge(dut.clk)
        s = int(dut.fsm_sample.value)
        e = int(dut.fsm_evaluate.value)
        c = int(dut.fsm_compare.value)

        if s:
            phase = "sample"
        elif e:
            phase = "evaluate"
        elif c:
            phase = "compare"
        else:
            phase = "wait"

        if phase != last_phase:
            transitions.append(phase)
            last_phase = phase

    dut._log.info(f"Phase transitions: {transitions}")
    expected = ["sample", "evaluate", "compare", "wait", "sample"]
    assert transitions == expected, f"Wrong order: {transitions}"
    dut._log.info("PASS: Phase order correct")


@cocotb.test()
async def test_reset_mid_cycle(dut):
    """Assert reset mid-cycle, verify all outputs go low."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)
    dut.enable.value = 1

    # Run into EVALUATE phase
    await ClockCycles(dut.clk, SAMPLE_CYCLES + 10)

    # Assert reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)

    assert int(dut.fsm_sample.value) == 0, "sample not cleared on reset"
    assert int(dut.fsm_evaluate.value) == 0, "evaluate not cleared on reset"
    assert int(dut.fsm_compare.value) == 0, "compare not cleared on reset"
    assert int(dut.fsm_done.value) == 0, "done not cleared on reset"

    dut._log.info("PASS: Reset clears all outputs")


@cocotb.test()
async def test_enable_gating(dut):
    """Verify FSM does not run when enable=0."""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)
    dut.enable.value = 0
    await ClockCycles(dut.clk, 100)

    assert int(dut.fsm_sample.value) == 0
    assert int(dut.fsm_evaluate.value) == 0
    assert int(dut.fsm_compare.value) == 0
    assert int(dut.fsm_done.value) == 0

    dut._log.info("PASS: FSM inactive when enable=0")


def test_runner():
    """Entry point for cocotb-tools runner."""
    import os
    from cocotb_tools.runner import get_runner

    sim = os.environ.get("SIM", "icarus")
    runner = get_runner(sim)

    rtl_dir = os.path.join(os.path.dirname(__file__), "..", "rtl")
    runner.build(
        verilog_sources=[os.path.join(rtl_dir, "fsm_classifier.v")],
        hdl_toplevel="fsm_classifier",
        always=True,
    )
    runner.test(
        hdl_toplevel="fsm_classifier",
        test_module="test_fsm",
    )


if __name__ == "__main__":
    test_runner()
