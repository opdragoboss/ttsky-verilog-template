# test for min/max unit

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


def set_inputs(dut, a, b, min_select):
    dut.ui_in.value = (b << 4) | a
    dut.uio_in.value = 1 if min_select else 0


def get_output(dut):
    v = dut.uo_out.value.integer
    return (v & 0xF, (v >> 4) & 1, (v >> 5) & 1)


@cocotb.test()
async def test_min(dut):
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    set_inputs(dut, 10, 3, True)
    await ClockCycles(dut.clk, 1)
    result, a_lt_b, a_eq_b = get_output(dut)
    assert result == 3
    assert a_lt_b == 0

    set_inputs(dut, 2, 7, True)
    await ClockCycles(dut.clk, 1)
    result, a_lt_b, a_eq_b = get_output(dut)
    assert result == 2
    assert a_lt_b == 1

    set_inputs(dut, 5, 5, True)
    await ClockCycles(dut.clk, 1)
    result, a_lt_b, a_eq_b = get_output(dut)
    assert result == 5
    assert a_eq_b == 1


@cocotb.test()
async def test_max(dut):
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    set_inputs(dut, 10, 3, False)
    await ClockCycles(dut.clk, 1)
    result, a_lt_b, a_eq_b = get_output(dut)
    assert result == 10
    assert a_lt_b == 0

    set_inputs(dut, 2, 7, False)
    await ClockCycles(dut.clk, 1)
    result, a_lt_b, a_eq_b = get_output(dut)
    assert result == 7
    assert a_lt_b == 1

    set_inputs(dut, 5, 5, False)
    await ClockCycles(dut.clk, 1)
    result, a_lt_b, a_eq_b = get_output(dut)
    assert result == 5
    assert a_eq_b == 1


@cocotb.test()
async def test_minmax_all(dut):
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    tests = [
        (10, 3, True, 3),
        (10, 3, False, 10),
        (0, 15, True, 0),
        (0, 15, False, 15),
        (8, 8, True, 8),
        (8, 8, False, 8),
    ]
    for a, b, min_sel, exp in tests:
        set_inputs(dut, a, b, min_sel)
        await ClockCycles(dut.clk, 1)
        result, _, _ = get_output(dut)
        assert result == exp, f"a={a} b={b} min_sel={min_sel}: got {result}, want {exp}"
