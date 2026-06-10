"""Device classification and rail detection.

Maps model names to (kind, terminal roles) so symbols can be drawn with
oriented pins. Sky130 PDK first; the prefix table is the dialect point
for other PDKs later.
"""
from __future__ import annotations

import re

from .db import Design, Device, Subckt

# (prefix, kind, role template). Roles are zipped against the actual net
# count: shorter → extras become b2, b3…; longer → truncated.
_SKY130 = [
    ("sky130_fd_pr__nfet", "nmos", ["d", "g", "s", "b"]),
    ("sky130_fd_pr__pfet", "pmos", ["d", "g", "s", "b"]),
    ("sky130_fd_pr__esd_nfet", "nmos", ["d", "g", "s", "b"]),
    ("sky130_fd_pr__esd_pfet", "pmos", ["d", "g", "s", "b"]),
    ("sky130_fd_pr__special_nfet", "nmos", ["d", "g", "s", "b"]),
    ("sky130_fd_pr__special_pfet", "pmos", ["d", "g", "s", "b"]),
    ("sky130_fd_pr__res", "res", ["p", "n", "b"]),
    ("sky130_fd_pr__cap_mim", "cap", ["p", "n", "b"]),
    ("sky130_fd_pr__cap_var", "cap", ["p", "n", "b"]),
    ("sky130_fd_pr__diode", "dio", ["p", "n"]),
    ("sky130_fd_pr__pnp", "pnp", ["c", "b", "e"]),
    ("sky130_fd_pr__npn", "npn", ["c", "b", "e", "s"]),
]

_VDD_RE = re.compile(r"^[adp]?v(dd|cc|dda|ddio|ddd|pwr)\w*$", re.I)
_GND_RE = re.compile(r"^([adp]?(gnd|vss)\w*|0)$", re.I)


def classify_design(design: Design) -> None:
    local = set(design.subckts)
    for sub in design.subckts.values():
        for dev in sub.devices:
            _classify_device(dev, local, design)
    for dev in design.top_devices:
        _classify_device(dev, local, design)


def _assign_roles(dev: Device, template: list[str]) -> None:
    roles = list(template[: len(dev.nets)])
    while len(roles) < len(dev.nets):
        roles.append(f"b{len(roles) - len(template) + 2}")
    dev.roles = roles


def _classify_device(dev: Device, local: set[str], design: Design) -> None:
    if dev.kind != "unknown":          # parser already settled R/C/L/V/I/B
        if not dev.roles:
            _assign_roles(dev, ["p", "n"])
        return

    model = dev.model
    if model in local:
        dev.kind = "sub"
        ports = design.subckts[model].ports
        if len(ports) != len(dev.nets):
            design.warnings.append(
                f"line {dev.line}: {dev.name}: {len(dev.nets)} nets vs "
                f"{len(ports)} ports of {model}")
        _assign_roles(dev, list(ports))
        return

    for prefix, kind, roles in _SKY130:
        if model.startswith(prefix):
            dev.kind = kind
            _assign_roles(dev, roles)
            return

    letter = dev.name[0].lower()
    if letter == "m":
        dev.kind = "nmos" if "n" in model[:4] else "pmos"
        _assign_roles(dev, ["d", "g", "s", "b"])
        return
    if letter == "d":
        dev.kind = "dio"
        _assign_roles(dev, ["p", "n"])
        return
    if letter == "q":
        dev.kind = "pnp" if "pnp" in model else "npn"
        _assign_roles(dev, ["c", "b", "e", "s"])
        return

    dev.kind = "unknown"
    _assign_roles(dev, [f"t{i}" for i in range(1, len(dev.nets) + 1)])
    design.warnings.append(
        f"line {dev.line}: {dev.name}: unknown model '{model}' — drawn as box")


# ---------------------------------------------------------------- rails

def rail_class(net: str) -> str | None:
    """'vdd' | 'gnd' | None for an individual net name."""
    if _VDD_RE.match(net):
        return "vdd"
    if _GND_RE.match(net):
        return "gnd"
    return None


def rails_of(sub: Subckt) -> dict[str, str]:
    """net -> 'vdd'|'gnd' for every supply-class net in the sheet."""
    out: dict[str, str] = {}
    for net in sub.nets():
        rc = rail_class(net)
        if rc:
            out[net] = rc
    return out


def short_model(dev: Device) -> str:
    """Compact model text for symbol annotation."""
    m = dev.model
    if m.startswith("sky130_fd_pr__"):
        m = m[len("sky130_fd_pr__"):]
    if not m and "value" in dev.params:
        return dev.params["value"]
    return m
