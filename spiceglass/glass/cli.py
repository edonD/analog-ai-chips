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

from .engine.classify import classify_design
from .engine.parser import parse_file
from .engine.place import place
from .engine.render_svg import render_sheet
from .engine.route import route
from .engine.verify import verify

_EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def _render_one(design, name: str, out_svg: str, png: bool,
                physical: bool = False, sheet=None, asc: str = None) -> bool:
    sub = design.subckts[name]
    wires = None
    if sheet is None:
        overrides = None
        sc = f"{os.path.splitext(design.path)[0]}.{name}.place.json"
        if os.path.exists(sc):
            import json
            with open(sc, encoding="utf-8") as fh:
                data = json.load(fh)
            overrides = data.get("human")
            wires = data.get("wires")
            print("          applying human placement: "
                  f"{os.path.basename(sc)}")
        sheet = place(sub, overrides)
    else:
        wires = getattr(sheet, "plan_wires", None)   # plan wire paths
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
    if asc:
        from .asc.emit import export_asc
        print(f"          asc -> {export_asc(sheet, routing, asc)}")
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
    rp.add_argument("file", nargs="?", default=None)
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
    rp.add_argument("--plan", default=None, metavar="PLAN",
                    help="realize this .plan file instead of automatic "
                         "placement (netlist from the plan header)")
    rp.add_argument("--asc", default=None, metavar="ASC",
                    help="also export an LTspice schematic (.asc + local "
                         "sg_sym/ symbol library) — experimental")

    jp = sp.add_parser("json", help="dump the circuit database as JSON")
    jp.add_argument("file")

    ep = sp.add_parser("edit", help="the web app: .asc editor (a .cir/.plan "
                                    "is converted to .asc on open)")
    ep.add_argument("file", nargs="?", default=None,
                    help="optional; omit to start with the in-app file picker")
    ep.add_argument("--port", type=int, default=8137)
    ep.add_argument("--no-browser", action="store_true")

    bp = sp.add_parser("op", help="operating-point back-annotation: node "
                       "voltages + MOSFET regions (needs a simulatable deck)")
    bp.add_argument("file")

    scp = sp.add_parser("score", help="routing quality metrics "
                                      "(algo vs saved human placement)")
    scp.add_argument("file")
    scp.add_argument("--subckt", default=None)

    op = sp.add_parser("optimize", help="show the placement optimizer: seed "
                       "vs crossing-minimised layout + full decision trace")
    op.add_argument("file")
    op.add_argument("--subckt", default=None)
    op.add_argument("-o", "--out", default=None, metavar="BASE")
    op.add_argument("--png", action="store_true")

    pp = sp.add_parser("plan", help="emit the automatic interpretation "
                                    "as an editable .plan file")
    pp.add_argument("file")
    pp.add_argument("--subckt", default=None)
    pp.add_argument("-o", "--out", default=None)

    dpp = sp.add_parser("diff-plan", help="diff a hand-edited golden plan "
                        "against the automatic interpretation")
    dpp.add_argument("golden")
    dpp.add_argument("--file", default=None,
                     help="netlist (default: from the plan header)")

    args = ap.parse_args(argv)

    if args.cmd == "plan":
        from .engine.plan import plan_for
        design = parse_file(args.file)
        classify_design(design)
        name = args.subckt or design.root().name
        text = plan_for(design, name)
        out = args.out or f"{os.path.splitext(args.file)[0]}.{name}.plan"
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"plan -> {out}")
        return 0

    if args.cmd == "render" and args.file \
            and args.file.lower().endswith(".asc"):
        from .asc.parse import asc_to_svg, parse_asc
        sheet = parse_asc(args.file)
        svg = asc_to_svg(sheet, os.path.dirname(os.path.abspath(args.file)))
        out = args.out or os.path.splitext(args.file)[0] + ".svg"
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(svg)
        print(f"[ASC] {os.path.basename(args.file)}: "
              f"{len(sheet.insts)} symbols, {len(sheet.wires)} wires "
              f"-> {out}")
        for w in sheet.warnings:
            print(f"   asc     {w}")
        if args.png:
            _to_png(out)
        return 0

    if args.cmd == "render" and getattr(args, "plan", None):
        from .engine.plan import parse_plan, realize_plan
        with open(args.plan, encoding="utf-8") as fh:
            plan = parse_plan(fh.read())
        for w in plan.warnings:
            print(f"   plan    {w}")
        candidates = [args.file,
                      os.path.join(os.path.dirname(os.path.abspath(args.plan)),
                                   plan.source),
                      plan.source]
        netpath = next((c for c in candidates if c and os.path.exists(c)),
                       None)
        if netpath is None:
            print(f"cannot find netlist '{plan.source}' — pass it explicitly:"
                  f" glass render <netlist> --plan {args.plan}")
            return 2
        design = parse_file(netpath)
        classify_design(design)
        if args.grid:
            from .geom import set_grid_mm
            set_grid_mm(args.grid)
        name = plan.name or design.root().name
        sheet = realize_plan(design.subckts[name], plan)
        out = args.out or os.path.splitext(args.plan)[0] + ".svg"
        ok = _render_one(design, name, out, args.png, args.physical,
                         sheet=sheet, asc=args.asc)
        return 0 if ok else 1

    if args.cmd == "op":
        from .engine.op import run_op_file
        r = run_op_file(args.file)
        if not r.ok:
            print(f"  op: {r.error}")
            return 1
        print(f"  {len(r.nodes)} nodes, {len(r.mos)} MOSFETs")
        for n, v in sorted(r.nodes.items()):
            print(f"    {n:20} {v:+.4f} V")
        if r.mos:
            print("  transistors (region | Vgs Vds Vdsat | Id):")
            for name, d in r.mos.items():
                print(f"    {name:8} {d['region']:6} "
                      f"Vgs={d['vgs']:+.3f} Vds={d['vds']:+.3f} "
                      f"Vdsat={d['vdsat']:+.3f}  Id={d['id']:.3e}")
        return 0

    if args.cmd == "edit":
        from .web.server import serve
        serve(args.file, args.port, open_browser=not args.no_browser)
        return 0

    if args.cmd == "diff-plan":
        from .engine.plan import diff_plans, parse_plan, plan_for
        with open(args.golden, encoding="utf-8") as fh:
            golden = parse_plan(fh.read())
        cands = [args.file,
                 os.path.join(os.path.dirname(os.path.abspath(args.golden)),
                              golden.source), golden.source]
        netpath = next((c for c in cands if c and os.path.exists(c)), None)
        if netpath is None:
            print(f"cannot find netlist '{golden.source}'")
            return 2
        design = parse_file(netpath)
        classify_design(design)
        name = golden.name or design.root().name
        auto = parse_plan(plan_for(design, name))
        report, n = diff_plans(auto, golden)
        print(report)
        print(f"\n{n} device(s) differ — each line above is a rule the "
              "interpreter should learn.")
        return 0

    if args.cmd == "score":
        import json
        from .engine.score import score
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
    if args.cmd == "optimize":
        from .engine.score import score
        design = parse_file(args.file)
        classify_design(design)
        name = args.subckt or design.root().name
        if name not in design.subckts:
            print(f"no such subckt '{name}'; have: {', '.join(design.order)}")
            return 2
        sub = design.subckts[name]
        base = args.out or f"{os.path.splitext(args.file)[0]}.{name}"

        def run(opt, tr=None):
            sheet = place(sub, optimize=opt, trace=tr)
            routing = route(sheet)
            return sheet, routing, verify(routing), score(sheet, routing)

        seed_sheet, seed_r, seed_v, seed_sc = run(False)
        tr: list = []
        opt_sheet, opt_r, opt_v, opt_sc = run(True, tr)

        bar = "=" * 68
        print(bar)
        print(f"PLACEMENT OPTIMIZER — {name}  ({len(sub.devices)} devices)")
        print(bar)
        for line in tr:
            print(line)
        print("-" * 68)
        print("routed result (REAL score, after A* routing + verify):")
        print(f"  seed : {seed_sc.row()}  verified={seed_v.ok}")
        print(f"  opt  : {opt_sc.row()}  verified={opt_v.ok}")
        print(f"  delta: crossings {opt_sc.crossings - seed_sc.crossings:+d}  "
              f"bends {opt_sc.bends - seed_sc.bends:+d}  "
              f"len {opt_sc.wirelength - seed_sc.wirelength:+d} mm")
        meta = {"path": os.path.basename(design.path),
                "date": _dt.date.today().isoformat(), "physical": False}
        for tag, sh, r, v in (("seed", seed_sheet, seed_r, seed_v),
                              ("optimized", opt_sheet, opt_r, opt_v)):
            out = f"{base}.{tag}.svg"
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(render_sheet(sh, r, v, meta))
            print(f"  {tag:10} -> {out}")
            if args.png:
                _to_png(out)
        return 0 if opt_v.ok else 1

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
        ok = _render_one(design, name, out, args.png, args.physical,
                         asc=args.asc)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
