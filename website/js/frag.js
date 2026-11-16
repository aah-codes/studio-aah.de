// Frag-Feld im Hero der Startseite (Anna 16.11.2026): sucht nur in den häufigen Fragen der Website (daten/fragen.json,
// erzeugt von werkzeuge/fragen-index.py) und zeigt die passendsten Antworten mit Link. Alles läuft im Browser, nichts wird gesendet.
(function () {
  // Punkteraster im Hero: rund um die Maus deutlicher (Anna 17.11.2026, wie früher die hellgrauen Punkte)
  var buehne = document.querySelector('[data-raster]');
  if (buehne && window.matchMedia('(hover: hover)').matches) {
    buehne.addEventListener('pointermove', function (ev) {
      var r = buehne.getBoundingClientRect();
      buehne.style.setProperty('--mx', ((ev.clientX - r.left) / r.width * 100).toFixed(1) + '%');
      buehne.style.setProperty('--my', ((ev.clientY - r.top) / r.height * 100).toFixed(1) + '%');
    });
  }
})();
(function () {
  var form = document.querySelector('[data-frag]');
  var ziel = document.querySelector('[data-frag-antworten]');
  if (!form || !ziel) return;
  var feld = form.querySelector('input');
  var daten = null;

  // Füllwörter, die keine Bedeutung tragen
  var STOPP = ('aber alle als also am an auch auf aus bei bin bis bitte da dann das dass dem den der des die dies doch du ein eine einem einen einer es für gibt habe hat ich ihr ihre im in ist ja kann man mein meine mich mir mit muss nach nicht noch nur ob oder sie sind so über um und uns von vor was welche welcher welches wenn wer wie wird wir wo zu zum zur sich mehr gut').split(' ');
  // Gleiche Bedeutung, andere Wörter
  var GLEICH = { webseite: 'website', homepage: 'website', internetseite: 'website', seite: 'website', preis: 'kosten', preise: 'kosten', kostet: 'kosten', teuer: 'kosten', budget: 'kosten',
    dauert: 'dauer', lange: 'dauer', wochen: 'dauer', relaunch: 'redesign', ai: 'ki', logo: 'marke', branding: 'marke', bewerber: 'fachkräfte', mitarbeiter: 'fachkräfte' };

  function norm(t) {
    return t.toLowerCase().replace(/studio aah!?/g, ' ').replace(/[^a-zäöüß0-9]+/g, ' ').trim();
  }
  function woerter(t) {
    return norm(t).split(' ').filter(function (w) { return w.length > 1 && STOPP.indexOf(w) < 0; }).map(function (w) { return GLEICH[w] || w; });
  }
  function treffer(wort, liste) {
    // ganzes Wort zählt voll, Wortanfang (ab 4 Buchstaben) halb: „website“ findet „website-check“, „kosten“ findet „kostenlos“ schwächer
    var p = 0;
    for (var i = 0; i < liste.length; i++) {
      if (liste[i] === wort) { p = Math.max(p, 1); }
      else if (wort.length > 3 && (liste[i].indexOf(wort) === 0 || wort.indexOf(liste[i]) === 0 && liste[i].length > 3)) { p = Math.max(p, 0.5); }
    }
    return p;
  }
  function bewerten(frage) {
    var w = woerter(frage);
    if (!w.length) return [];
    return daten.map(function (e) {
      if (!e._f) { e._f = woerter(e.f); e._a = woerter(e.a + ' ' + e.s); }
      var punkte = 0;
      w.forEach(function (x) { punkte += 3 * treffer(x, e._f) + treffer(x, e._a); });
      return { e: e, p: punkte / w.length };
    }).filter(function (x) { return x.p >= 1; }).sort(function (a, b) { return b.p - a.p; }).slice(0, 3);
  }
  function kurz(t) {
    if (t.length <= 260) return t;
    var s = t.slice(0, 260);
    return s.slice(0, s.lastIndexOf(' ')) + ' …';
  }
  function el(tag, klasse, text) {
    var e = document.createElement(tag);
    if (klasse) e.className = klasse;
    if (text) e.textContent = text;
    return e;
  }
  // Antwort wie im Chat (Anna 17.11.2026: „ganz simpel wie Google“, „wie mit einem Chatbot“): Frage als Blase rechts,
  // eine kurze Antwort links (ein bis zwei Sätze) mit Link; Folgefragen hängen sich an, höchstens drei Runden sichtbar
  function saetze(t) {
    // nur nach Satzzeichen mit Leerzeichen und Großbuchstaben trennen; „STUDIO AAH!“ und „2.450 €“ bleiben ganz
    var teile = t.replace(/STUDIO AAH!/g, 'STUDIO AAH\u00a7').split(/(?<=[.?!])\s+(?=[A-ZÄÖÜ„])/).map(function (x) { return x.replace(/STUDIO AAH\u00a7/g, 'STUDIO AAH!') + ' '; });
    var aus = teile[0];
    if (aus.length < 120 && teile[1]) aus += teile[1];
    return aus.trim().length > 280 ? kurz(aus.trim()) : aus.trim();
  }
  function link(text, href) {
    var a = el('a', 'textlink', text + ' ');
    a.href = href;
    var pfeil = el('span', null, '→'); pfeil.setAttribute('aria-hidden', 'true'); a.appendChild(pfeil);
    return a;
  }
  function zeigen(frage) {
    var treffer = bewerten(frage)[0];
    var verlauf = ziel.querySelector('.fh-chat') || ziel.appendChild(el('ol', 'fh-chat'));
    var runde = el('li', 'fh-runde');
    runde.appendChild(el('p', 'fh-ich', frage));
    var antwort = el('div', 'fh-sie');
    if (treffer) {
      antwort.appendChild(el('p', null, saetze(treffer.e.a)));
      antwort.appendChild(link('Mehr dazu', treffer.e.u || './'));
    } else {
      antwort.appendChild(el('p', null, 'Dazu habe ich hier noch keine Antwort. Rufen Sie mich an: 0176 830 898 79, oder schreiben Sie mir.'));
      antwort.appendChild(link('Beratung anfragen', 'kontakt/'));
    }
    runde.appendChild(antwort);
    verlauf.appendChild(runde);
    while (verlauf.children.length > 3) verlauf.removeChild(verlauf.firstChild);
    feld.value = '';
    feld.placeholder = 'Noch eine Frage?';
  }
  function laden() {
    if (daten) return Promise.resolve();
    var v = (document.querySelector('script[src*="frag.js"]') || {}).src || '';
    return fetch('daten/fragen.json' + (v.indexOf('?') > 0 ? v.slice(v.indexOf('?')) : '')).then(function (r) { return r.json(); }).then(function (d) { daten = d; });
  }

  feld.addEventListener('focus', function () { laden().catch(function () {}); }, { once: true });
  form.addEventListener('submit', function (ev) {
    var frage = feld.value.trim();
    if (!frage) { ev.preventDefault(); feld.focus(); return; }
    ev.preventDefault();
    laden().then(function () { zeigen(frage); }).catch(function () { form.submit(); });
  });
})();
