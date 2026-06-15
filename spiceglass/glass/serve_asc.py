"""SpiceGlass unified editor server — the one web app.

`.asc` is the hub. A `.cir`/`.spice`/`.plan` is converted to `.asc`
(place → route → emit, next to the source) on open and then edited like
any other sheet. The browser owns parse/render/cull/sync; this server
only does what the browser cannot: read `.asy` artwork off disk, convert
netlists, list/open/upload files, persist saves, and host the symbol
designer.

See research/asc-web-renderer.md for the architecture, and the
consolidation note: going .asc-hub means there is no live netlist state,
so the old .cir-only views (live placement editor, router visualization)
retire — their engine lives on here as the converter and in the CLI.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .geom import UNIT
from .parse_asc import native_symbol, parse_asc, parse_asy, resolve_asy

REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
VIEWER = os.path.join(os.path.dirname(__file__), "..", "viewer")


def symbol_json(symname: str, asc_dir: str) -> dict | None:
    """Resolve a symbol name to drawable geometry (symbol-local units).

    Returns None when neither a .asy file nor a native glyph is known,
    so the client can draw a dashed placeholder box."""
    path = resolve_asy(symname, asc_dir)
    sym = parse_asy(path) if path else native_symbol(symname)
    if sym is None:
        return None
    return {
        "lines": [list(t) for t in sym.lines],
        "circles": [list(t) for t in sym.circles],
        "rects": [list(t) for t in sym.rects],
        "arcs": [list(t) for t in sym.arcs],
        "pins": [list(t) for t in sym.pins],
        "native": path is None,
    }


def _symbols_in(text: str) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        t = line.split()
        if t and t[0].upper() == "SYMBOL" and len(t) >= 2:
            name = t[1].replace("\\\\", "\\")
            if name not in seen:
                seen.add(name)
                names.append(name)
    return names


def convert_to_asc(path: str) -> str:
    """Netlist/plan → LTspice .asc (+ a local sg_sym/ library) written
    next to the source. Returns the .asc path. The placement/routing
    engine is the converter; the .asc it emits is what you edit."""
    from .classify import classify_design
    from .emit_asc import export_asc
    from .parser import parse_file
    from .place import place
    from .route import route

    low = path.lower()
    base = os.path.splitext(path)[0]
    if low.endswith(".plan"):
        from .plan import parse_plan, realize_plan
        with open(path, encoding="utf-8") as fh:
            plan = parse_plan(fh.read())
        cands = [os.path.join(os.path.dirname(os.path.abspath(path)),
                              plan.source), plan.source]
        net = next((c for c in cands if c and os.path.exists(c)), None)
        if net is None:
            raise ValueError(f"plan references netlist '{plan.source}' "
                             "which was not found next to the plan")
        design = parse_file(net)
        classify_design(design)
        name = plan.name or design.root().name
        sheet = realize_plan(design.subckts[name], plan)
        wires = getattr(sheet, "plan_wires", None)
        routing = route(sheet, pinned=wires)
        out = base + ".asc"
    else:
        design = parse_file(path)
        classify_design(design)
        _register_top(design)
        name = design.root().name
        if name not in design.subckts and design.order:
            name = design.order[-1]
        sheet = place(design.subckts[name])
        routing = route(sheet)
        out = f"{base}.{name}.asc"
    return export_asc(sheet, routing, out)


def _register_top(design) -> None:
    """Testbench files keep devices outside any .subckt — expose them as
    a synthetic '(top)' sheet so they can be converted too."""
    if design.top_devices and "(top)" not in design.subckts:
        from .db import Subckt
        top = Subckt(name="(top)", ports=[], devices=design.top_devices)
        design.subckts["(top)"] = top
        design.order.append("(top)")


def discover() -> list[str]:
    """Repo files worth one click: schematics, netlists, plans."""
    out: list[str] = []
    skip = {"node_modules", "pepties", "uploads", "sg_sym", "testdata"}
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if not d.startswith((".", "__"))
                   and d not in skip]
        for f in files:
            if f.endswith((".asc", ".plan")) or \
               f.endswith((".cir", ".spice", ".sp")):
                out.append(os.path.relpath(os.path.join(root, f), REPO))
    return sorted(out, key=lambda p: (not p.endswith(".asc"),
                                      not p.endswith(".plan"), p.lower()))


class AppState:
    def __init__(self, path: str | None = None):
        self.src: str | None = None       # what the user opened
        self.path: str | None = None      # the .asc actually edited
        if path:
            self.set_file(path)

    def set_file(self, path: str) -> None:
        self.src = os.path.abspath(path)
        self.path = self.src if self.src.lower().endswith(".asc") \
            else convert_to_asc(self.src)

    def dir(self) -> str:
        return os.path.dirname(self.path) if self.path else REPO

    def text(self) -> str:
        if not self.path:
            return ""
        from .parse_asc import _read_text
        return _read_text(self.path)

    def lib(self, names: list[str]) -> dict:
        return {n: symbol_json(n, self.dir()) for n in names}

    def bootstrap(self) -> dict:
        if not self.path:
            return {"file": None, "source": None, "text": "",
                    "w": 880, "h": 680, "symbols": {}}
        text = self.text()
        sheet = parse_asc(self.path)
        try:
            rel = os.path.relpath(self.src, REPO)
        except ValueError:
            rel = None
        return {"file": os.path.basename(self.path),
                "source": os.path.basename(self.src) if self.src else None,
                "rel": rel,
                "converted": self.src != self.path,
                "text": text, "w": sheet.w, "h": sheet.h,
                "symbols": self.lib(_symbols_in(text))}

    def open(self, path: str) -> dict:
        if not os.path.isabs(path):
            path = os.path.join(REPO, path)
        self.set_file(path)
        return self.bootstrap()

    def upload(self, name: str, content: str) -> dict:
        updir = os.path.join(os.path.dirname(__file__), "..", "uploads")
        os.makedirs(updir, exist_ok=True)
        dest = os.path.join(updir, os.path.basename(name) or "upload.asc")
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(content)
        return self.open(dest)

    def save(self, text: str) -> str:
        if not self.path:
            raise ValueError("no file open")
        with open(self.path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        return self.path


# -------------------------------------------------------- symbol designer
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
            "pins": [[r, offs[r][0] * UNIT, offs[r][1] * UNIT] for r in roles],
            "builtin": builtin_symbol_svg(dev),
            "custom": custom.get(kind),
        }
    return {"unit": UNIT, "kinds": kinds}


# --------------------------------------------------------------- HTTP
class Handler(BaseHTTPRequestHandler):
    state: AppState = None      # set by serve()

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

    def _page(self, name: str) -> None:
        with open(os.path.join(VIEWER, name), "rb") as fh:
            self._send(fh.read(), "text/html; charset=utf-8")

    def do_GET(self):
        url = urlparse(self.path)
        if url.path in ("/", "/index.html"):
            return self._page("asc_editor.html")
        if url.path.startswith("/symbols"):
            return self._page("symbols.html")
        if url.path == "/api/asc":
            return self._json(self.state.bootstrap())
        if url.path == "/api/files":
            return self._json({"files": discover()})
        if url.path == "/api/symbols":
            return self._json(_symbol_payload())
        if url.path == "/api/symlib":
            q = parse_qs(url.query)
            names = [n for n in q.get("names", [""])[0].split(",") if n]
            return self._json(self.state.lib(names))
        self._json({"error": "not found"}, 404)

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(n) or b"{}"
            try:
                body = json.loads(raw.decode("utf-8"))
            except UnicodeDecodeError:
                body = json.loads(raw.decode("latin-1"))
            url = urlparse(self.path)
            if url.path == "/api/save":
                return self._json({"saved": self.state.save(
                    body.get("text", ""))})
            if url.path == "/api/symlib":
                return self._json(self.state.lib(body.get("names", [])))
            if url.path == "/api/open":
                try:
                    return self._json(self.state.open(body.get("path", "")))
                except Exception as exc:
                    return self._json(
                        {"error": f"could not open: {exc}"}, 400)
            if url.path == "/api/upload":
                try:
                    return self._json(self.state.upload(
                        body.get("name", "upload.asc"),
                        body.get("content", "")))
                except Exception as exc:
                    return self._json(
                        {"error": f"could not load: {exc}"}, 400)
            if url.path == "/api/symbol":
                from .symbols import save
                return self._json({"saved": save(body["kind"],
                                                 body.get("elems"))})
            self._json({"error": "not found"}, 404)
        except Exception as exc:               # never drop the connection
            try:
                self._json({"error": f"{type(exc).__name__}: {exc}"}, 500)
            except Exception:
                pass


def serve(path: str | None, port: int) -> None:
    Handler.state = AppState(path)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    where = os.path.basename(path) if path else "no file — pick one in the app"
    print(f"SpiceGlass: http://127.0.0.1:{port}/  ({where})")
    print("Edit the text or drag in the canvas — they stay in sync. "
          "Open/upload files in the app · Ctrl-S saves · /symbols designer.")
    httpd.serve_forever()


# legacy alias (older callers used serve_asc)
serve_asc = serve
