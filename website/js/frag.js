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

  // Themen (daten/fragen.json aus werkzeuge/inhalte/hero-themen.json, Anna 17.11.2026): aus jeder Stichwort-Gruppe eines Themas
  // muss ein Wort(anfang) in der Frage stehen; das Thema mit den meisten Gruppen gewinnt, bei Gleichstand das obere
  function woerter(t) {
    return t.toLowerCase().replace(/studio aah!?/g, ' ').replace(/[^a-zäöüß0-9]+/g, ' ').trim().split(' ');
  }
  function passt(gruppe, w) {
    return gruppe.some(function (s) {
      return w.some(function (x) { return s.length <= 3 ? x === s || x === s + 's' : x.indexOf(s) === 0 || (x.length > 4 && x.indexOf(s) > 0 && s.length > 4); });
    });
  }
  function bewerten(frage) {
    var w = woerter(frage), best = null;
    daten.forEach(function (t) {
      if (t.g.every(function (g) { return passt(g, w); }) && (!best || t.g.length > best.g.length)) best = t;
    });
    return best ? [{ e: best }] : [];
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
    // nur nach Satzzeichen mit Leerzeichen und Großbuchstaben trennen; „STUDIO AAH!“, „2.450 €“ und Abkürzungen wie „Dr.“ (Wortverbinder) bleiben ganz
    var teile = t.replace(/STUDIO AAH!/g, 'STUDIO AAH\u00a7').replace(/\b(Dr|Nr|ca|bzw|inkl|z\. B|u\. a|vgl)\. /g, '$1.\u2060 ').split(/(?<=[.?!])\s+(?=[A-ZÄÖÜ„])/).map(function (x) { return x.replace(/STUDIO AAH\u00a7/g, 'STUDIO AAH!').replace(/\u2060/g, '') + ' '; });
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
