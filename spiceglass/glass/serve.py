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

    def build(self, overrides):
        sub = self.design.subckts[self.subname]
        sheet = place(sub, overrides)
        routing = route(sheet)
        verdict = verify(routing)
        return sub, sheet, routing, verdict

    def positions(self, overrides=None) -> dict:
        sub, sheet, _, _ = self.build(overrides)
        return {d.name: {"x": sheet.pos(d).x, "y": sheet.pos(d).y,
                         "orient": sheet.pos(d).orient}
                for d in sub.devices}

    def payload(self, overrides) -> dict:
        sub, sheet, routing, verdict = self.build(overrides)
        devs = []
        for d in sub.devices:
            p = sheet.pos(d)
            devs.append({"name": d.name, "kind": d.kind, "x": p.x, "y": p.y,
                         "orient": p.orient, "symbol": symbol_svg(d),
                         "ann": _annotation(d), "section": d.section,
                         "nets": dict(zip(d.roles, d.nets))})
        return {"subckt": sub.name, "ports": sub.ports, "unit": UNIT,
                "width": sheet.width, "height": sheet.height,
                "devices": devs,
                "tiles": [[m.name for m in t.devices()] for t in sheet.tiles],
                "wires": render_wires_svg(routing),
                "furniture": render_furniture_svg(routing),
                "verify": {"ok": verdict.ok, "errors": verdict.errors,
                           "warnings": verdict.warnings},
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

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            page = os.path.join(os.path.dirname(__file__), "..", "viewer",
                                "editor.html")
            with open(page, "rb") as fh:
                self._send(fh.read(), "text/html; charset=utf-8")
            return
        if self.path.startswith("/api/sheet"):
            overrides = None
            if "reset" not in self.path:
                sc = sidecar_path(self.state.path, self.state.subname)
                if os.path.exists(sc):
                    with open(sc, encoding="utf-8") as fh:
                        overrides = json.load(fh).get("human")
            self._json(self.state.payload(overrides))
            return
        self._json({"error": "not found"}, 404)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n) or b"{}")
        if self.path == "/api/route":
            p = self.state.payload(body.get("positions"))
            self._json({"wires": p["wires"], "furniture": p["furniture"],
                        "verify": p["verify"], "width": p["width"],
                        "height": p["height"]})
            return
        if self.path == "/api/save":
            human = body.get("positions", {})
            sc = sidecar_path(self.state.path, self.state.subname)
            data = {"netlist": os.path.basename(self.state.path),
                    "subckt": self.state.subname,
                    "unit_note": "positions in grid units",
                    "algo": self.state.positions(None),
                    "human": human}
            with open(sc, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=1)
            self._json({"saved": sc})
            return
        self._json({"error": "not found"}, 404)


def serve(path: str, subname: str | None, port: int) -> None:
    Handler.state = EditorState(path, subname)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"SpiceGlass editor: http://127.0.0.1:{port}/  "
          f"({Handler.state.subname} from {os.path.basename(path)})")
    print("Ctrl+C to stop. Save writes:",
          sidecar_path(Handler.state.path, Handler.state.subname))
    httpd.serve_forever()
