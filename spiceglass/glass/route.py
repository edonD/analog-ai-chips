"""Orthogonal trunk router with rail stubs and net labels.

Rail nets are never routed — every rail terminal gets a stub glyph.
High-fanout nets become named label stubs (analog convention for bias
lines). Everything else gets vertical-drop + horizontal-trunk routing
with per-band track allocation so trunks never overlap.

Every emitted artifact is tagged with enough information for verify.py
to rebuild connectivity *geometrically* and compare it to the netlist.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .db import Subckt
from .geom import ROW_H, pin_pos
from .place import Sheet

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
    side: str = "C"    # L | R | C relative to the symbol body (escape direction)


@dataclass
class Routing:
    segments: list[Seg] = field(default_factory=list)
    stubs: list[Stub] = field(default_factory=list)
    dots: list[tuple[float, float]] = field(default_factory=list)
    terminals: list[Terminal] = field(default_factory=list)
    dangling: list[Terminal] = field(default_factory=list)


def route(sheet: Sheet) -> Routing:
    sub: Subckt = sheet.sub
    r = Routing()

    # ---- collect every terminal with its absolute pin position
    net_pins: dict[str, list[Terminal]] = {}
    for d in sub.devices:
        p = sheet.pos(d)
        for role, net in zip(d.roles, d.nets):
            x, y = pin_pos(d, role, p.x, p.y, p.mirror)
            dx = x - p.x
            side = "L" if dx < -20 else ("R" if dx > 20 else "C")
            t = Terminal(dev=d.name, role=role, net=net, x=x, y=y, side=side)
            r.terminals.append(t)
            net_pins.setdefault(net, []).append(t)

    band_use: dict[int, int] = {}
    # vertical-lane registry: rounded x -> [(net, ymin, ymax)], used to keep
    # different nets' vertical runs from overlapping on one line. Pins are
    # seeded as zero-length intervals so no vertical ever runs over a
    # foreign pin (the classic stacked-box-pin short).
    lanes: dict[float, list[tuple[str, float, float]]] = {}
    for t in r.terminals:
        lanes.setdefault(round(t.x, 1), []).append((t.net, t.y, t.y))

    def track_y(pins: list[Terminal]) -> float:
        ys = sorted(t.y for t in pins)
        mid = ys[len(ys) // 2]
        band = round((mid - 84.0) / ROW_H)
        k = band_use.get(band, 0)
        band_use[band] = k + 1
        base = 84.0 + band * ROW_H + ROW_H / 2.0
        offset = (k % 7 - 3) * 9.0
        return base + offset

    ports = set(sub.ports)

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

        if len(pins) == 1:
            t = pins[0]
            if net in ports:
                r.stubs.append(Stub(kind="port", net=net, px=t.x, py=t.y,
                                    direction=_label_dir(t), text=net))
            else:
                r.dangling.append(t)
            continue

        _route_net(r, net, pins, track_y, lanes)
        if net in ports:
            t = _port_anchor(pins, net)
            r.stubs.append(Stub(kind="port", net=net, px=t.x, py=t.y,
                                direction="left" if _INPUTISH.match(net) else "right",
                                text=net))

    return r


def _stub_dir(t: Terminal, kind: str) -> str:
    if t.role in ("d", "s", "p", "n", "c", "e") :
        # top/bottom pin: stub continues outward
        return "up" if kind == "vdd" else "down"
    return "side_up" if kind == "vdd" else "side_down"


def _label_dir(t: Terminal) -> str:
    if t.role == "g" or t.role == "b" and abs(t.y) >= 0:
        return "left" if t.role == "g" else "right"
    return "right"


def _port_anchor(pins: list[Terminal], net: str) -> Terminal:
    if _INPUTISH.match(net):
        return min(pins, key=lambda t: t.x)
    return max(pins, key=lambda t: t.x)


def _claim_lane(lanes, net: str, x: float, y1: float, y2: float,
                side: str) -> float:
    """Return an x where a vertical (y1..y2) won't overlap another net."""
    lo, hi = min(y1, y2), max(y1, y2)
    step = -7.0 if side == "L" else 7.0
    cand = x
    for _ in range(12):
        kx = round(cand, 1)
        clash = any(n != net and hi > a - 0.2 and lo < b + 0.2
                    for (n, a, b) in lanes.get(kx, []))
        if not clash:
            lanes.setdefault(kx, []).append((net, lo, hi))
            return cand
        cand += step
    lanes.setdefault(round(cand, 1), []).append((net, lo, hi))
    return cand


def _route_net(r: Routing, net: str, pins: list[Terminal], track_y,
               lanes) -> None:
    xs = {round(t.x, 1) for t in pins}
    if len(xs) == 1:
        ordered = sorted(pins, key=lambda t: t.y)
        x = _claim_lane(lanes, net, ordered[0].x, ordered[0].y,
                        ordered[-1].y, ordered[0].side)
        if abs(x - ordered[0].x) > 0.1:     # column line already taken: jog
            for t in ordered:
                r.segments.append(Seg(t.x, t.y, x, t.y, net))
            r.segments.append(Seg(x, ordered[0].y, x, ordered[-1].y, net))
        else:
            for a, b in zip(ordered, ordered[1:]):
                if abs(a.y - b.y) > 0.1:
                    r.segments.append(Seg(a.x, a.y, b.x, b.y, net))
        return

    ty = track_y(pins)
    drop_xs: list[float] = []
    for t in pins:
        if abs(t.y - ty) <= 0.1:
            drop_xs.append(t.x)
            continue
        dx = _claim_lane(lanes, net, t.x, t.y, ty, t.side)
        if abs(dx - t.x) > 0.1:
            r.segments.append(Seg(t.x, t.y, dx, t.y, net))   # escape jog
        r.segments.append(Seg(dx, t.y, dx, ty, net))
        drop_xs.append(dx)
    minx, maxx = min(drop_xs), max(drop_xs)
    if maxx - minx > 0.1:
        r.segments.append(Seg(minx, ty, maxx, ty, net))
    for x in drop_xs:
        if len(drop_xs) > 2 and minx + 0.1 < x < maxx - 0.1:
            r.dots.append((x, ty))
