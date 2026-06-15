"""Built-in clean-room symbol library, on LTspice's functional pins.

LTspice's own .asy files cannot be redistributed (ADI EULA), so this is
ORIGINAL artwork anchored to LTspice's published pin coordinates — the
pins are interoperability facts (so wires land and netlists order
correctly), the drawing is ours. Pin coordinates were cross-checked
against open LTspice symbol mirrors and the project's 150-schematic
corpus. When real .asy files are available (an LTspice install, or a
sheet's local sg_sym/), those are used instead and this is the fallback.

Each builder returns an AsySymbol (symbol-local units, +x right, +y down,
16 units = one grid square). Pins are (x, y, name) in SpiceOrder.
"""
from __future__ import annotations


def _S():
    from .parse import AsySymbol
    return AsySymbol()


# ----------------------------------------------------------- 2-terminal
def _two(kind, a, b):
    s = _S()
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) // 2, (y0 + y1) // 2
    s.pins = [(x0, y0, "1"), (x1, y1, "2")]
    if kind == "res":
        s.lines += [(x0, y0, x0, my - 28), (x0, my + 28, x1, y1),
                    (x0, my - 28, x0 + 8, my - 22),
                    (x0 + 8, my - 22, x0 - 8, my - 11),
                    (x0 - 8, my - 11, x0 + 8, my),
                    (x0 + 8, my, x0 - 8, my + 11),
                    (x0 - 8, my + 11, x0 + 8, my + 22),
                    (x0 + 8, my + 22, x0, my + 28)]
    elif kind == "cap":
        s.lines += [(x0, y0, x0, my - 6), (x0, my + 6, x1, y1),
                    (x0 - 16, my - 6, x0 + 16, my - 6),
                    (x0 - 16, my + 6, x0 + 16, my + 6)]
    elif kind == "polcap":
        s.lines += [(x0, y0, x0, my - 6), (x0, my + 6, x1, y1),
                    (x0 - 16, my - 6, x0 + 16, my - 6),
                    (x0 - 11, my + 6, x0 + 11, my + 6),
                    (x0 + 8, my - 16, x0 + 16, my - 16),
                    (x0 + 12, my - 20, x0 + 12, my - 12)]    # + mark
    elif kind == "ind":
        s.lines += [(x0, y0, x0, my - 24), (x0, my + 24, x1, y1)]
        for k in range(3):
            yb = my - 24 + k * 16
            s.lines += [(x0, yb, x0 + 10, yb + 4),
                        (x0 + 10, yb + 4, x0 + 10, yb + 12),
                        (x0 + 10, yb + 12, x0, yb + 16)]
    elif kind in ("dio", "zener", "schottky", "led", "tvs"):
        s.lines += [(x0, y0, x0, my - 10), (x0, my + 10, x1, y1),
                    (x0 - 12, my - 10, x0 + 12, my - 10),
                    (x0 - 12, my - 10, x0, my + 10),
                    (x0 + 12, my - 10, x0, my + 10),
                    (x0 - 12, my + 10, x0 + 12, my + 10)]
        if kind == "zener":
            s.lines += [(x0 - 12, my + 10, x0 - 16, my + 14),
                        (x0 + 12, my + 10, x0 + 16, my + 6)]
        elif kind == "schottky":
            s.lines += [(x0 - 12, my + 10, x0 - 12, my + 16),
                        (x0 - 12, my + 16, x0 - 8, my + 16),
                        (x0 + 12, my + 10, x0 + 12, my + 4),
                        (x0 + 12, my + 4, x0 + 8, my + 4)]
        elif kind == "led":
            s.lines += [(x0 + 14, my - 14, x0 + 22, my - 22),
                        (x0 + 22, my - 22, x0 + 18, my - 21),
                        (x0 + 22, my - 22, x0 + 21, my - 18)]
    elif kind in ("vsrc", "isrc", "bv", "bi"):
        s.lines += [(x0, y0, x0, my - 24), (x0, my + 24, x1, y1)]
        if kind in ("bv", "bi"):
            r = 24                                # behavioral = diamond
            s.lines += [(x0, my - r, x0 + r, my), (x0 + r, my, x0, my + r),
                        (x0, my + r, x0 - r, my), (x0 - r, my, x0, my - r)]
        else:
            s.circles.append((x0 - 24, my - 24, x0 + 24, my + 24))
        if kind in ("vsrc", "bv"):
            s.lines += [(x0, my - 16, x0, my - 6),
                        (x0 - 5, my - 11, x0 + 5, my - 11),
                        (x0 - 5, my + 11, x0 + 5, my + 11)]
        else:                                     # current arrow
            s.lines += [(x0, my - 12, x0, my + 12),
                        (x0, my - 12, x0 - 5, my - 2),
                        (x0, my - 12, x0 + 5, my - 2)]
    return s


# ----------------------------------------------------------- transistors
def _bjt(pnp):
    s = _S()
    s.pins = [(64, 0, "C"), (0, 48, "B"), (64, 96, "E")]
    s.lines += [(0, 48, 24, 48), (24, 28, 24, 68),
                (64, 0, 64, 24), (64, 24, 24, 42),
                (64, 96, 64, 72), (64, 72, 24, 54)]
    s.lines += ([(34, 46, 46, 36), (34, 46, 44, 50)] if pnp
                else [(54, 68, 44, 56), (54, 68, 42, 66)])
    return s


def _mos(pmos, bulk):
    s = _S()
    s.pins = [(48, 0, "D"), (0, 80, "G"), (48, 96, "S")]
    s.lines += [(0, 80, 16, 80), (16, 60, 16, 100), (24, 58, 24, 102),
                (48, 0, 48, 64), (48, 64, 24, 64),
                (48, 96, 24, 96), (24, 96, 24, 84), (24, 84, 48, 84)]
    s.lines += [(24, 64, 24, 76), (24, 76, 48, 76)]       # source/drain stubs
    if bulk:
        s.pins.append((48, 48, "B"))
        s.lines += [(24, 80, 40, 80), (40, 80, 48, 80), (48, 48, 48, 80)]
        arrow = [(40, 80, 34, 76), (40, 80, 34, 84)] if not pmos \
            else [(28, 80, 34, 76), (28, 80, 34, 84)]
        s.lines += arrow
    if pmos:
        s.circles.append((6, 72, 22, 88))                 # gate bubble
    return s


def _jfet(pjf):
    s = _S()
    s.pins = [(48, 0, "D"), (0, 64, "G"), (48, 96, "S")]
    s.lines += [(0, 64, 24, 64), (24, 40, 24, 88),
                (48, 0, 48, 40), (48, 40, 24, 40),
                (48, 96, 48, 56), (48, 56, 24, 56)]
    s.lines += ([(8, 64, 18, 60), (8, 64, 18, 68)] if pjf      # gate arrow
                else [(18, 64, 8, 60), (18, 64, 8, 68)])
    return s


# ----------------------------------------------------------- sources/ctrl
def _ctrl_src(kind):
    """e=VCVS f=CCCS g=VCCS h=CCVS — diamond source, with control inputs
    on the left for the voltage-controlled (4-pin) variants."""
    s = _S()
    if kind == "g":                          # VCCS: +/- vertically flipped
        s.pins = [(0, 96, "1"), (0, 16, "2"), (-48, 32, "NC+"), (-48, 80, "NC-")]
        a, b, mid = (0, 96), (0, 16), 56
    elif kind == "e":                        # VCVS
        s.pins = [(0, 16, "1"), (0, 96, "2"), (-48, 32, "NC+"), (-48, 80, "NC-")]
        a, b, mid = (0, 16), (0, 96), 56
    elif kind == "f":                        # CCCS (2-pin)
        s.pins = [(0, 0, "1"), (0, 80, "2")]
        a, b, mid = (0, 0), (0, 80), 40
    else:                                    # h CCVS (2-pin)
        s.pins = [(0, 16, "1"), (0, 96, "2")]
        a, b, mid = (0, 16), (0, 96), 56
    r = 24
    s.lines += [(a[0], a[1], 0, mid - r), (0, mid + r, b[0], b[1]),
                (0, mid - r, r, mid), (r, mid, 0, mid + r),
                (0, mid + r, -r, mid), (-r, mid, 0, mid - r)]
    if kind in ("e", "h"):                   # voltage out: +/-
        s.lines += [(0, mid - 14, 0, mid - 4), (-5, mid - 9, 5, mid - 9),
                    (-5, mid + 9, 5, mid + 9)]
    else:                                    # current out: arrow
        s.lines += [(0, mid - 11, 0, mid + 11), (0, mid - 11, -4, mid - 1),
                    (0, mid - 11, 4, mid - 1)]
    if len(s.pins) == 4:                      # control input stubs + diamond
        for (px, py) in ((-48, 32), (-48, 80)):
            s.lines.append((px, py, px + 14, py))
    return s


def _switch():
    """sw: 4-pin voltage-controlled switch — terminals (0,16)/(0,96),
    control inputs (-48,32)/(-48,80)."""
    s = _S()
    s.pins = [(0, 16, "1"), (0, 96, "2"), (-48, 80, "NC+"), (-48, 32, "NC-")]
    s.lines += [(0, 16, 0, 40), (0, 96, 0, 72),
                (0, 40, 16, 68)]                          # open blade
    s.circles += [(-2, 38, 2, 42), (-2, 70, 2, 74)]       # contacts
    for (px, py) in ((-48, 80), (-48, 32)):
        s.lines.append((px, py, px + 14, py))             # control stubs
    return s


# ----------------------------------------------------------------- opamps
def _opamp():
    s = _S()
    s.pins = [(-32, 48, "In-"), (-32, 80, "In+"), (32, 64, "OUT")]
    s.lines += [(-32, 32, -32, 96), (-32, 32, 32, 64), (-32, 96, 32, 64),
                (-26, 48, -18, 48), (-22, 44, -22, 52),   # - on order-1 (inv)
                (-26, 80, -18, 80)]                        # + on order-2
    return s


def _opamp2():
    s = _S()
    s.pins = [(-32, 80, "In+"), (-32, 48, "In-"), (0, 32, "V+"),
              (0, 96, "V-"), (32, 64, "OUT")]
    s.lines += [(-32, 32, -32, 96), (-32, 32, 32, 64), (-32, 96, 32, 64),
                (-26, 80, -18, 80), (-22, 76, -22, 84),    # + on order-1
                (-26, 48, -18, 48),                        # -
                (0, 32, 0, 48), (0, 96, 0, 80)]            # power stubs
    return s


def _uopamp2():
    """UniversalOpamp2 — centred frame, negative-Y inputs."""
    s = _S()
    s.pins = [(-32, 16, "In+"), (-32, -16, "In-"), (0, -32, "V+"),
              (0, 32, "V-"), (32, 0, "OUT")]
    s.lines += [(-32, -32, -32, 32), (-32, -32, 32, 0), (-32, 32, 32, 0),
                (-26, 16, -18, 16), (-22, 12, -22, 20),    # + (order-1)
                (-26, -16, -18, -16),                      # -
                (0, -32, 0, -16), (0, 32, 0, 16)]
    return s


# ----------------------------------------------------------------- registry
def lookup(symname: str):
    n = symname.replace("/", "\\").split("\\")[-1].lower()
    if n in ("res", "res2"):
        return _two("res", (16, 16), (16, 96)) if n == "res" \
            else _two("res", (16, 0), (16, 64))
    if n == "cap":
        return _two("cap", (16, 0), (16, 64))
    if n == "polcap":
        return _two("polcap", (16, 0), (16, 64))
    if n in ("ind", "ind2"):
        return _two("ind", (16, 16), (16, 96))
    if n in ("diode", "schottky", "zener", "led", "tvs"):
        kind = {"diode": "dio"}.get(n, n)
        return _two(kind, (16, 0), (16, 64))
    if n in ("voltage", "battery", "cell"):
        return _two("vsrc", (0, 16), (0, 96))
    if n in ("current", "load"):
        return _two("isrc", (0, 0), (0, 80))
    if n in ("bv", "b"):
        return _two("bv", (0, 16), (0, 96))
    if n in ("bi", "bi2"):
        return _two("bi", (0, 0), (0, 80))
    if n in ("e", "e2"):
        return _ctrl_src("e")
    if n == "g":
        return _ctrl_src("g")
    if n == "f":
        return _ctrl_src("f")
    if n == "h":
        return _ctrl_src("h")
    if n in ("sw", "sw2", "csw"):
        return _switch()
    if n in ("npn", "npn2", "npn3"):
        return _bjt(pnp=False)
    if n in ("pnp", "pnp2"):
        return _bjt(pnp=True)
    if n == "nmos":
        return _mos(pmos=False, bulk=False)
    if n == "pmos":
        return _mos(pmos=True, bulk=False)
    if n in ("nmos4", "nmos4d"):
        return _mos(pmos=False, bulk=True)
    if n in ("pmos4", "pmos4d"):
        return _mos(pmos=True, bulk=True)
    if n in ("njf", "njf4"):
        return _jfet(pjf=False)
    if n in ("pjf", "pjf4"):
        return _jfet(pjf=True)
    if n in ("opamp", "uopamp"):
        return _opamp()
    if n in ("universalopamp2",):
        return _uopamp2()
    if n in ("opamp2", "lt1001", "lt1006", "lt1007", "lt1012", "lt1013",
             "lt1720") or n.startswith(("lt1", "lt2", "lt6", "ad8", "ada")):
        return _opamp2()
    return None
