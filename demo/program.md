# THE LOOP — Demo Website: Agent Design Program v2

## Mission
Iterate on `demo/index.html` (and its CSS/JS modules) until it reaches world-class quality.
Target bar: NVIDIA product pages, Apple event microsites, Linear.app.

Use **Puppeteer** to screenshot the page, analyze what you see, fix the weakest thing,
re-screenshot to verify, and commit. Repeat until the quality gate is met.

---

## File Structure
```
demo/
├── index.html          # HTML structure
├── program.md          # THIS FILE — agent instructions + progress tracker
├── css/
│   ├── base.css        # Variables, reset, cursor, loader, ticker, nav
│   ├── hero.css        # LOCKED — hero section only (do NOT touch)
│   ├── scenes.css      # Per-scene backgrounds and layout
│   └── components.css  # Reusable UI components
└── js/
    ├── main.js         # Init, cursor, ticker, nav, loader
    ├── bg-three.js     # Three.js particle background
    ├── canvas-wave.js  # Scene 1 wave animation
    ├── canvas-loop.js  # Loop diagram
    ├── canvas-neuro.js # Neuro pipeline canvas
    ├── canvas-csac.js  # CSAC atomic clock canvas
    └── animations.js   # GSAP scroll triggers (no const TAU here!)
```

---

## Hero Section — LOCKED
**Never change** #s0:
- Text: "THE LOOP", eyebrow, subtitle — untouchable
- Font (Inter 900), letter-spacing, glitch effect — untouchable
- You MAY only change: bg-three.js particles, scan-line colour, gradient overlays behind text

---

## How to Use Puppeteer

### Setup (run once)
```bash
cd demo
npm init -y
npm install puppeteer
```

### Screenshot script — save as `demo/screenshot.js`
```js
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  // Load the page as a file URL
  const filePath = 'file://' + path.resolve(__dirname, 'index.html').replace(/\\/g, '/');
  await page.goto(filePath, { waitUntil: 'networkidle0', timeout: 15000 });

  const outDir = path.join(__dirname, 'screenshots');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

  // Desktop viewport
  await page.setViewport({ width: 1440, height: 900 });
  await page.waitForTimeout(2000); // let animations settle

  // Screenshot each scene by scrolling
  const scenes = [
    { id: 's0',     label: 'hero',      scrollY: 0 },
    { id: 's1',     label: 'problem',   scrollY: 900 },
    { id: 's2',     label: 'chip',      scrollY: 1800 },
    { id: 's-mems', label: 'mems',      scrollY: 2800 },
    { id: 's-neuro',label: 'neuro',     scrollY: 4200 },
    { id: 's3',     label: 'loop',      scrollY: 5400 },
    { id: 's5',     label: 'terminal',  scrollY: 6300 },
    { id: 's6',     label: 'stats',     scrollY: 7200 },
    { id: 's7',     label: 'claim',     scrollY: 8100 },
  ];

  for (const s of scenes) {
    await page.evaluate(y => window.scrollTo(0, y), s.scrollY);
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(outDir, `desktop_${s.label}.png`), fullPage: false });
    console.log(`✓ desktop_${s.label}.png`);
  }

  // Mobile viewport
  await page.setViewport({ width: 375, height: 812 });
  await page.goto(filePath, { waitUntil: 'networkidle0', timeout: 15000 });
  await page.waitForTimeout(2000);

  for (const s of scenes) {
    await page.evaluate(y => window.scrollTo(0, y), s.scrollY * 1.2);
    await page.waitForTimeout(600);
    await page.screenshot({ path: path.join(outDir, `mobile_${s.label}.png`), fullPage: false });
    console.log(`✓ mobile_${s.label}.png`);
  }

  await browser.close();
  console.log('\nAll screenshots saved to demo/screenshots/');
})();
```

### Run screenshots
```bash
node demo/screenshot.js
```

### Read screenshots
Use the Read tool on each `demo/screenshots/*.png` to visually inspect the result.

---

## Agent Workflow (repeat until quality gate met)

```
1. Run: node demo/screenshot.js
2. Read every screenshot with the Read tool
3. List what looks wrong or weak (be specific: spacing, colour, alignment, text cut off, etc.)
4. Pick the SINGLE worst problem
5. Fix it in the CSS/JS files
6. Run: node demo/screenshot.js  (re-screenshot to verify fix)
7. Read the relevant screenshot to confirm it looks better
8. Commit: git add -A && git commit -m "design: <what> — <why better>"
9. Update the Progress Tracker below
10. Go to step 1
```

---

## Design Quality Checklist

For each scene, the agent should verify:

### Global
- [ ] Top nav (frosted glass) — visible, brand + section name readable, progress bar fills on scroll
- [ ] Nav dots (right side) — visible, correct active dot highlighted
- [ ] Ticker (bottom bar) — scrolling, text readable at small size
- [ ] Film grain — subtle, not overpowering
- [ ] Cursor — custom dot + ring visible on hover
- [ ] Loader — counts to 100%, fades out smoothly before hero appears
- [ ] Section dividers — thin line between scenes (not in #s7)
- [ ] No horizontal scrollbar at any viewport width

### Scene 0 — Hero
- [ ] "THE LOOP" fills most of the viewport width
- [ ] Glitch effect fires on load and every ~4.5s
- [ ] Three.js particle field visible behind text
- [ ] Scan line sweeps before text appears
- [ ] Scroll prompt visible at bottom

### Scene 1 — Problem
- [ ] Wave canvas fills full scene background
- [ ] "10,000×" overhead number is large and red/glowing
- [ ] Three headline lines animate up into view
- [ ] Dark vignette makes text readable over wave
- [ ] Answer line ("What if the sensor was the intelligence?") visible

### Scene 2 — Chip
- [ ] Chip rings spinning, halo pulsing
- [ ] Chip image (or SVG fallback) centered, with violet glow
- [ ] Chip scan line animating
- [ ] Spec list items animate in from right
- [ ] Spec hover: cyan border + background tint + text colour change
- [ ] On mobile (375px): chip visual stacks above spec list, centered

### Scene MEMS
- [ ] Two-column layout: pipeline left, CSAC card right
- [ ] On mobile: stacks to single column cleanly
- [ ] All 5 pipeline nodes visible with icons, names, spec badges
- [ ] CSAC canvas shows atomic physics simulation (atoms, beam, PD glow)
- [ ] CSAC canvas fits within card at all widths
- [ ] CSAC data rows (frequency, stability, size, power) visible

### Scene Neuro
- [ ] Two-column: neuro canvas sticky left, specs scroll right
- [ ] Canvas shows 6 pipeline blocks animating in
- [ ] Claim card, metrics grid, prior-art gap table, phases list all visible
- [ ] Phase dots: green = complete, pulsing cyan = in progress, grey = pending
- [ ] On mobile: canvas above, specs below

### Scene 3 — The Loop
- [ ] Loop diagram canvas animates: ring → nodes → arrows → particles → "∞ RECURSIVE"
- [ ] 5 nodes visible with correct colours (violet, green, cyan, amber, red)
- [ ] Canvas is square, centered, max-width 100% on mobile

### Scene 5 — Terminal
- [ ] Terminal box has macOS-style traffic light dots
- [ ] Lines typewrite in one by one (not all at once)
- [ ] Green checkmarks and coloured text tokens visible
- [ ] Terminal box fits within scene width on mobile

### Scene 6 — Stats
- [ ] 4 cells (or 2×2 on mobile): 300µW, 10–30×, 4 classes, 0 batteries
- [ ] Numbers count up from 0 on scroll
- [ ] Hover: gradient bg + number scales up + cyan underline slides in
- [ ] Cell border with colour accent (--c variable) visible

### Scene 7 — Claim / CTA
- [ ] Large headline with gradient "hardware." text
- [ ] Body paragraph readable
- [ ] Two buttons: primary (gradient violet→cyan) + outline (transparent border)
- [ ] Primary button hover: gradient reverses direction
- [ ] On mobile: buttons stack vertically, full width

---

## Design Tokens (do not change)
```css
--void: #000000      /* page background */
--violet: #7c3aed    /* primary accent */
--violet-l: #a78bfa  /* secondary violet */
--cyan: #00d4ff      /* highlights */
--green: #00ff87     /* success, metrics */
--amber: #ffb700     /* CSAC */
--red: #ff3d5a       /* problem section */
```

---

## Known Remaining Issues (as of last review)
These are the items most likely to need attention. Check screenshots to confirm, then fix:

1. **Stats cells `--c` variable** — `.st-cell::before` uses `background: linear-gradient(90deg,transparent,var(--c),transparent)` but `--c` is never set on the cells. Each cell needs an inline `style="--c: var(--cyan)"` or similar.
2. **Terminal typewriter on mobile** — `maxWidth` animation may clip awkwardly on 375px; verify screenshot.
3. **MEMS scene on mobile** — verify CSAC canvas doesn't overflow its card container.
4. **Neuro sticky canvas** — `position:sticky; top:50%; transform:translateY(-50%)` may not work correctly inside a grid on all browsers; verify desktop screenshot.
5. **Wave canvas height** — the wave canvas is `position:absolute; inset:0` but the canvas JS may still draw at a fixed pixel size; verify scene 1 screenshot fills the viewport.
6. **Scene transitions** — check if there's visible jarring/flash between scenes when scrolling fast.
7. **Mobile nav dots** — verify they don't overlap content on 375px.
8. **Loader timing** — on slow connections (CDN fonts/scripts not cached), loader may clear before GSAP is ready; consider adding a `DOMContentLoaded` guard.
9. **`btn-o` span wrapping** — the outline button text is in a `<span>` for z-index, verify it renders correctly.
10. **Three.js on mobile** — particle field should still be visible but less dense; check hero mobile screenshot.

---

## Progress Tracker

Update this section after every commit.

| # | Issue | Status | Commit |
|---|-------|--------|--------|
| 0 | Initial modular refactor | ✅ Done | 54c0b03 / 83f6f70 |
| 1 | `const TAU` redeclaration crash (page was all black) | ✅ Fixed | — |
| 2 | Stats `--c` colour variable missing on cells | ⬜ Pending | — |
| 3 | Wave canvas pixel-size mismatch | ⬜ Pending | — |
| 4 | Neuro sticky canvas browser compat | ⬜ Pending | — |
| 5 | Terminal typewriter mobile | ⬜ Pending | — |
| 6 | MEMS mobile overflow | ⬜ Pending | — |
| 7 | Scene transition smoothness | ⬜ Pending | — |
| 8 | Mobile nav dot overlap | ⬜ Pending | — |
| 9 | Loader CDN timing guard | ⬜ Pending | — |
| 10 | Three.js mobile density | ⬜ Pending | — |

---

## Quality Gate
Done when a senior designer from Apple, NVIDIA, or Linear says "production-ready."
Until then: screenshot → analyze → fix → verify → commit → repeat.

## Commit Format
```
design: <what changed> — <why it's better>
```
