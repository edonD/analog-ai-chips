#!/usr/bin/env python3
"""Generate xschem block-level schematic and PNG for digital_top.

Creates:
  - digital_top.sch  (xschem text format)
  - digital_top.png  (matplotlib block diagram)
"""

import os
import subprocess

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# ===========================================================================
# Helper state
# ===========================================================================
lines = []   # C lines (components) and T lines (text)
wires = []   # N lines
pin_id = [0]


def pid():
    pin_id[0] += 1
    return pin_id[0]


def text(x, y, s, layer=8, size=0.3):
    lines.append(f'T {{{s}}} {x} {y} 0 0 {size} {size} {{layer={layer}}}')


def iopin(x, y, rot, flip, lab):
    n = pid()
    lines.append(
        f'C {{devices/iopin.sym}} {x} {y} {rot} {flip} '
        f'{{name=p{n} lab={lab}}}'
    )


def labpin(x, y, rot, flip, lab):
    n = pid()
    lines.append(
        f'C {{devices/lab_pin.sym}} {x} {y} {rot} {flip} '
        f'{{name=p{n} lab={lab}}}'
    )


def wire(x1, y1, x2, y2, lab):
    wires.append(f'N {x1} {y1} {x2} {y2} {{lab={lab}}}')


def rect_block(x, y, w, h, name, layer=4, size=0.4):
    """Draw a rectangle using 4 wires (xschem lines) and a centred title."""
    # xschem B (box) element:  B layer x1 y1 x2 y2 {}
    lines.append(f'B {layer} {x} {y} {x+w} {y+h} {{}}')
    # Title centred inside
    tx = x + w // 2 - len(name) * 4
    ty = y + 15
    text(tx, ty, name, layer=layer, size=size)


# ===========================================================================
# Build schematic
# ===========================================================================
def build_sch():
    header = (
        "v {xschem version=3.4.4 file_version=1.2}\n"
        "G {}\nK {}\nV {}\nS {}\nE {}\n"
    )

    # -----------------------------------------------------------------------
    # Title block
    # -----------------------------------------------------------------------
    text(-200, -1100, "VibroSense Block 08: Digital Control", layer=15, size=1.0)
    text(-200, -1040, "SPI slave + 16-reg file + classifier FSM + debounce/IRQ + clk divider  |  SKY130 sky130_fd_sc_hd", layer=15, size=0.5)
    text(-200, -990, "744 cells  |  10,259 um^2  |  ~1.6 uW @ 1 MHz  |  28/28 tests PASS", layer=15, size=0.4)

    # -----------------------------------------------------------------------
    # Module boxes  (laid out left-to-right)
    # x-positions:  SPI(0), RegFile(500), FSM(1000), Debounce(1000), ClkDiv(1000)
    # -----------------------------------------------------------------------

    # SPI Slave  —  leftmost
    spi_x, spi_y = 0, -900
    spi_w, spi_h = 350, 380
    rect_block(spi_x, spi_y, spi_w, spi_h, "spi_slave")
    text(spi_x + 10, spi_y + 40, "SPI Mode 0", layer=8, size=0.25)
    text(spi_x + 10, spi_y + 65, "Toggle CDC", layer=8, size=0.25)
    text(spi_x + 10, spi_y + 90, "Shadow Registers", layer=8, size=0.25)
    text(spi_x + 10, spi_y + 115, "Split MISO", layer=8, size=0.25)

    # Register File
    rf_x, rf_y = 550, -900
    rf_w, rf_h = 350, 380
    rect_block(rf_x, rf_y, rf_w, rf_h, "reg_file")
    text(rf_x + 10, rf_y + 40, "16 x 8-bit regs", layer=8, size=0.25)
    text(rf_x + 10, rf_y + 65, "0x00-0x0F", layer=8, size=0.25)
    text(rf_x + 10, rf_y + 90, "CTRL[0]=FSM_EN", layer=8, size=0.25)
    text(rf_x + 10, rf_y + 115, "Shadow data bus", layer=8, size=0.25)

    # FSM Classifier — top-right
    fsm_x, fsm_y = 1100, -900
    fsm_w, fsm_h = 350, 170
    rect_block(fsm_x, fsm_y, fsm_w, fsm_h, "fsm_classifier")
    text(fsm_x + 10, fsm_y + 40, "Counter FSM", layer=8, size=0.25)
    text(fsm_x + 10, fsm_y + 65, "S/E/C/W phases", layer=8, size=0.25)

    # Debounce — mid-right
    deb_x, deb_y = 1100, -680
    deb_w, deb_h = 350, 170
    rect_block(deb_x, deb_y, deb_w, deb_h, "debounce")
    text(deb_x + 10, deb_y + 40, "Consecutive-match", layer=8, size=0.25)
    text(deb_x + 10, deb_y + 65, "IRQ generation", layer=8, size=0.25)

    # Clock Divider — bottom-right
    clk_x, clk_y = 1100, -460
    clk_w, clk_h = 350, 120
    rect_block(clk_x, clk_y, clk_w, clk_h, "clk_divider")
    text(clk_x + 10, clk_y + 40, "/2, /4, /8, /16", layer=8, size=0.25)
    text(clk_x + 10, clk_y + 65, "(clock enables)", layer=8, size=0.25)

    # -----------------------------------------------------------------------
    # External I/O pins (iopin.sym) on edges
    # -----------------------------------------------------------------------

    # Left-side inputs
    left_io = [
        ("sck",          -200, -880),
        ("mosi",         -200, -840),
        ("cs_n",         -200, -800),
        ("clk",          -200, -640),
        ("rst_n",        -200, -600),
        ("adc_data_in[7:0]", -200, -560),
        ("adc_done",     -200, -520),
        ("class_result[3:0]", -200, -700),
        ("class_valid",  -200, -660),
    ]
    for lab, lx, ly in left_io:
        iopin(lx, ly, 0, 1, lab)
        wire(lx, ly, spi_x, ly, lab)

    # Left-side outputs (MISO) — from SPI box left edge
    miso_io = [
        ("miso_data",  -200, -760),
        ("miso_oe_n",  -200, -720),
    ]
    for lab, lx, ly in miso_io:
        iopin(lx, ly, 0, 0, lab)
        wire(spi_x, ly, lx, ly, lab)

    # Right-side outputs
    right_x = 1650
    right_outputs_fsm = [
        ("fsm_sample",   right_x, -880),
        ("fsm_evaluate", right_x, -850),
        ("fsm_compare",  right_x, -820),
    ]
    for lab, rx, ry in right_outputs_fsm:
        iopin(rx, ry, 0, 0, lab)
        wire(fsm_x + fsm_w, ry, rx, ry, lab)

    right_outputs_deb = [
        ("irq_n", right_x, -650),
    ]
    for lab, rx, ry in right_outputs_deb:
        iopin(rx, ry, 0, 0, lab)
        wire(deb_x + deb_w, ry, rx, ry, lab)

    right_outputs_clk = [
        ("clk_div2",  right_x, -440),
        ("clk_div4",  right_x, -420),
        ("clk_div8",  right_x, -400),
        ("clk_div16", right_x, -380),
    ]
    for lab, rx, ry in right_outputs_clk:
        iopin(rx, ry, 0, 0, lab)
        wire(clk_x + clk_w, ry, rx, ry, lab)

    # Right-side outputs from reg_file (config outputs)
    config_right_x = rf_x + rf_w + 30
    config_outputs = [
        ("gain[1:0]",      right_x, -890),
        ("tune1[3:0]",     right_x, -870),
        ("tune2[3:0]",     right_x, -850),
        ("tune3[3:0]",     right_x, -830),
        ("tune4[3:0]",     right_x, -810),
        ("tune5[3:0]",     right_x, -790),
        ("weights[31:0]",  right_x, -770),
        ("thresh[7:0]",    right_x, -750),
        ("debounce_val[3:0]", right_x, -730),
        ("adc_chan[1:0]",  right_x, -710),
        ("adc_start",      right_x, -690),
    ]
    # These come out the right side of reg_file — run bus rightward
    # Use label pins at reg_file right edge, then connect to I/O
    rf_out_y_start = -870
    for idx, (lab, rx, ry) in enumerate(config_outputs):
        out_y = rf_out_y_start + idx * 20
        labpin(rf_x + rf_w, out_y, 0, 0, lab)

    # Simplify: put config iopins on right side of diagram, label pin connected
    for lab, rx, ry in config_outputs:
        iopin(rx, ry, 0, 0, lab)
        labpin(rx - 30, ry, 0, 1, lab)

    # -----------------------------------------------------------------------
    # Internal interconnections (SPI <-> RegFile)
    # -----------------------------------------------------------------------
    # SPI wr_en, wr_addr, wr_data -> reg_file
    spi_rf_signals = [
        ("spi_wr_en",       spi_x + spi_w, -860, rf_x, -860),
        ("spi_wr_addr[6:0]", spi_x + spi_w, -830, rf_x, -830),
        ("spi_wr_data[7:0]", spi_x + spi_w, -800, rf_x, -800),
        ("spi_status_rd",   spi_x + spi_w, -770, rf_x, -770),
    ]
    for lab, x1, y1, x2, y2 in spi_rf_signals:
        wire(x1, y1, x2, y2, lab)
        labpin((x1 + x2) // 2, y1 - 5, 0, 0, lab)

    # Shadow data bus (reg_file -> spi_slave, 128-bit)
    wire(rf_x, -740, spi_x + spi_w, -740, "shadow_data_bus[127:0]")
    labpin((rf_x + spi_x + spi_w) // 2, -735, 0, 0, "shadow_data_bus[127:0]")

    # snapshot_req (spi -> reg_file)
    wire(spi_x + spi_w, -710, rf_x, -710, "snapshot_req")
    labpin((spi_x + spi_w + rf_x) // 2, -705, 0, 0, "snapshot_req")

    # RegFile -> FSM (fsm_enable)
    wire(rf_x + rf_w, -600, fsm_x, -860, "fsm_enable")
    labpin(rf_x + rf_w + 50, -600, 0, 0, "fsm_enable")

    # FSM -> Debounce (fsm_done)
    wire(fsm_x + fsm_w // 2, fsm_y + fsm_h, fsm_x + fsm_w // 2, deb_y, "fsm_done")
    labpin(fsm_x + fsm_w // 2 + 5, (fsm_y + fsm_h + deb_y) // 2, 0, 0, "fsm_done")

    # RegFile -> Debounce (debounce_val, debounce_wr_pulse)
    wire(rf_x + rf_w, -630, deb_x, -630, "rf_debounce_val[3:0]")
    labpin((rf_x + rf_w + deb_x) // 2, -625, 0, 0, "rf_debounce_val[3:0]")
    wire(rf_x + rf_w, -660, deb_x, -660, "rf_debounce_wr")
    labpin((rf_x + rf_w + deb_x) // 2, -655, 0, 0, "rf_debounce_wr")

    # External signals -> Debounce (class_result routed)
    wire(spi_x, -700, spi_x - 20, -700, "class_result[3:0]")
    # Route class_result from left edge down to debounce
    wire(spi_x, -700, spi_x, -650, "class_result[3:0]")
    wire(spi_x, -650, deb_x, -650, "class_result[3:0]")
    labpin(spi_x + 200, -645, 0, 0, "class_result[3:0]")

    # clk/rst_n to all sub-blocks (just label pins, implicit connection)
    for bx, by in [(spi_x, spi_y + spi_h - 20), (rf_x, rf_y + rf_h - 20),
                    (fsm_x, fsm_y + fsm_h - 20), (deb_x, deb_y + deb_h - 20),
                    (clk_x, clk_y + clk_h - 20)]:
        labpin(bx + 5, by, 0, 1, "clk")
        labpin(bx + 5, by + 15, 0, 1, "rst_n")

    # ADC signals routed to reg_file
    wire(spi_x, -560, rf_x, -560, "adc_data_in[7:0]")
    wire(spi_x, -520, rf_x, -520, "adc_done")

    # -----------------------------------------------------------------------
    # Assemble output
    # -----------------------------------------------------------------------
    out = header
    for w in wires:
        out += w + '\n'
    for l in lines:
        out += l + '\n'
    return out


# ===========================================================================
# Matplotlib PNG block diagram
# ===========================================================================
def build_png(outpath):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    fig, ax = plt.subplots(1, 1, figsize=(20, 12))
    ax.set_xlim(-3, 19)
    ax.set_ylim(-1, 13)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(8, 12.5, "VibroSense Block 08: Digital Control", fontsize=18,
            fontweight='bold', ha='center', va='center',
            fontfamily='monospace')
    ax.text(8, 12.0, "SPI + RegFile + FSM + Debounce + ClkDiv  |  SKY130 HD  |  744 cells  |  10,259 um\u00b2  |  ~1.6 \u00b5W @ 1 MHz",
            fontsize=9, ha='center', va='center', color='#555555',
            fontfamily='monospace')

    # Outer boundary
    outer = patches.FancyBboxPatch((0, 0.5), 16, 11, boxstyle="round,pad=0.15",
                                    edgecolor='#333333', facecolor='#f8f8f0',
                                    linewidth=2.5)
    ax.add_patch(outer)
    ax.text(8, 11.2, "digital_top", fontsize=14, fontweight='bold',
            ha='center', va='center', color='#333333', fontfamily='monospace')

    def draw_module(x, y, w, h, title, details, color='#ddeeff'):
        r = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                    edgecolor='#336699', facecolor=color,
                                    linewidth=1.8)
        ax.add_patch(r)
        ax.text(x + w/2, y + h - 0.35, title, fontsize=11, fontweight='bold',
                ha='center', va='center', fontfamily='monospace', color='#1a3355')
        for i, d in enumerate(details):
            ax.text(x + w/2, y + h - 0.75 - i*0.32, d, fontsize=7.5,
                    ha='center', va='center', fontfamily='monospace', color='#555555')

    # SPI Slave
    draw_module(0.8, 6.5, 3.5, 4.0, "spi_slave", [
        "SPI Mode 0 (CPOL=0, CPHA=0)",
        "16-bit: 8-addr + 8-data",
        "Toggle-based CDC (SCK\u2192CLK)",
        "Shadow register snapshot",
        "Split MISO (data + oe_n)",
        "Per-txn reset via cs_n",
    ])

    # Register File
    draw_module(5.5, 6.5, 3.5, 4.0, "reg_file", [
        "16 \u00d7 8-bit registers",
        "Addr 0x00\u20130x0F",
        "CTRL[0] = FSM enable",
        "STATUS read-to-clear",
        "ADC start self-clear",
        "128-bit shadow bus out",
    ])

    # FSM Classifier
    draw_module(10.2, 8.5, 3.5, 2.0, "fsm_classifier", [
        "10-bit counter FSM",
        "SAMPLE(64)\u2192EVAL(128)",
        "\u2192COMPARE(4)\u2192WAIT(804)",
        "Gated by CTRL[0]",
    ])

    # Debounce
    draw_module(10.2, 5.5, 3.5, 2.5, "debounce", [
        "Consecutive-match filter",
        "Configurable threshold",
        "IRQ_N push-pull output",
        "Class result latching",
        "Counter reset on change",
    ])

    # Clock Divider
    draw_module(10.2, 3.0, 3.5, 2.0, "clk_divider", [
        "4-bit counter",
        "/2, /4, /8, /16 taps",
        "(Clock-enable signals,",
        "NOT true clock-tree)",
    ])

    # --- Arrows / connections ---
    arrow_kw = dict(arrowstyle='->', color='#336699', lw=1.5,
                    connectionstyle='arc3,rad=0')
    arrow_kw_thick = dict(arrowstyle='->', color='#cc4400', lw=2.0,
                          connectionstyle='arc3,rad=0')

    # SPI -> RegFile (write path)
    ax.annotate('', xy=(5.5, 9.2), xytext=(4.3, 9.2),
                arrowprops=arrow_kw)
    ax.text(4.9, 9.4, "wr_en/addr/data", fontsize=6.5, ha='center',
            fontfamily='monospace', color='#336699')

    # RegFile -> SPI (shadow data bus)
    ax.annotate('', xy=(4.3, 8.0), xytext=(5.5, 8.0),
                arrowprops=dict(arrowstyle='->', color='#009966', lw=2.0))
    ax.text(4.9, 7.7, "shadow[127:0]", fontsize=6.5, ha='center',
            fontfamily='monospace', color='#009966')

    # SPI -> RegFile (status_rd, snapshot_req)
    ax.annotate('', xy=(5.5, 8.6), xytext=(4.3, 8.6),
                arrowprops=arrow_kw)
    ax.text(4.9, 8.8, "status_rd / snap_req", fontsize=6, ha='center',
            fontfamily='monospace', color='#336699')

    # RegFile -> FSM (fsm_enable)
    ax.annotate('', xy=(10.2, 9.5), xytext=(9.0, 9.5),
                arrowprops=arrow_kw_thick)
    ax.text(9.6, 9.7, "fsm_enable", fontsize=6.5, ha='center',
            fontfamily='monospace', color='#cc4400')

    # FSM -> Debounce (fsm_done)
    ax.annotate('', xy=(11.95, 8.0), xytext=(11.95, 8.5),
                arrowprops=arrow_kw)
    ax.text(12.3, 8.25, "fsm_done", fontsize=6.5, ha='left',
            fontfamily='monospace', color='#336699')

    # RegFile -> Debounce (debounce_val, debounce_wr)
    ax.annotate('', xy=(10.2, 7.0), xytext=(9.0, 7.0),
                arrowprops=arrow_kw)
    ax.text(9.6, 7.2, "deb_val/wr", fontsize=6.5, ha='center',
            fontfamily='monospace', color='#336699')

    # --- Left-side external pins ---
    left_pins_in = [
        ("sck", 10.0), ("mosi", 9.6), ("cs_n", 9.2),
        ("clk", 7.2), ("rst_n", 6.8),
        ("adc_data[7:0]", 6.0), ("adc_done", 5.6),
        ("class_result[3:0]", 5.0), ("class_valid", 4.6),
    ]
    for lab, y in left_pins_in:
        ax.annotate('', xy=(0.8, y), xytext=(-0.5, y),
                    arrowprops=dict(arrowstyle='->', color='#333333', lw=1.0))
        ax.text(-0.7, y, lab, fontsize=7, ha='right', va='center',
                fontfamily='monospace', fontweight='bold', color='#1a3355')

    left_pins_out = [
        ("miso_data", 8.4), ("miso_oe_n", 8.0),
    ]
    for lab, y in left_pins_out:
        ax.annotate('', xy=(-0.5, y), xytext=(0.8, y),
                    arrowprops=dict(arrowstyle='->', color='#333333', lw=1.0))
        ax.text(-0.7, y, lab, fontsize=7, ha='right', va='center',
                fontfamily='monospace', fontweight='bold', color='#993300')

    # --- Right-side config outputs (from reg_file) ---
    config_pins = [
        ("gain[1:0]", 10.3), ("tune1-5[3:0]", 9.9),
        ("weights[31:0]", 9.5), ("thresh[7:0]", 9.1),
        ("debounce_val[3:0]", 8.7), ("adc_chan[1:0]", 8.3), ("adc_start", 7.9),
    ]
    for lab, y in config_pins:
        ax.annotate('', xy=(15.5, y), xytext=(14.0, y),
                    arrowprops=dict(arrowstyle='->', color='#333333', lw=1.0))
        ax.text(15.7, y, lab, fontsize=7, ha='left', va='center',
                fontfamily='monospace', fontweight='bold', color='#993300')
    # Connect a bus line from reg_file right edge
    ax.plot([9.0, 14.0], [9.0, 9.0], color='#336699', lw=1.0, ls='--')
    ax.plot([14.0, 14.0], [7.9, 10.3], color='#336699', lw=1.0, ls='--')

    # --- Right-side FSM outputs ---
    fsm_pins = [("fsm_sample", 9.7), ("fsm_evaluate", 9.3), ("fsm_compare", 8.9)]
    for lab, y in fsm_pins:
        ax.annotate('', xy=(15.5, y), xytext=(13.7, y),
                    arrowprops=dict(arrowstyle='->', color='#333333', lw=1.0))
        ax.text(15.7, y, lab, fontsize=7, ha='left', va='center',
                fontfamily='monospace', fontweight='bold', color='#993300')

    # Debounce output
    ax.annotate('', xy=(15.5, 6.5), xytext=(13.7, 6.5),
                arrowprops=dict(arrowstyle='->', color='#cc0000', lw=1.5))
    ax.text(15.7, 6.5, "irq_n", fontsize=8, ha='left', va='center',
            fontfamily='monospace', fontweight='bold', color='#cc0000')

    # Clock divider outputs
    clk_pins = [("clk_div2", 4.8), ("clk_div4", 4.4), ("clk_div8", 4.0), ("clk_div16", 3.6)]
    for lab, y in clk_pins:
        ax.annotate('', xy=(15.5, y), xytext=(13.7, y),
                    arrowprops=dict(arrowstyle='->', color='#333333', lw=1.0))
        ax.text(15.7, y, lab, fontsize=7, ha='left', va='center',
                fontfamily='monospace', fontweight='bold', color='#993300')

    # class_result routed to debounce
    ax.plot([0.3, 0.3, 10.2], [5.0, 6.5, 6.5], color='#336699', lw=1.0, ls=':')

    # ADC signals routed to reg_file
    ax.plot([0.3, 0.3, 5.5], [6.0, 7.5, 7.5], color='#336699', lw=1.0, ls=':')
    ax.text(2.9, 7.6, "adc_data/done", fontsize=6, ha='center',
            fontfamily='monospace', color='#336699')

    # clk/rst_n distribution note
    ax.text(8, 1.5, "clk and rst_n distributed to all sub-blocks",
            fontsize=8, ha='center', va='center', style='italic',
            color='#888888', fontfamily='monospace')

    # Footer
    ax.text(8, 0.3, "Generated 2026-03-24  |  SKY130 sky130_fd_sc_hd  |  Yosys 0.33  |  28/28 tests PASS  |  Tapeout-ready",
            fontsize=7, ha='center', va='center', color='#999999',
            fontfamily='monospace')

    plt.tight_layout()
    plt.savefig(outpath, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Generated {outpath}")


# ===========================================================================
# Main
# ===========================================================================
if __name__ == '__main__':
    # Generate .sch file
    sch = build_sch()
    sch_path = os.path.join(OUTDIR, 'digital_top.sch')
    with open(sch_path, 'w') as f:
        f.write(sch)
    print(f"Generated {sch_path} ({len(sch)} bytes, {len(lines)} components, {len(wires)} wires)")

    # Try xschem rendering first
    png_path = os.path.join(OUTDIR, 'digital_top.png')
    try:
        result = subprocess.run([
            'xvfb-run', '--auto-servernum',
            '--server-args=-screen 0 1920x1080x24',
            'xschem', '--tcl',
            f'xschem load {sch_path}; xschem zoom_full; xschem print png {png_path}; xschem exit',
            '--quit'
        ], capture_output=True, text=True, timeout=30)
        if os.path.exists(png_path) and os.path.getsize(png_path) > 1000:
            print(f"xschem rendered {png_path}")
        else:
            raise RuntimeError("xschem render produced no/small output")
    except Exception as e:
        print(f"xschem render failed ({e}), falling back to matplotlib")
        build_png(png_path)
