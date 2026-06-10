"""Grid-native symbol geometry — the systematic core.

Everything in this pipeline thinks in INTEGER GRID UNITS:
  * every symbol is a footprint tile of whole units,
  * every pin sits exactly on a grid crossing,
  * placement positions device origins on grid crossings,
  * routing tracks are integer grid lines,
  * verification compares integer coordinates exactly (no epsilons).
Pixels exist only at the render boundary (UNIT px per grid unit), which
is also what will make xschem/.sch export a pure scale factor.

Pin positions are the contract: renderer artwork must land its pins
exactly here, the router starts wires exactly here, and the verifier
exploits that exactness.
"""
from __future__ import annotations

from .db import Device

UNIT = 10            # px per grid unit (render scale only)

COL_PITCH = 18       # units between column centers
ROW_PITCH = 14       # units between row centers   (symbol is 8 tall -> 6 tracks free)
MARGIN = 8           # sheet margin, units
SECTION_GAP = 5      # extra units between section groups
ROW0_OFFSET = 7      # units from top margin to row-0 center

BOX_W = 12           # subckt instance box width, units
BOX_PIN_DY = 2       # vertical pin spacing on box edges, units


def box_height(nports: int) -> int:
    """Box height in units (even, pins on-grid)."""
    side = (nports + 1) // 2
    return max(8, 2 * side + 4)


TILE_PITCH = 10      # member spacing inside composite tiles, units


def _orient(pins: dict[str, tuple[int, int]], orient: str) -> dict:
    if orient == "MX":      # mirror about the through-axis (x=0)
        return {r: (-dx, dy) for r, (dx, dy) in pins.items()}
    if orient == "R90":     # lay flat: (dx,dy) -> (dy,-dx)
        return {r: (dy, -dx) for r, (dx, dy) in pins.items()}
    return pins


def pin_offsets(dev: Device, orient: str = "R0") -> dict[str, tuple[int, int]]:
    """role -> (dx, dy) from device origin, in integer grid units.

    THROUGH-AXIS RULE: every series terminal (D/S, P/N) sits on x=0 so
    any series chain renders as one straight vertical line — symbol
    artwork is asymmetric around the axis, pins are not.
    """
    k = dev.kind
    if k in ("nmos", "pmos"):
        pins = {"g": (-3, 0), "b": (3, 0)}
        if k == "nmos":
            pins["d"] = (0, -4)
            pins["s"] = (0, 4)
        else:                       # PMOS drawn source-up (toward VDD)
            pins["s"] = (0, -4)
            pins["d"] = (0, 4)
        pins = _orient(pins, orient)
        return {r: pins.get(r, (3, 0)) for r in dev.roles}
    if k in ("res", "cap", "ind", "dio", "vsrc", "isrc", "bsrc"):
        pins = _orient({"p": (0, -4), "n": (0, 4), "b": (2, 0)}, orient)
        return {r: pins.get(r, (2, 0)) for r in dev.roles}
    if k in ("pnp", "npn"):
        pins = _orient({"c": (0, -4), "b": (-3, 0), "e": (0, 4), "s": (3, 1)},
                       orient)
        return {r: pins.get(r, (2, 0)) for r in dev.roles}
    # subckt box / unknown: half the pins left, half right, on-grid
    n = len(dev.roles)
    side = (n + 1) // 2
    h = box_height(n)
    out: dict[str, tuple[int, int]] = {}
    for i, role in enumerate(dev.roles):
        if i < side:
            out[role] = (-BOX_W // 2, -h // 2 + 2 + i * BOX_PIN_DY)
        else:
            out[role] = (BOX_W // 2, -h // 2 + 2 + (i - side) * BOX_PIN_DY)
    return out


def pin_pos(dev: Device, role: str, x: int, y: int,
            orient: str = "R0") -> tuple[int, int]:
    dx, dy = pin_offsets(dev, orient)[role]
    return (x + dx, y + dy)
