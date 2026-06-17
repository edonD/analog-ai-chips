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

from ..geom import UNIT
from ..asc.parse import native_symbol, parse_asc, parse_asy, resolve_asy

REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
VIEWER = os.path.join(os.path.dirname(__file__), "..", "..", "viewer")


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
    from ..engine.classify import classify_design
    from ..asc.emit import export_asc
    from ..engine.parser import parse_file
    from ..engine.place import place
    from ..engine.route import route

    low = path.lower()
    base = os.path.splitext(path)[0]
    if low.endswith(".plan"):
        from ..engine.plan import parse_plan, realize_plan
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
        sub = design.subckts[name]
        sheet, routing, note = _best_placement(sub)
        out = export_asc(sheet, routing, f"{base}.{name}.asc")
        if note:                   # transparency: record what the optimizer did
            with open(out, "a", encoding="utf-8") as fh:
                fh.write(f"TEXT 64 {(sheet.height + 4) * 8} Left 1 ;{note}\n")
        return out
    return export_asc(sheet, routing, out)


def _best_placement(sub, max_rank: int = 6):
    """Verify-gated optimization: try the optimizer's top-ranked orderings
    and keep the best one that BOTH verifies and beats the seed; never
    trade correctness for looks. Returns (sheet, routing, note)."""
    from ..engine.place import place
    from ..engine.route import route
    from ..engine.score import score
    from ..engine.verify import verify

    seed = place(sub); seed_r = route(seed)
    s0 = score(seed, seed_r)
    seed_ok = verify(seed_r).ok

    seen, chosen = set(), None
    for k in range(max_rank):
        sh = place(sub, optimize=True, opt_rank=k)
        sig = tuple((d.name, sh.pos(d).x, sh.pos(d).y) for d in sub.devices)
        if sig in seen:          # ranks exhausted (same order repeats)
            break
        seen.add(sig)
        r = route(sh)
        if not verify(r).ok:
            continue
        sc = score(sh, r)
        if sc.crossings < s0.crossings or sc.wirelength < s0.wirelength:
            note = (f"auto-arranged: crossings {s0.crossings}->{sc.crossings}, "
                    f"wirelength {s0.wirelength}->{sc.wirelength}mm "
                    f"(SpiceGlass optimizer)")
            return sh, r, note          # best-first: first improvement wins
        chosen = chosen or (sh, r)      # verifies but no better; remember
    if seed_ok:
        return seed, seed_r, ""
    return (chosen or (seed, seed_r)) + \
        ("auto-placed (optimization could not verify)",)


def _register_top(design) -> None:
    """Testbench files keep devices outside any .subckt — expose them as
    a synthetic '(top)' sheet so they can be converted too."""
    if design.top_devices and "(top)" not in design.subckts:
        from ..engine.db import Subckt
        top = Subckt(name="(top)", ports=[], devices=design.top_devices)
        design.subckts["(top)"] = top
        design.order.append("(top)")


IMPORT_DIR = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "..", "uploads", "imported_sym"))

_BUILTIN_PALETTE = ["res", "cap", "ind", "diode", "nmos", "pmos", "npn",
                    "pnp", "njf", "pjf", "voltage", "current", "bv", "bi",
                    "e", "g", "sw", "opamp", "opamp2"]


def import_library(name: str, content: str) -> dict:
    """Convert an uploaded KiCad .kicad_sym or xschem .sym to .asy files
    in IMPORT_DIR (so they resolve like any symbol). Returns the names."""
    from ..asc.import_sym import asy_text, import_text
    fmt = "kicad" if name.lower().endswith(".kicad_sym") else "xschem"
    syms = import_text(content, fmt)
    os.makedirs(IMPORT_DIR, exist_ok=True)
    written = []
    for sname, sym in syms.items():
        base = (os.path.splitext(os.path.basename(name))[0]
                if fmt == "xschem" else sname)
        safe = "".join(c for c in base if c.isalnum() or c in "_-+.") or "sym"
        with open(os.path.join(IMPORT_DIR, safe + ".asy"), "w",
                  encoding="utf-8") as fh:
            fh.write(asy_text(sym, safe))
        written.append(safe)
    return {"imported": sorted(written), "count": len(written), "format": fmt}


def list_imported() -> list[str]:
    if not os.path.isdir(IMPORT_DIR):
        return []
    return sorted(os.path.splitext(f)[0] for f in os.listdir(IMPORT_DIR)
                  if f.lower().endswith(".asy"))


_DIR_CAP = 20       # max netlists listed per directory — generated
                    # benchmark corpora hold thousands of .cir; listing them
                    # all makes the file dropdown unusably slow.


def discover() -> list[str]:
    """Repo files worth one click: schematics, netlists, plans. Each
    directory contributes at most _DIR_CAP netlists so a bulk generated
    corpus (benchmark/real, benchmark/hier, ...) can't flood the picker."""
    skip = {"node_modules", "pepties", "uploads", "sg_sym", "testdata",
            "benchmark",    # 1000s of generated test netlists
            "Spice64"}      # vendored ngspice example corpus (stress only)
                            # curated samples live in examples/
    by_dir: dict[str, list[str]] = {}
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs
                   if not d.startswith((".", "__", "tmp"))
                   and d not in skip and not d.endswith("_results")]
        for f in files:
            if f.endswith((".asc", ".plan", ".cir", ".spice", ".sp")):
                by_dir.setdefault(root, []).append(
                    os.path.relpath(os.path.join(root, f), REPO))
    out: list[str] = []
    for paths in by_dir.values():
        # keep .asc/.plan first, then a capped sample of netlists
        paths.sort(key=lambda p: (not p.endswith(".asc"),
                                  not p.endswith(".plan"), p.lower()))
        out.extend(paths[:_DIR_CAP])
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
        from ..asc.parse import _read_text
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
        updir = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
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
    from ..engine.db import Device
    from ..geom import pin_offsets
    from ..engine.render_svg import builtin_symbol_svg
    from ..engine.symbols import lib
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
        if url.path == "/api/library":
            return self._json({"imported": list_imported(),
                               "builtin": _BUILTIN_PALETTE})
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
                from ..engine.symbols import save
                return self._json({"saved": save(body["kind"],
                                                 body.get("elems"))})
            if url.path == "/api/import":
                try:
                    return self._json(import_library(
                        body.get("name", "lib.kicad_sym"),
                        body.get("content", "")))
                except Exception as exc:
                    return self._json(
                        {"error": f"import failed: {exc}"}, 400)
            self._json({"error": "not found"}, 404)
        except Exception as exc:               # never drop the connection
            try:
                self._json({"error": f"{type(exc).__name__}: {exc}"}, 500)
            except Exception:
                pass


def _port_free(port: int) -> bool:
    """True if nothing is already serving on the port. We probe with a
    connect because on Windows SO_REUSEADDR lets a second bind silently
    hijack a live port, so bind-failure alone is not reliable."""
    import socket
    with socket.socket() as s:
        s.settimeout(0.2)
        return s.connect_ex(("127.0.0.1", port)) != 0


def serve(path: str | None, port: int, open_browser: bool = True) -> None:
    from ..asc import parse as _parse
    os.makedirs(IMPORT_DIR, exist_ok=True)
    if IMPORT_DIR not in _parse.EXTRA_SYM_DIRS:        # imported libs resolve
        _parse.EXTRA_SYM_DIRS.append(IMPORT_DIR)
    Handler.state = AppState(path)
    httpd = None
    for p in range(port, port + 25):       # busy port? just take the next one
        if not _port_free(p):
            continue
        try:
            httpd = ThreadingHTTPServer(("127.0.0.1", p), Handler)
            port = p
            break
        except OSError:
            continue
    if httpd is None:
        print(f"SpiceGlass: no free port near {port} — close other copies "
              "and try again.")
        return
    url = f"http://127.0.0.1:{port}/"
    where = os.path.basename(path) if path else "no file — pick one in the app"
    print()
    print(f"  SpiceGlass is running at  {url}   ({where})")
    print("  Edit the text or drag in the canvas — they stay in sync.")
    print("  Open/upload files in the app · Ctrl-S saves · /symbols designer.")
    print("  Keep this window open while you work; close it to stop.")
    print()
    if open_browser:
        import threading
        import webbrowser
        threading.Timer(0.9, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  SpiceGlass stopped.")


# legacy alias (older callers used serve_asc)
serve_asc = serve
