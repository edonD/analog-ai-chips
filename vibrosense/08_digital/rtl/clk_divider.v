`timescale 1ns / 1ps
// =============================================================================
// clk_divider.v — Clock Divider for VibroSense-1
// =============================================================================
// Generates divided clock-enable signals: /2, /4, /8, /16 from system clock.
//
// IMPORTANT: These outputs are DATA-PATH signals (counter taps), NOT true
// clock-tree signals. They toggle at the divided rate but are synchronous to
// the system clock rising edge. Use them as clock-enable qualifiers, NOT as
// clock inputs to downstream flops.
//
// If a true divided clock is needed for analog blocks, instantiate proper
// clock gating cells (e.g., sky130_fd_sc_hd__dlclkp) driven by these enables.
//
// All outputs 50% duty cycle. Synchronous reset.
// =============================================================================

module clk_divider #(
    parameter DIV_WIDTH = 4    // 4-bit counter -> div2, div4, div8, div16
) (
    input  wire clk,
    input  wire rst_n,
    output wire clk_div2,   // clock-enable at clk/2 rate
    output wire clk_div4,   // clock-enable at clk/4 rate
    output wire clk_div8,   // clock-enable at clk/8 rate
    output wire clk_div16   // clock-enable at clk/16 rate
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
