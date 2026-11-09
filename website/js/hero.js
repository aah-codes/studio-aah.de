// Hero der Startseite „Bauhaus-Bühne“ (Anna, freigegeben 09.11.2026)
// – Das Auge der Figur folgt Maus oder Finger („Hier werden Sie gesehen.“).
// – Maus oder Tastatur-Fokus auf einer Leistung: Die Figur zeigt mit dem Arm darauf und schaut hin.
// – Klick auf die Figur: neue Pose und neuer Ausruf (AAH! → OHO! → WOW!).
// Ohne JavaScript steht die fertige Figur in der Pose „AAH!“; bei „Bewegung reduzieren“ wechseln die Posen ohne Übergang (CSS).
(() => {
  const hero = document.querySelector('.bb-hero');
  if (!hero) return;
  const figur = hero.querySelector('.bb-figur');
  const svg = figur.querySelector('svg');
  const ausruf = hero.querySelector('.bb-ausruf span');
  const POSEN = [
    { ruf: 'AAH!', 'arm-l': 145, 'arm-r': -145, 'bein-l': 8, 'bein-r': -8 },
    { ruf: 'OHO!', 'arm-l': 165, 'arm-r': -34, 'bein-l': 0, 'bein-r': -38 },
    { ruf: 'WOW!', 'arm-l': 92, 'arm-r': -92, 'bein-l': 22, 'bein-r': -22 },
  ];
  let nr = 0;
  const setze = (pose) => ['arm-l', 'arm-r', 'bein-l', 'bein-r'].forEach((k) => figur.style.setProperty(`--${k}`, `${pose[k]}deg`));
  // Punkt der Figur (Koordinaten der Zeichnung) auf dem Bildschirm
  const punkt = (x, y) => { const m = svg.getScreenCTM(); return { x: m.a * x + m.c * y + m.e, y: m.b * x + m.d * y + m.f }; };

  const schaue = (zx, zy) => {
    const kopf = punkt(0, -352), dx = zx - kopf.x, dy = zy - kopf.y, d = Math.hypot(dx, dy) || 1, r = Math.min(13, d / 10);
    figur.style.setProperty('--ax', `${(dx / d * r).toFixed(1)}px`);
    figur.style.setProperty('--ay', `${(dy / d * r).toFixed(1)}px`);
  };
  hero.addEventListener('pointermove', (e) => schaue(e.clientX, e.clientY));

  // Zeigen: der Arm auf der Seite der Form dreht sich zur Form, der andere hängt abgespreizt (Hand neben dem Rock)
  const zeige = (li) => {
    const f = li.querySelector('.bb-form').getBoundingClientRect(), fx = f.left + f.width / 2, fy = f.top + f.height / 2;
    const links = fx < punkt(0, 0).x, s = punkt(links ? -30 : 30, -290);
    const w = Math.atan2(-(fx - s.x), fy - s.y) * 180 / Math.PI;
    figur.style.setProperty(links ? '--arm-l' : '--arm-r', `${w.toFixed(0)}deg`);
    figur.style.setProperty(links ? '--arm-r' : '--arm-l', `${links ? -34 : 34}deg`);
    schaue(fx, fy);
  };
  const zurueck = () => setze(POSEN[nr]);
  hero.querySelectorAll('.bb-f').forEach((li) => {
    const a = li.querySelector('a');
    li.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') zeige(li); });
    li.addEventListener('pointerleave', zurueck);
    a.addEventListener('focus', () => zeige(li));
    a.addEventListener('blur', zurueck);
  });

  figur.addEventListener('click', () => {
    nr = (nr + 1) % POSEN.length;
    setze(POSEN[nr]);
    ausruf.textContent = POSEN[nr].ruf;
    ausruf.classList.remove('bb-neu');
    void ausruf.offsetWidth; // Animation neu starten
    ausruf.classList.add('bb-neu');
  });
})();
