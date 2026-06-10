"""Structure recognition — maps transistor subgraphs onto composite tiles.

The placer should not have to rediscover analog relationships wire by
wire. Recognized structures become TILES: placement macros whose
defining wires (mirror gate rail, shared pair source, diode link) are
pre-routed inside the tile, exactly the way a designer draws them.
Validated approach: exact subgraph matching on SPICE netlists is the
primitive tier of ALIGN's annotation flow (Kunal et al., TCAD 2023).

Recognition order matters: pairs claim their tails first (the tail
under the pair is a stronger drawing convention than tail-as-mirror),
then gate-tied mirror banks, then pair+load composition into 5T cores,
then lone diode-connected links.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .db import Device, Subckt


@dataclass
class Tile:
    kind: str                       # 'mirror' | 'pair' | '5t' | 'diode1'
    members: list[Device]           # mirror: outputs L->R; pair: [m1, m2]
    tail: Device | None = None      # pair/5t
    loads: list[Device] = field(default_factory=list)   # 5t: above members
    diode: Device | None = None     # mirror/5t: diode-connected member
    section: str = ""
    line: int = 0

    def devices(self) -> list[Device]:
        out = list(self.members) + list(self.loads)
        if self.tail is not None:
            out.append(self.tail)
        return out


def recognize(sub: Subckt, rails: dict[str, str]) -> tuple[list[Tile], set[str]]:
    tiles: list[Tile] = []
    claimed: set[str] = set()
    mos = [d for d in sub.devices if d.kind in ("nmos", "pmos")]

    def free(d: Device) -> bool:
        return d.name not in claimed

    # ---- 1. differential pairs (+ tail): two same-kind FETs sharing a
    #         non-rail source, distinct gates, distinct drains
    by_source: dict[str, list[Device]] = {}
    for d in mos:
        s = d.net_of("s")
        if s and s not in rails:
            by_source.setdefault(s, []).append(d)
    for s, devs in by_source.items():
        cand = [d for d in devs if free(d)]
        if len(cand) != 2:
            continue
        m1, m2 = sorted(cand, key=lambda d: d.line)
        if m1.kind != m2.kind:
            continue
        if m1.net_of("g") == m2.net_of("g") or m1.net_of("d") == m2.net_of("d"):
            continue
        tail = next((t for t in mos if free(t) and t not in (m1, m2)
                     and t.net_of("d") == s), None)
        t = Tile(kind="pair", members=[m1, m2], tail=tail,
                 section=m1.section, line=m1.line)
        tiles.append(t)
        claimed.update(d.name for d in t.devices())

    # ---- 2. mirror banks: same kind + same gate net + same source net
    by_key: dict[tuple, list[Device]] = {}
    for d in mos:
        if not free(d):
            continue
        g, s = d.net_of("g"), d.net_of("s")
        if g is None or s is None:
            continue
        by_key.setdefault((d.kind, g, s), []).append(d)
    for (kind, g, s), devs in by_key.items():
        if len(devs) < 2:
            continue
        diode = next((d for d in devs if d.net_of("d") == g), None)
        ordered = sorted(devs, key=lambda d: (d is not diode, d.line))
        t = Tile(kind="mirror", members=ordered, diode=diode,
                 section=ordered[0].section, line=ordered[0].line)
        tiles.append(t)
        claimed.update(d.name for d in ordered)

    # ---- 3. compose pair + its 2-output load mirror into a 5T core
    for pt in [t for t in tiles if t.kind == "pair"]:
        dnets = {pt.members[0].net_of("d"), pt.members[1].net_of("d")}
        for mt in [t for t in tiles if t.kind == "mirror"
                   and len(t.members) == 2]:
            if mt.members[0].kind == pt.members[0].kind:
                continue                      # loads are the opposite kind
            if {m.net_of("d") for m in mt.members} != dnets:
                continue
            # align loads over the pair members by drain net
            loads = sorted(mt.members,
                           key=lambda m: 0 if m.net_of("d")
                           == pt.members[0].net_of("d") else 1)
            pt.kind = "5t"
            pt.loads = loads
            pt.diode = mt.diode
            tiles.remove(mt)
            break

    # ---- 4. lone diode-connected FETs get a drawn gate-drain link
    for d in mos:
        if free(d) and d.net_of("g") == d.net_of("d"):
            tiles.append(Tile(kind="diode1", members=[d],
                              section=d.section, line=d.line))
            claimed.add(d.name)

    return tiles, claimed
