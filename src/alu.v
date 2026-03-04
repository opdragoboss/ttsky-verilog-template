// 4-bit ALU submodule - used by min/max unit
// op: 00=ADD 01=SUB 10=AND 11=OR

`default_nettype none

module alu_4bit (
    input  wire [3:0] a,
    input  wire [3:0] b,
    input  wire [1:0] op,
    output wire [3:0] result,
    output wire       carry,
    output wire       zero
);

  wire [4:0] sum = a + b;
  wire [4:0] diff = a - b;

  reg [3:0] r;
  reg c, z;

  always @(*) begin
    case (op)
      2'b00: begin
        r = sum[3:0];
        c = sum[4];
        z = (sum[3:0] == 0);
      end
      2'b01: begin
        r = diff[3:0];
        c = diff[4];
        z = (diff[3:0] == 0);
      end
      2'b10: begin
        r = a & b;
        c = 0;
        z = ((a & b) == 0);
      end
      2'b11: begin
        r = a | b;
        c = 0;
        z = ((a | b) == 0);
      end
      default: begin
        r = 0;
        c = 0;
        z = 1;
      end
    endcase
  end

  assign result = r;
  assign carry = c;
  assign zero = z;

endmodule
