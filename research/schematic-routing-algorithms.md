# Schematic Wire Routing: Algorithm Selection for SpiceGlass

**Research date:** 2026-06-10
**Question:** The interconnect is SpiceGlass's weak point (naive trunk-and-drop router; users hand-move wires). What is the best algorithm for aesthetic orthogonal wire routing in schematic diagrams — integer grid, fixed symbol tiles, nets of 2–6 terminals, 10–100 nets/sheet, minimal bends/crossings, deterministic, pure-Python implementable?
**Method:** Deep-research harness — 106 agents, 24 sources, 120 claims extracted, 25 adversarially verified (23 confirmed, 2 refuted).
**Baselines to beat** (`glass score`, current router): bias_generator **563 len / 19 bends / 8 crossings**; ota5 51/4/0; rms_crest_top **238/15/10**.

---

## Verdict

**Reimplement the Wybrow–Marriott–Stuckey orthogonal connector routing pipeline (GD 2009 — the algorithm inside libavoid) in pure Python.** It was the only architecture for which verification produced complete, unanimous evidence, and it matches our problem statement *exactly*: object-avoiding orthogonal connector routing against fixed shapes for interactive diagram editors.

The three stages (all from the GD 2009 paper, read in full by verifiers):

1. **Orthogonal Visibility Graph (OVG).** Project horizontal/vertical visibility lines through every obstacle corner and every connector pin; graph nodes at their intersections, edges along the lines. O(n²) nodes/edges for n obstacles, built in O(n²) (line-sweep O(n log n)). The authors' own framing bridges to EDA classics: it is *"a modification to maze running in which we use a non-uniform grid whose mesh size is tailored to the geometry of the diagram"* — Lee routing on exactly the grid lines that matter.
2. **A\* search** over **(node, entry-direction) states** carrying separate length and bend counts, with an admissible remaining-bends heuristic (enumerated as 0–4 cases). Guarantee (Theorem 2): per-connector optimal route for **any single monotonic penalty f(length, bends)** in O(n² log n). *Refuted nuance:* it is NOT "optimal in both length and bends" bi-objectively, and not global across connectors — one monotonic combined cost, per connector.
3. **Nudging.** Routes may share segments after search; a post-pass assigns pseudo-directions, builds per-shared-edge left-to-right orderings (O(e²)), then separates wires. Theorem 3: if the shared-edge graph is path-consistent, the ordering achieves the **minimal number of connector crossings** and pushes unavoidable crossings to segment ends; Theorem 4: planar shared-edge graph → planar layout. Final coordinates center wires in "alleys" via the satisfy_VPSC projection.

**The production-validated cost model** (ELK ships libavoid as its fixed-position edge router): `segmentPenalty 10` is the **only** nonzero penalty — `crossingPenalty 0`. Crossings are controlled by the nudge *ordering*, not the search. That settles our penalty weights.

## Why this one (verified evidence)

- **On-domain adoption:** Inkscape's connector tool (libavoid vendored in-tree), Dunnart, Gaphas (Python, via compiled bindings), an unnamed *commercial circuit diagram editor* (self-reported), and **Eclipse ELK**, which wraps libavoid as `org.eclipse.elk.alg.libavoid` — "Only route the edges without touching the node's positions" — precisely our fixed-tile constraint. yWorks' commercial ChannelEdgeRouter independently uses the same **route-then-nudge** two-phase pattern (path-find with overlaps allowed, then split/distribute in channels), confirming the architecture is the production standard. (Refuted: the claim that yFiles never moves nodes — 0-3. Note also yFiles' default path-finder is pattern-based, not search, with costs nodeCrossing 50 / edgeCrossing 5 / bend 1 — a cheaper option if we ever need one.)
- **Performance headroom:** C++ libavoid routes <100-node sheets "in a fraction of a second" (111 ms for a 100-node grid, 2009 hardware; 197–216 ms at 185 objects/225 connectors, 2012 hardware; 0.3–0.4 ms per connector). Even 10–100× slower in pure Python, our sheets (≤60 tiles, ≤40 nets) stay sub-second for batch; live-drag re-route is plausible but unproven (the millisecond incremental results are for the 2005 *poly-line* router; the orthogonal OVG rebuilds non-incrementally).
- **Multi-terminal nets** (our 2–6 pin case): the authors' "Orthogonal hyperedge routing" (Diagrams 2012, LNCS 7352) is the dedicated follow-up; pragmatic alternative is decomposing each net into an MST of 2-pin connectors and letting nudging merge/order shared trunks (open question — start pragmatic).
- **Skip the 2014 "1-bend visibility graph" speedup:** the authors' own benchmarks show no benefit below ~200 objects (197 vs 216 ms; its graph is *larger* there). It pays only at thousands of objects.
- **Don't bind, reimplement:** libavoid is C++ (LGPL 2.1+/commercial dual license), SWIG bindings only, no PyPI package, no pure-Python port — a clean-room reimplementation from the two papers is the practical path and keeps SpiceGlass zero-dependency.

## Coverage gaps (honest)

Only the connector-routing and framework-router angles survived adversarial verification. **Nothing survived** on the classic EDA algorithms (Lee/Mikami-Tabuchi/Hightower details, channel routing left-edge/Yoshimura-Kuh, FLUTE Steiner trees + license, PathFinder), KiCad push-and-shove internals, Graphviz ortho, mxGraph/JointJS, or the Purchase-style aesthetics studies — so this is a strong positive case for one architecture, not a verified head-to-head. The bridge to the classics is the 2009 authors' own "maze running on a non-uniform grid" remark. Open questions worth revisiting: whether plain full-grid A* (far less code) matches OVG quality at our scale, and whether nudging's VPSC projection can be replaced by exact per-alley interval-graph track assignment (classic channel-routing left-edge) — at our scale, almost certainly yes, and we already think in integer tracks.

## Implementation plan for SpiceGlass (router v2)

Keep unchanged: rail folding, label stubs, port flags, tile preroutes (become routing obstacles/claimed tracks), the geometric verifier (safety net), `glass score` (proof of improvement).

1. `glass/ovg.py` — obstacles = symbol tile bboxes (already computed for `glass score`) + sheet border; interesting lines through tile corners and pins; OVG nodes/edges with blocked-interval handling.
2. `glass/route2.py` —
   - multi-pin nets → MST decomposition into 2-pin connectors (Manhattan metric);
   - A\* over (node, entry-direction), cost = length + 10·bends (ELK's production weight), deterministic tie-breaks;
   - shared-segment detection → GD 2009 ordering (pseudo-directions + incremental insertion) → **exact per-alley track assignment by interval coloring** in whole grid units (replacing satisfy_VPSC — simpler and exact at our scale);
   - emit `Seg`s; junction dots at T-points.
3. Acceptance: `glass score` strictly improves on all three baselines (esp. crossings 8→ and 10→ low single digits), all sheets VERIFIED, batch runtime < 2 s/sheet.
4. Editor integration is automatic (server-side re-route on drag already architecture-agnostic).

## Sources

Primary (all verified 3-0 unless noted): GD 2009 paper https://users.monash.edu/~mwybrow/papers/wybrow-gd-2009.pdf · Diagrams 2014 https://users.monash.edu/~mwybrow/papers/marriott-diagrams-2014.pdf · GD 2005 https://users.monash.edu/~mwybrow/papers/wybrow-gd-2005.pdf (poly-line only) · libavoid docs https://www.adaptagrams.org/documentation/libavoid.html · repo https://github.com/mjwybrow/adaptagrams (LGPL 2.1+, pushed 2025-10-29) · ELK libavoid wrapper https://eclipse.dev/elk/reference/algorithms/org-eclipse-elk-alg-libavoid.html (segmentPenalty 10, crossingPenalty 0) · yFiles ChannelEdgeRouter https://docs.yworks.com/yfiles-html/dguide/layout/channel_edge_router.html (vendor docs).
Refuted: bi-objective optimality (1-2); yFiles fixed-node claim (0-3).
Hyperedge follow-up to acquire: Diagrams 2012, LNCS 7352, DOI 10.1007/978-3-642-31223-6_10.

**Verification stats:** 5 angles, 24 sources fetched, 120 claims extracted, 25 verified: 23 confirmed, 2 refuted.
