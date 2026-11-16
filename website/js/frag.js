// Frag-Feld im Hero der Startseite (Anna 16.11.2026): sucht nur in den häufigen Fragen der Website (daten/fragen.json,
// erzeugt von werkzeuge/fragen-index.py) und zeigt die passendsten Antworten mit Link. Alles läuft im Browser, nichts wird gesendet.
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
  function zeigen(frage) {
    var liste = bewerten(frage);
    ziel.textContent = '';
    if (!liste.length) {
      var leer = el('div', 'fh-leer');
      leer.appendChild(el('p', null, 'Dazu habe ich hier noch keine Antwort. Fragen Sie mich direkt:'));
      var wege = el('p', 'fh-leer-wege');
      var tel = el('a', 'textlink', '0176 830 898 79'); tel.href = 'tel:+4917683089879';
      var mail = el('a', 'textlink', 'info@studio-aah.de'); mail.href = 'mailto:info@studio-aah.de';
      var anfrage = el('a', 'textlink', 'Beratung anfragen '); anfrage.href = 'kontakt/';
      var pfeil = el('span', null, '→'); pfeil.setAttribute('aria-hidden', 'true'); anfrage.appendChild(pfeil);
      wege.appendChild(tel); wege.appendChild(document.createTextNode(' · ')); wege.appendChild(mail); wege.appendChild(document.createTextNode(' · ')); wege.appendChild(anfrage);
      leer.appendChild(wege);
      ziel.appendChild(leer);
      return;
    }
    var ul = el('ul', 'fh-liste');
    liste.forEach(function (x) {
      var li = el('li');
      li.appendChild(el('h2', 'fh-frage', x.e.f));
      li.appendChild(el('p', null, kurz(x.e.a)));
      var a = el('a', 'textlink', 'Mehr dazu: ' + x.e.s + ' ');
      a.href = x.e.u || './';
      var pfeil = el('span', null, '→'); pfeil.setAttribute('aria-hidden', 'true'); a.appendChild(pfeil);
      li.appendChild(a);
      ul.appendChild(li);
    });
    ziel.appendChild(ul);
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
