"""Round-trip verifier — turns a picture into a proof.

Rebuilds connectivity purely from the drawn geometry (wire segments,
rail stubs, net labels) and compares the resulting terminal grouping
against the input netlist. Catches router bugs both ways:
opens (net split into pieces) and shorts (distinct nets touching,
including collinear overlaps).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .route import Routing, Seg

EPS = 0.25


@dataclass
class VerifyResult:
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    n_terminals: int = 0
    n_nets: int = 0


class _UF:
    def __init__(self) -> None:
        self.p: dict[str, str] = {}

    def find(self, a: str) -> str:
        self.p.setdefault(a, a)
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def _key(x: float, y: float) -> str:
    return f"{round(x, 1)}:{round(y, 1)}"


def _on_segment(x: float, y: float, s: Seg) -> bool:
    if abs(s.x1 - s.x2) < EPS:                       # vertical
        return (abs(x - s.x1) < EPS and
                min(s.y1, s.y2) - EPS <= y <= max(s.y1, s.y2) + EPS)
    if abs(s.y1 - s.y2) < EPS:                       # horizontal
        return (abs(y - s.y1) < EPS and
                min(s.x1, s.x2) - EPS <= x <= max(s.x1, s.x2) + EPS)
    return False


def verify(routing: Routing) -> VerifyResult:
    res = VerifyResult(ok=True)
    uf = _UF()

    segs = routing.segments
    for s in segs:
        uf.union(_key(s.x1, s.y1), _key(s.x2, s.y2))

    # T-joins: an endpoint lying on another segment's body
    endpoints = []
    for s in segs:
        endpoints.append((s.x1, s.y1, s))
        endpoints.append((s.x2, s.y2, s))
    for (x, y, owner) in endpoints:
        for s in segs:
            if s is owner:
                continue
            if _on_segment(x, y, s):
                uf.union(_key(x, y), _key(s.x1, s.y1))

    # stubs bind pins to virtual rail/label nodes
    for st in routing.stubs:
        if st.kind in ("vdd", "gnd"):
            uf.union(_key(st.px, st.py), f"RAIL:{st.net}")
        else:
            uf.union(_key(st.px, st.py), f"LBL:{st.text}")

    # ---- group terminals by geometric component
    comp_nets: dict[str, set[str]] = {}
    net_comps: dict[str, set[str]] = {}
    for t in routing.terminals:
        c = uf.find(_key(t.x, t.y))
        comp_nets.setdefault(c, set()).add(t.net)
        net_comps.setdefault(t.net, set()).add(c)
    res.n_terminals = len(routing.terminals)
    res.n_nets = len(net_comps)

    # shorts: one geometric component, two netlist nets
    for c, nets in comp_nets.items():
        if len(nets) > 1:
            res.ok = False
            res.errors.append("SHORT: drawn geometry connects nets "
                              + ", ".join(sorted(nets)))
    # virtual collisions (e.g. vdd stub unioned into gnd structure)
    seen_virtual: dict[str, str] = {}
    for v in list(uf.p):
        if v.startswith(("RAIL:", "LBL:")):
            c = uf.find(v)
            if c in seen_virtual and seen_virtual[c] != v:
                res.ok = False
                res.errors.append(f"SHORT: {seen_virtual[c]} touches {v}")
            else:
                seen_virtual[c] = v

    # opens: a net whose terminals ended up in 2+ components
    for net, comps in net_comps.items():
        if len(comps) > 1:
            res.ok = False
            res.errors.append(f"OPEN: net '{net}' split into {len(comps)} pieces")

    # collinear overlap between different nets = invisible short
    for i, a in enumerate(segs):
        for b in segs[i + 1:]:
            if a.net == b.net:
                continue
            if _overlap(a, b):
                res.ok = False
                res.errors.append(
                    f"SHORT (overlap): '{a.net}' and '{b.net}' share a track")

    for t in routing.dangling:
        res.warnings.append(f"dangling: {t.dev}.{t.role} (net '{t.net}')")
    return res


def _overlap(a: Seg, b: Seg) -> bool:
    av = abs(a.x1 - a.x2) < EPS
    bv = abs(b.x1 - b.x2) < EPS
    if av != bv:
        return False
    if av:                                            # both vertical
        if abs(a.x1 - b.x1) > EPS:
            return False
        lo = max(min(a.y1, a.y2), min(b.y1, b.y2))
        hi = min(max(a.y1, a.y2), max(b.y1, b.y2))
        return hi - lo > EPS
    if abs(a.y1 - b.y1) > EPS:
        return False
    lo = max(min(a.x1, a.x2), min(b.x1, b.x2))
    hi = min(max(a.x1, a.x2), max(b.x1, b.x2))
    return hi - lo > EPS
