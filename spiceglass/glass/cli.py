"""SpiceGlass CLI.

  python -m glass render design.cir [-o out.svg] [--subckt NAME] [--all] [--png]
  python -m glass json   design.cir
"""
from __future__ import annotations

import argparse
import datetime as _dt
import os
import subprocess
import sys

from .classify import classify_design
from .parser import parse_file
from .place import place
from .render_svg import render_sheet
from .route import route
from .verify import verify

_EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def _render_one(design, name: str, out_svg: str, png: bool) -> bool:
    sub = design.subckts[name]
    sheet = place(sub)
    routing = route(sheet)
    verdict = verify(routing)
    meta = {"path": os.path.basename(design.path),
            "date": _dt.date.today().isoformat()}
    svg = render_sheet(sheet, routing, verdict, meta)
    with open(out_svg, "w", encoding="utf-8") as fh:
        fh.write(svg)
    status = "VERIFIED" if verdict.ok else "MISMATCH"
    print(f"[{status}] {name}: {len(sub.devices)} devices, "
          f"{verdict.n_nets} nets -> {out_svg}")
    for e in verdict.errors:
        print(f"   ERROR   {e}")
    for w in verdict.warnings:
        print(f"   warn    {w}")
    if png:
        _to_png(out_svg)
    return verdict.ok


def _to_png(svg_path: str) -> None:
    edge = next((p for p in _EDGE_CANDIDATES if os.path.exists(p)), None)
    if not edge:
        print("   warn    Edge not found; skipping PNG")
        return
    png_path = os.path.splitext(svg_path)[0] + ".png"
    url = "file:///" + os.path.abspath(svg_path).replace("\\", "/")
    # size from the svg header
    import re
    head = open(svg_path, encoding="utf-8").read(400)
    m = re.search(r'width="(\d+)"\s+height="(\d+)"', head)
    w, h = (m.group(1), m.group(2)) if m else ("1600", "1000")
    subprocess.run([edge, "--headless=new", "--disable-gpu",
                    f"--screenshot={os.path.abspath(png_path)}",
                    f"--window-size={w},{h}", url],
                   capture_output=True, timeout=60)
    print(f"          png -> {png_path}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="glass")
    sp = ap.add_subparsers(dest="cmd", required=True)

    rp = sp.add_parser("render", help="netlist -> schematic SVG")
    rp.add_argument("file")
    rp.add_argument("-o", "--out", default=None)
    rp.add_argument("--subckt", default=None)
    rp.add_argument("--all", action="store_true",
                    help="render every subckt in the file")
    rp.add_argument("--png", action="store_true",
                    help="also screenshot to PNG via headless Edge")

    jp = sp.add_parser("json", help="dump the circuit database as JSON")
    jp.add_argument("file")

    args = ap.parse_args(argv)
    design = parse_file(args.file)
    classify_design(design)
    for w in design.warnings:
        print(f"   parse   {w}")

    if args.cmd == "json":
        print(design.to_json())
        return 0

    base = os.path.splitext(args.file)[0]
    ok = True
    if args.all:
        for name in design.order:
            ok &= _render_one(design, name, f"{base}.{name}.svg", args.png)
    else:
        name = args.subckt or design.root().name
        if name not in design.subckts:
            print(f"no such subckt '{name}'; have: {', '.join(design.order)}")
            return 2
        out = args.out or f"{base}.{name}.svg"
        ok = _render_one(design, name, out, args.png)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
