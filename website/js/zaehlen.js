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
  // Bildschirmleser bekommen die echte Zahl in einem unsichtbaren Text, die laufende Zahl ist nur fürs Auge
  zahlen.forEach((z) => {
    const echt = document.createElement('span');
    echt.className = 'unsichtbar';
    echt.textContent = z.dataset.zaehlen;
    z.before(echt);
    z.setAttribute('aria-hidden', 'true');
    z.textContent = '0';
    beob.observe(z);
  });
})();

// Studio-Foto: Hinweise erscheinen nacheinander, sobald das Bild ins Bild kommt (bei „Bewegung reduzieren“ sofort)
(() => {
  const bild = document.querySelector('.studio-bild');
  if (!bild) return;
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) { bild.classList.add('los'); return; }
  bild.classList.add('wartet');
  // Startet, sobald das Bild das untere Viertel des Fensters überschreitet (unabhängig von der Bildhöhe)
  const beob = new IntersectionObserver((e) => { if (e.some((x) => x.isIntersecting)) { bild.classList.add('los'); beob.disconnect(); } }, { rootMargin: '0px 0px -25% 0px' });
  beob.observe(bild);
})();
