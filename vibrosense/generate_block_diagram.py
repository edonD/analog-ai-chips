"""Generate a cleaner, publication-style system architecture diagram for VibroSense-1."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


BG = "#f6f8fb"
CHIP_BG = "#fcfdff"
CARD_BG = "#ffffff"
TEXT = "#132238"
MUTED = "#5f6f82"
BORDER = "#d5deea"
GRID = "#e8edf4"
LINE = "#8fa1b5"

SENSOR = "#1f8f68"
ANALOG = "#2563eb"
CLASSIFIER = "#7c4dff"
DIGITAL = "#b7791f"
SUPPORT = "#6b7a90"
OFFLINE = "#8b5cf6"
ALERT = "#c0392b"

SENSOR_FILL = "#eef8f3"
ANALOG_FILL = "#eef4ff"
CLASSIFIER_FILL = "#f5f0ff"
DIGITAL_FILL = "#fff5e7"
SUPPORT_FILL = "#f4f6f9"

FONT = "DejaVu Sans"
MONO = "DejaVu Sans Mono"

DPI = 200
FIG_W = 21
FIG_H = 13


def rounded_box(ax, x, y, w, h, fc, ec, lw=1.2, radius=0.9, z=1, alpha=1.0):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        alpha=alpha,
        zorder=z,
    )
    ax.add_patch(patch)
    return patch


def label_chip(ax, x, y, text, fc, tc=TEXT, fs=8.6, mono=False, z=6):
    width = max(3.2, 0.24 * len(text) + 1.0)
    rounded_box(ax, x, y, width, 1.05, fc=fc, ec="none", lw=0, radius=0.35, z=z)
    ax.text(
        x + width / 2,
        y + 0.52,
        text,
        ha="center",
        va="center",
        fontsize=fs,
        color=tc,
        family=MONO if mono else FONT,
        weight="bold",
        zorder=z + 1,
    )
    return width


def draw_panel(ax, x, y, w, h, accent, fill, stage, title, subtitle,
               title_fs=11.5, sub_fs=8.6, badge_fs=8.0):
    rounded_box(ax, x, y, w, h, fc=fill, ec=BORDER, lw=1.1, radius=1.0, z=1.5)
    # top accent line removed for cleaner look
    stage_w = label_chip(ax, x + 1.0, y + h - 2.95, stage, fc=accent, tc="white", fs=badge_fs)
    ax.text(
        x + 1.0 + stage_w + 0.8,
        y + h - 2.45,
        title,
        ha="left",
        va="center",
        fontsize=title_fs,
        color=TEXT,
        family=FONT,
        weight="bold",
        zorder=5,
    )
    ax.text(
        x + 1.0,
        y + h - 4.1,
        subtitle,
        ha="left",
        va="center",
        fontsize=sub_fs,
        color=MUTED,
        family=FONT,
        zorder=5,
    )


def draw_card(ax, x, y, w, h, title, accent, lines=None, block=None, meta=None, fs=8.5, title_fs=10.2):
    rounded_box(ax, x, y, w, h, fc=CARD_BG, ec=BORDER, lw=1.0, radius=0.7, z=3)
    badge_bottom = y + h  # track where badge ends for title placement
    if block:
        badge_y = y + h - 1.55
        label_chip(ax, x + 0.8, badge_y, block, fc=accent, tc="white", fs=7.6, mono=True, z=5)
        badge_bottom = badge_y
    if meta:
        ax.text(
            x + w - 0.65,
            y + h - 1.0,
            meta,
            ha="right",
            va="center",
            fontsize=7.2,
            color=MUTED,
            family=MONO,
            zorder=5,
        )
    title_x = x + 0.9
    title_y = badge_bottom - 1.1 if block else y + h - 1.35
    ax.text(
        title_x,
        title_y,
        title,
        ha="left",
        va="top",
        fontsize=title_fs,
        color=TEXT,
        family=FONT,
        weight="bold",
        zorder=5,
        linespacing=1.15,
    )
    # count newlines in title to offset lines properly
    n_title_lines = title.count("\n") + 1
    title_text_bottom = title_y - n_title_lines * (title_fs * 0.12 + 0.35)
    if lines:
        top = title_text_bottom - 0.45
        for idx, line in enumerate(lines):
            ax.text(
                title_x,
                top - idx * (fs * 0.16 + 0.72),
                line,
                ha="left",
                va="center",
                fontsize=fs,
                color=MUTED,
                family=FONT,
                zorder=5,
            )


def draw_mini_row(ax, x, y, w, h, badge, label, accent):
    rounded_box(ax, x, y, w, h, fc="#fbfdff", ec=BORDER, lw=0.9, radius=0.42, z=4)
    label_chip(ax, x + 0.35, y + 0.38, badge, fc=accent, tc="white", fs=6.8, mono=True, z=5)
    ax.text(
        x + 2.6,
        y + h / 2,
        label,
        ha="left",
        va="center",
        fontsize=7.6,
        color=TEXT,
        family=FONT,
        zorder=6,
    )


def draw_pill(ax, x, y, w, h, text, fc, tc, fs=7.0):
    rounded_box(ax, x, y, w, h, fc=fc, ec="none", lw=0, radius=0.45, z=5)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fs,
        color=tc,
        family=FONT,
        weight="bold",
        zorder=6,
    )


def arrow(ax, x1, y1, x2, y2, color=LINE, lw=1.5, rad=0.0, dashed=False, ms=14):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=lw,
            mutation_scale=ms,
            linestyle="--" if dashed else "-",
            connectionstyle=f"arc3,rad={rad}",
            shrinkA=3,
            shrinkB=3,
        ),
        zorder=4.5,
    )


def arrow_label(ax, x, y, text, color=MUTED, fs=7.5, fc=BG, mono=False):
    width = max(2.5, 0.2 * len(text) + 0.7)
    rounded_box(ax, x - width / 2, y - 0.52, width, 1.04, fc=fc, ec="none", lw=0, radius=0.25, z=5, alpha=0.96)
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fs,
        color=color,
        family=MONO if mono else FONT,
        zorder=6,
    )


def draw_background(ax):
    for gx in range(4, 138, 4):
        ax.plot([gx, gx], [8, 82], color=GRID, lw=0.45, zorder=0)
    for gy in range(8, 84, 4):
        ax.plot([3, 137], [gy, gy], color=GRID, lw=0.45, zorder=0)


def main():
    plt.rcParams["font.family"] = FONT
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 92)
    ax.axis("off")

    draw_background(ax)

    ax.text(
        70,
        87.0,
        "VibroSense-1 System Architecture",
        ha="center",
        va="center",
        fontsize=24.5,
        color=TEXT,
        weight="bold",
    )
    ax.text(
        70,
        83.8,
        "SkyWater SKY130A | 1.8 V | <300 uW always-on | 4-class bearing fault detection",
        ha="center",
        va="center",
        fontsize=12.0,
        color=MUTED,
    )
    ax.plot([24, 116], [81.0, 81.0], color=BORDER, lw=1.0, zorder=1)

    rounded_box(ax, 24, 14, 94, 62, fc=CHIP_BG, ec="#bcc9d8", lw=1.25, radius=1.2, z=1)
    ax.text(26, 73.8, "VIBROSENSE-1 CHIP", ha="left", va="center", fontsize=9.6, color=TEXT, weight="bold")
    ax.text(
        116.0,
        73.8,
        "Always-on analog path with lightweight wake logic",
        ha="right",
        va="center",
        fontsize=8.6,
        color=MUTED,
    )
    ax.plot([26, 116], [34.0, 34.0], color=BORDER, lw=0.95, zorder=2)
    ax.text(26.6, 34.9, "Support, calibration and offline assets", ha="left", va="bottom", fontsize=8.6, color=MUTED)

    # -- Sensor input: clean monochrome block --
    sx, sy, sw, sh = 4, 44, 15, 16
    rounded_box(ax, sx, sy, sw, sh, fc="#f8faf9", ec="#c8d5ce", lw=1.1, radius=1.0, z=1.5)
    cx = sx + sw / 2
    ax.text(cx, sy + sh - 2.2, "MEMS", ha="center", va="center",
            fontsize=13, color="#1a1a1a", family=MONO, weight="bold", zorder=5)
    ax.text(cx, sy + sh - 4.0, "Accelerometer", ha="center", va="center",
            fontsize=10, color="#1a1a1a", family=MONO, weight="bold", zorder=5)
    ax.plot([sx + 2.5, sx + sw - 2.5], [sy + sh - 5.2, sy + sh - 5.2],
            color="#c8d5ce", lw=0.8, zorder=3)
    ax.text(cx, sy + sh - 6.8, "ADXL355", ha="center", va="center",
            fontsize=9.5, color=MUTED, family=MONO, zorder=5)
    ax.text(cx, sy + sh - 8.6, "+/-2 g  |  +/-660 mV", ha="center", va="center",
            fontsize=7.5, color=MUTED, family=FONT, zorder=5)
    ax.text(cx, sy + 1.8, "external sensor", ha="center", va="center",
            fontsize=7.0, color="#8a9e90", family=FONT, zorder=5)

    # ── helper: monochrome sub-block inside the chip ──
    C1 = "#1a1a1a"  # dark text
    C2 = MUTED      # secondary text
    C3 = "#d0d8e0"  # divider / border
    BX = "#f5f7fa"  # block fill

    BLOCK_TITLE_FS = 9.5  # uniform title size for all blocks

    def mono_block(x, y, w, h, title, specs=None, sub=None, ec=C3, spec_offset=0, title_fs=None):
        rounded_box(ax, x, y, w, h, fc=BX, ec=ec, lw=1.0, radius=0.8, z=3)
        cx = x + w / 2
        tfs = title_fs if title_fs else BLOCK_TITLE_FS
        ax.text(cx, y + h - 1.6, title, ha="center", va="center",
                fontsize=tfs, color=C1, family=MONO, weight="bold", zorder=5)
        # specs lines
        if specs:
            for i, s in enumerate(specs):
                ax.text(cx, y + h - 3.2 - spec_offset - i * 1.5, s, ha="center", va="center",
                        fontsize=min(7.8, w * 0.56), color=C2, family=FONT, zorder=5)
        # subtle subtitle at bottom
        if sub:
            ax.text(cx, y + 1.0, sub, ha="center", va="center",
                    fontsize=min(6.8, w * 0.48), color="#9aa5b0", family=FONT, zorder=5)

    def mono_row(x, y, w, h, label):
        rounded_box(ax, x, y, w, h, fc="#eef1f5", ec=C3, lw=0.7, radius=0.35, z=4)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=7.2, color=C1, family=MONO, zorder=5)

    # ── 02: Analog feature extraction ──
    # outer container
    ax0, ay0, aw0, ah0 = 27, 38, 56, 32
    rounded_box(ax, ax0, ay0, aw0, ah0, fc="#f8fafd", ec="#b8c8d8", lw=1.1, radius=1.0, z=1.5)
    ax.text(ax0 + aw0 / 2, ay0 + ah0 - 1.6, "Analog Feature Extraction", ha="center", va="center",
            fontsize=11, color=C1, family=MONO, weight="bold", zorder=5)

    # PGA
    mono_block(29, 54, 9, 10, "PGA",
               specs=["1x / 4x / 16x / 64x"],
               sub="10 uW")

    # BPF bank — 5 channel rows
    mono_block(40, 48, 17, 18, "BPF Bank",
               sub="42.5 uW")
    bands = ["100-500 Hz", "0.5-2 kHz", "2-5 kHz", "5-10 kHz", "10-20 kHz"]
    for i, b in enumerate(bands):
        mono_row(41.2, 61.5 - i * 2.6, 14.6, 2.1, b)

    # Envelope detectors
    mono_block(59, 48, 13, 18, "Envelope\nDetectors",
               specs=["5x rectify + LPF", "~10 Hz bandwidth"],
               sub="5x 21 uW", spec_offset=1.8)

    # Broadband: RMS / Crest / Kurtosis
    mono_block(40, 40, 32, 5.5, "RMS  |  Crest  |  Kurtosis",
               sub="8 uW")

    # Feature vector column — shows the 8 analog DC voltages that feed the classifier
    fvx, fvy, fvw, fvh = 74, 47, 7, 19
    rounded_box(ax, fvx, fvy, fvw, fvh, fc="#eef1f5", ec=C3, lw=0.9, radius=0.6, z=3)
    fvcx = fvx + fvw / 2
    ax.text(fvcx, fvy + fvh - 1.2, "Feature", ha="center", va="center",
            fontsize=7.8, color=C1, family=MONO, weight="bold", zorder=5)
    ax.text(fvcx, fvy + fvh - 2.5, "Vector", ha="center", va="center",
            fontsize=7.8, color=C1, family=MONO, weight="bold", zorder=5)
    ax.plot([fvx + 1.0, fvx + fvw - 1.0], [fvy + fvh - 3.3, fvy + fvh - 3.3],
            color=C3, lw=0.7, zorder=4)
    # 8 feature rows — each is a DC voltage line going to the classifier
    fv_labels = [
        ("Band 1", "100-500 Hz"),
        ("Band 2", "0.5-2 kHz"),
        ("Band 3", "2-5 kHz"),
        ("Band 4", "5-10 kHz"),
        ("Band 5", "10-20 kHz"),
        ("RMS", "broadband"),
        ("Crest", "peak/RMS"),
        ("Kurt.", "impulsive"),
    ]
    for i, (name, desc) in enumerate(fv_labels):
        fy = fvy + fvh - 4.4 - i * 1.7
        ax.text(fvcx, fy, name, ha="center", va="center",
                fontsize=6.2, color=C1, family=MONO, weight="bold", zorder=5)
    ax.text(fvcx, fvy + 0.8, "8 DC voltages", ha="center", va="center",
            fontsize=5.8, color="#9aa5b0", family=FONT, zorder=5)

    # ── 03: Classifier ──
    cx0, cy0, cw0, ch0 = 85, 38, 14, 32
    rounded_box(ax, cx0, cy0, cw0, ch0, fc="#f8f6fd", ec="#c4b8e0", lw=1.1, radius=1.0, z=1.5)
    ax.text(cx0 + cw0 / 2, cy0 + ch0 - 1.6, "Classifier", ha="center", va="center",
            fontsize=11, color=C1, family=MONO, weight="bold", zorder=5)

    mono_block(87, 52, 10, 13, "Charge-Domain\nMAC",
               specs=["8x4 array", "MIM cap weights", "winner-take-all"],
               sub="<0.001 uW", ec="#c4b8e0")

    # output classes
    rounded_box(ax, 87, 40, 10, 9.5, fc=BX, ec="#c4b8e0", lw=0.9, radius=0.6, z=3)
    ax.text(92, 48.2, "Output", ha="center", va="center",
            fontsize=8.5, color=C1, family=MONO, weight="bold", zorder=5)
    draw_pill(ax, 87.6, 45.8, 4.2, 1.3, "Normal", "#e8f5e9", "#2e7d32", fs=6.8)
    draw_pill(ax, 92.4, 45.8, 4.2, 1.3, "Imbalance", "#fff8e1", "#9a6700", fs=6.2)
    draw_pill(ax, 87.6, 43.8, 4.2, 1.3, "Bearing", "#ffebee", "#c62828", fs=6.8)
    draw_pill(ax, 92.4, 43.8, 4.2, 1.3, "Looseness", "#fff3e0", "#e65100", fs=6.2)
    ax.text(92, 41.2, "4-class fault decision", ha="center", va="center",
            fontsize=6.5, color="#9aa5b0", family=FONT, zorder=5)

    # ── 04: Digital / Wake logic ──
    dx0, dy0, dw0, dh0 = 101, 38, 15, 32
    rounded_box(ax, dx0, dy0, dw0, dh0, fc="#fdfaf5", ec="#d8ccaa", lw=1.1, radius=1.0, z=1.5)
    ax.text(dx0 + dw0 / 2, dy0 + dh0 - 1.6, "Digital Control", ha="center", va="center",
            fontsize=10, color=C1, family=MONO, weight="bold", zorder=5)

    mono_block(103, 52, 11, 12, "SPI + FSM",
               specs=["config weights", "debounce", "class latch"],
               sub="1.4 uW", ec="#d8ccaa")

    mono_block(103, 40, 11, 9, "Wake Path",
               specs=["assert IRQ", "wake host MCU"],
               ec="#d8ccaa")

    # ── Host MCU (external) ──
    hx, hy, hw, hh = 121, 44, 15, 16
    rounded_box(ax, hx, hy, hw, hh, fc="#f8faf9", ec="#c8d5ce", lw=1.1, radius=1.0, z=1.5)
    hcx = hx + hw / 2
    ax.text(hcx, hy + hh - 2.2, "Host MCU", ha="center", va="center",
            fontsize=11, color=C1, family=MONO, weight="bold", zorder=5)
    ax.plot([hx + 2.5, hx + hw - 2.5], [hy + hh - 3.8, hy + hh - 3.8],
            color="#c8d5ce", lw=0.8, zorder=3)
    ax.text(hcx, hy + hh - 5.4, "sleeps until IRQ", ha="center", va="center",
            fontsize=7.5, color=C2, family=FONT, zorder=5)
    ax.text(hcx, hy + hh - 7.0, "reads on demand", ha="center", va="center",
            fontsize=7.5, color=C2, family=FONT, zorder=5)
    ax.text(hcx, hy + hh - 8.6, "transmit anomaly", ha="center", va="center",
            fontsize=7.5, color=C2, family=FONT, zorder=5)
    ax.text(hcx, hy + 1.4, "external", ha="center", va="center",
            fontsize=6.8, color="#8a9e90", family=FONT, zorder=5)

    # ── Support row (bottom) ──
    def support_block(x, y, w, h, title, line1, line2=""):
        rounded_box(ax, x, y, w, h, fc="#f4f6f8", ec=C3, lw=0.9, radius=0.7, z=3)
        cx = x + w / 2
        ax.text(cx, y + h - 1.8, title, ha="center", va="center",
                fontsize=8.5, color=C1, family=MONO, weight="bold", zorder=5)
        ax.text(cx, y + h - 3.6, line1, ha="center", va="center",
                fontsize=7.0, color=C2, family=FONT, zorder=5)
        if line2:
            ax.text(cx, y + h - 5.0, line2, ha="center", va="center",
                    fontsize=7.0, color=C2, family=FONT, zorder=5)

    support_block(29, 19, 17, 9, "Bias Generator", "507 nA reference", "0.97 uW")
    support_block(48.5, 19, 17, 9, "OTA", "folded-cascode", "reused in B02-B05")
    support_block(68, 19, 17, 9, "SAR ADC", "8-bit on-demand", "28 uW active")
    support_block(88, 19, 26, 9, "Offline Training", "CWRU dataset  |  128 weights", "loaded via SPI")

    # ── Arrows (monochrome) ──
    A1 = "#5a6a78"  # arrow color
    A2 = "#8090a0"  # secondary

    arrow(ax, 19, 52, 29, 59, color=A1, lw=2.0, ms=15)
    arrow_label(ax, 23, 56.5, "vibration signal", color=A1, fc=BG)

    arrow(ax, 38, 59, 40, 59, color=A2, lw=1.5, ms=12)
    arrow(ax, 57, 57, 59, 57, color=A2, lw=1.5, ms=12)
    arrow(ax, 72, 57, 74, 56, color=A2, lw=1.5, ms=12)
    arrow(ax, 34, 54, 45, 45.5, color=A2, lw=1.2, ms=10)
    arrow(ax, 72, 42.8, 74, 50, color=A2, lw=1.2, ms=10)

    arrow(ax, 81, 56, 87, 58, color=A1, lw=2.0, ms=15)
    arrow_label(ax, 84, 59.5, "8 features", color=A1, fc=BG, mono=True)

    arrow(ax, 97, 58, 103, 58, color=A1, lw=1.8, ms=14)
    arrow_label(ax, 100, 60, "4-class", color=A1, fc=BG)

    arrow(ax, 114, 44, 121, 52, color="#a03030", lw=2.2, ms=15)
    arrow_label(ax, 117.5, 49, "IRQ", color="#a03030", fc="#fff5f5", mono=True)

    arrow(ax, 101, 28, 92, 52, color=A2, lw=1.0, rad=0.08, dashed=True, ms=10)
    arrow_label(ax, 95, 40, "weights via SPI", color=A2, fc=BG)

    # ── Footer ──
    ax.text(70, 10.5, "Total always-on power budget:  ~200-300 uW", ha="center", va="center",
            fontsize=9, color=C2, family=FONT)

    out_dir = Path(__file__).resolve().parent
    fig.savefig(out_dir / "system_block_diagram.png", dpi=DPI, bbox_inches="tight", facecolor=BG, pad_inches=0.28)
    fig.savefig(out_dir / "system_block_diagram.svg", bbox_inches="tight", facecolor=BG, pad_inches=0.28)
    plt.close(fig)


if __name__ == "__main__":
    main()
