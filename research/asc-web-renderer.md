# Rendering `.asc` schematics in the browser — architecture decision

*Date: 2026-06-15. Decision record for SpiceGlass's interactive `.asc` editor.*

We need a browser editor where the **raw `.asc` text** and the **graphical schematic**
edit each other interchangeably, and that stays smooth on complex circuits. This
records what the prior art teaches and the architecture we chose.

## What the prior art does

### KiCanvas (Thea Flowers) — the closest sibling
The best open-source web schematic renderer. KiCad, not LTspice, but the rendering
engine is directly transferable:

- **WebGL2, retained geometry, full redraw per frame.** Geometry is tessellated to
  triangles **once on load**, uploaded into GPU buffers, and the CPU arrays are
  dropped. Every frame is a full redraw, but cheap: clear, then per layer bind a
  shader, set **one 3×3 matrix uniform**, issue ~3 `drawArrays` calls. Pan/zoom
  only mutates a camera → a new matrix. No dirty-rect, no scene graph beyond a flat
  layer list.
- **Batch by primitive type, not per-object.** All polylines of a layer concatenate
  into one buffer; one draw call. A circle is a zero-length round-capped line reusing
  the line shader. Filled polygons via earcut.
- **Text = stroke-font polylines.** No `fillText`, no glyph atlas — KiCad's Hershey
  font decoded to polylines through the same line pipeline. Resolution-independent.
- **No viewport culling and no spatial index for *drawing*** — pre-baked VBOs make
  "draw everything" cheaper than traversing a tree. Hit-testing is a linear bbox scan.
- All geometry stays in **world coordinates**; world→clip happens on the GPU via
  `projection · camera` each frame. That is *why* pan/zoom is free.

### The rendering-tier evidence
- **SVG DOM** degrades past a few thousand nodes (commonly cited 3–5k; as low as
  1–2.5k once interactive). Cost scales with **node count** (style recalc, reflow,
  hit-region upkeep), not pixels. Out for the main scene at our scale; fine for a
  thin selection-handle overlay.
- **Canvas2D, batched**, handles **tens of thousands** of primitives at 60 fps
  (AG-Grid: 100k points 287 ms naive → 15.4 ms batched). Bottleneck is draw-call /
  state-change overhead, not pixels. Group draws by stroke style; layer static vs.
  dynamic; pre-render repeated symbols offscreen; integer coords; `{alpha:false}`.
- **WebGL (PixiJS v8 / regl)** is the ceiling — hundreds of thousands to millions —
  but lines must be drawn as triangle geometry (ANGLE on Windows caps `gl.LINES` at
  1 px), and text wants MSDF atlases. Much more machinery.
- **Spatial index + viewport culling is the biggest single win** and the recurring
  lesson (Lucidchart: the *spatial query*, not drawing, was the 10k-object wall; an
  R-tree made the visible-set computation >1000× faster). With culling, draw cost is
  proportional to what's **on screen**, so the same renderer that handles 1k handles
  100k as long as you only ever draw the visible window.
- **Static base + thin interactive overlay** is the universal editor pattern (Figma,
  tldraw, Excalidraw, Lucid, Miro): lift the dragged element to an overlay so the
  big base layer never repaints mid-drag.

### Bidirectional text ↔ graphics sync
- **One source of truth: the text buffer.** The parsed AST is a *derived index over
  the text*, never a parallel authoritative model — that is what makes divergence
  structurally impossible (tldraw single-store, recast lossless reprint, CodeMirror
  live-preview all do this).
- `.asc` is the friendliest possible format for this: strictly line-oriented, one
  record per line, every entity a **contiguous line range**, no nesting. So:
  - **text → graphics** is a pure full re-parse (sub-millisecond for a flat grammar;
    no tree-sitter needed). Render is the only thing worth debouncing.
  - **graphics → text** is a **minimal line patch** computed from each node's stored
    source-line index — never a whole-file re-serialize. That preserves comments,
    unknown directives (`WINDOW`, `IOPIN`, custom `SYMATTR`), ordering, whitespace.
- **Origin-tag** every mutation so a render never echoes an edit (no feedback loop),
  and patch only the changed lines so the cursor never jumps.
- **Node ids bridge both ways:** stamp an id on each drawn element and map cursor
  line ⇄ node for click-to-highlight in both panes.
- Cadence: parse+render debounced ~120 ms on typing; move on `requestAnimationFrame`
  during drag; commit exactly one line-patch on `pointerup` (= one undo step).

## Decision for SpiceGlass

**Canvas2D + retained world-space display list + uniform-grid spatial index +
viewport culling + a thin overlay, with the text buffer as the single source of
truth.**

Rationale:
- Real schematics are hundreds–to–low-thousands of primitives; our synthetic stress
  case is ~150k. Batched Canvas2D **with culling** covers both — culling makes the
  draw proportional to the visible window, which is the property that actually scales,
  and Canvas2D needs no shader/tessellation/MSDF machinery (it has native `fillText`).
  This fits the project's stdlib / no-build-tool constraint.
- We adopt KiCanvas's load-bearing ideas in Canvas2D form: **parse once → flat
  display list in world coordinates**, per frame just set the transform and draw the
  **culled** subset. WebGL/PixiJS is the documented next step *if* profiling ever
  demands it — the architecture (retained scene, culling, layers, world coords) ports
  unchanged.
- Symbol geometry (`.asy`, ours or LTspice's) lives on disk, so the **server resolves
  symbols to JSON**; the browser does parsing, rendering, culling, hit-testing, and
  the bidirectional sync entirely client-side.

### Concrete component choices
| Concern | Choice |
| --- | --- |
| Source of truth | the `.asc` text buffer; AST is a derived index over `raw_lines` |
| Parser | client-side line parser, full re-parse per change (records src line per node) |
| Renderer | Canvas2D, retained world-space display list, HiDPI, `{alpha:false}` |
| Scale | uniform-grid spatial hash → cull to viewport + broad-phase hit-test |
| Symbols | server `/api/symlib` returns parsed `.asy` geometry as JSON (cached, lazy) |
| Text → graphics | debounced (~120 ms) re-parse + re-render |
| Graphics → text | drag on rAF; on `pointerup` patch only the entity's line(s) |
| Loop/cursor safety | origin-tagged edits; line-granular patches keep the cursor put |
| Selection bridge | node id ⇄ source line; click either pane highlights the other |

Implemented in `glass/web/server.py` (server + symbol JSON), the
`glass/asc/` format layer (parse/emit) and the `glass/engine/` converter,
with the front-end in `viewer/asc_editor.html`; launched by `glass edit`.
