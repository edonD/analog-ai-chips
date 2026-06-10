"""Branch-column analog placer — the moat.

Encodes how analog designers actually draw schematics:

1. Rails fold away (VDD top, GND bottom — stubs, not wires).
2. Every VDD→GND source-drain path is a vertical column:
   PMOS at the top, NMOS/res at the bottom.
3. Columns are ordered left→right by the netlist's own narrative order
   (AI-written netlists are ordered logically) grouped by the LLM's
   section comments, which we treat as placement clusters.
4. Vertical position is anchored globally: devices that can reach GND
   through channels sit at row (H-1 - level_from_gnd), so the sources
   of a differential pair, mirror transistors, and rail devices align
   automatically across columns.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .classify import rails_of
from .db import Device, Subckt
from .geom import COL_PITCH, MARGIN, ROW0_OFFSET, ROW_PITCH, SECTION_GAP

LABEL_FANOUT = 5     # nets with >= this many terminals become named stubs


@dataclass
class Placed:
    dev: Device
    col: int = 0
    row: int = 0
    x: int = 0          # grid units
    y: int = 0          # grid units
    mirror: bool = False


@dataclass
class Sheet:
    sub: Subckt
    placed: dict[str, Placed] = field(default_factory=dict)   # by device name
    rails: dict[str, str] = field(default_factory=dict)       # net -> vdd|gnd
    label_nets: set[str] = field(default_factory=set)
    columns: list[list[Device]] = field(default_factory=list)
    col_section: list[str] = field(default_factory=list)
    width: int = 0      # grid units
    height: int = 0     # grid units
    rows: int = 0

    def pos(self, dev: Device) -> Placed:
        return self.placed[dev.name]


def _channel(dev: Device) -> tuple[str, str] | None:
    return dev.channel_nets()


def place(sub: Subckt) -> Sheet:
    sheet = Sheet(sub=sub)
    sheet.rails = rails_of(sub)
    rails = sheet.rails
    devices = sub.devices

    # ---- label nets: high fanout → stubs instead of routed wires
    for net in sub.nets():
        if net in rails:
            continue
        if sub.fanout(net) >= LABEL_FANOUT:
            sheet.label_nets.add(net)

    # ---- channel index: net -> devices having a channel terminal there
    chan_at: dict[str, list[Device]] = {}
    for d in devices:
        ch = _channel(d)
        if not ch:
            continue
        for n in ch:
            if n is not None:
                chan_at.setdefault(n, []).append(d)

    # ---- net distance maps to both rails through channel edges (computed
    #      BEFORE column growth: the walker only chains a step that makes
    #      monotonic progress toward the opposite rail — that is what
    #      separates a series stack from a lateral switch or pair member)
    def _bfs(rail_kind: str) -> dict[str, int]:
        dist: dict[str, int] = {n: 0 for n, k in rails.items() if k == rail_kind}
        frontier = list(dist)
        while frontier:
            nxt = []
            for n in frontier:
                for d in chan_at.get(n, []):
                    ch = _channel(d)
                    other = ch[0] if ch[1] == n else ch[1]
                    if other is None or other in rails:
                        continue
                    if other not in dist or dist[other] > dist[n] + 1:
                        dist[other] = dist[n] + 1
                        nxt.append(other)
            frontier = nxt
        return dist

    level = _bfs("gnd")          # also anchors rows later
    level_vdd = _bfs("vdd")

    used: set[str] = set()
    columns: list[list[Device]] = []

    def grow(seed: Device, start_net: str, downward: bool) -> list[Device]:
        """Walk series chains from a rail-touching seed."""
        target = level if downward else level_vdd     # distance to shrink
        col = [seed]
        used.add(seed.name)
        ch = _channel(seed)
        cur = ch[0] if ch[1] == start_net else ch[1]
        while cur is not None and cur not in rails:
            here = target.get(cur, 99)

            def progress(c: Device) -> int | None:
                ch_c = _channel(c)
                other = ch_c[0] if ch_c[1] == cur else ch_c[1]
                if other in rails:
                    want = "gnd" if downward else "vdd"
                    return 0 if rails[other] == want else None
                d = target.get(other, 99)
                return d if d < here else None        # monotonic only

            cands = [(c, progress(c)) for c in chan_at.get(cur, [])
                     if c.name not in used]
            cands = [(c, p) for c, p in cands if p is not None]
            if not cands:
                break
            prev = col[-1]
            def score(cp) -> tuple:
                c, p = cp
                same_sec = 0 if (c.section and c.section == prev.section) else 1
                kindpref = {"nmos": 0, "pmos": 0, "res": 1, "dio": 1,
                            "bsrc": 2, "cap": 3}.get(c.kind, 4)
                return (same_sec, p, kindpref, c.line)
            nxt = min(cands, key=score)[0]
            col.append(nxt)
            used.add(nxt.name)
            ch = _channel(nxt)
            cur = ch[0] if ch[1] == cur else ch[1]
        return col

    # 1) VDD-anchored columns, netlist order
    for d in devices:
        if d.name in used:
            continue
        ch = _channel(d)
        if not ch:
            continue
        vdd_terms = [n for n in ch if n in rails and rails[n] == "vdd"]
        if vdd_terms:
            columns.append(grow(d, vdd_terms[0], downward=True))

    # 2) GND-anchored columns for the rest (leakers, startup R, B-sources…)
    for d in devices:
        if d.name in used:
            continue
        ch = _channel(d)
        if not ch:
            continue
        gnd_terms = [n for n in ch if n in rails and rails[n] == "gnd"]
        if gnd_terms:
            col = grow(d, gnd_terms[0], downward=False)
            columns.append(list(reversed(col)))   # store top→bottom

    # 3) lateral devices (both channel nets internal) and boxes / leftovers
    for d in devices:
        if d.name not in used:
            columns.append([d])
            used.add(d.name)

    # ---- rows
    maxlevel = max(level.values(), default=1)
    rows = max(maxlevel + 1, max((len(c) for c in columns), default=1), 2)
    sheet.rows = rows

    def assign_rows(col: list[Device]) -> None:
        top_i = 0
        for i, d in enumerate(col):
            ch = _channel(d)
            if ch and any(n in sheet.rails and sheet.rails[n] == "vdd" for n in ch):
                # top-anchored chain from VDD keeps walk order
                row = top_i
                top_i += 1
            elif ch:
                lvls = [level[n] for n in ch if n in level]
                if lvls:
                    row = rows - 1 - min(lvls)
                else:
                    row = min(i, rows - 1)
                top_i = row + 1
            else:                      # boxes: middle band, stack downward
                row = min(1 + i, rows - 1)
            sheet.placed[d.name] = Placed(dev=d, row=row)

    for col in columns:
        assign_rows(col)

    # resolve collisions within a column (two devices landing on one row)
    for col in columns:
        taken: dict[int, int] = {}
        for d in col:
            p = sheet.placed[d.name]
            while p.row in taken:
                p.row -= 1 if p.row > 0 else -1
            taken[p.row] = 1

    # ---- column x-order: section appearance order, then first line
    sec_order = {s: i for i, s in enumerate(sub.sections)}
    def col_key(col: list[Device]) -> tuple:
        first = col[0]
        sec = sec_order.get(first.section, len(sec_order))
        return (sec, first.line)
    columns.sort(key=col_key)
    sheet.columns = columns
    sheet.col_section = [c[0].section for c in columns]

    # ---- grid coordinates (extra gap whenever the section changes)
    x = MARGIN + COL_PITCH // 2
    prev_sec = None
    for ci, col in enumerate(columns):
        sec = sheet.col_section[ci]
        if prev_sec is not None and sec != prev_sec:
            x += SECTION_GAP
        prev_sec = sec
        for d in col:
            p = sheet.placed[d.name]
            p.col = ci
            p.x = x
            p.y = MARGIN + ROW0_OFFSET + p.row * ROW_PITCH
        x += COL_PITCH

    sheet.width = x + MARGIN
    sheet.height = MARGIN + ROW0_OFFSET + (rows - 1) * ROW_PITCH + MARGIN + 4

    # ---- gate orientation: face the gate toward its net's nearest column
    for d in devices:
        if d.kind not in ("nmos", "pmos"):
            continue
        g = d.net_of("g")
        if g is None or g in sheet.rails or g in sheet.label_nets:
            continue
        p = sheet.placed[d.name]
        xs = [sheet.placed[o.name].x for o, r in sub.terminals(g)
              if o.name != d.name and o.name in sheet.placed]
        if xs and sum(xs) / len(xs) > p.x:
            p.mirror = True
    return sheet
