/* Blogartikel: Kapitel-Leiste mit Fortschritt und Lesebalken. */
(function () {
  var text = document.querySelector('.artikel-text');
  if (!text) return;

  /* ---------- Kapitel und Fortschritt ---------- */
  var leiste = document.querySelector('.artikel-leiste');
  var links = leiste ? Array.prototype.slice.call(leiste.querySelectorAll('.kl-schritte a')) : [];
  var ziele = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  var balken = document.createElement('div');
  balken.className = 'lese-balken';
  balken.setAttribute('aria-hidden', 'true');
  document.body.appendChild(balken);
  var bahn = leiste && leiste.querySelector('.kl-fortschritt span');

  function aktualisieren() {
    var r = text.getBoundingClientRect();
    var gesamt = r.height - window.innerHeight * 0.6;
    var anteil = Math.min(1, Math.max(0, -r.top / (gesamt > 0 ? gesamt : 1)));
    balken.style.transform = 'scaleX(' + anteil + ')';
    if (bahn) bahn.style.transform = 'scaleX(' + anteil + ')';
    var aktiv = -1;
    ziele.forEach(function (z, i) { if (z && z.getBoundingClientRect().top < window.innerHeight * 0.35) aktiv = i; });
    links.forEach(function (a, i) {
      var li = a.parentNode;
      li.classList.toggle('aktiv', i === aktiv);
      li.classList.toggle('erledigt', i < aktiv);
      if (i === aktiv) a.setAttribute('aria-current', 'step'); else a.removeAttribute('aria-current');
    });
  }
  var geplant = false;
  window.addEventListener('scroll', function () {
    if (geplant) return;
    geplant = true;
    window.requestAnimationFrame(function () { geplant = false; aktualisieren(); });
  }, { passive: true });
  window.addEventListener('resize', aktualisieren);
  aktualisieren();

})();
