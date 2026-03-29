/* ─── WAVE CANVAS (scene 1) ─── */
(function(){
  const canvas = document.getElementById('wave-c');
  const ctx = canvas.getContext('2d');
  let W,H,t=0;
  function resize(){
    const parent = canvas.parentElement;
    W = canvas.width  = parent ? parent.offsetWidth  : window.innerWidth;
    H = canvas.height = parent ? parent.offsetHeight : window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);
  if (typeof ResizeObserver !== 'undefined') {
    new ResizeObserver(resize).observe(canvas.parentElement || document.body);
  }
  function draw(){
    requestAnimationFrame(draw);
    t+=0.012;
    ctx.clearRect(0,0,W,H);

    const waves = [
      {freq:1.8,  amp:70, color:'rgba(0,212,255,',   offset:0,    lw:2.5},
      {freq:3.2,  amp:45, color:'rgba(124,58,237,',  offset:1.1,  lw:2},
      {freq:5.6,  amp:28, color:'rgba(0,255,135,',   offset:2.3,  lw:1.5},
      {freq:2.4,  amp:35, color:'rgba(255,61,90,',   offset:3.7,  lw:1.5},
    ];

    waves.forEach(w=>{
      ctx.beginPath();
      for(let x=0;x<=W;x+=2){
        const y = H/2 + Math.sin(x/W*Math.PI*2*w.freq + t + w.offset)*w.amp
                      + Math.sin(x/W*Math.PI*4*w.freq + t*1.3 + w.offset)*w.amp*0.4;
        x===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
      }
      const grad = ctx.createLinearGradient(0,0,W,0);
      grad.addColorStop(0,  w.color+'0)');
      grad.addColorStop(0.12,w.color+'1)');
      grad.addColorStop(0.88,w.color+'1)');
      grad.addColorStop(1,  w.color+'0)');
      ctx.strokeStyle=grad; ctx.lineWidth=w.lw; ctx.stroke();
    });
  }
  draw();
})();
