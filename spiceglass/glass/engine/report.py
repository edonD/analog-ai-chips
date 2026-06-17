"""Design-report generation — README-grade markdown from the engine.

Ties together everything SpiceGlass knows about a netlist into the kind of
block writeup a designer keeps by hand: ports, recognized structures, a
device table with faithful sizing, and (optionally) the DC operating point
— node voltages and per-transistor region. Pure read-only.
"""
from __future__ import annotations

from .classify import device_value
from .db import Design, Subckt
from .structure import recognize_structures


def _device_table(sub: Subckt) -> list[str]:
    rows = ["| Device | Type | Model | Sizing | Nets |",
            "|---|---|---|---|---|"]
    for d in sub.devices:
        sizing = device_value(d) or "—"
        rows.append(f"| {d.name} | {d.kind} | {d.model or '—'} | "
                    f"{sizing} | {' '.join(d.nets)} |")
    return rows


def _op_section(sub: Subckt, op) -> list[str]:
    """OP table for the devices/nets on this subckt (op keyed by ngspice
    names; here we show top-level matches — bare device/net names)."""
    out = []
    regions = {name: d for name, d in op.mos.items() if "." not in name}
    rows = [(d.name, regions[d.name.lower()])
            for d in sub.devices if d.name.lower() in regions]
    if rows:
        out += ["", "**Operating point — transistor regions**", "",
                "| Device | Region | Vgs | Vds | Id |", "|---|---|---|---|---|"]
        for name, r in rows:
            out.append(f"| {name} | {r['region']} | {r['vgs']:+.3f} | "
                       f"{r['vds']:+.3f} | {r['id']:.3e} |")
    nodes = {n: v for n, v in op.nodes.items() if "." not in n}
    sub_nets = {x.lower() for x in sub.nets()}
    shown = sorted((n, v) for n, v in nodes.items() if n in sub_nets)
    if shown:
        out += ["", "**Node voltages**", "",
                "| Net | V |", "|---|---|"]
        out += [f"| {n} | {v:+.4f} |" for n, v in shown]
    return out


def markdown_report(design: Design, op=None, title: str = "") -> str:
    out = [f"# {title or design.path or 'SpiceGlass report'}", ""]
    blocks = [(n, design.subckts[n]) for n in design.order
              if design.subckts[n].devices]
    if design.top_devices:        # flat / testbench devices outside any subckt
        blocks.insert(0, ("(top)", Subckt(name="(top)", ports=[],
                                          devices=design.top_devices)))
    if design.params:
        out += ["**Parameters:** "
                + ", ".join(f"`{k}={v}`" for k, v in design.params.items()),
                ""]
    for name, sub in blocks:
        out.append(f"## {name}")
        out.append(f"*Ports:* {', '.join(sub.ports) or '(none)'}  ")
        out.append(f"*{len(sub.devices)} devices · {len(sub.nets())} nets*")
        structs = recognize_structures(sub)
        if structs:
            out.append("")
            out.append("**Recognized structures**")
            for s in structs:
                out.append(f"- {s['kind']}: {', '.join(s['devices'])}")
        out.append("")
        out += _device_table(sub)
        if op is not None and getattr(op, "ok", False):
            out += _op_section(sub, op)
        out.append("")
    return "\n".join(out) + "\n"
