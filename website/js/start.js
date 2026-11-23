/* Startseite: Hero mit Frag-Feld als Chat und Diashow */
(function () {
  var hero = document.querySelector('.hl'); if (!hero) return;

  // Chips stellen ihre Frage ins Feld und schicken sie ab
  hero.querySelectorAll('.hl-chip').forEach(function (c) { c.addEventListener('click', function () {
    var f = hero.querySelector('[data-frag]'); if (!f) return;
    f.querySelector('input').value = c.dataset.frage;
    if (f.requestSubmit) f.requestSubmit(); else f.dispatchEvent(new Event('submit', { cancelable: true })); }); });

  // Chat-Ansicht: sobald eine Frage gestellt ist, Überschrift kleiner, Chatfenster mit Feld unten (Scrollen macht js/frag.js)
  var verlauf = hero.querySelector('.hl-antworten');
  if (verlauf && 'MutationObserver' in window) new MutationObserver(function () {
    hero.classList.toggle('ist-chat', !!verlauf.textContent.trim());
  }).observe(verlauf, { childList: true, subtree: true });

  // Diashow: Bilder blenden ineinander, Pause-Button; Bilder ab Folie 2 laden erst kurz vorher
  var folien = hero.querySelectorAll('.hl-folie'), p = hero.querySelector('.hl-pause');
  if (!folien.length || !p) return;
  var DAUER = 6000, i = 0, uhr = null, still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function lade(f) { f.querySelectorAll('img[data-src]').forEach(function (b) { if (b.dataset.srcset) { b.srcset = b.dataset.srcset; b.removeAttribute('data-srcset'); } b.src = b.dataset.src; b.removeAttribute('data-src'); }); }
  function zeige(n) {
    i = (n + folien.length) % folien.length;
    lade(folien[i]); lade(folien[(i + 1) % folien.length]);
    folien.forEach(function (f, k) {
      f.classList.toggle('ist-aktiv', k === i); f.setAttribute('aria-hidden', k === i ? 'false' : 'true');
      if (k === i) f.querySelectorAll('img').forEach(function (b) { b.style.animation = 'none'; void b.offsetHeight; b.style.animation = ''; });
    });
    plane();
  }
  function plane() { clearTimeout(uhr); if (!hero.classList.contains('ist-pausiert')) uhr = setTimeout(function () { zeige(i + 1); }, +(folien[i].dataset.dauer || DAUER)); }
  function pause(an) {
    hero.classList.toggle('ist-pausiert', an);
    p.setAttribute('aria-label', an ? 'Diashow abspielen' : 'Diashow anhalten'); p.textContent = an ? '▶' : '❚❚';
    if (an) clearTimeout(uhr); else zeige(i + 1);
  }
  p.addEventListener('click', function () { pause(!hero.classList.contains('ist-pausiert')); });
  if (still) { pause(true); lade(folien[1]); } else zeige(0);
})();
