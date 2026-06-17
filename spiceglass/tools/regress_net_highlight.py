"""Net-highlight gate test (IMPROVEMENT_LOOP improvement 2).

Gate H1 (exactness vs the oracle): the net membership returned by
net_at() must equal the round-trip verifier's net partition. For every
labelled net on a converted sheet we click a point ON that net and assert
net_at returns EXACTLY that net's wire set — no missing segments, none
from any other net.

Also H3-ish: clicking empty space highlights nothing.

    python tools/regress_net_highlight.py
"""
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.asc.parse import parse_asc_text                # noqa: E402
from glass.web.server import AppState, net_at             # noqa: E402


def _wire_net_map(text):
    """Ground-truth partition: union-find over wires + flags, returns
    {root: set(segs)} and the flag name per root — independent re-derivation
    used to check net_at agrees on EVERY net (not just the clicked one)."""
    sheet = parse_asc_text(text)
    w = sheet.wires
    p = {}

    def find(a):
        p.setdefault(a, a)
        while p[a] != a:
            p[a] = p[p[a]]; a = p[a]
        return a

    def uni(a, b):
        p[find(a)] = find(b)
    K = lambda x, y: f"{int(x)},{int(y)}"               # noqa: E731

    def on(x, y, s):
        x1, y1, x2, y2 = s
        if x1 == x2:
            return x == x1 and min(y1, y2) <= y <= max(y1, y2)
        if y1 == y2:
            return y == y1 and min(x1, x2) <= x <= max(x1, x2)
        return False
    for (x1, y1, x2, y2) in w:
        uni(K(x1, y1), K(x2, y2))
    ends = {(s[0], s[1]) for s in w} | {(s[2], s[3]) for s in w}
    for (ex, ey) in ends:
        for s in w:
            if on(ex, ey, s):
                uni(K(ex, ey), K(s[0], s[1]))
    for (fx, fy, nm) in sheet.flags:
        uni(K(fx, fy), "NET:" + nm)
    groups = {}
    for s in w:
        groups.setdefault(find(K(s[0], s[1])), set()).add(tuple(s))
    return groups, w


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(here, ".."))
    files = sorted(glob.glob("examples/hier_*.cir")) + \
        sorted(glob.glob("examples/leaf_*.cir"))
    checked, fails = 0, []
    for f in files:
        st = AppState(os.path.abspath(f))
        text = st.bootstrap()["text"]
        groups, wires = _wire_net_map(text)
        for root, segset in groups.items():
            seg0 = next(iter(segset))             # click the 1st seg's start
            cx, cy = seg0[0], seg0[1]
            got = net_at(text, st.dir(), x=cx, y=cy)
            gotset = {tuple(s) for s in got["segments"]}
            checked += 1
            if gotset != segset:
                fails.append((os.path.basename(f), (cx, cy),
                              f"got {len(gotset)} vs truth {len(segset)}"))
        # H3: empty space -> nothing
        empty = net_at(text, st.dir(), x=999999, y=999999)
        if empty["segments"]:
            fails.append((os.path.basename(f), "empty", "highlighted nothing-space"))

    print(f"net-highlight gate H1: checked {checked} nets across {len(files)} sheets")
    if fails:
        print(f"FAIL ({len(fails)}):")
        for who, pt, err in fails[:30]:
            print(f"  {who} @ {pt}  {err}")
        return 1
    print("PASS — net_at partition == verifier-style net partition (exact); "
          "empty space highlights nothing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
