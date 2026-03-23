`timescale 1ns / 1ps
// =============================================================================
// debounce.v — Debounce and IRQ Logic for VibroSense-1
// =============================================================================
// Requires N consecutive anomaly detections before asserting IRQ.
// N = debounce_val (0 = IRQ on first detection).
// Class change resets counter. IRQ deasserts on normal classification.
// =============================================================================

module debounce #(
    parameter CNT_W  = 4,   // debounce counter width
    parameter CLASS_W = 4   // classification result width
) (
    input  wire               clk,
    input  wire               rst_n,

    // From FSM
    input  wire               fsm_done,       // 1-clk pulse per classification cycle

    // From analog classifier
    input  wire [CLASS_W-1:0] class_result,   // 0=normal, nonzero=fault type
    input  wire               class_valid,    // strobe: result is valid

    // From register file
    input  wire [CNT_W-1:0]   debounce_val,   // threshold for consecutive detections
    input  wire               debounce_wr,     // pulse: DEBOUNCE register was written

    // Outputs
    output reg                irq_assert,      // 1 = anomaly confirmed
    output reg  [CLASS_W-1:0] irq_class,       // fault class that triggered IRQ
    output wire               irq_n            // active-low open-drain IRQ
);

    reg [CNT_W-1:0]   detect_count;
    reg [CLASS_W-1:0]  last_class;

    // IRQ_N: active low. In simulation, use 1'bz for deasserted (high-Z).
    // For synthesis, treat as push-pull active-low.
    assign irq_n = irq_assert ? 1'b0 : 1'b1;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            detect_count <= {CNT_W{1'b0}};
            last_class   <= {CLASS_W{1'b0}};
            irq_assert   <= 1'b0;
            irq_class    <= {CLASS_W{1'b0}};
        end else begin
            // DEBOUNCE register written: reset counter
            if (debounce_wr) begin
                detect_count <= {CNT_W{1'b0}};
            end

            // On each classification cycle completion
            if (fsm_done) begin
                if (class_result != {CLASS_W{1'b0}}) begin
                    // Anomaly detected
                    if (class_result != last_class && last_class != {CLASS_W{1'b0}}) begin
                        // Class changed (between different fault types): reset counter
                        detect_count <= {{(CNT_W-1){1'b0}}, 1'b1};
                        irq_assert   <= 1'b0;
                    end else begin
                        // Same class or first detection after normal
                        if (detect_count < {CNT_W{1'b1}}) begin
                            detect_count <= detect_count + {{(CNT_W-1){1'b0}}, 1'b1};
                        end
                    end
                    last_class <= class_result;

                    // Check threshold
                    if ((class_result == last_class || last_class == {CLASS_W{1'b0}}) &&
                        (detect_count + {{(CNT_W-1){1'b0}}, 1'b1} >= {1'b0, debounce_val})) begin
                        // Note: detect_count+1 because we increment this cycle
                        // For debounce_val=0: 0+1=1 >= 0, always true → immediate
                        // For debounce_val=3: need count+1 >= 3, so count >= 2, meaning 3rd detection
                        irq_assert <= 1'b1;
                        irq_class  <= class_result;
                    end
                end else begin
                    // Normal classification: reset everything
                    detect_count <= {CNT_W{1'b0}};
                    last_class   <= {CLASS_W{1'b0}};
                    irq_assert   <= 1'b0;
                end
            end
        end
    end

endmodule
