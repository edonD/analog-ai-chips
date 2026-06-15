"""Placement optimization — reorder the left-to-right objects (tiles and
series columns) to minimise wire crossings, fully transparently.

Readability of a schematic is dominated by CROSSINGS (graph-drawing
aesthetics: crossings worst, then bends, then length). The analog
conventions are already fixed upstream — rails fold to stubs, recognized
structures are tiles, every branch is a vertical column. The biggest
remaining freedom is the ORDER of those columns/tiles along the x-axis.

In a linear (left-to-right) arrangement, two nets cross exactly when
their column-spans INTERLEAVE (a < c < b < d). That is an exact,
routing-free proxy for inter-column crossings, computable in
microseconds, so we can search many orderings. We also keep a soft
"section contiguity" term so the netlist's functional clustering (the
LLM's section comments — a real readability cue) survives.

Every step the search takes is appended to a `trace` list, so the whole
optimisation is inspectable: seed cost, each improving candidate, and the
winner, with the crossing / wirelength / section-break breakdown.
"""
from __future__ import annotations

import itertools
import math

W_CROSS, W_BREAK, W_HPWL = 1000, 50, 1     # crossings dominate the scalar


def _devs(o):
    kind, val = o
    return val.devices() if kind == "tile" else val


def _label(o):
    kind, val = o
    devs = val.members if kind == "tile" else val
    nm = "/".join(d.name for d in devs[:3]) + ("…" if len(devs) > 3 else "")
    return ("T:" if kind == "tile" else "") + nm


def _section(o):
    kind, val = o
    d = val.members[0] if kind == "tile" else val[0]
    return d.section or ""


def _nets(o, rails, label_nets):
    nets = set()
    for d in _devs(o):
        for n in d.nets:
            if n and n not in rails and n not in label_nets:
                nets.add(n)
    return nets


def cost(order, onets, osec):
    """(crossings, hpwl, section_breaks) for a left-to-right ordering."""
    pos: dict[str, list[int]] = {}
    for i, o in enumerate(order):
        for n in onets[id(o)]:
            pos.setdefault(n, []).append(i)
    spans = [(min(p), max(p)) for p in pos.values() if max(p) > min(p)]
    hpwl = sum(b - a for a, b in spans)
    cr = 0
    for i in range(len(spans)):
        a1, b1 = spans[i]
        for j in range(i + 1, len(spans)):
            a2, b2 = spans[j]
            if a1 < a2 < b1 < b2 or a2 < a1 < b2 < b1:
                cr += 1
    seen, breaks, prev = set(), 0, None
    for o in order:
        s = osec[id(o)]
        if s != prev and s in seen:
            breaks += 1
        seen.add(s); prev = s
    return {"crossings": cr, "hpwl": hpwl, "section_breaks": breaks}


def _scalar(c):
    return W_CROSS * c["crossings"] + W_BREAK * c["section_breaks"] \
        + W_HPWL * c["hpwl"]


def optimize_order(objects, rails, label_nets, trace=None):
    """Return a reordered copy of `objects` with fewer crossings. Appends
    a human-readable decision log to `trace` (a list of strings)."""
    n = len(objects)
    if n < 2:
        return list(objects)
    onets = {id(o): _nets(o, rails, label_nets) for o in objects}
    osec = {id(o): _section(o) for o in objects}
    idx = {id(o): i for i, o in enumerate(objects)}

    def order_idx(order):
        return [idx[id(o)] for o in order]

    def log(m):
        if trace is not None:
            trace.append(m)

    seed = list(objects)
    sc = cost(seed, onets, osec)
    log("objects (left->right seed):")
    for i, o in enumerate(objects):
        nets = sorted(onets[id(o)])
        log(f"  [{i}] {_label(o):22} sec={osec[id(o)] or '-':10} "
            f"nets={','.join(nets[:6])}{'…' if len(nets) > 6 else ''}")
    log(f"seed cost: crossings={sc['crossings']} hpwl={sc['hpwl']} "
        f"section_breaks={sc['section_breaks']}  (scalar {_scalar(sc)})")

    best, bestc, bests = seed, sc, _scalar(sc)
    if n <= 7:
        total = math.factorial(n)
        log(f"search: exhaustive over {total} orderings of {n} objects")
        for perm in itertools.permutations(objects):
            c = cost(perm, onets, osec); s = _scalar(c)
            if s < bests:
                best, bestc, bests = list(perm), c, s
                log(f"  improve -> {order_idx(best)}  "
                    f"crossings={c['crossings']} hpwl={c['hpwl']} "
                    f"breaks={c['section_breaks']}")
    else:
        log(f"search: greedy relocation on {n} objects (n!>5040)")
        improved = True
        while improved:
            improved = False
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    cand = best[:]; o = cand.pop(i); cand.insert(j, o)
                    c = cost(cand, onets, osec); s = _scalar(c)
                    if s < bests:
                        best, bestc, bests = cand, c, s
                        improved = True
                        log(f"  move {_label(o)} -> slot {j}  "
                            f"crossings={c['crossings']} hpwl={c['hpwl']}")
                        break
                if improved:
                    break
    log(f"BEST order {order_idx(best)}: crossings={bestc['crossings']} "
        f"hpwl={bestc['hpwl']} section_breaks={bestc['section_breaks']}  "
        f"(seed was {sc['crossings']}/{sc['hpwl']}/{sc['section_breaks']})")
    return best
