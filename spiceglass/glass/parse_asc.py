"""LTspice .asc reader + renderer — the assembler layer, readable.

Parses .asc sheets and .asy symbols (ours from sg_sym/, or LTspice's
native library if an installation is found) and renders faithful SVG.
Transform convention matches glass.geom's orientation algebra, so our
own exports round-trip pixel-faithfully; mirrored orientations of
foreign files are experimental.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

S_DEFAULT_W, S_DEFAULT_H = 880, 680

_LT_SYM_DIRS = [
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\ADI\LTspice\lib\sym"),
    r"C:\Program Files\ADI\LTspice\lib\sym",
    r"C:\Program Files\LTC\LTspiceXVII\lib\sym",
    os.path.expandvars(r"%USERPROFILE%\Documents\LTspiceXVII\lib\sym"),
]


@dataclass
class AscInstance:
    sym: str
    x: int
    y: int
    rot: str = "R0"
    attrs: dict[str, str] = field(default_factory=dict)


@dataclass
class AscSheet:
    w: int = S_DEFAULT_W
    h: int = S_DEFAULT_H
    wires: list[tuple[int, int, int, int]] = field(default_factory=list)
    flags: list[tuple[int, int, str]] = field(default_factory=list)
    insts: list[AscInstance] = field(default_factory=list)
    texts: list[tuple[int, int, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class AsySymbol:
    lines: list[tuple[int, int, int, int]] = field(default_factory=list)
    circles: list[tuple[int, int, int, int]] = field(default_factory=list)
    rects: list[tuple[int, int, int, int]] = field(default_factory=list)
    arcs: list[tuple] = field(default_factory=list)
    pins: list[tuple[int, int, str]] = field(default_factory=list)


def _read_text(path: str) -> str:
    raw = open(path, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1252", "replace")


def parse_asc(path: str) -> AscSheet:
    sheet = AscSheet()
    pending: AscInstance | None = None
    for no, line in enumerate(_read_text(path).splitlines(), 1):
        t = line.split()
        if not t:
            continue
        head = t[0].upper()
        try:
            if head == "SHEET" and len(t) >= 4:
                sheet.w, sheet.h = int(t[2]), int(t[3])
            elif head == "WIRE" and len(t) >= 5:
                sheet.wires.append(tuple(int(v) for v in t[1:5]))
            elif head == "FLAG" and len(t) >= 4:
                sheet.flags.append((int(t[1]), int(t[2]), t[3]))
            elif head == "SYMBOL" and len(t) >= 5:
                pending = AscInstance(sym=t[1].replace("\\\\", "\\"),
                                      x=int(t[2]), y=int(t[3]),
                                      rot=t[4].upper())
                sheet.insts.append(pending)
            elif head == "SYMATTR" and len(t) >= 3 and pending is not None:
                pending.attrs[t[1]] = " ".join(t[2:])
            elif head == "TEXT" and len(t) >= 5:
                m = re.search(r"TEXT\s+(-?\d+)\s+(-?\d+)\s+\S+\s+\S+\s+(.*)",
                              line)
                if m:
                    sheet.texts.append((int(m.group(1)), int(m.group(2)),
                                        m.group(3).lstrip("!;")))
        except ValueError:
            sheet.warnings.append(f"line {no}: unparsed: {line.strip()}")
    return sheet


def parse_asy(path: str) -> AsySymbol:
    sym = AsySymbol()
    pin: tuple[int, int] | None = None
    for line in _read_text(path).splitlines():
        t = line.split()
        if not t:
            continue
        head = t[0].upper()
        try:
            if head == "LINE" and len(t) >= 6:
                sym.lines.append(tuple(int(v) for v in t[2:6]))
            elif head == "CIRCLE" and len(t) >= 6:
                sym.circles.append(tuple(int(v) for v in t[2:6]))
            elif head == "RECTANGLE" and len(t) >= 6:
                sym.rects.append(tuple(int(v) for v in t[2:6]))
            elif head == "ARC" and len(t) >= 10:
                sym.arcs.append(tuple(int(v) for v in t[2:10]))
            elif head == "PIN" and len(t) >= 3:
                pin = (int(t[1]), int(t[2]))
            elif head == "PINATTR" and len(t) >= 3 and t[1] == "PinName" \
                    and pin is not None:
                sym.pins.append((pin[0], pin[1], t[2]))
                pin = None
        except ValueError:
            pass
    return sym


def resolve_asy(symname: str, asc_dir: str) -> str | None:
    rel = symname.replace("\\", os.sep) + ".asy"
    cands = [os.path.join(asc_dir, rel)]
    base = os.path.basename(rel)
    cands += [os.path.join(d, rel) for d in _LT_SYM_DIRS]
    cands += [os.path.join(d, base) for d in _LT_SYM_DIRS]
    return next((c for c in cands if os.path.exists(c)), None)


# same algebra as glass.geom.orient_xy (LTspice M-variants experimental)
_ROT = {
    "R0": lambda x, y: (x, y), "R90": lambda x, y: (y, -x),
    "R180": lambda x, y: (-x, -y), "R270": lambda x, y: (-y, x),
    "M0": lambda x, y: (-x, y), "M180": lambda x, y: (x, -y),
    "M90": lambda x, y: (y, x), "M270": lambda x, y: (-y, -x),
}

_TF = {"R0": "", "R90": " rotate(-90)", "R180": " rotate(180)",
       "R270": " rotate(90)", "M0": " scale(-1 1)",
       "M180": " scale(1 -1)", "M90": " rotate(-90) scale(-1 1)",
       "M270": " rotate(-90) scale(1 -1)"}


def asc_to_svg(sheet: AscSheet, asc_dir: str) -> str:
    import html

    def esc(s: str) -> str:
        return html.escape(s, quote=True)

    # bounds: include geometry, not just declared sheet size
    xs = [0, sheet.w]
    ys = [0, sheet.h]
    for (x1, y1, x2, y2) in sheet.wires:
        xs += [x1, x2]
        ys += [y1, y2]
    for inst in sheet.insts:
        xs += [inst.x - 80, inst.x + 80]
        ys += [inst.y - 80, inst.y + 80]
    x0, y0 = min(xs) - 24, min(ys) - 24
    W, H = max(xs) - x0 + 48, max(ys) - y0 + 48

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" '
         f'height="{H}" viewBox="{x0} {y0} {W} {H}" '
         'font-family="Segoe UI, Arial, sans-serif">',
         '<style>line,circle,ellipse,rect,path{stroke:#1b1b1b;'
         'stroke-width:2;fill:none}'
         'circle.dot{fill:#1b1b1b !important;stroke:none !important}'
         'path.gnd{fill:#1b1b1b !important;stroke:none !important}'
         'text{stroke:none;fill:#222;font-size:14px}'
         '.flag{fill:#0b4ea2;font-weight:600}.nm{font-weight:600}'
         '.val{fill:#666;font-size:12px}</style>',
         f'<rect x="{x0}" y="{y0}" width="{W}" height="{H}" fill="white" '
         'stroke="none"/>']

    for (x1, y1, x2, y2) in sheet.wires:
        p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')

    # junction dots: an endpoint touching >=3 wire ends, or lying on
    # another wire's interior (LTspice derives these too)
    ends: dict[tuple[int, int], int] = {}
    for (x1, y1, x2, y2) in sheet.wires:
        ends[(x1, y1)] = ends.get((x1, y1), 0) + 1
        ends[(x2, y2)] = ends.get((x2, y2), 0) + 1
    for (x, y), n in ends.items():
        on_interior = any(
            (a == c and a == x and min(b, d) < y < max(b, d)) or
            (b == d and b == y and min(a, c) < x < max(a, c))
            for (a, b, c, d) in sheet.wires)
        if n >= 3 or (n >= 1 and on_interior):
            p.append(f'<circle class="dot" cx="{x}" cy="{y}" r="4"/>')

    for (x, y, name) in sheet.flags:
        if name == "0":
            p.append(f'<path class="gnd" d="M {x-10} {y+2} L {x+10} {y+2} '
                     f'L {x} {y+12} Z"/>')
            p.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+2}"/>')
        else:
            p.append(f'<text class="flag" x="{x+4}" y="{y-4}">'
                     f'{esc(name)}</text>')

    missing: set[str] = set()
    for inst in sheet.insts:
        asy_path = resolve_asy(inst.sym, asc_dir)
        tf = _TF.get(inst.rot, "")
        p.append(f'<g transform="translate({inst.x} {inst.y}){tf}">')
        if asy_path:
            sym = parse_asy(asy_path)
            for (a, b, c, d) in sym.lines:
                p.append(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>')
            for (a, b, c, d) in sym.rects:
                p.append(f'<rect x="{min(a, c)}" y="{min(b, d)}" '
                         f'width="{abs(c - a)}" height="{abs(d - b)}"/>')
            for (a, b, c, d) in sym.circles:
                cx, cy = (a + c) / 2, (b + d) / 2
                p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{abs(c-a)/2}" '
                         f'ry="{abs(d-b)/2}" fill="none" stroke="#1b1b1b" '
                         'stroke-width="2"/>')
        else:
            missing.add(inst.sym)
            p.append('<rect x="-24" y="-24" width="48" height="48" '
                     'stroke-dasharray="4 3"/>')
        p.append('</g>')
        nm = inst.attrs.get("InstName", "")
        val = inst.attrs.get("Value", "")
        if nm:
            p.append(f'<text class="nm" x="{inst.x + 30}" '
                     f'y="{inst.y - 10}">{esc(nm)}</text>')
        if val:
            p.append(f'<text class="val" x="{inst.x + 30}" '
                     f'y="{inst.y + 8}">{esc(val)}</text>')

    for (x, y, txt) in sheet.texts:
        p.append(f'<text x="{x}" y="{y}" class="val">{esc(txt)}</text>')
    for m in sorted(missing):
        sheet.warnings.append(f"symbol not found: {m} (dashed box)")
    p.append("</svg>")
    return "\n".join(p)
