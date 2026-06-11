"""Headless SVG -> PNG via Edge (for vision-model feedback)."""
from __future__ import annotations

import os
import re
import subprocess
import tempfile

_EDGE = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def edge_path() -> str | None:
    return next((p for p in _EDGE if os.path.exists(p)), None)


def svg_to_png_bytes(svg_text: str, max_w: int = 1800) -> bytes | None:
    edge = edge_path()
    if edge is None:
        return None
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg_text[:600])
    w, h = (int(m.group(1)), int(m.group(2))) if m else (1600, 1000)
    scale = min(1.0, max_w / max(w, 1))
    w, h = int(w * scale) or 1, int(h * scale) or 1
    with tempfile.TemporaryDirectory() as td:
        svg = os.path.join(td, "sheet.svg")
        png = os.path.join(td, "sheet.png")
        with open(svg, "w", encoding="utf-8") as fh:
            fh.write(svg_text)
        url = "file:///" + svg.replace("\\", "/")
        try:
            subprocess.run(
                [edge, "--headless=new", "--disable-gpu",
                 f"--screenshot={png}", f"--window-size={w},{h}",
                 "--virtual-time-budget=3000", url],
                capture_output=True, timeout=60, check=False)
            with open(png, "rb") as fh:
                return fh.read()
        except (OSError, subprocess.TimeoutExpired):
            return None
