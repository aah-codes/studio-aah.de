// Hero: Mockups bewegen sich beim Scrollen leicht versetzt (Parallaxe).
// Bei „Bewegung reduzieren“ passiert nichts; ohne JavaScript stehen die Bilder still.
(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const teile = [...document.querySelectorAll('.hero-mockups [data-tiefe]')];
  if (!teile.length) return;
  let geplant = false;
  function bewegen() {
    const y = window.scrollY;
    teile.forEach((t) => { t.style.setProperty('--versatz', `${(y * parseFloat(t.dataset.tiefe)).toFixed(1)}px`); });
    geplant = false;
  }
  window.addEventListener('scroll', () => { if (!geplant) { geplant = true; requestAnimationFrame(bewegen); } }, { passive: true });
})();
