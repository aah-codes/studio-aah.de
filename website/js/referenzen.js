// Projektseiten (/referenzen/<projekt>/): Abläufe der Bausteine aus werkzeuge/referenzen.py.
// Wird nur dort geladen (wie css/referenzen.css). Alles, was von selbst läuft, hält bei „Bewegung reduzieren“ an
// und hat eine Pause-Taste (WCAG 2.2.2).
(() => {
  const ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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
  // Läuft nur sichtbar und ohne „Bewegung reduzieren“, Pause-Taste hält an.
  (() => {
    document.querySelectorAll('[data-vfilm]').forEach((f) => {
      const seiten = [...f.querySelectorAll('.vf-seite')], fenster = f.querySelector('.vf-fenster'), blende = f.querySelector('.vf-blende');
      const zeiger = f.querySelector('.vf-zeiger'), adresse = f.querySelector('.vf-adresse'), phase = f.querySelector('.vf-phase'), texte = f.querySelector('.vf-texte');
      const knopf = f.querySelector('.vf-knopf'), basis = adresse.textContent;
      let nr = -1, uhr = null, laeuft = false, sichtbar = false;
      const warte = (ms, fn) => { clearTimeout(uhr); uhr = setTimeout(fn, ms); };
      const zeige = (n) => {
        const s = seiten[n], vorher = seiten[nr];
        if (vorher) { vorher.classList.remove('aktiv'); vorher.style.transition = 'opacity .5s'; vorher.style.transform = 'translateY(0)'; }
        s.style.transition = 'opacity .5s'; s.style.transform = 'translateY(0)'; s.classList.add('aktiv'); nr = n;
        adresse.textContent = basis + s.dataset.pfad; phase.textContent = texte.dataset[s.dataset.phase];
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
  })();

  // Handy-Paar (Projektseiten): rechts scrollt das Bewerbungsformular hoch und füllt sich wie von Hand (nachgestellt, nichts wird gesendet).
  // Läuft nur sichtbar und ohne „Bewegung reduzieren“; Pause-Taste hält beide Handys an.
  (() => {
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
    document.querySelectorAll('[data-story]').forEach((f) => {
      const datenEl = f.querySelector('.st-daten'), daten = JSON.parse(datenEl.textContent);
      const szenen = [...f.querySelectorAll('.st-szene')], fenster = f.querySelector('.st-fenster'), blende = f.querySelector('.vf-blende');
      const zeiger = f.querySelector('.vf-zeiger'), adresse = f.querySelector('.vf-adresse'), phase = f.querySelector('.st-phase');
      const titel = f.querySelector('.st-titel'), knopf = f.querySelector('.st-knopf'), kapitel = [...f.querySelectorAll('.st-kapitel')];
      const basis = adresse ? adresse.textContent : '';
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
        if (adresse) adresse.textContent = basis + (d.pfad || ''); if (titel) titel.textContent = d.titel || '';
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

  // Pause-Tasten für Bewegung, die per CSS läuft (WCAG 2.2.2): die Klasse „pause“ am Bereich hält sie an.
  // Mega-Menü-Film, Funnel-Karte, laufende Bildschirmwand im Einstieg, Bühne mit Handy, Karriere-Seiten.
  (() => {
    const TASTEN = [['.cs-mega-film', '.mf-knopf', 'Film'], ['.cs-funnel-karte', '.fk-knopf'], ['.cs-hero-wand', '.hw-knopf'],
                    ['.cs-buehne-bild', '.bn-knopf'], ['.cs-karriere', '.kr-knopf']];
    TASTEN.forEach(([bereich, taste, was = 'Bewegung']) => document.querySelectorAll(bereich).forEach((b) => {
      const k = b.querySelector(taste);
      if (!k) return;
      k.addEventListener('click', () => {
        const aus = b.classList.toggle('pause');
        k.textContent = aus ? '▶' : '❚❚';
        k.setAttribute('aria-label', `${was} ${aus ? (was === 'Film' ? 'abspielen' : 'starten') : 'anhalten'}`);
      });
    }));
  })();

  // Galerie zum Durchklicken (Referenz Jana, Anna 16.10.2026): Klick aufs Bild zeigt das nächste, ohne eigene Pfeile und Zähler
  (() => {
    document.querySelectorAll('.cs-durchklick').forEach((g) => {
      const bilder = [...g.querySelectorAll('.dk-bilder img')]; let i = 0;
      g.querySelector('.dk-bilder').addEventListener('click', () => { i = (i + 1) % bilder.length; bilder.forEach((b, k) => { b.hidden = k !== i; }); });
    });
  })();
})();
