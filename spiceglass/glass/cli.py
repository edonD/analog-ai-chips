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


def _render_one(design, name: str, out_svg: str, png: bool,
                physical: bool = False) -> bool:
    sub = design.subckts[name]
    overrides = wires = None
    sc = f"{os.path.splitext(design.path)[0]}.{name}.place.json"
    if os.path.exists(sc):
        import json
        with open(sc, encoding="utf-8") as fh:
            data = json.load(fh)
        overrides = data.get("human")
        wires = data.get("wires")
        print(f"          applying human placement: {os.path.basename(sc)}")
    sheet = place(sub, overrides)
    routing = route(sheet, pinned=wires)
    verdict = verify(routing)
    meta = {"path": os.path.basename(design.path),
            "date": _dt.date.today().isoformat(),
            "physical": physical}
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
    # size from the viewBox (width attr may be physical mm)
    import re
    head = open(svg_path, encoding="utf-8").read(500)
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', head)
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
    rp.add_argument("--grid", type=float, default=None, metavar="MM",
                    help="grid pitch in millimetres (default 1.0)")
    rp.add_argument("--physical", action="store_true",
                    help="emit SVG with true physical size (mm units)")

    jp = sp.add_parser("json", help="dump the circuit database as JSON")
    jp.add_argument("file")

    ep = sp.add_parser("edit", help="interactive editor in the browser")
    ep.add_argument("file")
    ep.add_argument("--subckt", default=None)
    ep.add_argument("--port", type=int, default=8137)
    ep.add_argument("--no-browser", action="store_true")

    scp = sp.add_parser("score", help="routing quality metrics "
                                      "(algo vs saved human placement)")
    scp.add_argument("file")
    scp.add_argument("--subckt", default=None)

    args = ap.parse_args(argv)

    if args.cmd == "edit":
        from .serve import serve
        if not args.no_browser:
            import threading
            import webbrowser
            threading.Timer(
                0.8, lambda: webbrowser.open(
                    f"http://127.0.0.1:{args.port}/")).start()
        serve(args.file, args.subckt, args.port)
        return 0

    if args.cmd == "score":
        import json
        from .score import score
        design = parse_file(args.file)
        classify_design(design)
        name = args.subckt or design.root().name
        sub = design.subckts[name]

        def measure(overrides):
            sheet = place(sub, overrides)
            routing = route(sheet)
            return score(sheet, routing), verify(routing).ok

        algo, ok_a = measure(None)
        print(f"algo : {algo.row()}  verified={ok_a}")
        sc = f"{os.path.splitext(args.file)[0]}.{name}.place.json"
        if os.path.exists(sc):
            with open(sc, encoding="utf-8") as fh:
                human, ok_h = measure(json.load(fh).get("human"))
            print(f"human: {human.row()}  verified={ok_h}")
            print(f"delta: len{human.wirelength - algo.wirelength:+d}  "
                  f"bends{human.bends - algo.bends:+d}  "
                  f"crossings{human.crossings - algo.crossings:+d}  "
                  f"through{human.through - algo.through:+d}")
        return 0
    design = parse_file(args.file)
    classify_design(design)
    for w in design.warnings:
        print(f"   parse   {w}")

    if args.cmd == "json":
        print(design.to_json())
        return 0

    if getattr(args, "grid", None):
        from .geom import set_grid_mm
        set_grid_mm(args.grid)

    base = os.path.splitext(args.file)[0]
    ok = True
    if args.all:
        for name in design.order:
            ok &= _render_one(design, name, f"{base}.{name}.svg", args.png,
                              args.physical)
    else:
        name = args.subckt or design.root().name
        if name not in design.subckts:
            print(f"no such subckt '{name}'; have: {', '.join(design.order)}")
            return 2
        out = args.out or f"{base}.{name}.svg"
        ok = _render_one(design, name, out, args.png, args.physical)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
