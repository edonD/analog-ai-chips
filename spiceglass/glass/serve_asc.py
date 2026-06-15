"""Interactive LTspice .asc editor server — `glass edit sheet.asc`.

The browser is the renderer/editor; this server is thin. It serves the
editor page, resolves symbol artwork (.asy on disk — ours from sg_sym/
or LTspice's library, falling back to corpus-derived native glyphs) to
JSON, and persists the .asc text on save.

The .asc TEXT is the single source of truth (see
research/asc-web-renderer.md). The client parses, renders, culls,
hit-tests and round-trips edits as minimal line patches; the only thing
it cannot do alone is read .asy files off disk, which is this server's
whole job.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .parse_asc import (native_symbol, parse_asc, parse_asy, resolve_asy)


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


class AscEditorState:
    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        self.dir = os.path.dirname(self.path)

    def text(self) -> str:
        from .parse_asc import _read_text
        return _read_text(self.path)

    def lib(self, names: list[str]) -> dict:
        return {n: symbol_json(n, self.dir) for n in names}

    def bootstrap(self) -> dict:
        text = self.text()
        sheet = parse_asc(self.path)
        return {"file": os.path.basename(self.path), "text": text,
                "w": sheet.w, "h": sheet.h,
                "symbols": self.lib(_symbols_in(text))}

    def save(self, text: str) -> None:
        with open(self.path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)


class Handler(BaseHTTPRequestHandler):
    state: AscEditorState = None      # set by serve_asc()

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
        url = urlparse(self.path)
        if url.path in ("/", "/index.html"):
            page = os.path.join(os.path.dirname(__file__), "..", "viewer",
                                "asc_editor.html")
            with open(page, "rb") as fh:
                self._send(fh.read(), "text/html; charset=utf-8")
            return
        if url.path == "/api/asc":
            self._json(self.state.bootstrap())
            return
        if url.path == "/api/symlib":
            q = parse_qs(url.query)
            raw = q.get("names", [""])[0]
            names = [n for n in raw.split(",") if n]
            self._json(self.state.lib(names))
            return
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
                self.state.save(body.get("text", ""))
                self._json({"saved": self.state.path})
                return
            if url.path == "/api/symlib":
                names = body.get("names", [])
                self._json(self.state.lib(names))
                return
            self._json({"error": "not found"}, 404)
        except Exception as exc:               # never drop the connection
            try:
                self._json({"error": f"{type(exc).__name__}: {exc}"}, 500)
            except Exception:
                pass


def serve_asc(path: str, port: int) -> None:
    Handler.state = AscEditorState(path)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"SpiceGlass .asc editor: http://127.0.0.1:{port}/  "
          f"({os.path.basename(path)})")
    print("Edit the text or drag in the canvas — they stay in sync. "
          "Ctrl-S saves to disk.")
    httpd.serve_forever()
