/**
 * Recall Agency — Ambient Agent-Flow 3D Scene
 * A minimal, atmospheric Three.js background with flowing data particles.
 */
document.addEventListener('DOMContentLoaded', () => {

  /* ── Clean up old 3D remnants ────────────── */
  // Remove any existing canvases from old builds or Elementor
  document.querySelectorAll('canvas').forEach(c => c.remove());
  // Remove old three-bg wrappers
  const oldWrap = document.getElementById('rc-three-bg');
  if (oldWrap) oldWrap.remove();
  // Remove Elementor particle containers
  document.querySelectorAll('.eael-particles-wrap, #tsparticles, [id^="particles"]').forEach(el => el.remove());

  /* ── Scene Setup ─────────────────────────── */
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x09090B);
  scene.fog = new THREE.FogExp2(0x09090B, 0.0008);

  const camera = new THREE.PerspectiveCamera(
    60, window.innerWidth / window.innerHeight, 1, 2000
  );
  camera.position.set(0, 0, 400);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const wrap = document.createElement('div');
  wrap.id = 'rc-three-bg';
  Object.assign(wrap.style, {
    position: 'fixed', inset: '0',
    zIndex: '0', pointerEvents: 'none'
  });
  document.body.prepend(wrap);
  wrap.appendChild(renderer.domElement);

  /* ── Particles (Agent Data Flow) ─────────── */
  const COUNT = 1800;
  const geo = new THREE.BufferGeometry();
  const pos = new Float32Array(COUNT * 3);
  const vel = new Float32Array(COUNT); // speed per particle

  for (let i = 0; i < COUNT; i++) {
    pos[i * 3]     = (Math.random() - 0.5) * 1600;   // x
    pos[i * 3 + 1] = (Math.random() - 0.5) * 1000;   // y
    pos[i * 3 + 2] = (Math.random() - 0.5) * 1200;   // z
    vel[i] = 0.2 + Math.random() * 0.6;
  }

  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));

  const mat = new THREE.PointsMaterial({
    color: 0x00FFD1,
    size: 1.8,
    transparent: true,
    opacity: 0.5,
    sizeAttenuation: true
  });

  const particles = new THREE.Points(geo, mat);
  scene.add(particles);

  /* ── Secondary dim star layer ─────────────── */
  const starCount = 600;
  const starGeo = new THREE.BufferGeometry();
  const starPos = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount * 3; i++) {
    starPos[i] = (Math.random() - 0.5) * 2000;
  }
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  const starMat = new THREE.PointsMaterial({
    color: 0xffffff, size: 0.6,
    transparent: true, opacity: 0.2
  });
  scene.add(new THREE.Points(starGeo, starMat));

  /* ── Subtle grid plane ───────────────────── */
  const gridHelper = new THREE.GridHelper(1200, 40, 0x00FFD1, 0x00FFD1);
  gridHelper.position.y = -200;
  gridHelper.material.opacity = 0.04;
  gridHelper.material.transparent = true;
  scene.add(gridHelper);

  /* ── Animation Loop ──────────────────────── */
  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    const posArr = geo.attributes.position.array;

    // Flow particles slowly downward-left (like data streaming)
    for (let i = 0; i < COUNT; i++) {
      posArr[i * 3]     -= vel[i] * 0.3;  // drift left
      posArr[i * 3 + 1] -= vel[i] * 0.15; // drift down

      // Wrap around when out of bounds
      if (posArr[i * 3] < -800) posArr[i * 3] = 800;
      if (posArr[i * 3 + 1] < -500) posArr[i * 3 + 1] = 500;
    }
    geo.attributes.position.needsUpdate = true;

    // Slow camera sway
    camera.position.x = Math.sin(t * 0.08) * 30;
    camera.position.y = Math.cos(t * 0.06) * 20;
    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);
  }
  animate();

  /* ── GSAP Scroll Reveals ─────────────────── */
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    // Remove any old canvases from previous builds
    document.querySelectorAll('canvas').forEach(c => {
      if (c !== renderer.domElement) c.remove();
    });

    // Set all rc-reveal elements to hidden initially via GSAP
    const reveals = document.querySelectorAll('.rc-reveal');
    gsap.set(reveals, { opacity: 0, y: 40 });

    // Hero elements — animate immediately (above the fold)
    const heroReveals = document.querySelectorAll('.rc-hero .rc-reveal');
    heroReveals.forEach((el, i) => {
      gsap.to(el, {
        opacity: 1, y: 0,
        duration: 0.9,
        delay: 0.3 + i * 0.15,
        ease: 'power3.out'
      });
    });

    // Below-fold elements — animate on scroll
    const scrollReveals = document.querySelectorAll('.rc-section .rc-reveal, .rc-cta .rc-reveal');
    scrollReveals.forEach((el, i) => {
      gsap.to(el, {
        opacity: 1, y: 0,
        duration: 0.8,
        delay: (i % 4) * 0.08,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 88%',
          once: true
        }
      });
    });

    // Floating island header
    const header = document.querySelector('.site-header');
    if (header) {
      ScrollTrigger.create({
        start: 'top -80',
        onUpdate: (self) => {
          if (self.scroll() > 80) {
            header.classList.add('is-sticky');
          } else {
            header.classList.remove('is-sticky');
          }
        }
      });
    }

    // Parallax camera on scroll
    ScrollTrigger.create({
      start: 'top top',
      end: 'bottom bottom',
      scrub: 1,
      onUpdate: (self) => {
        camera.position.z = 400 - self.progress * 200;
        particles.rotation.y = self.progress * 0.3;
      }
    });
  }

  /* ── Resize ──────────────────────────────── */
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
});
