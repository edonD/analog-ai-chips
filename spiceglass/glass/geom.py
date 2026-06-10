"""Symbol geometry shared by placer, router, renderer, and verifier.

All coordinates are SVG-style (y grows downward), relative to the
device origin (cell center). Pin positions are the contract: the
renderer must draw symbol artwork whose pins land exactly here, and
the router starts wires exactly here — the verifier exploits that.
"""
from __future__ import annotations

from .db import Device

COL_W = 190          # column pitch
ROW_H = 130          # row pitch
MARGIN = 90          # sheet margin
SECTION_GAP = 46     # extra gap between section groups

BOX_W = 132          # subckt instance box
BOX_PIN_DY = 22


def box_height(nports: int) -> int:
    side = (nports + 1) // 2
    return max(72, side * BOX_PIN_DY + 28)


def pin_offsets(dev: Device, mirror: bool = False) -> dict[str, tuple[float, float]]:
    """role -> (dx, dy) from device origin."""
    k = dev.kind
    if k in ("nmos", "pmos"):
        pins = {"g": (-30.0, 0.0), "b": (16.0, 0.0)}
        if k == "nmos":
            pins["d"] = (8.0, -38.0)
            pins["s"] = (8.0, 38.0)
        else:                       # PMOS drawn source-up (toward VDD)
            pins["s"] = (8.0, -38.0)
            pins["d"] = (8.0, 38.0)
        if mirror:
            pins = {r: (-dx, dy) for r, (dx, dy) in pins.items()}
        return {r: pins[r] for r in dev.roles if r in pins} | {
            r: pins.get(r, (16.0, 0.0)) for r in dev.roles}
    if k in ("res", "cap", "ind", "dio"):
        pins = {"p": (0.0, -38.0), "n": (0.0, 38.0), "b": (18.0, 0.0)}
        return {r: pins.get(r, (18.0, 0.0)) for r in dev.roles}
    if k in ("vsrc", "isrc", "bsrc"):
        return {r: {"p": (0.0, -38.0), "n": (0.0, 38.0)}.get(r, (18.0, 0.0))
                for r in dev.roles}
    if k in ("pnp", "npn"):
        pins = {"c": (10.0, -38.0), "b": (-30.0, 0.0), "e": (10.0, 38.0),
                "s": (18.0, 10.0)}
        return {r: pins.get(r, (18.0, 0.0)) for r in dev.roles}
    # subckt box / unknown: half the pins left, half right
    n = len(dev.roles)
    side = (n + 1) // 2
    h = box_height(n)
    out: dict[str, tuple[float, float]] = {}
    for i, role in enumerate(dev.roles):
        if i < side:
            y = -h / 2 + 24 + i * BOX_PIN_DY
            out[role] = (-BOX_W / 2, y)
        else:
            y = -h / 2 + 24 + (i - side) * BOX_PIN_DY
            out[role] = (BOX_W / 2, y)
    return out


def pin_pos(dev: Device, role: str, x: float, y: float,
            mirror: bool = False) -> tuple[float, float]:
    dx, dy = pin_offsets(dev, mirror)[role]
    return (x + dx, y + dy)
