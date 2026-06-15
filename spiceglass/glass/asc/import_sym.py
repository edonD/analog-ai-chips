"""Import real symbol libraries (KiCad .kicad_sym, xschem .sym) and
convert them to our AsySymbol / LTspice .asy — so SpiceGlass can use the
huge KiCad/PDK ecosystems while staying native to the .asc hub.

Pins are converted to the exact connection points (the electrical
contract) so wires land and SPICE order is preserved; geometry is mapped
to our integer grid (16 units = 1.27 mm). KiCad libraries are CC-BY-SA
(attribution kept by the caller); xschem .sym is GPL for the base lib but
Apache for the PDK libs — we convert the user's own files on demand and
never bundle vendor symbols in the repo.
"""
from __future__ import annotations

import math

KI_SCALE = 16.0 / 1.27          # KiCad mm -> our units (16u = 1.27mm)
XS_SCALE = 1.6                  # xschem (10u grid) -> our 16u grid


def _sym():
    from .parse import AsySymbol
    return AsySymbol()


# =================================================================== KiCad
def _tokenize(s: str):
    toks, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c in " \t\r\n":
            i += 1
        elif c in "()":
            toks.append(c); i += 1
        elif c == '"':
            j, buf = i + 1, []
            while j < n:
                if s[j] == "\\" and j + 1 < n:
                    buf.append(s[j + 1]); j += 2; continue
                if s[j] == '"':
                    break
                buf.append(s[j]); j += 1
            toks.append(("".join(buf))); i = j + 1
        else:
            j = i
            while j < n and s[j] not in ' \t\r\n()"':
                j += 1
            toks.append(s[i:j]); i = j
    return toks


def _parse_sexpr(text: str):
    toks = _tokenize(text)
    pos = 0

    def rd():
        nonlocal pos
        t = toks[pos]; pos += 1
        if t == "(":
            lst = []
            while toks[pos] != ")":
                lst.append(rd())
            pos += 1
            return lst
        return t
    # skip to first '('
    while pos < len(toks) and toks[pos] != "(":
        pos += 1
    return rd() if pos < len(toks) else []


def _kids(node, head):
    return [c for c in node if isinstance(c, list) and c and c[0] == head]


def _first(node, head):
    for c in node:
        if isinstance(c, list) and c and c[0] == head:
            return c
    return None


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def _kc(x, y):                      # KiCad mm -> our units (Y down)
    return round(x * KI_SCALE), round(-y * KI_SCALE)


def parse_kicad_lib(text: str) -> dict:
    """All symbols in a .kicad_sym -> {name: AsySymbol}."""
    tree = _parse_sexpr(text)
    if not tree or tree[0] != "kicad_symbol_lib":
        return {}
    raw = {}
    for s in _kids(tree, "symbol"):
        if len(s) >= 2 and isinstance(s[1], str):
            raw[s[1]] = s
    out = {}
    for name in raw:
        try:
            sym = _build_kicad(name, raw)
            if sym and sym.pins:
                out[name.split(":")[-1]] = sym
        except Exception:
            pass
    return out


def _build_kicad(name, raw, _depth=0):
    node = raw[name]
    sym = _sym()
    ext = _first(node, "extends")
    if ext and len(ext) >= 2 and ext[1] in raw and _depth < 6:
        sym = _build_kicad(ext[1], raw, _depth + 1)   # inherit parent body
    # nested unit/style sub-symbols: take style 1, units 0 (common) and 1
    for sub in _kids(node, "symbol"):
        nm = sub[1] if len(sub) >= 2 and isinstance(sub[1], str) else ""
        parts = nm.rsplit("_", 2)
        unit = int(parts[1]) if len(parts) == 3 and parts[1].isdigit() else 0
        style = int(parts[2]) if len(parts) == 3 and parts[2].isdigit() else 1
        if style not in (0, 1) or unit not in (0, 1):
            continue
        _collect_kicad(sub, sym)
    return sym


def _collect_kicad(sub, sym):
    for r in _kids(sub, "rectangle"):
        st, en = _first(r, "start"), _first(r, "end")
        x1, y1 = _kc(_num(st[1]), _num(st[2]))
        x2, y2 = _kc(_num(en[1]), _num(en[2]))
        sym.rects.append((x1, y1, x2, y2))
    for pl in _kids(sub, "polyline"):
        pts = _first(pl, "pts")
        xy = [(_num(p[1]), _num(p[2])) for p in _kids(pts, "xy")]
        for a, b in zip(xy, xy[1:]):
            x1, y1 = _kc(*a); x2, y2 = _kc(*b)
            sym.lines.append((x1, y1, x2, y2))
    for ci in _kids(sub, "circle"):
        ce = _first(ci, "center"); r = _num(_first(ci, "radius")[1])
        cx, cy = _num(ce[1]), _num(ce[2])
        x1, y1 = _kc(cx - r, cy - r); x2, y2 = _kc(cx + r, cy + r)
        sym.circles.append((x1, y1, x2, y2))
    for ar in _kids(sub, "arc"):
        a = _arc_from_3pt(_first(ar, "start"), _first(ar, "mid"),
                          _first(ar, "end"))
        if a:
            sym.arcs.append(a)
    for pin in _kids(sub, "pin"):
        at = _first(pin, "at"); ln = _num((_first(pin, "length") or [0, 0])[1])
        x, y, ang = _num(at[1]), _num(at[2]), _num(at[3]) if len(at) > 3 else 0
        nm = _first(pin, "name"); name = nm[1] if nm and len(nm) > 1 else ""
        ex, ey = _kc(x, y)                                   # connection point
        ix, iy = _kc(x + ln * math.cos(math.radians(ang)),
                     y + ln * math.sin(math.radians(ang)))   # into body
        if (ex, ey) != (ix, iy):
            sym.lines.append((ex, ey, ix, iy))               # pin stem
        sym.pins.append((ex, ey, name if name not in ("~", "") else
                         str(len(sym.pins) + 1)))


def _arc_from_3pt(st, mid, en):
    if not (st and mid and en):
        return None
    p = [_kc(_num(st[1]), _num(st[2])), _kc(_num(mid[1]), _num(mid[2])),
         _kc(_num(en[1]), _num(en[2]))]
    (ax, ay), (bx, by), (cx, cy) = p
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-6:
        return None
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay)
          + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx)
          + (cx * cx + cy * cy) * (bx - ax)) / d
    r = math.hypot(ax - ux, ay - uy)
    if r < 0.5:
        return None
    ang = lambda px, py: math.atan2(py - uy, px - ux)
    a0, am, a1 = ang(ax, ay), ang(bx, by), ang(cx, cy)
    dm = (am - a0) % (2 * math.pi); de = (a1 - a0) % (2 * math.pi)
    s, e = (p[0], p[2]) if dm <= de else (p[2], p[0])   # CCW passes mid
    return (round(ux - r), round(uy - r), round(ux + r), round(uy + r),
            s[0], s[1], e[0], e[1])


# ================================================================== xschem
def parse_xschem(text: str):
    """One xschem .sym -> AsySymbol."""
    sym = _sym()
    for line in text.splitlines():
        t = line.split()
        if not t:
            continue
        h = t[0]
        try:
            if h == "L" and len(t) >= 6:
                sym.lines.append((round(_num(t[2]) * XS_SCALE),
                                  round(_num(t[3]) * XS_SCALE),
                                  round(_num(t[4]) * XS_SCALE),
                                  round(_num(t[5]) * XS_SCALE)))
            elif h == "B" and len(t) >= 6:
                x1, y1 = _num(t[2]) * XS_SCALE, _num(t[3]) * XS_SCALE
                x2, y2 = _num(t[4]) * XS_SCALE, _num(t[5]) * XS_SCALE
                if t[1] == "5":                              # pin box
                    m = line[line.find("{"):]
                    nm = ""
                    mm = __import__("re").search(r"name=([^\s}]+)", m)
                    if mm:
                        nm = mm.group(1)
                    sym.pins.append((round((x1 + x2) / 2), round((y1 + y2) / 2),
                                     nm or str(len(sym.pins) + 1)))
                else:
                    sym.rects.append((round(x1), round(y1),
                                      round(x2), round(y2)))
            elif h == "A" and len(t) >= 7:                   # arc/circle
                cx, cy = _num(t[2]) * XS_SCALE, _num(t[3]) * XS_SCALE
                r = _num(t[4]) * XS_SCALE
                a0 = math.radians(_num(t[5])); sweep = math.radians(_num(t[6]))
                if abs(_num(t[6])) >= 359:
                    sym.circles.append((round(cx - r), round(cy - r),
                                        round(cx + r), round(cy + r)))
                else:
                    s = (cx + r * math.cos(a0), cy - r * math.sin(a0))
                    e = (cx + r * math.cos(a0 + sweep),
                         cy - r * math.sin(a0 + sweep))
                    sym.arcs.append((round(cx - r), round(cy - r),
                                     round(cx + r), round(cy + r),
                                     round(s[0]), round(s[1]),
                                     round(e[0]), round(e[1])))
            elif h == "P" and len(t) >= 4:                   # polygon
                npts = int(_num(t[2]))
                co = [(_num(t[3 + 2 * k]) * XS_SCALE, _num(t[4 + 2 * k]) * XS_SCALE)
                      for k in range(npts)]
                for a, b in zip(co, co[1:]):
                    sym.lines.append((round(a[0]), round(a[1]),
                                      round(b[0]), round(b[1])))
        except (ValueError, IndexError):
            pass
    return sym


# ============================================================== .asy emit
def asy_text(sym, name="imported") -> str:
    """AsySymbol -> LTspice .asy text (so imports round-trip + resolve)."""
    out = ["Version 4", "SymbolType CELL"]
    for (x1, y1, x2, y2) in sym.lines:
        out.append(f"LINE Normal {x1} {y1} {x2} {y2}")
    for (x1, y1, x2, y2) in sym.rects:
        out.append(f"RECTANGLE Normal {x1} {y1} {x2} {y2}")
    for (x1, y1, x2, y2) in sym.circles:
        out.append(f"CIRCLE Normal {x1} {y1} {x2} {y2}")
    for ar in sym.arcs:
        out.append("ARC Normal " + " ".join(str(v) for v in ar[:8]))
    out.append("WINDOW 0 0 -16 Left 2")
    out.append("WINDOW 3 0 16 Left 2")
    for i, (x, y, nm) in enumerate(sym.pins, 1):
        out.append(f"PIN {x} {y} NONE 0")
        out.append(f"PINATTR PinName {nm}")
        out.append(f"PINATTR SpiceOrder {i}")
    return "\n".join(out) + "\n"


def import_text(content: str, fmt: str) -> dict:
    """Parse uploaded library content -> {name: AsySymbol}.
    fmt: 'kicad' (.kicad_sym, many) or 'xschem' (.sym, one)."""
    if fmt == "kicad":
        return parse_kicad_lib(content)
    sym = parse_xschem(content)
    return {"imported": sym} if sym.pins or sym.lines else {}
