`timescale 1ns / 1ps
// =============================================================================
// fsm_classifier.v — Classifier Timing FSM for VibroSense-1
// =============================================================================
// Generates sample/evaluate/compare phase signals for the analog MAC.
// Counter-based (no state register). Parameterized phase durations.
// Total period = SAMPLE_CYCLES + EVAL_CYCLES + COMP_CYCLES + WAIT_CYCLES.
// =============================================================================

module fsm_classifier #(
    parameter SAMPLE_CYCLES = 64,
    parameter EVAL_CYCLES   = 128,
    parameter COMP_CYCLES   = 4,
    parameter WAIT_CYCLES   = 804,
    parameter CNT_WIDTH     = 10   // ceil(log2(SAMPLE+EVAL+COMP+WAIT))
) (
    input  wire clk,
    input  wire rst_n,
    input  wire enable,         // FSM enable (always-on after config)

    output wire fsm_sample,     // high during SAMPLE phase
    output wire fsm_evaluate,   // high during EVALUATE phase
    output wire fsm_compare,    // high during COMPARE phase
    output wire fsm_done        // 1-clk pulse at end of COMPARE
);

    // Phase boundaries (combinational constants)
    localparam [CNT_WIDTH-1:0] SAMPLE_END  = SAMPLE_CYCLES - 1;
    localparam [CNT_WIDTH-1:0] EVAL_START  = SAMPLE_CYCLES;
    localparam [CNT_WIDTH-1:0] EVAL_END    = SAMPLE_CYCLES + EVAL_CYCLES - 1;
    localparam [CNT_WIDTH-1:0] COMP_START  = SAMPLE_CYCLES + EVAL_CYCLES;
    localparam [CNT_WIDTH-1:0] COMP_END    = SAMPLE_CYCLES + EVAL_CYCLES + COMP_CYCLES - 1;
    localparam [CNT_WIDTH-1:0] TOTAL       = SAMPLE_CYCLES + EVAL_CYCLES + COMP_CYCLES + WAIT_CYCLES;
    localparam [CNT_WIDTH-1:0] CNT_MAX     = TOTAL - 1;

    reg [CNT_WIDTH-1:0] cnt;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt <= {CNT_WIDTH{1'b0}};
        end else if (enable) begin
            if (cnt >= CNT_MAX)
                cnt <= {CNT_WIDTH{1'b0}};
            else
                cnt <= cnt + {{(CNT_WIDTH-1){1'b0}}, 1'b1};
        end else begin
            cnt <= {CNT_WIDTH{1'b0}};
        end
    end

    // Combinational decode — force low during reset
    assign fsm_sample   = rst_n & enable & (cnt <= SAMPLE_END);
    assign fsm_evaluate = rst_n & enable & (cnt >= EVAL_START) & (cnt <= EVAL_END);
    assign fsm_compare  = rst_n & enable & (cnt >= COMP_START) & (cnt <= COMP_END);
    assign fsm_done     = rst_n & enable & (cnt == COMP_END);

endmodule
