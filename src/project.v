// min/max unit - uses ALU (SUB) to compare A and B, outputs min or max
// A on ui[3:0], B on ui[7:4], uio[0]=1 for min / 0 for max
// output on uo[3:0], uo[4]=a_lt_b, uo[5]=a_eq_b

`default_nettype none

module tt_um_ethan_minmax (
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
  wire min_select = uio_in[0];

  wire [3:0] alu_result;
  wire borrow;
  wire zero;

  alu_4bit alu (
      .a(a),
      .b(b),
      .op(2'b01),
      .result(alu_result),
      .carry(borrow),
      .zero(zero)
  );

  // borrow = 1 means A < B -> min=A, max=B
  // borrow = 0 means A >= B -> min=B, max=A
  wire [3:0] min_val = borrow ? a : b;
  wire [3:0] max_val = borrow ? b : a;
  wire [3:0] out = min_select ? min_val : max_val;

  assign uo_out  = {2'b0, zero, borrow, out};
  assign uio_out = 0;
  assign uio_oe  = 0;

  wire _unused = &{ena, clk, rst_n, uio_in[7:1], 1'b0};

endmodule
