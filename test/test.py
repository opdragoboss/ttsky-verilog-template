# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

"""
testbench for 4-bit ALU.
Tests ADD, SUB, AND, OR operations and flags.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


def set_inputs(dut, a, b, op):
    dut.ui_in.value = (b << 4) | a
    dut.uio_in.value = op


def get_output(dut):
    v = dut.uo_out.value.integer
    return (v & 0xF, (v >> 4) & 1, (v >> 5) & 1)


@cocotb.test()
async def test_alu_add(dut):
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    set_inputs(dut, 5, 3, 0)
    await ClockCycles(dut.clk, 1)
    result, carry, zero = get_output(dut)
    assert result == 8
    assert carry == 0
    assert zero == 0

    set_inputs(dut, 9, 7, 0)
    await ClockCycles(dut.clk, 1)
    result, carry, zero = get_output(dut)
    assert result == 0
    assert carry == 1
    assert zero == 1


@cocotb.test()
async def test_alu_sub(dut):
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    set_inputs(dut, 10, 3, 1)
    await ClockCycles(dut.clk, 1)
    result, carry, zero = get_output(dut)
    assert result == 7
    assert carry == 0

    set_inputs(dut, 3, 5, 1)
    await ClockCycles(dut.clk, 1)
    result, carry, zero = get_output(dut)
    assert result == 14
    assert carry == 1


@cocotb.test()
async def test_alu_and(dut):
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    set_inputs(dut, 0b1100, 0b1010, 2)
    await ClockCycles(dut.clk, 1)
    result, carry, zero = get_output(dut)
    assert result == 0b1000
    assert zero == 0

    set_inputs(dut, 5, 2, 2)
    await ClockCycles(dut.clk, 1)
    result, carry, zero = get_output(dut)
    assert result == 0
    assert zero == 1


@cocotb.test()
async def test_alu_or(dut):
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    set_inputs(dut, 0b1100, 0b0011, 3)
    await ClockCycles(dut.clk, 1)
    result, carry, zero = get_output(dut)
    assert result == 0b1111
    assert zero == 0

    set_inputs(dut, 0, 0, 3)
    await ClockCycles(dut.clk, 1)
    result, carry, zero = get_output(dut)
    assert result == 0
    assert zero == 1


@cocotb.test()
async def test_alu_all_ops(dut):
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    tests = [
        (7, 2, 0, 9, 0, 0),
        (7, 2, 1, 5, 0, 0),
        (7, 2, 2, 2, 0, 0),
        (7, 2, 3, 7, 0, 0),
    ]
    for a, b, op, exp_result, exp_carry, exp_zero in tests:
        set_inputs(dut, a, b, op)
        await ClockCycles(dut.clk, 1)
        result, carry, zero = get_output(dut)
        assert result == exp_result
        assert carry == exp_carry
        assert zero == exp_zero
