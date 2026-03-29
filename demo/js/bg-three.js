/* ─── THREE.JS BACKGROUND ─── */
(function() {
  const renderer = new THREE.WebGLRenderer({
    canvas: document.getElementById('three-canvas'),
    alpha:true, antialias:false
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.5));
  renderer.setSize(window.innerWidth, window.innerHeight);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 2000);
  camera.position.z = 700;

  window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
  });

  // particles — reduce density on mobile for performance
  const N = window.innerWidth < 768 ? 600 : 1800;
  const positions = new Float32Array(N*3);
  const colors    = new Float32Array(N*3);
  const sizes     = new Float32Array(N);
  const palette = [
    [0.48, 0.23, 0.93], // violet
    [0.00, 0.83, 1.00], // cyan
    [0.00, 1.00, 0.53], // green
  ];
  for(let i=0;i<N;i++){
    positions[i*3]   = (Math.random()-0.5)*1400;
    positions[i*3+1] = (Math.random()-0.5)*1400;
    positions[i*3+2] = (Math.random()-0.5)*800;
    const c = palette[Math.floor(Math.random()*3)];
    colors[i*3]=c[0]; colors[i*3+1]=c[1]; colors[i*3+2]=c[2];
    sizes[i] = Math.random()*2+0.5;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions,3));
  geo.setAttribute('color',    new THREE.BufferAttribute(colors,3));
  geo.setAttribute('size',     new THREE.BufferAttribute(sizes,1));

  const mat = new THREE.ShaderMaterial({
    vertexShader:`
      attribute float size;
      attribute vec3 color;
      varying vec3 vColor;
      void main(){
        vColor = color;
        vec4 mvp = modelViewMatrix * vec4(position,1.0);
        gl_PointSize = size * (350.0 / -mvp.z);
        gl_Position = projectionMatrix * mvp;
      }
    `,
    fragmentShader:`
      varying vec3 vColor;
      void main(){
        vec2 uv = gl_PointCoord - 0.5;
        float d = dot(uv,uv);
        if(d > 0.25) discard;
        float a = 1.0 - d*4.0;
        gl_FragColor = vec4(vColor, a * 0.5);
      }
    `,
    transparent:true,vertexColors:true,depthWrite:false,blending:THREE.AdditiveBlending
  });

  const pts = new THREE.Points(geo,mat);
  scene.add(pts);

  // mouse parallax
  let tx=0,ty=0;
  document.addEventListener('mousemove', e => {
    tx = (e.clientX/window.innerWidth  - 0.5) * 30;
    ty = (e.clientY/window.innerHeight - 0.5) * 20;
  });

  let scrollY = 0;
  window.addEventListener('scroll', ()=>{ scrollY = window.scrollY; });

  function animate(){
    requestAnimationFrame(animate);
    const t = Date.now()*0.0003;
    pts.rotation.y = t*0.08 + tx*0.002;
    pts.rotation.x = t*0.04 + ty*0.002;
    pts.position.y = -scrollY*0.04;
    renderer.render(scene,camera);
  }
  animate();
})();
