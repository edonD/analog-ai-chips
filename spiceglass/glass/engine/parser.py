"""ngspice-subset SPICE parser.

Grounded in the netlists this project's AI flows actually emit
(vibrosense/*, pvdd/*): .subckt hierarchy, X-instances of Sky130 PDK
primitives and local subckts, plain R/C with value suffixes, B/G
behavioral sources with free-form expressions, '+' continuations,
and LLM-written section comments which we capture as placement hints.

Anything we cannot interpret is recorded in Design.warnings — devices
are never silently dropped (program.md rule: no silent drops).
"""
from __future__ import annotations

import os
import re

from .db import Design, Device, Subckt

# .include "f" / .inc f   and   .lib "f" section
_INC_RE = re.compile(r'^\s*\.inc(?:lude)?\s+(.+?)\s*$', re.I)
_LIB_RE = re.compile(r'^\s*\.lib\s+(\S+)\s+(\S+)\s*$', re.I)
_MAX_INC_BYTES = 8_000_000
_MAX_INC_DEPTH = 25


def _lib_section(text: str, section: str) -> str:
    """Extract a `.lib <section> … .endl` block (ngspice corner libs)."""
    out, grab = [], False
    for ln in text.splitlines():
        s = ln.strip().lower()
        if s.startswith(".lib ") and s.split()[1:2] == [section.lower()]:
            grab = True
            continue
        if grab and s.startswith(".endl"):
            break
        if grab:
            out.append(ln)
    return "\n".join(out)


def _expand_includes(text, basedir, seen=None, depth=0):
    """Splice .include/.inc files (and .lib sections) inline so multi-file
    decks parse completely. Resolves relative to `basedir`; guards cycles,
    depth, and size; missing files become a warning, never a crash."""
    if seen is None:
        seen = set()
    out, warnings = [], []
    if depth > _MAX_INC_DEPTH:
        return text, ["include depth limit exceeded"]
    for line in text.splitlines():
        m = _INC_RE.match(line)
        lib = None if m else _LIB_RE.match(line)
        if not m and not lib:
            out.append(line)
            continue
        raw = (m.group(1) if m else lib.group(1)).strip().strip('"\'')
        section = lib.group(2) if lib else None
        path = raw if os.path.isabs(raw) else os.path.join(basedir, raw)
        path = os.path.normpath(path)
        if path in seen:
            warnings.append(f"include cycle skipped: {raw}")
            continue
        if not os.path.exists(path):
            warnings.append(f"include not found: {raw}")
            out.append(f"* [missing include: {raw}]")
            continue
        try:
            if os.path.getsize(path) > _MAX_INC_BYTES:
                warnings.append(f"include too large, skipped: {raw}")
                continue
            with open(path, encoding="utf-8", errors="replace") as fh:
                inc = fh.read()
        except OSError as e:
            warnings.append(f"include unreadable {raw}: {e}")
            continue
        if section:
            inc = _lib_section(inc, section)
        exp, w = _expand_includes(inc, os.path.dirname(path),
                                  seen | {path}, depth + 1)
        warnings.extend(w)
        out.append(f"* >>> include {raw}"
                   + (f" [{section}]" if section else ""))
        out.append(exp)
        out.append(f"* <<< end {raw}")
    return "\n".join(out), warnings

# ---------------------------------------------------------------- sections

# single-line banner:  ** ===== Title =====   |  * --- Title ---
_SECTION_ONE = re.compile(r"^\*+\s*[=\-]{3,}\s*(.+?)\s*[=\-]{3,}\s*$")
# a rule line:         * ============================
_RULE = re.compile(r"^\*+[\s=\-]*$")


def _clean_comment(line: str) -> str:
    return line.lstrip("*").strip()


# ---------------------------------------------------------------- tokenizing

def _strip_inline_comment(line: str) -> str:
    """Strip ' ; ' and ' $ ' comments outside quotes."""
    out = []
    in_q = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "'":
            in_q = not in_q
        if not in_q and ch in ";$" and (i == 0 or line[i - 1].isspace()):
            break
        out.append(ch)
        i += 1
    return "".join(out)


def _tokens(line: str) -> list[str]:
    """Whitespace split, but keep '...'-quoted and {...} groups intact."""
    toks, cur, q = [], [], None
    for ch in line:
        if q:
            cur.append(ch)
            if (q == "'" and ch == "'") or (q == "{" and ch == "}"):
                q = None
            continue
        if ch in "'{":
            q = "'" if ch == "'" else "{"
            cur.append(ch)
        elif ch.isspace():
            if cur:
                toks.append("".join(cur))
                cur = []
        else:
            cur.append(ch)
    if cur:
        toks.append("".join(cur))
    return toks


def _strip_inline(s: str) -> str:
    """Drop HSPICE/CDL inline comments and layout properties: everything
    from a whitespace-delimited '$' or '//' to end of line (e.g. device
    lines like `... l=1u $X=0 $SUB=vss`). Leaves normal cards untouched."""
    cut = len(s)
    for tok in (" $", "\t$", " //", "\t//"):
        i = s.find(tok)
        if 0 <= i < cut:
            cut = i
    return s[:cut].rstrip()


import ast as _ast                                            # noqa: E402
import operator as _opr                                       # noqa: E402

_SUFFIX = {"t": 1e12, "g": 1e9, "meg": 1e6, "k": 1e3, "mil": 25.4e-6,
           "m": 1e-3, "u": 1e-6, "n": 1e-9, "p": 1e-12, "f": 1e-15}
_BINOPS = {_ast.Add: _opr.add, _ast.Sub: _opr.sub, _ast.Mult: _opr.mul,
           _ast.Div: _opr.truediv, _ast.Pow: _opr.pow}
_UNOPS = {_ast.USub: _opr.neg, _ast.UAdd: _opr.pos}
_NUM_SUF = re.compile(r'(?<![\w.])(\d+\.?\d*(?:e[-+]?\d+)?)'
                      r'(t|g|meg|mil|k|m|u|n|p|f)\b', re.I)
_PLAIN = re.compile(r'^[-+]?\d+\.?\d*(?:e[-+]?\d+)?'
                    r'(?:t|g|meg|mil|k|m|u|n|p|f)?$', re.I)


def _spice_floats(expr: str) -> str:
    return _NUM_SUF.sub(
        lambda m: repr(float(m.group(1)) * _SUFFIX[m.group(2).lower()]), expr)


def _eval_expr(expr: str, vals: dict[str, float]) -> float:
    """Safe arithmetic eval of a SPICE param expression (no code exec):
    numbers w/ SI suffixes, + - * / ** ( ), and references to resolved
    params. Raises on anything else (caller leaves it verbatim)."""
    tree = _ast.parse(_spice_floats(expr.strip().strip("'\"{} ")), mode="eval")

    def ev(node):
        if isinstance(node, _ast.Expression):
            return ev(node.body)
        if isinstance(node, _ast.Constant):
            return float(node.value)
        if isinstance(node, _ast.BinOp) and type(node.op) in _BINOPS:
            return _BINOPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, _ast.UnaryOp) and type(node.op) in _UNOPS:
            return _UNOPS[type(node.op)](ev(node.operand))
        if isinstance(node, _ast.Name):
            return vals[node.id.lower()]
        raise ValueError("unsupported expression")
    return ev(tree.body)


def _fmt_eng(x: float) -> str:
    if x == 0:
        return "0"
    for suf, mul in (("t", 1e12), ("g", 1e9), ("meg", 1e6), ("k", 1e3),
                     ("", 1.0), ("m", 1e-3), ("u", 1e-6), ("n", 1e-9),
                     ("p", 1e-12), ("f", 1e-15)):
        if abs(x) >= mul:
            return f"{x / mul:.4g}{suf}"
    return f"{x:.4g}"


def _resolve_params(raw: dict[str, str]) -> dict[str, float]:
    vals: dict[str, float] = {}
    for _ in range(12):                       # fixpoint over inter-param refs
        progress = False
        for k, e in raw.items():
            try:
                v = _eval_expr(e, vals)
            except Exception:
                continue
            if vals.get(k.lower()) != v:
                vals[k.lower()] = v
                progress = True
        if not progress:
            break
    return vals


def _eval_device_params(design: "Design") -> None:
    """Evaluate parameter EXPRESSIONS on devices to numbers (plain numeric
    values are left untouched; unresolved expressions stay verbatim)."""
    vals = _resolve_params(design.params)

    def fix(dev):
        for k, v in list(dev.params.items()):
            if not isinstance(v, str) or _PLAIN.match(v):
                continue
            try:
                dev.params[k] = _fmt_eng(_eval_expr(v, vals))
            except Exception:
                pass                          # leave verbatim, no crash
    for sub in design.subckts.values():
        for d in sub.devices:
            fix(d)
    for d in design.top_devices:
        fix(d)


def _split_params(tokens: list[str]) -> tuple[list[str], dict[str, str]]:
    """Separate positional tokens from key=value parameters, tolerating
    spaces around '=' (common in foundry/HSPICE decks, e.g. `W= 1u`,
    `W = 1u`, `W =1u`) — otherwise the value gets misread as a node."""
    pos, params, i, n = [], {}, 0, len(tokens)
    while i < n:
        t = tokens[i]
        if t.startswith(("'", "{")):
            pos.append(t)
            i += 1
        elif "=" in t:                         # 'k=v' or 'k=' (+ next token)
            k, _, v = t.partition("=")
            if v == "" and i + 1 < n:
                v = tokens[i + 1]
                i += 1
            params[k.lower()] = v
            i += 1
        elif i + 1 < n and tokens[i + 1].startswith("="):   # 'k' '=v' / '=' 'v'
            rest = tokens[i + 1][1:]
            if rest == "" and i + 2 < n:
                rest = tokens[i + 2]
                i += 1
            params[t.lower()] = rest
            i += 2
        else:
            pos.append(t)
            i += 1
    return pos, params


# ---------------------------------------------------------------- main parse

_BEHAVIORAL = "befgh"   # B nonlinear, E/G controlled, F/H current-controlled
_IGNORED_DOTS = (".option", ".options", ".param", ".include", ".lib", ".model",
                 ".global", ".temp", ".ic", ".nodeset", ".save", ".meas",
                 ".measure", ".dc", ".ac", ".tran", ".op", ".noise", ".print",
                 ".plot", ".probe", ".csparam", ".func", ".if", ".else",
                 ".endif", ".title", ".width")


def parse_file(path: str) -> Design:
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    text, inc_warn = _expand_includes(
        text, os.path.dirname(os.path.abspath(path)))
    design = parse_text(text, path)
    design.warnings.extend(inc_warn)
    return design


def parse_text(text: str, path: str = "<string>") -> Design:
    design = Design(path=path)
    raw_lines = text.lstrip("﻿").splitlines()

    # ---- pass 1: join continuations, keep (first_line_no, full_line) pairs,
    #      and interleave comment lines for section tracking
    items: list[tuple[str, int, str]] = []   # (type 'c'|'l', lineno, content)
    logical: tuple[int, list[str]] | None = None
    for no, raw in enumerate(raw_lines, 1):
        s = raw.strip()
        if not s:
            if logical:
                items.append(("l", logical[0], " ".join(logical[1])))
                logical = None
            continue
        if s.startswith(("*", "$")):          # '$'-first line = CDL/HSPICE comment
            if logical:
                items.append(("l", logical[0], " ".join(logical[1])))
                logical = None
            items.append(("c", no, s))
            continue
        s = _strip_inline(s)                  # drop ' $...' / ' //...' tails
        if not s:
            continue
        if s.startswith("+"):
            if logical:
                logical[1].append(s[1:].strip())
            else:
                design.warnings.append(f"line {no}: continuation with no card")
            continue
        if logical:
            items.append(("l", logical[0], " ".join(logical[1])))
        logical = (no, [s])
    if logical:
        items.append(("l", logical[0], " ".join(logical[1])))

    # ---- pass 2: sections + cards
    section = ""
    cur: Subckt | None = None
    in_control = False
    i = 0
    while i < len(items):
        typ, no, content = items[i]

        if typ == "c":
            # consume the whole comment run at once
            run = []
            while i < len(items) and items[i][0] == "c":
                run.append(items[i][2])
                i += 1
            new = None
            for ln in run:
                m = _SECTION_ONE.match(ln)
                if m:
                    new = m.group(1).strip()
                    break
            if new is None and len(run) >= 2 and _RULE.match(run[0]):
                txt = _clean_comment(run[1])
                if txt:
                    new = txt
            if new and re.search(r"\w", new):    # no symbol-only titles
                section = new
            continue

        i += 1
        line = _strip_inline_comment(content).strip()
        if not line:
            continue
        low = line.lower()

        if in_control:
            if low.startswith(".endc"):
                in_control = False
            continue
        if low.startswith(".control"):
            in_control = True
            design.warnings.append(f"line {no}: .control block skipped")
            continue

        if low.startswith("."):
            toks = _tokens(line)
            head = toks[0].lower()
            if head == ".subckt":
                pos, _ = _split_params(toks[1:])
                if not pos:
                    design.warnings.append(f"line {no}: .subckt without name")
                    continue
                cur = Subckt(name=pos[0].lower(),
                             ports=[p.lower() for p in pos[1:]], line=no)
                design.subckts[cur.name] = cur
                design.order.append(cur.name)
                section = ""
                continue
            if head == ".ends":
                cur = None
                section = ""
                continue
            if head == ".end":
                break
            if head == ".param":
                _, prm = _split_params(toks[1:])
                design.params.update(prm)
                continue
            if head in _IGNORED_DOTS:
                continue
            design.warnings.append(f"line {no}: unhandled card: {line[:60]}")
            continue

        dev = _parse_device(line, no, design)
        if dev is None:
            continue
        dev.section = section
        target = cur.devices if cur else design.top_devices
        target.append(dev)

    # record section order per subckt
    for sub in design.subckts.values():
        seen: dict[str, None] = {}
        for d in sub.devices:
            if d.section:
                seen.setdefault(d.section)
        sub.sections = list(seen)
    _eval_device_params(design)          # resolve .param expressions to numbers
    return design


def _parse_device(line: str, no: int, design: Design) -> Device | None:
    letter = line[0].lower()
    toks = _tokens(line)
    name = toks[0]

    if letter in _BEHAVIORAL:
        # Bxx n+ n- <expression possibly with spaces>
        if len(toks) < 4:
            design.warnings.append(f"line {no}: malformed source: {line[:60]}")
            return None
        nets = [toks[1].lower(), toks[2].lower()]
        expr = line.split(None, 3)[3] if len(line.split(None, 3)) > 3 else ""
        return Device(name=name, kind="bsrc", model="", nets=nets,
                      roles=["p", "n"], expr=expr, line=no)

    if letter in "xmqd":
        pos, params = _split_params(toks[1:])
        if len(pos) < 2:
            design.warnings.append(f"line {no}: malformed device: {line[:60]}")
            return None
        model = pos[-1].lower()
        nets = [n.lower() for n in pos[:-1]]
        return Device(name=name, kind="unknown", model=model, nets=nets,
                      params=params, line=no)

    if letter in "rcl":
        pos, params = _split_params(toks[1:])
        if len(pos) < 2:
            design.warnings.append(f"line {no}: malformed RLC: {line[:60]}")
            return None
        nets = [pos[0].lower(), pos[1].lower()]
        if len(pos) >= 3:
            params.setdefault("value", pos[2])
        kind = {"r": "res", "c": "cap", "l": "ind"}[letter]
        return Device(name=name, kind=kind, model="", nets=nets,
                      roles=["p", "n"], params=params, line=no)

    if letter in "vi":
        if len(toks) < 3:
            design.warnings.append(f"line {no}: malformed source: {line[:60]}")
            return None
        nets = [toks[1].lower(), toks[2].lower()]
        spec = " ".join(toks[3:])
        kind = "vsrc" if letter == "v" else "isrc"
        return Device(name=name, kind=kind, model="", nets=nets,
                      roles=["p", "n"], params={"spec": spec}, line=no)

    design.warnings.append(f"line {no}: unsupported element '{letter}': {line[:60]}")
    return None
