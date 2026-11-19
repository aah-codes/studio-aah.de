// Frag-Feld im Hero der Startseite (Anna 16.11.2026): sucht nur in den häufigen Fragen der Website (daten/fragen.json,
// erzeugt von werkzeuge/fragen-index.py) und zeigt die passendsten Antworten mit Link. Alles läuft im Browser, nichts wird gesendet.
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
  // eine kurze Antwort links (ein bis zwei Sätze) mit Link; neueste Runde oben, höchstens drei Runden sichtbar
  function link(text, href) {
    var extern = /^https?:/.test(href);
    var a = el('a', 'fh-quelle', text + ' ');
    a.href = href;
    if (extern) { a.target = '_blank'; a.rel = 'noopener'; }   // LinkedIn & Co. immer in neuem Fenster (Anna 17.11.2026)
    var pfeil = el('span', null, extern ? '↗' : '→'); pfeil.setAttribute('aria-hidden', 'true'); a.appendChild(pfeil);
    return a;
  }
  // Chat nach Vorbild WhatsApp (Anna 18.11.2026: „nimm whatsapp als inspo für chat“): Frage als blaue Blase rechts mit Uhrzeit
  // und Haken, kurz „schreibt …“, dann Annas Antwort als weiße Blase links mit Foto und Name; Links als Zeilen unten in der Blase.
  // Reihenfolge wie im Messenger: neueste Runde unten direkt über dem Feld, höchstens drei Runden
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function uhrzeit() {
    var d = new Date();
    return ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2);
  }
  function zeit(eigen) {
    var s = el('span', 'fh-zeit', uhrzeit());
    if (eigen) { var h = el('span', 'fh-haken', '✓✓'); h.setAttribute('aria-hidden', 'true'); s.appendChild(h); }
    return s;
  }
  function hinscrollen(e) { ziel.scrollTop = Math.max(0, e.offsetTop - 12); }
  function zeigen(frage) {
    var treffer = bewerten(frage)[0];
    var verlauf = ziel.querySelector('.fh-chat');
    if (!verlauf) {
      verlauf = ziel.appendChild(el('ol', 'fh-chat'));
      verlauf.appendChild(el('li', 'fh-tag', 'Heute'));
    }
    var runde = el('li', 'fh-runde');
    var ich = el('p', 'fh-ich', frage);
    ich.appendChild(zeit(true));
    runde.appendChild(ich);
    var tippt = el('p', 'fh-tippt');
    tippt.setAttribute('aria-label', 'Anna schreibt');
    tippt.appendChild(el('span')); tippt.appendChild(el('span')); tippt.appendChild(el('span'));
    runde.appendChild(tippt);
    verlauf.appendChild(runde);
    var runden = verlauf.querySelectorAll('.fh-runde');
    if (runden.length > 3) verlauf.removeChild(runden[0]);
    hinscrollen(runde);
    feld.value = '';
    feld.placeholder = 'Noch eine Frage?';

    var zeile = el('div', 'fh-zeile');
    var foto = el('img', 'fh-foto');
    foto.src = 'bilder/anna-haertelt-studio-blau-rund-192.jpg'; foto.alt = ''; foto.width = 32; foto.height = 32;
    zeile.appendChild(foto);
    var antwort = el('div', 'fh-sie');
    zeile.appendChild(antwort);
    antwort.appendChild(el('p', 'fh-name', 'Anna Härtelt'));
    var quellen = el('p', 'fh-quellen');
    if (treffer) {
      var t = treffer.e;
      antwort.appendChild(el('p', 'fh-kurz', t.a));
      if (t.p && t.p.length) {
        var ul = el('ul', 'fh-punkte');
        t.p.forEach(function (x) { ul.appendChild(el('li', null, x)); });
        antwort.appendChild(ul);
      }
      t.l.forEach(function (l) { quellen.appendChild(link(l[0], l[1])); });
    } else {
      antwort.appendChild(el('p', 'fh-kurz', 'Gute Frage! Dazu habe ich hier noch keine fertige Antwort. Rufen Sie mich gern an: 0176 830 898 79, oder schreiben Sie mir.'));
      quellen.appendChild(link('Beratung anfragen', 'kontakt/'));
    }
    antwort.appendChild(zeit(false));
    if (quellen.childNodes.length) antwort.appendChild(quellen);
    setTimeout(function () {
      if (tippt.parentNode) runde.replaceChild(zeile, tippt);
      hinscrollen(runde);
    }, still ? 0 : 900);
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
