"""Operating-point back-annotation.

Runs ngspice on a SIMULATABLE deck (models + sources + a bias point),
reads every node voltage and each MOSFET's operating-point parameters,
and classifies each transistor's region (off / triode / saturation).
This is what turns a converted schematic from "a picture" into "a picture
that tells you whether the circuit is biased right".

Requirements (honest): the deck must be simulatable by ngspice — i.e. its
models resolve (generic .model lines, or a PDK .lib the user has). On a
bare .subckt with no models we can't simulate; node voltages cover any
deck, transistor regions need plain M devices (subckt-wrapped PDK X
devices expose nodes but not @m op vectors).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field

_HERE = os.path.dirname(os.path.abspath(__file__))

I_OFF = 1e-9        # |Id| below this ⇒ the device is OFF
_NUM = r"[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?"

# ngspice's predefined constant vectors — `print all` lists THESE (and only
# these) when the operating point failed/empty, so they must never be read
# as node voltages, and their presence with no real nodes signals failure.
_CONSTS = frozenset((
    "false", "true", "boltz", "c", "e", "echarge", "i", "kelvin", "no",
    "pi", "planck", "yes", "temper", "vt", "hertz", "time"))


@dataclass
class OpResult:
    ok: bool = False
    error: str = ""
    nodes: dict[str, float] = field(default_factory=dict)
    mos: dict[str, dict] = field(default_factory=dict)   # name -> {vgs,vds,
    #                                                       vdsat,id,region}


def ngspice_bin() -> str | None:
    """Locate ngspice — the bundled Spice64 build first, then PATH."""
    cands = [
        os.path.join(_HERE, "..", "..", "Spice64", "bin", "ngspice_con.exe"),
        shutil.which("ngspice_con"), shutil.which("ngspice"),
    ]
    for c in cands:
        if c and os.path.exists(c):
            return os.path.abspath(c)
    return None


def _mos_names(text: str) -> list[str]:
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if s and s[0] in "mM" and not s.startswith(("*", ".")):
            out.append(s.split()[0])
    return out


def _enumerate_mos(text: str) -> list[str]:
    """ngspice op-vector names for every MOSFET, including those inside
    subckt instances: top-level `m1`, nested `m.<instpath>.<dev>` (dotted
    instance path, matching ngspice's @device addressing). Falls back to a
    flat scan if the deck won't structurally parse."""
    from .parser import parse_text
    from .classify import classify_design
    try:
        d = parse_text(text)
        classify_design(d)
    except Exception:
        return _mos_names(text)
    out: list[str] = []

    def walk(subname, path, seen):
        sub = d.subckts.get(subname)
        if not sub or subname in seen:
            return
        for dev in sub.devices:
            if dev.kind in ("nmos", "pmos"):
                out.append(f"m.{path}.{dev.name}".lower())
            elif dev.kind == "sub":
                walk(dev.model, f"{path}.{dev.name}", seen | {subname})

    for dev in d.top_devices:
        if dev.kind in ("nmos", "pmos"):
            out.append(dev.name.lower())
        elif dev.kind == "sub":
            walk(dev.model, dev.name, set())
    return out or _mos_names(text)


def _strip_control_end(text: str) -> str:
    """Drop any existing .control…​.endc block and bare .end (keep .ends),
    so we can append our own deterministic control section."""
    out, skip = [], False
    for ln in text.splitlines():
        low = ln.strip().lower()
        if low.startswith(".control"):
            skip = True
            continue
        if skip:
            if low.startswith(".endc"):
                skip = False
            continue
        if low == ".end":
            continue
        out.append(ln)
    return "\n".join(out)


def _region(vds: float, vdsat: float, idd: float) -> str:
    if abs(idd) < I_OFF:
        return "off"
    if abs(vds) + 1e-12 >= abs(vdsat):
        return "sat"
    return "triode"


def run_op(text: str, timeout: int = 30) -> OpResult:
    """Simulate the deck's operating point and return node voltages +
    per-MOSFET region. Never raises — failures come back as ok=False."""
    binp = ngspice_bin()
    if not binp:
        return OpResult(ok=False, error="ngspice not found")

    body = _strip_control_end(text)
    lines = body.splitlines()
    if not lines or lines[0].strip().startswith("."):
        body = "* spiceglass op\n" + body      # ngspice eats line 1 as title

    ctrl = [".control", "op", "print all"]
    mos = _enumerate_mos(body)               # incl. devices inside subckts
    for m in mos:
        ctrl.append(f"print @{m}[vgs] @{m}[vds] @{m}[vdsat] @{m}[id]")
    ctrl += [".endc", ".end"]
    deck = body + "\n" + "\n".join(ctrl) + "\n"

    tmp = tempfile.NamedTemporaryFile("w", suffix=".cir", delete=False,
                                      encoding="utf-8", newline="\n")
    try:
        tmp.write(deck)
        tmp.close()
        try:
            p = subprocess.run([binp, "-b", tmp.name], capture_output=True,
                               text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return OpResult(ok=False, error="ngspice timed out")
        out = (p.stdout or "") + "\n" + (p.stderr or "")
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass

    res = OpResult()
    raw: dict[str, dict] = {}
    for ln in out.splitlines():
        m = re.match(rf"@([\w.]+)\[(\w+)\]\s*=\s*({_NUM})\s*$", ln.strip())
        if m:
            raw.setdefault(m.group(1).lower(), {})[m.group(2)] = \
                float(m.group(3))
            continue
        m = re.match(rf"([A-Za-z][\w.:]*)\s*=\s*({_NUM})\s*$", ln.strip())
        if m and "#" not in m.group(1) and not m.group(1).endswith("branch") \
                and m.group(1).lower() not in _CONSTS:
            res.nodes[m.group(1).lower()] = float(m.group(2))

    for name in mos:
        d = raw.get(name.lower())
        if not d:
            continue
        vds, vdsat, idd = d.get("vds", 0.0), d.get("vdsat", 0.0), \
            d.get("id", 0.0)
        res.mos[name] = {"vgs": d.get("vgs", 0.0), "vds": vds,
                         "vdsat": vdsat, "id": idd,
                         "region": _region(vds, vdsat, idd)}

    if not res.nodes:
        low = out.lower()
        if "could not find a valid model" in low or "can't find model" in low:
            res.error = "unresolved model(s) — deck not simulatable here"
        elif "no simulations run" in low:
            res.error = "no operating point produced"
        else:
            res.error = ("no operating point — deck needs models + sources "
                         "to be simulatable (a bare .subckt can't be biased)")
        res.ok = False
        return res
    res.ok = True
    return res


def run_op_file(path: str, timeout: int = 30) -> OpResult:
    from ..asc.parse import _read_text
    return run_op(_read_text(path), timeout=timeout)
