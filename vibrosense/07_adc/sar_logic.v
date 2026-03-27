// ============================================================
// VibroSense-1 Block 07: 8-bit SAR ADC — SAR Control Logic
// ============================================================
// Synchronous SAR FSM: 10 clock cycles per conversion
//   1 cycle: sample (track input)
//   8 cycles: bit decisions (MSB to LSB)
//   1 cycle: done flag
//
// Ports:
//   clk      — conversion clock (100 kHz nominal)
//   rst_n    — async reset (active low)
//   convert  — start conversion (1-cycle pulse)
//   comp_out — comparator output (1 = Vin > Vdac, 0 = Vin < Vdac)
//   dac_ctrl — 8-bit DAC switch control (1 = connect to Vref)
//   sample   — sample switch control (1 = sampling, 0 = hold)
//   result   — 8-bit ADC output
//   done     — conversion complete (1-cycle pulse)
// ============================================================
module sar_8bit (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       convert,
    input  wire       comp_out,
    output reg  [7:0] dac_ctrl,
    output reg        sample,
    output reg  [7:0] result,
    output reg        done
);

// State encoding
localparam S_IDLE   = 4'd0;
localparam S_SAMPLE = 4'd1;
localparam S_BIT7   = 4'd2;
localparam S_BIT6   = 4'd3;
localparam S_BIT5   = 4'd4;
localparam S_BIT4   = 4'd5;
localparam S_BIT3   = 4'd6;
localparam S_BIT2   = 4'd7;
localparam S_BIT1   = 4'd8;
localparam S_BIT0   = 4'd9;
localparam S_DONE   = 4'd10;

reg [3:0] state;
reg [7:0] sar_reg;  // accumulates bit decisions

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        state    <= S_IDLE;
        sample   <= 1'b1;     // track by default
        dac_ctrl <= 8'b0;
        sar_reg  <= 8'b0;
        result   <= 8'b0;
        done     <= 1'b0;
    end else begin
        done <= 1'b0;  // default: not done
        case (state)
            S_IDLE: begin
                sample   <= 1'b1;   // keep sampling / tracking
                dac_ctrl <= 8'b0;
                if (convert) begin
                    state <= S_SAMPLE;
                end
            end

            S_SAMPLE: begin
                sample   <= 1'b0;           // hold input
                sar_reg  <= 8'b0;
                dac_ctrl <= 8'b1000_0000;   // try MSB first
                state    <= S_BIT7;
            end

            S_BIT7: begin
                // Evaluate comparator result for bit 7
                if (comp_out) begin
                    sar_reg[7] <= 1'b1;             // Vin > Vdac7: keep bit
                end else begin
                    sar_reg[7] <= 1'b0;             // Vin < Vdac7: clear bit
                    dac_ctrl[7] <= 1'b0;
                end
                dac_ctrl[6] <= 1'b1;    // try bit 6
                state <= S_BIT6;
            end

            S_BIT6: begin
                if (comp_out) begin
                    sar_reg[6] <= 1'b1;
                end else begin
                    sar_reg[6] <= 1'b0;
                    dac_ctrl[6] <= 1'b0;
                end
                dac_ctrl[5] <= 1'b1;
                state <= S_BIT5;
            end

            S_BIT5: begin
                if (comp_out) begin
                    sar_reg[5] <= 1'b1;
                end else begin
                    sar_reg[5] <= 1'b0;
                    dac_ctrl[5] <= 1'b0;
                end
                dac_ctrl[4] <= 1'b1;
                state <= S_BIT4;
            end

            S_BIT4: begin
                if (comp_out) begin
                    sar_reg[4] <= 1'b1;
                end else begin
                    sar_reg[4] <= 1'b0;
                    dac_ctrl[4] <= 1'b0;
                end
                dac_ctrl[3] <= 1'b1;
                state <= S_BIT3;
            end

            S_BIT3: begin
                if (comp_out) begin
                    sar_reg[3] <= 1'b1;
                end else begin
                    sar_reg[3] <= 1'b0;
                    dac_ctrl[3] <= 1'b0;
                end
                dac_ctrl[2] <= 1'b1;
                state <= S_BIT2;
            end

            S_BIT2: begin
                if (comp_out) begin
                    sar_reg[2] <= 1'b1;
                end else begin
                    sar_reg[2] <= 1'b0;
                    dac_ctrl[2] <= 1'b0;
                end
                dac_ctrl[1] <= 1'b1;
                state <= S_BIT1;
            end

            S_BIT1: begin
                if (comp_out) begin
                    sar_reg[1] <= 1'b1;
                end else begin
                    sar_reg[1] <= 1'b0;
                    dac_ctrl[1] <= 1'b0;
                end
                dac_ctrl[0] <= 1'b1;
                state <= S_BIT0;
            end

            S_BIT0: begin
                if (comp_out) begin
                    sar_reg[0] <= 1'b1;
                end else begin
                    sar_reg[0] <= 1'b0;
                    dac_ctrl[0] <= 1'b0;
                end
                state <= S_DONE;
            end

            S_DONE: begin
                result   <= sar_reg;
                done     <= 1'b1;
                sample   <= 1'b1;   // return to track mode
                dac_ctrl <= 8'b0;   // all switches to GND
                state    <= S_IDLE;
            end

            default: state <= S_IDLE;
        endcase
    end
end

endmodule
