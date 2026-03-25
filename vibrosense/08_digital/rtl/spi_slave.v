`timescale 1ns / 1ps
// =============================================================================
// spi_slave.v — SPI Slave Interface for VibroSense-1
// =============================================================================
// SPI Mode 0 (CPOL=0, CPHA=0). 16-bit transaction: 8-bit addr + 8-bit data.
// Address bit[7] = R/W flag (1=read, 0=write).
// Clock domain crossing: toggle-based CDC for writes (SCK->clk).
// Reads: shadow registers updated every CLK cycle (always fresh, no SCK:CLK constraint).
// MISO: separate miso_data + miso_oe_n outputs (no internal tristate).
//
// Reset strategy:
//   - clk-domain FFs: async reset via rst_n
//   - SCK-domain per-transaction FFs (bit_cnt, rw_flag, etc.): async reset via cs_n posedge
//   - SCK-domain persistent FFs (wr_toggle, rd_toggle, holds): async reset via rst_n
//     (rst_n is safe here because it's held asserted for many cycles at power-on,
//      long enough for all domains to see it. SCK is idle during reset.)
// Each always block has at most one async reset -> clean standard-cell mapping.
// =============================================================================

module spi_slave #(
    parameter ADDR_W = 7,
    parameter DATA_W = 8,
    parameter NUM_REGS = 16   // number of registers to shadow (0x00..0x0F)
) (
    // System clock domain
    input  wire               clk,
    input  wire               rst_n,

    // SPI pins
    input  wire               sck,
    input  wire               mosi,
    input  wire               cs_n,
    output wire               miso_data,
    output wire               miso_oe_n,    // active-low output enable

    // Register file interface (clk domain)
    output reg                wr_en,
    output reg  [ADDR_W-1:0]  wr_addr,
    output reg  [DATA_W-1:0]  wr_data,
    output reg                status_rd,     // pulse when reading STATUS register

    // Shadow register load interface (clk domain)
    input  wire [NUM_REGS*DATA_W-1:0] shadow_data_in  // flat bus of all register read values
);

    // =========================================================================
    // SCK Domain Logic
    // =========================================================================

    // Per-transaction state (reset by cs_n posedge)
    reg [3:0]  bit_cnt;
    reg [7:0]  shift_in;
    reg        rw_flag;
    reg [6:0]  addr_latched;
    reg        rd_is_status;

    // Persistent state across transactions (reset by rst_n only)
    reg        wr_toggle;
    reg [6:0]  wr_addr_hold;
    reg [7:0]  wr_data_hold;
    reg        rd_toggle;

    // MISO shift register (reset by cs_n posedge)
    reg [7:0]  shift_out;
    reg        miso_bit;

    // Shadow register buffer (clk domain write, SCK domain read)
    reg [DATA_W-1:0] shadow_regs [0:NUM_REGS-1];

    // MISO output
    assign miso_data = miso_bit;
    assign miso_oe_n = cs_n;  // output enabled (low) when cs_n is low

    // -------------------------------------------------------------------------
    // Shadow register update (clk domain) — free-running every cycle
    // -------------------------------------------------------------------------
    // Shadow buffer updates every CLK cycle so it always holds the latest
    // register values. This eliminates any SCK:CLK ratio constraint — SPI
    // reads are correct regardless of how fast SCK runs relative to CLK.
    integer si;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (si = 0; si < NUM_REGS; si = si + 1)
                shadow_regs[si] <= {DATA_W{1'b0}};
        end else begin
            for (si = 0; si < NUM_REGS; si = si + 1)
                shadow_regs[si] <= shadow_data_in[si*DATA_W +: DATA_W];
        end
    end

    // -------------------------------------------------------------------------
    // Rising edge of SCK: per-transaction state (async reset: cs_n posedge)
    // -------------------------------------------------------------------------
    always @(posedge sck or posedge cs_n) begin
        if (cs_n) begin
            bit_cnt      <= 4'd0;
            rw_flag      <= 1'b0;
            shift_in     <= 8'd0;
            addr_latched <= 7'd0;
            rd_is_status <= 1'b0;
        end else begin
            shift_in <= {shift_in[6:0], mosi};
            bit_cnt  <= bit_cnt + 4'd1;

            if (bit_cnt == 4'd7) begin
                rw_flag      <= shift_in[6];
                addr_latched <= {shift_in[5:0], mosi};
            end

            // rd_is_status is set at bit 15 for read transactions
            if (bit_cnt == 4'd15 && rw_flag) begin
                rd_is_status <= (addr_latched[3:0] == 4'hC);
            end
        end
    end

    // -------------------------------------------------------------------------
    // Rising edge of SCK: persistent CDC state (async reset: rst_n)
    // -------------------------------------------------------------------------
    // wr_toggle, rd_toggle, wr_addr_hold, wr_data_hold must survive across
    // transactions so the clk-domain synchronizers can detect the toggle.
    always @(posedge sck or negedge rst_n) begin
        if (!rst_n) begin
            wr_toggle    <= 1'b0;
            rd_toggle    <= 1'b0;
            wr_addr_hold <= 7'd0;
            wr_data_hold <= 8'd0;
        end else if (!cs_n) begin
            // Only active during transaction (cs_n low)
            if (bit_cnt == 4'd15) begin
                if (!rw_flag) begin
                    wr_addr_hold <= addr_latched;
                    wr_data_hold <= {shift_in[6:0], mosi};
                    wr_toggle    <= ~wr_toggle;
                end else begin
                    rd_toggle    <= ~rd_toggle;
                end
            end
        end
    end

    // -------------------------------------------------------------------------
    // Falling edge of SCK: shift out MISO (async reset: cs_n posedge)
    // -------------------------------------------------------------------------
    wire [DATA_W-1:0] shadow_rd_data;
    assign shadow_rd_data = (addr_latched < NUM_REGS[6:0]) ?
                            shadow_regs[addr_latched[3:0]] : {DATA_W{1'b0}};

    always @(negedge sck or posedge cs_n) begin
        if (cs_n) begin
            miso_bit  <= 1'b0;
            shift_out <= 8'd0;
        end else begin
            if (bit_cnt == 4'd8) begin
                miso_bit  <= shadow_rd_data[7];
                shift_out <= {shadow_rd_data[6:0], 1'b0};
            end else if (bit_cnt > 4'd8 && bit_cnt <= 4'd15) begin
                miso_bit  <= shift_out[7];
                shift_out <= {shift_out[6:0], 1'b0};
            end else begin
                miso_bit <= 1'b0;
            end
        end
    end

    // =========================================================================
    // Clock Domain Crossing: SCK -> clk (write path)
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
    // Clock Domain Crossing: SCK -> clk (read-complete for status_rd)
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

endmodule
