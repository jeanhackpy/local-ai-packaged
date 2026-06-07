/**
 * REcall Agency — Main JS v3
 * Tabs + Scroll reveal + GSAP counters
 * No jQuery dependency.
 */

(function () {
  'use strict';

  /* ── 1. INTERSECTION OBSERVER — Scroll reveal ── */
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -48px 0px' }
  );

  document.querySelectorAll('.rc-reveal, .rc-reveal-group').forEach((el) => {
    revealObserver.observe(el);
  });

  /* ── 2. SOLUTIONS TABS ── */
  const tabs   = document.querySelectorAll('.rc-tab');
  const panels = document.querySelectorAll('.rc-tab-panel');

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;

      tabs.forEach((t) => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      panels.forEach((p) => p.classList.remove('active'));

      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');

      const panel = document.getElementById('tab-' + target);
      if (panel) panel.classList.add('active');
    });
  });

  /* ── 3. GSAP ANIMATIONS (loaded via functions.php) ── */
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    gsap.from('.rc-hero__inner > *', {
      opacity: 0,
      y: 30,
      duration: 0.9,
      stagger: 0.12,
      ease: 'power3.out',
      delay: 0.2,
    });

    /* Animated counters */
    document.querySelectorAll('.rc-stat__number').forEach((el) => {
      const spanEl = el.querySelector('span');
      if (!spanEl) return;
      const raw    = spanEl.textContent.replace(/[^0-9.]/g, '');
      const target = parseFloat(raw);
      if (isNaN(target)) return;

      const obj = { val: 0 };
      ScrollTrigger.create({
        trigger: el,
        start: 'top 85%',
        once: true,
        onEnter: () => {
          gsap.to(obj, {
            val: target,
            duration: 1.6,
            ease: 'power2.out',
            onUpdate: () => {
              spanEl.textContent =
                target % 1 === 0
                  ? Math.round(obj.val).toString()
                  : obj.val.toFixed(1);
            },
          });
        },
      });
    });

    /* Cards stagger */
    document.querySelectorAll('.rc-products__grid, .rc-features__grid').forEach((grid) => {
      gsap.from(grid.querySelectorAll('.rc-card, .rc-feature'), {
        scrollTrigger: { trigger: grid, start: 'top 80%', once: true },
        opacity: 0,
        y: 24,
        duration: 0.7,
        stagger: 0.1,
        ease: 'power2.out',
      });
    });
  }

  /* ── 4. Nav scroll shadow ── */
  const nav = document.querySelector('.rc-nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.style.boxShadow = window.scrollY > 40
        ? '0 4px 32px rgba(0,0,0,0.45)'
        : 'none';
    }, { passive: true });
  }

})();
