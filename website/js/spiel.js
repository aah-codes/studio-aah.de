/* Hero-Spiel „AAH! Durch Leipzig“ (Anna 10.11.2026, Startseite; Entwurfsordner website/entwurf-hero-spiel/ nur lokal)
   Eigenes Lauf-und-Spring-Spiel in Annas Bildsprache (kein Nachbau eines bestehenden Spiels):
   – Freistehend wie das Dino-Spiel: nur eine Bodenlinie, kein Rahmen. Scharf gezeichnet (Gerätepixel), kräftige Farben.
   – Die Bauhaus-Figur läuft durch Leipzig: Uni-Riese, Völkerschlachtdenkmal, Baustellen mit Kran und Baken, Autos, Bäume.
   – Probleme als Störenfriede: Funkstille-Gespenst (keine neuen Kunden), Tool-Virus (Software, die keiner nutzt),
     Zeitfresser (alle rennen, nichts wird fertig) und ein Haufen Mist. Draufspringen: platt. Seitlich dagegen: OHO!
   – Die Fachkraft (gelber Rock) läuft hin und her und hüpft weg. Gefangen: Die Figur wächst und hält einen Treffer aus.
   – Schwarze Blöcke in der Luft: von unten anstoßen, eine Leistung fliegt heraus und steigt bis in die Schrift.
   – Alle fünf Leistungen gesammelt: gewonnen, Konfetti, Button „Projekt anfragen“.
   – Erst eine kurze Demo (höchstens 5 Sekunden, mit Pause-Taste), die das Spiel erklärt; dann „Spielen“.
   Ton aus, bis man ihn einschaltet. Eigene Klänge (Web Audio), keine fremden Tonaufnahmen. */
(function () {
  'use strict';
  var wurzel = document.querySelector('[data-spiel]');
  if (!wurzel) return;
  var cv = wurzel.querySelector('canvas'), c = cv.getContext('2d');
  var W = 960, H = 260, BODEN = 236;
  var F = { sch: '#0e1011', ws: '#ffffff', bl: '#2a5fe6', rot: '#ff3b2f', pink: '#ff4fa3', rosa: '#ff8fc8', gelb: '#ffe600', gr: '#9a9d9e', grh: '#d6d8d9', creme: '#eeece7' };
  var LEISTUNGEN = [   // Marketing & Vertrieb in Schwarz, damit sich die Farben klar unterscheiden (Anna: zwei Rosatöne zu ähnlich)
    { name: 'Webdesign', form: 'kreis', farbe: F.bl }, { name: 'Markenbildung', form: 'quadrat', farbe: F.rot },
    { name: 'UI/UX', form: 'halbkreis', farbe: F.pink }, { name: 'Marketing & Vertrieb', form: 'halbkreis', farbe: F.sch },
    { name: 'KI & Digitalisierung', form: 'dreieck', farbe: F.gelb }];
  var GEGNER = [
    { art: 'gespenst', name: 'Funkstille', b: 40, h: 46 }, { art: 'virus', name: 'Tool-Chaos', b: 40, h: 40 },
    { art: 'fresser', name: 'Zeitfresser', b: 48, h: 44 }, { art: 'mist', name: 'Mist', b: 42, h: 30 }];
  var chips = wurzel.querySelectorAll('[data-leistung]');
  var meldungEl = wurzel.querySelector('[data-meldung]'), startKnopf = wurzel.querySelector('[data-start]');
  var knopfTon = wurzel.querySelector('[data-ton]'), knopfPause = wurzel.querySelector('[data-pause]'), sieg = wurzel.querySelector('[data-sieg]');
  var ruhig = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  function groesse() {
    var r = cv.getBoundingClientRect(), schmal = r.width < 600;
    H = schmal ? 360 : 260; BODEN = H - 24;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.width * H / W * dpr);
  }

  // ---------- Ton ----------
  var tonAn = false, ac = null;
  try { tonAn = localStorage.getItem('spiel-ton') === 'an'; } catch (e) {}
  function tonKnopf() { knopfTon.setAttribute('aria-pressed', tonAn ? 'true' : 'false'); knopfTon.querySelector('span').textContent = tonAn ? 'Ton aus' : 'Ton an'; }
  tonKnopf();
  knopfTon.addEventListener('click', function () { tonAn = !tonAn; tonKnopf(); try { localStorage.setItem('spiel-ton', tonAn ? 'an' : 'aus'); } catch (e) {} });
  function ton(folge) {
    if (!tonAn || s.demo) return;
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
  var TON = { sprung: [[380, .13, 'square', 820]], platt: [[260, .07, 'square', 80], [120, .12, 'triangle', 60]],
    block: [[200, .05], [700, .08, 'square', 1400]], sammeln: [[988, .06], [1318, .14]],
    wachsen: [[330, .06], [392, .06], [494, .06], [659, .06], [784, .06], [988, .14]], schrumpfen: [[600, .1, 'sawtooth', 200]],
    oho: [[520, .15, 'sawtooth', 280], [280, .3, 'sawtooth', 110]], sieg: [[523, .1], [659, .1], [784, .1], [1046, .12], [784, .08], [1046, .35]] };

  // ---------- Zustand ----------
  var s;
  function neu(demo) {
    s = { demo: !!demo, lauf: !!demo, aus: false, gewonnen: false, pause: false, t: 0, tempo: 4.2, weg: 0, gross: false,
          f: { x: 120, y: BODEN, vy: 0, amBoden: true, blink: 0 }, gegner: [], bloecke: [], gaben: [], kraft: null, funken: [], blasen: [],
          naechstG: demo ? 25 : 90, naechstB: demo ? 50 : 60, naechstK: demo ? 9999 : 420, gesammelt: [], bekannt: {} };
    chips.forEach(function (ch) { ch.classList.remove('ist-gesammelt'); });
    if (sieg) sieg.hidden = true;
  }

  // ---------- Zeichnen ----------
  function form(art, x, y, g, farbe) {
    c.fillStyle = farbe; c.beginPath();
    if (art === 'kreis') c.arc(x, y, g / 2, 0, Math.PI * 2);
    else if (art === 'quadrat') c.rect(x - g / 2, y - g / 2, g, g);
    else if (art === 'halbkreis') c.arc(x, y + g / 4, g / 2, Math.PI, 0);
    else { c.moveTo(x + g / 2, y - g / 2); c.lineTo(x + g / 2, y + g / 2); c.lineTo(x - g / 2, y + g / 2); }
    c.fill();
  }
  function wiederhole(x, laenge, tempo) { return ((x - s.weg * tempo) % laenge + laenge) % laenge - 80; }
  function leipzig() {
    var L = W + 400;
    // Skyline in Hellgrau: Uni-Riese, Völkerschlachtdenkmal, Hauptbahnhof
    c.fillStyle = F.grh;
    var x = wiederhole(140, L, .12); c.fillRect(x, BODEN - 170, 36, 170); c.beginPath(); c.arc(x + 18, BODEN - 170, 18, Math.PI, 0); c.fill(); c.fillRect(x + 16, BODEN - 200, 4, 16);
    x = wiederhole(560, L, .12); c.fillRect(x, BODEN - 40, 120, 40); c.fillRect(x + 20, BODEN - 70, 80, 30); c.beginPath(); c.arc(x + 60, BODEN - 70, 34, Math.PI, 0); c.fill();
    x = wiederhole(900, L, .12); for (var i = 0; i < 4; i++) { c.beginPath(); c.arc(x + 30 + i * 52, BODEN - 40, 26, Math.PI, 0); c.fill(); } c.fillRect(x, BODEN - 40, 210, 40);
    // Baustelle: Kran, Absperrung, Baken
    x = wiederhole(380, L, .3);
    c.fillStyle = F.sch; c.fillRect(x, BODEN - 160, 6, 160); c.fillRect(x - 40, BODEN - 160, 150, 6); c.fillRect(x + 90, BODEN - 154, 2, 40);
    c.fillStyle = F.gelb; c.fillRect(x + 84, BODEN - 114, 16, 16);
    for (var k = 0; k < 5; k++) { c.fillStyle = k % 2 ? F.ws : F.rot; c.fillRect(x + 20 + k * 14, BODEN - 28, 14, 10); }
    c.fillStyle = F.sch; c.fillRect(x + 22, BODEN - 18, 3, 18); c.fillRect(x + 84, BODEN - 18, 3, 18);
    // Bäume als Bauhaus-Formen
    [[60, F.pink, 22], [260, F.gelb, 18], [720, F.rosa, 26], [1180, F.bl, 18]].forEach(function (b) {
      var bx = wiederhole(b[0], L, .45); c.fillStyle = F.sch; c.fillRect(bx - 2, BODEN - b[2] * 2, 4, b[2] * 2); c.fillStyle = b[1]; c.beginPath(); c.arc(bx, BODEN - b[2] * 2 - b[2] * .6, b[2], 0, 7); c.fill(); });
    // Autos auf der hinteren Spur
    [[0, F.rot], [520, F.bl], [980, F.gelb]].forEach(function (a) {
      var ax = wiederhole(a[0], L, .75); c.fillStyle = a[1]; c.fillRect(ax, BODEN - 26, 58, 16); c.beginPath(); c.arc(ax + 26, BODEN - 26, 16, Math.PI, 0); c.fill();
      c.fillStyle = F.ws; c.fillRect(ax + 18, BODEN - 36, 16, 8); c.fillStyle = F.sch; c.beginPath(); c.arc(ax + 14, BODEN - 8, 7, 0, 7); c.arc(ax + 46, BODEN - 8, 7, 0, 7); c.fill(); });
  }
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
  function augen(x, y) {
    c.fillStyle = F.ws; c.beginPath(); c.arc(x - 7, y, 6, 0, 7); c.arc(x + 7, y, 6, 0, 7); c.fill();
    c.fillStyle = F.sch; c.beginPath(); c.arc(x - 9, y + 1, 3, 0, 7); c.arc(x + 5, y + 1, 3, 0, 7); c.fill();
  }
  function gegner(g) {
    var x = g.x, y = BODEN, w = Math.sin((s.t + g.x) / 6);
    c.save();
    if (g.platt) { c.translate(x + g.b / 2, y); c.scale(1 + g.platt * .6, Math.max(.12, 1 - g.platt)); c.translate(-(x + g.b / 2), -y); c.globalAlpha = Math.max(0, 1 - g.platt * .5); }
    if (g.art === 'gespenst') {
      var gy = y - 10 + w * 6;
      c.fillStyle = F.gr; c.beginPath(); c.arc(x + 20, gy - 26, 20, Math.PI, 0); c.lineTo(x + 40, gy);
      for (var i = 0; i < 4; i++) { c.lineTo(x + 35 - i * 10, gy - (i % 2 ? 0 : 7)); c.lineTo(x + 30 - i * 10, gy); }
      c.closePath(); c.fill(); augen(x + 20, gy - 28); c.fillStyle = F.sch; c.fillRect(x + 14, gy - 16, 12, 3);
    } else if (g.art === 'virus') {
      c.translate(x + 20, y - 20); c.rotate(-s.t / 8); c.fillStyle = F.gr;
      for (var k = 0; k < 8; k++) { c.rotate(Math.PI / 4); c.fillRect(-3, -22, 6, 10); c.beginPath(); c.arc(0, -22, 4, 0, 7); c.fill(); }
      c.beginPath(); c.arc(0, 0, 15, 0, 7); c.fill(); c.rotate(s.t / 8); augen(0, -2);
    } else if (g.art === 'fresser') {
      var maul = Math.abs(Math.sin(s.t / 5)) * .7;
      c.fillStyle = F.gr; c.beginPath(); c.moveTo(x + 24, y - 22); c.arc(x + 24, y - 22, 22, Math.PI + maul, Math.PI * 3 - maul); c.closePath(); c.fill();
      augen(x + 28, y - 32);
      c.fillStyle = F.ws; c.strokeStyle = F.sch; c.lineWidth = 2; c.beginPath(); c.arc(x - 4, y - 22, 8, 0, 7); c.fill(); c.stroke();
      c.beginPath(); c.moveTo(x - 4, y - 22); c.lineTo(x - 4, y - 27); c.moveTo(x - 4, y - 22); c.lineTo(x, y - 22); c.stroke();
    } else {
      c.fillStyle = F.gr; c.beginPath(); c.ellipse(x + 21, y - 6, 21, 7, 0, 0, 7); c.ellipse(x + 21, y - 15, 15, 6, 0, 0, 7); c.ellipse(x + 21, y - 23, 9, 5, 0, 0, 7); c.fill();
      augen(x + 21, y - 15); c.fillStyle = F.sch;
      for (var m = 0; m < 2; m++) { var a = s.t / 6 + m * 3; c.fillRect(x + 21 + Math.cos(a) * 18, y - 40 + Math.sin(a * 1.3) * 6, 3, 3); }
    }
    c.restore();
    if (!g.platt && g.zeigName) etikett(g.name, x + g.b / 2, y - g.h - 18, F.sch, F.ws);
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
  function zeichne() {
    c.setTransform(cv.width / W, 0, 0, cv.height / H, 0, 0);
    c.clearRect(0, 0, W, H);
    leipzig();
    c.fillStyle = F.sch; c.fillRect(0, BODEN, W, 3);
    for (var i = 0; i < 14; i++) c.fillRect(wiederhole(i * 79, W + 160, 1), BODEN + 10 + (i % 3) * 4, 8 + (i % 2) * 6, 2);
    s.bloecke.forEach(block);
    s.gaben.forEach(function (g) { form(g.l.form, g.x, g.y, 34, g.l.farbe); });
    s.gegner.forEach(gegner);
    if (s.kraft) { var k = s.kraft; figur(k.x, BODEN - k.sprung, .62, F.gelb, true, k.sprung > 0); if (!s.bekannt.kraft) etikett('Fachkraft: Fang mich!', k.x, BODEN - 92 - k.sprung, F.gelb, F.sch); }
    if (!(s.f.blink > 0 && Math.floor(s.t / 4) % 2)) figur(s.f.x, s.f.y, s.gross ? 1.35 : 1, F.bl, s.f.amBoden && s.lauf && !s.aus, !s.f.amBoden);
    s.funken.forEach(function (p) { c.globalAlpha = Math.max(0, p.l / 30); form(p.form, p.x, p.y, p.g, p.farbe); }); c.globalAlpha = 1;
    s.blasen.forEach(function (b) {
      c.font = '30px Anton, Impact, sans-serif'; var bw = c.measureText(b.text).width + 20;
      c.save(); c.translate(b.x, b.y); c.rotate(-.06); c.fillStyle = F.sch; c.fillRect(-bw / 2, -30, bw, 40); c.fillStyle = F.ws; c.fillText(b.text, -bw / 2 + 10, 2); c.restore();
    });
    LEISTUNGEN.forEach(function (l, i) { var x = W - 190 + i * 38, y = 24;
      if (s.gesammelt.indexOf(i) < 0) { c.strokeStyle = F.grh; c.lineWidth = 2; c.strokeRect(x - 13, y - 13, 26, 26); } else form(l.form, x, y, 24, l.farbe); });
  }

  // ---------- Spiel ----------
  function blase(text, x, y) { s.blasen.push({ text: text, x: x, y: y, l: 45 }); }
  function funken(x, y, n) { for (var i = 0; i < n; i++) { var l = LEISTUNGEN[i % 5]; s.funken.push({ x: x, y: y, vx: (Math.random() - .5) * 9, vy: -Math.random() * 8 - 2, l: 30, g: 8 + Math.random() * 9, form: l.form, farbe: l.farbe }); } }
  function springen() {
    if (s.demo) { demoEnde(); }
    if (s.aus || s.gewonnen) { neu(); starten(); return; }
    if (!s.lauf) starten();
    if (s.pause) { pauseUm(false); return; }
    if (s.f.amBoden) { s.f.vy = -15.5; s.f.amBoden = false; ton(TON.sprung); }
  }
  function starten() { s.lauf = true; meldung(''); if (startKnopf) startKnopf.hidden = true; }
  function meldung(t) { meldungEl.textContent = t; meldungEl.hidden = !t; }
  function treffer() {
    if (s.f.blink > 0) return;
    if (s.gross) { s.gross = false; s.f.blink = 90; ton(TON.schrumpfen); blase('OHO!', s.f.x, s.f.y - 140); return; }
    s.aus = true; ton(TON.oho); blase('OHO!', s.f.x, s.f.y - 110); meldung('OHO! Nochmal: Leertaste oder Tippen.');
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
  function schritt() {
    if (!s.lauf || s.pause || s.aus || s.gewonnen) return;
    s.t++; s.tempo = Math.min(7.5, 4.2 + s.t / 1400); s.weg += s.tempo;
    var k = s.gross ? 1.35 : 1, fh = 98 * k, fb = 30 * k;
    if (s.demo) demoSchritt();
    s.f.vy += .8; s.f.y += s.f.vy; if (s.f.blink > 0) s.f.blink--;
    if (s.f.y >= BODEN) { s.f.y = BODEN; s.f.vy = 0; s.f.amBoden = true; }
    var fl = s.f.x - fb / 2, fr = s.f.x + fb / 2, fo = s.f.y - fh;
    if (--s.naechstB <= 0) {
      var offen = LEISTUNGEN.map(function (l, i) { return i; }).filter(function (i) { return s.gesammelt.indexOf(i) < 0 && !s.bloecke.some(function (b) { return b.i === i && !b.leer; }); });
      if (offen.length) { var i = offen[Math.floor(Math.random() * offen.length)]; s.bloecke.push({ x: W + 20, y: BODEN - 170, l: LEISTUNGEN[i], i: i, stoss: 0 }); }
      s.naechstB = 110 + Math.floor(Math.random() * 60);
    }
    s.bloecke.forEach(function (b) {
      b.x -= s.tempo; if (b.stoss > 0) b.stoss -= 2;
      if (!b.leer && s.f.vy < 0 && fr > b.x && fl < b.x + 42 && fo <= b.y + 42 && fo > b.y + 14) { b.leer = true; b.stoss = 10; s.f.vy = 2; leistungHoch(b); }
    });
    s.bloecke = s.bloecke.filter(function (b) { return b.x > -60; });
    s.gaben.forEach(function (g) {
      g.alter = (g.alter || 0) + 1;
      if (g.alter < 14) { g.x -= s.tempo * .3; g.vy += .4; g.y += g.vy; }        // springt aus dem Block hoch
      else { g.x += (s.f.x - g.x) * .18; g.y += (s.f.y - 60 * (s.gross ? 1.35 : 1) - g.y) * .18; }   // dann fliegt sie zur Figur
      if (!g.weg && Math.abs(g.x - s.f.x) < 32 && g.y > fo - 24 && g.y < s.f.y) {
        g.weg = true;
        if (s.gesammelt.indexOf(g.i) < 0) {
          s.gesammelt.push(g.i); ton(TON.sammeln); blase('WOW!', g.x, g.y - 30); funken(g.x, g.y, 14);
          if (!s.demo && chips[g.i]) chips[g.i].classList.add('ist-gesammelt');
          if (s.gesammelt.length === LEISTUNGEN.length && !s.demo) gewinnen();
        }
      }
    });
    s.gaben = s.gaben.filter(function (g) { return !g.weg && g.x > -40; });
    if (--s.naechstG <= 0) {
      var v = GEGNER[Math.floor(Math.random() * GEGNER.length)];
      var g = Object.assign({ x: W + 30, platt: 0 }, v); g.zeigName = !s.bekannt[g.art]; s.bekannt[g.art] = true;
      s.gegner.push(g); s.naechstG = 70 + Math.floor(Math.random() * 80);
    }
    s.gegner.forEach(function (g) {
      g.x -= s.tempo + (g.art === 'virus' ? 1.5 : g.art === 'fresser' ? .8 : 0);
      if (g.platt) { g.platt += .06; return; }
      if (fr > g.x + 6 && fl < g.x + g.b - 6 && s.f.y > BODEN - g.h) {
        if (s.f.vy > 0 && s.f.y - s.f.vy <= BODEN - g.h + 8) {
          g.platt = .01; s.f.vy = -11; s.f.amBoden = false; ton(TON.platt); funken(g.x + g.b / 2, BODEN - g.h, 8);
          blase(['WOW!', 'AAH!', 'PLATT!'][Math.floor(Math.random() * 3)], g.x + g.b / 2, BODEN - g.h - 44);
        } else if (!s.demo) treffer();
      }
    });
    s.gegner = s.gegner.filter(function (g) { return g.x > -60 && g.platt < 1.2; });
    if (!s.kraft && !s.gross && --s.naechstK <= 0) s.kraft = { x: W + 30, sprung: 0, vsy: 0 };
    if (s.kraft) {
      var kr = s.kraft; kr.x -= s.tempo * .35; kr.x += Math.sin(s.t / 18) * 3.5;
      if (Math.abs(kr.x - s.f.x) < 130 && kr.sprung === 0 && Math.random() < .04) kr.vsy = 9;
      kr.sprung = Math.max(0, kr.sprung + kr.vsy); kr.vsy = kr.sprung > 0 ? kr.vsy - .6 : 0;
      if (Math.abs(kr.x - s.f.x) < 28 && Math.abs((BODEN - kr.sprung) - s.f.y) < 60) {
        s.kraft = null; s.gross = true; s.bekannt.kraft = true; s.naechstK = 900; ton(TON.wachsen); blase('AAH! Fachkraft gefunden', s.f.x + 80, s.f.y - 150); funken(s.f.x, s.f.y - 60, 20);
      } else if (kr.x < -40) { s.kraft = null; s.naechstK = 500; }
    }
    s.funken.forEach(function (p) { p.x += p.vx; p.y += p.vy; p.vy += .35; p.l--; }); s.funken = s.funken.filter(function (p) { return p.l > 0; });
    s.blasen.forEach(function (b) { b.l--; b.y -= .6; }); s.blasen = s.blasen.filter(function (b) { return b.l > 0; });
  }
  function gewinnen() {
    s.gewonnen = true; ton(TON.sieg); blase('AAH!', s.f.x + 40, s.f.y - 140); funken(s.f.x, s.f.y - 80, 30);
    meldung(''); if (sieg) sieg.hidden = false; document.dispatchEvent(new Event('konfetti'));
  }

  // ---------- Demo: höchstens 5 Sekunden, erklärt das Spiel, dann „Spielen“ ----------
  var DEMO = [[0, 'So geht’s: Springen mit Leertaste oder Tippen'], [75, 'Auf die Probleme springen: platt!'], [150, 'Schwarze Blöcke von unten anstoßen: Leistung!'], [225, 'Alle fünf Leistungen sammeln. Bereit?']];
  function demoSchritt() {
    DEMO.forEach(function (d) { if (s.t === d[0] + 1) meldung(d[1]); });
    var nah = s.gegner.find(function (g) { return !g.platt && g.x - s.f.x < 70 && g.x - s.f.x > 20; });
    var blockNah = s.bloecke.find(function (b) { return !b.leer && b.x - s.f.x < 40 && b.x - s.f.x > -10; });
    if ((nah || blockNah) && s.f.amBoden) { s.f.vy = -15.5; s.f.amBoden = false; }
    if (s.t === 30) s.kraft = { x: W - 120, sprung: 0, vsy: 0 };
    if (s.t >= 300) demoEnde();
  }
  function demoEnde() {
    if (!s || !s.demo) return;
    neu(false); meldung(''); if (startKnopf) startKnopf.hidden = false;
  }

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
  function pauseUm(an) {
    s.pause = an === undefined ? !s.pause : an; knopfPause.setAttribute('aria-pressed', s.pause ? 'true' : 'false');
    knopfPause.querySelector('span').textContent = s.pause ? 'Weiter' : 'Pause';
    if (!s.demo) meldung(s.pause ? 'Pause. Leertaste oder Tippen: weiter.' : '');
  }
  knopfPause.addEventListener('click', function () { if (s.lauf && !s.aus && !s.gewonnen) pauseUm(); });
  var nochmal = wurzel.querySelector('[data-nochmal]'); if (nochmal) nochmal.addEventListener('click', function () { neu(); starten(); cv.focus(); });
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { if (!e[0].isIntersecting && s.lauf && !s.demo && !s.pause && !s.aus && !s.gewonnen) pauseUm(true); }).observe(cv);
  document.addEventListener('visibilitychange', function () { if (document.hidden && s.lauf && !s.demo && !s.pause && !s.aus && !s.gewonnen) pauseUm(true); });
  window.addEventListener('resize', function () { groesse(); });

  groesse();
  if (ruhig) { neu(false); meldung('Springen mit Leertaste oder Tippen. Probleme platt machen, Leistungen sammeln.'); if (startKnopf) startKnopf.hidden = false; }
  else neu(true);
  requestAnimationFrame(schleife);
})();
