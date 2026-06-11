"""Routing/placement quality metrics — the objective function.

Counts what actually hurts schematic readability (graph-drawing
aesthetics literature: crossings worst, then bends, then length):

  wirelength  total Manhattan length of drawn segments (grid units)
  bends       corner points (exactly one H + one V segment of a net meet)
  crossings   interior intersections of different-net segments
  through     segments cutting through a symbol tile's interior
  area        sheet bounding box (kilo-units²)

Used to compare router versions and to diff algorithmic placement
against saved human edits (the adaptation loop).
"""
from __future__ import annotations

from dataclasses import dataclass

from .geom import BOX_W, box_height, pin_offsets
from .place import Sheet
from .route import Routing, Seg


@dataclass
class Score:
    wirelength: int = 0
    bends: int = 0
    crossings: int = 0
    through: int = 0
    area_ku2: float = 0.0
    segments: int = 0

    def row(self) -> str:
        return (f"len={self.wirelength}mm  bends={self.bends}  "
                f"crossings={self.crossings}  through={self.through}  "
                f"area={self.area_ku2:.0f}cm²  segs={self.segments}")


def _is_h(s: Seg) -> bool:
    return s.y1 == s.y2


def _bbox(dev, p) -> tuple[int, int, int, int]:
    """Conservative symbol-interior box (grid units, exclusive of pins)."""
    k = dev.kind
    if k in ("nmos", "pmos"):
        x0, x1 = (-3, 3)
    elif k in ("res", "cap", "ind", "dio", "vsrc", "isrc", "bsrc"):
        x0, x1 = (-2, 2)
    elif k in ("pnp", "npn"):
        x0, x1 = (-3, 3)
    else:
        w = BOX_W // 2
        h = box_height(len(dev.roles)) // 2
        return (p.x - w + 1, p.y - h + 1, p.x + w - 1, p.y + h - 1)
    y0, y1 = -3, 3
    from .geom import ROTATED
    if p.orient in ROTATED:
        x0, x1, y0, y1 = y0, y1, x0, x1
    return (p.x + x0 + 1, p.y + y0 + 1, p.x + x1 - 1, p.y + y1 - 1)


def score(sheet: Sheet, routing: Routing) -> Score:
    from .geom import GRID_MM
    sc = Score()
    segs = routing.segments
    sc.segments = len(segs)
    # physical sheet area in cm² (1 unit = GRID_MM mm)
    sc.area_ku2 = sheet.width * sheet.height * GRID_MM * GRID_MM / 100.0

    # wirelength
    for s in segs:
        sc.wirelength += abs(s.x2 - s.x1) + abs(s.y2 - s.y1)

    # bends: points where exactly one H and one V segment of a net meet
    pts: dict[tuple[str, int, int], list[bool]] = {}
    for s in segs:
        for (x, y) in ((s.x1, s.y1), (s.x2, s.y2)):
            pts.setdefault((s.net, x, y), []).append(_is_h(s))
    for orientations in pts.values():
        if len(orientations) == 2 and orientations[0] != orientations[1]:
            sc.bends += 1

    # crossings: interior H×V intersections between different nets
    hs = [s for s in segs if _is_h(s)]
    vs = [s for s in segs if not _is_h(s)]
    for h in hs:
        hx0, hx1 = min(h.x1, h.x2), max(h.x1, h.x2)
        for v in vs:
            if v.net == h.net:
                continue
            vy0, vy1 = min(v.y1, v.y2), max(v.y1, v.y2)
            if hx0 < v.x1 < hx1 and vy0 < h.y1 < vy1:
                sc.crossings += 1

    # wires cutting through symbol interiors
    boxes = []
    for d in sheet.sub.devices:
        p = sheet.pos(d)
        boxes.append((d.name, _bbox(d, p)))
    pin_owner: dict[str, set[str]] = {}
    for d in sheet.sub.devices:
        for net in d.nets:
            pin_owner.setdefault(net, set()).add(d.name)
    for s in segs:
        sx0, sx1 = min(s.x1, s.x2), max(s.x1, s.x2)
        sy0, sy1 = min(s.y1, s.y2), max(s.y1, s.y2)
        for name, (bx0, by0, bx1, by1) in boxes:
            if name in pin_owner.get(s.net, ()):  # its own wires may touch
                continue
            if sx1 < bx0 or sx0 > bx1 or sy1 < by0 or sy0 > by1:
                continue
            ox = min(sx1, bx1) - max(sx0, bx0)
            oy = min(sy1, by1) - max(sy0, by0)
            if ox > 0 or oy > 0:
                sc.through += 1
                break
    return sc
