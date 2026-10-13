// Hero: Leiste mit den Leistungen (Karten wie bei Dribbble, Anna 13.10.2026), die auf die Maus reagiert.
// Maus links/rechts im Hero = Leiste läuft in diese Richtung (je weiter außen, desto schneller); über einer Karte hält sie an.
// Kein Kippen oder Zoomen der Karten (Anna 13.10.2026: alle Bilder müssen scharf sein); beim Darüberfahren heben sie sich per CSS.
// Ziehen mit Maus oder Finger verschiebt die Leiste; ein Klick ohne Ziehen öffnet die Leistung.
// Pause-Taste hält die Leiste an (Bewegung, die von selbst läuft, muss sich anhalten lassen).
// Tastatur: Fokus auf einer Karte hält die Leiste an und schiebt die Karte ins Bild.
// Bei „Bewegung reduzieren“ steht die Leiste und lässt sich nur ziehen; ohne JavaScript steht sie still.
(() => {
  const hero = document.querySelector('.hero-buehne');
  const band = hero && hero.querySelector('.hero-band');
  if (!band) return;
  const spur = band.querySelector('.hero-spur');
  const pause = band.querySelector('.band-pause');
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Inhalt doppeln, damit die Leiste endlos laufen kann; die Kopie bleibt mit der Maus klickbar,
  // ist aber für Vorleser und Tastatur unsichtbar (sonst stünde jede Leistung doppelt in der Liste)
  [...spur.children].forEach((t) => {
    const kopie = t.cloneNode(true);
    kopie.setAttribute('aria-hidden', 'true');
    kopie.setAttribute('tabindex', '-1');
    spur.appendChild(kopie);
  });
    const grund = still ? 0 : -0.9;
  let x = 0, tempo = 0, zielTempo = grund, maus = null, ziehen = null, gezogen = false, breite = 0, angehalten = false, ueberKarte = false, fokus = false;
  const messen = () => { breite = spur.scrollWidth / 2; };
  messen();
  window.addEventListener('resize', messen);
  window.addEventListener('load', messen);

  if (pause) pause.addEventListener('click', () => {
    angehalten = !angehalten;
    pause.setAttribute('aria-pressed', String(angehalten));
    pause.querySelector('.unsichtbar').textContent = angehalten ? 'Laufband weiterlaufen lassen' : 'Laufband anhalten';
  });

  hero.addEventListener('pointermove', (e) => {
    const r = hero.getBoundingClientRect();
    hero.style.setProperty('--mx', `${((e.clientX - r.left) / r.width * 100).toFixed(1)}%`);
    hero.style.setProperty('--my', `${((e.clientY - r.top) / r.height * 100).toFixed(1)}%`);
    if (e.pointerType !== 'mouse') return;
    maus = { x: e.clientX, y: e.clientY };
    ueberKarte = !!e.target.closest('.kat');
    if (!still) zielTempo = -((e.clientX - r.left) / r.width - .5) * 7;
  });
  hero.addEventListener('pointerleave', () => { maus = null; ueberKarte = false; zielTempo = grund; band.classList.remove('aktiv'); });

  // Ziehen erst ab 6 px Bewegung, damit ein normaler Klick auf eine Karte den Link öffnet
  band.addEventListener('pointerdown', (e) => {
    if (e.target.closest('.band-pause')) return;
    ziehen = { x: e.clientX, start: x, id: e.pointerId }; gezogen = false;
  });
  band.addEventListener('pointermove', (e) => {
    if (!ziehen) return;
    const dx = e.clientX - ziehen.x;
    if (!gezogen && Math.abs(dx) > 6) { gezogen = true; band.classList.add('zieht'); band.setPointerCapture(ziehen.id); }
    if (gezogen) { x = ziehen.start + dx; tempo = 0; }
  });
  const loslassen = () => { ziehen = null; band.classList.remove('zieht'); };
  band.addEventListener('pointerup', loslassen);
  band.addEventListener('pointercancel', loslassen);
  band.addEventListener('click', (e) => { if (gezogen) { e.preventDefault(); e.stopPropagation(); gezogen = false; } }, true);
  band.addEventListener('dragstart', (e) => e.preventDefault());

  band.addEventListener('focusin', (e) => {
    const karte = e.target.closest('.kat');
    if (!karte) return;
    fokus = true; tempo = 0;
    const b = band.getBoundingClientRect(), k = karte.getBoundingClientRect();
    if (k.left < b.left + 24 || k.right > b.right - 24) x -= k.left - b.left - 24;
  });
  band.addEventListener('focusout', () => { fokus = false; });

  function schritt() {
    if (breite) {
      const bandR = band.getBoundingClientRect();
            const imBand = !!maus && maus.y > bandR.top - 40 && maus.y < bandR.bottom + 40;
      const halt = angehalten || ueberKarte || fokus;
      if (!ziehen || !gezogen) { tempo += ((halt ? 0 : imBand ? zielTempo * .35 : zielTempo) - tempo) * .06; x += tempo; }
      x = ((x % breite) - breite) % breite;
      spur.style.transform = `translate3d(${Math.round(x)}px,0,0)`; // ganze Pixel: Bilder und Schrift bleiben scharf
      band.classList.toggle('aktiv', imBand && !still);
    }
    requestAnimationFrame(schritt);
  }
  requestAnimationFrame(schritt);
})();

// Animation-Karte: der Erklärfilm (animiertes WebP, läuft einmal) startet beim Darüberfahren neu;
// bei „Bewegung reduzieren“ zeigt das <picture> nur das Standbild
(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  let nr = 0;
  document.querySelectorAll('.hero-spur .kat').forEach((karte) => {
    const bild = karte.querySelector('.kb-anim');
    if (!bild) return;
    const quelle = bild.getAttribute('src');
    let start = Date.now();
    karte.addEventListener('mouseenter', () => {
      if (Date.now() - start < 5000) return; // läuft noch: nicht neu laden
      start = Date.now();
      bild.src = `${quelle}?neu=${++nr}`;
    });
  });
})();
