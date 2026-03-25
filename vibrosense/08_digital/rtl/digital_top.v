`timescale 1ns / 1ps
// =============================================================================
// digital_top.v — Top-Level Digital Control for VibroSense-1
// =============================================================================
// Instantiates: spi_slave, reg_file, fsm_classifier, debounce, clk_divider.
// All analog interface signals wired to register file outputs.
//
// Silicon-ready: no internal tristates, proper CDC with shadow registers,
// real adc_done input, FSM gated by CTRL register enable bit.
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

    // SPI interface (miso split into data + output-enable for pad-level tristate)
    input  wire        sck,
    input  wire        mosi,
    input  wire        cs_n,
    output wire        miso_data,
    output wire        miso_oe_n,

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
    input  wire        adc_done,       // real ADC done signal from analog

    // Analog classifier interface
    input  wire [3:0]  class_result,
    input  wire        class_valid,

    // Classifier FSM outputs (to analog MAC)
    output wire        fsm_sample,
    output wire        fsm_evaluate,
    output wire        fsm_compare,

    // Divided clock-enable signals (see clk_divider.v for usage notes)
    output wire        clk_div2,
    output wire        clk_div4,
    output wire        clk_div8,
    output wire        clk_div16
);

    // =========================================================================
    // Internal wires
    // =========================================================================

    // SPI -> Register File
    wire        spi_wr_en;
    wire [6:0]  spi_wr_addr;
    wire [7:0]  spi_wr_data;
    wire        spi_status_rd;

    // Shadow register data bus (16 regs x 8 bits = 128 bits)
    wire [127:0] shadow_data_bus;

    // Register File -> Debounce
    wire [3:0]  rf_debounce_val;
    wire        rf_debounce_wr_pulse;

    // FSM
    wire        fsm_done;
    wire        fsm_enable;

    // Debounce
    wire        irq_assert;
    wire [3:0]  irq_class;

    // ADC
    wire        rf_adc_start;

    // =========================================================================
    // Sub-block instantiations
    // =========================================================================

    spi_slave #(
        .ADDR_W   (7),
        .DATA_W   (8),
        .NUM_REGS (16)
    ) u_spi (
        .clk            (clk),
        .rst_n          (rst_n),
        .sck            (sck),
        .mosi           (mosi),
        .cs_n           (cs_n),
        .miso_data      (miso_data),
        .miso_oe_n      (miso_oe_n),
        .wr_en          (spi_wr_en),
        .wr_addr        (spi_wr_addr),
        .wr_data        (spi_wr_data),
        .status_rd      (spi_status_rd),
        .shadow_data_in (shadow_data_bus)
    );

    reg_file #(
        .ADDR_W       (7),
        .DATA_W       (8),
        .NUM_REGS     (16)
    ) u_regfile (
        .clk               (clk),
        .rst_n             (rst_n),
        .wr_en             (spi_wr_en),
        .wr_addr           (spi_wr_addr),
        .wr_data           (spi_wr_data),
        .shadow_data_out   (shadow_data_bus),
        .status_rd         (spi_status_rd),
        .class_result      (class_result),
        .class_valid       (fsm_done),   // latch result when FSM says done
        .adc_data_in       (adc_data_in),
        .adc_done          (adc_done),   // real ADC done from analog block
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
        .fsm_enable        (fsm_enable),
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
