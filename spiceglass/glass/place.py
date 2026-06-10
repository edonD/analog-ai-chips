"""Branch-column analog placer with composite tiles.

Drawing conventions encoded:
1. Rails fold away (VDD top, GND bottom — stubs, not wires).
2. Recognized structures (mirror banks, diff pairs, 5T cores, diode
   links) are placed as TILES whose defining wires are pre-routed
   inside the tile — the placer moves objects, never relationships.
3. Remaining devices form series columns: every step must make
   monotonic progress toward the opposite rail (separates series
   stacks from lateral switches and pair members).
4. Lateral leftovers (both channel nets internal) lie flat (R90).
5. Columns/tiles are ordered by the netlist's own narrative order,
   grouped by the LLM's section comments.
6. Rows anchor to rail distance so related devices align across
   columns automatically.

All coordinates are integer grid units (see glass.geom).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .classify import rails_of
from .db import Device, Subckt
from .geom import (COL_PITCH, MARGIN, ROW0_OFFSET, ROW_PITCH, SECTION_GAP,
                   TILE_PITCH)
from .recognize import Tile, recognize

LABEL_FANOUT = 5     # nets with >= this many drawn endpoints become stubs


@dataclass
class Placed:
    dev: Device
    col: int = 0
    row: int = 0
    x: int = 0          # grid units
    y: int = 0          # grid units
    orient: str = "R0"  # R0 | MX | R90


@dataclass
class Sheet:
    sub: Subckt
    placed: dict[str, Placed] = field(default_factory=dict)   # by device name
    rails: dict[str, str] = field(default_factory=dict)       # net -> vdd|gnd
    label_nets: set[str] = field(default_factory=set)
    columns: list[list[Device]] = field(default_factory=list)
    preroutes: list[tuple[int, int, int, int, str]] = field(default_factory=list)
    covered: set[tuple[str, str]] = field(default_factory=set)  # (dev, role)
    taps: list[tuple[str, int, int, str]] = field(default_factory=list)
    width: int = 0      # grid units
    height: int = 0     # grid units
    rows: int = 0

    def pos(self, dev: Device) -> Placed:
        return self.placed[dev.name]


def _channel(dev: Device) -> tuple[str, str] | None:
    return dev.channel_nets()


# ---------------------------------------------------------------- coverage

def _tile_covered(t: Tile) -> set[tuple[str, str]]:
    cov: set[tuple[str, str]] = set()
    if t.kind == "mirror":
        for m in t.members:
            cov.add((m.name, "g"))
    elif t.kind in ("pair", "5t"):
        m1, m2 = t.members
        cov.add((m1.name, "s"))
        cov.add((m2.name, "s"))
        if t.tail is not None:
            cov.add((t.tail.name, "d"))
        if t.kind == "5t":
            for ld in t.loads:
                cov.add((ld.name, "g"))
            cov.add((m1.name, "d"))
            cov.add((m2.name, "d"))
    elif t.kind == "diode1":
        cov.add((t.members[0].name, "g"))
    return cov


# ---------------------------------------------------------------- main

def place(sub: Subckt) -> Sheet:
    sheet = Sheet(sub=sub)
    sheet.rails = rails_of(sub)
    rails = sheet.rails
    devices = sub.devices

    tiles, claimed = recognize(sub, rails)
    for t in tiles:
        sheet.covered |= _tile_covered(t)
        for m in t.devices():       # one tile = one section cluster
            m.section = t.section

    # ---- channel index over ALL devices (levels are electrical facts)
    chan_at: dict[str, list[Device]] = {}
    for d in devices:
        ch = _channel(d)
        if not ch:
            continue
        for n in ch:
            if n is not None:
                chan_at.setdefault(n, []).append(d)

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

    level = _bfs("gnd")
    level_vdd = _bfs("vdd")

    # ---- label nets: count only endpoints that will actually be drawn
    for net in sub.nets():
        if net in rails:
            continue
        terms = sub.terminals(net)
        uncov = [1 for d, r in terms if (d.name, r) not in sheet.covered]
        eff = len(uncov) + (1 if len(uncov) < len(terms) and uncov else 0)
        if eff >= LABEL_FANOUT:
            sheet.label_nets.add(net)

    # ---- series columns over the unclaimed remainder
    used: set[str] = set(claimed)
    columns: list[list[Device]] = []

    def grow(seed: Device, start_net: str, downward: bool) -> list[Device]:
        target = level if downward else level_vdd
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
                return d if d < here else None

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

    for d in devices:
        if d.name in used:
            continue
        ch = _channel(d)
        if not ch:
            continue
        vdd_terms = [n for n in ch if n in rails and rails[n] == "vdd"]
        if vdd_terms:
            columns.append(grow(d, vdd_terms[0], downward=True))
    for d in devices:
        if d.name in used:
            continue
        ch = _channel(d)
        if not ch:
            continue
        gnd_terms = [n for n in ch if n in rails and rails[n] == "gnd"]
        if gnd_terms:
            columns.append(list(reversed(grow(d, gnd_terms[0], downward=False))))
    laterals: set[str] = set()
    for d in devices:
        if d.name not in used:
            ch = _channel(d)
            if ch and ch[0] not in rails and ch[1] not in rails \
               and d.kind in ("nmos", "pmos", "res", "cap"):
                laterals.add(d.name)
            columns.append([d])
            used.add(d.name)

    # ---- sheet rows
    maxlevel = max(level.values(), default=1)
    rows = max(maxlevel + 1, max((len(c) for c in columns), default=1), 2)
    sheet.rows = rows
    sheet.columns = columns

    def row_y(row: int) -> int:
        return MARGIN + ROW0_OFFSET + row * ROW_PITCH

    # ---- order all objects (tiles + chains) by (section, line)
    sec_order = {s: i for i, s in enumerate(sub.sections)}

    objects: list[tuple] = [("tile", t) for t in tiles] + \
                           [("chain", c) for c in columns]

    def obj_key(o) -> tuple:
        kind, val = o
        first = val.members[0] if kind == "tile" else val[0]
        return (sec_order.get(first.section, len(sec_order)), first.line)
    objects.sort(key=obj_key)

    def obj_width(o) -> int:
        kind, val = o
        if kind == "chain":
            return COL_PITCH
        if val.kind in ("pair", "5t"):
            return TILE_PITCH + 14
        if val.kind == "mirror":
            return (len(val.members) - 1) * TILE_PITCH + 14
        return COL_PITCH                       # diode1

    # ---- chain row assignment (tiles handled in their layout)
    def assign_rows(col: list[Device]) -> None:
        top_i = 0
        for i, d in enumerate(col):
            ch = _channel(d)
            if ch and any(n in rails and rails[n] == "vdd" for n in ch):
                row = top_i
                top_i += 1
            elif ch:
                lvls = [level[n] for n in ch if n in level]
                row = (rows - 1 - min(lvls)) if lvls else min(i, rows - 1)
                top_i = row + 1
            else:
                row = min(1 + i, rows - 1)
            sheet.placed[d.name] = Placed(dev=d, row=row)
        taken: dict[int, int] = {}
        for d in col:
            p = sheet.placed[d.name]
            while p.row in taken:
                p.row -= 1 if p.row > 0 else -1
            taken[p.row] = 1

    # ---- lay everything left to right
    x = MARGIN
    prev_sec = None
    for ci, o in enumerate(objects):
        kind, val = o
        first = val.members[0] if kind == "tile" else val[0]
        sec = first.section
        if prev_sec is not None and sec != prev_sec:
            x += SECTION_GAP
        prev_sec = sec
        w = obj_width(o)
        if kind == "chain":
            assign_rows(val)
            cx = x + w // 2
            for d in val:
                p = sheet.placed[d.name]
                p.col = ci
                p.x = cx
                p.y = row_y(p.row)
                if d.name in laterals:
                    p.orient = "R90"
        else:
            _lay_tile(sheet, val, x + 7, rows, level, row_y, ci)
        x += w

    sheet.width = x + MARGIN
    sheet.height = MARGIN + ROW0_OFFSET + (rows - 1) * ROW_PITCH + MARGIN + 4

    # ---- gate orientation for chain devices: face the driver
    for d in devices:
        if d.kind not in ("nmos", "pmos") or d.name in claimed \
           or d.name in laterals:
            continue
        g = d.net_of("g")
        if g is None or g in rails or g in sheet.label_nets:
            continue
        p = sheet.placed[d.name]
        xs = [sheet.placed[o2.name].x for o2, r in sub.terminals(g)
              if o2.name != d.name and o2.name in sheet.placed]
        if xs and sum(xs) / len(xs) > p.x:
            p.orient = "MX"
    return sheet


# ---------------------------------------------------------------- tiles

def _lay_tile(sheet: Sheet, t: Tile, x0: int, rows: int,
              level: dict[str, int], row_y, ci: int) -> None:
    """Place tile members and emit the pre-routed internal wires."""
    rails = sheet.rails
    pre = sheet.preroutes

    if t.kind == "mirror":
        m0 = t.members[0]
        src = m0.net_of("s")
        top = src in rails and rails[src] == "vdd"
        row = 0 if top else rows - 1
        y = row_y(row)
        rail_dy = 5 if top else -5          # gate rail toward sheet interior
        gnet = m0.net_of("g")
        xs = []
        for i, m in enumerate(t.members):
            mx = x0 + i * TILE_PITCH
            xs.append(mx)
            sheet.placed[m.name] = Placed(dev=m, col=ci, row=row, x=mx, y=y)
            pre.append((mx - 3, y, mx - 3, y + rail_dy, gnet))   # gate drop
        pre.append((xs[0] - 3, y + rail_dy, xs[-1] - 3, y + rail_dy, gnet))
        if t.diode is not None:
            dx = sheet.placed[t.diode.name].x
            dpin = 4 if top else -4          # drain pin side
            pre.append((dx, y + rail_dy, dx, y + dpin, gnet))
        else:
            # gate driven externally: expose one tap on the rail
            sheet.taps.append((gnet, xs[0] - 3, y + rail_dy, "L"))

    elif t.kind in ("pair", "5t"):
        m1, m2 = t.members
        snet = m1.net_of("s")
        prow = rows - 1 - level.get(snet, 1)
        prow = max(prow, 1 if t.kind == "5t" else 0)
        py = row_y(prow)
        x1, x2 = x0, x0 + TILE_PITCH
        mid = x0 + TILE_PITCH // 2
        sheet.placed[m1.name] = Placed(dev=m1, col=ci, row=prow, x=x1, y=py)
        sheet.placed[m2.name] = Placed(dev=m2, col=ci, row=prow, x=x2, y=py,
                                       orient="MX")
        # shared source bus
        pre.append((x1, py + 4, x1, py + 6, snet))
        pre.append((x2, py + 4, x2, py + 6, snet))
        pre.append((x1, py + 6, x2, py + 6, snet))
        if t.tail is not None:
            trow = prow + 1
            ty = row_y(trow)
            sheet.placed[t.tail.name] = Placed(dev=t.tail, col=ci, row=trow,
                                               x=mid, y=ty)
            pre.append((mid, py + 6, mid, ty - 4, snet))
        if t.kind == "5t":
            lrow = prow - 1
            ly = row_y(lrow)
            gnet = t.loads[0].net_of("g")
            for ld, lx in zip(t.loads, (x1, x2)):
                sheet.placed[ld.name] = Placed(dev=ld, col=ci, row=lrow,
                                               x=lx, y=ly)
                pre.append((lx, ly + 4, lx, py - 4,
                            ld.net_of("d")))         # drain link to pair
                pre.append((lx - 3, ly, lx - 3, ly + 5, gnet))
            pre.append((x1 - 3, ly + 5, x2 - 3, ly + 5, gnet))
            if t.diode is not None:
                dx = sheet.placed[t.diode.name].x
                pre.append((dx, ly + 5, dx, ly + 4, gnet))

    elif t.kind == "diode1":
        m = t.members[0]
        ch = _channel(m)
        lvls = [level[n] for n in ch if n in level]
        row = (rows - 1 - min(lvls)) if lvls else rows - 1
        y = row_y(row)
        sheet.placed[m.name] = Placed(dev=m, col=ci, row=row,
                                      x=x0 + COL_PITCH // 2 - 7, y=y)
        mx = sheet.placed[m.name].x
        dnet = m.net_of("g")
        dpin = -4 if m.kind == "nmos" else 4   # drain side (nmos drain up)
        pre.append((mx - 3, y, mx - 3, y + dpin - (1 if dpin < 0 else -1), dnet))
        pre.append((mx - 3, y + dpin - (1 if dpin < 0 else -1), mx,
                    y + dpin - (1 if dpin < 0 else -1), dnet))
        pre.append((mx, y + dpin - (1 if dpin < 0 else -1), mx, y + dpin, dnet))
