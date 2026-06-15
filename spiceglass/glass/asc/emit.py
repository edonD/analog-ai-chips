"""LTspice .asc export (experimental).

Writes the realized schematic as an LTspice schematic plus a local
symbol library (.asy files in an `sg_sym/` folder next to the .asc —
LTspice resolves symbols from the sheet's directory). Our symbols are
exported with pin positions that exactly match glass.geom under the
scale 1 grid unit (1 mm) = 8 LTspice units, so wires land on pins.

Coordinates remain a DERIVED artifact: the plan is the language, the
realizer makes the numbers, this module just changes their costume.
"""
from __future__ import annotations

import os

from ..engine.db import Subckt
from ..geom import pin_offsets
from ..engine.place import Sheet
from ..engine.route import Routing

S = 8          # LTspice units per grid unit (1 mm)

# our orientation group -> LTspice names. LTspice's R90 is the OPPOSITE
# rotation sense from ours (measured empirically, see probe_rot.py),
# so the rotations swap; the mirror compositions line up directly.
_ORIENT = {"R0": "R0", "R90": "R270", "R180": "R180", "R270": "R90",
           "MX": "M0", "MY": "M180", "MX90": "M90", "MY90": "M270"}

# symbol artwork in LTspice units, drawn around the origin so that the
# pins land at pin_offsets * S. (lines only; good enough to read)
_ART = {
    "nmos": [(0, -32, 0, -13), (0, -13, -11, -13), (0, 32, 0, 13),
             (0, 13, -11, 13), (-11, -14, -11, 14), (-17, -10, -17, 10),
             (-24, 0, -17, 0), (-11, 0, 24, 0), (-11, 0, -4, -3),
             (-11, 0, -4, 3)],
    "pmos": [(0, -32, 0, -13), (0, -13, -11, -13), (0, 32, 0, 13),
             (0, 13, -11, 13), (-11, -14, -11, 14), (-17, -10, -17, 10),
             (-24, 0, -19, 0), (-11, 0, 24, 0), (4, -3, 11, 0),
             (4, 3, 11, 0)],
    "res": [(0, -32, 0, -17), (0, -17, 6, -14), (6, -14, -6, -8),
            (-6, -8, 6, -2), (6, -2, -6, 4), (-6, 4, 6, 10),
            (6, 10, 0, 14), (0, 14, 0, 32)],
    "cap": [(0, -32, 0, -4), (-11, -4, 11, -4), (-11, 4, 11, 4),
            (0, 4, 0, 32)],
    "dio": [(0, -32, 0, -7), (-8, -7, 8, -7), (-8, -7, 0, 7),
            (8, -7, 0, 7), (-8, 7, 8, 7), (0, 7, 0, 32)],
    "vsrc": [(0, -32, 0, -12), (0, 12, 0, 32), (-10, 0, 10, 0),
             (0, -10, 0, 10)],
    "isrc": [(0, -32, 0, -12), (0, 12, 0, 32), (0, -8, 0, 8),
             (0, 8, -4, 2), (0, 8, 4, 2)],
    "bsrc": [(0, -32, 0, -12), (0, 12, 0, 32), (-10, 0, 0, -10),
             (0, -10, 10, 0), (10, 0, 0, 10), (0, 10, -10, 0)],
}
_ART["ind"] = _ART["res"]
_ART["pnp"] = _ART["pmos"]
_ART["npn"] = _ART["nmos"]


def _custom_art(kind: str) -> list | None:
    """Symbol-designer artwork (symbols.json) converted to LTspice
    units — whatever you draw in /symbols ships into the .asy too.
    Designer coords are px at 10 px/mm; LTspice gets S units/mm."""
    from ..engine.symbols import lib
    elems = lib().get(kind)
    if not elems:
        return None
    k = S / 10.0
    out = []
    for e in elems:
        if e.get("t") == "line":
            out.append(("LINE", round(e["x1"] * k), round(e["y1"] * k),
                        round(e["x2"] * k), round(e["y2"] * k)))
        elif e.get("t") == "circle":
            r = e["r"] * k
            out.append(("CIRCLE", round(e["cx"] * k - r),
                        round(e["cy"] * k - r),
                        round(e["cx"] * k + r), round(e["cy"] * k + r)))
    return out or None


def _asy_for(kind: str, roles: list[str]) -> str:
    from ..engine.db import Device
    dev = Device(name="_", kind=kind, model="", nets=[""] * len(roles),
                 roles=list(roles))
    offs = pin_offsets(dev)
    lines = ["Version 4", "SymbolType CELL"]
    custom = _custom_art(kind)
    if custom:
        for item in custom:
            if item[0] == "LINE":
                lines.append(f"LINE Normal {item[1]} {item[2]} "
                             f"{item[3]} {item[4]}")
            else:
                lines.append(f"CIRCLE Normal {item[1]} {item[2]} "
                             f"{item[3]} {item[4]}")
    else:
        for (x1, y1, x2, y2) in _ART.get(kind, [(-16, -16, 16, 16)]):
            lines.append(f"LINE Normal {x1} {y1} {x2} {y2}")
    lines.append("WINDOW 0 28 -32 Left 2")
    for i, r in enumerate(roles, 1):
        dx, dy = offs[r]
        lines.append(f"PIN {dx * S} {dy * S} NONE 8")
        lines.append(f"PINATTR PinName {r}")
        lines.append(f"PINATTR SpiceOrder {i}")
    return "\n".join(lines) + "\n"


def export_asc(sheet: Sheet, routing: Routing, out_path: str) -> str:
    """Write .asc + local sg_sym/*.asy library. Returns the .asc path."""
    sub: Subckt = sheet.sub
    outdir = os.path.dirname(os.path.abspath(out_path)) or "."
    symdir = os.path.join(outdir, "sg_sym")
    os.makedirs(symdir, exist_ok=True)

    lines = ["Version 4",
             f"SHEET 1 {sheet.width * S} {sheet.height * S}"]

    # wires (preroutes are already inside routing.segments)
    for s in routing.segments:
        lines.append(f"WIRE {int(s.x1) * S} {int(s.y1) * S} "
                     f"{int(s.x2) * S} {int(s.y2) * S}")

    # rails / labels / ports as flags (gnd-class becomes LTspice node 0)
    for st in routing.stubs:
        name = "0" if st.kind == "gnd" else st.net
        lines.append(f"FLAG {int(st.px) * S} {int(st.py) * S} {name}")

    written: set[str] = set()
    for d in sub.devices:
        p = sheet.pos(d)
        kind = d.kind if d.kind in _ART else None
        if kind is None:           # subckt boxes etc: flag pins, skip body
            for role, net in zip(d.roles, d.nets):
                from ..geom import pin_pos
                x, y = pin_pos(d, role, p.x, p.y, p.orient)
                lines.append(f"FLAG {x * S} {y * S} "
                             f"{'0' if net in sheet.rails and sheet.rails[net] == 'gnd' else net}")
            continue
        sym = f"sg_{kind}{len(d.roles)}"
        if sym not in written:
            with open(os.path.join(symdir, sym + ".asy"), "w",
                      encoding="utf-8") as fh:
                fh.write(_asy_for(kind, d.roles))
            written.add(sym)
        rot = _ORIENT.get(p.orient, "R0")
        lines.append(f"SYMBOL sg_sym\\\\{sym} {p.x * S} {p.y * S} {rot}")
        lines.append(f"SYMATTR InstName {d.name}")
        val = d.model or d.params.get("value", "")
        wl = " ".join(f"{k}={v}" for k, v in d.params.items()
                      if k in ("w", "l", "m"))
        if val or wl:
            lines.append(f"SYMATTR Value {(val + ' ' + wl).strip()}")
    lines.append(f"TEXT {8 * S} {(sheet.height + 2) * S} Left 2 "
                 f";{sub.name} — exported by SpiceGlass (grid 1mm = {S}u)")

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return out_path
