"""User-editable symbol artwork library.

The symbol designer page saves per-kind artwork (lines/circles/polylines
in px, drawn on a 0.5-unit snap grid) to symbols.json next to the
package. Renderers check this library before the built-in artwork.
Pins are NOT editable — they are the grid contract in glass.geom.
"""
from __future__ import annotations

import json
import os

_PATH = os.path.join(os.path.dirname(__file__), "..", "symbols.json")
_cache: dict | None = None
_mtime: float = -1.0


def lib() -> dict:
    """kind -> list of element dicts. Reloads when the file changes."""
    global _cache, _mtime
    try:
        m = os.path.getmtime(_PATH)
    except OSError:
        _cache = {}
        return _cache
    if _cache is None or m != _mtime:
        with open(_PATH, encoding="utf-8") as fh:
            _cache = json.load(fh)
        _mtime = m
    return _cache


def save(kind: str, elems: list[dict] | None) -> str:
    data = lib().copy()
    if elems is None:
        data.pop(kind, None)
    else:
        data[kind] = elems
    with open(_PATH, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
    global _cache, _mtime
    _cache = None
    return _PATH


def to_svg(elems: list[dict]) -> list[str]:
    out = []
    for e in elems:
        sw = 2.6 if e.get("thick") else 1.8
        t = e.get("t")
        if t == "line":
            out.append(f'<line x1="{e["x1"]}" y1="{e["y1"]}" x2="{e["x2"]}" '
                       f'y2="{e["y2"]}" stroke-width="{sw}"/>')
        elif t == "circle":
            out.append(f'<circle cx="{e["cx"]}" cy="{e["cy"]}" r="{e["r"]}" '
                       f'fill="white" stroke-width="{sw}"/>')
        elif t == "dot":
            out.append(f'<circle cx="{e["cx"]}" cy="{e["cy"]}" r="{e["r"]}" '
                       f'stroke="none"/>')
    return out
