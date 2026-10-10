// Hero: Bildband mit Projekten, das auf die Maus reagiert.
// Maus links/rechts im Hero = Band läuft in diese Richtung (je weiter außen, desto schneller); über den Bildern langsamer.
// Bilder nahe am Mauszeiger werden größer, heben sich und kippen leicht; die anderen treten zurück.
// Ziehen mit Maus oder Finger verschiebt das Band. Ohne Maus läuft es langsam von selbst.
// Bei „Bewegung reduzieren“ steht das Band und lässt sich nur ziehen; ohne JavaScript steht es still.
(() => {
  const hero = document.querySelector('.hero-buehne');
  const band = hero && hero.querySelector('.hero-band');
  if (!band) return;
  const spur = band.querySelector('.hero-spur');
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Inhalt doppeln, damit das Band endlos laufen kann
  [...spur.children].forEach((t) => spur.appendChild(t.cloneNode(true)));
  const teile = [...spur.children];
  const grund = still ? 0 : -0.3;
  let x = 0, tempo = 0, zielTempo = grund, maus = null, ziehen = null, breite = 0;
  const messen = () => { breite = spur.scrollWidth / 2; };
  messen();
  window.addEventListener('resize', messen);
  window.addEventListener('load', messen);

  hero.addEventListener('pointermove', (e) => {
    const r = hero.getBoundingClientRect();
    hero.style.setProperty('--mx', `${((e.clientX - r.left) / r.width * 100).toFixed(1)}%`);
    hero.style.setProperty('--my', `${((e.clientY - r.top) / r.height * 100).toFixed(1)}%`);
    if (e.pointerType !== 'mouse') return;
    maus = { x: e.clientX, y: e.clientY };
    if (!still) zielTempo = -((e.clientX - r.left) / r.width - .5) * 7;
  });
  hero.addEventListener('pointerleave', () => { maus = null; zielTempo = grund; band.classList.remove('aktiv'); });
  band.addEventListener('pointerdown', (e) => { ziehen = { x: e.clientX, start: x }; band.classList.add('zieht'); band.setPointerCapture(e.pointerId); });
  band.addEventListener('pointermove', (e) => { if (ziehen) { x = ziehen.start + (e.clientX - ziehen.x); tempo = 0; } });
  const loslassen = () => { ziehen = null; band.classList.remove('zieht'); };
  band.addEventListener('pointerup', loslassen);
  band.addEventListener('pointercancel', loslassen);

  function schritt() {
    if (breite) {
      const bandR = band.getBoundingClientRect();
      const sichtbar = bandR.bottom > 0 && bandR.top < innerHeight;
      const imBand = !!maus && maus.y > bandR.top - 40 && maus.y < bandR.bottom + 40;
      if (!ziehen) { tempo += ((imBand ? zielTempo * .35 : zielTempo) - tempo) * .06; x += tempo; }
      x = ((x % breite) - breite) % breite;
      spur.style.transform = `translate3d(${x.toFixed(1)}px,0,0)`;
      band.classList.toggle('aktiv', imBand && !still);
      if (sichtbar && !still) {
        teile.forEach((t) => {
          const r = t.getBoundingClientRect();
          if (r.right < -200 || r.left > innerWidth + 200) return;
          const mitte = r.left + r.width / 2;
          const nah = imBand ? Math.max(0, 1 - Math.abs(maus.x - mitte) / 320) : 0;
          const kipp = imBand ? Math.max(-1, Math.min(1, (maus.x - mitte) / 400)) : 0;
          const hoch = imBand ? (maus.y - (bandR.top + bandR.height / 2)) / bandR.height : 0;
          t.style.transform = `translateY(${(-nah * 18).toFixed(1)}px) scale(${(1 + nah * .16).toFixed(3)}) rotateY(${(kipp * 10).toFixed(1)}deg) rotateX(${(-hoch * nah * 10).toFixed(1)}deg)`;
          t.style.zIndex = nah > .4 ? 2 : 1;
          t.classList.toggle('nah', nah > .55);
        });
      }
    }
    requestAnimationFrame(schritt);
  }
  requestAnimationFrame(schritt);
})();
