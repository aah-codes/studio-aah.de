// Kennzahlen zählen einmal hoch, sobald sie ins Bild kommen. Ohne JavaScript oder bei „Bewegung reduzieren“ steht die Zahl einfach da.
(() => {
  const zahlen = [...document.querySelectorAll('[data-zaehlen]')];
  if (!zahlen.length || !('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const los = (el) => {
    const ziel = +el.dataset.zaehlen, start = performance.now(), dauer = 1400;
    const schritt = (jetzt) => {
      const f = Math.min(1, (jetzt - start) / dauer);
      el.textContent = Math.round(ziel * (1 - Math.pow(1 - f, 3)));
      if (f < 1) requestAnimationFrame(schritt);
    };
    requestAnimationFrame(schritt);
  };
  const beob = new IntersectionObserver((e) => e.forEach((x) => { if (x.isIntersecting) { beob.unobserve(x.target); los(x.target); } }), { threshold: .6 });
  zahlen.forEach((z) => { z.textContent = '0'; beob.observe(z); });
})();
