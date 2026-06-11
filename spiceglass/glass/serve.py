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
    def __init__(self, path: str, subname: str | None,
                 plan_path: str | None = None):
        self.plan_path = os.path.abspath(plan_path) if plan_path else None
        self._last_payload: dict | None = None
        self.load_path(path, subname)

    def load_path(self, path: str, subname: str | None = None) -> None:
        self.path = os.path.abspath(path)
        self.design = parse_file(self.path)
        classify_design(self.design)
        self._register_top()
        self.subname = subname or self.design.root().name
        if self.subname not in self.design.subckts and self.design.order:
            self.subname = self.design.order[-1]

    def _register_top(self) -> None:
        """Testbench-style files keep devices outside any .subckt —
        expose them as a synthetic '(top)' sheet."""
        if self.design.top_devices and "(top)" not in self.design.subckts:
            from .db import Subckt
            top = Subckt(name="(top)", ports=[],
                         devices=self.design.top_devices)
            seen: dict[str, None] = {}
            for d in top.devices:
                if d.section:
                    seen.setdefault(d.section)
            top.sections = list(seen)
            self.design.subckts["(top)"] = top
            self.design.order.append("(top)")

    def load_text(self, filename: str, text: str) -> None:
        """Persist an uploaded netlist and switch to it (uploads get
        their own dir so sidecars/saved placements have a home)."""
        safe = os.path.basename(filename) or "uploaded.cir"
        updir = os.path.join(os.path.dirname(__file__), "..", "uploads")
        os.makedirs(updir, exist_ok=True)
        dest = os.path.join(updir, safe)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(text)
        self.load_path(dest)

    def build(self, overrides, wires=None):
        if self.plan_path:
            from .plan import parse_plan, realize_plan
            with open(self.plan_path, encoding="utf-8") as fh:
                text = fh.read()
            plan = parse_plan(text)
            self._plan_warnings = list(plan.warnings)
            # fresh netlist parse: realization mutates Device.section
            design = parse_file(self.path)
            classify_design(design)
            sub = design.subckts[plan.name or self.subname]
            sheet = realize_plan(sub, plan)
            wires = getattr(sheet, "plan_wires", None)
        else:
            sub = self.design.subckts[self.subname]
            sheet = place(sub, overrides)
        routing = route(sheet, pinned=wires)
        verdict = verify(routing)
        return sub, sheet, routing, verdict

    def plan_text(self) -> str:
        with open(self.plan_path, encoding="utf-8") as fh:
            return fh.read()

    def plan_mtime(self) -> float:
        try:
            return os.path.getmtime(self.plan_path)
        except OSError:
            return 0.0

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
        if self.plan_path:
            try:
                p = self._payload(overrides, wires)
                p["mode"] = "plan"
                p["plan_text"] = self.plan_text()
                p["plan_mtime"] = self.plan_mtime()
                p["plan_error"] = ""
                p["verify"]["warnings"] = (
                    getattr(self, "_plan_warnings", [])
                    + p["verify"]["warnings"])
                self._last_payload = p
                return p
            except (ValueError, KeyError) as exc:
                # invalid plan: keep showing the last good schematic
                base = self._last_payload or {"devices": [], "paths": {},
                                              "pre_segs": [], "dots": [],
                                              "pinned": [], "furniture": "",
                                              "subckt": self.subname,
                                              "ports": [], "subckts": [],
                                              "tiles": [], "file": "",
                                              "unit": UNIT, "grid_mm": 1,
                                              "width": 60, "height": 30,
                                              "verify": {"ok": False,
                                                         "errors": [],
                                                         "warnings": []},
                                              "sidecar": ""}
                return {**base, "mode": "plan",
                        "plan_text": self.plan_text(),
                        "plan_mtime": self.plan_mtime(),
                        "plan_error": str(exc)}
        p = self._payload(overrides, wires)
        p["mode"] = "auto"
        return p

    def _payload(self, overrides, wires=None) -> dict:
        from .render_svg import render_sections_svg
        from .route import tile_halfdims
        sub, sheet, routing, verdict = self.build(overrides, wires)
        devs = []
        for d in sub.devices:
            p = sheet.pos(d)
            hw, hh = tile_halfdims(d)
            devs.append({"name": d.name, "kind": d.kind, "x": p.x, "y": p.y,
                         "orient": p.orient, "symbol": symbol_svg(d),
                         "hw": hw, "hh": hh,
                         "ann": _annotation(d), "section": d.section,
                         "nets": dict(zip(d.roles, d.nets))})
        from .geom import GRID_MM
        return {"subckt": sub.name, "ports": sub.ports, "unit": UNIT,
                "grid_mm": GRID_MM,
                "file": os.path.basename(self.path),
                "subckts": list(self.design.order),
                "width": sheet.width, "height": sheet.height,
                "devices": devs,
                "tiles": [[m.name for m in t.devices()] for t in sheet.tiles],
                "paths": routing.paths,
                "pre_segs": [list(p) for p in sheet.preroutes],
                "dots": routing.dots,
                "pinned": routing.pinned_nets,
                "sections": render_sections_svg(sheet),
                "furniture": render_furniture_svg(routing),
                "verify": {"ok": verdict.ok, "errors": verdict.errors,
                           "warnings": (verdict.warnings + routing.warnings
                                        + self.design.warnings)},
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
        if self.path.startswith("/api/stat"):
            agent = getattr(self.state, "agent", None)
            self._json({"mode": "plan" if self.state.plan_path else "auto",
                        "plan_mtime": self.state.plan_mtime()
                        if self.state.plan_path else 0,
                        "agent": {"running": agent.running,
                                  "iter": agent.iter,
                                  "max": agent.max_iters,
                                  "log": agent.log[-40:]}
                        if agent else None})
            return
        self._json({"error": "not found"}, 404)

    def _page(self, name: str):
        page = os.path.join(os.path.dirname(__file__), "..", "viewer", name)
        with open(page, "rb") as fh:
            self._send(fh.read(), "text/html; charset=utf-8")

    def do_POST(self):
        try:
            self._post()
        except Exception as exc:           # never drop the connection
            try:
                self._json({"error": f"{type(exc).__name__}: {exc}"}, 500)
            except Exception:
                pass

    def _post(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n) or b"{}"
        try:
            body = json.loads(raw.decode("utf-8"))
        except UnicodeDecodeError:
            body = json.loads(raw.decode("latin-1"))
        if self.path == "/api/route":
            p = self.state.payload(body.get("positions"),
                                   body.get("wires"))
            self._json({"paths": p["paths"], "pre_segs": p["pre_segs"],
                        "dots": p["dots"], "pinned": p["pinned"],
                        "sections": p.get("sections", ""),
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
        if self.path == "/api/open":
            try:
                self.state.load_text(body.get("name", "uploaded.cir"),
                                     body.get("content", ""))
            except Exception as exc:           # surface parse crashes
                self._json({"error": f"could not load: {exc}"}, 400)
                return
            if not self.state.design.order:
                self._json({"error": "no devices or subcircuits found"}, 400)
                return
            sc = self._sidecar()
            self._json(self.state.payload(sc.get("human"), sc.get("wires")))
            return
        if self.path == "/api/subckt":
            name = body.get("name")
            if name not in self.state.design.subckts:
                self._json({"error": f"no such subckt '{name}'"}, 400)
                return
            self.state.subname = name
            sc = self._sidecar()
            self._json(self.state.payload(sc.get("human"), sc.get("wires")))
            return
        if self.path == "/api/plan" and self.state.plan_path:
            with open(self.state.plan_path, "w", encoding="utf-8") as fh:
                fh.write(body.get("text", ""))
            self._json(self.state.payload(None))
            return
        if self.path == "/api/agent":
            st = self.state
            action = body.get("action")
            agent = getattr(st, "agent", None)
            if action == "start":
                if not st.plan_path:
                    self._json({"error": "agent needs plan mode "
                                "(glass edit file.plan)"}, 400)
                    return
                if agent is not None and agent.running:
                    self._json({"error": "agent already running"}, 400)
                    return
                from .agent import AgentRun
                st.agent = AgentRun(
                    st, body.get("goal", ""),
                    body.get("model") or "gpt-4o",
                    body.get("base_url") or "https://api.openai.com/v1",
                    body.get("api_key") or "",
                    int(body.get("max_iters") or 6))
                st.agent.start()
                self._json({"ok": True})
                return
            if action == "stop" and agent is not None:
                agent.stop_flag = True
                self._json({"ok": True})
                return
            self._json({"error": "unknown agent action"}, 400)
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


def serve(path: str, subname: str | None, port: int,
          plan_path: str | None = None) -> None:
    Handler.state = EditorState(path, subname, plan_path)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    mode = f"PLAN MODE: {os.path.basename(plan_path)}" if plan_path else \
        f"{Handler.state.subname} from {os.path.basename(path)}"
    print(f"SpiceGlass editor: http://127.0.0.1:{port}/  ({mode})")
    if plan_path:
        print("Live: edit the .plan in any editor and save — the "
              "schematic re-realizes automatically.")
    httpd.serve_forever()
