/* ─── ANIMATIONS ─── */
const TAU = Math.PI*2;

gsap.registerPlugin(ScrollTrigger);

/* ─── OPENING SEQUENCE ─── */
function startOpening(){
  const tl = gsap.timeline();

  // scan line sweeps down
  tl.set('#scan-line', { opacity:1, top:'-2px' })
    .to('#scan-line', { top:'102%', duration:1.1, ease:'power1.inOut' })
    .to('#scan-line', { opacity:0, duration:0.2 }, '-=0.2')

  // eyebrow
    .to('#ey0', { opacity:1, y:0, duration:0.7, ease:'power2.out' }, '-=0.5')

  // characters fly in
    .to(['#hc0','#hc1','#hc2','#hc3','#hc4','#hc5','#hc6'], {
      opacity:1, y:0, rotate:0, filter:'blur(0px)',
      duration:0.6, stagger:0.07, ease:'back.out(1.4)'
    }, '-=0.3')

  // glitch effect
    .call(() => {
      const g = document.getElementById('glitch-title');
      g.classList.add('glitching');
      setTimeout(() => g.classList.remove('glitching'), 360);
    }, null, '+=0.1')

  // subtitle
    .to('#hero-sub', { opacity:1, y:0, duration:0.8, ease:'power2.out' }, '+=0.1')
    .to('#scroll-p', { opacity:1, duration:0.6 }, '+=0.3');

  // periodic glitch
  setInterval(() => {
    const g = document.getElementById('glitch-title');
    g.classList.add('glitching');
    setTimeout(() => g.classList.remove('glitching'), 350);
  }, 4500);
}

/* ─── GSAP INITIAL STATES ─── */
gsap.set(['#ey0','#hero-sub','#scroll-p'], {opacity:0, y:15});
gsap.set('.hero-char', {opacity:0, y:60, rotate:4, filter:'blur(8px)'});

gsap.set(['#prob-over','#prob-k','#prob-ans'], {opacity:0, y:12});
gsap.set(['.prob-line-inner'], {y:'115%'});

gsap.set(['#ctag','#ch1','#ch2'], {opacity:0, x:25});
gsap.set('.spec-item', {opacity:0, x:18});
gsap.set('#chip-wrap', {opacity:0, scale:0.85, y:20});

gsap.set(['#nr-ey','#nr-h','#nr-tag'], {opacity:0, y:12});
gsap.set(['#nr-claim','#nr-metrics','#nr-gap','#nr-phases'], {opacity:0, x:22});
gsap.set(['.nr-gap-row'], {opacity:0, x:14});
gsap.set(['.nr-phase'], {opacity:0, x:12});

gsap.set(['#mems-ey','#mems-h','#mems-p'], {opacity:0, y:12});
gsap.set(['#pipe-title','#csac-title'], {opacity:0});
gsap.set(['.pipe-node'], {opacity:0, x:-18});
gsap.set('#csac-card', {opacity:0, y:22});

gsap.set(['#loop-ey','#loop-h','#loop-p'], {opacity:0, y:12});
gsap.set(['#pfey','#pfh','#pfp'], {opacity:0, y:12});
gsap.set('#term', {opacity:0, y:35});
gsap.set('.tl', {opacity:0, x:0});
gsap.set(['#stey','#sth'], {opacity:0, y:12});
gsap.set('.st-cell', {opacity:0, y:18});
gsap.set(['#clev','#clh','#clp','#clcta'], {opacity:0, y:15});

/* ─── SCROLL TRIGGERS ─── */
function on(trigger, fn, start='top 58%'){
  ScrollTrigger.create({ trigger, start, once:true, onEnter:fn });
}

// Neuro scene
on('#s-neuro', ()=>{
  const tl=gsap.timeline();
  tl.to(['#nr-ey','#nr-h','#nr-tag'],{opacity:1,y:0,duration:0.6,stagger:0.1,ease:'power2.out'})
    .call(startNrCanvas, null, '+=0.2')
    .to('#nr-claim',   {opacity:1,x:0,duration:0.6,ease:'power2.out'}, '+=0.1')
    .to('#nr-metrics', {opacity:1,x:0,duration:0.6,ease:'power2.out'}, '-=0.3')
    .to('#nr-gap',     {opacity:1,x:0,duration:0.5}, '-=0.3')
    .to('.nr-gap-row', {opacity:1,x:0,duration:0.4,stagger:0.1,ease:'power2.out'}, '-=0.2')
    .to('#nr-phases',  {opacity:1,x:0,duration:0.5}, '-=0.2')
    .to('.nr-phase',   {opacity:1,x:0,duration:0.4,stagger:0.1,ease:'power2.out'}, '-=0.2');
}, 'top 55%');

// MEMS scene
on('#s-mems', ()=>{
  const tl=gsap.timeline();
  tl.to(['#mems-ey','#mems-h','#mems-p'],{opacity:1,y:0,duration:0.6,stagger:0.1,ease:'power2.out'})
    .to('#pipe-title',{opacity:1,duration:0.5},'-=0.1')
    .to('#csac-title',{opacity:1,duration:0.5},'-=0.4')
    .to('.pipe-node',{opacity:1,x:0,duration:0.5,stagger:0.18,ease:'power2.out'},'-=0.1')
    .to('#csac-card',{opacity:1,y:0,duration:0.7,ease:'power2.out'},'-=0.5')
    .call(startCSAC, null, '+=0.2');
}, 'top 55%');

// S1
on('#s1', ()=>{
  const tl=gsap.timeline();
  tl.to('#prob-over', {opacity:1,y:0,duration:0.8,ease:'power3.out'})
    .to('#prob-k', {opacity:1,y:0,duration:0.5},'-=0.3')
    .to('#pl0',{y:'0%',duration:0.65,ease:'power3.out'},'-=0.2')
    .to('#pl1',{y:'0%',duration:0.65,ease:'power3.out'},'-=0.38')
    .to('#pl2',{y:'0%',duration:0.65,ease:'power3.out'},'-=0.38')
    .to('#prob-ans',{opacity:1,y:0,duration:0.7,ease:'power2.out'},'+=0.12');
});

// S2
on('#s2', ()=>{
  gsap.to('#chip-wrap',{opacity:1,scale:1,y:0,duration:1.1,ease:'power2.out'});
  const tl=gsap.timeline({delay:0.25});
  tl.to('#ctag',{opacity:1,x:0,duration:0.5,ease:'power2.out'})
    .to('#ch1', {opacity:1,x:0,duration:0.6,ease:'power3.out'},'-=0.25')
    .to('#ch2', {opacity:1,x:0,duration:0.5},'-=0.3')
    .to('.spec-item',{opacity:1,x:0,duration:0.4,stagger:0.07,ease:'power2.out'},'-=0.2');
});

// S3
on('#s3', ()=>{
  const tl=gsap.timeline();
  tl.to('#loop-ey',{opacity:1,y:0,duration:0.5})
    .to('#loop-h', {opacity:1,y:0,duration:0.6,ease:'power2.out'},'-=0.25')
    .to('#loop-p', {opacity:1,y:0,duration:0.5},'-=0.2')
    .call(startLoop,null,'+=0.3');
});

// S5 — typewriter per terminal line
on('#s5', ()=>{
  const tl=gsap.timeline();
  tl.to(['#pfey','#pfh','#pfp'],{opacity:1,y:0,duration:0.5,stagger:0.1})
    .to('#term',{opacity:1,y:0,duration:0.7,ease:'power2.out'},'-=0.1');

  // typewriter: each line appears then "types" by expanding width
  const lines = document.querySelectorAll('.tl');
  lines.forEach((ln, i) => {
    // set each line: visible but clipped at width:0
    gsap.set(ln, { opacity:1, x:0, overflow:'hidden', whiteSpace:'nowrap', maxWidth:'0%' });
    tl.to(ln, {
      maxWidth:'100%',
      duration: 0.35 + ln.textContent.trim().length * 0.004,
      ease:'steps(30)',
      delay: i === 0 ? 0.15 : 0,
    }, `>+${i===0 ? 0 : 0.05}`);
  });

  // after last line, re-allow wrapping for readability on narrow screens
  tl.call(()=>{
    lines.forEach(ln=>{ ln.style.whiteSpace=''; ln.style.maxWidth=''; });
  });
});

// S6
on('#s6', ()=>{
  gsap.to(['#stey','#sth'],{opacity:1,y:0,duration:0.6,stagger:0.1});
  gsap.to('.st-cell',{opacity:1,y:0,duration:0.6,stagger:0.1,delay:0.25,ease:'power2.out'});
  setTimeout(()=>{
    document.querySelectorAll('.cnt').forEach(el=>{
      const target=parseInt(el.dataset.t);
      const start=performance.now();
      const dur=target===0?300:1600;
      (function tick(now){
        const t=Math.min(1,(now-start)/dur);
        const e=1-Math.pow(1-t,3);
        el.textContent=Math.round(e*target);
        if(t<1) requestAnimationFrame(tick);
      })(performance.now());
    });
  },500);
});

// S7
on('#s7', ()=>{
  gsap.to(['#clev','#clh','#clp','#clcta'],{opacity:1,y:0,duration:0.7,stagger:0.15,ease:'power2.out'});
});
