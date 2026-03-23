`timescale 1ns / 1ps
// =============================================================================
// digital_top.v — Top-Level Digital Control for VibroSense-1
// =============================================================================
// Instantiates: spi_slave, reg_file, fsm_classifier, debounce, clk_divider.
// All analog interface signals wired to register file outputs.
// =============================================================================

module digital_top #(
    // FSM timing parameters
    parameter SAMPLE_CYCLES = 64,
    parameter EVAL_CYCLES   = 128,
    parameter COMP_CYCLES   = 4,
    parameter WAIT_CYCLES   = 804,
    parameter FSM_CNT_WIDTH = 10
) (
    // System
    input  wire        clk,
    input  wire        rst_n,

    // SPI interface
    input  wire        sck,
    input  wire        mosi,
    input  wire        cs_n,
    output wire        miso,

    // Interrupt
    output wire        irq_n,

    // PGA configuration
    output wire [1:0]  gain,

    // BPF tuning DACs
    output wire [3:0]  tune1,
    output wire [3:0]  tune2,
    output wire [3:0]  tune3,
    output wire [3:0]  tune4,
    output wire [3:0]  tune5,

    // Classifier weights and threshold
    output wire [31:0] weights,
    output wire [7:0]  thresh,

    // Debounce setting
    output wire [3:0]  debounce_val,

    // ADC interface
    output wire [1:0]  adc_chan,
    output wire        adc_start,
    input  wire [7:0]  adc_data_in,

    // Analog classifier interface
    input  wire [3:0]  class_result,
    input  wire        class_valid,

    // Classifier FSM outputs (to analog MAC)
    output wire        fsm_sample,
    output wire        fsm_evaluate,
    output wire        fsm_compare,

    // Divided clocks
    output wire        clk_div2,
    output wire        clk_div4,
    output wire        clk_div8,
    output wire        clk_div16
);

    // =========================================================================
    // Internal wires
    // =========================================================================

    // SPI → Register File
    wire        spi_wr_en;
    wire [6:0]  spi_wr_addr;
    wire [7:0]  spi_wr_data;
    wire [6:0]  spi_rd_addr;
    wire [7:0]  rf_rd_data;
    wire        spi_status_rd;

    // Register File → Debounce
    wire [3:0]  rf_debounce_val;
    wire        rf_debounce_wr_pulse;

    // FSM
    wire        fsm_done;
    wire        fsm_enable;

    // Debounce
    wire        irq_assert;
    wire [3:0]  irq_class;

    // ADC done — directly from class_valid for simplicity (separate in real chip)
    // For now, adc_done is pulsed when ADC data is updated externally
    // We'll detect adc_data_in changes — actually, use a simple mechanism:
    // When adc_start goes high and then adc_data_in changes, that's "done"
    // For RTL: we use adc_start falling edge as a proxy (self-clearing)
    // Better: use the adc_done as the complement — tie to an external signal

    // ADC done generation: detect when adc_data_in is valid
    // In real chip, this comes from the ADC. For now, we generate it from
    // a register write to ADC_DATA (but that's read-only...).
    // Solution: add an adc_done input port. Let's connect it from outside.
    // Actually the program.md doesn't specify an adc_done pin, so we'll
    // synthesize a simple handshake: adc_start goes high for 1 cycle,
    // then after some delay, data appears on adc_data_in.
    // We detect data validity by seeing adc_start go low (which happens
    // automatically via self-clear), then assume data arrives within
    // some cycles. For simplicity, we sample adc_data_in when it changes.

    // Simple approach: always capture adc_data_in into ADC_DATA register
    // on every clock when NOT busy. This is handled in reg_file.
    // Use a delayed adc_start to generate done after a configurable delay.

    reg [3:0] adc_done_cnt;
    reg       adc_done_r;
    wire      rf_adc_start;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            adc_done_cnt <= 4'd0;
            adc_done_r   <= 1'b0;
        end else begin
            adc_done_r <= 1'b0;
            if (rf_adc_start) begin
                adc_done_cnt <= 4'd10;  // 10 cycle delay for ADC conversion
            end else if (adc_done_cnt > 4'd0) begin
                adc_done_cnt <= adc_done_cnt - 4'd1;
                if (adc_done_cnt == 4'd1) begin
                    adc_done_r <= 1'b1;
                end
            end
        end
    end

    // FSM is always enabled after reset (can be gated by a register bit if needed)
    assign fsm_enable = 1'b1;

    // =========================================================================
    // Sub-block instantiations
    // =========================================================================

    spi_slave #(
        .ADDR_W (7),
        .DATA_W (8)
    ) u_spi (
        .clk       (clk),
        .rst_n     (rst_n),
        .sck       (sck),
        .mosi      (mosi),
        .cs_n      (cs_n),
        .miso      (miso),
        .wr_en     (spi_wr_en),
        .wr_addr   (spi_wr_addr),
        .wr_data   (spi_wr_data),
        .rd_addr   (spi_rd_addr),
        .rd_data   (rf_rd_data),
        .status_rd (spi_status_rd)
    );

    reg_file #(
        .ADDR_W       (7),
        .DATA_W       (8)
    ) u_regfile (
        .clk               (clk),
        .rst_n             (rst_n),
        .wr_en             (spi_wr_en),
        .wr_addr           (spi_wr_addr),
        .wr_data           (spi_wr_data),
        .rd_addr           (spi_rd_addr),
        .rd_data           (rf_rd_data),
        .status_rd         (spi_status_rd),
        .class_result      (class_result),
        .class_valid       (fsm_done),   // latch result when FSM says done
        .adc_data_in       (adc_data_in),
        .adc_done          (adc_done_r),
        .gain              (gain),
        .tune1             (tune1),
        .tune2             (tune2),
        .tune3             (tune3),
        .tune4             (tune4),
        .tune5             (tune5),
        .weights           (weights),
        .thresh            (thresh),
        .debounce_val      (rf_debounce_val),
        .adc_chan           (adc_chan),
        .adc_start         (rf_adc_start),
        .debounce_wr_pulse (rf_debounce_wr_pulse)
    );

    assign debounce_val = rf_debounce_val;
    assign adc_start    = rf_adc_start;

    fsm_classifier #(
        .SAMPLE_CYCLES (SAMPLE_CYCLES),
        .EVAL_CYCLES   (EVAL_CYCLES),
        .COMP_CYCLES   (COMP_CYCLES),
        .WAIT_CYCLES   (WAIT_CYCLES),
        .CNT_WIDTH     (FSM_CNT_WIDTH)
    ) u_fsm (
        .clk          (clk),
        .rst_n        (rst_n),
        .enable       (fsm_enable),
        .fsm_sample   (fsm_sample),
        .fsm_evaluate (fsm_evaluate),
        .fsm_compare  (fsm_compare),
        .fsm_done     (fsm_done)
    );

    debounce #(
        .CNT_W   (4),
        .CLASS_W (4)
    ) u_debounce (
        .clk           (clk),
        .rst_n         (rst_n),
        .fsm_done      (fsm_done),
        .class_result  (class_result),
        .class_valid   (class_valid),
        .debounce_val  (rf_debounce_val),
        .debounce_wr   (rf_debounce_wr_pulse),
        .irq_assert    (irq_assert),
        .irq_class     (irq_class),
        .irq_n         (irq_n)
    );

    clk_divider #(
        .DIV_WIDTH (4)
    ) u_clkdiv (
        .clk      (clk),
        .rst_n    (rst_n),
        .clk_div2 (clk_div2),
        .clk_div4 (clk_div4),
        .clk_div8 (clk_div8),
        .clk_div16(clk_div16)
    );

endmodule
