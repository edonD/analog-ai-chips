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
    groups: list[dict] = field(default_factory=list)
    diode_links: list[str] = field(default_factory=list)
    laterals: list[str] = field(default_factory=list)
    flow: list[tuple[str, list]] = field(default_factory=list)
    orient: dict[str, str] = field(default_factory=dict)
    shifts: dict[str, tuple[int, int]] = field(default_factory=dict)
    wires: list[tuple[str, list[tuple[int, int]]]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ================================================================ emit

def emit_plan(sub: Subckt, sheet: Sheet) -> str:
    """Write the automatic interpretation of a PLACED sheet as a .plan."""
    lines = [f"plan {sub.name}  from {_src_name(sheet)}  grid 1mm", ""]

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


def parse_plan(text: str) -> Plan:
    plan = Plan()
    in_flow = False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        toks = _TOKEN.findall(line)
        head = toks[0].lower()

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
            plan.orient[toks[1]] = toks[2].upper()
            continue
        if head == "shift" and len(toks) >= 4:
            plan.shifts[toks[1]] = (int(toks[2]), int(toks[3]))
            continue
        if head == "wire":
            pts = [tuple(int(v) for v in t.split(","))
                   for t in toks[3:] if "," in t]
            plan.wires.append((toks[1], pts))
            plan.warnings.append(
                f"wire hint for '{toks[1]}' parsed but not applied yet (P3)")
            continue
        if in_flow:
            plan.warnings.append(f"unrecognized flow line: {line.strip()}")
        else:
            plan.warnings.append(f"unrecognized line: {line.strip()}")
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

    _emit_tile_wiring(sheet)
    return sheet


# ================================================================ helpers

def plan_for(design: Design, subname: str) -> str:
    """Run automatic interpretation and emit its plan."""
    sub = design.subckts[subname]
    sheet = place(sub)
    sheet._src = design.path
    return emit_plan(sub, sheet)
