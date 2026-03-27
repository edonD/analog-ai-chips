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

    draw_panel(
        ax,
        4,
        42,
        15,
        20,
        SENSOR,
        SENSOR_FILL,
        "01",
        "Sensor input",
        "",
        title_fs=9.5,
        sub_fs=7.4,
        badge_fs=7.2,
    )
    draw_card(
        ax,
        5.6,
        47.5,
        11.6,
        11.0,
        "MEMS\naccelerometer",
        SENSOR,
        lines=["ADXL355 or similar", "+/-2 g full scale", "+/-660 mV output"],
        meta="external",
        title_fs=8.8,
        fs=7.0,
    )
    ax.text(11.4, 44.8, "on rotating machine", ha="center", va="center", fontsize=7.0, color=MUTED)

    draw_panel(
        ax,
        27,
        38,
        56,
        32,
        ANALOG,
        ANALOG_FILL,
        "02",
        "Analog feature extraction",
        "Convert continuous vibration into 8 low-rate analog features",
    )
    draw_card(
        ax,
        29.0,
        52.0,
        9.0,
        11.5,
        "PGA",
        ANALOG,
        lines=["1x/4x/16x/64x", "normalizes input"],
        block="B02",
        meta="10 uW",
        fs=7.4,
        title_fs=9.8,
    )
    draw_card(
        ax,
        40.0,
        48.0,
        17.0,
        17.5,
        "BPF bank",
        ANALOG,
        lines=["5 spectral channels"],
        block="B03",
        meta="42.5 uW",
        fs=7.4,
        title_fs=9.8,
    )
    draw_card(
        ax,
        59.0,
        48.0,
        13.0,
        17.5,
        "Envelope\ndetectors",
        ANALOG,
        lines=["5x AC-to-DC", "rectify + LPF", "~10 Hz bandwidth"],
        block="B04",
        meta="5x21 uW",
        fs=7.0,
        title_fs=8.8,
    )
    draw_card(
        ax,
        40.0,
        39.8,
        32.0,
        6.0,
        "Broadband statistics",
        ANALOG,
        lines=["RMS | Crest | Kurtosis  (from PGA)"],
        block="B05",
        meta="8 uW",
        fs=7.4,
        title_fs=9.2,
    )
    draw_card(
        ax,
        74.0,
        46.5,
        7.0,
        19.0,
        "Feature\nvector",
        ANALOG,
        lines=["8 analog", "features"],
        fs=6.8,
        title_fs=8.0,
    )

    row_y = [61.8, 58.8, 55.8, 52.8, 49.8]
    band_labels = ["100-500 Hz", "0.5-2 kHz", "2-5 kHz", "5-10 kHz", "10-20 kHz"]
    for idx, (y, label) in enumerate(zip(row_y, band_labels), start=1):
        draw_mini_row(ax, 41.1, y, 14.6, 2.3, f"CH{idx}", label, ANALOG)

    for idx, (fx, fy, label) in enumerate(
        [
            (74.7, 60.9, "E1"),
            (77.9, 60.9, "E2"),
            (74.7, 57.8, "E3"),
            (77.9, 57.8, "E4"),
            (74.7, 54.7, "E5"),
            (77.9, 54.7, "RMS"),
            (74.7, 51.6, "Crest"),
            (77.9, 51.6, "Kurt."),
        ]
    ):
        draw_pill(ax, fx, fy, 2.4 if idx < 5 else 3.0, 1.25, label, "#dbe7ff" if idx < 5 else "#edf2f7", ANALOG if idx < 5 else TEXT)

    draw_panel(
        ax,
        85,
        38,
        14,
        32,
        CLASSIFIER,
        CLASSIFIER_FILL,
        "03",
        "Classifier",
        "Charge-domain MAC + WTA",
    )
    draw_card(
        ax,
        87.0,
        51.2,
        10.0,
        13.0,
        "Charge-domain\nMAC",
        CLASSIFIER,
        lines=["8x4 MAC array", "MIM cap weights", "winner-take-all"],
        block="B06",
        meta="<0.001 uW",
        fs=7.0,
        title_fs=9.0,
    )
    draw_card(
        ax,
        87.0,
        40.6,
        10.0,
        8.0,
        "Output classes",
        CLASSIFIER,
        lines=["4-way fault decision"],
        fs=7.0,
        title_fs=8.8,
    )
    draw_pill(ax, 87.8, 42.6, 3.0, 1.2, "Normal", "#eaf8f0", SENSOR)
    draw_pill(ax, 91.6, 42.6, 4.5, 1.2, "Imbalance", "#fff5db", "#9a6700")
    draw_pill(ax, 87.8, 40.9, 3.4, 1.2, "Bearing", "#fdeaea", ALERT)
    draw_pill(ax, 92.0, 40.9, 4.0, 1.2, "Looseness", "#fff0e5", "#b45309")

    draw_panel(
        ax,
        101,
        38,
        15,
        32,
        DIGITAL,
        DIGITAL_FILL,
        "04",
        "Wake logic",
        "SPI, debounce and IRQ path",
    )
    draw_card(
        ax,
        103.0,
        50.8,
        11.0,
        12.0,
        "Digital control",
        DIGITAL,
        lines=["SPI config", "debounce / FSM", "class latch + IRQ"],
        block="B08",
        meta="1.4 uW",
        fs=7.2,
        title_fs=9.0,
    )
    draw_card(
        ax,
        103.0,
        40.6,
        11.0,
        7.6,
        "Wake path",
        DIGITAL,
        lines=["assert IRQ", "wake host MCU"],
        fs=7.2,
        title_fs=9.0,
    )

    draw_panel(
        ax,
        121,
        42,
        15,
        20,
        SUPPORT,
        SUPPORT_FILL,
        "EXT",
        "Host MCU",
        "Wakes on IRQ",
    )
    draw_card(
        ax,
        123.0,
        48.2,
        10.8,
        9.4,
        "Host MCU\nand radio",
        SUPPORT,
        lines=["sleeps until IRQ", "reads on demand", "transmit anomaly"],
        fs=7.0,
        title_fs=8.8,
    )

    draw_card(
        ax,
        29.0,
        20.0,
        17.5,
        8.5,
        "Bias generator",
        SUPPORT,
        lines=["shared reference current"],
        block="B00",
        meta="0.97 uW",
        fs=7.4,
        title_fs=9.2,
    )
    draw_card(
        ax,
        48.8,
        20.0,
        17.5,
        8.5,
        "OTA building block",
        SUPPORT,
        lines=["reused in B02-B05"],
        block="B01",
        meta="0.90 uW ea",
        fs=7.4,
        title_fs=9.2,
    )
    draw_card(
        ax,
        68.6,
        20.0,
        17.5,
        8.5,
        "SAR ADC",
        ANALOG,
        lines=["8-bit on-demand readback"],
        block="B07",
        meta="28 uW act.",
        fs=7.4,
        title_fs=9.2,
    )
    draw_card(
        ax,
        88.4,
        20.0,
        26.0,
        8.5,
        "Offline training",
        OFFLINE,
        lines=["CWRU dataset, weights via SPI"],
        block="B09",
        meta="128 weights",
        fs=7.4,
        title_fs=9.2,
    )

    arrow(ax, 17.5, 53.6, 29.0, 57.8, color=SENSOR, lw=2.4, rad=0.0, ms=16)
    arrow_label(ax, 22.4, 56.9, "analog vibration", color=SENSOR, fc=BG)

    arrow(ax, 38.0, 57.8, 40.0, 57.8, color=ANALOG, lw=1.8, ms=13)
    arrow(ax, 57.0, 56.5, 59.0, 56.5, color=ANALOG, lw=1.8, ms=13)
    arrow(ax, 72.0, 56.5, 74.0, 56.0, color=ANALOG, lw=1.8, ms=13)
    arrow(ax, 34.0, 52.0, 45.0, 45.8, color=ANALOG, lw=1.5, rad=0.0, ms=12)
    arrow(ax, 72.0, 42.8, 74.0, 50.0, color=ANALOG, lw=1.5, rad=0.0, ms=12)

    arrow(ax, 81.0, 56.0, 87.0, 57.6, color=CLASSIFIER, lw=2.2, rad=0.0, ms=16)
    arrow_label(ax, 84.0, 59.8, "8 features", color=CLASSIFIER, fc=CLASSIFIER_FILL, mono=True)

    arrow(ax, 97.0, 57.6, 103.0, 57.0, color=DIGITAL, lw=2.1, ms=16)
    arrow_label(ax, 100.0, 59.8, "4-class result", color=DIGITAL, fc=DIGITAL_FILL)
    arrow(ax, 114.0, 44.4, 123.0, 52.6, color=ALERT, lw=2.4, ms=16)
    arrow_label(ax, 118.5, 49.7, "IRQ", color=ALERT, fc="#fff1ef", mono=True)

    arrow(ax, 101.5, 28.5, 92.0, 51.2, color=OFFLINE, lw=1.2, rad=0.10, dashed=True, ms=12)
    arrow_label(ax, 95.6, 40.0, "weights via SPI", color=OFFLINE, fc=BG)

    ax.text(
        26.6,
        17.2,
        "Bias and OTA support are shown without internal bias nets to keep the architecture readable.",
        ha="left",
        va="center",
        fontsize=8.0,
        color=MUTED,
    )

    ax.text(26.6, 10.2, "Legend:", ha="left", va="center", fontsize=8.3, color=MUTED, weight="bold")
    draw_pill(ax, 31.4, 9.65, 6.5, 1.15, "external", SENSOR_FILL, SENSOR)
    draw_pill(ax, 39.0, 9.65, 8.6, 1.15, "analog core", ANALOG_FILL, ANALOG)
    draw_pill(ax, 48.5, 9.65, 8.0, 1.15, "classifier", CLASSIFIER_FILL, CLASSIFIER)
    draw_pill(ax, 57.5, 9.65, 6.8, 1.15, "digital", DIGITAL_FILL, DIGITAL)
    draw_pill(ax, 65.4, 9.65, 12.2, 1.15, "support / offline", SUPPORT_FILL, SUPPORT)
    ax.text(116.0, 10.2, "Main always-on budget: ~200-300 uW", ha="right", va="center", fontsize=8.3, color=MUTED)

    out_dir = Path(__file__).resolve().parent
    fig.savefig(out_dir / "system_block_diagram.png", dpi=DPI, bbox_inches="tight", facecolor=BG, pad_inches=0.28)
    fig.savefig(out_dir / "system_block_diagram.svg", bbox_inches="tight", facecolor=BG, pad_inches=0.28)
    plt.close(fig)


if __name__ == "__main__":
    main()
