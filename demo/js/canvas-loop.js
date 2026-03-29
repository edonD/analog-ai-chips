/* ─── LOOP CANVAS (scene 3) ─── */
const TAU = Math.PI*2;

let loopStarted = false;
window.startLoop = function startLoop(){
  if(loopStarted) return; loopStarted=true;
  const canvas = document.getElementById('loop-c');
  const ctx = canvas.getContext('2d');
  const CX=310,CY=310,R=195;

  const nodes = [
    { a:-Math.PI/2,            label:['AI AGENT','Claude / LLM'],    col:'#7c3aed', glow:'rgba(124,58,237,' },
    { a:-Math.PI/2+TAU/5,      label:['EDA TOOLS','Xschem · ngspice'],col:'#00ff87', glow:'rgba(0,255,135,' },
    { a:-Math.PI/2+TAU*2/5,    label:['SIMULATE','SPICE · Corners'],  col:'#00d4ff', glow:'rgba(0,212,255,' },
    { a:-Math.PI/2+TAU*3/5,    label:['SILICON','SKY130A'],           col:'#ffb700', glow:'rgba(255,183,0,' },
    { a:-Math.PI/2+TAU*4/5,    label:['EDGE AI','300µW Inference'],   col:'#ff3d5a', glow:'rgba(255,61,90,' },
  ];

  // flowing particles on edges
  const particles = [];
  for(let e=0;e<5;e++){
    for(let p=0;p<5;p++){
      particles.push({ edge:e, progress:p/5, speed:0.004+Math.random()*0.002 });
    }
  }

  const NR = 50;
  const start = performance.now();

  function ease(t){ return t<0.5?2*t*t:-1+(4-2*t)*t }

  function frame(now){
    const elapsed = (now-start)/1000;
    ctx.clearRect(0,0,620,620);

    // orbit ring
    const rt = Math.min(1,elapsed/0.9);
    ctx.beginPath();
    ctx.arc(CX,CY,R,-Math.PI/2,-Math.PI/2+TAU*ease(rt));
    ctx.strokeStyle='rgba(255,255,255,0.06)'; ctx.lineWidth=1; ctx.stroke();

    // draw arrows + flowing particles
    if(elapsed>1.8){
      nodes.forEach((n,i)=>{
        const nx = nodes[(i+1)%5];
        const at = Math.min(1,(elapsed-2.0-i*0.12)/0.55);
        if(at<=0) return;

        const x0=CX+Math.cos(n.a)*R, y0=CY+Math.sin(n.a)*R;
        const x1=CX+Math.cos(nx.a)*R, y1=CY+Math.sin(nx.a)*R;
        const dx=x1-x0, dy=y1-y0, len=Math.sqrt(dx*dx+dy*dy);
        const ux=dx/len, uy=dy/len;
        const sx=x0+ux*NR, sy=y0+uy*NR;
        const ex=x0+ux*(NR+(len-NR*2)*ease(at));
        const ey=y0+uy*(NR+(len-NR*2)*ease(at));

        const g=ctx.createLinearGradient(sx,sy,ex,ey);
        g.addColorStop(0,n.col+'88');g.addColorStop(1,nx.col+'cc');
        ctx.beginPath();ctx.moveTo(sx,sy);ctx.lineTo(ex,ey);
        ctx.strokeStyle=g;ctx.lineWidth=1.5;
        ctx.setLineDash([6,5]);ctx.stroke();ctx.setLineDash([]);

        // arrowhead
        if(at>0.9){
          const fa=(at-0.9)/0.1;
          ctx.beginPath();
          ctx.moveTo(ex,ey);
          ctx.lineTo(ex-ux*9-uy*5,ey-uy*9+ux*5);
          ctx.lineTo(ex-ux*9+uy*5,ey-uy*9-ux*5);
          ctx.closePath();
          ctx.fillStyle=nx.col;ctx.globalAlpha=fa;ctx.fill();ctx.globalAlpha=1;
        }

        // flowing particles
        if(at>0.95 && elapsed>3.0){
          particles.filter(p=>p.edge===i).forEach(p=>{
            p.progress+=p.speed;
            if(p.progress>1) p.progress-=1;
            const px=sx+(ex-sx)*p.progress;
            const py=sy+(ey-sy)*p.progress;
            ctx.beginPath();ctx.arc(px,py,2.5,0,TAU);
            ctx.fillStyle=nx.col;ctx.globalAlpha=0.9;ctx.fill();ctx.globalAlpha=1;
          });
        }
      });
    }

    // nodes
    nodes.forEach((n,i)=>{
      const ns = Math.min(1,(elapsed-(0.5+i*0.22))/0.45);
      if(ns<=0) return;
      const x=CX+Math.cos(n.a)*R, y=CY+Math.sin(n.a)*R;

      // glow
      const gr=ctx.createRadialGradient(x,y,0,x,y,NR*2.5);
      gr.addColorStop(0,n.glow+(0.2*ns)+')');gr.addColorStop(1,'transparent');
      ctx.beginPath();ctx.arc(x,y,NR*2.5,0,TAU);ctx.fillStyle=gr;ctx.fill();

      // ring
      const r=NR*ease(ns);
      ctx.beginPath();ctx.arc(x,y,r,0,TAU);
      ctx.strokeStyle=n.col;ctx.lineWidth=1.5;ctx.globalAlpha=ns;ctx.stroke();

      // fill
      ctx.beginPath();ctx.arc(x,y,r,0,TAU);
      ctx.fillStyle='rgba(0,0,0,0.55)';ctx.fill();ctx.globalAlpha=1;

      // label
      if(ns>0.5){
        const lt=(ns-0.5)/0.5;
        ctx.globalAlpha=lt;
        ctx.font="700 10px 'Inter',sans-serif";
        ctx.textAlign='center';ctx.textBaseline='middle';
        ctx.fillStyle='#ffffff';
        ctx.fillText(n.label[0],x,y-7);
        ctx.font="400 8.5px 'JetBrains Mono',monospace";
        ctx.fillStyle='rgba(255,255,255,0.45)';
        ctx.fillText(n.label[1],x,y+7);
        ctx.globalAlpha=1;
      }
    });

    // center symbol
    if(elapsed>3.5){
      const ct=Math.min(1,(elapsed-3.5)/0.8);
      const pulse=0.85+Math.sin(elapsed*2.5)*0.15;
      ctx.globalAlpha=ct*pulse;
      ctx.font="900 28px 'Inter',sans-serif";
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillStyle='#ffffff';ctx.fillText('∞',CX,CY-5);
      ctx.font="500 8.5px 'JetBrains Mono',monospace";
      ctx.fillStyle=`rgba(0,212,255,${0.7*ct})`;
      ctx.fillText('RECURSIVE',CX,CY+12);
      ctx.globalAlpha=1;
    }

    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
};
