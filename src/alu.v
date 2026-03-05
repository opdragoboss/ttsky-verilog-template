// 4-bit ALU submodule - used by min/max unit
// op: 00=ADD 01=SUB 10=AND 11=OR
// rewritten with continuous assignments to avoid latch inference and reduce gate overhead

`default_nettype none

module alu_4bit (
    input  wire [3:0] a,
    input  wire [3:0] b,
    input  wire [1:0] op,
    output wire [3:0] result,
    output wire       carry,
    output wire       zero
);

  wire [4:0] sum  = a + b;
  wire [4:0] diff = a - b;
  wire [3:0] and_r = a & b;
  wire [3:0] or_r  = a | b;

  assign result = (op == 2'b00) ? sum[3:0]  :
                  (op == 2'b01) ? diff[3:0] :
                  (op == 2'b10) ? and_r      :
                                  or_r;

  assign carry  = (op == 2'b00) ? sum[4]  :
                  (op == 2'b01) ? diff[4] :
                  1'b0;

  assign zero = (result == 4'b0);

endmodule
