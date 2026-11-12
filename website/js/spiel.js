/* Hero-Spiel „Play the game“ durch Leipzig (Anna 10.11.2026, Fassung 3; Entwurfsordner website/entwurf-hero-spiel/ nur lokal)
   Eigenes Lauf-und-Spring-Spiel in Annas Bildsprache (kein Nachbau eines bestehenden Spiels, keine fremden Töne oder Figuren).
   – Freistehend, nur Bodenlinie. Die Bauhaus-Figur läuft schnell zur Bildmitte und dann durch Leipzig
     (Völkerschlachtdenkmal, Weisheitszahn, Hauptbahnhof, Baustelle, Autos, Bäume).
   – Fünf Probleme laufen herum. Draufspringen verwandelt sie in das, was Unternehmen wollen:
       Funkstille → neue Kunden · Unsichtbar (Auge zu) → Auge geht auf, Reichweite · Tool-Chaos → Zeit
       Zeitfresser → Zeit · Ebbe in der Kasse → Geld. Seitlich dagegen kostet ein Leben (drei Leben).
   – Die Fachkraft läuft weg; gefangen: ein Mitarbeiter mehr, die Figur wächst und hält einen Treffer aus.
   – Schwarze Blöcke von unten anstoßen: Leistung fliegt heraus bis in die Schrift. Alle fünf gefunden: nächstes Level.
   – Das Spiel läuft weiter, bis die Leben weg sind; dann „Game over“ mit Play again.
   – Beim Ankommen steht alles still (Anna 12.11.2026, ersetzt die laufende Demo): Standbild und rechts eine Card mit Überschrift
     und Spielen-Button. „Spielen“ startet zuerst ein Intro, das in der Card Schritt für Schritt erklärt, was man tun kann
     (auch einmal einen Block von unten anstoßen). Der Button in der Card startet dann das Spiel.
   – Oben nur die drei Leben, kein Geld; die Chips unter dem Spiel zählen die ergriffenen Lösungen. Ton aus, bis man ihn einschaltet. */
(function () {
  'use strict';
  var wurzel = document.querySelector('[data-spiel]');
  if (!wurzel) return;
  var cv = wurzel.querySelector('canvas'), c = cv.getContext('2d');
  var W = 960, H = 290, BODEN = 266;   // Desktop 290 hoch (Anna 12.11.2026: Platz über dem Kopf, damit man die Arme beim Sprung sieht)
  var F = { sch: '#0e1011', ws: '#ffffff', bl: '#2a5fe6', rot: '#ff3b2f', pink: '#ff4fa3', rosa: '#ff8fc8', gelb: '#ffe600', gr: '#9a9d9e', grh: '#d6d8d9' };
  // Die fünf Lösungen in der Reihenfolge eines Projekts (Anna 10.11.2026); jedes Level beginnt wieder vorn, wie beim iterativen Arbeiten
  var LEISTUNGEN = [
    { name: 'Markenbildung', form: 'quadrat', farbe: F.rot }, { name: 'UI/UX', form: 'halbkreis', farbe: F.pink },
    { name: 'Webdesign', form: 'kreis', farbe: F.bl }, { name: 'Marketing & Vertrieb', form: 'halbkreis', farbe: F.sch },
    { name: 'KI & Digitalisierung', form: 'dreieck', farbe: F.gelb }];
  // Die fünf Probleme und was aus ihnen wird
  var PROBLEME = [
    { art: 'funkstille', name: 'Funkstille', b: 40, h: 46, lohn: 'kunden', menge: 1, text: '+1 Kunde' },
    { art: 'unsichtbar', name: 'Unsichtbar', b: 44, h: 40, lohn: 'reichweite', menge: 250, text: '+250 Reichweite' },
    { art: 'toolchaos', name: 'Tool-Chaos', b: 40, h: 40, lohn: 'zeit', menge: 2, text: '+2 Stunden' },
    { art: 'zeitfresser', name: 'Zeitfresser', b: 48, h: 44, lohn: 'zeit', menge: 3, text: '+3 Stunden' },
    { art: 'ebbe', name: 'Ebbe in der Kasse', b: 44, h: 38, lohn: 'euro', menge: 500, text: '+500 €' },
    // Der Wettbewerb rennt Ihnen entgegen: draufspringen hält den Kunden (Stammkunde), drüberspringen lässt ihn einen Kunden wegschnappen
    { art: 'konkurrenz', name: 'Wettbewerb', b: 34, h: 62, lohn: 'stammkunden', menge: 1, text: '+1 Stammkunde' }];
  var chips = wurzel.querySelectorAll('[data-leistung]');
  // Zähler je Chip: wie oft die Lösung in diesem Spiel schon ergriffen wurde
  var zahlen = Array.prototype.map.call(chips, function (ch) {
    var z = document.createElement('b'); z.className = 'sl-zahl'; z.setAttribute('aria-hidden', 'true'); z.hidden = true;
    (ch.querySelector('a') || ch).appendChild(z); return z; });
  function chipZahl(i, n) { if (!zahlen[i]) return; zahlen[i].textContent = n; zahlen[i].hidden = false; zahlen[i].classList.toggle('sl-null', !n); }
  var startKnopf = wurzel.querySelector('[data-start]'), kartenEl = wurzel.querySelector('[data-karte]');
  var kSchritt = wurzel.querySelector('[data-karte-schritt]'), kTitel = wurzel.querySelector('[data-karte-titel]'), kText = wurzel.querySelector('[data-karte-text]');
  var modus = 'still';   // still → intro → bereit → spiel
  // Card: Schrittzeile, Überschrift, Text und Button-Beschriftung; ohne Titel verschwindet die Card
  function karte(titel, text, schritt, knopf) {
    kartenEl.hidden = !titel; if (!titel) return;
    kTitel.textContent = titel; kText.textContent = text || ''; kText.hidden = !text;
    kSchritt.textContent = schritt || ''; kSchritt.hidden = !schritt;
    startKnopf.firstChild.nodeValue = (knopf || 'Spielen') + ' ';
  }
  var knopfTon = wurzel.querySelector('[data-ton]'), knopfPause = wurzel.querySelector('[data-pause]');
  var bilanzBox = wurzel.querySelector('[data-sieg]'), bilanzText = wurzel.querySelector('[data-bilanz]');
  var ruhig = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var zahl = new Intl.NumberFormat('de-DE');

  function groesse() {
    var r = cv.getBoundingClientRect();
    H = r.width < 600 ? 360 : 290; BODEN = H - 24;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.width * H / W * dpr);
  }

  // ---------- Ton ----------
  var tonAn = false, ac = null;
  try { tonAn = localStorage.getItem('spiel-ton') === 'an'; } catch (e) {}
  function tonKnopf() { knopfTon.setAttribute('aria-pressed', tonAn ? 'true' : 'false'); knopfTon.setAttribute('aria-label', tonAn ? 'Ton ausschalten' : 'Ton einschalten'); }
  tonKnopf();
  knopfTon.addEventListener('click', function () { tonAn = !tonAn; tonKnopf(); try { localStorage.setItem('spiel-ton', tonAn ? 'an' : 'aus'); } catch (e) {} });
  function ton(folge) {
    if (!tonAn || !s || s.demo) return;
    try {
      ac = ac || new (window.AudioContext || window.webkitAudioContext)();
      var t = ac.currentTime;
      folge.forEach(function (n) {
        var o = ac.createOscillator(), g = ac.createGain();
        o.type = n[2] || 'square'; o.frequency.setValueAtTime(n[0], t);
        if (n[3]) o.frequency.exponentialRampToValueAtTime(n[3], t + n[1]);
        g.gain.setValueAtTime(.07, t); g.gain.exponentialRampToValueAtTime(.0001, t + n[1]);
        o.connect(g); g.connect(ac.destination); o.start(t); o.stop(t + n[1] + .02); t += n[1] * .85;
      });
    } catch (e) {}
  }
  var TON = { sprung: [[380, .13, 'square', 820]], platt: [[260, .07, 'square', 80], [520, .1, 'square', 1040]],
    block: [[200, .05], [700, .08, 'square', 1400]], muenze: [[1318, .05], [1760, .1]], sammeln: [[988, .06], [1318, .14]],
    wachsen: [[330, .06], [392, .06], [494, .06], [659, .06], [784, .06], [988, .14]], schrumpfen: [[600, .1, 'sawtooth', 200]],
    autsch: [[520, .12, 'sawtooth', 260]], ende: [[520, .15, 'sawtooth', 280], [280, .3, 'sawtooth', 110]],
    level: [[523, .1], [659, .1], [784, .1], [1046, .12], [784, .08], [1046, .35]] };

  // ---------- Zustand ----------
  var s;
  function neu(demo) {
    s = { demo: !!demo, lauf: !!demo, aus: false, pause: false, t: 0, tempo: 3.5, weg: 0, gross: false, level: 1, leben: 3,
          punkte: { euro: 0, reichweite: 0, kunden: 0, stammkunden: 0, fachkraefte: 0, zeit: 0 },
          f: { x: 110, y: BODEN, vy: 0, amBoden: true, blink: 0 }, gegner: [], bloecke: [], gaben: [], muenzen: [], kraft: null,
          funken: [], blasen: [], lohn: [], naechstG: demo ? 1e9 : 70, naechstB: demo ? 1e9 : 70, naechstK: demo ? 1e9 : 360, naechstM: 1e9,
          gesammelt: [], bekannt: {}, zaehler: [0, 0, 0, 0, 0] };
    chips.forEach(function (ch, i) { ch.classList.remove('ist-gesammelt'); chipZahl(i, 0); });
    if (bilanzBox) bilanzBox.hidden = true;
    pauseAnzeige();
  }

  // ---------- Zeichnen: Grundformen ----------
  function form(art, x, y, g, farbe) {
    c.fillStyle = farbe; c.beginPath();
    if (art === 'kreis') c.arc(x, y, g / 2, 0, Math.PI * 2);
    else if (art === 'quadrat') c.rect(x - g / 2, y - g / 2, g, g);
    else if (art === 'halbkreis') c.arc(x, y + g / 4, g / 2, Math.PI, 0);
    else { c.moveTo(x + g / 2, y - g / 2); c.lineTo(x + g / 2, y + g / 2); c.lineTo(x - g / 2, y + g / 2); }
    c.fill();
  }
  function herz(x, y, g, farbe) {   // Grundform-Herz: gedrehtes Quadrat und zwei Halbkreise
    c.save(); c.translate(x, y); c.fillStyle = farbe; c.rotate(Math.PI / 4); c.fillRect(-g / 2, -g / 2, g, g); c.rotate(-Math.PI / 4);
    c.beginPath(); c.arc(-g * .35, -g * .35, g * .5, 0, 7); c.arc(g * .35, -g * .35, g * .5, 0, 7); c.fill(); c.restore();
  }
  function muenze(x, y, r) {
    c.fillStyle = F.gelb; c.beginPath(); c.arc(x, y, r, 0, 7); c.fill();
    c.fillStyle = F.sch; c.font = '700 ' + Math.round(r * 1.2) + 'px Manrope, system-ui, sans-serif'; c.textAlign = 'center'; c.fillText('€', x, y + r * .42); c.textAlign = 'left';
  }
  function wiederhole(x, laenge, tempo) { return ((x - s.weg * tempo) % laenge + laenge) % laenge - 120; }
  function beschriftung(t, x, y) { c.fillStyle = F.gr; c.font = '600 12px Manrope, system-ui, sans-serif'; c.textAlign = 'center'; c.fillText(t, x, y); c.textAlign = 'left'; }

  // ---------- Leipzig ----------
  // Skyline aus Grundformen (Anna 12.11.2026): vorn die Wahrzeichen in Hellgrau mit Häuserreihen dazwischen,
  // hinten eine ruhigere Dachlandschaft in Creme. Eigene Zeichnung, nur Silhouetten ohne Beschriftung.
  function zufall(z) { return function () { z = (z * 16807) % 2147483647; return z / 2147483647; }; }
  function umlauf(x, laenge, tempo, rand) { var sx = ((x - s.weg * tempo) % laenge + laenge) % laenge; return sx > W + (rand || 0) ? sx - laenge : sx; }
  function vieleck(p) { c.beginPath(); c.moveTo(p[0], p[1]); for (var i = 2; i < p.length; i += 2) c.lineTo(p[i], p[i + 1]); c.closePath(); c.fill(); }
  function kuppel(x, y, r) { c.beginPath(); c.arc(x, y, r, Math.PI, 0); c.fill(); }
  function spitze(x, y, b, h) { vieleck([x - b / 2, y, x, y - h, x + b / 2, y]); }
  function weiss(f) { c.fillStyle = F.ws; f(); c.fillStyle = F.grh; }
  var B;   // Bodenlinie beim Zeichnen
  var WAHRZEICHEN = [
    { x: 70, b: 162, z: function (x) {                       // Gewandhaus: Glasfront, schräges Dach
      c.fillRect(x, B - 70, 150, 70); vieleck([x - 6, B - 70, x + 156, B - 94, x + 156, B - 70]);
      weiss(function () { for (var i = 0; i < 6; i++) c.fillRect(x + 12 + i * 23, B - 58, 3, 50); }); } },
    { x: 262, b: 44, z: function (x) {                       // Mendebrunnen: Becken und Obelisk
      c.fillRect(x, B - 10, 44, 10); c.fillRect(x + 8, B - 18, 28, 8); c.fillRect(x + 17, B - 66, 10, 48); spitze(x + 22, B - 66, 12, 18); } },
    { x: 336, b: 64, z: function (x) {                       // Weisheitszahn (City-Hochhaus): hohe Scheibe mit gerundeter Krone und Antenne
      c.beginPath(); c.moveTo(x, B); c.lineTo(x, B - 196); c.quadraticCurveTo(x + 54, B - 180, x + 64, B - 146); c.lineTo(x + 64, B); c.closePath(); c.fill();
      c.fillRect(x + 4, B - 218, 3, 22);
      weiss(function () { for (var i = 0; i < 4; i++) c.fillRect(x + 12 + i * 13, B - 140, 2, 132); }); } },
    { x: 418, b: 84, z: function (x) {                       // Paulinum: steiler Giebel mit hohem Spitzbogenfenster
      c.fillRect(x, B - 66, 84, 66); vieleck([x, B - 66, x + 42, B - 132, x + 84, B - 66]);
      c.fillRect(x - 2, B - 82, 5, 82); c.fillRect(x + 81, B - 82, 5, 82);
      weiss(function () { c.fillRect(x + 36, B - 92, 12, 70); spitze(x + 42, B - 92, 12, 14); }); } },
    { x: 524, b: 200, z: function (x) {                      // Oper: breiter Block mit Attika
      c.fillRect(x, B - 62, 200, 62); c.fillRect(x + 20, B - 76, 160, 14);
      weiss(function () { for (var i = 0; i < 8; i++) c.fillRect(x + 14 + i * 24, B - 52, 8, 30); }); } },
    { x: 900, b: 170, z: function (x) {                      // Neues Rathaus: Block mit hohem Turm, Uhr und Kuppel
      c.fillRect(x, B - 72, 170, 72); vieleck([x, B - 72, x + 10, B - 88, x + 160, B - 88, x + 170, B - 72]);
      c.fillRect(x + 6, B - 104, 14, 32); spitze(x + 13, B - 104, 16, 16);
      c.fillRect(x + 70, B - 166, 32, 94); c.fillRect(x + 66, B - 172, 40, 6); kuppel(x + 86, B - 172, 15);
      c.fillRect(x + 83, B - 198, 6, 14); spitze(x + 86, B - 198, 8, 14);
      weiss(function () { c.beginPath(); c.arc(x + 86, B - 146, 7, 0, 7); c.fill(); for (var i = 0; i < 5; i++) c.fillRect(x + 16 + i * 32, B - 56, 8, 22); }); } },
    { x: 1250, b: 190, z: function (x) {                     // Thomaskirche: Schiff mit steilem Dach, Turm mit Haube
      c.fillRect(x, B - 60, 144, 60); vieleck([x - 4, B - 60, x + 72, B - 114, x + 148, B - 60]);
      c.fillRect(x + 144, B - 136, 34, 136); c.fillRect(x + 140, B - 140, 42, 6); kuppel(x + 161, B - 140, 14);
      c.fillRect(x + 158, B - 166, 6, 14); spitze(x + 161, B - 166, 8, 18);
      weiss(function () { for (var i = 0; i < 4; i++) { c.fillRect(x + 20 + i * 30, B - 46, 8, 30); spitze(x + 24 + i * 30, B - 46, 8, 8); } }); } },
    { x: 1580, b: 196, z: function (x) {                     // Altes Rathaus: langes Haus, Giebel im Dach, schlanker Turm
      c.fillRect(x, B - 54, 196, 54); vieleck([x, B - 54, x + 12, B - 84, x + 184, B - 84, x + 196, B - 54]);
      for (var i = 0; i < 4; i++) spitze(x + 32 + i * 44, B - 84, 22, 16);
      c.fillRect(x + 112, B - 124, 16, 70); kuppel(x + 120, B - 124, 10); c.fillRect(x + 117, B - 144, 6, 12); spitze(x + 120, B - 144, 6, 12);
      weiss(function () { for (var i = 0; i < 9; i++) { c.fillRect(x + 8 + i * 21, B - 20, 10, 20); kuppel(x + 13 + i * 21, B - 20, 5); } }); } },
    { x: 1900, b: 260, z: function (x) {                     // Hauptbahnhof: zwei Eckbauten, Halle mit Bögen
      c.fillRect(x, B - 74, 44, 74); c.fillRect(x + 216, B - 74, 44, 74); spitze(x + 22, B - 74, 44, 12); spitze(x + 238, B - 74, 44, 12);
      c.fillRect(x + 44, B - 44, 172, 44); for (var i = 0; i < 4; i++) kuppel(x + 65 + i * 43, B - 44, 21);
      weiss(function () { [x + 22, x + 238].forEach(function (m) { c.fillRect(m - 8, B - 48, 16, 30); kuppel(m, B - 48, 8); }); }); } },
    { x: 2250, b: 200, z: function (x) {                     // Reichsgericht: Eckpavillons, Säulen, große Kuppel
      c.fillRect(x, B - 60, 200, 60); c.fillRect(x, B - 72, 30, 12); c.fillRect(x + 170, B - 72, 30, 12);
      c.fillRect(x + 66, B - 84, 68, 24); c.fillRect(x + 78, B - 106, 44, 22); kuppel(x + 100, B - 106, 26);
      c.fillRect(x + 96, B - 144, 8, 14); spitze(x + 100, B - 144, 8, 12);
      weiss(function () { for (var i = 0; i < 6; i++) c.fillRect(x + 72 + i * 11, B - 56, 3, 46); }); } },
    { x: 2560, b: 200, z: function (x) {                     // Völkerschlachtdenkmal: Stufen, wuchtiger Körper, Wächterkranz, Kuppel
      c.fillRect(x, B - 12, 200, 12); c.fillRect(x + 22, B - 26, 156, 14);
      vieleck([x + 42, B - 26, x + 62, B - 112, x + 138, B - 112, x + 158, B - 26]);
      c.fillRect(x + 54, B - 120, 92, 8); for (var i = 0; i < 8; i++) c.fillRect(x + 57 + i * 11.5, B - 136, 8, 16);
      kuppel(x + 100, B - 134, 32);
      weiss(function () { c.fillRect(x + 92, B - 72, 16, 46); kuppel(x + 100, B - 72, 8); }); } }];
  var STADT_L = W * 3, HINTEN_L = W * 2, HAEUSER = [], DAECHER = [];
  (function () {   // Häuserreihen zwischen den Wahrzeichen und eine Dachlandschaft dahinter, immer gleich (fester Startwert)
    var r = zufall(11), frei = 0;
    WAHRZEICHEN.concat([{ x: STADT_L, b: 0 }]).forEach(function (w) {
      var x = frei + 4;
      while (w.x - x > 30) { var hb = Math.min(w.x - 4 - x, 26 + Math.floor(r() * 34)); HAEUSER.push({ x: x, b: hb, h: 24 + Math.floor(r() * 30), dach: Math.floor(r() * 3) }); x += hb + 2; }
      frei = w.x + w.b;
    });
    var r2 = zufall(5), x2 = 0;
    while (x2 < HINTEN_L) { var db = 36 + Math.floor(r2() * 70); DAECHER.push({ x: x2, b: db, h: 40 + Math.floor(r2() * 64), dach: Math.floor(r2() * 4) }); x2 += db; }
  })();
  function haus(x, b, h, dach) {
    c.fillRect(x, B - h, b, h);
    if (dach === 1) vieleck([x, B - h, x + b / 2, B - h - Math.min(22, b * .45), x + b, B - h]);
    else if (dach === 2) c.fillRect(x + b * .25, B - h - 8, b * .5, 8);
    else if (dach === 3) kuppel(x + b / 2, B - h, Math.min(14, b / 3));
  }
  function leipzig() {
    B = BODEN;
    c.fillStyle = '#eeece7';                                            // hinten: Dachlandschaft in Creme, langsamer
    DAECHER.forEach(function (d) { var x = umlauf(d.x, HINTEN_L, .06); if (x + d.b > 0) haus(x, d.b, d.h, d.dach); });
    c.fillStyle = F.grh;                                                // vorn: Häuser und Wahrzeichen
    HAEUSER.forEach(function (d) { var x = umlauf(d.x, STADT_L, .12); if (x + d.b > 0) haus(x, d.b, d.h, d.dach); });
    WAHRZEICHEN.forEach(function (w) { var x = umlauf(w.x, STADT_L, .12); if (x + w.b + 10 > 0) w.z(x); });
    // eine Baustelle: Kran und Absperrung
    var x = umlauf(900, W + 900, .3, 60);
    c.strokeStyle = F.sch; c.lineWidth = 2;                                         // Gittermast
    c.strokeRect(x, BODEN - 170, 14, 170); c.beginPath();
    for (var z = 0; z < 8; z++) { c.moveTo(x, BODEN - z * 21); c.lineTo(x + 14, BODEN - (z + 1) * 21); }
    c.moveTo(x - 50, BODEN - 170); c.lineTo(x + 140, BODEN - 170); c.moveTo(x - 50, BODEN - 162); c.lineTo(x + 140, BODEN - 162);   // Ausleger
    for (var a2 = 0; a2 < 9; a2++) { c.moveTo(x - 50 + a2 * 21, BODEN - 162); c.lineTo(x - 40 + a2 * 21, BODEN - 170); }
    c.moveTo(x + 7, BODEN - 196); c.lineTo(x - 50, BODEN - 170); c.moveTo(x + 7, BODEN - 196); c.lineTo(x + 140, BODEN - 170);   // Abspannung
    c.moveTo(x + 7, BODEN - 196); c.lineTo(x + 7, BODEN - 170); c.moveTo(x + 112, BODEN - 162); c.lineTo(x + 112, BODEN - 110); c.stroke();
    c.fillStyle = F.gr; c.fillRect(x - 50, BODEN - 162, 20, 16);                   // Gegengewicht
    c.fillStyle = F.gelb; c.fillRect(x + 14, BODEN - 158, 16, 14);                 // Kabine
    c.fillStyle = F.sch; c.fillRect(x + 108, BODEN - 112, 8, 4);                   // Haken
    c.fillStyle = F.gelb; c.fillRect(x + 100, BODEN - 106, 24, 18);                // Last
    for (var b = 0; b < 5; b++) { c.fillStyle = b % 2 ? F.ws : F.rot; c.fillRect(x + 20 + b * 14, BODEN - 28, 14, 10); }
    c.fillStyle = F.sch; c.fillRect(x + 22, BODEN - 18, 3, 18); c.fillRect(x + 84, BODEN - 18, 3, 18);
    // zwei Bäume, ein Auto
    [[200, F.pink, 22], [1100, F.gelb, 18]].forEach(function (t) {
      var bx = umlauf(t[0], W + 700, .45, 30); c.fillStyle = F.sch; c.fillRect(bx - 2, BODEN - t[2] * 2, 4, t[2] * 2); c.fillStyle = t[1]; c.beginPath(); c.arc(bx, BODEN - t[2] * 2.6, t[2], 0, 7); c.fill(); });
    var ax = umlauf(400, W + 1400, .75); c.fillStyle = F.bl; c.fillRect(ax, BODEN - 26, 58, 16); c.beginPath(); c.arc(ax + 26, BODEN - 26, 16, Math.PI, 0); c.fill();
    c.fillStyle = F.ws; c.fillRect(ax + 18, BODEN - 36, 16, 8); c.fillStyle = F.sch; c.beginPath(); c.arc(ax + 14, BODEN - 8, 7, 0, 7); c.arc(ax + 46, BODEN - 8, 7, 0, 7); c.fill();
  }

  // ---------- Figuren ----------
  function figur(x, y, k, rock, laeuft, hoch) {
    c.save(); c.translate(x, y); c.scale(k, k);
    var sch = laeuft ? Math.sin(s.t / 3) * 12 : 0;
    c.fillStyle = F.sch;
    c.save(); c.translate(-8, -34); c.rotate(sch * Math.PI / 180); c.fillRect(-3, 0, 6, 34); c.restore();
    c.save(); c.translate(8, -34); c.rotate(-sch * Math.PI / 180); c.fillRect(-3, 0, 6, 34); c.restore();
    c.fillRect(-15, -70, 30, 30);
    var arm = hoch ? 155 : 25;   // springt: beide Arme hoch und nach außen (Anna 12.11.2026)
    c.save(); c.translate(-11, -66); c.rotate(arm * Math.PI / 180); c.fillRect(-3, 0, 6, 30); c.beginPath(); c.arc(0, 32, 4, 0, 7); c.fill(); c.restore();
    c.save(); c.translate(11, -66); c.rotate(-arm * Math.PI / 180); c.fillRect(-3, 0, 6, 30); c.beginPath(); c.arc(0, 32, 4, 0, 7); c.fill(); c.restore();
    c.fillStyle = F.ws; c.beginPath(); c.arc(0, -34, 25, Math.PI, 0); c.fill();
    c.fillStyle = rock; c.beginPath(); c.arc(0, -34, 22, Math.PI, 0); c.fill();
    c.fillStyle = F.sch; c.beginPath(); c.arc(0, -86, 12, 0, 7); c.fill();
    c.fillStyle = F.ws; c.beginPath(); c.arc(4, -88, 3, 0, 7); c.fill();
    c.restore();
  }
  function augen(x, y, zu) {
    if (zu) { c.fillStyle = F.sch; c.fillRect(x - 13, y - 1, 10, 3); c.fillRect(x + 3, y - 1, 10, 3); return; }
    c.fillStyle = F.ws; c.beginPath(); c.arc(x - 7, y, 6, 0, 7); c.arc(x + 7, y, 6, 0, 7); c.fill();
    c.fillStyle = F.sch; c.beginPath(); c.arc(x - 9, y + 1, 3, 0, 7); c.arc(x + 5, y + 1, 3, 0, 7); c.fill();
  }
  function gegner(g) {
    var x = g.x, y = BODEN - (g.hoehe || 0), w = Math.sin((s.t + g.x) / 6);
    c.save();
    if (g.platt && g.art !== 'unsichtbar') { c.translate(x + g.b / 2, y); c.scale(1 + g.platt * .6, Math.max(.12, 1 - g.platt)); c.translate(-(x + g.b / 2), -y); c.globalAlpha = Math.max(0, 1 - g.platt * .5); }
    if (g.platt && g.art === 'unsichtbar') c.globalAlpha = Math.max(0, 1 - g.platt * .6);
    if (g.art === 'funkstille') {          // Gespenst, schwebt, stummer Mund
      var gy = y - 10 + w * 6;
      c.fillStyle = F.gr; c.beginPath(); c.arc(x + 20, gy - 26, 20, Math.PI, 0); c.lineTo(x + 40, gy);
      for (var i = 0; i < 4; i++) { c.lineTo(x + 35 - i * 10, gy - (i % 2 ? 0 : 7)); c.lineTo(x + 30 - i * 10, gy); }
      c.closePath(); c.fill(); augen(x + 20, gy - 28); c.fillStyle = F.sch; c.fillRect(x + 14, gy - 16, 12, 3);
    } else if (g.art === 'unsichtbar') {   // Auge zu; draufspringen öffnet es
      c.fillStyle = F.gr; c.beginPath(); c.ellipse(x + 22, y - 20, 22, 20, 0, 0, 7); c.fill();
      if (g.platt) { c.fillStyle = F.ws; c.beginPath(); c.ellipse(x + 22, y - 22, 16, 11, 0, 0, 7); c.fill(); c.fillStyle = F.bl; c.beginPath(); c.arc(x + 22, y - 22, 7, 0, 7); c.fill(); c.fillStyle = F.sch; c.beginPath(); c.arc(x + 22, y - 22, 3, 0, 7); c.fill(); }
      else { c.strokeStyle = F.sch; c.lineWidth = 3; c.beginPath(); c.arc(x + 22, y - 24, 12, .2, Math.PI - .2); c.stroke(); for (var l = 0; l < 4; l++) c.fillRect(x + 12 + l * 6, y - 12, 2, 5); }
    } else if (g.art === 'toolchaos') {    // Virus mit Stacheln, rollt
      c.translate(x + 20, y - 20); c.rotate(-s.t / 8); c.fillStyle = F.gr;
      for (var k = 0; k < 8; k++) { c.rotate(Math.PI / 4); c.fillRect(-3, -22, 6, 10); c.beginPath(); c.arc(0, -22, 4, 0, 7); c.fill(); }
      c.beginPath(); c.arc(0, 0, 15, 0, 7); c.fill(); c.rotate(s.t / 8); augen(0, -2);
    } else if (g.art === 'zeitfresser') {  // frisst Uhren
      var maul = Math.abs(Math.sin(s.t / 5)) * .7;
      c.fillStyle = F.gr; c.beginPath(); c.moveTo(x + 24, y - 22); c.arc(x + 24, y - 22, 22, Math.PI + maul, Math.PI * 3 - maul); c.closePath(); c.fill();
      augen(x + 28, y - 32);
      c.fillStyle = F.ws; c.strokeStyle = F.sch; c.lineWidth = 2; c.beginPath(); c.arc(x - 4, y - 22, 8, 0, 7); c.fill(); c.stroke();
      c.beginPath(); c.moveTo(x - 4, y - 22); c.lineTo(x - 4, y - 27); c.moveTo(x - 4, y - 22); c.lineTo(x, y - 22); c.stroke();
    } else if (g.art === 'konkurrenz') {   // Wettbewerb: graue Figur mit Aktenkoffer, rennt
      figur(x + 17, y, .62, F.gr, true, false);
      c.fillStyle = F.sch; c.fillRect(x + 26, y - 30, 14, 10); c.fillRect(x + 30, y - 33, 6, 3);
    } else {                                // Ebbe in der Kasse: leerer Geldsack mit Motte
      c.fillStyle = F.gr; c.beginPath(); c.ellipse(x + 22, y - 15, 22, 15, 0, 0, 7); c.fill(); c.fillRect(x + 14, y - 36, 16, 8);
      augen(x + 22, y - 18); c.fillStyle = F.sch; c.font = '700 11px Manrope, system-ui, sans-serif'; c.fillText('0 €', x + 13, y - 4);
      var a = s.t / 6; c.fillStyle = F.sch; c.fillRect(x + 22 + Math.cos(a) * 20, y - 44 + Math.sin(a * 1.3) * 6, 4, 3);
    }
    c.restore();
    if (!g.platt && g.zeigName) etikett(g.name, x + g.b / 2, BODEN - g.h - 18, F.sch, F.ws);
  }
  function etikett(t, x, y, grund, schrift) {
    c.font = '600 15px Manrope, system-ui, sans-serif'; var tw = c.measureText(t).width;
    c.fillStyle = grund; c.fillRect(x - tw / 2 - 9, y - 17, tw + 18, 24); c.fillStyle = schrift; c.fillText(t, x - tw / 2, y);
  }
  function block(b) {
    var y = b.y - (b.stoss > 0 ? b.stoss : 0);
    if (b.leer) { c.fillStyle = F.grh; c.fillRect(b.x, y, 42, 42); return; }
    c.fillStyle = F.sch; c.fillRect(b.x, y, 42, 42);
    form(b.l.form, b.x + 21, y + 21, 22, b.l.farbe === F.sch ? F.ws : b.l.farbe);
  }
  function anzeige() {   // oben nur die drei Leben (Anna 12.11.2026: Geld raus); die Lösungen zählen die Chips unter dem Spiel
    for (var n = 0; n < 3; n++) { if (n < s.leben) herz(26 + n * 26, 22, 10, F.rot); else { c.globalAlpha = .2; herz(26 + n * 26, 22, 10, F.gr); c.globalAlpha = 1; } }
    if (s.level > 1) { c.fillStyle = F.sch; c.font = '700 14px Manrope, system-ui, sans-serif'; c.fillText('Level ' + s.level, 104, 27); }
  }
  function zeichne() {
    c.setTransform(cv.width / W, 0, 0, cv.height / H, 0, 0);
    c.clearRect(0, 0, W, H);
    leipzig();
    c.fillStyle = F.sch; c.fillRect(0, BODEN, W, 3);
    for (var i = 0; i < 14; i++) c.fillRect(wiederhole(i * 79, W + 240, 1), BODEN + 10 + (i % 3) * 4, 8 + (i % 2) * 6, 2);
    s.bloecke.forEach(block);
    s.muenzen.forEach(function (m) { muenze(m.x, m.y + Math.sin((s.t + m.x) / 8) * 3, 11); });
    s.gaben.forEach(function (g) { form(g.l.form, g.x, g.y, 34, g.l.farbe); });
    s.gegner.forEach(gegner);
    if (s.kraft) { var k = s.kraft; figur(k.x, BODEN - k.sprung, .62, F.gelb, true, k.sprung > 0); if (!s.bekannt.kraft) etikett('Fachkraft: Fang mich!', k.x, BODEN - 92 - k.sprung, F.gelb, F.sch); }
    if (!(s.f.blink > 0 && Math.floor(s.t / 4) % 2)) figur(s.f.x, s.f.y, s.gross ? 1.35 : 1, F.bl, s.f.amBoden && s.lauf && !s.aus, !s.f.amBoden);
    s.funken.forEach(function (p) { c.globalAlpha = Math.max(0, p.l / 30); form(p.form, p.x, p.y, p.g, p.farbe); }); c.globalAlpha = 1;
    s.lohn.forEach(function (p) { c.globalAlpha = Math.min(1, p.l / 20); etikett(p.text, p.x, p.y, p.farbe, p.farbe === F.gelb ? F.sch : F.ws); }); c.globalAlpha = 1;
    s.blasen.forEach(function (b) {
      c.font = '30px Anton, Impact, sans-serif'; var bw = c.measureText(b.text).width + 20;
      c.save(); c.translate(b.x, b.y); c.rotate(-.06); c.fillStyle = F.sch; c.fillRect(-bw / 2, -30, bw, 40); c.fillStyle = F.ws; c.fillText(b.text, -bw / 2 + 10, 2); c.restore();
    });
    anzeige();
    if (s.banner) {   // Level-Wechsel: großes Schild in der Mitte
      var a = Math.min(1, (s.banner.bis - s.t) / 20); c.globalAlpha = a;
      c.font = '64px Anton, Impact, sans-serif'; c.textAlign = 'center';
      var bw = Math.max(c.measureText(s.banner.titel).width + 60, 460);
      c.fillStyle = F.sch; c.fillRect(W / 2 - bw / 2, 52, bw, 132);
      c.fillStyle = F.ws; c.fillText(s.banner.titel, W / 2, 118);
      c.font = '600 16px Manrope, system-ui, sans-serif'; c.fillStyle = F.gelb; c.fillText(s.banner.zeile, W / 2, 146);
      c.fillStyle = F.ws; c.fillText(s.banner.regel, W / 2, 170); c.textAlign = 'left'; c.globalAlpha = 1;
    }
  }

  // ---------- Spiel ----------
  function blase(text, x, y) { s.blasen.push({ text: text, x: x, y: y, l: 45 }); }
  function lohn(text, x, y, farbe) { s.lohn.push({ text: text, x: x, y: y, l: 55, farbe: farbe }); }
  function funken(x, y, n) { for (var i = 0; i < n; i++) { var l = LEISTUNGEN[i % 5]; s.funken.push({ x: x, y: y, vx: (Math.random() - .5) * 9, vy: -Math.random() * 8 - 2, l: 30, g: 8 + Math.random() * 9, form: l.form, farbe: l.farbe }); } }
  function springen() {
    if (modus === 'still') { intro(); return; }
    if (s.demo) { spielStart(); return; }
    if (s.aus) { neu(false); starten(); return; }
    if (!s.lauf) starten();
    if (s.pause) { pauseUm(false); return; }
    if (s.f.amBoden) { s.f.vy = -14; s.f.amBoden = false; ton(TON.sprung); }
  }
  function starten() { s.lauf = true; modus = 'spiel'; karte(''); pauseAnzeige(); }
  function treffer() {
    if (s.f.blink > 0) return;
    if (s.gross) { s.gross = false; s.f.blink = 90; ton(TON.schrumpfen); blase('OHO!', s.f.x, s.f.y - 140); return; }
    s.leben--; s.f.blink = 100;
    if (s.leben > 0) { ton(TON.autsch); blase('OHO!', s.f.x, s.f.y - 110); return; }
    s.aus = true; ton(TON.ende); blase('OHO!', s.f.x, s.f.y - 110); bilanz();
  }
  function bilanz() {   // Ende: nur Botschaft und Play again; die Zahlen stehen oben rechts im Spiel
    bilanzBox.hidden = false; pauseAnzeige();
  }
  function belohnen(g) {
    var p = PROBLEME.filter(function (x) { return x.art === g.art; })[0];
    s.punkte[p.lohn] += p.menge;
    var farbe = p.lohn === 'euro' ? F.gelb : p.lohn === 'reichweite' ? F.bl : p.lohn === 'kunden' || p.lohn === 'stammkunden' ? F.pink : F.sch;
    lohn(p.text, g.x + g.b / 2, BODEN - g.h - 50, farbe);
  }
  function leistungHoch(b) {
    s.gaben.push({ l: b.l, i: b.i, x: b.x + 21, y: b.y - 24, vy: -6 });
    ton(TON.block); funken(b.x + 21, b.y, 10);
    if (s.demo) return;
    var r = cv.getBoundingClientRect(), sx = r.width / W, sy = r.height / H;
    var el = document.createElement('span'); el.className = 'spiel-flug spiel-flug-' + b.l.form; el.style.setProperty('--f', b.l.farbe);
    el.style.left = (r.left + window.scrollX + (b.x + 21) * sx) + 'px'; el.style.top = (r.top + window.scrollY + b.y * sy) + 'px';
    el.setAttribute('aria-hidden', 'true'); el.textContent = b.l.name;
    document.body.appendChild(el); setTimeout(function () { el.remove(); }, 1600);
  }
  // Die Spielregeln, eine je Level
  var REGELN = ['Regel 1: Wer nicht gesehen wird, verliert.', 'Regel 2: Wer alles allein macht, verliert Zeit.',
    'Regel 3: Wer gute Leute hält, gewinnt auf Dauer.', 'Regel 4: Der Wettbewerb schläft nicht.', 'Regel 5: Treue Kunden sind mehr wert als neue.'];
  function naechstesLevel() {
    s.level++; s.gesammelt = []; s.punkte.euro += 1000;
    chips.forEach(function (ch) { ch.classList.remove('ist-gesammelt'); });
    ton(TON.level); funken(s.f.x, s.f.y - 80, 30);
    s.banner = { bis: s.t + 170, titel: 'Level ' + s.level + '!', zeile: 'Alle fünf Lösungen gefunden.', regel: REGELN[(s.level - 2) % REGELN.length] };
    s.naechstG = Math.max(s.naechstG, 190); s.gegner = s.gegner.filter(function (g) { return g.x < s.f.x; });
    if (!s.demo) document.dispatchEvent(new Event('konfetti'));
  }
  function schritt() {
    if (!s.lauf || s.pause || s.aus) return;
    s.t++; s.tempo = Math.min(6.2, 3.5 + s.t / 3000 + (s.level - 1) * .3); s.weg += s.tempo;
    var k = s.gross ? 1.35 : 1, fh = 98 * k, fb = 30 * k;
    if (s.demo) demoSchritt();
    if (s.banner && s.t > s.banner.bis) s.banner = null;
    var mitte = W * .42; s.f.x += (mitte - s.f.x) * .06;                       // schnell zur Mitte
    s.f.vy += .8; s.f.y += s.f.vy; if (s.f.blink > 0) s.f.blink--;
    if (s.f.y >= BODEN) { s.f.y = BODEN; s.f.vy = 0; s.f.amBoden = true; }
    var fl = s.f.x - fb / 2, fr = s.f.x + fb / 2, fo = s.f.y - fh;
    // Leistungs-Blöcke
    if (--s.naechstB <= 0) {
      var offen = LEISTUNGEN.map(function (l, i) { return i; }).filter(function (i) { return s.gesammelt.indexOf(i) < 0 && !s.bloecke.some(function (b) { return b.i === i && !b.leer; }); });
      if (offen.length) { var i = offen[0]; s.bloecke.push({ x: W + 20, y: BODEN - 170, l: LEISTUNGEN[i], i: i, stoss: 0 }); }
      s.naechstB = 170 + Math.floor(Math.random() * 90);
    }
    s.bloecke.forEach(function (b) {
      b.x -= s.tempo; if (b.stoss > 0) b.stoss -= 2;
      if (!b.leer && s.f.vy < 0 && fr > b.x && fl < b.x + 42 && fo <= b.y + 42 && fo > b.y + 14) { b.leer = true; b.stoss = 10; s.f.vy = 2; leistungHoch(b); }
    });
    s.bloecke = s.bloecke.filter(function (b) { return b.x > -60; });
    s.gaben.forEach(function (g) {
      g.alter = (g.alter || 0) + 1;
      if (g.alter < 14) { g.x -= s.tempo * .3; g.vy += .4; g.y += g.vy; }
      else { g.x += (s.f.x - g.x) * .18; g.y += (s.f.y - 60 * k - g.y) * .18; }
      if (!g.weg && Math.abs(g.x - s.f.x) < 32 && g.y > fo - 24 && g.y < s.f.y) {
        g.weg = true;
        if (s.gesammelt.indexOf(g.i) < 0) {
          s.gesammelt.push(g.i); ton(TON.sammeln); blase('WOW!', g.x, g.y - 30); funken(g.x, g.y, 14);
          if (!s.demo && chips[g.i]) { chips[g.i].classList.add('ist-gesammelt'); s.zaehler[g.i]++; chipZahl(g.i, s.zaehler[g.i]); }
          if (s.gesammelt.length === LEISTUNGEN.length) { if (s.demo) s.gesammelt = []; else naechstesLevel(); }
        }
      }
    });
    s.gaben = s.gaben.filter(function (g) { return !g.weg && g.x > -40; });
    // Münzen in der Luft: seit 12.11.2026 ohne Geldanzeige nicht mehr im Spiel (naechstM bleibt sehr groß)
    if (--s.naechstM <= 0) { var hy = BODEN - 90 - Math.random() * 60; for (var m = 0; m < 3; m++) s.muenzen.push({ x: W + 20 + m * 34, y: hy - Math.sin(m / 2 * Math.PI) * 24, wert: 50 }); s.naechstM = 240 + Math.floor(Math.random() * 160); }
    s.muenzen.forEach(function (mz) {
      mz.x -= s.tempo;
      if (!mz.weg && Math.abs(mz.x - s.f.x) < 24 && mz.y > fo - 12 && mz.y < s.f.y) { mz.weg = true; s.punkte.euro += mz.wert; ton(TON.muenze); }
    });
    s.muenzen = s.muenzen.filter(function (mz) { return !mz.weg && mz.x > -30; });
    // Probleme laufen herum
    if (--s.naechstG <= 0) {
      var v = s.demo ? PROBLEME[(s.demoNr = (s.demoNr || 0) + 1) % PROBLEME.length] : PROBLEME[Math.floor(Math.random() * PROBLEME.length)];   // in der Demo jedes Problem einmal
      var g = Object.assign({ x: W + 30, platt: 0, phase: Math.random() * 6 }, v); g.zeigName = !s.bekannt[g.art]; s.bekannt[g.art] = true;
      s.gegner.push(g); s.naechstG = s.demo ? 95 : Math.max(70, 120 - s.level * 8) + Math.floor(Math.random() * 80);
    }
    s.gegner.forEach(function (g) {
      var eigen = g.art === 'konkurrenz' ? 2.6 : g.art === 'toolchaos' ? 1.8 : g.art === 'zeitfresser' ? 1.2 : g.art === 'funkstille' ? Math.sin((s.t + g.phase * 30) / 20) * 2.2 : g.art === 'unsichtbar' ? Math.sin((s.t + g.phase * 30) / 14) * 1.6 : .4;
      g.x -= s.tempo + eigen; g.v = s.tempo + eigen;
      if (g.art === 'ebbe') { g.hoehe = Math.max(0, Math.sin((s.t + g.phase * 40) / 12) * 18); }   // Geldsack hüpft
      if (g.platt) { g.platt += .05; return; }
      var gy = BODEN - (g.hoehe || 0);
      if (fr > g.x + 6 && fl < g.x + g.b - 6 && s.f.y > gy - g.h && fo < gy) {
        if (s.f.vy > 0 && s.f.y - s.f.vy <= gy - g.h + 10) {
          g.platt = .01; s.f.vy = -11; s.f.amBoden = false; ton(TON.platt); funken(g.x + g.b / 2, gy - g.h, 8);
          blase(['WOW!', 'AAH!'][Math.floor(Math.random() * 2)], g.x + g.b / 2, gy - g.h - 80); belohnen(g);
        } else if (!s.demo) treffer();
      }
    });
    s.gegner.forEach(function (g) {   // Wettbewerb ist vorbei, ohne dass man ihn überholt hat: ein Kunde ist weg
      if (g.art === 'konkurrenz' && !g.platt && !g.vorbei && g.x + g.b < s.f.x - 40) {
        g.vorbei = true;
        if (s.punkte.kunden > 0 && !s.demo) { s.punkte.kunden--; lohn('Kunde weg!', s.f.x - 60, BODEN - 120, F.gr); ton(TON.schrumpfen); }
      }
    });
    s.gegner = s.gegner.filter(function (g) { return g.x > -70 && g.platt < 1.4; });
    // Fachkraft: läuft hin und her, hüpft weg
    if (!s.kraft && --s.naechstK <= 0) s.kraft = { x: W + 30, sprung: 0, vsy: 0 };
    if (s.kraft) {
      var kr = s.kraft; kr.x -= s.tempo * .35; kr.x += Math.sin(s.t / 18) * 3.5;
      if (Math.abs(kr.x - s.f.x) < 130 && kr.sprung === 0 && Math.random() < .04) kr.vsy = 9;
      kr.sprung = Math.max(0, kr.sprung + kr.vsy); kr.vsy = kr.sprung > 0 ? kr.vsy - .6 : 0;
      if (Math.abs(kr.x - s.f.x) < 28 && Math.abs((BODEN - kr.sprung) - s.f.y) < 60) {
        s.kraft = null; s.bekannt.kraft = true; s.naechstK = 900; s.punkte.fachkraefte++;
        if (!s.gross) { s.gross = true; ton(TON.wachsen); } else ton(TON.sammeln);
        blase('AAH! Fachkraft gefunden', s.f.x + 80, s.f.y - 150); lohn('+1 Fachkraft', s.f.x, s.f.y - 190, F.gelb); funken(s.f.x, s.f.y - 60, 20);
      } else if (kr.x < -40) { s.kraft = null; s.naechstK = 450; }
    }
    s.funken.forEach(function (p) { p.x += p.vx; p.y += p.vy; p.vy += .35; p.l--; }); s.funken = s.funken.filter(function (p) { return p.l > 0; });
    s.blasen.forEach(function (b) { b.l--; b.y -= .6; }); s.blasen = s.blasen.filter(function (b) { return b.l > 0; });
    s.lohn.forEach(function (p) { p.l--; p.y -= .9; }); s.lohn = s.lohn.filter(function (p) { return p.l > 0; });
  }

  // ---------- Intro ----------
  // Startet erst auf „Spielen“ (Anna 12.11.2026). Feste Abfolge: jedes Element erscheint zu seinem Schritt in der Card,
  // die Figur springt allein, auch einmal von unten gegen einen schwarzen Block. Danach steht alles still, bis man spielt.
  var SCHRITTE = [[0, 'Springen', 'Mit der Leertaste, dem Pfeil nach oben oder per Tippen.'],
    [220, 'Probleme platt machen', 'Springen Sie auf die Probleme und den Wettbewerb. Dann werden sie zu Kunden, Reichweite, Zeit und Geld.'],
    [470, 'Chancen ergreifen', 'Stoßen Sie die schwarzen Blöcke von unten an. Darin stecken die fünf Lösungen.'],
    [720, 'Fachkraft fangen', 'Die gelbe Fachkraft macht Ihr Team stärker. Alle fünf Lösungen gefunden: nächstes Level. Sie haben drei Leben.']];
  var INTRO_ENDE = 960;
  function problem(art) {
    var v = PROBLEME.filter(function (x) { return x.art === art; })[0];
    var g = Object.assign({ x: W + 30, platt: 0, phase: 1 }, v); g.zeigName = true; s.gegner.push(g);
  }
  function demoSchritt() {
    SCHRITTE.forEach(function (d, i) { if (s.t === d[0] + 1) karte(d[1], d[2], 'So geht’s · ' + (i + 1) + ' von ' + SCHRITTE.length, 'Spielen'); });
    if (s.t === 40) problem('toolchaos');
    if (s.t === 250) problem('funkstille');
    if (s.t === 330) problem('konkurrenz');
    if (s.t === 380) s.bloecke.push({ x: W + 20, y: BODEN - 170, l: LEISTUNGEN[0], i: 0, stoss: 0 });
    if (s.t === 690) s.kraft = { x: s.f.x + 170, sprung: 0, vsy: 0 };
    // so abspringen, dass die Figur nach etwa 26 Bildern von oben auf dem Problem landet
    var nah = s.gegner.find(function (g) { return !g.platt && g.v > 0 && Math.abs((g.x + g.b / 2 - s.f.x) / g.v - 26) < 1; });
    var blockNah = s.bloecke.find(function (b) { return !b.leer && b.x - s.f.x < 26 && b.x - s.f.x > -12; });   // knapp vor dem Block abspringen, damit der Kopf ihn trifft
    if ((nah || blockNah) && s.f.amBoden) { s.f.vy = -14; s.f.amBoden = false; }
    if (s.t >= INTRO_ENDE && s.f.amBoden) { s.lauf = false; modus = 'bereit'; karte('Alles klar?', 'Dann sind Sie dran.', '', 'Spielen'); pauseAnzeige(); }
  }
  function intro() { neu(true); s.lauf = true; modus = 'intro'; karte(SCHRITTE[0][1], SCHRITTE[0][2], 'So geht’s · 1 von ' + SCHRITTE.length, 'Spielen'); pauseAnzeige(); }
  function spielStart() { neu(false); starten(); cv.focus(); }
  // Standbild beim Ankommen: Figur in der Mitte, links ein Block und ein Problem, nichts bewegt sich
  function standbild() {
    neu(true); s.lauf = false; modus = 'still'; s.f.x = W * .42; s.weg = 600;   // Stadt etwas weiter, damit das Auto nicht vor der Figur steht
    s.bloecke.push({ x: W * .16, y: BODEN - 170, l: LEISTUNGEN[0], i: 0, stoss: 0 });
    problem('unsichtbar'); s.gegner[0].x = W * .27; s.gegner[0].zeigName = false;
    karte('Schaffen Sie es durch Leipzig?', '', '', 'Spielen');
  }

  var letzte = 0;
  var sichtbar = true;
  function schleife(zeit) { if (sichtbar && zeit - letzte >= 15) { schritt(); zeichne(); letzte = zeit; } requestAnimationFrame(schleife); }

  // ---------- Bedienung ----------
  cv.addEventListener('pointerdown', function (e) { e.preventDefault(); springen(); });
  startKnopf.addEventListener('click', function () { if (modus === 'still') intro(); else if (modus === 'spiel' && s.pause) { pauseUm(false); cv.focus(); } else spielStart(); });
  function imBild() { var r = cv.getBoundingClientRect(); return r.bottom > 0 && r.top < window.innerHeight; }
  document.addEventListener('keydown', function (e) {
    if (!(e.code === 'Space' || e.code === 'ArrowUp' || e.code === 'KeyW')) return;
    var z = e.target; if (z && z.closest && (z.closest('input, textarea, select, [contenteditable]') || (z.closest('a, button') && !z.closest('[data-start]')))) return;
    if (!imBild()) return;
    e.preventDefault(); springen();
  });
  function pauseAnzeige() {   // Play/Pause-Icon: spielt es gerade, zeigt der Button „Pause“, sonst „Spielen“
    var spielt = s.lauf && !s.pause && !s.aus;
    knopfPause.setAttribute('aria-pressed', spielt ? 'false' : 'true');
    knopfPause.setAttribute('aria-label', modus === 'intro' ? (spielt ? 'Intro anhalten' : 'Intro fortsetzen') : spielt ? 'Spiel anhalten' : 'Spiel starten');
  }
  function pauseUm(an) {
    s.pause = an === undefined ? !s.pause : an;
    if (!s.demo) karte(s.pause ? 'Pause' : '', 'Leertaste oder Tippen: weiter.', '', 'Weiter');
    pauseAnzeige();
  }
  knopfPause.addEventListener('click', function () {
    if (modus === 'still') { intro(); return; }
    if (modus === 'bereit') { spielStart(); return; }
    if (s.demo) { s.pause = !s.pause; pauseAnzeige(); return; }
    if (!s.lauf || s.aus) { if (s.aus) neu(false); starten(); return; }
    pauseUm();
  });
  var nochmal = wurzel.querySelector('[data-nochmal]'); if (nochmal) nochmal.addEventListener('click', function () { neu(false); starten(); cv.focus(); });
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { sichtbar = e[0].isIntersecting; if (!sichtbar && s.lauf && !s.demo && !s.pause && !s.aus) pauseUm(true); }).observe(cv);
  document.addEventListener('visibilitychange', function () { if (document.hidden && s.lauf && !s.demo && !s.pause && !s.aus) pauseUm(true); });
  window.addEventListener('resize', groesse);

  if (location.hash === '#test') window.spielTest = { zustand: function () { return s; }, modus: function () { return modus; }, schritt: schritt, zeichne: zeichne, springen: springen, intro: intro };   // nur zum Testen
  groesse();
  standbild();
  requestAnimationFrame(schleife);
})();
