"""Wire routing front-end.

Net classification (rail stubs, label stubs, ports, tile coverage/taps)
lives here; the actual wire paths come from glass.route2 — the GD 2009
orthogonal-visibility-graph A* router with nudging. Tile preroutes are
first-class geometry: the router may join them (route-to-net) and the
nudging pass treats them as immovable occupied tracks.

Every emitted artifact carries enough information for verify.py to
rebuild connectivity geometrically and compare it to the netlist.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .db import Subckt
from .geom import BOX_W, box_height, pin_pos
from .place import Sheet
from .route2 import Router2

_INPUTISH = re.compile(r"^(v?in\w*|vi[pm]\w*|clk\w*|reset\w*|en\w*|vcm|"
                       r"vb[npc]\w*|i?ref\w*_in)$", re.I)


@dataclass
class Seg:
    x1: float
    y1: float
    x2: float
    y2: float
    net: str


@dataclass
class Stub:
    kind: str          # vdd | gnd | label | port
    net: str
    px: float          # pin point (connects to symbol)
    py: float
    direction: str     # up | down | left | right
    text: str = ""
    role: str = ""     # terminal role; 'b' (bulk) renders compact/unlabeled


@dataclass
class Terminal:
    dev: str
    role: str
    net: str
    x: float
    y: float
    side: str = "C"    # L | R | C relative to the symbol body
    esc: str = "U"     # portal escape direction L|R|U|D


@dataclass
class Routing:
    segments: list[Seg] = field(default_factory=list)
    stubs: list[Stub] = field(default_factory=list)
    dots: list[tuple[float, float]] = field(default_factory=list)
    terminals: list[Terminal] = field(default_factory=list)
    dangling: list[Terminal] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    paths: dict[str, list] = field(default_factory=dict)   # editable routes
    pinned_nets: list[str] = field(default_factory=list)   # user-pinned
    debug: dict | None = None


def _obstacle(dev, p) -> tuple[int, int, int, int]:
    """Inflated symbol-tile rectangle (1-unit routing buffer)."""
    k = dev.kind
    if k in ("nmos", "pmos", "pnp", "npn"):
        hw, hh = 4, 5
    elif k in ("res", "cap", "ind", "dio", "vsrc", "isrc", "bsrc"):
        hw, hh = 3, 5
    else:
        hw = BOX_W // 2 + 1
        hh = box_height(len(dev.roles)) // 2 + 1
        return (p.x - hw, p.y - hh, p.x + hw, p.y + hh)
    if p.orient == "R90":
        hw, hh = hh, hw
    return (p.x - hw, p.y - hh, p.x + hw, p.y + hh)


def route(sheet: Sheet, debug: bool = False,
          pinned: dict[str, list] | None = None) -> Routing:
    """`pinned`: net -> list of point-paths the user hand-edited in the
    editor. A pinned net bypasses the engine IF its geometry still
    touches every pin of the net; otherwise the pin is dropped and the
    net re-routes normally (e.g. after the device moved away)."""
    sub: Subckt = sheet.sub
    r = Routing()
    pinned = pinned or {}

    # ---- collect every terminal with its absolute pin position
    net_pins: dict[str, list[Terminal]] = {}
    for d in sub.devices:
        p = sheet.pos(d)
        for role, net in zip(d.roles, d.nets):
            x, y = pin_pos(d, role, p.x, p.y, p.orient)
            dx, dy = x - p.x, y - p.y
            side = "L" if dx < -1 else ("R" if dx > 1 else "C")
            esc = ("L" if dx < -1 else "R") if abs(dx) > abs(dy) else \
                  ("U" if dy < 0 else "D")
            t = Terminal(dev=d.name, role=role, net=net, x=x, y=y,
                         side=side, esc=esc)
            r.terminals.append(t)
            if (d.name, role) in sheet.covered:
                continue            # terminal is wired inside a tile
            net_pins.setdefault(net, []).append(t)

    # tile taps participate in global routing as ordinary pins
    for (net, x, y, side) in sheet.taps:
        net_pins.setdefault(net, []).append(
            Terminal(dev="~tap", role="t", net=net, x=x, y=y,
                     side=side, esc="L" if side == "L" else "R"))

    covered_nets = {d.nets[i] for d in sub.devices
                    for i, role in enumerate(d.roles)
                    if (d.name, role) in sheet.covered}

    # tile preroutes are first-class geometry
    pre_by_net: dict[str, list[tuple[int, int, int, int]]] = {}
    for (x1, y1, x2, y2, net) in sheet.preroutes:
        r.segments.append(Seg(x1, y1, x2, y2, net))
        pre_by_net.setdefault(net, []).append((x1, y1, x2, y2))

    ports = set(sub.ports)
    jobs: list[tuple[str, list[Terminal]]] = []

    for net, pins in net_pins.items():
        if net in sheet.rails:
            kind = sheet.rails[net]
            for t in pins:
                r.stubs.append(Stub(kind=kind, net=net, px=t.x, py=t.y,
                                    direction=_stub_dir(t, kind), text=net,
                                    role=t.role))
            continue
        if net in sheet.label_nets:
            is_port = net in ports
            for t in pins:
                r.stubs.append(Stub(kind="port" if is_port else "label",
                                    net=net, px=t.x, py=t.y,
                                    direction=_label_dir(t), text=net,
                                    role=t.role))
            continue
        if len(pins) == 1 and net not in pre_by_net:
            t = pins[0]
            if net in ports:
                r.stubs.append(Stub(kind="port", net=net, px=t.x, py=t.y,
                                    direction=_label_dir(t), text=net))
            elif net not in covered_nets:
                r.dangling.append(t)
            continue
        jobs.append((net, pins))

    # ---- user-pinned wire paths: validate that every pin of the net
    #      still lies on the pinned geometry, then bypass the engine
    from .route2 import _on_seg
    valid_pinned: dict[str, list] = {}
    for net, paths in pinned.items():
        job = next((j for j in jobs if j[0] == net), None)
        if job is None:
            continue
        segs = []
        for path in paths:
            for a, b in zip(path, path[1:]):
                segs.append((a[0], a[1], b[0], b[1]))
        if segs and all(any(_on_seg(t.x, t.y, s) for s in segs)
                        for t in job[1]):
            valid_pinned[net] = [[list(p) for p in path] for path in paths]
        else:
            r.warnings.append(f"pinned wires for '{net}' no longer reach "
                              "all pins — re-routed")
    jobs = [j for j in jobs if j[0] not in valid_pinned]
    r.pinned_nets = sorted(valid_pinned)

    existing = {net: list(segs) for net, segs in pre_by_net.items()}
    for net, paths in valid_pinned.items():
        for path in paths:
            for a, b in zip(path, path[1:]):
                existing.setdefault(net, []).append(
                    (a[0], a[1], b[0], b[1]))

    # ---- the OVG/A* engine
    rects = [_obstacle(d, sheet.pos(d)) for d in sub.devices]
    portal: dict[tuple[int, int], str] = {}
    for net, pins in jobs:
        for t in pins:
            portal[(t.x, t.y)] = t.esc
    bounds = (1, 1, max(sheet.width - 1, 10), max(sheet.height - 1, 10))
    engine = Router2(rects, portal, bounds, debug=debug)
    result = engine.route_all(
        [(net, [(t.x, t.y) for t in pins]) for net, pins in jobs],
        existing)
    r.warnings.extend(result.warnings)

    net_segs: dict[str, list[Seg]] = {}
    for (x1, y1, x2, y2, net) in sheet.preroutes:
        net_segs.setdefault(net, []).append(Seg(x1, y1, x2, y2, net))
    all_paths = dict(result.paths)
    for net, paths in valid_pinned.items():
        all_paths.setdefault(net, [])
        all_paths[net] = all_paths[net] + paths
    r.paths = all_paths
    for net, paths in all_paths.items():
        for path in paths or []:
            for (a, b) in zip(path, path[1:]):
                if a == b:
                    continue
                s = Seg(a[0], a[1], b[0], b[1], net)
                r.segments.append(s)
                net_segs.setdefault(net, []).append(s)

    # junction dots: same-net endpoint landing on a segment interior
    for net, segs in net_segs.items():
        for s in segs:
            for (x, y) in ((s.x1, s.y1), (s.x2, s.y2)):
                for o in segs:
                    if o is s:
                        continue
                    if _interior(x, y, o):
                        r.dots.append((x, y))

    if debug:
        g = result.ovg
        r.debug = {
            "rects": rects,
            "vspans": g.vspans if g else [],
            "hspans": g.hspans if g else [],
            "nodes": len(g.coords) if g else 0,
            "nets": [{"net": v.net, "pins": v.pins, "raw": v.raw,
                      "visited": v.visited, "cost": v.cost}
                     for v in result.viz],
        }

    # ---- port flags
    for net, pins in net_pins.items():
        if net in sheet.rails or net in sheet.label_nets or net not in ports:
            continue
        if len(pins) >= 2 or net in pre_by_net:
            t = _port_anchor(pins, net)
            r.stubs.append(Stub(kind="port", net=net, px=t.x, py=t.y,
                                direction="left" if _INPUTISH.match(net)
                                else "right", text=net))
    flagged = {s.net for s in r.stubs if s.kind == "port"}
    flagged |= set(sheet.rails)
    for net in ports:
        if net in flagged or net in sheet.label_nets:
            continue
        t = next((t for t in r.terminals if t.net == net), None)
        if t is not None:
            r.stubs.append(Stub(kind="port", net=net, px=t.x, py=t.y,
                                direction=_label_dir(t), text=net))
    return r


def _interior(x, y, s: Seg) -> bool:
    if s.x1 == s.x2:
        return x == s.x1 and min(s.y1, s.y2) < y < max(s.y1, s.y2)
    return y == s.y1 and min(s.x1, s.x2) < x < max(s.x1, s.x2)


def _stub_dir(t: Terminal, kind: str) -> str:
    if t.role in ("d", "s", "p", "n", "c", "e"):
        return "up" if kind == "vdd" else "down"
    return "side_up" if kind == "vdd" else "side_down"


def _label_dir(t: Terminal) -> str:
    if t.side == "L":
        return "left"
    if t.side == "R":
        return "right"
    return "left" if t.role == "g" else "right"


def _port_anchor(pins: list[Terminal], net: str) -> Terminal:
    if _INPUTISH.match(net):
        return min(pins, key=lambda t: t.x)
    return max(pins, key=lambda t: t.x)
