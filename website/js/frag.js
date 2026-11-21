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
  // Text mit [Wort](adresse) in Text- und Link-Knoten zerlegen (nie innerHTML)
  function mitLinks(ziel, text) {
    var re = /\[([^\]]+)\]\(([^)\s]+)\)/g, pos = 0, m;
    while ((m = re.exec(text))) {
      if (m.index > pos) ziel.appendChild(document.createTextNode(text.slice(pos, m.index)));
      var a = el('a', null, m[1]); a.href = m[2];
      if (/^https?:/.test(m[2])) { a.target = '_blank'; a.rel = 'noopener'; }   // extern immer in neuem Fenster (Anna 17.11.2026)
      ziel.appendChild(a); pos = re.lastIndex;
    }
    if (pos < text.length) ziel.appendChild(document.createTextNode(text.slice(pos)));
    return ziel;
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
  // Reaktionen wie im Messenger deuten (Anna 20.11.2026: Rakete auf den Preis heißt „passt, finde ich gut“):
  // nur Emojis oder kurze Zustimmung → passende Antwort mit Kontaktwegen; nachdenkliche Emojis → Einladung zu weiteren Fragen
  var letzte = null;
  var JA = ['👍', '🚀', '❤', '😍', '🙌', '✨', '🔥', '✅', '🎉', '🤝', '👏', '💯', '😊', '🥳', '💪', '🙏', '☺', '😀', '😃', '😄', '👌', '😂',
    'ok', 'okay', 'super', 'top', 'toll', 'klasse', 'perfekt', 'prima', 'passt', 'gut', 'sehr', 'cool', 'genial', 'wunderbar', 'danke', 'ja', 'gern', 'gerne', 'mega', 'klingt', 'prima', 'schön', 'fair'];
  var HMM = ['🤔', '😅', '👀', '😕', '🤨', '😬', '🙈', 'hm', 'hmm', 'hmmm', 'teuer', 'zu'];
  var KONTAKT = ['Anrufen: [0176 830 898 79](tel:+4917683089879)', 'Schreiben: [info@studio-aah.de](mailto:info@studio-aah.de)', 'Termin: [Beratung anfragen](kontakt/)'];
  function reaktion(frage) {
    var teile = frage.toLowerCase().match(/\p{Extended_Pictographic}|[a-zäöüß]+/gu);
    if (!teile || teile.length > 4) return null;
    var alle = function (liste) { return teile.every(function (x) { return liste.indexOf(x) >= 0; }); };
    if (alle(JA)) {
      var preis = letzte && /€/.test(letzte.a + ' ' + (letzte.p || []).join(' '));
      return { a: preis ? 'Wunderbar, dann passt der Preis in dein Budget! Lass uns über deine Website sprechen, das Erstgespräch ist kostenlos.'
                        : 'Das freut mich! Wenn du magst, sprechen wir direkt darüber, das Erstgespräch ist kostenlos.', p: KONTAKT };
    }
    if (alle(HMM.concat(JA))) return { a: 'Noch nicht ganz überzeugt? Frag mich gern weiter, zum Beispiel: Wie läuft ein Projekt ab? Oder wir klären es kurz persönlich.', p: KONTAKT };
    return null;
  }
  function zeigen(frage) {
    var eigen = reaktion(frage);
    var treffer = eigen ? { e: eigen } : bewerten(frage)[0];
    if (treffer && !eigen) letzte = treffer.e;
    var verlauf = ziel.querySelector('.fh-chat');
    if (!verlauf) {
      verlauf = ziel.appendChild(el('ol', 'fh-chat'));
      verlauf.appendChild(el('li', 'fh-tag', 'Heute'));
    }
    ton('senden');
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
    // Antwort wie ein Wiki oder die KI-Übersicht bei Google (Anna 20.11.2026): kurze Zusammenfassung, bis zu drei Stichpunkte,
    // Links direkt im Text als [Wort](adresse) aus daten/fragen.json, keine Link-Zeilen mehr unten in der Blase
    if (treffer) {
      var t = treffer.e;
      // Mit Namen und lockerer (Anna 21.11.2026), nur wenn der Name bekannt ist und die Antwort keine eigene Begrüßung hat
      var nm = merk('aah-name').slice(0, 28);
      if (nm && !eigen) {
        var auf = ['Gute Frage, ', 'Klar, ', 'Kurz gesagt, '][Math.floor(Math.random() * 3)];
        antwort.appendChild(el('p', 'fh-anrede', auf + nm + ':'));
      }
      antwort.appendChild(mitLinks(el('p', 'fh-kurz'), t.a));
      if (t.p && t.p.length) {
        var ul = el('ul', 'fh-punkte');
        t.p.forEach(function (x) { ul.appendChild(mitLinks(el('li'), x)); });
        antwort.appendChild(ul);
      }
    } else {
      // Unbekannte Frage (Anna 21.11.2026): drei Wege wie auf der Kontaktseite
      antwort.appendChild(el('p', 'fh-kurz', 'Gute Frage! Die beantworte ich dir lieber persönlich:'));
      var wege = el('p', 'fh-wege');
      [['Termin buchen', 'https://calendar.app.google/muK5JmpfbsXsDEq47', true], ['Anrufen', 'tel:+4917683089879'], ['Schreiben', 'kontakt/']].forEach(function (w) {
        var a = el('a', null, w[0]); a.href = w[1];
        if (w[2]) { a.target = '_blank'; a.rel = 'noopener'; }
        wege.appendChild(a);
      });
      antwort.appendChild(wege);
    }
    antwort.appendChild(zeit(false));
    setTimeout(function () {
      if (tippt.parentNode) { runde.replaceChild(zeile, tippt); ton('antwort'); }
      hinscrollen(runde);
    }, still ? 0 : 900);
  }
  function laden() {
    if (daten) return Promise.resolve();
    var v = (document.querySelector('script[src*="frag.js"]') || {}).src || '';
    return fetch('daten/fragen.json' + (v.indexOf('?') > 0 ? v.slice(v.indexOf('?')) : '')).then(function (r) { return r.json(); }).then(function (d) { daten = d; });
  }

  // Chat schließen (Anna 20.11.2026): X oben rechts, Klick auf die blaue Fläche oder Esc führt zurück zum Feld mit Unterzeile
  var START = feld.placeholder, panel = form.closest('.hl-panel'), zu = document.querySelector('[data-frag-zu]');
  function schliessen() {
    if (!ziel.textContent.trim()) return;
    ziel.innerHTML = ''; feld.value = ''; feld.placeholder = START; modus();
  }
  if (zu) zu.addEventListener('click', schliessen);
  if (panel) panel.addEventListener('click', function (ev) { if (ev.target === panel) schliessen(); });
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && panel && panel.contains(document.activeElement)) schliessen(); });

  // Eingabe wie bei WhatsApp (Anna 20.11.2026): runder Button mit Papierflieger, rechts im Feld eine Emoji-Auswahl.
  // Leise Töne beim Senden und bei der Antwort. Diktieren entfernt (Anna 21.11.2026).
  var senden = form.querySelector('[data-senden]'), emojiAuf = form.querySelector('[data-emoji-auf]'), emojis = form.querySelector('.hl-emojis');

  // Töne aus dem Browser selbst (Web Audio), keine Dateien, nur nach einem Klick
  var klang = null;
  function ton(art) {
    try {
      klang = klang || new (window.AudioContext || window.webkitAudioContext)();
      var folge = { senden: [[620, 0, .07], [930, .06, .08]], antwort: [[880, 0, .1], [1320, .09, .14]] }[art];
      folge.forEach(function (n) {
        var o = klang.createOscillator(), g = klang.createGain(), t0 = klang.currentTime + n[1];
        o.type = 'sine'; o.frequency.value = n[0];
        g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(0.06, t0 + 0.01); g.gain.exponentialRampToValueAtTime(0.0001, t0 + n[2]);
        o.connect(g); g.connect(klang.destination); o.start(t0); o.stop(t0 + n[2] + 0.02);
      });
    } catch (e) {}
  }

  function beispiel() { return /\?$/.test(feld.placeholder) && feld.placeholder !== 'Noch eine Frage?' ? feld.placeholder : ''; }
  function modus() {}

  // Emoji-Auswahl: fügt an der Schreibmarke ein, bleibt offen wie bei WhatsApp, schließt mit Esc oder Klick daneben
  function emojiPanel(auf) {
    if (!emojis) return;
    emojis.hidden = !auf; emojiAuf.setAttribute('aria-expanded', auf ? 'true' : 'false');
  }
  if (emojiAuf) emojiAuf.addEventListener('click', function () { emojiPanel(emojis.hidden); });
  if (emojis) emojis.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-emoji]'); if (!b) return;
    var a = feld.selectionStart == null ? feld.value.length : feld.selectionStart, e = feld.selectionEnd == null ? a : feld.selectionEnd;
    feld.value = (feld.value.slice(0, a) + b.textContent + feld.value.slice(e)).slice(0, 200);
    var pos = a + b.textContent.length; feld.focus(); try { feld.setSelectionRange(pos, pos); } catch (x) {}
    modus();
  });
  document.addEventListener('click', function (ev) { if (emojis && !emojis.hidden && !form.contains(ev.target)) emojiPanel(false); });

  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && emojis && !emojis.hidden) emojiPanel(false);
  });

  feld.addEventListener('focus', function () { laden().catch(function () {}); }, { once: true });
  // Erst der Name (Anna 21.11.2026: „Hi, ich bin Anna. Wie heißt du?“, Platzhalter wie im 4. Entwurf). Der Name bleibt nur in diesem
  // Browser-Tab (sessionStorage), wird nirgends hingeschickt. Danach wird das Feld wieder zum Frag-Feld.
  var FRAGE = form.getAttribute('data-frag-beispiel') || '';
  var titel = document.querySelector('[data-frag-titel]');
  function merk(k, v) { try { if (v === undefined) return sessionStorage.getItem(k) || ''; sessionStorage.setItem(k, v); } catch (e) { return ''; } return v; }
  var nameNoetig = form.hasAttribute('data-frag-name');
  function alsFrage(name) {
    nameNoetig = false; START = FRAGE || START; feld.placeholder = START;
    feld.setAttribute('maxlength', '200'); feld.setAttribute('enterkeyhint', 'search');
    var lab = form.querySelector('label'); if (lab) lab.textContent = 'Deine Frage an STUDIO AAH!';
    if (titel) titel.textContent = 'Hi ' + name + '! Wie kann ich dir weiterhelfen?';
    // Name aus dem Hero auch im letzten Abschnitt aufgreifen (Anna 22.11.2026: „Paul, bist du fit für 2027?“)
    var nf = document.querySelector('[data-name-frage]'); if (nf) nf.textContent = name + ', bist du fit für 2027?';
    form.removeAttribute('data-frag-name');   // jetzt erscheinen die Frage-Chips
  }
  var gemerkt = nameNoetig ? merk('aah-name').slice(0, 28) : '';
  if (gemerkt) alsFrage(gemerkt);
  function begruessen(name) {
    merk('aah-name', name);
    var verlauf = ziel.querySelector('.fh-chat') || ziel.appendChild(el('ol', 'fh-chat'));
    if (!verlauf.querySelector('.fh-tag')) verlauf.appendChild(el('li', 'fh-tag', 'Heute'));
    ton('senden');
    var runde = el('li', 'fh-runde'), ich = el('p', 'fh-ich', name);
    ich.appendChild(zeit(true)); runde.appendChild(ich);
    var zeile = el('div', 'fh-zeile'), foto = el('img', 'fh-foto');
    foto.src = 'bilder/anna-haertelt-studio-blau-rund-192.jpg'; foto.alt = ''; foto.width = 32; foto.height = 32;
    zeile.appendChild(foto);
    var antwort = el('div', 'fh-sie');
    antwort.appendChild(el('p', 'fh-name', 'Anna Härtelt'));
    antwort.appendChild(el('p', 'fh-kurz', 'Schön, dich kennenzulernen, ' + name + '! Wie kann ich dir weiterhelfen?'));
    antwort.appendChild(zeit(false));
    zeile.appendChild(antwort); runde.appendChild(zeile);
    verlauf.appendChild(runde); hinscrollen(runde);
    feld.value = ''; alsFrage(name); ton('antwort'); feld.focus();
  }
  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    if (nameNoetig) {
      var name = feld.value.trim().replace(/[<>]/g, '').slice(0, 28);
      if (!name) { feld.focus(); return; }
      emojiPanel(false); begruessen(name); return;
    }
    // Leeres Feld: beim ersten Mal die Beispielfrage aus dem Platzhalter beantworten (Anna 20.11.2026: „muss nichts eingeben,
    // kann einfach nur Antwort klicken und sehe schon die Funktionalität“)
    var frage = feld.value.trim() || beispiel();
    if (!frage) { feld.focus(); return; }
    emojiPanel(false);
    laden().then(function () { zeigen(frage); modus(); }).catch(function () { form.submit(); });
  });
})();
