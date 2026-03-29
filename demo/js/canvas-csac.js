/* ─── CSAC ATOMIC CLOCK CANVAS ─── */
const TAU = Math.PI*2;

let csacStarted = false;
window.startCSAC = function startCSAC(){
  if(csacStarted) return; csacStarted = true;
  const canvas = document.getElementById('csac-canvas');
  if(!canvas) return;
  const ctx = canvas.getContext('2d');
  const W=380, H=220;

  // ── Layout constants ──
  // Left zone: VCSEL die
  const VCSEL_X=28, VCSEL_W=44, VCSEL_Y=30, VCSEL_H=H-60;
  // Centre zone: vapor cell
  const CELL_X=96, CELL_W=186, CELL_Y=28, CELL_H=H-58;
  const CELL_CX=CELL_X+CELL_W/2, CELL_CY=CELL_Y+CELL_H/2;
  // Right zone: photodetector
  const PD_X=302, PD_W=44, PD_Y=30, PD_H=H-60;
  // Beam Y
  const BY = H/2 - 4;
  // Bottom: output signal strip
  const SIG_Y = H-22;

  // ── Rb atoms ──
  const atoms=[];
  const NA=28;
  for(let i=0;i<NA;i++){
    atoms.push({
      x: CELL_X+12 + Math.random()*(CELL_W-24),
      y: CELL_Y+10 + Math.random()*(CELL_H-20),
      vx:(Math.random()-0.5)*0.35,
      vy:(Math.random()-0.5)*0.35,
      phase:Math.random()*TAU,
      r:1.6+Math.random()*1.2,
      state:0, // 0=ground, 1=excited
      exciteTimer:0,
    });
  }

  // ── Photon particles (travel VCSEL→PD along beam) ──
  const photons=[];
  for(let i=0;i<18;i++){
    photons.push({
      x: VCSEL_X+VCSEL_W + Math.random()*(CELL_W+PD_W+30),
      speed: 2.8+Math.random()*1.4,
      absorbed:false,
      opacity:0.7+Math.random()*0.3,
    });
  }

  // ── MW signal wave ──
  let sigOffset=0;

  // ── PD signal (varies with absorption) ──
  let pdLevel=0.6, pdTarget=0.6;

  const startT = performance.now();

  function rr(ctx,x,y,w,h,r){
    ctx.beginPath();
    ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);
    ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);
    ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);
    ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();
  }

  function frame(){
    const elapsed=(performance.now()-startT)/1000;
    ctx.clearRect(0,0,W,H);
    sigOffset+=2.2;

    // ── Background ──
    ctx.fillStyle='#07060d';
    ctx.fillRect(0,0,W,H);

    // ── VCSEL die ──
    rr(ctx,VCSEL_X,VCSEL_Y,VCSEL_W,VCSEL_H,6);
    ctx.fillStyle='rgba(255,60,60,0.07)';ctx.fill();
    rr(ctx,VCSEL_X,VCSEL_Y,VCSEL_W,VCSEL_H,6);
    ctx.strokeStyle='rgba(255,60,60,0.45)';ctx.lineWidth=1;ctx.stroke();

    // VCSEL emitter
    const vcPulse=0.6+0.4*Math.sin(elapsed*18);
    const vcGrad=ctx.createRadialGradient(VCSEL_X+VCSEL_W/2,BY,0,VCSEL_X+VCSEL_W/2,BY,18);
    vcGrad.addColorStop(0,`rgba(255,80,60,${0.9*vcPulse})`);
    vcGrad.addColorStop(1,'transparent');
    ctx.beginPath();ctx.arc(VCSEL_X+VCSEL_W/2,BY,18,0,TAU);ctx.fillStyle=vcGrad;ctx.fill();
    ctx.beginPath();ctx.arc(VCSEL_X+VCSEL_W/2,BY,4,0,TAU);
    ctx.fillStyle=`rgba(255,120,80,${vcPulse})`;ctx.fill();

    ctx.font="600 7.5px 'JetBrains Mono',monospace";
    ctx.textAlign='center';ctx.textBaseline='top';
    ctx.fillStyle='rgba(255,100,80,0.6)';
    ctx.fillText('VCSEL',VCSEL_X+VCSEL_W/2,VCSEL_Y+6);
    ctx.fillStyle='rgba(255,100,80,0.35)';
    ctx.fillText('795nm',VCSEL_X+VCSEL_W/2,VCSEL_Y+17);

    // ── Vapor cell ──
    // Outer glow
    const cGlow=ctx.createRadialGradient(CELL_CX,CELL_CY,0,CELL_CX,CELL_CY,CELL_W*0.6);
    cGlow.addColorStop(0,'rgba(255,183,0,0.04)');cGlow.addColorStop(1,'transparent');
    rr(ctx,CELL_X,CELL_Y,CELL_W,CELL_H,8);ctx.fillStyle=cGlow;ctx.fill();

    rr(ctx,CELL_X,CELL_Y,CELL_W,CELL_H,8);
    ctx.strokeStyle='rgba(255,183,0,0.35)';ctx.lineWidth=1.2;ctx.stroke();

    // Cell label
    ctx.font="700 8px 'JetBrains Mono',monospace";
    ctx.textAlign='center';ctx.textBaseline='top';
    ctx.fillStyle='rgba(255,183,0,0.5)';
    ctx.fillText('MEMS VAPOR CELL  ·  Rb-87',CELL_CX,CELL_Y+7);

    // MW antenna rings (two dashed arcs above and below)
    const mwPhase=elapsed*4;
    [0.3,0.5,0.7].forEach((frac,i)=>{
      const r2=frac*CELL_W*0.48;
      const a2=0.7+0.3*Math.sin(mwPhase+i*1.2);
      ctx.beginPath();ctx.arc(CELL_CX,CELL_CY,r2,0,TAU);
      ctx.strokeStyle=`rgba(167,139,250,${0.08*a2})`;
      ctx.lineWidth=r2*0.04+0.5;
      ctx.setLineDash([3,4]);ctx.stroke();ctx.setLineDash([]);
    });

    // MW label (bottom of cell)
    ctx.font="500 7px 'JetBrains Mono',monospace";
    ctx.textAlign='center';ctx.textBaseline='bottom';
    ctx.fillStyle='rgba(167,139,250,0.4)';
    ctx.fillText('6.834 682 610 GHz',CELL_CX,CELL_Y+CELL_H-6);

    // ── Atoms ──
    let absorbedCount=0;
    atoms.forEach(a=>{
      // Drift + bounce
      a.x+=a.vx; a.y+=a.vy;
      if(a.x<CELL_X+4||a.x>CELL_X+CELL_W-4) a.vx*=-1;
      if(a.y<CELL_Y+18||a.y>CELL_Y+CELL_H-14) a.vy*=-1;

      // Excite if photon passes close to beam
      if(a.exciteTimer>0){ a.exciteTimer--; a.state=1; } else { a.state=0; }

      // Quantum-state-based colour
      const baseA = a.state===1 ? 'rgba(255,183,0,' : 'rgba(255,183,0,';
      const alpha = a.state===1
        ? 0.9
        : 0.25+0.2*Math.sin(elapsed*2+a.phase);
      ctx.beginPath();ctx.arc(a.x,a.y,a.r+(a.state===1?1.5:0),0,TAU);
      ctx.fillStyle=baseA+alpha+')';ctx.fill();

      if(a.state===1){
        ctx.beginPath();ctx.arc(a.x,a.y,a.r+4,0,TAU);
        ctx.fillStyle='rgba(255,183,0,0.12)';ctx.fill();
        absorbedCount++;
      }
    });

    // PD level follows absorption (more absorbed → less reaches PD)
    pdTarget = 0.85 - (absorbedCount/atoms.length)*0.5;
    pdLevel += (pdTarget-pdLevel)*0.04;

    // ── Photon beam ──
    const beamGrad=ctx.createLinearGradient(VCSEL_X+VCSEL_W,BY,PD_X,BY);
    beamGrad.addColorStop(0,'rgba(255,80,60,0.5)');
    beamGrad.addColorStop(0.5,'rgba(255,100,70,0.25)');
    beamGrad.addColorStop(1,'rgba(255,80,60,0.0)');
    ctx.beginPath();ctx.moveTo(VCSEL_X+VCSEL_W,BY);ctx.lineTo(PD_X,BY);
    ctx.strokeStyle=beamGrad;ctx.lineWidth=2;ctx.stroke();

    // Photon particles
    photons.forEach(p=>{
      p.x+=p.speed;
      if(p.x>PD_X+PD_W) p.x=VCSEL_X+VCSEL_W;

      // Check for atom collision near beam
      if(!p.absorbed){
        atoms.forEach(a=>{
          if(Math.abs(a.y-BY)<12 && Math.abs(a.x-p.x)<6 && a.state===0){
            if(Math.random()<0.07){
              a.exciteTimer=18+Math.floor(Math.random()*12);
              p.x=PD_X+PD_W+1; // restart
            }
          }
        });
      }

      // fade near edges
      let fa=1;
      const dx2=p.x-(VCSEL_X+VCSEL_W);
      const totLen=PD_X-(VCSEL_X+VCSEL_W);
      if(dx2/totLen<0.08) fa=dx2/(totLen*0.08);
      if(dx2/totLen>0.92) fa=(1-dx2/totLen)/0.08;
      fa=Math.max(0,Math.min(1,fa));

      ctx.beginPath();ctx.arc(p.x,BY,2,0,TAU);
      ctx.fillStyle=`rgba(255,100,70,${p.opacity*fa})`;ctx.fill();
    });

    // ── Photodetector ──
    rr(ctx,PD_X,PD_Y,PD_W,PD_H,6);
    ctx.fillStyle=`rgba(0,200,255,${0.04+pdLevel*0.06})`;ctx.fill();
    rr(ctx,PD_X,PD_Y,PD_W,PD_H,6);
    ctx.strokeStyle=`rgba(0,200,255,${0.3+pdLevel*0.3})`;ctx.lineWidth=1;ctx.stroke();

    // PD active area glow
    const pdG=ctx.createRadialGradient(PD_X+PD_W/2,BY,0,PD_X+PD_W/2,BY,20);
    pdG.addColorStop(0,`rgba(0,200,255,${pdLevel*0.35})`);pdG.addColorStop(1,'transparent');
    ctx.beginPath();ctx.arc(PD_X+PD_W/2,BY,20,0,TAU);ctx.fillStyle=pdG;ctx.fill();

    ctx.font="600 7.5px 'JetBrains Mono',monospace";
    ctx.textAlign='center';ctx.textBaseline='top';
    ctx.fillStyle=`rgba(0,200,255,${0.4+pdLevel*0.3})`;
    ctx.fillText('PD',PD_X+PD_W/2,PD_Y+6);

    // ── Output signal (bottom strip) ──
    const stripH=16;
    ctx.fillStyle='rgba(255,183,0,0.04)';
    ctx.fillRect(0,SIG_Y-2,W,stripH);

    // Frequency lock signal: stable sine
    ctx.beginPath();
    for(let x=0;x<=W;x+=1){
      const phase=(x/W)*Math.PI*14-sigOffset*0.04;
      const noise=(Math.random()-0.5)*0.4;
      const y=SIG_Y+6 - (pdLevel*4+2)*Math.sin(phase)+noise;
      x===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
    }
    ctx.strokeStyle='rgba(255,183,0,0.6)';ctx.lineWidth=1;ctx.stroke();

    ctx.font="500 6.5px 'JetBrains Mono',monospace";
    ctx.textAlign='left';ctx.textBaseline='bottom';
    ctx.fillStyle='rgba(255,183,0,0.3)';
    ctx.fillText('FREQUENCY LOCK OUTPUT',4,H-1);

    // Stability label right
    ctx.textAlign='right';
    ctx.fillStyle='rgba(0,255,135,0.4)';
    ctx.fillText('σ_y = 3×10⁻¹⁰/√τ',W-4,H-1);

    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
};
