"""SVG renderer: symbol library + wires + furniture.

Pin positions MUST match glass.geom — that contract is what lets the
verifier treat the drawing as ground truth.
"""
from __future__ import annotations

import html

from .classify import short_model
from .db import Device, Subckt
from .geom import BOX_PIN_DY, BOX_W, box_height, pin_offsets
from .place import Sheet
from .route import Routing, Stub

WIRE = "#1b1b1b"
SYM = "#111111"
LABELC = "#a14d00"
PORTC = "#0b4ea2"
RAILC = "#444444"
SECTION_FILLS = ["#fff3df", "#e8f3e6", "#e6ecf7", "#f7e6ee", "#eef7e6",
                 "#f3e6f7", "#e6f5f7", "#f7f0e6"]


def _esc(t: str) -> str:
    return html.escape(t, quote=True)


# ------------------------------------------------------------ symbols

def _mos(dev: Device) -> list[str]:
    pmos = dev.kind == "pmos"
    e = []
    e.append('<line x1="8" y1="-38" x2="8" y2="-20"/>')      # top stub
    e.append('<line x1="8" y1="20" x2="8" y2="38"/>')        # bottom stub
    e.append('<line x1="8" y1="-20" x2="8" y2="20"/>')       # channel
    e.append('<line x1="0" y1="-14" x2="0" y2="14"/>')       # gate plate
    e.append('<line x1="8" y1="-20" x2="22" y2="-20"/>')
    e.append('<line x1="8" y1="20" x2="22" y2="20"/>')
    if pmos:
        e.append('<circle cx="-6" cy="0" r="5" fill="white"/>')
        e.append('<line x1="-30" y1="0" x2="-11" y2="0"/>')
    else:
        e.append('<line x1="-30" y1="0" x2="0" y2="0"/>')
        e.append('<path d="M 2 26 L 8 32 L 2 32 Z" fill="{c}" stroke="none"/>'
                 .format(c=SYM))                              # source arrow tick
    if "b" in dev.roles:
        e.append('<line x1="8" y1="0" x2="16" y2="0"/>')
    return e


def _res(dev: Device) -> list[str]:
    pts = []
    y = -22
    step = 44 / 6
    xs = [0, 9, -9, 9, -9, 9, 0]
    for i, x in enumerate(xs):
        pts.append(f"{x},{y + i * step:.1f}")
    e = ['<line x1="0" y1="-38" x2="0" y2="-22"/>',
         '<line x1="0" y1="22" x2="0" y2="38"/>',
         f'<polyline points="{" ".join(pts)}" fill="none"/>']
    if "b" in dev.roles:
        e.append('<line x1="0" y1="0" x2="18" y2="0" stroke-dasharray="3 2"/>')
    return e


def _cap(dev: Device) -> list[str]:
    e = ['<line x1="0" y1="-38" x2="0" y2="-6"/>',
         '<line x1="0" y1="6" x2="0" y2="38"/>',
         '<line x1="-13" y1="-6" x2="13" y2="-6"/>',
         '<line x1="-13" y1="6" x2="13" y2="6"/>']
    if "b" in dev.roles:
        e.append('<line x1="0" y1="6" x2="18" y2="6" stroke-dasharray="3 2"/>')
        e.append('<line x1="18" y1="6" x2="18" y2="0"/>')
    return e


def _dio(dev: Device) -> list[str]:
    return ['<line x1="0" y1="-38" x2="0" y2="-9"/>',
            '<line x1="0" y1="9" x2="0" y2="38"/>',
            f'<path d="M -10 -9 L 10 -9 L 0 9 Z" fill="none"/>',
            '<line x1="-10" y1="9" x2="10" y2="9"/>']


def _src(dev: Device) -> list[str]:
    e = ['<line x1="0" y1="-38" x2="0" y2="-16"/>',
         '<line x1="0" y1="16" x2="0" y2="38"/>']
    if dev.kind == "bsrc":
        e.append('<path d="M 0 -16 L 13 0 L 0 16 L -13 0 Z" fill="white"/>')
        e.append('<text x="0" y="4" text-anchor="middle" class="sym">B</text>')
    else:
        e.append('<circle cx="0" cy="0" r="15" fill="white"/>')
        mark = "V" if dev.kind == "vsrc" else "I"
        e.append(f'<text x="0" y="4" text-anchor="middle" class="sym">{mark}</text>')
    return e


def _bjt(dev: Device) -> list[str]:
    return ['<circle cx="2" cy="0" r="18" fill="none"/>',
            '<line x1="-30" y1="0" x2="-6" y2="0"/>',
            '<line x1="-6" y1="-10" x2="-6" y2="10"/>',
            '<line x1="-6" y1="-4" x2="10" y2="-14"/>',
            '<line x1="10" y1="-14" x2="10" y2="-38"/>',
            '<line x1="-6" y1="4" x2="10" y2="14"/>',
            '<line x1="10" y1="14" x2="10" y2="38"/>']


def _box(dev: Device) -> list[str]:
    h = box_height(len(dev.roles))
    e = [f'<rect x="{-BOX_W/2}" y="{-h/2}" width="{BOX_W}" height="{h}" '
         f'rx="4" fill="white"/>']
    offs = pin_offsets(dev, False)
    for role in dev.roles:
        px, py = offs[role]
        anchor = "start" if px < 0 else "end"
        tx = px + 6 if px < 0 else px - 6
        e.append(f'<text x="{tx}" y="{py + 3.5}" text-anchor="{anchor}" '
                 f'class="pin">{_esc(role)}</text>')
    e.append(f'<text x="0" y="{h/2 - 8}" text-anchor="middle" class="boxmodel">'
             f'{_esc(dev.model)}</text>')
    return e


def _symbol_elems(dev: Device) -> list[str]:
    k = dev.kind
    if k in ("nmos", "pmos"):
        return _mos(dev)
    if k == "res":
        return _res(dev)
    if k in ("cap",):
        return _cap(dev)
    if k == "dio":
        return _dio(dev)
    if k in ("vsrc", "isrc", "bsrc"):
        return _src(dev)
    if k in ("pnp", "npn"):
        return _bjt(dev)
    return _box(dev)


# ------------------------------------------------------------ stubs

def _stub_svg(s: Stub, multi_gnd: bool) -> str:
    e = []
    x, y = s.px, s.py
    bulk = s.role == "b"
    if s.kind == "vdd":
        if s.direction.startswith("side"):
            e.append(f'<line x1="{x}" y1="{y}" x2="{x + 12}" y2="{y}"/>')
            x += 12
            e.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - 10}"/>')
            y -= 10
        else:
            e.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - 14}"/>')
            y -= 14
        bw = 5 if bulk else 9
        e.append(f'<line x1="{x - bw}" y1="{y}" x2="{x + bw}" y2="{y}" '
                 'stroke-width="2.4"/>')
        if not bulk:
            e.append(f'<text x="{x}" y="{y - 5}" text-anchor="middle" '
                     f'class="rail">{_esc(s.text.upper())}</text>')
    elif s.kind == "gnd":
        if s.direction.startswith("side"):
            e.append(f'<line x1="{x}" y1="{y}" x2="{x + 12}" y2="{y}"/>')
            x += 12
        e.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + 12}"/>')
        y += 12
        widths = (5, 3) if bulk else (9, 6, 3)
        for i, w in enumerate(widths):
            e.append(f'<line x1="{x - w}" y1="{y + i * 4}" x2="{x + w}" '
                     f'y2="{y + i * 4}" stroke-width="2"/>')
        if multi_gnd and not bulk:
            e.append(f'<text x="{x}" y="{y + 22}" text-anchor="middle" '
                     f'class="rail">{_esc(s.text)}</text>')
    else:                                   # label | port
        dx = -22 if s.direction == "left" else 22
        e.append(f'<line x1="{x}" y1="{y}" x2="{x + dx}" y2="{y}"/>')
        cls = "port" if s.kind == "port" else "netlabel"
        anchor = "end" if dx < 0 else "start"
        tx = x + dx + (4 if dx > 0 else -4)
        if s.kind == "port":
            w = 7 * max(3, len(s.text))
            bx = x + dx if dx > 0 else x + dx - w
            e.append(f'<rect x="{bx}" y="{y - 9}" width="{w}" height="18" '
                     f'rx="3" fill="white" stroke="{PORTC}" stroke-width="1.4"/>')
            tx = bx + w / 2
            anchor = "middle"
        e.append(f'<text x="{tx}" y="{y + 4}" text-anchor="{anchor}" '
                 f'class="{cls}">{_esc(s.text)}</text>')
    return "".join(e)


# ------------------------------------------------------------ sheet

def render_sheet(sheet: Sheet, routing: Routing, verdict, meta: dict) -> str:
    sub: Subckt = sheet.sub
    W, H = sheet.width, sheet.height + 70
    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" '
        f'height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" '
        'font-family="Segoe UI, Arial, sans-serif">')
    parts.append("""<style>
 line, polyline, path, rect, circle { stroke: %s; stroke-width: 1.8; }
 .wire { stroke: %s; stroke-width: 1.6; }
 text { stroke: none; fill: #222; font-size: 11px; }
 .name { font-weight: 600; font-size: 11px; }
 .param { fill: #666; font-size: 9.5px; }
 .pin { font-size: 9px; fill: #333; }
 .sym { font-size: 11px; font-weight: 700; }
 .boxmodel { font-size: 9.5px; fill: #555; font-style: italic; }
 .rail { font-size: 9px; fill: %s; font-weight: 600; }
 .netlabel { font-size: 10.5px; fill: %s; font-style: italic; }
 .port { font-size: 10.5px; fill: %s; font-weight: 700; }
 .sectitle { font-size: 11px; fill: #8a7340; font-weight: 600; }
 .title { font-size: 16px; font-weight: 700; }
 .meta { font-size: 10px; fill: #555; }
</style>""" % (SYM, WIRE, RAILC, LABELC, PORTC))
    parts.append(f'<rect x="0" y="0" width="{W:.0f}" height="{H:.0f}" '
                 'fill="white" stroke="none"/>')

    # section shading (behind everything)
    sec_bounds: dict[str, list[float]] = {}
    for d in sub.devices:
        p = sheet.pos(d)
        b = sec_bounds.setdefault(d.section or "", [p.x, p.y, p.x, p.y])
        b[0] = min(b[0], p.x); b[1] = min(b[1], p.y)
        b[2] = max(b[2], p.x); b[3] = max(b[3], p.y)
    si = 0
    for sec in sub.sections:
        if sec not in sec_bounds:
            continue
        x0, y0, x1, y1 = sec_bounds[sec]
        fill = SECTION_FILLS[si % len(SECTION_FILLS)]
        si += 1
        parts.append(f'<rect x="{x0 - 72}" y="{y0 - 62}" width="{x1 - x0 + 144}" '
                     f'height="{y1 - y0 + 124}" rx="10" fill="{fill}" '
                     'stroke="none" opacity="0.7"/>')
        parts.append(f'<text x="{x0 - 66}" y="{y0 - 68}" class="sectitle">'
                     f'{_esc(sec)}</text>')

    # wires
    for s in routing.segments:
        parts.append(f'<line class="wire" x1="{s.x1:.1f}" y1="{s.y1:.1f}" '
                     f'x2="{s.x2:.1f}" y2="{s.y2:.1f}"/>')
    for (x, y) in routing.dots:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{WIRE}" '
                     'stroke="none"/>')

    # stubs
    gnd_nets = {s.net for s in routing.stubs if s.kind == "gnd"}
    multi_gnd = len(gnd_nets) > 1
    for s in routing.stubs:
        parts.append(_stub_svg(s, multi_gnd))

    # dangling markers
    for t in routing.dangling:
        parts.append(f'<circle cx="{t.x}" cy="{t.y}" r="4" fill="none" '
                     'stroke="#cc0000" stroke-width="1.6"/>')

    # symbols + annotations
    for d in sub.devices:
        p = sheet.pos(d)
        sx = -1 if p.mirror else 1
        parts.append(f'<g transform="translate({p.x:.1f} {p.y:.1f}) '
                     f'scale({sx} 1)" fill="none">')
        parts.extend(_symbol_elems(d))
        parts.append('</g>')
        parts.append(f'<text x="{p.x - 34}" y="{p.y - 44}" class="name">'
                     f'{_esc(d.name)}</text>')
        ann = _annotation(d)
        if ann:
            parts.append(f'<text x="{p.x + 20}" y="{p.y + 58}" class="param" '
                         f'text-anchor="start">{_esc(ann)}</text>')

    # title block + stamp
    y0 = H - 46
    parts.append(f'<line x1="{20}" y1="{y0 - 14}" x2="{W - 20}" y2="{y0 - 14}" '
                 'stroke="#999" stroke-width="1"/>')
    parts.append(f'<text x="26" y="{y0 + 6}" class="title">{_esc(sub.name)}</text>')
    nd = len(sub.devices)
    parts.append(f'<text x="26" y="{y0 + 22}" class="meta">'
                 f'{_esc(meta.get("path", ""))} — {nd} devices — '
                 f'ports: {_esc(", ".join(sub.ports))} — SpiceGlass M0 — '
                 f'{_esc(meta.get("date", ""))}</text>')
    if verdict is not None:
        ok = verdict.ok
        color = "#0a7d28" if ok else "#bb1111"
        label = "VERIFIED ✓" if ok else "MISMATCH ✗"
        parts.append(f'<rect x="{W - 150}" y="14" width="128" height="30" rx="6" '
                     f'fill="none" stroke="{color}" stroke-width="2.4"/>')
        parts.append(f'<text x="{W - 86}" y="34" text-anchor="middle" '
                     f'style="fill:{color};font-weight:800;font-size:14px">'
                     f'{label}</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def _annotation(dev: Device) -> str:
    bits = []
    sm = short_model(dev)
    if sm:
        bits.append(sm)
    for k in ("w", "l", "m"):
        if k in dev.params:
            bits.append(f"{k}={dev.params[k]}")
    if dev.kind in ("res", "cap", "ind") and "value" in dev.params and not dev.model:
        bits = [dev.params["value"]]
    if dev.expr:
        ex = dev.expr if len(dev.expr) <= 28 else dev.expr[:25] + "…"
        bits.append(ex)
    return "  ".join(bits)
