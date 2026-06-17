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

from .engine.db import Device

UNIT = 10            # px per grid unit (screen render scale only)

# THE PHYSICAL GRID. 1 grid unit = GRID_MM millimetres. Every pin, device
# origin, wire segment, routing track and nudge offset is an integer
# number of grid units by construction (the verifier compares exact
# integers), so the entire design sits on this grid — change GRID_MM to
# rescale the whole system (finer/coarser grids later).
GRID_MM = 1.0


def set_grid_mm(mm: float) -> None:
    global GRID_MM
    GRID_MM = float(mm)

COL_PITCH = 18       # units between column centers
ROW_PITCH = 14       # units between row centers   (symbol is 8 tall -> 6 tracks free)
MARGIN = 8           # sheet margin, units
SECTION_GAP = 5      # extra units between section groups
ROW0_OFFSET = 7      # units from top margin to row-0 center

BOX_W = 12           # subckt instance box width, units
BOX_PIN_DY = 2       # vertical pin spacing on box edges, units


def box_height(nports: int) -> int:
    """Box height in units, sized to hug the pin column + margin."""
    side = (nports + 1) // 2
    return max(6, (side - 1) * BOX_PIN_DY + 4)


TILE_PITCH = 10      # member spacing inside composite tiles, units


# The 8-element orientation group of the square (LTspice/OpenAccess
# convention). Pin transform and the matching SVG transform string MUST
# stay in lockstep — router and verifier trust the pin algebra, the
# renderers draw with the strings.
ORIENTS = ("R0", "R90", "R180", "R270", "MX", "MY", "MX90", "MY90")

ORIENT_TF = {
    "R0": "", "R90": " rotate(-90)", "R180": " rotate(180)",
    "R270": " rotate(90)", "MX": " scale(-1 1)", "MY": " scale(1 -1)",
    "MX90": " rotate(-90) scale(-1 1)",
    "MY90": " rotate(-90) scale(1 -1)",
}

ROTATED = {"R90", "R270", "MX90", "MY90"}    # width/height swap


def orient_xy(dx: int, dy: int, orient: str) -> tuple[int, int]:
    if orient == "R90":
        return (dy, -dx)
    if orient == "R180":
        return (-dx, -dy)
    if orient == "R270":
        return (-dy, dx)
    if orient == "MX":
        return (-dx, dy)
    if orient == "MY":
        return (dx, -dy)
    if orient == "MX90":
        return (dy, dx)
    if orient == "MY90":
        return (-dy, -dx)
    return (dx, dy)


def _orient(pins: dict[str, tuple[int, int]], orient: str) -> dict:
    if orient == "R0":
        return pins
    return {r: orient_xy(dx, dy, orient) for r, (dx, dy) in pins.items()}


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
    # subckt box / unknown: half the pins left, half right, each column
    # vertically CENTRED about the origin so the box looks balanced
    n = len(dev.roles)
    side = (n + 1) // 2          # left column count (rest go right)

    def col_ys(count: int) -> list[int]:
        start = -((count - 1) * BOX_PIN_DY) // 2
        return [start + i * BOX_PIN_DY for i in range(count)]
    lys, rys = col_ys(side), col_ys(n - side)
    out: dict[str, tuple[int, int]] = {}
    for i, role in enumerate(dev.roles):
        out[role] = ((-BOX_W // 2, lys[i]) if i < side
                     else (BOX_W // 2, rys[i - side]))
    return out


def pin_pos(dev: Device, role: str, x: int, y: int,
            orient: str = "R0") -> tuple[int, int]:
    dx, dy = pin_offsets(dev, orient)[role]
    return (x + dx, y + dy)
