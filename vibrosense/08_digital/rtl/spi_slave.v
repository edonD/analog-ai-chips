`timescale 1ns / 1ps
// =============================================================================
// spi_slave.v — SPI Slave Interface for VibroSense-1
// =============================================================================
// SPI Mode 0 (CPOL=0, CPHA=0). 16-bit transaction: 8-bit addr + 8-bit data.
// Address bit[7] = R/W flag (1=read, 0=write).
// Clock domain crossing: toggle-based CDC for writes (SCK→clk).
// Reads: register file rd_data sampled directly (stable in clk domain).
// =============================================================================

module spi_slave #(
    parameter ADDR_W = 7,
    parameter DATA_W = 8
) (
    // System clock domain
    input  wire               clk,
    input  wire               rst_n,

    // SPI pins
    input  wire               sck,
    input  wire               mosi,
    input  wire               cs_n,
    output wire               miso,

    // Register file interface (clk domain)
    output reg                wr_en,
    output reg  [ADDR_W-1:0]  wr_addr,
    output reg  [DATA_W-1:0]  wr_data,
    output wire [ADDR_W-1:0]  rd_addr,      // combinational from SCK domain
    input  wire [DATA_W-1:0]  rd_data,      // combinational from reg_file
    output reg                status_rd     // pulse when reading STATUS register
);

    // =========================================================================
    // SCK Domain Logic
    // =========================================================================

    reg [3:0]  bit_cnt;
    reg [7:0]  shift_in;       // 8-bit shift register (reused for addr and data)
    reg [7:0]  shift_out;      // MISO shift register
    reg        rw_flag;
    reg [6:0]  addr_latched;

    // Write completion toggle (for CDC)
    reg        wr_toggle;
    reg [6:0]  wr_addr_hold;
    reg [7:0]  wr_data_hold;

    // Read completion toggle (for status_rd CDC)
    reg        rd_toggle;
    reg        rd_is_status;

    // MISO: driven during data phase of read, tristate when CS_N high
    reg miso_bit;
    assign miso = cs_n ? 1'bz : miso_bit;

    // Read address: directly from SCK-domain addr_latched for combinational read
    assign rd_addr = addr_latched;

    // -------------------------------------------------------------------------
    // Rising edge of SCK: sample MOSI, process protocol
    // -------------------------------------------------------------------------
    always @(posedge sck or posedge cs_n) begin
        if (cs_n) begin
            bit_cnt <= 4'd0;
            rw_flag <= 1'b0;
        end else begin
            // Shift in MOSI
            shift_in <= {shift_in[6:0], mosi};
            bit_cnt  <= bit_cnt + 4'd1;

            if (bit_cnt == 4'd7) begin
                // Address byte complete (bits 0-7 shifted in)
                // shift_in[6:0] has bits A7..A1, mosi is A0
                rw_flag      <= shift_in[6];  // A7 = R/W flag
                addr_latched <= {shift_in[5:0], mosi};  // A6..A0
            end

            if (bit_cnt == 4'd15) begin
                // Data byte complete
                if (!rw_flag) begin
                    // Write transaction: capture for CDC
                    wr_addr_hold <= addr_latched;
                    wr_data_hold <= {shift_in[6:0], mosi};
                    wr_toggle    <= ~wr_toggle;
                end else begin
                    // Read transaction complete
                    rd_toggle    <= ~rd_toggle;
                    rd_is_status <= (addr_latched[3:0] == 4'hC);
                end
            end
        end
    end

    // -------------------------------------------------------------------------
    // Falling edge of SCK: shift out MISO
    // -------------------------------------------------------------------------
    // Load shift_out with read data at bit 8 (first data bit on MISO).
    // For bits 9-15, shift out remaining bits.
    always @(negedge sck or posedge cs_n) begin
        if (cs_n) begin
            miso_bit  <= 1'b0;
            shift_out <= 8'd0;
        end else begin
            if (bit_cnt == 4'd8) begin
                // Load read data (rd_data is combinational from reg_file via rd_addr)
                miso_bit  <= rd_data[7];
                shift_out <= {rd_data[6:0], 1'b0};
            end else if (bit_cnt > 4'd8 && bit_cnt <= 4'd15) begin
                miso_bit  <= shift_out[7];
                shift_out <= {shift_out[6:0], 1'b0};
            end else begin
                miso_bit <= 1'b0;
            end
        end
    end

    // =========================================================================
    // Clock Domain Crossing: SCK → clk (write path)
    // =========================================================================

    reg wr_sync1, wr_sync2, wr_sync3;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_sync1 <= 1'b0;
            wr_sync2 <= 1'b0;
            wr_sync3 <= 1'b0;
        end else begin
            wr_sync1 <= wr_toggle;
            wr_sync2 <= wr_sync1;
            wr_sync3 <= wr_sync2;
        end
    end

    wire wr_pulse = wr_sync2 ^ wr_sync3;

    // =========================================================================
    // Clock Domain Crossing: SCK → clk (read-complete for status_rd)
    // =========================================================================

    reg rd_sync1, rd_sync2, rd_sync3;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rd_sync1 <= 1'b0;
            rd_sync2 <= 1'b0;
            rd_sync3 <= 1'b0;
        end else begin
            rd_sync1 <= rd_toggle;
            rd_sync2 <= rd_sync1;
            rd_sync3 <= rd_sync2;
        end
    end

    wire rd_pulse = rd_sync2 ^ rd_sync3;

    // =========================================================================
    // Output to register file (clk domain)
    // =========================================================================

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_en     <= 1'b0;
            wr_addr   <= {ADDR_W{1'b0}};
            wr_data   <= {DATA_W{1'b0}};
            status_rd <= 1'b0;
        end else begin
            wr_en     <= 1'b0;
            status_rd <= 1'b0;

            if (wr_pulse) begin
                wr_en   <= 1'b1;
                wr_addr <= wr_addr_hold;
                wr_data <= wr_data_hold;
            end

            if (rd_pulse && rd_is_status) begin
                status_rd <= 1'b1;
            end
        end
    end

    // =========================================================================
    // Initialize toggle registers (simulation only, not synthesizable)
    // =========================================================================
    initial begin
        wr_toggle    = 1'b0;
        rd_toggle    = 1'b0;
        rd_is_status = 1'b0;
        addr_latched = 7'd0;
    end

endmodule
