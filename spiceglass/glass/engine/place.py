"""Placement: interpretation (heuristics) + realization (deterministic).

place()      — the automatic path: recognize tiles, grow series columns,
               order by the netlist narrative, then realize.
realization  — _realize() turns an ORDERED list of objects (tiles and
               columns) into grid coordinates. It contains no guessing;
               glass.plan drives it from a hand-editable .plan file
               through exactly the same code path (GlassPlan P1).

Drawing conventions encoded:
1. Rails fold away (VDD top, GND bottom — stubs, not wires).
2. Recognized structures (mirror banks, diff pairs, 5T cores, diode
   links) are placed as TILES whose defining wires are pre-routed.
3. Remaining devices form series columns: every step must make
   monotonic progress toward the opposite rail.
4. Lateral leftovers (both channel nets internal) lie flat (R90).
5. Objects are ordered by the netlist's own narrative order, grouped
   by the LLM's section comments (or by .plan regions).
6. Rows anchor to rail distance so related devices align across
   columns automatically.

All coordinates are integer grid units (see glass.geom).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .classify import rails_of
from .db import Device, Subckt
from ..geom import (COL_PITCH, MARGIN, ROW0_OFFSET, ROW_PITCH, SECTION_GAP,
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
    tiles: list = field(default_factory=list)
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


# ---------------------------------------------------------------- analysis

def levels_of(sub: Subckt, rails: dict[str, str]):
    """Channel index + rail-distance maps (shared electrical facts)."""
    chan_at: dict[str, list[Device]] = {}
    for d in sub.devices:
        ch = _channel(d)
        if not ch:
            continue
        for n in ch:
            if n is not None:
                chan_at.setdefault(n, []).append(d)

    def _bfs(rail_kind: str) -> dict[str, int]:
        dist: dict[str, int] = {n: 0 for n, k in rails.items()
                                if k == rail_kind}
        frontier = list(dist)
        while frontier:
            nxt = []
            for n in frontier:
                for d in chan_at.get(n, []):
                    # capacitors are AC loads, not DC level-setting paths —
                    # a cap to a rail must not collapse a node's stack level
                    if d.kind == "cap":
                        continue
                    ch = _channel(d)
                    other = ch[0] if ch[1] == n else ch[1]
                    if other is None or other in rails:
                        continue
                    if other not in dist or dist[other] > dist[n] + 1:
                        dist[other] = dist[n] + 1
                        nxt.append(other)
            frontier = nxt
        return dist

    return chan_at, _bfs("gnd"), _bfs("vdd")


def label_nets_of(sheet: Sheet) -> None:
    """High-fanout nets become stubs — counting only drawn endpoints."""
    sub = sheet.sub
    for net in sub.nets():
        if net in sheet.rails:
            continue
        terms = sub.terminals(net)
        uncov = [1 for d, r in terms if (d.name, r) not in sheet.covered]
        eff = len(uncov) + (1 if len(uncov) < len(terms) and uncov else 0)
        if eff >= LABEL_FANOUT:
            sheet.label_nets.add(net)


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


# ---------------------------------------------------------------- automatic

def place(sub: Subckt, overrides: dict[str, dict] | None = None,
          optimize: bool = False, trace: list | None = None,
          opt_rank: int = 0) -> Sheet:
    """Automatic interpretation + realization; `overrides` (dev ->
    {x,y,orient}) applies human edits AFTER it — tile wiring re-derives
    from the final positions. When `optimize` is set, the left-to-right
    object order is searched to minimise crossings (see engine.optimize);
    pass a `trace` list to capture the optimisation's decisions."""
    sheet = Sheet(sub=sub)
    sheet.rails = rails_of(sub)
    rails = sheet.rails
    devices = sub.devices

    tiles, claimed = recognize(sub, rails)
    sheet.tiles = tiles
    for t in tiles:
        sheet.covered |= _tile_covered(t)
        for m in t.devices():       # one tile = one section cluster
            m.section = t.section

    chan_at, level, level_vdd = levels_of(sub, rails)
    label_nets_of(sheet)

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
            columns.append(list(reversed(grow(d, gnd_terms[0],
                                              downward=False))))
    laterals: set[str] = set()
    for d in devices:
        if d.name not in used:
            ch = _channel(d)
            if ch and ch[0] not in rails and ch[1] not in rails \
               and d.kind in ("nmos", "pmos", "res", "cap"):
                laterals.add(d.name)
            columns.append([d])
            used.add(d.name)

    sheet.columns = columns

    sec_order = {s: i for i, s in enumerate(sub.sections)}
    # empty-section objects slot at their natural netlist position
    # instead of dumping to the end (R4 fallback)
    sec_first = {}
    for d in devices:
        if d.section:
            sec_first.setdefault(d.section, d.line)

    def sec_idx(section: str, line: int) -> float:
        if section in sec_order:
            return float(sec_order[section])
        before = sum(1 for s, fl in sec_first.items() if fl <= line)
        return before - 0.5

    def base_key(first) -> tuple:
        return (sec_idx(first.section, first.line), float(first.line))

    # ---- golden-plan rule (rms_squarer): a lateral device slots right
    #      after the COLUMN of its same-section channel partner
    col_of: dict[str, list] = {}
    for col in columns:
        for d in col:
            col_of[d.name] = col
    key_override: dict[int, tuple] = {}
    for col in columns:
        d = col[0]
        if len(col) != 1 or d.name not in laterals:
            continue
        ch = _channel(d) or ()
        partner = next((o for o in devices
                        if o.name != d.name and o.section == d.section
                        and o.channel_nets()
                        and any(n in o.channel_nets() for n in ch)), None)
        if partner is not None and partner.name in col_of \
           and col_of[partner.name] is not col:
            pcol = col_of[partner.name]
            k = base_key(pcol[0])
            key_override[id(col)] = (k[0], k[1] + 0.5)

    objects: list[tuple] = [("tile", t) for t in tiles] + \
                           [("chain", c) for c in columns]

    def obj_key(o) -> tuple:
        kind, val = o
        if kind == "chain" and id(val) in key_override:
            return key_override[id(val)]
        first = val.members[0] if kind == "tile" else val[0]
        return base_key(first)
    objects.sort(key=obj_key)

    # ---- golden-plan rule (bias_generator): a section that is just one
    #      lone capacitor merges into the preceding region (comp caps
    #      belong with the block they compensate)
    for i, (kind, val) in enumerate(objects):
        if kind != "chain" or len(val) != 1 or val[0].kind != "cap" or i == 0:
            continue
        sec = val[0].section
        alone = all((v.members[0] if k == "tile" else v[0]).section != sec
                    for j, (k, v) in enumerate(objects) if j != i)
        if alone:
            pk, pv = objects[i - 1]
            val[0].section = (pv.members[0] if pk == "tile"
                              else pv[0]).section

    if optimize:
        from .structure import device_structure_map
        dev_struct = device_structure_map(sub, rails)   # recognition hint
        if trace is not None:
            from .optimize import optimize_order
            objects = optimize_order(objects, sheet.rails, sheet.label_nets,
                                     trace, dev_struct=dev_struct)
        else:
            from .optimize import optimize_candidates
            cands = optimize_candidates(objects, sheet.rails,
                                        sheet.label_nets,
                                        dev_struct=dev_struct)
            objects = cands[min(opt_rank, len(cands) - 1)]

    _realize(sheet, objects, laterals, level, claimed)

    # ---- human overrides (editor) — applied last, wiring follows
    if overrides:
        for name, o in overrides.items():
            p = sheet.placed.get(name)
            if p is None:
                continue
            p.x = int(o.get("x", p.x))
            p.y = int(o.get("y", p.y))
            p.orient = o.get("orient", p.orient)
        maxx = max((p.x for p in sheet.placed.values()), default=10)
        maxy = max((p.y for p in sheet.placed.values()), default=10)
        sheet.width = max(sheet.width, maxx + MARGIN + 6)
        sheet.height = max(sheet.height, maxy + MARGIN + 6)

    _emit_tile_wiring(sheet)
    return sheet


# ---------------------------------------------------------------- realize

def row_y(row: int) -> int:
    return MARGIN + ROW0_OFFSET + row * ROW_PITCH


def _realize(sheet: Sheet, objects: list[tuple], laterals: set[str],
             level: dict[str, int], claimed: set[str]) -> None:
    """Deterministic geometry from an ORDERED object list. No guessing:
    everything order/grouping-related was decided by the caller."""
    sub = sheet.sub
    rails = sheet.rails
    chains = [val for kind, val in objects if kind == "chain"]
    maxlevel = max(level.values(), default=1)
    rows = max(maxlevel + 1, max((len(c) for c in chains), default=1), 2)
    sheet.rows = rows

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

    def obj_width(o) -> int:
        kind, val = o
        if kind == "chain":
            return COL_PITCH
        if val.kind in ("pair", "5t"):
            return TILE_PITCH + 14
        if val.kind == "mirror":
            return (len(val.members) - 1) * TILE_PITCH + 14
        return COL_PITCH                       # diode1

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

    sheet.width = x + MARGIN + 8          # +8: room for right-edge labels
    sheet.height = MARGIN + ROW0_OFFSET + (rows - 1) * ROW_PITCH + MARGIN + 4

    # ---- gate orientation for chain devices: face the driver
    for d in sub.devices:
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


# ---------------------------------------------------------------- tiles

def _lay_tile(sheet: Sheet, t: Tile, x0: int, rows: int,
              level: dict[str, int], row_y, ci: int) -> None:
    """Assign tile member POSITIONS (wiring is emitted later from the
    final positions so human edits keep tile relationships intact)."""
    rails = sheet.rails

    if t.kind == "mirror":
        src = t.members[0].net_of("s")
        top = src in rails and rails[src] == "vdd"
        row = 0 if top else rows - 1
        y = row_y(row)
        for i, m in enumerate(t.members):
            sheet.placed[m.name] = Placed(dev=m, col=ci, row=row,
                                          x=x0 + i * TILE_PITCH, y=y)

    elif t.kind in ("pair", "5t"):
        m1, m2 = t.members
        snet = m1.net_of("s")
        # a PMOS pair has its source UP and drain DOWN (opposite an NMOS
        # pair), so its tail sits ABOVE and its loads BELOW — otherwise the
        # source rail and the drain->load wires cross (the SHORT we hit).
        pmos_pair = m1.kind == "pmos"
        prow = rows - 1 - level.get(snet, 1)
        prow = max(prow, 1 if (t.kind == "5t" or pmos_pair) else 0)
        py = row_y(prow)
        x1, x2 = x0, x0 + TILE_PITCH
        sheet.placed[m1.name] = Placed(dev=m1, col=ci, row=prow, x=x1, y=py)
        sheet.placed[m2.name] = Placed(dev=m2, col=ci, row=prow, x=x2, y=py,
                                       orient="MX")
        trow = prow - 1 if pmos_pair else prow + 1   # tail on the source side
        lrow = prow + 1 if pmos_pair else prow - 1   # loads on the drain side
        if t.tail is not None:
            sheet.placed[t.tail.name] = Placed(
                dev=t.tail, col=ci, row=trow,
                x=x0 + TILE_PITCH // 2, y=row_y(trow))
        if t.kind == "5t":
            ly = row_y(lrow)
            for ld, lx in zip(t.loads, (x1, x2)):
                sheet.placed[ld.name] = Placed(dev=ld, col=ci, row=lrow,
                                               x=lx, y=ly)

    elif t.kind == "diode1":
        m = t.members[0]
        ch = _channel(m)
        lvls = [level[n] for n in ch if n in level]
        row = (rows - 1 - min(lvls)) if lvls else rows - 1
        sheet.placed[m.name] = Placed(dev=m, col=ci, row=row,
                                      x=x0 + COL_PITCH // 2 - 7, y=row_y(row))


def _emit_tile_wiring(sheet: Sheet) -> None:
    """Pre-route tile internals from CURRENT member positions (orient-
    and drag-aware). Every segment starts/ends exactly on a pin, so the
    round-trip verifier checks tile internals like any other wire."""
    from ..geom import pin_pos
    pre = sheet.preroutes
    pre.clear()
    sheet.taps.clear()

    def pin(dev: Device, role: str) -> tuple[int, int]:
        p = sheet.placed[dev.name]
        return pin_pos(dev, role, p.x, p.y, p.orient)

    def rail_block(members: list[Device], diode: Device | None,
                   gnet: str, below: bool) -> tuple[int, int]:
        """Common gate rail + drops (+ diode link). Returns a tap point."""
        gpins = [pin(m, "g") for m in members]
        raily = (max(gy for _, gy in gpins) + 5) if below else \
                (min(gy for _, gy in gpins) - 5)
        for gx, gy in gpins:
            if gy != raily:
                pre.append((gx, gy, gx, raily, gnet))
        lo = min(gx for gx, _ in gpins)
        hi = max(gx for gx, _ in gpins)
        if lo != hi:
            pre.append((lo, raily, hi, raily, gnet))
        if diode is not None:
            dx, dy = pin(diode, "d")
            pre.append((dx, raily, dx, dy, gnet))
            if dx < lo:
                pre.append((dx, raily, lo, raily, gnet))
            elif dx > hi:
                pre.append((hi, raily, dx, raily, gnet))
        return (lo, raily)

    for t in sheet.tiles:
        if t.kind == "mirror":
            gnet = t.members[0].net_of("g")
            below = t.members[0].kind == "pmos"   # rail toward interior
            tap = rail_block(t.members, t.diode, gnet, below)
            if t.diode is None:
                sheet.taps.append((gnet, tap[0], tap[1], "L"))

        elif t.kind in ("pair", "5t"):
            m1, m2 = t.members
            snet = m1.net_of("s")
            s1, s2 = pin(m1, "s"), pin(m2, "s")
            nmos_pair = m1.kind == "nmos"
            busy = (max(s1[1], s2[1]) + 2) if nmos_pair else \
                   (min(s1[1], s2[1]) - 2)
            xs = [s1[0], s2[0]]
            for sx, sy in (s1, s2):
                if sy != busy:
                    pre.append((sx, sy, sx, busy, snet))
            if t.tail is not None:
                tdx, tdy = pin(t.tail, "d")
                xs.append(tdx)
                if tdy != busy:
                    pre.append((tdx, busy, tdx, tdy, snet))
            if min(xs) != max(xs):
                pre.append((min(xs), busy, max(xs), busy, snet))
            # a tail-less pair whose shared source is a SIGNAL node (e.g. a
            # mixer's switching quad) must route that source out to the rest
            # of the net — expose the rail as a tap, like a mirror gate rail.
            if t.tail is None and snet not in sheet.rails:
                sheet.taps.append((snet, min(xs), busy, "L"))
            if t.kind == "5t":
                for ld, pm in zip(t.loads, t.members):
                    dnet = ld.net_of("d")
                    lx, lyy = pin(ld, "d")
                    px, pyy = pin(pm, "d")
                    if lx == px:
                        pre.append((lx, lyy, lx, pyy, dnet))
                    else:
                        midy = (lyy + pyy) // 2
                        pre.append((lx, lyy, lx, midy, dnet))
                        pre.append((lx, midy, px, midy, dnet))
                        pre.append((px, midy, px, pyy, dnet))
                gnet = t.loads[0].net_of("g")
                below = t.loads[0].kind == "pmos"
                tap = rail_block(t.loads, t.diode, gnet, below)
                exposed = any((d.name, "d") not in sheet.covered
                              for d in t.loads if d.net_of("d") == gnet) or \
                          t.diode is not None
                if not exposed:
                    sheet.taps.append((gnet, tap[0], tap[1], "L"))

        elif t.kind == "diode1":
            m = t.members[0]
            dnet = m.net_of("g")
            gx, gy = pin(m, "g")
            dx, dy = pin(m, "d")
            elbow = dy + (1 if dy > gy else -1)
            pre.append((gx, gy, gx, elbow, dnet))
            pre.append((gx, elbow, dx, elbow, dnet))
            pre.append((dx, elbow, dx, dy, dnet))
