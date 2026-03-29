/* ─── NEURO PIPELINE CANVAS ─── */
const TAU = Math.PI*2;

let nrStarted = false;
window.startNrCanvas = function startNrCanvas(){
  if(nrStarted) return; nrStarted = true;
  const canvas = document.getElementById('nr-canvas');
  if(!canvas) return;
  const ctx = canvas.getContext('2d');
  const W=320, H=540;

  const stages = [
    { label:'ACOUSTIC INPUT', sub:'1–10 MHz ultrasound', col:'rgba(255,255,255,', icon:'~' },
    { label:'SiN MEMBRANE',   sub:'50µm · f₀=5MHz · Q>100', col:'rgba(0,212,255,', icon:'◎' },
    { label:'RING RESONATOR', sub:'Q=50k · g_om>1GHz/nm', col:'rgba(167,139,250,', icon:'⬡' },
    { label:'HOPF AMPLIFIER', sub:'SKY130 · µ≈−0.05 · <1mW', col:'rgba(0,255,135,', icon:'⚡' },
    { label:'LIF NEURON',     sub:'<500µW · Spike train · No ADC', col:'rgba(255,61,90,', icon:'◆' },
    { label:'SNN BACKEND',    sub:'Digital · Zero ADC pipeline', col:'rgba(255,183,0,', icon:'⬡' },
  ];

  const BLOCK_H = 56;
  const BLOCK_W = 260;
  const BX = (W-BLOCK_W)/2;
  const GAP = (H - stages.length*BLOCK_H) / (stages.length-1);
  const FULL_H = BLOCK_H + GAP;

  // flowing particles
  const particles = [];
  for(let s=0;s<5;s++){
    for(let p=0;p<4;p++){
      particles.push({ seg:s, t: (p/4), speed:0.004+Math.random()*0.003 });
    }
  }

  const startTime = performance.now();

  function ease(t){ return t<0.5?2*t*t:-1+(4-2*t)*t }

  function drawBlock(i, progress){
    const y = i*FULL_H;
    const st = stages[i];
    const alpha = Math.min(1, progress*2);
    const scaleX = ease(Math.min(1, progress));

    ctx.save();
    ctx.translate(BX + BLOCK_W/2, y + BLOCK_H/2);
    ctx.scale(scaleX, 1);
    ctx.translate(-(BLOCK_W/2), -(BLOCK_H/2));

    // bg
    ctx.beginPath();
    roundRect(ctx, 0, 0, BLOCK_W, BLOCK_H, 8);
    ctx.fillStyle = st.col+'0.07)';
    ctx.fill();
    // border
    ctx.beginPath();
    roundRect(ctx, 0, 0, BLOCK_W, BLOCK_H, 8);
    ctx.strokeStyle = st.col+(0.4*alpha)+')';
    ctx.lineWidth = 1.2;
    ctx.stroke();

    // icon circle
    ctx.beginPath();
    ctx.arc(24, BLOCK_H/2, 14, 0, TAU);
    ctx.fillStyle = st.col+'0.15)';
    ctx.fill();
    ctx.font = "600 14px 'Inter',sans-serif";
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillStyle = st.col+(0.9*alpha)+')';
    ctx.fillText(st.icon, 24, BLOCK_H/2);

    // label
    ctx.font = "700 10.5px 'Inter',sans-serif";
    ctx.textAlign='left'; ctx.textBaseline='top';
    ctx.fillStyle = `rgba(255,255,255,${alpha})`;
    ctx.fillText(st.label, 46, 12);

    // sub
    ctx.font = "400 9px 'JetBrains Mono',monospace";
    ctx.fillStyle = st.col+(0.55*alpha)+')';
    ctx.fillText(st.sub, 46, 28);

    ctx.restore();
  }

  function roundRect(ctx,x,y,w,h,r){
    ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);
    ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);
    ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);
    ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();
  }

  function frame(){
    const elapsed = (performance.now()-startTime)/1000;
    ctx.clearRect(0,0,W,H);

    // draw blocks
    stages.forEach((st,i)=>{
      const revealTime = i*0.22;
      const progress = Math.max(0, Math.min(1,(elapsed-revealTime)/0.4));
      if(progress>0) drawBlock(i, progress);
    });

    // draw connector lines
    for(let i=0;i<stages.length-1;i++){
      const revealTime = (i+0.5)*0.22;
      const lt = Math.max(0, Math.min(1,(elapsed-revealTime)/0.3));
      if(lt<=0) continue;
      const x = W/2;
      const y0 = i*FULL_H + BLOCK_H;
      const y1 = y0 + GAP*ease(lt);
      const g = ctx.createLinearGradient(x,y0,x,y1);
      g.addColorStop(0, stages[i].col+'0.5)');
      g.addColorStop(1, stages[i+1].col+'0.5)');
      ctx.beginPath();ctx.moveTo(x,y0);ctx.lineTo(x,y1);
      ctx.strokeStyle=g;ctx.lineWidth=1.5;
      ctx.setLineDash([4,3]);ctx.stroke();ctx.setLineDash([]);

      // arrow tip
      if(lt>0.9){
        const fa=(lt-0.9)/0.1;
        ctx.beginPath();
        ctx.moveTo(x,y1);ctx.lineTo(x-5,y1-8);ctx.lineTo(x+5,y1-8);ctx.closePath();
        ctx.fillStyle=stages[i+1].col+(0.8*fa)+')';ctx.fill();
      }
    }

    // flowing particles
    if(elapsed>1.2){
      particles.forEach(p=>{
        const segReveal = (p.seg+0.5)*0.22;
        if(elapsed < segReveal+0.3) return;
        p.t += p.speed;
        if(p.t>1) p.t-=1;
        const x = W/2;
        const y0 = p.seg*FULL_H + BLOCK_H;
        const y1 = y0 + GAP;
        const py = y0 + (y1-y0)*p.t;
        const col1 = stages[p.seg].col;
        const col2 = stages[p.seg+1].col;
        const mix = p.t;
        ctx.beginPath();ctx.arc(x,py,2.5,0,TAU);
        ctx.fillStyle=mix<0.5?col1+'0.9)':col2+'0.9)';
        ctx.fill();
        // glow
        ctx.beginPath();ctx.arc(x,py,5,0,TAU);
        ctx.fillStyle=mix<0.5?col1+'0.15)':col2+'0.15)';
        ctx.fill();
      });
    }

    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
};
