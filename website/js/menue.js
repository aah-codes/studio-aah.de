// Mega-Menü „Service“: öffnet per Klick, schließt mit Esc oder Klick daneben.
// Ohne JavaScript führt „Service“ einfach auf /service/.
(() => {
  const schalter = document.querySelector('.mm-toggle');
  const menue = document.getElementById('mm');
  const schleier = document.querySelector('.mm-schleier');
  if (!schalter || !menue || !schleier) return;

  // Fokus nur bei Bedienung mit der Tastatur in das Menü setzen – sonst erscheint beim Klick ein Fokusrahmen
  function oeffnen(perTastatur) {
    menue.hidden = false;
    schleier.hidden = false;
    requestAnimationFrame(() => { menue.classList.add('offen'); schleier.classList.add('offen'); });
    schalter.setAttribute('aria-expanded', 'true');
    const erster = menue.querySelector('a');
    if (erster && perTastatur) erster.focus({ preventScroll: true });
  }
  function schliessen(zurueck) {
    if (schalter.getAttribute('aria-expanded') !== 'true') return;
    menue.classList.remove('offen');
    schleier.classList.remove('offen');
    schalter.setAttribute('aria-expanded', 'false');
    setTimeout(() => { if (!menue.classList.contains('offen')) { menue.hidden = true; schleier.hidden = true; } }, 450);
    if (zurueck) schalter.focus();
  }
  schalter.addEventListener('click', (e) => {
    e.preventDefault();
    schalter.getAttribute('aria-expanded') === 'true' ? schliessen(false) : oeffnen(e.detail === 0);
  });
  schleier.addEventListener('click', () => schliessen(false));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') schliessen(true); });
  menue.addEventListener('focusout', (e) => {
    if (!menue.contains(e.relatedTarget) && e.relatedTarget !== schalter) schliessen(false);
  });
})();

// Newsletter im Fuß: sendet an Brevo ohne Seitenwechsel und zeigt danach einen Hinweis (ohne JavaScript öffnet Brevo eine eigene Seite)
(() => {
  const f = document.querySelector('.fuss-newsletter');
  if (!f || !window.fetch) return;
  const meldung = f.querySelector('.fuss-nl-meldung');
  f.addEventListener('submit', (e) => {
    e.preventDefault();
    if (f.email_address_check.value) return; // Spam-Falle
    const knopf = f.querySelector('button');
    knopf.disabled = true;
    fetch(f.action, { method: 'POST', body: new FormData(f), mode: 'no-cors' })
      .then(() => { meldung.textContent = 'Fast geschafft: Bitte bestätigen Sie Ihre Anmeldung über den Link in der E-Mail, die ich Ihnen gerade geschickt habe.'; f.reset(); })
      .catch(() => { meldung.textContent = 'Das hat leider nicht geklappt. Bitte versuchen Sie es später noch einmal oder schreiben Sie an info@studio-aah.de.'; })
      .finally(() => { meldung.hidden = false; knopf.disabled = false; });
  });
})();

// Sprungmarken auf Leistungsseiten: markiert den Abschnitt, in dem man gerade ist (schiebt nur die Leiste, nie die Seite)
(() => {
  const leiste = document.querySelector('.lsx-chips');
  if (!leiste || !('IntersectionObserver' in window)) return;
  const links = [...leiste.querySelectorAll('a[href^="#"]')];
  const ziele = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const beob = new IntersectionObserver((eintraege) => {
    eintraege.forEach((e) => {
      if (!e.isIntersecting) return;
      links.forEach((a) => a.classList.toggle('aktiv', a.getAttribute('href') === `#${e.target.id}`));
      const aktiv = links.find((a) => a.classList.contains('aktiv'));
      if (aktiv && leiste.scrollWidth > leiste.clientWidth) leiste.scrollTo({ left: aktiv.offsetLeft - 16, behavior: 'smooth' });
    });
  }, { rootMargin: '-35% 0px -60% 0px' });
  ziele.forEach((z) => beob.observe(z));
})();

// Film zu einer Referenz: Klick auf das Vorschaubild öffnet den Film groß in einem Fenster (Esc, Klick daneben oder × schließt)
(() => {
  const knoepfe = document.querySelectorAll('.film-knopf');
  if (!knoepfe.length) return;
  let dlg;
  const zu = () => { const v = dlg.querySelector('video'); v.pause(); v.removeAttribute('src'); v.load(); dlg.close(); };
  knoepfe.forEach((k) => k.addEventListener('click', () => {
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.className = 'film-dialog';
      dlg.innerHTML = '<button type="button" class="film-zu" aria-label="Film schließen">×</button><video controls playsinline></video>';
      document.body.appendChild(dlg);
      dlg.querySelector('.film-zu').addEventListener('click', zu);
      dlg.addEventListener('click', (e) => { if (e.target === dlg) zu(); });
      dlg.addEventListener('cancel', (e) => { e.preventDefault(); zu(); });
    }
    const v = dlg.querySelector('video');
    v.src = k.dataset.film;
    v.setAttribute('aria-label', k.dataset.titel || 'Film');
    dlg.showModal();
    v.play().catch(() => {});
  }));
})();

// Erklärfilm Corporate Identity (Brand-Seite): startet, wenn er ins Bild kommt; „Noch einmal ansehen“ startet neu.
// Bei „Bewegung reduzieren“ steht sofort das fertige Bild.
(() => {
  document.querySelectorAll('.ci-film').forEach((film) => {
    const svgs = [...film.querySelectorAll('svg')];
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      svgs.forEach((s) => { if (s.pauseAnimations) { s.pauseAnimations(); s.setCurrentTime(14); } });
      return;
    }
    film.classList.add('wartet');
    svgs.forEach((s) => s.pauseAnimations && s.pauseAnimations());
    // WCAG 2.2.2: Bewegung, die von selbst läuft, hält nach dem Aufbau an (rund 10 s Austausch, dann Ruhe)
    let ruhe = null;
    const start = () => {
      clearTimeout(ruhe);
      film.classList.add('neu');
      void film.offsetWidth; // Animationen zurücksetzen
      film.classList.remove('neu', 'wartet', 'ruhe');
      svgs.forEach((s) => { if (s.setCurrentTime) { s.setCurrentTime(0); s.unpauseAnimations(); } });
      ruhe = setTimeout(() => { svgs.forEach((s) => s.pauseAnimations && s.pauseAnimations()); film.classList.add('ruhe'); }, 22000);
    };
    const knopf = film.querySelector('.ci-nochmal-knopf');
    if (knopf) knopf.addEventListener('click', start);
    if (!('IntersectionObserver' in window)) { start(); return; }
    // data-wiederholen: kurzer Film (unter 5 s) startet bei jedem Hineinscrollen neu (Bauhaus-Formen, Anna 11.10.2026)
    const wieder = film.hasAttribute('data-wiederholen');
    const beob = new IntersectionObserver((e) => { if (e[0].isIntersecting) { start(); if (!wieder) beob.disconnect(); } }, { threshold: wieder ? 0.6 : 0.12 });
    beob.observe(film);
  });
})();

// Referenz-Karussell: blättert alle 7 Sekunden weiter (nur sichtbar und ohne „Bewegung reduzieren“),
// Pfeile blättern, Pause-Knopf hält an; Wischen auf dem Handy funktioniert über das Scrollen der Spur.
(() => {
  const ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-karussell]').forEach((ks) => {
    const spur = ks.querySelector('.ks-spur'), karten = [...spur.children], punkte = ks.querySelector('.ks-punkte');
    const pk = ks.querySelector('[data-pause]');
    karten.forEach(() => punkte.appendChild(document.createElement('i')));
    let nr = 0, uhr = null, sichtbar = false;
    const markiere = () => { [...punkte.children].forEach((p, i) => { p.classList.remove('aktiv'); void p.offsetWidth; p.classList.toggle('aktiv', i === nr); }); };
    const zeige = (n) => { nr = (n + karten.length) % karten.length; spur.scrollTo({ left: karten[nr].offsetLeft - spur.offsetLeft }); markiere(); };
    const lauf = () => { clearInterval(uhr); if (sichtbar && !ks.classList.contains('pause')) uhr = setInterval(() => zeige(nr + 1), 7000); };
    ks.querySelector('[data-weiter]').addEventListener('click', () => { zeige(nr + 1); lauf(); });
    ks.querySelector('[data-zurueck]').addEventListener('click', () => { zeige(nr - 1); lauf(); });
    pk.addEventListener('click', () => {
      const p = ks.classList.toggle('pause');
      pk.textContent = p ? '▶' : '❚❚';
      pk.setAttribute('aria-label', p ? 'Automatisches Weiterblättern starten' : 'Automatisches Weiterblättern anhalten');
      if (!p) markiere();
      lauf();
    });
    // Nach Wischen die aktuelle Karte übernehmen
    let t; spur.addEventListener('scroll', () => { clearTimeout(t); t = setTimeout(() => {
      const i = karten.reduce((b, k, j) => Math.abs(k.offsetLeft - spur.offsetLeft - spur.scrollLeft) < Math.abs(karten[b].offsetLeft - spur.offsetLeft - spur.scrollLeft) ? j : b, 0);
      if (i !== nr) { nr = i; markiere(); lauf(); }
    }, 120); });
    if (ruhig) { ks.classList.add('pause'); pk.textContent = '▶'; pk.setAttribute('aria-label', 'Automatisches Weiterblättern starten'); }
    markiere();
    // Bilder aller Karten vorladen, sobald das Karussell in die Nähe kommt (sonst bleibt die nächste Karte beim Blättern kurz weiß)
    const vorladen = () => spur.querySelectorAll('img[loading="lazy"]').forEach((i) => { i.loading = 'eager'; });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver((e, b) => { if (e[0].isIntersecting) { vorladen(); b.disconnect(); } }, { rootMargin: '600px 0px' }).observe(ks);
      new IntersectionObserver((e) => { sichtbar = e[0].isIntersecting; lauf(); }, { threshold: 0.3 }).observe(ks);
    } else vorladen();
  });
})();

// Umschalter „Für wen“ (Tabs): Klick und Pfeiltasten
(() => {
  document.querySelectorAll('.dk-umschalter[role="tablist"]').forEach((liste) => {
    const tabs = [...liste.querySelectorAll('[role="tab"]')];
    const waehle = (b) => tabs.forEach((x) => {
      const an = x === b;
      x.setAttribute('aria-selected', String(an)); x.tabIndex = an ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).hidden = !an;
    });
    liste.addEventListener('click', (e) => { const b = e.target.closest('[role="tab"]'); if (b) waehle(b); });
    liste.addEventListener('keydown', (e) => {
      const i = tabs.indexOf(document.activeElement); if (i < 0) return;
      const n = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : null;
      if (n === null) return;
      e.preventDefault(); const b = tabs[(n + tabs.length) % tabs.length]; waehle(b); b.focus();
    });
  });
})();

// Website-Ökosystem: gestrichelte Kurven von jeder Karte zur Website, je Richtung ein wandernder Punkt, jeder zweite blau (SMIL, Zeit läuft mit dem Film)
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  document.querySelectorAll('.oeko').forEach((oeko) => {
    const svg = oeko.querySelector('.oeko-linien'), web = oeko.querySelector('.oeko-website');
    const zeichnen = () => {
      svg.innerHTML = '';
      if (getComputedStyle(svg).display === 'none') return;
      const o = oeko.getBoundingClientRect(), w = web.getBoundingClientRect();
      let punkt = 0;
      oeko.querySelectorAll('.oeko-karte').forEach((k, i) => {
        const r = k.getBoundingClientRect(), links = r.left < w.left;
        // Andockpunkte gleichmäßig über die Website-Seite verteilen, je nach Zahl der Karten auf dieser Seite
        const geschw = [...k.parentElement.children], n = geschw.length, nr = geschw.indexOf(k);
        const x1 = (links ? r.right : r.left) - o.left, y1 = r.top + r.height / 2 - o.top;
        const x2 = (links ? w.left : w.right) - o.left, y2 = w.top + w.height * (n > 1 ? 0.2 + nr * 0.6 / (n - 1) : 0.5) - o.top;
        const mx = (x1 + x2) / 2, d = `M${x1} ${y1}C${mx} ${y1} ${mx} ${y2} ${x2} ${y2}`;
        const pfad = document.createElementNS(NS, 'path'); pfad.setAttribute('d', d); pfad.setAttribute('class', 'oeko-linie'); svg.appendChild(pfad);
        const richtung = k.dataset.richtung, rueck = `M${x2} ${y2}C${mx} ${y2} ${mx} ${y1} ${x1} ${y1}`;
        const wege = richtung === 'rein' ? [d] : richtung === 'raus' ? [rueck] : [d, rueck];
        wege.forEach((weg, j) => {
          const c = document.createElementNS(NS, 'circle'); c.setAttribute('r', '4'); c.setAttribute('class', punkt++ % 2 ? 'ci-f oeko-punkt-blau' : 'ci-f'); c.setAttribute('opacity', '0');
          const start = 5.4 + i * 0.35 + j * 1.6;
          c.innerHTML = `<animateMotion dur="3.2s" begin="${start}s" repeatCount="indefinite" path="${weg}"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="3.2s" begin="${start}s" repeatCount="indefinite"/>`;
          svg.appendChild(c);
        });
      });
    };
    zeichnen();
    let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(zeichnen, 200); });
    // Linien einblenden, wenn die Außenkarten stehen (rund 4,5 s nach Filmstart)
    const an = () => { oeko.classList.remove('linien-an'); setTimeout(() => { zeichnen(); oeko.classList.add('linien-an'); }, window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 4500); };
    if ('IntersectionObserver' in window) new IntersectionObserver((e, b) => { if (e[0].isIntersecting) { an(); b.disconnect(); } }, { threshold: 0.12 }).observe(oeko);
    else an();
    const knopf = oeko.querySelector('.ci-nochmal-knopf'); if (knopf) knopf.addEventListener('click', an);
  });
})();

// Aktivstatus im Menü (Anna 13.10.2026): Der Kopf ist auf allen Seiten gleich, deshalb markiert dieses Skript die aktuelle Seite
// (aria-current="page") und den Bereich, in dem sie liegt (aria-current="true", z. B. Blog bei einem Artikel, Leistungen auf /service/).
(() => {
  const ohneIndex = (p) => p.replace(/index\.html$/, '');
  const hier = ohneIndex(location.pathname);
  const start = ohneIndex(new URL(document.querySelector('.kopf-logo')?.getAttribute('href') || './', location.href).pathname);
  document.querySelectorAll('.kopf-nav > ul > li > a:not(.mm-toggle), .kopf-nav .mm-liste a, .kopf-mobil nav a').forEach((a) => {
    const ziel = ohneIndex(new URL(a.getAttribute('href'), location.href).pathname);
    if (ziel === hier) a.setAttribute('aria-current', 'page');
    else if (ziel !== start && hier.startsWith(ziel)) a.setAttribute('aria-current', 'true');
  });
  if (hier.startsWith(`${start}service/`)) {
    document.querySelector('.mm-toggle')?.classList.add('aktiv');
    document.querySelector('.kopf-mobil .mobil-unter > summary')?.classList.add('aktiv');
  }
})();

// Projektseiten: Elemente mit data-einblenden bekommen beim ersten Sichtbarwerden die Klasse „sichtbar“ (Sitemap, Notizzettel, Schieberegler);
// Schieberegler Wireframe ↔ fertig folgt dem Regler
(() => {
  const els = document.querySelectorAll('[data-einblenden]');
  if (els.length && 'IntersectionObserver' in window) {
    const b = new IntersectionObserver((e) => e.forEach((x) => { if (x.isIntersecting) { x.target.classList.add('sichtbar'); b.unobserve(x.target); } }), { threshold: 0.35 });
    els.forEach((e) => b.observe(e));
  } else els.forEach((e) => e.classList.add('sichtbar'));
  document.querySelectorAll('.cs-schieber input').forEach((r) => r.addEventListener('input', () => {
    const s = r.closest('.cs-schieber'); s.style.transition = 'none'; s.style.setProperty('--pos', r.value + '%');
  }));
})();

// Vorher/Nachher-Film (Projektseiten): blättert durch alte und neue Seiten, jede Seite scrollt einmal durch; dazwischen eine Wischblende.
// Läuft nur sichtbar und ohne „Bewegung reduzieren“, Pause-Taste hält an. Karriere-Abschnitt: Pause-Taste für das Durchlaufen der Seiten.
(() => {
  const ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-vfilm]').forEach((f) => {
    const seiten = [...f.querySelectorAll('.vf-seite')], fenster = f.querySelector('.vf-fenster'), blende = f.querySelector('.vf-blende');
    const zeiger = f.querySelector('.vf-zeiger'), adresse = f.querySelector('.vf-adresse'), phase = f.querySelector('.vf-phase'), texte = f.querySelector('.vf-texte');
    const knopf = f.querySelector('.vf-knopf');
    let nr = -1, uhr = null, laeuft = false, sichtbar = false;
    const warte = (ms, fn) => { clearTimeout(uhr); uhr = setTimeout(fn, ms); };
    const zeige = (n) => {
      const s = seiten[n], vorher = seiten[nr];
      if (vorher) { vorher.classList.remove('aktiv'); vorher.style.transition = 'opacity .5s'; vorher.style.transform = 'translateY(0)'; }
      s.style.transition = 'opacity .5s'; s.style.transform = 'translateY(0)'; s.classList.add('aktiv'); nr = n;
      adresse.textContent = 'bauer-ingbau.de/' + s.dataset.pfad; phase.textContent = texte.dataset[s.dataset.phase];
      const weg = Math.max(0, s.offsetHeight - fenster.offsetHeight);
      warte(700, () => { s.style.transition = 'opacity .5s, transform 4s ease-in-out'; s.style.transform = `translateY(-${weg}px)`; warte(4300, weiter); });
    };
    const weiter = () => {
      if (!laeuft) return;
      const n = (nr + 1) % seiten.length, s = seiten[n];
      if (seiten[nr] && s.dataset.phase !== seiten[nr].dataset.phase) {   // Wischblende zwischen Vorher und Nachher
        blende.classList.remove('weg'); blende.classList.add('an');
        warte(1400, () => { zeige(n); blende.classList.add('weg'); blende.classList.remove('an'); });
        return;
      }
      if (+s.dataset.x > 0) {   // „Klick“ in die Navigation
        zeiger.style.opacity = 1; zeiger.style.left = s.dataset.x + '%'; zeiger.style.top = '3%';
        warte(800, () => { zeiger.classList.add('klick'); setTimeout(() => { zeiger.classList.remove('klick'); zeiger.style.opacity = 0; }, 200); zeige(n); });
      } else zeige(n);
    };
    const start = () => { if (laeuft || ruhig) return; laeuft = true; knopf.textContent = '❚❚'; knopf.setAttribute('aria-label', 'Film anhalten'); weiter(); };
    const halt = () => { laeuft = false; clearTimeout(uhr); knopf.textContent = '▶'; knopf.setAttribute('aria-label', 'Film abspielen');
      const s = seiten[nr]; if (s) { const m = getComputedStyle(s).transform; s.style.transition = 'opacity .5s'; s.style.transform = m === 'none' ? '' : m; } };
    knopf.addEventListener('click', () => { if (laeuft) { halt(); f.dataset.angehalten = '1'; } else { delete f.dataset.angehalten; laeuft = true; knopf.textContent = '❚❚'; knopf.setAttribute('aria-label', 'Film anhalten'); weiter(); } });
    zeige(0); if (ruhig) halt();
    if ('IntersectionObserver' in window) new IntersectionObserver((e) => { sichtbar = e[0].isIntersecting; if (sichtbar && !f.dataset.angehalten) start(); else if (!sichtbar && laeuft) halt(); }, { threshold: 0.4 }).observe(f);
  });
  document.querySelectorAll('.kr-knopf').forEach((k) => k.addEventListener('click', () => {
    const s = k.closest('.cs-karriere'), p = s.classList.toggle('pause');
    k.textContent = p ? '▶' : '❚❚'; k.setAttribute('aria-label', p ? 'Bewegung fortsetzen' : 'Bewegung anhalten');
  }));
})();

// Handy-Paar (Projektseiten): rechts scrollt das Bewerbungsformular hoch und füllt sich wie von Hand (nachgestellt, nichts wird gesendet).
// Läuft nur sichtbar und ohne „Bewegung reduzieren“; Pause-Taste hält beide Handys an.
(() => {
  const ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-handyduo]').forEach((d) => {
    const seite = d.querySelector('.hd-rechts .h3d-seite'), start = parseFloat(getComputedStyle(d.querySelector('.hd-rechts')).getPropertyValue('--start')) || 0;
    const felder = [...d.querySelectorAll('.hd-eingabe')], knopf = d.querySelector('.hd-knopf');
    let uhr = null, laeuft = false;
    const warte = (ms) => new Promise((r) => { uhr = setTimeout(r, ms); });
    const runde = async () => {
      while (laeuft) {
        felder.forEach((f) => { f.textContent = ''; f.classList.remove('tippt'); });
        seite.style.transform = 'translateY(0)'; await warte(1800); if (!laeuft) return;
        seite.style.transform = `translateY(-${start}%)`; await warte(2600);
        for (const f of felder) {
          if (!laeuft) return;
          if (f.offsetTop + seite.offsetTop > seite.parentElement.offsetHeight * 0.85 - seite.getBoundingClientRect().top + seite.parentElement.getBoundingClientRect().top) {
            seite.style.transform = `translateY(-${(f.offsetTop - seite.parentElement.offsetHeight * 0.4) / seite.offsetHeight * 100}%)`; await warte(2500);
          }
          f.classList.add('tippt');
          for (const z of f.dataset.text) { if (!laeuft) return; f.textContent += z; await warte(70); }
          f.classList.remove('tippt'); await warte(350);
        }
        await warte(3000);
      }
    };
    const an = () => { if (laeuft || ruhig || d.dataset.angehalten) return; laeuft = true; d.classList.remove('pause'); runde(); };
    const aus = () => { laeuft = false; clearTimeout(uhr); d.classList.add('pause'); };
    knopf.addEventListener('click', () => {
      if (laeuft) { aus(); d.dataset.angehalten = '1'; knopf.textContent = '▶'; knopf.setAttribute('aria-label', 'Bewegung fortsetzen'); }
      else { delete d.dataset.angehalten; knopf.textContent = '❚❚'; knopf.setAttribute('aria-label', 'Bewegung anhalten'); an(); }
    });
    if (ruhig) { d.classList.add('pause'); felder.forEach((f) => { f.textContent = f.dataset.text; }); seite.style.transform = `translateY(-${start}%)`; }
    else if ('IntersectionObserver' in window) new IntersectionObserver((e) => { if (e[0].isIntersecting) an(); else aus(); }, { threshold: 0.3 }).observe(d);
  });
})();

// Storytelling-Film (Projektseiten): Szenen nacheinander – scrollen, Zettel einblenden, tippen, zoomen, „klicken“; zwischen Vorher und Nachher eine Blende.
// Läuft nur sichtbar und ohne „Bewegung reduzieren“; Pause-Taste; Kapitel-Knöpfe springen zu einer Szene.
(() => {
  const ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-story]').forEach((f) => {
    const datenEl = f.querySelector('.st-daten'), daten = JSON.parse(datenEl.textContent);
    const szenen = [...f.querySelectorAll('.st-szene')], fenster = f.querySelector('.st-fenster'), blende = f.querySelector('.vf-blende');
    const zeiger = f.querySelector('.vf-zeiger'), adresse = f.querySelector('.vf-adresse'), phase = f.querySelector('.st-phase');
    const titel = f.querySelector('.st-titel'), knopf = f.querySelector('.st-knopf'), kapitel = [...f.querySelectorAll('.st-kapitel')];
    let nr = 0, uhren = [], laeuft = false;
    const spaeter = (ms, fn) => uhren.push(setTimeout(fn, ms));
    const stopp = () => { uhren.forEach(clearTimeout); uhren = []; };
    const zuruecksetzen = (sz) => {
      const s = sz.querySelector('.st-seite'), z = sz.querySelector('.st-zoom');
      s.style.setProperty('--d', '0ms'); s.style.setProperty('--y', daten[+sz.dataset.i].von || 0);
      z.style.setProperty('--s', 1); sz.querySelectorAll('.st-notiz').forEach((n) => n.classList.remove('zeigen'));
      sz.querySelectorAll('.st-eingabe').forEach((e) => { e.textContent = ''; e.classList.remove('tippt'); });
    };
    const tippe = (felder, i) => {
      if (i >= felder.length) return;
      const e = felder[i], text = e.dataset.text; let k = 0; e.classList.add('tippt');
      const schritt = () => { e.textContent = text.slice(0, ++k); if (k < text.length) spaeter(55, schritt); else { e.classList.remove('tippt'); spaeter(250, () => tippe(felder, i + 1)); } };
      schritt();
    };
    const zeige = (i, sofort) => {
      const d = daten[i], sz = szenen[i];
      szenen.forEach((x, j) => { if (j !== i) x.classList.remove('aktiv'); });
      zuruecksetzen(sz); void sz.offsetWidth; sz.classList.add('aktiv'); nr = i;
      if (adresse) adresse.textContent = 'bauer-ingbau.de/' + (d.pfad || ''); if (titel) titel.textContent = d.titel || '';
      if (phase) phase.textContent = datenEl.dataset[d.phase] || '';
      const k = kapitel.filter((x) => +x.dataset.ziel <= i).pop(); kapitel.forEach((x) => x.setAttribute('aria-current', String(x === k)));
      if (sofort) { // ruhig: Endzustand ohne Bewegung zeigen
        sz.querySelector('.st-seite').style.setProperty('--y', d.bis || 0);
        const alle = sz.querySelectorAll('.st-notiz'); alle.forEach((n, j) => { if ((d.bis || 0) === (d.von || 0) || j === alle.length - 1) n.classList.add('zeigen'); });
        sz.querySelectorAll('.st-eingabe').forEach((e) => { e.textContent = e.dataset.text; });
        return;
      }
      const s = sz.querySelector('.st-seite'), dauer = d.dauer;
      if ((d.bis || 0) !== (d.von || 0)) spaeter(500, () => { s.style.setProperty('--d', Math.round(dauer * 0.55) + 'ms'); s.style.setProperty('--y', d.bis); });
      // beim Scrollen: neuer Zettel ersetzt den vorigen (der zeigt sonst auf die falsche Stelle)
      const scrollt = (d.bis || 0) !== (d.von || 0), zettel = sz.querySelectorAll('.st-notiz');
      (d.notizen || []).forEach((n, j) => spaeter(n[3], () => { if (scrollt && j) zettel[j - 1].classList.remove('zeigen'); zettel[j].classList.add('zeigen'); }));
      if (d.zoom) spaeter(d.zoom[3], () => { const z = sz.querySelector('.st-zoom'); z.style.setProperty('--ox', d.zoom[1] + '%'); z.style.setProperty('--oy', d.zoom[2] + '%'); z.style.setProperty('--s', d.zoom[0]); });
      // vorausgefüllte Felder (aus der vorigen Szene) stehen sofort da, die übrigen werden getippt
      sz.querySelectorAll('.st-eingabe[data-fertig]').forEach((e) => { e.textContent = e.dataset.text; });
      const felder = [...sz.querySelectorAll('.st-eingabe:not([data-fertig])')];
      if (felder.length) spaeter(d.tippen_ab || 1500, () => tippe(felder, 0));
      spaeter(dauer, () => weiter(i));
    };
    const weiter = (i) => {
      const d = daten[i], n = (i + 1) % daten.length;
      const geh = () => {
        if (daten[n].phase !== d.phase) { blende.classList.remove('weg'); blende.classList.add('an'); spaeter(1500, () => { zeige(n); blende.classList.add('weg'); blende.classList.remove('an'); }); }
        else zeige(n);
      };
      if (d.klick) {
        zeiger.style.opacity = 1; zeiger.style.left = d.klick[0] + '%'; zeiger.style.top = d.klick[1] + '%';
        spaeter(800, () => { zeiger.classList.add('klick'); spaeter(220, () => { zeiger.classList.remove('klick'); zeiger.style.opacity = 0; geh(); }); });
      } else geh();
    };
    const an = () => { if (laeuft) return; laeuft = true; knopf.textContent = '❚❚'; knopf.setAttribute('aria-label', 'Film anhalten'); zeige(nr); };
    const aus = () => { laeuft = false; stopp(); knopf.textContent = '▶'; knopf.setAttribute('aria-label', 'Film abspielen'); };
    knopf.addEventListener('click', () => { if (laeuft) { aus(); f.dataset.angehalten = '1'; } else { delete f.dataset.angehalten; an(); } });
    kapitel.forEach((k) => k.addEventListener('click', () => { stopp(); nr = +k.dataset.ziel; if (ruhig || f.dataset.angehalten) zeige(nr, true); else { laeuft = false; an(); } }));
    f.zeigeSzene = (i) => { aus(); f.dataset.angehalten = '1'; zeige(i, true); }; // Endzustand einer Szene (Prüfen, Kapitel bei Pause)
    zeige(0, true);
    if (!ruhig && 'IntersectionObserver' in window) new IntersectionObserver((e) => { if (e[0].isIntersecting) { if (!f.dataset.angehalten) an(); } else if (laeuft) { laeuft = false; stopp(); } }, { threshold: 0.45 }).observe(f);
    else aus();
  });
})();

// Foto-Mockups (Projektseiten): Szene auf die Breite des Rahmens skalieren; Buch: Doppelseiten wechseln (Pause-Taste, nur sichtbar)
(() => {
  const ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const passe = (fm) => fm.style.setProperty('--k', fm.clientWidth / +getComputedStyle(fm).getPropertyValue('--sb'));
  document.querySelectorAll('[data-fm]').forEach((fm) => { passe(fm); if ('ResizeObserver' in window) new ResizeObserver(() => passe(fm)).observe(fm); });
  document.querySelectorAll('[data-buch]').forEach((b) => {
    const schirme = [...b.querySelectorAll('.fm-schirm')], knopf = b.querySelector('.fm-knopf'), n = schirme[0].children.length;
    let i = 0, uhr = null, sichtbar = false, aus = ruhig;
    const zeige = () => schirme.forEach((s) => [...s.children].forEach((x, j) => x.classList.toggle('aktiv', j === i)));
    const lauf = () => { clearInterval(uhr); if (sichtbar && !aus) uhr = setInterval(() => { i = (i + 1) % n; zeige(); }, 3200); };
    knopf.addEventListener('click', () => { aus = !aus; knopf.textContent = aus ? '▶' : '❚❚'; knopf.setAttribute('aria-label', aus ? 'Blättern starten' : 'Blättern anhalten'); lauf(); });
    if (ruhig) { knopf.textContent = '▶'; knopf.setAttribute('aria-label', 'Blättern starten'); }
    zeige();
    if ('IntersectionObserver' in window) new IntersectionObserver((e) => { sichtbar = e[0].isIntersecting; lauf(); }, { threshold: 0.3 }).observe(b);
  });
})();

// Heft (Unternehmenspräsentation): rechte Seite blättert in 3D um, dann liegt die nächste Doppelseite offen; nur sichtbar, Pause-Taste
(() => {
  const ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-heft]').forEach((h) => {
    // Heft wie gedruckt (Anna 14.10.2026): zu (nur Umschlag, mittig) → aufklappen → Doppelseiten → Rückseite → von vorn.
    // Leere Angabe = dort ist kein Blatt (links vom Umschlag, rechts von der Rückseite)
    const bogen = JSON.parse(h.dataset.seiten), heft = h.querySelector('.hf-heft'), l = h.querySelector('.hf-l'), r = h.querySelector('.hf-r');
    const blatt = h.querySelector('.hf-blatt'), vorn = h.querySelector('.hf-vorn'), hinten = h.querySelector('.hf-hinten'), knopf = h.querySelector('.hf-knopf');
    bogen.flat().filter(Boolean).forEach((s) => { const i = new Image(); i.src = s; });
    let i = 0, uhr = null, sichtbar = false, aus = ruhig;
    const setze = (img, s) => { img.classList.toggle('leer', !s); if (s) img.src = s; };
    const lage = (k) => { heft.classList.toggle('hf-zu-vorn', !bogen[k][0]); heft.classList.toggle('hf-zu-hinten', !bogen[k][1]); };
    const zeige = (k) => { setze(l, bogen[k][0]); setze(r, bogen[k][1]); lage(k); };
    zeige(0);
    const blaettern = () => {
      const n = (i + 1) % bogen.length;
      if (n === 0) {
        // nach der Rückseite: kurz ausblenden und wieder zugeklappt von vorn beginnen
        heft.classList.add('hf-weg');
        setTimeout(() => { zeige(0); i = 0; heft.classList.remove('hf-weg'); }, 500);
        return;
      }
      // Blatt zeigt vorn die alte rechte Seite und dreht sie nach links; danach ohne Übergang zurück und unsichtbar
      vorn.src = bogen[i][1]; hinten.src = bogen[n][0]; setze(r, bogen[n][1]); lage(n); blatt.classList.add('dreht');
      setTimeout(() => { setze(l, bogen[n][0]); blatt.classList.add('still'); blatt.classList.remove('dreht'); void blatt.offsetWidth; blatt.classList.remove('still'); i = n; }, 1150);
    };
    const lauf = () => { clearInterval(uhr); if (sichtbar && !aus) uhr = setInterval(blaettern, 3200); };
    knopf.addEventListener('click', () => { aus = !aus; knopf.textContent = aus ? '▶' : '❚❚'; knopf.setAttribute('aria-label', aus ? 'Blättern starten' : 'Blättern anhalten'); lauf(); });
    if (ruhig) { knopf.textContent = '▶'; knopf.setAttribute('aria-label', 'Blättern starten'); }
    if ('IntersectionObserver' in window) new IntersectionObserver((e) => { sichtbar = e[0].isIntersecting; lauf(); }, { threshold: 0.3 }).observe(h);
  });
})();

// Mega-Menü-Film: Pause-Taste (Anna 14.10.2026)
(() => {
  document.querySelectorAll('.cs-mega-film').forEach((f) => {
    const k = f.querySelector('.mf-knopf'); if (!k) return;
    k.addEventListener('click', () => { const aus = f.classList.toggle('pause'); k.textContent = aus ? '▶' : '❚❚'; k.setAttribute('aria-label', aus ? 'Film abspielen' : 'Film anhalten'); });
  });
})();

// Funnel-Karte (Variante B): Pause-Taste für das langsame Durchscrollen der Seiten
(() => {
  document.querySelectorAll('.cs-funnel-karte').forEach((f) => {
    const k = f.querySelector('.fk-knopf'); if (!k) return;
    k.addEventListener('click', () => { const aus = f.classList.toggle('pause'); k.textContent = aus ? '▶' : '❚❚'; k.setAttribute('aria-label', aus ? 'Bewegung starten' : 'Bewegung anhalten'); });
  });
})();
