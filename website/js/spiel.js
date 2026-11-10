/* Hero-Spiel „Play the game“ durch Leipzig (Anna 10.11.2026, Fassung 3; Entwurfsordner website/entwurf-hero-spiel/ nur lokal)
   Eigenes Lauf-und-Spring-Spiel in Annas Bildsprache (kein Nachbau eines bestehenden Spiels, keine fremden Töne oder Figuren).
   – Freistehend, nur Bodenlinie. Die Bauhaus-Figur läuft schnell zur Bildmitte und dann durch Leipzig
     (Völkerschlachtdenkmal, Weisheitszahn, Hauptbahnhof, Baustelle, Autos, Bäume).
   – Fünf Probleme laufen herum. Draufspringen verwandelt sie in das, was Unternehmen wollen:
       Funkstille → neue Kunden · Unsichtbar (Auge zu) → Auge geht auf, Reichweite · Tool-Chaos → Zeit
       Zeitfresser → Zeit · Ebbe in der Kasse → Geld. Seitlich dagegen kostet ein Leben (drei Leben).
   – Die Fachkraft läuft weg; gefangen: ein Mitarbeiter mehr, die Figur wächst und hält einen Treffer aus.
   – Schwarze Blöcke von unten anstoßen: Leistung fliegt heraus bis in die Schrift. Alle fünf gesammelt: nächstes Level.
   – Das Spiel läuft weiter, bis die Leben weg sind; dann zeigt es die Bilanz mit „Projekt anfragen“.
   – Kurze Demo (höchstens 5 s) vorab. Ton aus, bis man ihn einschaltet. Pause jederzeit. */
(function () {
  'use strict';
  var wurzel = document.querySelector('[data-spiel]');
  if (!wurzel) return;
  var cv = wurzel.querySelector('canvas'), c = cv.getContext('2d');
  var W = 960, H = 260, BODEN = 236;
  var F = { sch: '#0e1011', ws: '#ffffff', bl: '#2a5fe6', rot: '#ff3b2f', pink: '#ff4fa3', rosa: '#ff8fc8', gelb: '#ffe600', gr: '#9a9d9e', grh: '#d6d8d9' };
  var LEISTUNGEN = [
    { name: 'Webdesign', form: 'kreis', farbe: F.bl }, { name: 'Markenbildung', form: 'quadrat', farbe: F.rot },
    { name: 'UI/UX', form: 'halbkreis', farbe: F.pink }, { name: 'Marketing & Vertrieb', form: 'halbkreis', farbe: F.sch },
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
  var meldungEl = wurzel.querySelector('[data-meldung]'), startKnopf = wurzel.querySelector('[data-start]');
  var knopfTon = wurzel.querySelector('[data-ton]'), knopfPause = wurzel.querySelector('[data-pause]');
  var bilanzBox = wurzel.querySelector('[data-sieg]'), bilanzText = wurzel.querySelector('[data-bilanz]');
  var ruhig = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var zahl = new Intl.NumberFormat('de-DE');

  function groesse() {
    var r = cv.getBoundingClientRect();
    H = r.width < 600 ? 360 : 260; BODEN = H - 24;
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
    s = { demo: !!demo, lauf: !!demo, aus: false, pause: false, t: 0, tempo: 3.8, weg: 0, gross: false, level: 1, leben: 3,
          punkte: { euro: 0, reichweite: 0, kunden: 0, stammkunden: 0, fachkraefte: 0, zeit: 0 },
          f: { x: 110, y: BODEN, vy: 0, amBoden: true, blink: 0 }, gegner: [], bloecke: [], gaben: [], muenzen: [], kraft: null,
          funken: [], blasen: [], lohn: [], naechstG: demo ? 20 : 70, naechstB: demo ? 45 : 70, naechstK: demo ? 9999 : 360, naechstM: 120,
          gesammelt: [], bekannt: {} };
    chips.forEach(function (ch) { ch.classList.remove('ist-gesammelt'); });
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
  function leipzig() {   // Zentrum von Leipzig als ruhige Silhouetten, nacheinander wie auf einem Weg durch die Stadt
    var L = W * 3;
    c.fillStyle = F.grh;
    // Weisheitszahn (City-Hochhaus) gleich zu Beginn: hoch, mit schräg gerundeter Spitze
    var x = wiederhole(560, L, .12);
    c.beginPath(); c.moveTo(x, BODEN); c.lineTo(x, BODEN - 180); c.quadraticCurveTo(x + 24, BODEN - 226, x + 54, BODEN - 206); c.lineTo(x + 54, BODEN); c.fill();
    // Thomaskirche: Schiff mit steilem Dach, schlanker Turm mit Spitze
    x = wiederhole(1150, L, .12);
    c.fillRect(x, BODEN - 60, 150, 60); c.beginPath(); c.moveTo(x - 6, BODEN - 60); c.lineTo(x + 75, BODEN - 110); c.lineTo(x + 156, BODEN - 60); c.fill();
    c.fillRect(x + 150, BODEN - 130, 34, 130); c.beginPath(); c.moveTo(x + 146, BODEN - 130); c.lineTo(x + 167, BODEN - 176); c.lineTo(x + 188, BODEN - 130); c.fill();
    // Hauptbahnhof: lange Halle mit Bögen
    x = wiederhole(1700, L, .12);
    c.fillRect(x, BODEN - 40, 230, 40); for (var k = 0; k < 4; k++) { c.beginPath(); c.arc(x + 30 + k * 57, BODEN - 40, 28, Math.PI, 0); c.fill(); }
    // Völkerschlachtdenkmal: erst später, Stufensockel und Kuppel
    x = wiederhole(2450, L, .12);
    c.fillRect(x - 20, BODEN - 20, 200, 20); c.fillRect(x, BODEN - 44, 160, 24); c.fillRect(x + 30, BODEN - 92, 100, 48);
    c.beginPath(); c.arc(x + 80, BODEN - 92, 46, Math.PI, 0); c.fill();
    // eine Baustelle: Kran und Absperrung
    x = wiederhole(900, W + 900, .3);
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
      var bx = wiederhole(t[0], W + 700, .45); c.fillStyle = F.sch; c.fillRect(bx - 2, BODEN - t[2] * 2, 4, t[2] * 2); c.fillStyle = t[1]; c.beginPath(); c.arc(bx, BODEN - t[2] * 2.6, t[2], 0, 7); c.fill(); });
    var ax = wiederhole(400, W + 1400, .75); c.fillStyle = F.bl; c.fillRect(ax, BODEN - 26, 58, 16); c.beginPath(); c.arc(ax + 26, BODEN - 26, 16, Math.PI, 0); c.fill();
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
    var arm = hoch ? -150 : 25;
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
  function anzeige() {   // nur das Wichtigste: links die drei Leben, rechts die fünf Leistungen als Formen und das Geld
    for (var n = 0; n < 3; n++) { if (n < s.leben) herz(26 + n * 26, 22, 10, F.rot); else { c.globalAlpha = .2; herz(26 + n * 26, 22, 10, F.gr); c.globalAlpha = 1; } }
    if (s.level > 1) { c.fillStyle = F.sch; c.font = '700 14px Manrope, system-ui, sans-serif'; c.fillText('Level ' + s.level, 104, 27); }
    c.font = '700 16px Manrope, system-ui, sans-serif';
    var geld = zahl.format(s.punkte.euro) + ' €', tw = c.measureText(geld).width;
    c.fillStyle = F.sch; c.fillText(geld, W - 14 - tw, 27); muenze(W - 34 - tw, 21, 10);
    LEISTUNGEN.forEach(function (l, i) { var lx = W - 230 - tw + i * 32;
      if (s.gesammelt.indexOf(i) < 0) { c.globalAlpha = .18; form(l.form, lx, 21, 20, F.sch); c.globalAlpha = 1; } else form(l.form, lx, 21, 20, l.farbe); });
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
  }

  // ---------- Spiel ----------
  function blase(text, x, y) { s.blasen.push({ text: text, x: x, y: y, l: 45 }); }
  function lohn(text, x, y, farbe) { s.lohn.push({ text: text, x: x, y: y, l: 55, farbe: farbe }); }
  function funken(x, y, n) { for (var i = 0; i < n; i++) { var l = LEISTUNGEN[i % 5]; s.funken.push({ x: x, y: y, vx: (Math.random() - .5) * 9, vy: -Math.random() * 8 - 2, l: 30, g: 8 + Math.random() * 9, form: l.form, farbe: l.farbe }); } }
  function springen() {
    if (s.demo) demoEnde();
    if (s.aus) { neu(false); starten(); return; }
    if (!s.lauf) starten();
    if (s.pause) { pauseUm(false); return; }
    if (s.f.amBoden) { s.f.vy = -15.5; s.f.amBoden = false; ton(TON.sprung); }
  }
  function starten() { s.lauf = true; meldung(''); if (startKnopf) startKnopf.hidden = true; pauseAnzeige(); }
  function meldung(t) { meldungEl.textContent = t; meldungEl.hidden = !t; }
  function treffer() {
    if (s.f.blink > 0) return;
    if (s.gross) { s.gross = false; s.f.blink = 90; ton(TON.schrumpfen); blase('OHO!', s.f.x, s.f.y - 140); return; }
    s.leben--; s.f.blink = 100;
    if (s.leben > 0) { ton(TON.autsch); blase('OHO!', s.f.x, s.f.y - 110); return; }
    s.aus = true; ton(TON.ende); blase('OHO!', s.f.x, s.f.y - 110); bilanz();
  }
  function bilanz() {
    var p = s.punkte;
    bilanzText.textContent = 'Level ' + s.level + ' · ' + zahl.format(p.euro) + ' € · ' + (p.kunden + p.stammkunden) + (p.kunden + p.stammkunden === 1 ? ' Kunde' : ' Kunden') + ' · ' + p.fachkraefte + (p.fachkraefte === 1 ? ' Fachkraft' : ' Fachkräfte') + ' · ' + zahl.format(p.reichweite) + ' Reichweite';
    bilanzBox.hidden = false; pauseAnzeige();
  }
  function belohnen(g) {
    var p = PROBLEME.filter(function (x) { return x.art === g.art; })[0];
    s.punkte[p.lohn] += p.menge;
    var farbe = p.lohn === 'euro' ? F.gelb : p.lohn === 'reichweite' ? F.bl : p.lohn === 'kunden' || p.lohn === 'stammkunden' ? F.pink : F.sch;
    lohn(p.text, g.x + g.b / 2, BODEN - g.h - 50, farbe);
    if (p.lohn === 'euro') for (var i = 0; i < 3; i++) s.muenzen.push({ x: g.x + 20 + i * 30, y: BODEN - 110 - i * 18, wert: 50 });
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
    ton(TON.level); blase('AAH! Level ' + s.level, W / 2, 110); if (!s.demo) { meldung(REGELN[(s.level - 2) % REGELN.length]); s.regelBis = s.t + 200; } lohn('Alle Leistungen: +1.000 €', W / 2, 150, F.gelb); funken(s.f.x, s.f.y - 80, 30);
    if (!s.demo) document.dispatchEvent(new Event('konfetti'));
  }
  function schritt() {
    if (!s.lauf || s.pause || s.aus) return;
    s.t++; s.tempo = Math.min(7.2, 3.8 + s.t / 2000 + (s.level - 1) * .4); s.weg += s.tempo;
    var k = s.gross ? 1.35 : 1, fh = 98 * k, fb = 30 * k;
    if (s.demo) demoSchritt();
    if (s.regelBis && s.t > s.regelBis) { s.regelBis = 0; meldung(''); }
    var mitte = W * .42; s.f.x += (mitte - s.f.x) * .06;                       // schnell zur Mitte
    s.f.vy += .8; s.f.y += s.f.vy; if (s.f.blink > 0) s.f.blink--;
    if (s.f.y >= BODEN) { s.f.y = BODEN; s.f.vy = 0; s.f.amBoden = true; }
    var fl = s.f.x - fb / 2, fr = s.f.x + fb / 2, fo = s.f.y - fh;
    // Leistungs-Blöcke
    if (--s.naechstB <= 0) {
      var offen = LEISTUNGEN.map(function (l, i) { return i; }).filter(function (i) { return s.gesammelt.indexOf(i) < 0 && !s.bloecke.some(function (b) { return b.i === i && !b.leer; }); });
      if (offen.length) { var i = offen[Math.floor(Math.random() * offen.length)]; s.bloecke.push({ x: W + 20, y: BODEN - 170, l: LEISTUNGEN[i], i: i, stoss: 0 }); }
      s.naechstB = 120 + Math.floor(Math.random() * 70);
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
          if (!s.demo && chips[g.i]) chips[g.i].classList.add('ist-gesammelt');
          if (s.gesammelt.length === LEISTUNGEN.length) naechstesLevel();
        }
      }
    });
    s.gaben = s.gaben.filter(function (g) { return !g.weg && g.x > -40; });
    // Münzen in der Luft
    if (--s.naechstM <= 0) { var hy = BODEN - 90 - Math.random() * 60; for (var m = 0; m < 3; m++) s.muenzen.push({ x: W + 20 + m * 34, y: hy - Math.sin(m / 2 * Math.PI) * 24, wert: 50 }); s.naechstM = 160 + Math.floor(Math.random() * 120); }
    s.muenzen.forEach(function (mz) {
      mz.x -= s.tempo;
      if (!mz.weg && Math.abs(mz.x - s.f.x) < 24 && mz.y > fo - 12 && mz.y < s.f.y) { mz.weg = true; s.punkte.euro += mz.wert; ton(TON.muenze); }
    });
    s.muenzen = s.muenzen.filter(function (mz) { return !mz.weg && mz.x > -30; });
    // Probleme laufen herum
    if (--s.naechstG <= 0) {
      var v = PROBLEME[Math.floor(Math.random() * PROBLEME.length)];
      var g = Object.assign({ x: W + 30, platt: 0, phase: Math.random() * 6 }, v); g.zeigName = !s.bekannt[g.art]; s.bekannt[g.art] = true;
      s.gegner.push(g); s.naechstG = Math.max(40, 80 - s.level * 6) + Math.floor(Math.random() * 60);
    }
    s.gegner.forEach(function (g) {
      var eigen = g.art === 'konkurrenz' ? 2.6 : g.art === 'toolchaos' ? 1.8 : g.art === 'zeitfresser' ? 1.2 : g.art === 'funkstille' ? Math.sin((s.t + g.phase * 30) / 20) * 2.2 : g.art === 'unsichtbar' ? Math.sin((s.t + g.phase * 30) / 14) * 1.6 : .4;
      g.x -= s.tempo + eigen;
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
        s.kraft = null; s.bekannt.kraft = true; s.naechstK = 700; s.punkte.fachkraefte++;
        if (!s.gross) { s.gross = true; ton(TON.wachsen); } else ton(TON.sammeln);
        blase('AAH! Fachkraft gefunden', s.f.x + 80, s.f.y - 150); lohn('+1 Fachkraft', s.f.x, s.f.y - 190, F.gelb); funken(s.f.x, s.f.y - 60, 20);
      } else if (kr.x < -40) { s.kraft = null; s.naechstK = 450; }
    }
    s.funken.forEach(function (p) { p.x += p.vx; p.y += p.vy; p.vy += .35; p.l--; }); s.funken = s.funken.filter(function (p) { return p.l > 0; });
    s.blasen.forEach(function (b) { b.l--; b.y -= .6; }); s.blasen = s.blasen.filter(function (b) { return b.l > 0; });
    s.lohn.forEach(function (p) { p.l--; p.y -= .9; }); s.lohn = s.lohn.filter(function (p) { return p.l > 0; });
  }

  // ---------- Demo: höchstens 5 Sekunden ----------
  var DEMO = [[0, 'Play the game! Springen mit Leertaste oder Tippen'], [150, 'Auf Probleme springen: Sie werden zu Kunden, Reichweite, Zeit und Geld'], [300, 'Schwarze Blöcke von unten anstoßen: Leistung!'], [450, 'Den Wettbewerb überholen: draufspringen! Drei Leben.']];
  function demoSchritt() {
    DEMO.forEach(function (d) { if (s.t === d[0] + 1) meldung(d[1]); });
    var nah = s.gegner.find(function (g) { return !g.platt && g.x - s.f.x < 70 && g.x - s.f.x > 20; });
    var blockNah = s.bloecke.find(function (b) { return !b.leer && b.x - s.f.x < 40 && b.x - s.f.x > -10; });
    if ((nah || blockNah) && s.f.amBoden) { s.f.vy = -15.5; s.f.amBoden = false; }
    if (s.t === 30) s.kraft = { x: W - 120, sprung: 0, vsy: 0 };
    if (s.t >= 600) demoEnde();
  }
  function demoEnde() { if (!s || !s.demo) return; neu(false); meldung(''); if (startKnopf) startKnopf.hidden = false; }

  var letzte = 0;
  function schleife(zeit) { if (zeit - letzte >= 15) { schritt(); zeichne(); letzte = zeit; } requestAnimationFrame(schleife); }

  // ---------- Bedienung ----------
  cv.addEventListener('pointerdown', function (e) { e.preventDefault(); springen(); });
  if (startKnopf) startKnopf.addEventListener('click', function () { if (s.demo) demoEnde(); starten(); cv.focus(); });
  function imBild() { var r = cv.getBoundingClientRect(); return r.bottom > 0 && r.top < window.innerHeight; }
  document.addEventListener('keydown', function (e) {
    if (!(e.code === 'Space' || e.code === 'ArrowUp' || e.code === 'KeyW')) return;
    var z = e.target; if (z && z.closest && (z.closest('input, textarea, select, [contenteditable]') || (z.closest('a, button') && !z.closest('[data-start]')))) return;
    if (!imBild()) return;
    e.preventDefault(); springen();
  });
  function pauseAnzeige() {   // Play/Pause-Icon: spielt es gerade, zeigt der Button „Pause“, sonst „Spielen“
    var spielt = s.lauf && !s.pause && !s.aus && !s.demo;
    knopfPause.setAttribute('aria-pressed', spielt ? 'false' : 'true');
    knopfPause.setAttribute('aria-label', spielt ? 'Spiel anhalten' : 'Spiel starten');
  }
  function pauseUm(an) {
    s.pause = an === undefined ? !s.pause : an;
    if (!s.demo) meldung(s.pause ? 'Pause. Leertaste oder Tippen: weiter.' : '');
    pauseAnzeige();
  }
  knopfPause.addEventListener('click', function () {
    if (s.demo) { demoEnde(); starten(); return; }
    if (!s.lauf || s.aus) { if (s.aus) neu(false); starten(); return; }
    pauseUm();
  });
  var nochmal = wurzel.querySelector('[data-nochmal]'); if (nochmal) nochmal.addEventListener('click', function () { neu(false); starten(); cv.focus(); });
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { if (!e[0].isIntersecting && s.lauf && !s.demo && !s.pause && !s.aus) pauseUm(true); }).observe(cv);
  document.addEventListener('visibilitychange', function () { if (document.hidden && s.lauf && !s.demo && !s.pause && !s.aus) pauseUm(true); });
  window.addEventListener('resize', groesse);

  if (location.hash === '#test') window.spielTest = { zustand: function () { return s; }, schritt: schritt, springen: springen, demoEnde: demoEnde };   // nur zum Testen
  groesse();
  if (ruhig) { neu(false); meldung('Springen mit Leertaste oder Tippen. Probleme platt machen, Leistungen sammeln.'); if (startKnopf) startKnopf.hidden = false; }
  else neu(true);
  requestAnimationFrame(schleife);
})();
