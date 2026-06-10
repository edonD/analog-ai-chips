"""Circuit database — the spine of SpiceGlass.

Every other module (placer, renderer, verifier, cone extractor, doc
generator, future viewer/MCP server) is a query over these structures.
JSON-serializable by design.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict


@dataclass
class Device:
    name: str                 # instance name as written (XM1, R_rect, B_hw1)
    kind: str                 # nmos|pmos|res|cap|ind|dio|vsrc|isrc|bsrc|sub|unknown
    model: str                # sky130_fd_pr__nfet_01v8 | local subckt name | "" for value devices
    nets: list[str] = field(default_factory=list)    # connection order as written
    roles: list[str] = field(default_factory=list)   # parallel to nets: d/g/s/b, p/n, port names
    params: dict[str, str] = field(default_factory=dict)  # w, l, m, value...
    expr: str = ""            # behavioral expression for B/E/G sources
    section: str = ""         # comment-section cluster this device was written under
    line: int = 0             # source line (1-based) for cross-probing

    def net_of(self, role: str) -> str | None:
        for r, n in zip(self.roles, self.nets):
            if r == role:
                return n
        return None

    @property
    def is_mos(self) -> bool:
        return self.kind in ("nmos", "pmos")

    def channel_nets(self) -> tuple[str, str] | None:
        """The two terminals current flows between (placement backbone)."""
        if self.is_mos:
            return (self.net_of("d"), self.net_of("s"))
        if self.kind in ("res", "cap", "ind", "dio", "vsrc", "isrc", "bsrc"):
            if len(self.nets) >= 2:
                return (self.nets[0], self.nets[1])
        return None


@dataclass
class Subckt:
    name: str
    ports: list[str] = field(default_factory=list)
    devices: list[Device] = field(default_factory=list)
    sections: list[str] = field(default_factory=list)   # in appearance order
    line: int = 0

    def nets(self) -> list[str]:
        seen: dict[str, None] = {}
        for p in self.ports:
            seen.setdefault(p)
        for d in self.devices:
            for n in d.nets:
                seen.setdefault(n)
        return list(seen)

    def terminals(self, net: str) -> list[tuple[Device, str]]:
        out = []
        for d in self.devices:
            for r, n in zip(d.roles, d.nets):
                if n == net:
                    out.append((d, r))
        return out

    def fanout(self, net: str) -> int:
        return len(self.terminals(net))


@dataclass
class Design:
    path: str = ""
    subckts: dict[str, Subckt] = field(default_factory=dict)
    order: list[str] = field(default_factory=list)      # definition order
    top_devices: list[Device] = field(default_factory=list)  # devices outside any .subckt
    warnings: list[str] = field(default_factory=list)

    def root(self) -> Subckt:
        """Default sheet: the subckt not instantiated by any other (last if tie)."""
        if not self.order:
            top = Subckt(name="(top)", ports=[], devices=self.top_devices)
            return top
        instantiated = set()
        for s in self.subckts.values():
            for d in s.devices:
                if d.kind == "sub":
                    instantiated.add(d.model)
        roots = [n for n in self.order if n not in instantiated]
        pick = roots[-1] if roots else self.order[-1]
        return self.subckts[pick]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=1)

    @staticmethod
    def from_json(text: str) -> "Design":
        raw = json.loads(text)
        des = Design(path=raw.get("path", ""), order=raw.get("order", []),
                     warnings=raw.get("warnings", []))
        for name, s in raw.get("subckts", {}).items():
            sub = Subckt(name=s["name"], ports=s["ports"], sections=s.get("sections", []),
                         line=s.get("line", 0))
            sub.devices = [Device(**d) for d in s["devices"]]
            des.subckts[name] = sub
        des.top_devices = [Device(**d) for d in raw.get("top_devices", [])]
        return des
