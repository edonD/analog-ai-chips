"""
VibroSense-1 System Block Diagram Generator — v6 (Final Polish)
Publication-quality chip architecture diagram.
4800x2800 px, dark theme, clean 4-column horizontal flow.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ══════════════════════════════════════════════════
# COLOR PALETTE
# ══════════════════════════════════════════════════
BG        = '#0d1117'
BG_LIGHT  = '#161b22'
C_EXT     = '#4ade80'
C_ANA     = '#22d3ee'
C_CLASS   = '#a78bfa'
C_DIG     = '#f59e0b'
C_SUP     = '#6b7280'
C_TRAIN   = '#c084fc'
C_ALERT   = '#ef4444'
C_TXT     = '#ffffff'
C_DIM     = '#94a3b8'
C_ARROW   = '#cbd5e1'
C_BROAD   = '#60a5fa'

BAND_COLORS = ['#f87171', '#fb923c', '#fbbf24', '#a3e635', '#34d399']
CLASS_COLORS = {
    'Normal': '#4ade80', 'Imbalance': '#fbbf24',
    'Bearing': '#ef4444', 'Looseness': '#fb923c',
}

FONT  = 'Segoe UI'
FMONO = 'Consolas'
DPI   = 200
FW, FH = 24, 14


def draw_block(ax, x, y, w, h, title, specs, color,
               block_num=None, title_size=17, spec_size=12.5,
               border_width=2.5, fill_alpha=0.13):
    ax.add_patch(FancyBboxPatch(
        (x - 0.05, y - 0.05), w + 0.10, h + 0.10,
        boxstyle="round,pad=0.3",
        fc=color, ec='none', alpha=fill_alpha * 0.3, lw=0, zorder=1))
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.3",
        fc=color, ec='none', alpha=fill_alpha, lw=0, zorder=2))
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.3",
        fc='none', ec=color, alpha=0.80, lw=border_width, zorder=3))
    if block_num is not None:
        bx, by = x + 0.18, y + h - 0.50
        ax.add_patch(FancyBboxPatch(
            (bx, by), 0.80, 0.35,
            boxstyle="round,pad=0.04",
            fc=color, ec='none', alpha=0.30, lw=0, zorder=4))
        ax.text(bx + 0.40, by + 0.175, f'B{block_num:02d}',
                size=10.5, family=FMONO, color=color,
                ha='center', va='center', weight='bold', alpha=0.90, zorder=5)
    cx = x + w / 2
    cy = y + h / 2 + (0.28 if specs else 0)
    ax.text(cx, cy, title, size=title_size, family=FONT, color=C_TXT,
            ha='center', va='center', weight='bold', zorder=5,
            linespacing=1.3)
    if specs:
        ax.text(cx, cy - 0.55, specs, size=spec_size, family=FONT,
                color=C_DIM, ha='center', va='center', zorder=5,
                linespacing=1.3)


def draw_band_block(ax, x, y, w, h, label, color):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.12",
        fc=color, ec='none', alpha=0.13, lw=0, zorder=2))
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.12",
        fc='none', ec=color, alpha=0.70, lw=2.0, zorder=3))
    ax.text(x + w / 2, y + h / 2, label,
            size=13, family=FONT, color=C_TXT,
            ha='center', va='center', weight='bold', zorder=5)


def arrow(ax, x1, y1, x2, y2, color=C_ARROW, lw=2.0, ms=22, alpha=0.85,
          conn='arc3,rad=0', ls='-'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->', color=color, lw=lw,
                    connectionstyle=conn, mutation_scale=ms,
                    alpha=alpha, linestyle=ls),
                zorder=4)


def dashed_arrow(ax, x1, y1, x2, y2, color=C_SUP, lw=1.0, rad=0):
    arrow(ax, x1, y1, x2, y2, color=color, lw=lw, ms=14, alpha=0.40,
          conn=f'arc3,rad={rad}', ls='--')


def main():
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-0.5, 24.5)
    ax.set_ylim(-1.2, 14.0)
    ax.set_aspect('equal')
    ax.axis('off')

    # Subtle dot grid
    for gx in np.arange(0, 25, 1.0):
        for gy in np.arange(0, 14, 1.0):
            ax.plot(gx, gy, '.', color=BG_LIGHT, ms=0.5, zorder=0)

    # Border
    ax.add_patch(FancyBboxPatch(
        (-0.3, -1.0), 24.6, 14.6,
        boxstyle="round,pad=0.2",
        fc='none', ec=C_DIM, alpha=0.12, lw=1.0, zorder=0))

    # ══════════════════════════════════════════════
    # TITLE  (Issue #3: larger text ~28-30pt)
    # ══════════════════════════════════════════════
    ax.text(12.0, 13.15, 'VibroSense-1  System Architecture',
            size=30, family=FONT, color=C_TXT, ha='center',
            weight='bold', zorder=5)
    ax.text(12.0, 12.50,
            'SkyWater SKY130A  |  1.8 V  |  <300 \u00b5W Always-On  |  4-Class Bearing Fault Detection',
            size=16, family=FONT, color=C_DIM, ha='center', zorder=5)
    ax.plot([3.0, 21.0], [12.05, 12.05], color=C_DIM, lw=0.6, alpha=0.22)

    # ══════════════════════════════════════════════
    # BAND LAYOUT
    # ══════════════════════════════════════════════
    band_h = 0.85
    band_gap = 0.35
    total_5 = 5 * band_h + 4 * band_gap
    BAND_TOP_Y = 11.2  # top edge of band 1

    band_ys = []
    for i in range(5):
        by = BAND_TOP_Y - i * (band_h + band_gap) - band_h
        band_ys.append(by)
    band_centers = [by + band_h / 2 for by in band_ys]
    BAND_BOTTOM = band_ys[4]  # bottom edge of band 5

    # ──────────────────────────────────────────────
    # COLUMN 1: MEMS + PGA
    # ──────────────────────────────────────────────
    col1_x = 0.3
    col1_w = 2.8

    # MEMS
    mems_h = 1.7
    mems_y = band_centers[0] - 0.2
    draw_block(ax, col1_x, mems_y, col1_w, mems_h,
               'MEMS\nAccelerometer', '\u00b12 g  |  \u00b1660 mV', C_EXT,
               title_size=16, border_width=2.5)
    ax.text(col1_x + col1_w / 2, mems_y + mems_h + 0.22,
            'ADXL355 (external)', size=11.5, family=FONT,
            color=C_EXT, ha='center', alpha=0.65, zorder=5)

    # PGA
    pga_h = 2.2
    pga_y = (band_centers[1] + band_centers[3]) / 2 - pga_h / 2
    draw_block(ax, col1_x, pga_y, col1_w, pga_h,
               'PGA', '1 / 4 / 16 / 64\u00d7\n10 \u00b5W  |  49 T', C_ANA,
               block_num=2, title_size=17)

    # MEMS -> PGA
    arrow(ax, col1_x + col1_w / 2, mems_y,
          col1_x + col1_w / 2, pga_y + pga_h,
          C_EXT, lw=2.8, ms=22)

    # ──────────────────────────────────────────────
    # COLUMN 2: BPF BANK + RMS/CREST below
    # ──────────────────────────────────────────────
    bpf_x = 4.5
    bpf_w = 3.3

    ax.text(bpf_x + bpf_w / 2, BAND_TOP_Y + 0.55,
            'Block 03: BPF Bank',
            size=16, family=FONT, color=C_ANA, ha='center',
            weight='bold', zorder=5)
    ax.text(bpf_x + bpf_w / 2, BAND_TOP_Y + 0.15,
            '42.5 \u00b5W  |  ~500 T',
            size=11.5, family=FONT, color=C_DIM, ha='center', zorder=5)

    # Issue #5: larger band labels
    band_labels = [
        'BPF 1:  100\u2013500 Hz',
        'BPF 2:  0.5\u20132 kHz',
        'BPF 3:  2\u20135 kHz',
        'BPF 4:  5\u201310 kHz',
        'BPF 5:  10\u201320 kHz',
    ]
    for i in range(5):
        draw_band_block(ax, bpf_x, band_ys[i], bpf_w, band_h,
                        band_labels[i], BAND_COLORS[i])

    # PGA -> BPF fan-out
    pga_out_x = col1_x + col1_w
    pga_out_y = pga_y + pga_h / 2
    for i in range(5):
        dy = band_centers[i] - pga_out_y
        if abs(dy) < 1.0:
            rad = 0.0
        elif dy > 0:
            rad = 0.15
        else:
            rad = -0.12
        arrow(ax, pga_out_x, pga_out_y, bpf_x, band_centers[i],
              BAND_COLORS[i], lw=1.8, ms=16, alpha=0.60,
              conn=f'arc3,rad={rad}')

    # RMS / Crest / Kurtosis -- below bands
    rms_w, rms_h = 3.3, 1.5
    rms_x = bpf_x
    rms_y = BAND_BOTTOM - 0.7 - rms_h
    draw_block(ax, rms_x, rms_y, rms_w, rms_h,
               'RMS | Crest | Kurtosis',
               '3 broadband features\n8 \u00b5W  |  10 T', C_ANA,
               block_num=5, title_size=14, spec_size=10.5)

    # ─────────────────────────────────────────────────
    # Issue #4: Clean broadband dashed path PGA -> RMS -> Feature Vector
    # Route: PGA bottom -> down left side -> horizontal -> into RMS left
    # ─────────────────────────────────────────────────
    bb_turn_y = rms_y + rms_h / 2  # same height as RMS center
    bb_x = col1_x + col1_w * 0.25  # left side, clear of blocks
    # Vertical segment from PGA bottom going down
    ax.plot([bb_x, bb_x], [pga_y, bb_turn_y],
            color=C_BROAD, lw=2.2, alpha=0.50, ls='--', zorder=4)
    # Horizontal segment going right to RMS
    ax.plot([bb_x, rms_x], [bb_turn_y, bb_turn_y],
            color=C_BROAD, lw=2.2, alpha=0.50, ls='--', zorder=4)
    # Arrowhead entering RMS
    arrow(ax, rms_x - 0.5, bb_turn_y, rms_x, bb_turn_y,
          C_BROAD, lw=2.2, ms=18, alpha=0.55)

    # Issue #1: Remove the overlapping "Broadband path" label entirely.
    # The dashed blue line speaks for itself.

    # ──────────────────────────────────────────────
    # COLUMN 3a: ENVELOPE DETECTORS
    # ──────────────────────────────────────────────
    env_x = 9.0
    env_w = 2.6

    ax.text(env_x + env_w / 2, BAND_TOP_Y + 0.55,
            'Block 04: Envelope Det.',
            size=16, family=FONT, color=C_ANA, ha='center',
            weight='bold', zorder=5)
    ax.text(env_x + env_w / 2, BAND_TOP_Y + 0.15,
            '21 \u00b5W each  |  DC extraction',
            size=11.5, family=FONT, color=C_DIM, ha='center', zorder=5)

    env_labels = ['Env Det 1', 'Env Det 2', 'Env Det 3', 'Env Det 4', 'Env Det 5']
    for i in range(5):
        draw_band_block(ax, env_x, band_ys[i], env_w, band_h,
                        env_labels[i], BAND_COLORS[i])
        arrow(ax, bpf_x + bpf_w, band_centers[i],
              env_x, band_centers[i],
              BAND_COLORS[i], lw=2.0, ms=17, alpha=0.70)

    # ──────────────────────────────────────────────
    # COLUMN 3b: 8-FEATURE VECTOR
    # Issue #6: larger feature labels, evenly spaced
    # ──────────────────────────────────────────────
    fv_x = 12.6
    fv_w = 1.9
    fv_top = band_centers[0] + 0.7
    fv_bot = rms_y - 0.1
    fv_h = fv_top - fv_bot

    ax.add_patch(FancyBboxPatch(
        (fv_x, fv_bot), fv_w, fv_h,
        boxstyle="round,pad=0.15",
        fc=C_CLASS, ec=C_CLASS, alpha=0.06, lw=2.0, ls='--', zorder=2))

    ax.text(fv_x + fv_w / 2, fv_top + 0.55,
            '8-Feature', size=17, family=FONT, color=C_CLASS,
            ha='center', weight='bold', zorder=5)
    ax.text(fv_x + fv_w / 2, fv_top + 0.12,
            'Vector', size=17, family=FONT, color=C_CLASS,
            ha='center', weight='bold', zorder=5)

    feature_labels = [
        'E\u2081 band', 'E\u2082 band', 'E\u2083 band', 'E\u2084 band', 'E\u2085 band',
        'RMS', 'Crest', 'Kurt.'
    ]
    feature_colors = BAND_COLORS + [C_BROAD] * 3
    # Evenly space all 8 features within the box
    feat_margin = 0.35
    feat_avail = fv_h - 2 * feat_margin
    feat_spacing = feat_avail / 7
    feat_ys = []
    for i in range(8):
        fy = fv_top - feat_margin - i * feat_spacing
        feat_ys.append(fy)
        ax.text(fv_x + fv_w / 2, fy, feature_labels[i],
                size=11.5, family=FMONO, color=feature_colors[i],
                ha='center', va='center', weight='bold',
                alpha=0.90, zorder=6)

    # Envelope -> Feature Vector
    for i in range(5):
        arrow(ax, env_x + env_w, band_centers[i],
              fv_x, feat_ys[i],
              BAND_COLORS[i], lw=1.5, ms=14, alpha=0.55)

    # Issue #4: RMS -> Feature Vector — clean and visible
    for i in range(3):
        ry = rms_y + rms_h / 2 + (i - 1) * 0.35
        arrow(ax, rms_x + rms_w, ry,
              fv_x, feat_ys[5 + i],
              C_BROAD, lw=2.0, ms=16, alpha=0.65)

    # ──────────────────────────────────────────────
    # COLUMN 3c: CLASSIFIER
    # ──────────────────────────────────────────────
    cls_x, cls_w, cls_h = 15.5, 3.2, 4.5
    cls_cy = (fv_top + fv_bot) / 2
    cls_y = cls_cy - cls_h / 2
    draw_block(ax, cls_x, cls_y, cls_w, cls_h,
               'Charge-Domain\nMAC Classifier',
               '4-class output\n702 T  |  260 caps\n< 0.001 \u00b5W',
               C_CLASS, block_num=6, title_size=17, spec_size=12,
               border_width=2.5)

    # Feature Vector -> Classifier
    arrow(ax, fv_x + fv_w, cls_cy,
          cls_x, cls_cy,
          C_CLASS, lw=3.0, ms=24)
    ax.text((fv_x + fv_w + cls_x) / 2, cls_cy + 0.42,
            '8\u00d74 MAC', size=14, family=FMONO, color=C_CLASS,
            ha='center', alpha=0.70, zorder=5)

    # ──────────────────────────────────────────────
    # COLUMN 4: DIGITAL + IRQ + 4 CLASSES
    # ──────────────────────────────────────────────
    dig_x, dig_w, dig_h = 20.0, 3.6, 2.2
    dig_y = band_centers[0] - 0.5
    draw_block(ax, dig_x, dig_y, dig_w, dig_h,
               'Digital Control',
               'SPI | FSM | Debounce | IRQ\n645 cells  |  1.4 \u00b5W',
               C_DIG, block_num=8, title_size=17, spec_size=12)

    # Classifier -> Digital
    arrow(ax, cls_x + cls_w, cls_y + cls_h * 0.80,
          dig_x, dig_y + dig_h / 2,
          C_DIG, lw=2.5, ms=20, conn='arc3,rad=-0.12')
    ax.text((cls_x + cls_w + dig_x) / 2,
            (cls_y + cls_h * 0.80 + dig_y + dig_h / 2) / 2 + 0.55,
            'Class result', size=12, family=FONT, color=C_DIM,
            ha='center', zorder=5)

    # IRQ
    irq_y = dig_y + dig_h * 0.65
    arrow(ax, dig_x + dig_w, irq_y, 24.0, irq_y,
          C_ALERT, lw=3.0, ms=26)
    ax.text(24.05, irq_y + 0.25, 'IRQ', size=18, family=FMONO,
            color=C_ALERT, ha='left', weight='bold', zorder=5)
    ax.text(24.05, irq_y - 0.25, 'Wake MCU', size=11.5, family=FONT,
            color=C_DIM, ha='left', zorder=5)

    # 4 Output Classes
    oc_x = 20.0
    oc_w = 3.6
    class_h = 0.70
    class_gap = 0.32
    oc_top_y = dig_y - 1.2

    ax.text(oc_x + oc_w / 2, oc_top_y + 0.55,
            '4 Output Classes', size=15, family=FONT, color=C_DIM,
            ha='center', weight='bold', zorder=5)

    class_names = ['Normal', 'Imbalance', 'Bearing', 'Looseness']
    class_centers_y = []
    for i, name in enumerate(class_names):
        cy = oc_top_y - i * (class_h + class_gap)
        cc = CLASS_COLORS[name]
        ax.add_patch(FancyBboxPatch(
            (oc_x, cy), oc_w, class_h,
            boxstyle="round,pad=0.08",
            fc=cc, ec=cc, alpha=0.12, lw=2.0, zorder=2))
        ax.text(oc_x + oc_w / 2, cy + class_h / 2, name,
                size=15, family=FONT, color=cc, ha='center',
                va='center', weight='bold', zorder=5)
        class_centers_y.append(cy + class_h / 2)

    # Classifier -> classes
    mid_class_y = (class_centers_y[1] + class_centers_y[2]) / 2
    arrow(ax, cls_x + cls_w, cls_cy,
          oc_x, mid_class_y,
          C_CLASS, lw=1.8, ms=17, conn='arc3,rad=0.15', alpha=0.55)

    # ══════════════════════════════════════════════
    # POWER BUDGET
    # ══════════════════════════════════════════════
    pwr_x = 20.2
    pwr_y = class_centers_y[-1] - class_h / 2 - 1.6
    ax.add_patch(FancyBboxPatch(
        (pwr_x, pwr_y), 3.2, 1.2,
        boxstyle="round,pad=0.15",
        fc=C_DIG, ec=C_DIG, alpha=0.08, lw=1.5, zorder=2))
    ax.text(pwr_x + 1.6, pwr_y + 0.85, 'Power Budget',
            size=15, family=FONT, color=C_DIG, ha='center',
            weight='bold', zorder=5)
    ax.text(pwr_x + 1.6, pwr_y + 0.45, 'Total: ~200 \u00b5W',
            size=14, family=FONT, color=C_TXT, ha='center', zorder=5)
    ax.text(pwr_x + 1.6, pwr_y + 0.15, 'always-on analog path',
            size=10.5, family=FONT, color=C_DIM, ha='center', zorder=5)

    # ══════════════════════════════════════════════
    # SUPPORT ROW
    # Issue #2: Remove messy bias lines, add text note on B00 instead
    # ══════════════════════════════════════════════
    sep_y = 3.6
    ax.plot([0.3, 23.5], [sep_y, sep_y], color=C_DIM, lw=0.6,
            alpha=0.18, ls='--', zorder=1)
    ax.text(0.8, sep_y + 0.22,
            'SUPPORT  &  OFFLINE', size=10.5, family=FONT,
            color=C_DIM, ha='left', alpha=0.40, weight='bold', zorder=5)

    SUP_CY = 2.0
    s_h = 1.5

    b00_x, b00_w = 0.5, 4.2
    b00_y = SUP_CY - s_h / 2
    draw_block(ax, b00_x, b00_y, b00_w, s_h,
               'Bias Generator',
               '507 nA ref  |  0.97 \u00b5W\nBias \u2192 all analog blocks', C_SUP,
               block_num=0, title_size=14, spec_size=10.5,
               border_width=1.5, fill_alpha=0.08)

    # Issue #2: No bias bus lines drawn — the text note inside B00 is sufficient

    b01_x, b01_w = 5.7, 4.2
    b01_y = SUP_CY - s_h / 2
    draw_block(ax, b01_x, b01_y, b01_w, s_h,
               'OTA (Building Block)',
               '0.90 \u00b5W each', C_SUP,
               block_num=1, title_size=14, spec_size=10.5,
               border_width=1.5, fill_alpha=0.08)
    ax.text(b01_x + b01_w / 2, b01_y - 0.28,
            'Reused in B02\u2013B05', size=9.5, family=FONT,
            color=C_SUP, ha='center', alpha=0.50, style='italic', zorder=5)

    b07_x, b07_w = 10.9, 4.2
    b07_y = SUP_CY - s_h / 2
    draw_block(ax, b07_x, b07_y, b07_w, s_h,
               'SAR ADC',
               '8-bit  |  28 \u00b5W active', C_ANA,
               block_num=7, title_size=14, spec_size=10.5,
               border_width=1.5, fill_alpha=0.08)
    ax.text(b07_x + b07_w / 2, b07_y - 0.28,
            'On-demand (not always-on)  |  sleep mode', size=9.5,
            family=FONT, color=C_ANA, ha='center', alpha=0.50,
            style='italic', zorder=5)

    b09_x, b09_w = 16.1, 4.5
    b09_y = SUP_CY - s_h / 2
    draw_block(ax, b09_x, b09_y, b09_w, s_h,
               'Training (Offline)',
               'Python  |  CWRU dataset\n128 weights via SPI', C_TRAIN,
               block_num=9, title_size=14, spec_size=10.5,
               border_width=1.5, fill_alpha=0.08)

    dashed_arrow(ax, b09_x + b09_w / 2, b09_y + s_h,
                 cls_x + cls_w / 2, cls_y,
                 C_TRAIN, lw=1.2, rad=-0.10)
    # "Weights" label with background for readability
    wlx = (b09_x + b09_w / 2 + cls_x + cls_w / 2) / 2 + 0.6
    wly = (b09_y + s_h + cls_y) / 2 + 0.15
    ax.add_patch(FancyBboxPatch(
        (wlx - 0.60, wly - 0.20), 1.2, 0.40,
        boxstyle="round,pad=0.05",
        fc=BG, ec='none', alpha=0.75, lw=0, zorder=4))
    ax.text(wlx, wly, 'Weights', size=12, family=FONT, color=C_TRAIN,
            ha='center', alpha=0.70, zorder=5, weight='bold')

    dashed_arrow(ax, dig_x + dig_w / 2, dig_y,
                 b09_x + b09_w * 0.7, b09_y + s_h,
                 C_DIG, lw=0.9, rad=0.15)
    ax.text(dig_x + 0.3, (dig_y + b09_y + s_h) / 2 + 0.8,
            'SPI', size=10.5, family=FMONO, color=C_DIG,
            ha='center', alpha=0.50, zorder=5)

    dashed_arrow(ax, b07_x + b07_w / 2, b07_y + s_h,
                 rms_x + rms_w / 2, rms_y,
                 C_SUP, lw=0.9)

    # ══════════════════════════════════════════════
    # LEGEND  (Issue #3: larger text)
    # ══════════════════════════════════════════════
    legend_items = [
        ('External / Sensor', C_EXT),
        ('Analog Signal Path', C_ANA),
        ('Classifier', C_CLASS),
        ('Digital', C_DIG),
        ('Support / Offline', C_SUP),
    ]
    for i, (label, color) in enumerate(legend_items):
        lx = 1.5 + i * 4.0
        ax.plot(lx, -0.7, 's', color=color, ms=11, alpha=0.60, zorder=5)
        ax.text(lx + 0.35, -0.7, label, size=11.5, family=FONT, color=color,
                ha='left', va='center', alpha=0.70, zorder=5)

    ax.text(23.0, -0.7, 'T = transistors', size=10.5, family=FONT,
            color=C_DIM, ha='center', alpha=0.45, zorder=5)

    # ══════════════════════════════════════════════
    # SAVE
    # ══════════════════════════════════════════════
    out = r'C:\Users\derguti\analog-ai-chips\vibrosense\system_block_diagram.png'
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG,
                edgecolor='none', pad_inches=0.4)
    plt.close(fig)
    print(f'Saved: {out}  ({FW * DPI}x{FH * DPI} px)')


if __name__ == '__main__':
    main()
