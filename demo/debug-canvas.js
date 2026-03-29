const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  const filePath = 'file://' + path.resolve(__dirname, 'index.html').replace(/\\/g, '/');
  await page.goto(filePath, { waitUntil: 'networkidle0', timeout: 15000 });
  await new Promise(r => setTimeout(r, 2000));

  // Check if function exists
  const funcs = await page.evaluate(() => ({
    startNrCanvas: typeof window.startNrCanvas,
    startLoop: typeof window.startLoop,
    startCSAC: typeof window.startCSAC,
    nrStarted: window.nrStarted,
    loopStarted: window.loopStarted,
    csacStarted: window.csacStarted,
  }));
  console.log('Functions:', JSON.stringify(funcs, null, 2));

  // Force call
  await page.evaluate(() => {
    if (typeof window.startNrCanvas === 'function') {
      window.nrStarted = false; // reset flag so it can start
      window.startNrCanvas();
    }
  });
  await new Promise(r => setTimeout(r, 3000));

  const result = await page.evaluate(() => {
    const canvas = document.getElementById('nr-canvas');
    if (!canvas) return 'canvas not found';
    const ctx = canvas.getContext('2d');
    const data = ctx.getImageData(160, 100, 1, 1).data;
    const data2 = ctx.getImageData(160, 270, 1, 1).data;
    return {
      nrStarted: window.nrStarted,
      pixel100: Array.from(data),
      pixel270: Array.from(data2),
      elapsed: 'check',
    };
  });
  console.log('Canvas state after 3s:', JSON.stringify(result, null, 2));

  await browser.close();
})();
