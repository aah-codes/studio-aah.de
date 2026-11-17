/* Blogartikel (Anna 17.11.2026): Kapitel-Leiste mit Fortschritt und Vorlesen mit Tempo.
   Vorlesen nutzt nur Stimmen, die auf dem Gerät liegen (localService), nichts wird gesendet. */
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

  /* ---------- Vorlesen ---------- */
  var box = document.querySelector('.vorlesen');
  var sprache = window.speechSynthesis;
  if (!box || !sprache || typeof SpeechSynthesisUtterance === 'undefined') return;

  var start = box.querySelector('.vl-start');
  var stopp = box.querySelector('.vl-stopp');
  var tempo = box.querySelector('select');
  var symbol = box.querySelector('.vl-symbol');
  var beschriftung = box.querySelector('.vl-text');
  var stimme = null;

  function stimmeWaehlen() {
    var alle = sprache.getVoices().filter(function (v) { return v.localService && /^de/i.test(v.lang); });
    stimme = alle[0] || null;
    box.hidden = !stimme; /* ohne lokale deutsche Stimme kein Vorlesen */
  }
  stimmeWaehlen();
  if (typeof sprache.onvoiceschanged !== 'undefined') sprache.onvoiceschanged = stimmeWaehlen;

  var teile = [];
  var nr = 0;
  var zustand = 'aus'; /* aus | laeuft | pause */
  var aktuell = null; /* nur das zuletzt gestartete Stück darf weiterschalten */

  function teileSammeln() {
    var auswahl = '.kurz li, .artikel-text > p, .artikel-text > ul > li, .artikel-text > ol > li, .artikel-text > h2, .artikel-text > h3';
    return Array.prototype.slice.call(text.querySelectorAll(auswahl)).filter(function (el) {
      return !el.closest('.inhalt-verzeichnis, figure, .tabelle-scroll, .quellen, .artikel-schluss, .autorin, .artikel-faq, .artikel-seite, .artikel-leiste')
        && !(el.id === 'quellen');
    });
  }
  function sprechtext(el) {
    var k = el.cloneNode(true);
    Array.prototype.forEach.call(k.querySelectorAll('sup, [aria-hidden="true"]'), function (s) { s.remove(); });
    return k.textContent.replace(/\s+/g, ' ').trim();
  }
  function markieren(el) {
    Array.prototype.forEach.call(text.querySelectorAll('.vl-aktiv'), function (e) { e.classList.remove('vl-aktiv'); });
    if (el) el.classList.add('vl-aktiv');
  }
  function knopf() {
    var laeuft = zustand === 'laeuft';
    symbol.textContent = laeuft ? 'Ⅱ' : '▶';
    beschriftung.textContent = laeuft ? 'Pause' : (zustand === 'pause' ? 'Weiter vorlesen' : 'Artikel vorlesen');
    start.setAttribute('aria-pressed', laeuft ? 'true' : 'false');
    stopp.hidden = zustand === 'aus';
  }
  function sprechen() {
    if (nr >= teile.length) { beenden(); return; }
    var el = teile[nr];
    var u = new SpeechSynthesisUtterance(sprechtext(el));
    u.voice = stimme; u.lang = stimme.lang; u.rate = parseFloat(tempo.value);
    aktuell = u;
    u.onend = function () { if (u === aktuell && zustand === 'laeuft') { nr++; sprechen(); } };
    markieren(el);
    var r = el.getBoundingClientRect();
    if (r.top < 80 || r.bottom > window.innerHeight) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    sprache.speak(u);
  }
  function beenden() {
    zustand = 'aus'; nr = 0; aktuell = null; sprache.cancel(); markieren(null); knopf();
  }
  start.addEventListener('click', function () {
    if (zustand === 'laeuft') { zustand = 'pause'; sprache.pause(); }
    else if (zustand === 'pause') { zustand = 'laeuft'; sprache.resume(); }
    else { teile = teileSammeln(); nr = 0; zustand = 'laeuft'; aktuell = null; sprache.cancel(); sprechen(); }
    knopf();
  });
  stopp.addEventListener('click', beenden);
  tempo.addEventListener('change', function () {
    if (zustand === 'laeuft') { aktuell = null; sprache.cancel(); sprechen(); }
  });
  window.addEventListener('pagehide', function () { sprache.cancel(); });
})();
