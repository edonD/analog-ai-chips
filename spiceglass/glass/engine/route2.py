"""Router v2 — A* over the orthogonal visibility graph + nudging.

Implements the GD 2009 Wybrow/Marriott/Stuckey pipeline (libavoid's
algorithm; see research/schematic-routing-algorithms.md):

  * per-connector A* over (node, axis) states, cost = length + 10·bends
    (ELK's production segmentPenalty; crossings are NOT in the search
    cost — production default crossingPenalty 0),
  * multi-terminal nets route pin-by-pin INTO the net's growing tree
    (route-to-net), which produces shared trunks and Steiner-like joins,
  * a nudging pass separates different nets sharing a line by exact
    integer track offsets (interval-graph greedy coloring — the
    channel-routing replacement for the paper's VPSC projection).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from heapq import heappop, heappush

from .ovg import H, V, OVG, build_ovg

BEND = 10
OFFSETS = (0, 1, -1, 2, -2, 3, -3)
# terminal-jog reaches wider (more tracks) and runs a few passes, since a
# freed track can let another stuck terminal jog (3+ nets on one line)
_JOG_OFFSETS = (1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 7, -7, 8, -8)
_JOG_PASSES = 4


@dataclass
class NetViz:
    net: str
    pins: list[tuple[int, int]] = field(default_factory=list)
    raw: list[list[tuple[int, int]]] = field(default_factory=list)
    visited: list[tuple[int, int]] = field(default_factory=list)
    cost: int = 0


@dataclass
class RouteResult:
    paths: dict[str, list[list[list[int]]]] = field(default_factory=dict)
    viz: list[NetViz] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ovg: OVG | None = None


def _heur(x: int, y: int, axis: int, goals: list[tuple[int, int]]) -> int:
    best = None
    for gx, gy in goals:
        d = abs(x - gx) + abs(y - gy)
        if d == 0:
            return 0
        if x == gx:
            c = d + (0 if axis == V else BEND)
        elif y == gy:
            c = d + (0 if axis == H else BEND)
        else:
            c = d + BEND
        if best is None or c < best:
            best = c
    return best or 0


OCCUPIED = 40       # soft cost for riding a line another net already uses
VERTEX = 200        # soft cost for landing a corner/end on a foreign net's
                    # vertex (a true touch = short; pure crossings are free)
TURN_FOREIGN = 300  # soft cost for BENDING on a foreign net's body (the
                    # corner would touch it) — cross it straight instead


def _astar(g: OVG, starts: list[tuple[int, int | None]], goal_ids: set[int],
           goal_pts: list[tuple[int, int]], occ, net: str,
           viz: NetViz | None):
    heap = []
    ctr = 0
    best: dict[tuple[int, int], int] = {}
    came: dict[tuple[int, int], tuple | None] = {}
    for nid, axis in starts:
        for ax in ((axis,) if axis is not None else (H, V)):
            heappush(heap, (_heur(*g.coords[nid], ax, goal_pts),
                            0, ctr, nid, ax, None))
            ctr += 1
    while heap:
        f, gc, _, nid, ax, par = heappop(heap)
        key = (nid, ax)
        if key in best and best[key] <= gc:
            continue
        best[key] = gc
        came[key] = par
        if viz is not None and len(viz.visited) < 600:
            viz.visited.append(g.coords[nid])
        if nid in goal_ids:
            path = []
            k = key
            while k is not None:
                path.append(g.coords[k[0]])
                k = came[k]
            return path[::-1], gc
        x, y = g.coords[nid]
        for (nb, eaxis) in g.adj[nid]:
            nx, ny = g.coords[nb]
            step = abs(nx - x) + abs(ny - y)
            ng = gc + step + (0 if eaxis == ax else BEND)
            if occ is not None:
                if occ.foreign(eaxis, x, y, nx, ny, net):
                    ng += OCCUPIED
                if occ.vertex_foreign(nx, ny, net):
                    ng += VERTEX        # don't put our corner on their vertex
                if eaxis != ax and occ.point_on_foreign(x, y, net):
                    ng += TURN_FOREIGN  # don't bend on their wire body
            nkey = (nb, eaxis)
            if nkey in best and best[nkey] <= ng:
                continue
            ctr += 1
            heappush(heap, (ng + _heur(nx, ny, eaxis, goal_pts),
                            ng, ctr, nb, eaxis, key))
    return None, None


class _Occupancy:
    """Per-line interval registry of wires already committed."""

    def __init__(self):
        self.lines: dict[tuple[int, int], list[tuple[int, int, str]]] = {}
        self.vpts: dict[tuple[int, int], set[str]] = {}   # corner/end points

    def add_seg(self, x1, y1, x2, y2, net):
        if x1 == x2 and y1 != y2:
            self.lines.setdefault((V, x1), []).append(
                (min(y1, y2), max(y1, y2), net))
        elif y1 == y2 and x1 != x2:
            self.lines.setdefault((H, y1), []).append(
                (min(x1, x2), max(x1, x2), net))
        self.vpts.setdefault((x1, y1), set()).add(net)
        self.vpts.setdefault((x2, y2), set()).add(net)

    def vertex_foreign(self, x, y, net) -> bool:
        return any(n != net for n in self.vpts.get((x, y), ()))

    def point_on_foreign(self, x, y, net) -> bool:
        """Is (x,y) anywhere on another net's wire (interior or end)?
        Turning here would put our corner on their body — a short."""
        for (a, b, n) in self.lines.get((H, y), ()):
            if n != net and a <= x <= b:
                return True
        for (a, b, n) in self.lines.get((V, x), ()):
            if n != net and a <= y <= b:
                return True
        return False

    def add_path(self, path, net):
        for a, b in zip(path, path[1:]):
            self.add_seg(a[0], a[1], b[0], b[1], net)

    def foreign(self, axis, x1, y1, x2, y2, net) -> bool:
        if axis == V:
            lo, hi = min(y1, y2), max(y1, y2)
            items = self.lines.get((V, x1), ())
        else:
            lo, hi = min(x1, x2), max(x1, x2)
            items = self.lines.get((H, y1), ())
        return any(n != net and hi > a and lo < b for (a, b, n) in items)


def _on_seg(x: int, y: int, s) -> bool:
    x1, y1, x2, y2 = s
    if x1 == x2:
        return x == x1 and min(y1, y2) <= y <= max(y1, y2)
    if y1 == y2:
        return y == y1 and min(x1, x2) <= x <= max(x1, x2)
    return False


def _compress(path: list[tuple[int, int]]) -> list[list[int]]:
    """Drop collinear intermediate points; return mutable [x,y] lists."""
    if len(path) < 2:
        return [list(p) for p in path]
    out = [list(path[0])]
    for i in range(1, len(path) - 1):
        (ax, ay), (bx, by), (cx, cy) = path[i - 1], path[i], path[i + 1]
        if (ax == bx == cx) or (ay == by == cy):
            continue
        out.append(list(path[i]))
    out.append(list(path[-1]))
    return out


class Router2:
    def __init__(self, rects, pins, bounds, debug: bool = False):
        """pins: {(x,y): escape 'L'|'R'|'U'|'D'}"""
        self.debug = debug
        pin_list = [(x, y, esc) for (x, y), esc in pins.items()]
        self.g, self.pin_nodes = build_ovg(rects, pin_list, bounds)
        self.rects = rects

    def route_all(self, jobs: list[tuple[str, list[tuple[int, int]]]],
                  existing: dict[str, list[tuple[int, int, int, int]]],
                  ) -> RouteResult:
        """jobs: (net, pin coords). existing: net -> pre-routed segments
        (tile preroutes) the router may join and must not collide with."""
        res = RouteResult(ovg=self.g if self.debug else None)
        occ = _Occupancy()
        for net, segs in existing.items():
            for (x1, y1, x2, y2) in segs:
                occ.add_seg(x1, y1, x2, y2, net)

        # deterministic order: small/local nets first
        def span(job):
            _, pts = job
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            return (max(xs) - min(xs)) + (max(ys) - min(ys))
        jobs = sorted(jobs, key=lambda j: (len(j[1]), span(j), j[0]))

        for net, pts in jobs:
            viz = NetViz(net=net, pins=list(pts))
            paths = self._route_net(net, pts, existing.get(net, []), occ, viz)
            res.paths[net] = paths
            for path in paths:
                occ.add_path(path, net)
            if self.debug:
                res.viz.append(viz)
        self._nudge(res, existing)
        return res

    # -------------------------------------------------------- per net
    def _route_net(self, net, pts, pre_segs, occ, viz):
        """Connect every pin and every PREROUTE COMPONENT into one tree.
        Preroutes can form several disconnected islands (e.g. a mirror
        gate rail and a 5T drain link on the same net) — each island is
        a cluster that must be bridged, not assumed connected."""
        g = self.g

        # ---- cluster preroute segments into islands (union-find)
        parent: dict[int, int] = {}

        def find(a):
            while parent.setdefault(a, a) != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            parent[find(a)] = find(b)

        def touches(s1, s2) -> bool:
            for (x, y) in ((s1[0], s1[1]), (s1[2], s1[3])):
                if _on_seg(x, y, s2):
                    return True
            for (x, y) in ((s2[0], s2[1]), (s2[2], s2[3])):
                if _on_seg(x, y, s1):
                    return True
            return False

        for i in range(len(pre_segs)):
            for j in range(i + 1, len(pre_segs)):
                if touches(pre_segs[i], pre_segs[j]):
                    union(i, j)

        islands: dict[int, list] = {}
        for i, s in enumerate(pre_segs):
            islands.setdefault(find(i), []).append(s)

        # ---- build cluster list: each island + each pin not on an island
        clusters: list[dict] = []
        for segs in islands.values():
            pts_set = set()
            for (x1, y1, x2, y2) in segs:
                pts_set.add((x1, y1))
                pts_set.add((x2, y2))
            clusters.append({"pts": pts_set, "segs": segs})
        pin_cluster: dict[tuple[int, int], dict] = {}
        for p in pts:
            owner = None
            for c in clusters:
                if any(_on_seg(p[0], p[1], s) for s in c["segs"]):
                    owner = c
                    break
            if owner is not None:
                owner["pts"].add(p)
            else:
                c = {"pts": {p}, "segs": []}
                clusters.append(c)
            pin_cluster[p] = owner

        def nodes_of(c) -> list[tuple[int, int | None]]:
            out = []
            for p in c["pts"]:
                nid = g.ids.get(p)
                if nid is not None:
                    axis = self._escape_axis(p) if p in self.pin_nodes else None
                    out.append((nid, axis))
            return out

        # ---- grow one tree over all clusters, nearest-first
        clusters.sort(key=lambda c: (-len(c["segs"]), sorted(c["pts"])[0]))
        tree = clusters[0]
        tree_ids = {nid for nid, _ in nodes_of(tree)}
        tree_pts = list(tree["pts"])
        paths: list[list[list[int]]] = []
        remaining = clusters[1:]
        while remaining:
            remaining.sort(key=lambda c: min(
                abs(px - tx) + abs(py - ty)
                for (px, py) in c["pts"] for (tx, ty) in tree_pts))
            c = remaining.pop(0)
            starts = nodes_of(c)
            if not starts or not tree_ids:
                viz.raw.append([])
                continue
            path, cost = _astar(g, starts, tree_ids, tree_pts, occ, net, viz)
            if path is None:
                px, py = sorted(c["pts"])[0]
                tx, ty = tree_pts[0]
                paths.append([[px, py], [px, ty], [tx, ty]])
            else:
                viz.cost += cost
                viz.raw.append(list(path))
                paths.append(_compress(path))
                for p in path:
                    nid = g.ids.get(tuple(p))
                    if nid is not None:
                        tree_ids.add(nid)
                tree_pts.extend(tuple(p) for p in path)
            tree_ids |= {nid for nid, _ in nodes_of(c)}
            tree_pts.extend(c["pts"])
        return paths

    def _escape_axis(self, pt) -> int:
        # the pin's only OVG edge defines its axis
        nid = self.pin_nodes.get(pt)
        if nid is not None and self.g.adj[nid]:
            return self.g.adj[nid][0][1]
        return V

    # -------------------------------------------------------- nudging
    def _nudge(self, res: RouteResult, existing) -> None:
        """Separate different nets sharing a visibility line: exact
        integer track offsets via greedy interval coloring per line."""
        groups: dict[tuple[int, int], list] = {}

        def add(axis, coord, lo, hi, net, seg):  # seg None = immovable
            groups.setdefault((axis, coord), []).append(
                [lo, hi, net, seg])

        for net, segs in existing.items():
            for (x1, y1, x2, y2) in segs:
                if x1 == x2:
                    add(V, x1, min(y1, y2), max(y1, y2), net, None)
                else:
                    add(H, y1, min(x1, x2), max(x1, x2), net, None)

        movable = []
        for net, paths in res.paths.items():
            for path in paths or []:
                for k in range(len(path) - 1):
                    (x1, y1), (x2, y2) = path[k], path[k + 1]
                    if x1 == x2 and y1 != y2:
                        terminal = (k == 0 or k == len(path) - 2)
                        seg = None if terminal else (path, k, V)
                        add(V, x1, min(y1, y2), max(y1, y2), net, seg)
                    elif y1 == y2 and x1 != x2:
                        terminal = (k == 0 or k == len(path) - 2)
                        seg = None if terminal else (path, k, H)
                        add(H, y1, min(x1, x2), max(x1, x2), net, seg)

        unresolved: set[str] = set()
        for (axis, coord), items in groups.items():
            items.sort(key=lambda it: (it[3] is not None, it[0]))
            taken: dict[int, list] = {}
            for it in items:
                lo, hi, net, seg = it
                placed = False
                for off in OFFSETS if seg is not None else (0,):
                    if off and self._blocked(axis, coord + off, lo, hi):
                        continue
                    # touching (shared endpoint) counts as a clash: two
                    # DIFFERENT nets meeting at a point is a short, not a
                    # junction — separate them onto distinct tracks.
                    clash = any(n2 != net and hi >= a and lo <= b
                                for (a, b, n2) in taken.get(off, ()))
                    if not clash:
                        taken.setdefault(off, []).append((lo, hi, net))
                        if off and seg is not None:
                            self._shift(res, net, seg, coord, lo, hi, off)
                        placed = True
                        break
                if not placed:
                    taken.setdefault(0, []).append((lo, hi, net))
                    unresolved.add(
                        f"nudge: could not separate '{net}' on "
                        f"{'V' if axis == V else 'H'}{coord}")
        res.warnings.extend(sorted(unresolved))
        self._jog_terminals(res, existing)

    def _jog_terminals(self, res, existing) -> None:
        """Last resort for shorts the offset pass can't fix: a TERMINAL
        segment (one end pinned) stuck on a foreign net's track. Jog it —
        a short perpendicular stub at the pin, then run the rest on a free
        track. Only fires where an overlap STILL exists, so passing sheets
        are never touched. Jogs are deferred and applied high-index-first so
        path-index references stay valid."""
        def seglines():
            lines: dict[tuple[int, int], list] = {}
            for net, segs in existing.items():
                for (x1, y1, x2, y2) in segs:
                    if x1 == x2:
                        lines.setdefault((V, x1), []).append(
                            (min(y1, y2), max(y1, y2), net, None))
                    elif y1 == y2:
                        lines.setdefault((H, y1), []).append(
                            (min(x1, x2), max(x1, x2), net, None))
            for net, paths in res.paths.items():
                for path in paths or []:
                    n = len(path)
                    for k in range(n - 1):
                        (x1, y1), (x2, y2) = path[k], path[k + 1]
                        term = (k == 0 or k == n - 2)
                        ref = (path, k, term) if term else None
                        if x1 == x2 and y1 != y2:
                            lines.setdefault((V, x1), []).append(
                                (min(y1, y2), max(y1, y2), net, ref))
                        elif y1 == y2 and x1 != x2:
                            lines.setdefault((H, y1), []).append(
                                (min(x1, x2), max(x1, x2), net, ref))
            return lines

        # iterate: a jog can free a track that lets a stuck neighbour jog
        # too (3+ nets converging on one line). Each pass rebuilds geometry.
        for _pass in range(_JOG_PASSES):
            lines = seglines()
            jogs = []                              # (path, k, axis, coord, off)
            for (axis, coord), items in list(lines.items()):
                for (lo, hi, net, ref) in items:
                    if ref is None:
                        continue
                    if not any(n2 != net and hi >= a and lo <= b
                               for (a, b, n2, _) in items):
                        continue                   # no live clash here
                    for off in _JOG_OFFSETS:       # wider than the nudge
                        if self._blocked(axis, coord + off, lo, hi):
                            continue
                        other = lines.get((axis, coord + off), [])
                        if any(n2 != net and hi >= a and lo <= b
                               for (a, b, n2, _) in other):
                            continue
                        jogs.append((ref[0], ref[1], axis, coord, off))
                        lines.setdefault((axis, coord + off), []).append(
                            (lo, hi, net, None))
                        break
            if not jogs:
                break
            # apply deepest index first per path so inserts don't invalidate
            # earlier-index jogs on the same path
            for path, k, axis, coord, off in sorted(
                    jogs, key=lambda j: (id(j[0]), -j[1])):
                n = len(path)
                if k == 0:                          # pin is path[0]
                    px, py = path[0]
                    if axis == H:
                        path[1][1] = coord + off
                        path.insert(1, [px, coord + off])
                    else:
                        path[1][0] = coord + off
                        path.insert(1, [coord + off, py])
                else:                               # pin is path[-1]
                    px, py = path[-1]
                    if axis == H:
                        path[-2][1] = coord + off
                        path.insert(n - 1, [px, coord + off])
                    else:
                        path[-2][0] = coord + off
                        path.insert(n - 1, [coord + off, py])

    @staticmethod
    def _shift(res, net, seg, coord, lo, hi, off) -> None:
        """Move a middle segment sideways and drag along any same-net
        path endpoints that T-join onto it (junction-aware nudging)."""
        path, k, ax = seg
        deps = []
        for p2 in res.paths.get(net) or []:
            for idx in (0, -1):
                pt = p2[idx]
                if pt is path[k] or pt is path[k + 1]:
                    continue
                if ax == V and pt[0] == coord and lo <= pt[1] <= hi:
                    deps.append((pt, 0))
                elif ax == H and pt[1] == coord and lo <= pt[0] <= hi:
                    deps.append((pt, 1))
        if ax == V:
            path[k][0] += off
            path[k + 1][0] += off
        else:
            path[k][1] += off
            path[k + 1][1] += off
        for pt, ci in deps:
            pt[ci] += off

    def _blocked(self, axis, coord, lo, hi) -> bool:
        for (x0, y0, x1, y1) in self.rects:
            if axis == V and x0 < coord < x1 and hi > y0 and lo < y1:
                return True
            if axis == H and y0 < coord < y1 and hi > x0 and lo < x1:
                return True
        return False
