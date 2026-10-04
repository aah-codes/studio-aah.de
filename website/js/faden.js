// „Roter Faden“: Eine Linie zeichnet sich beim Scrollen vom Hero bis zum Knopf „Projekt anfragen“.
// Sie erzählt die Überschrift „Ihr Weg zu digitaler Sichtbarkeit“. Rein dekorativ (aria-hidden).
// Bei „Bewegung reduzieren“ steht die Linie vollständig da; ohne JavaScript gibt es keine Linie.
(() => {
  const main = document.querySelector('main.mit-faden');
  const svg = document.querySelector('.roter-faden');
  if (!main || !svg) return;
  const linie = svg.querySelector('.faden-linie');
  const punkt = svg.querySelector('.faden-punkt');
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let laenge = 0, tabelle = [], gezeichnet = false;

// Punkte: die Linie bleibt immer am rechten Rand (in der Hälfte des Seitenabstands, damit sie keine Inhalte kreuzt)
// und biegt erst am Ende waagerecht in den Knopf „Projekt anfragen“.
function punkte() {
  const m = main.getBoundingClientRect();
  const y = (el, wo = 'top') => el.getBoundingClientRect()[wo] - m.top;
  const breite = main.clientWidth;
  const randSeite = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--rand-seite')) || 32;
  const rechts = breite - Math.max(10, randSeite / 2);
  const hero = main.querySelector('.hero-buehne') || main.querySelector('.hero');
  const knopf = main.querySelector('.weg-ziel-knopf');
  if (!hero || !knopf) return null;
  const k = knopf.getBoundingClientRect();
  const ky = k.top - m.top + k.height / 2;
  return [
    [rechts, y(hero, 'bottom') - 8],
    [rechts, ky - 80],
    [rechts - 80, ky],
    [k.right - m.left + 14, ky],
  ];
}

  // Pfad: senkrechte Strecken an den Rändern, Seitenwechsel als kompakte S-Kurve (senkrechte Tangenten),
  // damit die Linie nur in den Lücken zwischen den Abschnitten die Seite wechselt
  function kurve(p) {
    let d = `M ${p[0][0].toFixed(1)} ${p[0][1].toFixed(1)}`;
    for (let i = 1; i < p.length; i++) {
      const [x1, y1] = p[i - 1], [x2, y2] = p[i];
      if (Math.abs(x2 - x1) < 1) { d += ` L ${x2.toFixed(1)} ${y2.toFixed(1)}`; continue; }
      if (Math.abs(y2 - y1) < 1) { d += ` L ${x2.toFixed(1)} ${y2.toFixed(1)}`; continue; }
      const naechster = p[i + 1];
      if (naechster && Math.abs(naechster[1] - y2) < 1) { d += ` C ${x1.toFixed(1)} ${y2.toFixed(1)}, ${x1.toFixed(1)} ${y2.toFixed(1)}, ${x2.toFixed(1)} ${y2.toFixed(1)}`; continue; }
      const h = (y2 - y1) / 2;
      d += ` C ${x1.toFixed(1)} ${(y1 + h).toFixed(1)}, ${x2.toFixed(1)} ${(y2 - h).toFixed(1)}, ${x2.toFixed(1)} ${y2.toFixed(1)}`;
    }
    return d;
  }

  function aufbauen() {
    const p = punkte();
    if (!p) return;
    svg.setAttribute('width', main.clientWidth);
    svg.setAttribute('height', main.scrollHeight);
    linie.setAttribute('d', kurve(p));
    laenge = linie.getTotalLength();
    linie.style.strokeDasharray = `${laenge}`;
    // Nachschlagetabelle: Höhe auf der Seite → gezeichnete Länge
    tabelle = [];
    // laufendes Maximum der Höhe, damit kleine Ausschläge der Kurve das Zeichnen nicht anhalten
    let hoechst = -Infinity;
    for (let l = 0; l <= laenge; l += 6) { hoechst = Math.max(hoechst, linie.getPointAtLength(l).y); tabelle.push([hoechst, l]); }
    tabelle.push([Math.max(hoechst, linie.getPointAtLength(laenge).y), laenge]);
    zeichnen();
  }

  function zeichnen() {
    gezeichnet = false;
    if (!laenge) return;
    let l = laenge;
    if (!still) {
      const spitze = window.scrollY + window.innerHeight * 0.62 - (main.getBoundingClientRect().top + window.scrollY);
      l = 0;
      for (const [yy, ll] of tabelle) { if (yy <= spitze) l = ll; else break; }
      if (spitze >= tabelle[tabelle.length - 1][0]) l = laenge;
    }
    linie.style.strokeDashoffset = `${laenge - l}`;
    const pt = linie.getPointAtLength(l);
    punkt.setAttribute('cx', pt.x.toFixed(1));
    punkt.setAttribute('cy', pt.y.toFixed(1));
    svg.classList.toggle('angekommen', l >= laenge - 2);
  }

  window.addEventListener('scroll', () => { if (!gezeichnet) { gezeichnet = true; requestAnimationFrame(zeichnen); } }, { passive: true });
  let warte;
  window.addEventListener('resize', () => { clearTimeout(warte); warte = setTimeout(aufbauen, 200); });
  window.addEventListener('load', aufbauen);
  aufbauen();
})();
