`timescale 1ns / 1ps
// =============================================================================
// reg_file.v — Register File for VibroSense-1 Digital Control
// =============================================================================
// 15 registers (0x00–0x0E), synchronous write, combinational read.
// Read-only registers: STATUS (0x0C), ADC_DATA (0x0E).
// ADC_CTRL[2] (start) is self-clearing.
// STATUS[7] (valid) is read-to-clear.
// =============================================================================

module reg_file #(
    parameter ADDR_W       = 7,
    parameter DATA_W       = 8,
    parameter NUM_REGS     = 15,   // 0x00..0x0E
    // Reset defaults
    parameter GAIN_RST     = 8'h00,
    parameter TUNE_RST     = 8'h08,
    parameter WEIGHT_RST   = 8'h00,
    parameter THRESH_RST   = 8'hFF,
    parameter DEBOUNCE_RST = 8'h03,
    parameter ADC_CTRL_RST = 8'h00
) (
    input  wire                clk,
    input  wire                rst_n,

    // Write port (from SPI slave, already in clk domain)
    input  wire                wr_en,
    input  wire [ADDR_W-1:0]   wr_addr,
    input  wire [DATA_W-1:0]   wr_data,

    // Read port (combinational)
    input  wire [ADDR_W-1:0]   rd_addr,
    output reg  [DATA_W-1:0]   rd_data,

    // Status read-to-clear strobe
    input  wire                status_rd,   // pulse when SPI reads STATUS

    // Inputs from analog/external
    input  wire [3:0]          class_result,
    input  wire                class_valid,
    input  wire [DATA_W-1:0]   adc_data_in,
    input  wire                adc_done,    // pulse when ADC conversion complete

    // Configuration outputs to analog blocks
    output wire [1:0]          gain,
    output wire [3:0]          tune1,
    output wire [3:0]          tune2,
    output wire [3:0]          tune3,
    output wire [3:0]          tune4,
    output wire [3:0]          tune5,
    output wire [31:0]         weights,
    output wire [DATA_W-1:0]   thresh,
    output wire [3:0]          debounce_val,
    output wire [1:0]          adc_chan,
    output wire                adc_start,

    // Debounce reset (pulsed when DEBOUNCE reg is written)
    output reg                 debounce_wr_pulse
);

    // -------------------------------------------------------------------------
    // Register storage
    // -------------------------------------------------------------------------
    reg [DATA_W-1:0] regs [0:NUM_REGS-1];

    // ADC start self-clear register
    reg adc_start_r;

    // STATUS valid bit (read-to-clear)
    reg status_valid;

    // ADC busy flag
    reg adc_busy;

    // -------------------------------------------------------------------------
    // Write logic
    // -------------------------------------------------------------------------
    integer i;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            regs[0]  <= GAIN_RST;
            regs[1]  <= TUNE_RST;
            regs[2]  <= TUNE_RST;
            regs[3]  <= TUNE_RST;
            regs[4]  <= TUNE_RST;
            regs[5]  <= TUNE_RST;
            regs[6]  <= WEIGHT_RST;
            regs[7]  <= WEIGHT_RST;
            regs[8]  <= WEIGHT_RST;
            regs[9]  <= WEIGHT_RST;
            regs[10] <= THRESH_RST;
            regs[11] <= DEBOUNCE_RST;
            regs[12] <= 8'h00;  // STATUS
            regs[13] <= ADC_CTRL_RST;
            regs[14] <= 8'h00;  // ADC_DATA
            adc_start_r       <= 1'b0;
            status_valid      <= 1'b0;
            adc_busy          <= 1'b0;
            debounce_wr_pulse <= 1'b0;
        end else begin
            debounce_wr_pulse <= 1'b0;

            // Self-clear ADC start
            if (adc_start_r) begin
                adc_start_r    <= 1'b0;
                regs[13][2]    <= 1'b0;
            end

            // ADC done: capture data, clear busy
            if (adc_done) begin
                regs[14]    <= adc_data_in;
                adc_busy    <= 1'b0;
                regs[13][3] <= 1'b0;
            end

            // Classification result capture
            if (class_valid) begin
                regs[12][3:0] <= class_result;
                status_valid  <= 1'b1;
            end

            // Read-to-clear STATUS valid bit
            if (status_rd) begin
                status_valid <= 1'b0;
            end

            // SPI write
            if (wr_en) begin
                case (wr_addr[3:0])
                    4'h0: regs[0]  <= {6'b0, wr_data[1:0]};        // GAIN: 2 bits
                    4'h1: regs[1]  <= {4'b0, wr_data[3:0]};        // TUNE1: 4 bits
                    4'h2: regs[2]  <= {4'b0, wr_data[3:0]};        // TUNE2
                    4'h3: regs[3]  <= {4'b0, wr_data[3:0]};        // TUNE3
                    4'h4: regs[4]  <= {4'b0, wr_data[3:0]};        // TUNE4
                    4'h5: regs[5]  <= {4'b0, wr_data[3:0]};        // TUNE5
                    4'h6: regs[6]  <= wr_data;                      // WEIGHT0
                    4'h7: regs[7]  <= wr_data;                      // WEIGHT1
                    4'h8: regs[8]  <= wr_data;                      // WEIGHT2
                    4'h9: regs[9]  <= wr_data;                      // WEIGHT3
                    4'hA: regs[10] <= wr_data;                      // THRESH
                    4'hB: begin
                        regs[11]          <= {4'b0, wr_data[3:0]};  // DEBOUNCE
                        debounce_wr_pulse <= 1'b1;
                    end
                    4'hC: ;  // STATUS: read-only, ignore write
                    4'hD: begin
                        regs[13][1:0] <= wr_data[1:0];  // ADC channel
                        if (wr_data[2]) begin
                            adc_start_r    <= 1'b1;
                            regs[13][2]    <= 1'b1;
                            adc_busy       <= 1'b1;
                            regs[13][3]    <= 1'b1;
                        end
                    end
                    4'hE: ;  // ADC_DATA: read-only, ignore write
                    default: ;  // out-of-range: ignore
                endcase
            end
        end
    end

    // -------------------------------------------------------------------------
    // Read logic (combinational)
    // -------------------------------------------------------------------------
    always @(*) begin
        if (rd_addr < NUM_REGS[ADDR_W-1:0]) begin
            if (rd_addr[3:0] == 4'hC) begin
                // STATUS: compose from class_result + valid bit
                rd_data = {status_valid, 3'b0, regs[12][3:0]};
            end else if (rd_addr[3:0] == 4'hD) begin
                // ADC_CTRL: compose with busy bit
                rd_data = {4'b0, adc_busy, regs[13][2], regs[13][1:0]};
            end else begin
                rd_data = regs[rd_addr[3:0]];
            end
        end else begin
            rd_data = 8'h00;
        end
    end

    // -------------------------------------------------------------------------
    // Output assignments
    // -------------------------------------------------------------------------
    assign gain         = regs[0][1:0];
    assign tune1        = regs[1][3:0];
    assign tune2        = regs[2][3:0];
    assign tune3        = regs[3][3:0];
    assign tune4        = regs[4][3:0];
    assign tune5        = regs[5][3:0];
    assign weights      = {regs[9], regs[8], regs[7], regs[6]};
    assign thresh       = regs[10];
    assign debounce_val = regs[11][3:0];
    assign adc_chan     = regs[13][1:0];
    assign adc_start    = adc_start_r;

endmodule
