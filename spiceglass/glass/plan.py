"""GlassPlan — the placement-intent language (P1).

A .plan file states STRUCTURE (groups) and NARRATIVE (flow of regions,
each holding tiles and [columns]) — never coordinates. Realization is
deterministic: the same .plan always renders the same schematic, through
exactly the same geometry code as the automatic placer.

    glass plan design.cir            -> writes design.<sub>.plan
    glass render --plan x.plan       -> realize + route + verify

Syntax (netlist-flavored, '#' comments):

    plan bias_generator from design.cir grid 1mm

    mirror PMIR = XM3 XM4 XM7
    core5t OTA  = pair(XMo1 XMo2) tail(XMo5) loads(XMo3 XMo4) diode(XMo3)
    pair   P1   = pair(M1 M2) tail(M5)
    diode-link  = XM1
    lateral     = XMsw

    flow
      region "Bias core"  PMIR [XM1]
      region "Startup"    [XC_gs XR_gs] [XMsw]

    orient XMsw R90
    shift  XC_comp +1 0
    wire   out_n via 38,35        # parsed; applied in a later milestone
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .db import Design, Subckt
from .place import (Sheet, _emit_tile_wiring, _realize, _tile_covered,
                    label_nets_of, levels_of, place)
from .classify import rails_of
from .recognize import Tile


@dataclass
class Plan:
    name: str = ""
    source: str = ""
    grid: str = "1mm"
    version: int = 0
    groups: list[dict] = field(default_factory=list)
    diode_links: list[str] = field(default_factory=list)
    laterals: list[str] = field(default_factory=list)
    flow: list[tuple[str, list]] = field(default_factory=list)
    orient: dict[str, str] = field(default_factory=dict)
    shifts: dict[str, tuple[int, int]] = field(default_factory=dict)
    places: dict[str, tuple[int, int]] = field(default_factory=dict)
    wire_paths: dict[str, list] = field(default_factory=dict)
    wires: list[tuple[str, list[tuple[int, int]]]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ================================================================ emit

def emit_plan(sub: Subckt, sheet: Sheet) -> str:
    """Write the automatic interpretation of a PLACED sheet as a .plan."""
    lines = ["glassplan 1",
             f"plan {sub.name}  from {_src_name(sheet)}  grid 1mm", ""]

    # ---- groups (named in x order)
    tiles = sorted(sheet.tiles,
                   key=lambda t: min(sheet.placed[m.name].x
                                     for m in t.devices()))
    names: dict[int, str] = {}
    counters = {"mirror": 0, "pair": 0, "5t": 0}
    dlinks, lats = [], []
    if tiles:
        lines.append("# structure: what the circuit IS "
                     "(correct these lines freely)")
    for t in tiles:
        if t.kind == "diode1":
            dlinks.append(t.members[0].name)
            continue
        counters[t.kind] = counters.get(t.kind, 0) + 1
        nm = {"mirror": "MIR", "pair": "PAIR", "5t": "OTA"}[t.kind] + \
            str(counters[t.kind])
        names[id(t)] = nm
        if t.kind == "mirror":
            lines.append(f"mirror {nm} = " +
                         " ".join(m.name for m in t.members))
        else:
            kw = "core5t" if t.kind == "5t" else "pair"
            s = f"{kw} {nm} = pair({t.members[0].name} {t.members[1].name})"
            if t.tail is not None:
                s += f" tail({t.tail.name})"
            if t.loads:
                s += f" loads({' '.join(m.name for m in t.loads)})"
            if t.diode is not None:
                s += f" diode({t.diode.name})"
            lines.append(s)
    for d in sheet.sub.devices:
        if sheet.placed[d.name].orient == "R90":
            lats.append(d.name)
    if dlinks:
        lines.append("diode-link = " + " ".join(dlinks))
    if lats:
        lines.append("lateral = " + " ".join(lats))

    # ---- flow: objects in x order, grouped into regions by section
    objs: list[tuple[int, str, str]] = []      # (x, item-text, section)
    for t in tiles:
        x = min(sheet.placed[m.name].x for m in t.devices())
        item = names.get(id(t), f"[{t.members[0].name}]")
        objs.append((x, item, t.section))
    placed_in_tiles = {m.name for t in tiles for m in t.devices()}
    for col in sheet.columns:
        col = [d for d in col if d.name not in placed_in_tiles]
        if not col:
            continue
        ordered = sorted(col, key=lambda d: sheet.placed[d.name].row)
        x = min(sheet.placed[d.name].x for d in col)
        objs.append((x, "[" + " ".join(d.name for d in ordered) + "]",
                     col[0].section))
    objs.sort(key=lambda o: o[0])

    lines += ["", "# narrative: regions left->right; [..] = a column,",
              "#            devices top->bottom (VDD..GND)", "flow"]
    cur: object = object()
    for _, item, sec in objs:
        if sec != cur:
            cur = sec
            lines.append(f'  region "{sec}" {item}')
        else:
            lines[-1] += " " + item
    return "\n".join(lines) + "\n"


def _src_name(sheet: Sheet) -> str:
    import os
    return os.path.basename(getattr(sheet, "_src", "") or "design.cir")


# ================================================================ parse

_TOKEN = re.compile(r'\[[^\]]*\]|"[^"]*"|\S+')


def _strip_comment(line: str) -> str:
    out = []
    in_q = False
    for ch in line:
        if ch == '"':
            in_q = not in_q
        if ch == "#" and not in_q:
            break
        out.append(ch)
    return "".join(out)


def parse_plan(text: str) -> Plan:
    """GlassPlan v1 parser (see design/glassplan-spec.md): version token,
    inline # comments, backslash continuation, line-numbered diagnostics,
    the 8-orientation group, place and wire-path escape hatches."""
    from .geom import ORIENTS
    plan = Plan()
    text = text.lstrip("﻿")        # Windows editors love BOMs

    logical: list[tuple[int, str]] = []
    pending: tuple[int, str] | None = None
    for no, raw in enumerate(text.splitlines(), 1):
        line = _strip_comment(raw).rstrip()
        if pending is not None:
            line = pending[1] + " " + line.strip()
            no = pending[0]
            pending = None
        if line.endswith("\\"):
            pending = (no, line[:-1].rstrip())
            continue
        if line.strip():
            logical.append((no, line))
    if pending is not None:
        logical.append(pending)

    in_flow = False
    for no, line in logical:
        toks = _TOKEN.findall(line)
        head = toks[0].lower()

        if head == "glassplan":
            try:
                plan.version = int(toks[1])
            except (IndexError, ValueError):
                plan.warnings.append(f"line {no}: bad version token")
            continue
        if head == "plan":
            plan.name = toks[1] if len(toks) > 1 else ""
            if "from" in [t.lower() for t in toks]:
                plan.source = toks[[t.lower() for t in toks].index("from") + 1]
            if "grid" in [t.lower() for t in toks]:
                plan.grid = toks[[t.lower() for t in toks].index("grid") + 1]
            continue
        if head == "flow":
            in_flow = True
            continue
        if head == "region":
            title = toks[1].strip('"') if len(toks) > 1 else ""
            items = []
            for t in toks[2:]:
                if t.startswith("["):
                    items.append(("column", t[1:-1].split()))
                else:
                    items.append(("group", t))
            plan.flow.append((title, items))
            continue
        if head in ("mirror",):
            name = toks[1]
            members = [t for t in toks[3:]] if toks[2] == "=" else toks[2:]
            plan.groups.append({"kind": "mirror", "name": name,
                                "members": members})
            continue
        if head in ("core5t", "pair"):
            body = line.split("=", 1)[1] if "=" in line else ""
            name = toks[1]
            g = {"kind": "5t" if head == "core5t" else "pair", "name": name,
                 "pair": _paren(body, "pair"), "tail": _paren(body, "tail"),
                 "loads": _paren(body, "loads"),
                 "diode": _paren(body, "diode")}
            plan.groups.append(g)
            continue
        if head == "diode-link":
            plan.diode_links += [t for t in toks[1:] if t != "="]
            continue
        if head == "lateral":
            plan.laterals += [t for t in toks[1:] if t != "="]
            continue
        if head == "orient" and len(toks) >= 3:
            o = toks[2].upper()
            if o not in ORIENTS:
                plan.warnings.append(
                    f"line {no}: unknown orientation '{toks[2]}' "
                    f"(valid: {' '.join(ORIENTS)})")
            else:
                plan.orient[toks[1]] = o
            continue
        if head == "shift" and len(toks) >= 4:
            try:
                plan.shifts[toks[1]] = (int(toks[2]), int(toks[3]))
            except ValueError:
                plan.warnings.append(f"line {no}: shift needs integers")
            continue
        if head == "place" and len(toks) >= 4:
            try:
                plan.places[toks[1]] = (int(toks[2]), int(toks[3]))
            except ValueError:
                plan.warnings.append(f"line {no}: place needs integers")
            continue
        if head == "wire" and len(toks) >= 3:
            mode = toks[2].lower()
            pts = []
            for t in toks[3:]:
                if "," not in t:
                    continue
                try:
                    x, y = t.split(",")
                    pts.append([int(x), int(y)])
                except ValueError:
                    plan.warnings.append(f"line {no}: bad point '{t}'")
            if mode == "path" and len(pts) >= 2:
                plan.wire_paths.setdefault(toks[1], []).append(pts)
            else:
                plan.wires.append((toks[1], [tuple(p) for p in pts]))
                plan.warnings.append(
                    f"line {no}: wire via-hints are not applied; use "
                    f"'wire {toks[1]} path x,y x,y ...'")
            continue
        if in_flow:
            plan.warnings.append(f"line {no}: unrecognized flow line: "
                                 f"{line.strip()}")
        else:
            plan.warnings.append(f"line {no}: unrecognized line: "
                                 f"{line.strip()}")
    if plan.version == 0:
        plan.warnings.append("no 'glassplan 1' version token — parsed as v0")
    return plan


def _paren(body: str, key: str) -> list[str]:
    m = re.search(rf"{key}\(([^)]*)\)", body)
    return m.group(1).split() if m else []


# ================================================================ realize

def realize_plan(sub: Subckt, plan: Plan) -> Sheet:
    """Deterministic geometry from a plan — same code path as place()."""
    sheet = Sheet(sub=sub)
    sheet.rails = rails_of(sub)
    rails = sheet.rails
    byname = {d.name: d for d in sub.devices}

    def dev(n: str):
        if n not in byname:
            raise ValueError(f"plan references unknown device '{n}'")
        return byname[n]

    # ---- groups -> tiles
    tiles_by_name: dict[str, Tile] = {}
    for g in plan.groups:
        if g["kind"] == "mirror":
            members = [dev(n) for n in g["members"]]
            diode = next((m for m in members
                          if m.net_of("d") == m.net_of("g")), None)
            t = Tile(kind="mirror", members=members, diode=diode,
                     section="", line=members[0].line)
        else:
            members = [dev(n) for n in g["pair"]]
            t = Tile(kind=g["kind"], members=members,
                     tail=dev(g["tail"][0]) if g["tail"] else None,
                     loads=[dev(n) for n in g["loads"]],
                     diode=dev(g["diode"][0]) if g["diode"] else None,
                     section="", line=members[0].line)
        tiles_by_name[g["name"]] = t
    for n in plan.diode_links:
        t = Tile(kind="diode1", members=[dev(n)], section="", line=dev(n).line)
        tiles_by_name[f"~dl_{n}"] = t

    # ---- flow -> ordered objects; regions become sections
    objects: list[tuple] = []
    used: set[str] = set()
    dlink_auto = {f"~dl_{n}" for n in plan.diode_links}
    for title, items in plan.flow:
        for kind, val in items:
            if kind == "group":
                t = tiles_by_name.get(val)
                if t is None:
                    raise ValueError(f"plan flow references unknown group "
                                     f"'{val}'")
                t.section = title
                for m in t.devices():
                    m.section = title
                    used.add(m.name)
                objects.append(("tile", t))
            else:
                if len(val) == 1 and f"~dl_{val[0]}" in tiles_by_name:
                    t = tiles_by_name[f"~dl_{val[0]}"]
                    t.section = title
                    t.members[0].section = title
                    used.add(val[0])
                    objects.append(("tile", t))
                    continue
                col = [dev(n) for n in val]
                for d in col:
                    d.section = title
                    used.add(d.name)
                objects.append(("chain", col))
    # diode links not explicitly placed ride along as their own column obj
    for nm in dlink_auto:
        t = tiles_by_name[nm]
        m = t.members[0]
        if m.name not in used:
            t.section = m.section
            objects.append(("tile", t))
            used.add(m.name)

    # ---- validation: every device exactly once
    missing = [d.name for d in sub.devices if d.name not in used]
    if missing:
        raise ValueError("plan does not place: " + ", ".join(missing))
    counts: dict[str, int] = {}
    for kind, val in objects:
        for d in (val.devices() if kind == "tile" else val):
            counts[d.name] = counts.get(d.name, 0) + 1
    dupes = [n for n, c in counts.items() if c > 1]
    if dupes:
        raise ValueError("plan places twice: " + ", ".join(dupes))

    # plan regions become the sheet's sections (shading + gaps)
    seen: dict[str, None] = {}
    for title, _ in plan.flow:
        if title:
            seen.setdefault(title)
    sub.sections = list(seen)

    # tiles that are referenced in flow AND declared as diode-link groups
    sheet.tiles = [val for kind, val in objects if kind == "tile"]
    for t in sheet.tiles:
        sheet.covered |= _tile_covered(t)

    chan_at, level, level_vdd = levels_of(sub, rails)
    label_nets_of(sheet)

    laterals = set(plan.laterals)
    _realize(sheet, objects, laterals,
             level, {m.name for t in sheet.tiles for m in t.devices()})

    for name, o in plan.orient.items():
        if name in sheet.placed:
            sheet.placed[name].orient = o
    for name, (dx, dy) in plan.shifts.items():
        if name in sheet.placed:
            sheet.placed[name].x += dx
            sheet.placed[name].y += dy
    for name, (x, y) in plan.places.items():
        if name in sheet.placed:
            sheet.placed[name].x = x
            sheet.placed[name].y = y
    if plan.places:
        maxx = max(p.x for p in sheet.placed.values())
        maxy = max(p.y for p in sheet.placed.values())
        sheet.width = max(sheet.width, maxx + 14)
        sheet.height = max(sheet.height, maxy + 14)

    # full wire paths from the plan ride the same pinned-wires machinery
    # as editor edits (validated against pins, immovable for other nets)
    sheet.plan_wires = {net: [list(map(list, p)) for p in paths]
                        for net, paths in plan.wire_paths.items()}

    _emit_tile_wiring(sheet)
    return sheet


# ================================================================ helpers

def plan_for(design: Design, subname: str) -> str:
    """Run automatic interpretation and emit its plan."""
    sub = design.subckts[subname]
    sheet = place(sub)
    sheet._src = design.path
    return emit_plan(sub, sheet)


# ================================================================ diff

def plan_facts(plan: Plan) -> dict[str, dict]:
    """Per-device facts a plan asserts: group, region, column partners."""
    facts: dict[str, dict] = {}

    def f(name: str) -> dict:
        return facts.setdefault(name, {"group": "", "region": "",
                                       "col": frozenset(), "orient": "R0"})

    group_members: dict[str, list[str]] = {}
    for g in plan.groups:
        if g["kind"] == "mirror":
            mem = list(g["members"])
        else:
            mem = list(g["pair"]) + list(g["tail"]) + list(g["loads"])
        group_members[g["name"]] = mem
        for n in mem:
            f(n)["group"] = f'{g["kind"]}:{" ".join(sorted(mem))}'
    for n in plan.diode_links:
        f(n)["group"] = "diode-link"
    for title, items in plan.flow:
        mates: list[str] = []
        for kind, val in items:
            mates += group_members.get(val, [val]) if kind == "group" \
                else list(val)
        for kind, val in items:
            if kind == "group":
                for n in group_members.get(val, [val]):
                    f(n)["region"] = frozenset(mates)
                    f(n)["rtitle"] = title
            else:
                for n in val:
                    f(n)["region"] = frozenset(mates)
                    f(n)["rtitle"] = title
                    f(n)["col"] = frozenset(val)
    for n, o in plan.orient.items():
        f(n)["orient"] = o
    for n in plan.laterals:
        f(n)["orient"] = "R90"
    return facts


def diff_plans(auto: Plan, golden: Plan) -> tuple[str, int]:
    """Categorized differences: what the human changed = what the
    interpreter should learn. Returns (report, devices_differing)."""
    fa, fg = plan_facts(auto), plan_facts(golden)
    lines: list[str] = []
    differing: set[str] = set()
    for n in sorted(set(fa) | set(fg)):
        a, g = fa.get(n, {}), fg.get(n, {})
        if a.get("group", "") != g.get("group", ""):
            lines.append(f"GROUPING  {n}: auto[{a.get('group') or '-'}] -> "
                         f"golden[{g.get('group') or '-'}]")
            differing.add(n)
        if a.get("region", frozenset()) != g.get("region", frozenset()):
            lines.append(f"REGION    {n}: auto[{a.get('rtitle') or '-'}] -> "
                         f"golden[{g.get('rtitle') or '-'}] "
                         "(membership changed)")
            differing.add(n)
        if a.get("col", frozenset()) != g.get("col", frozenset()):
            lines.append(f"COLUMN    {n}: auto[{' '.join(sorted(a.get('col', ()))) or '-'}]"
                         f" -> golden[{' '.join(sorted(g.get('col', ()))) or '-'}]")
            differing.add(n)
        if a.get("orient", "R0") != g.get("orient", "R0"):
            lines.append(f"ORIENT    {n}: {a.get('orient')} -> {g.get('orient')}")
            differing.add(n)
    ra = [t for t, _ in auto.flow]
    rg = [t for t, _ in golden.flow]
    if ra != rg:
        lines.append(f"FLOW ORDER auto[{' | '.join(ra)}]")
        lines.append(f"           golden[{' | '.join(rg)}]")
    if not lines:
        lines.append("no differences — interpreter matches the golden")
    return "\n".join(lines), len(differing)
