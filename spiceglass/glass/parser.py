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

import re

from .db import Design, Device, Subckt

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


def _split_params(tokens: list[str]) -> tuple[list[str], dict[str, str]]:
    """Separate positional tokens from key=value parameters."""
    pos, params = [], {}
    for t in tokens:
        if "=" in t and not t.startswith(("'", "{")):
            k, _, v = t.partition("=")
            params[k.lower()] = v
        else:
            pos.append(t)
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
    return parse_text(text, path)


def parse_text(text: str, path: str = "<string>") -> Design:
    design = Design(path=path)
    raw_lines = text.splitlines()

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
        if s.startswith("*"):
            if logical:
                items.append(("l", logical[0], " ".join(logical[1])))
                logical = None
            items.append(("c", no, s))
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
            if new:
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
