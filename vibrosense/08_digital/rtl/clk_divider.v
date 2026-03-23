`timescale 1ns / 1ps
// =============================================================================
// clk_divider.v — Clock Divider for VibroSense-1
// =============================================================================
// Generates divided clocks: /2, /4, /8, /16 from system clock.
// All outputs 50% duty cycle. Synchronous reset.
// =============================================================================

module clk_divider #(
    parameter DIV_WIDTH = 4    // 4-bit counter → div2, div4, div8, div16
) (
    input  wire clk,
    input  wire rst_n,
    output wire clk_div2,
    output wire clk_div4,
    output wire clk_div8,
    output wire clk_div16
);

    reg [DIV_WIDTH-1:0] cnt;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            cnt <= {DIV_WIDTH{1'b0}};
        else
            cnt <= cnt + {{(DIV_WIDTH-1){1'b0}}, 1'b1};
    end

    assign clk_div2  = cnt[0];
    assign clk_div4  = cnt[1];
    assign clk_div8  = cnt[2];
    assign clk_div16 = cnt[3];

endmodule
