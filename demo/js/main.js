/* ─── CURSOR ─── */
const cur = document.getElementById('cursor');
const curR = document.getElementById('cursor-ring');
let mx=0,my=0,rx=0,ry=0;
document.addEventListener('mousemove', e => { mx=e.clientX; my=e.clientY });
(function curLoop(){
  requestAnimationFrame(curLoop);
  cur.style.left = mx+'px'; cur.style.top = my+'px';
  rx += (mx-rx)*0.12; ry += (my-ry)*0.12;
  curR.style.left = rx+'px'; curR.style.top = ry+'px';
})();

/* ─── TICKER ─── */
const items = [
  'SkyWater SKY130A · 130nm Open-Source PDK',
  'Always-on power: 300 µW',
  'Designed by Claude (Anthropic LLM)',
  '5× Gm-C Band-Pass Filters · 100Hz–20kHz',
  'Charge-Domain MAC Classifier',
  '4-Class Bearing Fault Detection',
  '10–30× more efficient than MCU + FFT',
  'Folded-Cascode OTA · 67dB · 5 PVT corners',
  'Zero batteries required',
  'Kurzweil · Bostrom · Tegmark · AlphaChip',
  'MEMS SiN Membrane · 50µm · 5 MHz · Q>100',
  'Optical Ring Resonator · g_om > 1 GHz/nm · Q=50k',
  'Hopf Feedback Amplifier · Near-Bifurcation · <1mW · SKY130',
  'LIF Neuromorphic Encoder · <500µW · No ADC · Spike Train',
  'Rb-87 CSAC · Chip-Scale Atomic Clock · ±50ppb · MEMS Vapor Cell',
  '6.835 GHz Hyperfine Lock · GPS-Denied Navigation · 17cm³',
  'Analog AI Inference at the Edge',
  'Phase margin >56° worst-case corner',
  'MDP < 1 mPa·Hz⁻¹/² · Ultrasound Sensing Target',
];
const track = document.getElementById('ticker');
const html = items.map(t => `<span class="ticker-item"><span class="ticker-dot"></span>${t}</span>`).join('');
track.innerHTML = html + html; // duplicate for seamless loop

/* ─── LOADER ─── */
const loaderFill = document.getElementById('loader-fill');
const loaderPct  = document.getElementById('loader-pct');
const loaderEl   = document.getElementById('loader');

let loadVal = 0;
let pageLoaded = false;

// Only complete the loader after window.load fires (all scripts ready)
window.addEventListener('load', () => { pageLoaded = true; });

const loadTick = setInterval(() => {
  loadVal += Math.random() * 18 + 4;
  if (loadVal >= 100) {
    loadVal = 100;
    loaderFill.style.width = '100%';
    loaderPct.textContent = 'INITIALIZING 100%';
    clearInterval(loadTick);

    // Wait for window.load before starting GSAP animations
    const finishLoader = () => {
      setTimeout(() => {
        gsap.to(loaderEl, { opacity:0, duration:0.6, ease:'power2.in',
          onComplete: () => { loaderEl.style.display='none'; startOpening(); }
        });
      }, 220);
    };

    if (pageLoaded) {
      finishLoader();
    } else {
      window.addEventListener('load', finishLoader, { once: true });
    }
    return;
  }
  loaderFill.style.width = loadVal + '%';
  loaderPct.textContent = `INITIALIZING ${Math.floor(loadVal)}%`;
}, 60);

/* ─── PROGRESS BAR ─── */
gsap.to('#progress', {
  scaleX:1, ease:'none',
  scrollTrigger:{ scrub:0.3, start:'top top', end:'bottom bottom' }
});

/* ─── NAV DOTS + TOP NAV SECTION NAME ─── */
const allScenes = document.querySelectorAll('[data-s]');
const allDots   = document.querySelectorAll('.nav-dot');

// Section name map for the top nav
const sectionNames = {
  '0': 'Hero',
  '1': 'The Problem',
  '2': 'VibroSense-1',
  'm': 'MEMS Pipeline',
  'n': 'Neuro MEMS',
  '3': 'The Loop',
  '5': 'AI Design',
  '6': 'By the Numbers',
  '7': 'The Future',
};
const tnSection = document.getElementById('tn-section');

allScenes.forEach(sc => {
  new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting && e.intersectionRatio > 0.35) {
        allDots.forEach(d=>d.classList.remove('active'));
        const d = document.querySelector(`.nav-dot[data-s="${e.target.dataset.s}"]`);
        if(d) d.classList.add('active');
        // update top nav label
        if(tnSection) tnSection.textContent = sectionNames[e.target.dataset.s] || '';
      }
    });
  }, { threshold:0.35 }).observe(sc);
});
allDots.forEach(d => d.addEventListener('click', () => {
  document.querySelector(`[data-s="${d.dataset.s}"]`).scrollIntoView({behavior:'smooth'});
}));

/* ─── TOP NAV SCROLL PROGRESS ─── */
const tnProgress = document.getElementById('tn-progress');
window.addEventListener('scroll', () => {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
  if(tnProgress) tnProgress.style.width = pct + '%';
}, { passive: true });
