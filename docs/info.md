<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

Min/Max unit built on a 4-bit ALU. Uses the ALU's SUB operation to compare A and B (A - B gives borrow when A < B). Outputs min or max based on uio[0]: 1=min, 0=max. Pins: A on ui[3:0], B on ui[7:4], min/max select on uio[0]. Result on uo[3:0], A<B on uo[4], A=B on uo[5]. 

## How to test

Cocotb testbench with 3 tests - test_min (outputs min with a>b, a<b, a=b cases), test_max (same for max), test_minmax_all (covers edge cases). Uses asserts. Run: `cd test && make`

## External hardware

None

## GenAI tools

Used AI for help with creating testbenches using cocotb as well as some verilog code.
