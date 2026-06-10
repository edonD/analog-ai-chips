"""Orthogonal Visibility Graph (Wybrow/Marriott/Stuckey, GD 2009).

Instead of a full routing grid, visibility lines are projected only
through obstacle-rectangle sides and pin positions — "maze running on a
non-uniform grid whose mesh size is tailored to the geometry of the
diagram" (the authors' own description). Nodes are intersections of
free horizontal and vertical visibility intervals; pins attach as
portal nodes with a single escape edge out of their symbol's buffer.

All coordinates are integer grid units.
"""
from __future__ import annotations

from bisect import bisect_left, bisect_right, insort
from dataclasses import dataclass, field

H, V = 0, 1


@dataclass
class OVG:
    coords: list[tuple[int, int]] = field(default_factory=list)
    ids: dict[tuple[int, int], int] = field(default_factory=dict)
    adj: dict[int, list[tuple[int, int]]] = field(default_factory=dict)
    # visualization data
    rects: list[tuple[int, int, int, int]] = field(default_factory=list)
    vspans: list[tuple[int, int, int]] = field(default_factory=list)  # x,y0,y1
    hspans: list[tuple[int, int, int]] = field(default_factory=list)  # y,x0,x1

    def node(self, x: int, y: int) -> int:
        key = (x, y)
        nid = self.ids.get(key)
        if nid is None:
            nid = len(self.coords)
            self.ids[key] = nid
            self.coords.append(key)
            self.adj[nid] = []
        return nid

    def edge(self, a: int, b: int, axis: int) -> None:
        if b not in [n for n, _ in self.adj[a]]:
            self.adj[a].append((b, axis))
            self.adj[b].append((a, axis))


def _free_intervals(span: tuple[int, int],
                    blocks: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Subtract open block intervals from a closed span."""
    lo, hi = span
    out = []
    cur = lo
    for b0, b1 in sorted(blocks):
        if b1 <= cur:
            continue
        if b0 > hi:
            break
        if b0 > cur:
            out.append((cur, min(b0, hi)))
        cur = max(cur, b1)
        if cur >= hi:
            break
    if cur < hi:
        out.append((cur, hi))
    return [(a, b) for a, b in out if b >= a]


def build_ovg(rects: list[tuple[int, int, int, int]],
              pins: list[tuple[int, int, str]],
              bounds: tuple[int, int, int, int]) -> tuple[OVG, dict]:
    """rects: blocked rectangles (interiors are strictly blocked; lines on
    the boundary are allowed). pins: (x, y, escape) with escape L|R|U|D.
    Returns (ovg, pin_nodes: {(x,y) -> node_id})."""
    bx0, by0, bx1, by1 = bounds
    g = OVG(rects=list(rects))

    vxs = {bx0, bx1}
    hys = {by0, by1}
    for (x0, y0, x1, y1) in rects:
        vxs.update((x0, x1))
        hys.update((y0, y1))
    for (px, py, esc) in pins:
        if esc in ("U", "D"):
            vxs.add(px)
        else:
            hys.add(py)

    def vblocks(x: int) -> list[tuple[int, int]]:
        return [(y0, y1) for (x0, y0, x1, y1) in rects if x0 < x < x1]

    def hblocks(y: int) -> list[tuple[int, int]]:
        return [(x0, x1) for (x0, y0, x1, y1) in rects if y0 < y < y1]

    vfree = {x: _free_intervals((by0, by1), vblocks(x)) for x in sorted(vxs)}
    hfree = {y: _free_intervals((bx0, bx1), hblocks(y)) for y in sorted(hys)}
    for x, spans in vfree.items():
        for (a, b) in spans:
            g.vspans.append((x, a, b))
    for y, spans in hfree.items():
        for (a, b) in spans:
            g.hspans.append((y, a, b))

    def on_v(x: int, y: int) -> bool:
        return any(a <= y <= b for a, b in vfree.get(x, ()))

    def on_h(x: int, y: int) -> bool:
        return any(a <= x <= b for a, b in hfree.get(y, ()))

    # nodes at valid intersections; edges along each free interval
    per_v: dict[int, list[int]] = {x: [] for x in vfree}
    per_h: dict[int, list[int]] = {y: [] for y in hfree}
    for x in vfree:
        for y in hfree:
            if on_v(x, y) and on_h(x, y):
                per_v[x].append(y)
                per_h[y].append(x)

    for x, ys in per_v.items():
        ys.sort()
        for y1_, y2_ in zip(ys, ys[1:]):
            # consecutive nodes must share one free interval
            if any(a <= y1_ and y2_ <= b for a, b in vfree[x]):
                g.edge(g.node(x, y1_), g.node(x, y2_), V)
    for y, xs in per_h.items():
        xs.sort()
        for x1_, x2_ in zip(xs, xs[1:]):
            if any(a <= x1_ and x2_ <= b for a, b in hfree[y]):
                g.edge(g.node(y=y, x=x1_), g.node(y=y, x=x2_), H)

    # pin portals: one escape edge from the pin to the nearest node
    # outside its symbol buffer, along the escape direction
    pin_nodes: dict[tuple[int, int], int] = {}
    for (px, py, esc) in pins:
        pid = g.node(px, py)
        pin_nodes[(px, py)] = pid
        if esc in ("U", "D"):
            ys = per_v.get(px, [])
            if esc == "U":
                cands = [y for y in ys if y < py]
                tgt = max(cands) if cands else None
            else:
                cands = [y for y in ys if y > py]
                tgt = min(cands) if cands else None
            if tgt is not None:
                g.edge(pid, g.node(px, tgt), V)
        else:
            xs = per_h.get(py, [])
            if esc == "L":
                cands = [x for x in xs if x < px]
                tgt = max(cands) if cands else None
            else:
                cands = [x for x in xs if x > px]
                tgt = min(cands) if cands else None
            if tgt is not None:
                g.edge(pid, g.node(tgt, py), H)
    return g, pin_nodes
