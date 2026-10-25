// Allgemeine Abläufe auf allen Seiten: Menüs, Newsletter, Bereichsleiste, Erklärfilme, Karussell, „Für wen“, Aktivstatus.
// Die Abläufe der Projektseiten stehen in js/referenzen.js. Alles läuft in einem Block, damit nichts global wird.
(() => {
  // Klasse „js“ am <html>: Einblend-Animationen verstecken Inhalte nur, wenn JavaScript läuft (ohne bleibt alles sichtbar)
  document.documentElement.classList.add('js');

  // Bewegung reduzieren (Systemeinstellung): einmal abfragen, alle Teile richten sich danach
  const ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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
      if (schalter.getAttribute('aria-expanded') === 'true') schliessen(false);
      else oeffnen(e.detail === 0);
    });
    schleier.addEventListener('click', () => schliessen(false));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') schliessen(true); });
    menue.addEventListener('focusout', (e) => {
      if (!menue.contains(e.relatedTarget) && e.relatedTarget !== schalter) schliessen(false);
    });
  })();

  // Mobilmenü (<details>, funktioniert ohne JavaScript): Escape schließt es, der Fokus geht zurück auf „Menü“
  (() => {
    const mobil = document.querySelector('.kopf-mobil');
    if (!mobil) return;
    mobil.addEventListener('keydown', (e) => {
      if (e.key !== 'Escape' || !mobil.open) return;
      mobil.open = false;
      mobil.querySelector('summary').focus();
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

  // Bereichsleiste (Leistungsseiten, Blog, Preisseite): markiert den Abschnitt, in dem man gerade ist (schiebt nur die Leiste, nie die Seite)
  (() => {
    const leiste = document.querySelector('.preis-leiste');
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

  // Erklärfilm Corporate Identity (Brand-Seite): startet, wenn er ins Bild kommt; „Noch einmal ansehen“ startet neu.
  // Bei „Bewegung reduzieren“ steht sofort das fertige Bild.
  (() => {
    document.querySelectorAll('.ci-film').forEach((film) => {
      const svgs = [...film.querySelectorAll('svg')];
      if (ruhig) {
        svgs.forEach((s) => { if (s.pauseAnimations) { s.pauseAnimations(); s.setCurrentTime(14); } });
        return;
      }
      film.classList.add('wartet');
      svgs.forEach((s) => s.pauseAnimations && s.pauseAnimations());
      // WCAG 2.2.2: Bewegung, die von selbst läuft, hält nach dem Aufbau an (rund 22 s, dann Ruhe);
      // bis dahin lässt sie sich mit „Anhalten“ stoppen und mit „Weiter“ fortsetzen
      const DAUER = 22000;
      const pause = film.querySelector('.ci-pause-knopf');
      let ruhe = null, rest = DAUER, seit = 0;
      const anhalten = (an) => {
        film.classList.toggle('angehalten', an);
        svgs.forEach((s) => { if (!s.pauseAnimations) return; if (an) s.pauseAnimations(); else s.unpauseAnimations(); });
        if (pause) pause.innerHTML = an ? 'Weiter <span aria-hidden="true">▶</span>' : 'Anhalten <span aria-hidden="true">❚❚</span>';
      };
      const zurRuhe = () => {
        svgs.forEach((s) => s.pauseAnimations && s.pauseAnimations());
        film.classList.add('ruhe');
        if (pause) pause.hidden = true;
      };
      const laufen = () => { seit = Date.now(); ruhe = setTimeout(zurRuhe, rest); };
      const start = () => {
        clearTimeout(ruhe);
        film.classList.add('neu');
        void film.offsetWidth; // Animationen zurücksetzen
        film.classList.remove('neu', 'wartet', 'ruhe');
        svgs.forEach((s) => s.setCurrentTime && s.setCurrentTime(0));
        anhalten(false);
        if (pause) pause.hidden = false;
        rest = DAUER;
        laufen();
      };
      if (pause) pause.addEventListener('click', () => {
        const an = !film.classList.contains('angehalten');
        if (an) { clearTimeout(ruhe); rest -= Date.now() - seit; } else laufen();
        anhalten(an);
      });
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
  // Barrierefrei nach WAI-Muster „Carousel“: steht still, solange der Tastatur-Fokus darin ist; Bildschirmleser
  // sagen die neue Karte nur an, wenn nicht automatisch geblättert wird (aria-live „off“ beim Laufen).
  (() => {
    document.querySelectorAll('[data-karussell]').forEach((ks) => {
      const spur = ks.querySelector('.ks-spur'), karten = [...spur.children], punkte = ks.querySelector('.ks-punkte');
      const pk = ks.querySelector('[data-pause]');
      karten.forEach(() => punkte.appendChild(document.createElement('i')));
      let nr = 0, uhr = null, sichtbar = false, fokus = false;
      const markiere = () => { [...punkte.children].forEach((p, i) => { p.classList.remove('aktiv'); void p.offsetWidth; p.classList.toggle('aktiv', i === nr); }); };
      const zeige = (n) => { nr = (n + karten.length) % karten.length; spur.scrollTo({ left: karten[nr].offsetLeft - spur.offsetLeft }); markiere(); };
      const lauf = () => {
        clearInterval(uhr);
        const an = sichtbar && !fokus && !ks.classList.contains('pause');
        if (an) uhr = setInterval(() => zeige(nr + 1), 7000);
        spur.setAttribute('aria-live', an ? 'off' : 'polite');
      };
      ks.addEventListener('focusin', () => { fokus = true; lauf(); });
      ks.addEventListener('focusout', (e) => { if (!ks.contains(e.relatedTarget)) { fokus = false; lauf(); } });
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
        // am Handy gewählten Reiter ganz ins Bild schieben (Leiste ist seitlich ziehbar)
        if (an && liste.scrollWidth > liste.clientWidth) liste.scrollTo({ left: x.offsetLeft - (liste.clientWidth - x.offsetWidth) / 2, behavior: 'smooth' });
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
      const an = () => { oeko.classList.remove('linien-an'); setTimeout(() => { zeichnen(); oeko.classList.add('linien-an'); }, ruhig ? 0 : 4500); };
      if ('IntersectionObserver' in window) new IntersectionObserver((e, b) => { if (e[0].isIntersecting) { an(); b.disconnect(); } }, { threshold: 0.12 }).observe(oeko);
      else an();
      const knopf = oeko.querySelector('.ci-nochmal-knopf'); if (knopf) knopf.addEventListener('click', an);
    });
  })();

  // Golden Circle im Blog (Anna 19.10.2026): Kreise erscheinen einmal von innen nach außen, sobald die Grafik zu 40 % sichtbar ist.
  // Ohne IntersectionObserver oder JavaScript bleibt das fertige Bild stehen; „weniger Bewegung“ regelt stil.css.
  (() => {
    const gc = document.querySelector('.golden-circle');
    if (!gc || !('IntersectionObserver' in window)) return;
    gc.classList.add('is-animated');
    new IntersectionObserver((e, b) => { if (e[0].isIntersecting) { gc.classList.add('is-visible'); b.disconnect(); } }, { threshold: 0.4 }).observe(gc);
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

  // Link auf eine Frage im FAQ (z. B. #was-der-check-ist vom Formular): Frage aufklappen, dann hinspringen
  (() => {
    function oeffnen(hash) {
      let ziel = null;
      try { ziel = hash.length > 1 && document.getElementById(decodeURIComponent(hash.slice(1))); } catch (e) { return; }
      const frage = ziel && ziel.closest('details');
      if (frage && !frage.open) { frage.open = true; ziel.scrollIntoView(); }
    }
    addEventListener('hashchange', () => oeffnen(location.hash));
    // auch beim zweiten Klick auf denselben Link (dann gibt es kein hashchange)
    document.addEventListener('click', (e) => { const a = e.target.closest('a[href^="#"]'); if (a) oeffnen(a.getAttribute('href')); });
    oeffnen(location.hash);
  })();

  // Kostenrechner-Knopf unten rechts verdeckt nie einen anderen Knopf, Mail-/Telefon-Link oder Kontakt-/Anfrage-Link (Website-Check 18.10.2026):
  // liegt einer darunter, blendet er sich aus, bis wieder Platz ist. Ohne JavaScript bleibt er wie bisher sichtbar.
  (() => {
    // auf der Landingpage Website-Check der eigene Knopf zum Formular (der Kostenrechner-Knopf ist dort ausgeblendet)
    const knopf = document.querySelector('.sticky-check') || document.querySelector('.sticky-rechner');
    if (!knopf) return;
    const ziele = [...document.querySelectorAll('a, button, input[type="submit"]')].filter((el) => !knopf.contains(el)
      && (el.matches('.button, button, input[type="submit"], a[href^="mailto:"], a[href^="tel:"], form a')
        || /anfrag|kontakt|termin|e-mail|anrufen/i.test(el.textContent)));
    function pruefen() {
      const k = knopf.getBoundingClientRect();
      const verdeckt = ziele.some((el) => {
        const r = el.getBoundingClientRect();
        return r.width && r.left < k.right + 8 && r.right > k.left - 8 && r.top < k.bottom + 8 && r.bottom > k.top - 8;
      });
      knopf.classList.toggle('weg', verdeckt);
    }
    // Scroll-Ereignisse kommen höchstens einmal je Bild, deshalb ohne eigene Drosselung
    addEventListener('scroll', pruefen, { passive: true });
    addEventListener('resize', pruefen);
    addEventListener('load', pruefen);
    // erste Prüfung ohne Überblendung, sonst blitzt der Knopf beim Laden über „Projekt anfragen“ auf
    knopf.style.transition = 'none';
    pruefen();
    knopf.getBoundingClientRect(); // Stil jetzt anwenden, bevor die Überblendung zurückkommt
    knopf.style.transition = '';
  })();
})();
