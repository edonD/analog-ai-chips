"""Structure recognition — name the motifs in a subckt.

Pure analysis (never mutates the circuit or placement): identifies analog
and digital building blocks — differential pairs, current mirrors
(+cascode/Wilson), cascode stacks, source followers, CMOS gates
(inverter / NAND / NOR), cross-coupled latches. Used for dataset
recognition labels, design reports, and as the foundation for future
structure-aware placement.

Heuristics are conservative and overlap-tolerant: a device can belong to
more than one named structure (e.g. a mirror device that is also a
cascode reference). The output is a list of {kind, devices}.
"""
from __future__ import annotations

from .classify import rails_of
from .db import Subckt


def _g(d):
    return d.net_of("g")


def _d(d):
    return d.net_of("d")


def _s(d):
    return d.net_of("s")


def recognize_structures(sub: Subckt, rails: dict | None = None) -> list[dict]:
    if rails is None:
        rails = rails_of(sub)

    def rail(n):
        return rails.get(n)
    mos = [x for x in sub.devices if x.kind in ("nmos", "pmos")]
    out: list[dict] = []

    def add(kind, devs):
        out.append({"kind": kind, "devices": sorted(d.name for d in devs)})

    # --- current mirrors: same kind + same gate + same source, >=1 diode ---
    by_gate: dict[tuple, list] = {}
    for d in mos:
        by_gate.setdefault((d.kind, _g(d), _s(d)), []).append(d)
    mirror_gates = set()
    for (kind, g, s), devs in by_gate.items():
        if len(devs) >= 2 and any(_d(x) == _g(x) for x in devs):
            add("current_mirror", devs)
            mirror_gates.add(g)

    # --- differential pairs: 2 same-kind, shared non-rail source, distinct
    #     gates and drains ---
    by_src: dict[str, list] = {}
    for d in mos:
        if _s(d) and not rail(_s(d)):
            by_src.setdefault(_s(d), []).append(d)
    for s, devs in by_src.items():
        cand = [d for d in devs]
        if len(cand) == 2 and cand[0].kind == cand[1].kind \
                and _g(cand[0]) != _g(cand[1]) and _d(cand[0]) != _d(cand[1]):
            add("diff_pair", cand)

    # --- cascode stack: A.drain -> B.source (series), same kind, B gated by
    #     a non-signal (rail / mirror gate / bias-looking) net ---
    dmap: dict[str, list] = {}
    for d in mos:
        dmap.setdefault(_d(d), []).append(d)
    for b in mos:
        lowers = [a for a in dmap.get(_s(b), []) if a is not b
                  and a.kind == b.kind]
        for a in lowers:
            add("cascode", [a, b])

    # --- source follower (common-drain): drain on a rail, gate != source,
    #     source is the output (a non-rail node) ---
    for d in mos:
        if rail(_d(d)) and not rail(_s(d)) and _g(d) != _s(d):
            add("source_follower", [d])

    # --- CMOS gates: group an NMOS pull-down net with a PMOS pull-up at the
    #     same output node ---
    nfets = [d for d in mos if d.kind == "nmos"]
    pfets = [d for d in mos if d.kind == "pmos"]
    for outn in {_d(d) for d in mos if not rail(_d(d))}:
        pn = [d for d in nfets if _d(d) == outn]
        pp = [d for d in pfets if _d(d) == outn]
        if not pn or not pp:
            continue
        # inverter: one each, shared gate (input), sources on rails
        if len(pn) == 1 and len(pp) == 1 and _g(pn[0]) == _g(pp[0]) \
                and rail(_s(pn[0])) == "gnd" and rail(_s(pp[0])) == "vdd":
            add("inverter", [pn[0], pp[0]])
            continue
        # NAND2: 2 series NMOS to gnd, 2 parallel PMOS to vdd, distinct gates
        series_n = (len(pn) == 1 and not rail(_s(pn[0]))
                    and any(_d(x) == _s(pn[0]) and rail(_s(x)) == "gnd"
                            for x in nfets))
        par_p = (len(pp) == 2 and all(rail(_s(x)) == "vdd" for x in pp)
                 and _g(pp[0]) != _g(pp[1]))
        if series_n and par_p:
            add("nand2", pp + pn + [x for x in nfets
                                    if _d(x) == _s(pn[0])])
            continue
        # NOR2: 2 parallel NMOS to gnd, 2 series PMOS from vdd
        par_n = (len(pn) == 2 and all(rail(_s(x)) == "gnd" for x in pn)
                 and _g(pn[0]) != _g(pn[1]))
        series_p = (len(pp) == 1 and not rail(_s(pp[0]))
                    and any(_d(x) == _s(pp[0]) and rail(_s(x)) == "vdd"
                            for x in pfets))
        if par_n and series_p:
            add("nor2", pn + pp + [x for x in pfets
                                   if _d(x) == _s(pp[0])])

    # --- cross-coupled latch: two devices each gated by the other's drain ---
    for i, a in enumerate(mos):
        for b in mos[i + 1:]:
            if a.kind == b.kind and _g(a) == _d(b) and _g(b) == _d(a) \
                    and _d(a) != _d(b):
                add("cross_coupled", [a, b])

    return out


def structure_kinds(sub: Subckt, rails: dict | None = None) -> list[str]:
    """Sorted unique structure kinds present (a compact recognition label)."""
    return sorted({s["kind"] for s in recognize_structures(sub, rails)})
