"""Interactive schematic editor — `python -m glass edit design.cir`.

Thin-client architecture: the browser only moves symbols (grid-snapped);
every drop POSTs positions back and the SERVER re-runs routing and the
round-trip verifier, returning fresh wires plus a live VERIFIED badge.
Saving writes a sidecar JSON with BOTH the algorithmic and the human
placement — the diff between them is the training signal for adapting
the placer.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .classify import classify_design
from .geom import UNIT
from .parser import parse_file
from .place import place
from .render_svg import (_annotation, render_furniture_svg, render_wires_svg,
                         symbol_svg)
from .route import route
from .verify import verify


def sidecar_path(netlist_path: str, subname: str) -> str:
    base = os.path.splitext(netlist_path)[0]
    return f"{base}.{subname}.place.json"


class EditorState:
    def __init__(self, path: str, subname: str | None):
        self.path = os.path.abspath(path)
        self.design = parse_file(self.path)
        classify_design(self.design)
        self.subname = subname or self.design.root().name

    def build(self, overrides, wires=None):
        sub = self.design.subckts[self.subname]
        sheet = place(sub, overrides)
        routing = route(sheet, pinned=wires)
        verdict = verify(routing)
        return sub, sheet, routing, verdict

    def positions(self, overrides=None) -> dict:
        sub, sheet, _, _ = self.build(overrides)
        return {d.name: {"x": sheet.pos(d).x, "y": sheet.pos(d).y,
                         "orient": sheet.pos(d).orient}
                for d in sub.devices}

    def algo_payload(self, overrides) -> dict:
        """Everything the algorithm-visualization page needs: obstacles,
        OVG corridors, per-net raw/A*-visited/final data, and the score."""
        from .score import score
        sub = self.design.subckts[self.subname]
        sheet = place(sub, overrides)
        routing = route(sheet, debug=True)
        verdict = verify(routing)
        sc = score(sheet, routing)
        devs = []
        for d in sub.devices:
            p = sheet.pos(d)
            devs.append({"name": d.name, "x": p.x, "y": p.y,
                         "orient": p.orient, "symbol": symbol_svg(d)})
        finals = {}
        for s in routing.segments:
            finals.setdefault(s.net, []).append([s.x1, s.y1, s.x2, s.y2])
        return {"subckt": sub.name, "unit": UNIT,
                "width": sheet.width, "height": sheet.height,
                "devices": devs,
                "furniture": render_furniture_svg(routing),
                "debug": routing.debug,
                "finals": finals,
                "dots": routing.dots,
                "verify": {"ok": verdict.ok, "errors": verdict.errors},
                "score": {"wirelength": sc.wirelength, "bends": sc.bends,
                          "crossings": sc.crossings,
                          "through": sc.through},
                "warnings": routing.warnings}

    def payload(self, overrides, wires=None) -> dict:
        sub, sheet, routing, verdict = self.build(overrides, wires)
        devs = []
        for d in sub.devices:
            p = sheet.pos(d)
            devs.append({"name": d.name, "kind": d.kind, "x": p.x, "y": p.y,
                         "orient": p.orient, "symbol": symbol_svg(d),
                         "ann": _annotation(d), "section": d.section,
                         "nets": dict(zip(d.roles, d.nets))})
        from .geom import GRID_MM
        return {"subckt": sub.name, "ports": sub.ports, "unit": UNIT,
                "grid_mm": GRID_MM,
                "width": sheet.width, "height": sheet.height,
                "devices": devs,
                "tiles": [[m.name for m in t.devices()] for t in sheet.tiles],
                "paths": routing.paths,
                "pre_segs": [list(p) for p in sheet.preroutes],
                "dots": routing.dots,
                "pinned": routing.pinned_nets,
                "furniture": render_furniture_svg(routing),
                "verify": {"ok": verdict.ok, "errors": verdict.errors,
                           "warnings": verdict.warnings + routing.warnings},
                "sidecar": sidecar_path(self.path, self.subname)}


class Handler(BaseHTTPRequestHandler):
    state: EditorState = None     # set by serve()

    def log_message(self, fmt, *args):       # quiet
        pass

    def _send(self, body: bytes, ctype: str, code: int = 200) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code: int = 200) -> None:
        self._send(json.dumps(obj).encode("utf-8"),
                   "application/json; charset=utf-8", code)

    def _sidecar(self) -> dict:
        sc = sidecar_path(self.state.path, self.state.subname)
        if os.path.exists(sc):
            with open(sc, encoding="utf-8") as fh:
                return json.load(fh)
        return {}

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._page("editor.html")
        if self.path.startswith("/algo"):
            return self._page("algo.html")
        if self.path.startswith("/symbols"):
            return self._page("symbols.html")
        if self.path.startswith("/api/sheet"):
            sc = {} if "reset" in self.path else self._sidecar()
            self._json(self.state.payload(sc.get("human"), sc.get("wires")))
            return
        if self.path.startswith("/api/algo"):
            sc = self._sidecar()
            self._json(self.state.algo_payload(sc.get("human")))
            return
        if self.path.startswith("/api/symbols"):
            self._json(_symbol_payload())
            return
        self._json({"error": "not found"}, 404)

    def _page(self, name: str):
        page = os.path.join(os.path.dirname(__file__), "..", "viewer", name)
        with open(page, "rb") as fh:
            self._send(fh.read(), "text/html; charset=utf-8")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n) or b"{}")
        if self.path == "/api/route":
            p = self.state.payload(body.get("positions"),
                                   body.get("wires"))
            self._json({"paths": p["paths"], "pre_segs": p["pre_segs"],
                        "dots": p["dots"], "pinned": p["pinned"],
                        "furniture": p["furniture"], "verify": p["verify"],
                        "width": p["width"], "height": p["height"]})
            return
        if self.path == "/api/save":
            sc = sidecar_path(self.state.path, self.state.subname)
            data = {"netlist": os.path.basename(self.state.path),
                    "subckt": self.state.subname,
                    "unit_note": "positions/wires in grid units",
                    "algo": self.state.positions(None),
                    "human": body.get("positions", {}),
                    "wires": body.get("wires", {})}
            with open(sc, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=1)
            self._json({"saved": sc})
            return
        if self.path == "/api/symbol":
            from .symbols import save
            path = save(body["kind"], body.get("elems"))
            self._json({"saved": path})
            return
        self._json({"error": "not found"}, 404)


_KIND_ROLES = {
    "nmos": ["d", "g", "s", "b"], "pmos": ["d", "g", "s", "b"],
    "res": ["p", "n", "b"], "cap": ["p", "n", "b"], "dio": ["p", "n"],
    "vsrc": ["p", "n"], "isrc": ["p", "n"], "bsrc": ["p", "n"],
    "npn": ["c", "b", "e", "s"], "pnp": ["c", "b", "e"],
}


def _symbol_payload() -> dict:
    from .db import Device
    from .geom import pin_offsets
    from .render_svg import builtin_symbol_svg
    from .symbols import lib
    custom = lib()
    kinds = {}
    for kind, roles in _KIND_ROLES.items():
        dev = Device(name="_", kind=kind, model="", nets=[""] * len(roles),
                     roles=list(roles))
        offs = pin_offsets(dev)
        kinds[kind] = {
            "pins": [[r, offs[r][0] * UNIT, offs[r][1] * UNIT]
                     for r in roles],
            "builtin": builtin_symbol_svg(dev),
            "custom": custom.get(kind),
        }
    return {"unit": UNIT, "kinds": kinds}


def serve(path: str, subname: str | None, port: int) -> None:
    Handler.state = EditorState(path, subname)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"SpiceGlass editor: http://127.0.0.1:{port}/  "
          f"({Handler.state.subname} from {os.path.basename(path)})")
    print("Ctrl+C to stop. Save writes:",
          sidecar_path(Handler.state.path, Handler.state.subname))
    httpd.serve_forever()
