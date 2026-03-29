# THE LOOP — Demo Website: Agent Design Program

## Mission
Iterate on `demo/index.html` (and its CSS/JS modules) until it reaches an absolutely professional,
world-class standard. Think NVIDIA product pages, Apple event microsites, Linear.app —
that level of craft.

## File Structure
```
demo/
├── index.html          # HTML structure
├── css/
│   ├── base.css        # Variables, reset, chrome (cursor, loader, ticker, nav)
│   ├── hero.css        # LOCKED — hero section only
│   ├── scenes.css      # Per-scene backgrounds and layout
│   └── components.css  # Reusable UI components
└── js/
    ├── main.js         # Init, cursor, ticker, nav, loader
    ├── bg-three.js     # Three.js particle background
    ├── canvas-wave.js  # Scene 1 wave
    ├── canvas-loop.js  # Loop diagram
    ├── canvas-neuro.js # Neuro pipeline
    ├── canvas-csac.js  # CSAC atomic clock
    └── animations.js   # GSAP scroll triggers
```

## Hero Section — LOCKED
**Do NOT change** the hero (#s0):
- The text: "THE LOOP", the eyebrow, the subtitle — untouchable
- The font (Inter 900), letter-spacing, line-height — untouchable
- The glitch effect logic — untouchable
- The scroll prompt — untouchable

**You MAY improve** only:
- The Three.js background (`bg-three.js`) — particle density, motion, color palette
- The scan-line colour or timing
- The gradient overlays behind the text

## What "Professional" Means Here
- **Typography**: perfect hierarchy — one clear reading rhythm from eyebrow → title → subtitle → body
- **Spacing**: 8px grid, generous whitespace, no crowded sections
- **Colour**: the palette (violet/cyan/green/amber) is set — use it with restraint, not excess
- **Animation**: every motion is purposeful — reveals are clean, not flashy
- **Cards**: consistent border-radius, consistent padding, consistent glow strategy
- **Responsiveness**: every scene must work at 375px mobile width
- **Performance**: no layout jank, canvas loops are efficient

## Iteration Rules
1. **One focused improvement per iteration** — pick the weakest section, fix it, commit
2. **Never break what works** — test that the page still loads after each change
3. **Real content only** — all text is real technical content, never change specs or labels
4. **Commit format**: `design: <what changed> — <why it's better>`
5. **After each commit** — note what the next weakest element is

## Current Known Issues to Fix (Priority Order)
1. Scene 1 (Problem) — wave canvas + text layout can be tighter and more dramatic
2. Scene 2 (Chip) — chip visual alignment on mobile needs work; spec list could have better hover states
3. Scene MEMS (pipeline + CSAC) — the two-column layout collapses poorly on narrow screens
4. Scene Neuro — the sticky pipeline canvas needs `position:sticky` refinement
5. Scene 5 (Terminal) — terminal could use a subtle typewriter-style entrance per line
6. Scene 6 (Stats) — stat cells need hover animations that feel more premium
7. Scene 7 (Claim) — the final CTA buttons could be more refined
8. Global — add a thin frosted-glass top navigation bar showing current section name
9. Global — scene transitions: add subtle parallax on section backgrounds
10. Global — mobile: test and fix every breakpoint

## Design Tokens (do not change these)
```css
--void: #000000        /* page background */
--violet: #7c3aed      /* primary accent */
--violet-l: #a78bfa    /* secondary violet */
--cyan: #00d4ff        /* highlights, links */
--green: #00ff87       /* success, metrics */
--amber: #ffb700       /* CSAC, warnings */
--red: #ff3d5a         /* problem section */
```

## Canvas Animations — Improvement Areas
- `bg-three.js`: try adding grid lines between close particles (like a neural net), vary sizes more
- `canvas-loop.js`: make the node pulse animations react to mouse position (parallax)
- `canvas-csac.js`: the photon beam absorption is good — ensure atom count stabilises (not all absorb)
- `canvas-neuro.js`: add a faint background grid to the pipeline canvas

## Quality Gate
The page is "done" when a senior designer from Apple, NVIDIA, or Linear would look at it
and say "this feels production-ready." Until then, keep iterating.

## How to Run
Open `demo/index.html` directly in a browser. No build step required.
All dependencies are CDN-loaded (GSAP, Three.js, Google Fonts).
