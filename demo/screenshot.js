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
  await new Promise(r => setTimeout(r, 2000)); // let animations settle

  // Screenshot each scene by scrolling to actual element positions
  const sceneIds = [
    { id: 's0',      label: 'hero' },
    { id: 's1',      label: 'problem' },
    { id: 's2',      label: 'chip' },
    { id: 's-mems',  label: 'mems' },
    { id: 's-neuro', label: 'neuro' },
    { id: 's3',      label: 'loop' },
    { id: 's5',      label: 'terminal' },
    { id: 's6',      label: 'stats' },
    { id: 's7',      label: 'claim' },
  ];

  // First scroll slowly through the page to trigger all ScrollTrigger animations
  const totalHeight = await page.evaluate(() => document.body.scrollHeight);
  const step = 300;
  for (let y = 0; y <= totalHeight; y += step) {
    await page.evaluate(pos => window.scrollTo(0, pos), y);
    await new Promise(r => setTimeout(r, 80));
  }
  await new Promise(r => setTimeout(r, 1500));
  // Force-start canvas animations and show all GSAP-hidden elements
  await page.evaluate(() => {
    // Force-start canvas animations if scroll triggers haven't fired
    if (typeof window.startLoop === 'function') window.startLoop();
    if (typeof window.startNrCanvas === 'function') window.startNrCanvas();
    if (typeof window.startCSAC === 'function') window.startCSAC();
    // Force all GSAP-hidden elements visible
    const hidden = document.querySelectorAll('.tl,.st-cell,.nr-claim,.nr-metrics,.nr-gap,.nr-phases,.pipe-node,#csac-card,.nr-gap-row,.nr-phase,.spec-item,.chip-img-wrap,.nr-ey,.nr-h,.nr-tag,#nr-canvas,.nr-pipe-col,#prob-over,#prob-k,#prob-ans,.prob-line-inner,#ctag,#ch1,#ch2,#loop-ey,#loop-h,#loop-p,#pfey,#pfh,#pfp,#term,#stey,#sth,#clev,#clh,#clp,#clcta,#mems-ey,#mems-h,#mems-p,#pipe-title,#csac-title');
    hidden.forEach(el => { el.style.opacity='1'; el.style.transform='none'; el.style.maxWidth='100%'; });
  });
  await new Promise(r => setTimeout(r, 2500)); // extra wait for canvas rAF
  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise(r => setTimeout(r, 500));

  const scenes = [];
  for (const s of sceneIds) {
    const scrollY = await page.evaluate(id => {
      const el = document.getElementById(id);
      if (!el) return 0;
      const rect = el.getBoundingClientRect();
      const top = rect.top + window.scrollY;
      // For neuro, scroll into the grid area so both columns are visible
      if (id === 's-neuro') {
        const grid = el.querySelector('.nr-grid');
        if (grid) {
          const gridTop = grid.getBoundingClientRect().top + window.scrollY;
          return gridTop - window.innerHeight * 0.15;
        }
        return top + window.innerHeight * 0.35;
      }
      // For other tall scenes, scroll to show middle content
      const isTall = el.offsetHeight > window.innerHeight * 1.2;
      return top + (isTall ? window.innerHeight * 0.3 : 50);
    }, s.id);
    scenes.push({ ...s, scrollY });
  }

  for (const s of scenes) {
    await page.evaluate(y => window.scrollTo(0, y), s.scrollY);
    await new Promise(r => setTimeout(r, 900));
    await page.screenshot({ path: path.join(outDir, `desktop_${s.label}.png`), fullPage: false });
    console.log(`✓ desktop_${s.label}.png`);
  }

  // Mobile viewport
  await page.setViewport({ width: 375, height: 812 });
  await page.goto(filePath, { waitUntil: 'networkidle0', timeout: 15000 });
  await new Promise(r => setTimeout(r, 2000));

  // First scroll slowly through the page to trigger all ScrollTrigger animations
  const mTotalHeight = await page.evaluate(() => document.body.scrollHeight);
  for (let y2 = 0; y2 <= mTotalHeight; y2 += 300) {
    await page.evaluate(pos => window.scrollTo(0, pos), y2);
    await new Promise(r => setTimeout(r, 80));
  }
  await new Promise(r => setTimeout(r, 1500));
  await page.evaluate(() => {
    if (typeof window.startLoop === 'function') window.startLoop();
    if (typeof window.startNrCanvas === 'function') window.startNrCanvas();
    if (typeof window.startCSAC === 'function') window.startCSAC();
    const hidden = document.querySelectorAll('.tl,.st-cell,.nr-claim,.nr-metrics,.nr-gap,.nr-phases,.pipe-node,#csac-card,.nr-gap-row,.nr-phase,.spec-item,.chip-img-wrap,.nr-ey,.nr-h,.nr-tag,.nr-pipe-col,#nr-canvas,#prob-over,#prob-k,#prob-ans,.prob-line-inner,#ctag,#ch1,#ch2,#loop-ey,#loop-h,#loop-p,#pfey,#pfh,#pfp,#term,#stey,#sth,#clev,#clh,#clp,#clcta,#mems-ey,#mems-h,#mems-p,#pipe-title,#csac-title');
    hidden.forEach(el => { el.style.opacity='1'; el.style.transform='none'; el.style.maxWidth='100%'; });
  });
  await new Promise(r => setTimeout(r, 1000));
  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise(r => setTimeout(r, 500));

  const mobileScenes = [];
  for (const s of sceneIds) {
    const scrollY = await page.evaluate(id => {
      const el = document.getElementById(id);
      if (!el) return 0;
      const rect = el.getBoundingClientRect();
      const top = rect.top + window.scrollY;
      if (id === 's-neuro') {
        const grid = el.querySelector('.nr-grid');
        if (grid) {
          const gridTop = grid.getBoundingClientRect().top + window.scrollY;
          return gridTop - window.innerHeight * 0.1;
        }
        return top + window.innerHeight * 0.35;
      }
      const isTall = el.offsetHeight > window.innerHeight * 1.2;
      return top + (isTall ? window.innerHeight * 0.3 : 50);
    }, s.id);
    mobileScenes.push({ ...s, scrollY });
  }

  for (const s of mobileScenes) {
    await page.evaluate(y => window.scrollTo(0, y), s.scrollY);
    await new Promise(r => setTimeout(r, 700));
    await page.screenshot({ path: path.join(outDir, `mobile_${s.label}.png`), fullPage: false });
    console.log(`✓ mobile_${s.label}.png`);
  }

  await browser.close();
  console.log('\nAll screenshots saved to demo/screenshots/');
})();
