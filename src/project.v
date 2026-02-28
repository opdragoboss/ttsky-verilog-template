/*
 * 4-bit ALU - Tiny Tapeout HW6
 * SPDX-License-Identifier: Apache-2.0
 *
 * Operations: ADD, SUB, AND, OR
 * Pin mapping:
 *   ui_in[3:0]  = Operand A
 *   ui_in[7:4]  = Operand B
 *   uio_in[1:0] = Operation select (00=ADD, 01=SUB, 10=AND, 11=OR)
 *   uo_out[3:0] = Result
 *   uo_out[4]   = Carry/Borrow
 *   uo_out[5]   = Zero flag
 */

`default_nettype none

module tt_um_ethan_alu (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

  wire [3:0] a = ui_in[3:0];
  wire [3:0] b = ui_in[7:4];
  wire [1:0] op = uio_in[1:0];

  wire [4:0] sum = a + b;
  wire [4:0] diff = a - b;

  reg [3:0] result;
  reg carry;
  reg zero;

  always @(*) begin
    case (op)
      2'b00: begin  // ADD
        result = sum[3:0];
        carry = sum[4];
        zero = (sum[3:0] == 0);
      end
      2'b01: begin  // SUB
        result = diff[3:0];
        carry = diff[4];  // borrow when a < b
        zero = (diff[3:0] == 0);
      end
      2'b10: begin  // AND
        result = a & b;
        carry = 0;
        zero = ((a & b) == 0);
      end
      2'b11: begin  // OR
        result = a | b;
        carry = 0;
        zero = ((a | b) == 0);
      end
      default: begin
        result = 0;
        carry = 0;
        zero = 1;
      end
    endcase
  end

  assign uo_out = {2'b0, zero, carry, result};
  assign uio_out = 0;
  assign uio_oe = 0;

  wire _unused = &{ena, clk, rst_n, uio_in[7:2], 1'b0};

endmodule
