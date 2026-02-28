<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

Explain how your project works

4-bit ALU. Takes two 4-bit inputs A and B, does one of 4 ops based on 2-bit op select: 00=ADD, 01=SUB, 10=AND, 11=OR. Pins: A is ui[3:0], B is ui[7:4], op is uio[1:0]. Output: result on uo[3:0], carry/borrow on uo[4], zero flag on uo[5]. its'  combinational so it updates right away. For subtract the carry bit is actually borrow (goes high when a < b).

## How to test

Explain how to use your project

Cocotb testbench with 5 tests - one for each op plus one that hits all of them. Checks add (including 9+7 carry case), sub (including borrow), and/or with a few values. Uses asserts to pass/fail. Run: `cd test && make`

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any

None

GenAI tools

Used AI with creating testbenches using cocotb as well as some verilog code.
