// Kostenrechner auf der Preisseite: rechnet nur im Browser, speichert und sendet nichts.
// Ergebnis ist ein unverbindlicher Kostenvoranschlag (netto); weiter per E-Mail oder als PDF (Druckdialog des Browsers).
(() => {
  const form = document.getElementById('rechner-wahl');
  if (!form) return;

  // Pakete je Bereich (eins wählbar, Marketing mehrere) – Preise wie auf der Seite
  const bereiche = [
    { id: 'brand', name: 'Brand', pakete: [['Basic', 850], ['Medium', 2500], ['Premium', 4500]] },
    { id: 'uiux', name: 'UI/UX', pakete: [['Mini UX-Audit', 1200], ['UI/UX Audit Pro', 1500], ['Redesign kleine Webanwendung', 2600], ['Plattform / SaaS', 5850]] },
    { id: 'website', name: 'Website', pakete: [['Onepager', 1150], ['Website 5–6 Seiten', 2450], ['Redesign', 2850], ['Komplexes Projekt', 6000]] },
    { id: 'ki', name: 'KI & Digitalisierung', pakete: [['KI-Check', 900], ['KI-Einführung', 2000]] },
    { id: 'marketing', name: 'Marketing & Vertrieb', mehrfach: true, pakete: [['LinkedIn aufsetzen', 500], ['Post-Vorlagen', 400], ['Fachartikel', 300], ['Webinar aufsetzen', 850]] },
    { id: 'design', name: 'Design-Paket', pakete: [['Basic', 450], ['Umfassend', 2600]] },
  ];
  // Zusatzleistungen: art „anzahl“ = Zähler, „website“ = nur mit Website-Paket, „ohneWebsite“ = nur ohne
  const zusatz = [
    { id: 'seite', name: 'Weitere Seite', preis: 150, art: 'anzahl', bedingung: 'website' },
    { id: 'blog', name: 'Blog', preis: 490, bedingung: 'website' },
    { id: 'sprache', name: 'Weitere Sprache (+30 % auf das Website-Paket)', anteil: 0.3, art: 'anzahl', bedingung: 'website' },
    { id: 'newsletter', name: 'Newsletter-Anbindung', preis: 260, bedingung: 'website' },
    { id: 'texte', name: 'Texte schreiben (je Seite)', preis: 130, art: 'anzahl' },
    { id: 'schulung', name: 'Schulung (PDF oder Online-Termin)', preis: 70, wahl: ['PDF-Anleitung', 'Online-Termin'] },
    { id: 'kontakt', name: 'Kontaktformular', preis: 130, bedingung: 'ohneWebsite' },
    { id: 'seo', name: 'SEO-Grundeinrichtung', preis: 260, bedingung: 'ohneWebsite' },
    { id: 'logo', name: 'Logo einzeln', preis: 990 },
    { id: 'visitenkarte', name: 'Visitenkarte', preis: 195 },
    { id: 'social', name: 'Social-Media-Set', preis: 390 },
    { id: 'wartung', name: 'Wartung', monat: 45 },
    { id: 'illu', name: 'Illustration & Infografik', anfrage: true },
    { id: 'motion', name: 'Motion Design', anfrage: true },
  ];
  const LAUNCH = 150;
  const euro = (n) => Math.round(n).toLocaleString('de-DE');

  // Formular aufbauen
  let html = '';
  bereiche.forEach((b) => {
    html += `<fieldset class="wahl-gruppe"><legend>${b.name}</legend><div class="wahl-optionen">`;
    if (!b.mehrfach) html += `<label class="wahl-option"><input type="radio" name="${b.id}" value="" checked><span class="wahl-name">Nicht nötig</span></label>`;
    b.pakete.forEach(([n, p], i) => {
      html += `<label class="wahl-option"><input type="${b.mehrfach ? 'checkbox' : 'radio'}" name="${b.id}" value="${i}"><span class="wahl-name">${n}</span><span class="wahl-preis">ab ${euro(p)} €</span></label>`;
    });
    html += '</div></fieldset>';
  });
  html += '<fieldset class="wahl-gruppe"><legend>Zusatzleistungen</legend><div class="wahl-optionen">';
  html += `<p class="wahl-pflicht" id="wahl-launch" hidden>✓ Launch ${euro(LAUNCH)} € – bei jeder Website dabei (Domain, DNS, Umzug, Livegang)</p>`;
  zusatz.forEach((z) => {
    const preis = z.anfrage ? 'auf Anfrage' : z.monat ? `ab ${z.monat} € / Monat` : z.anteil ? '+30 %' : `${euro(z.preis)} €`;
    html += `<label class="wahl-option" data-zusatz="${z.id}"><input type="checkbox" name="z-${z.id}"><span class="wahl-name">${z.name}</span><span class="wahl-preis">${preis}</span>`;
    if (z.art === 'anzahl') html += `<input class="wahl-anzahl" type="number" name="n-${z.id}" min="1" max="30" value="1" aria-label="Anzahl ${z.name}">`;
    if (z.wahl) html += `<select class="wahl-auswahl" name="w-${z.id}" aria-label="Form der Schulung">${z.wahl.map((w) => `<option>${w}</option>`).join('')}</select>`;
    html += '<span class="wahl-hinweis"></span></label>';
  });
  html += '</div></fieldset>';
  form.innerHTML = html;

  const el = (id) => document.getElementById(id);
  let angezeigt = 0;

  function auswahl() {
    const posten = [];
    let einmalig = 0, monatlich = 0, websitePreis = 0;
    bereiche.forEach((b) => {
      form.querySelectorAll(`input[name="${b.id}"]:checked`).forEach((inp) => {
        if (inp.value === '') return;
        const [n, p] = b.pakete[+inp.value];
        posten.push([`${b.name}: ${n}`, p]);
        einmalig += p;
        if (b.id === 'website') websitePreis = p;
      });
    });
    const mitWebsite = websitePreis > 0;
    el('wahl-launch').hidden = !mitWebsite;
    if (mitWebsite) { posten.push(['Launch (Pflicht bei Website)', LAUNCH]); einmalig += LAUNCH; }
    zusatz.forEach((z) => {
      const label = form.querySelector(`[data-zusatz="${z.id}"]`);
      const cb = label.querySelector('input[type="checkbox"]');
      const gesperrt = (z.bedingung === 'website' && !mitWebsite) || (z.bedingung === 'ohneWebsite' && mitWebsite);
      cb.disabled = gesperrt;
      if (gesperrt) cb.checked = false;
      label.classList.toggle('gesperrt', gesperrt);
      label.querySelector('.wahl-hinweis').textContent = gesperrt ? (z.bedingung === 'website' ? 'nur mit Website-Paket' : 'im Website-Paket enthalten') : '';
      if (!cb.checked) return;
      const anzahl = z.art === 'anzahl' ? Math.max(1, +form.elements[`n-${z.id}`].value || 1) : 1;
      if (z.anfrage) { posten.push([`${z.name}`, null]); return; }
      if (z.monat) { monatlich += z.monat; posten.push([`${z.name}`, z.monat, 'monat']); return; }
      const preis = z.anteil ? websitePreis * z.anteil * anzahl : z.preis * anzahl;
      const extra = z.wahl ? ` – ${form.elements[`w-${z.id}`].value}` : '';
      posten.push([`${z.name}${anzahl > 1 ? ` × ${anzahl}` : ''}${extra}`, preis]);
      einmalig += preis;
    });
    return { posten, einmalig, monatlich };
  }

  function zaehlen(ziel) {
    const start = angezeigt, t0 = performance.now(), dauer = 500;
    const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function schritt(t) {
      const f = still ? 1 : Math.min(1, (t - t0) / dauer);
      const wert = start + (ziel - start) * (1 - Math.pow(1 - f, 3));
      el('summe-einmalig').textContent = euro(wert);
      el('summe-brutto').textContent = euro(wert * 1.19);
      if (f < 1) requestAnimationFrame(schritt); else angezeigt = ziel;
    }
    requestAnimationFrame(schritt);
    // Sicherheitsnetz: falls der Browser keine Animationsbilder liefert (z. B. Hintergrund-Tab), Endwert setzen
    clearTimeout(zaehlen.t); zaehlen.t = setTimeout(() => { if (angezeigt !== ziel) { angezeigt = ziel; el('summe-einmalig').textContent = euro(ziel); el('summe-brutto').textContent = euro(ziel * 1.19); } }, dauer + 100);
  }

  function zeilenText(a) {
    return a.posten.map(([n, p, art]) => `– ${n}: ${p === null ? 'auf Anfrage' : art === 'monat' ? `ab ${euro(p)} € / Monat` : `ab ${euro(p)} €`}`).join('\n');
  }

  function aktualisieren() {
    const a = auswahl();
    zaehlen(a.einmalig);
    el('summe-monat-zeile').hidden = !a.monatlich;
    el('summe-monat').textContent = euro(a.monatlich);
    el('summe-liste').innerHTML = a.posten.length
      ? a.posten.map(([n, p, art]) => `<li><span>${n}</span><b>${p === null ? 'auf Anfrage' : art === 'monat' ? `${euro(p)} €/Monat` : `${euro(p)} €`}</b></li>`).join('')
      : '<li class="gedaempft">Noch nichts ausgewählt.</li>';
    const text = `Hallo Anna,\n\nich habe mir mit dem Kostenrechner auf studio-aah.de folgendes zusammengestellt:\n\n${zeilenText(a) || '– (noch nichts ausgewählt)'}\n\nRichtwert: ab ${euro(a.einmalig)} € netto einmalig${a.monatlich ? ` zzgl. ab ${euro(a.monatlich)} € / Monat` : ''}\n\nIch würde gern ein kostenloses Erstgespräch vereinbaren.\n\nÜber mich / mein Vorhaben:\n`;
    el('rechner-mail').href = `mailto:info@studio-aah.de?subject=${encodeURIComponent('Kostenvoranschlag über den Rechner')}&body=${encodeURIComponent(text)}`;
    // Druckfassung für das PDF
    const datum = new Date().toLocaleDateString('de-DE');
    el('druck-bereich').innerHTML = `<p class="druck-marke">STUDIO AAH!</p><h1>Kostenvoranschlag (unverbindlich)</h1><p>Erstellt am ${datum} mit dem Kostenrechner auf studio-aah.de</p>
      <table>${a.posten.map(([n, p, art]) => `<tr><td>${n}</td><td>${p === null ? 'auf Anfrage' : art === 'monat' ? `ab ${euro(p)} € / Monat` : `ab ${euro(p)} €`}</td></tr>`).join('')}
      <tr class="druck-summe"><td>Richtwert einmalig (netto)</td><td>ab ${euro(a.einmalig)} €</td></tr><tr><td>inkl. 19 % USt.</td><td>ab ${euro(a.einmalig * 1.19)} €</td></tr>${a.monatlich ? `<tr><td>monatlich (netto)</td><td>ab ${euro(a.monatlich)} €</td></tr>` : ''}</table>
      <p><b>So geht es weiter:</b> 1. Kostenvoranschlag · 2. kostenloses Erstgespräch (Ist-Stand, Ziele, Bedarf, Zielgruppe) · 3. Angebot · 4. Vertrag</p>
      <p>Der Festpreis entsteht erst nach dem Erstgespräch. Kontakt: info@studio-aah.de · studio-aah.de</p>`;
  }

  form.addEventListener('input', aktualisieren);
  form.addEventListener('change', aktualisieren);
  el('rechner-pdf').addEventListener('click', () => { aktualisieren(); document.body.classList.add('druck-rechner'); window.print(); });
  window.addEventListener('afterprint', () => document.body.classList.remove('druck-rechner'));
  aktualisieren();
})();

// Bereichsleiste: markiert beim Scrollen den Abschnitt, in dem man gerade ist
(() => {
  const links = [...document.querySelectorAll('.preis-leiste a')];
  if (!links.length || !('IntersectionObserver' in window)) return;
  const ziele = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const beob = new IntersectionObserver((eintraege) => {
    eintraege.forEach((e) => {
      if (!e.isIntersecting) return;
      links.forEach((a) => a.classList.toggle('aktiv', a.getAttribute('href') === `#${e.target.id}`));
      const aktiv = links.find((a) => a.classList.contains('aktiv'));
      if (aktiv) aktiv.scrollIntoView({ block: 'nearest', inline: 'nearest' });
    });
  }, { rootMargin: '-35% 0px -60% 0px' });
  ziele.forEach((z) => beob.observe(z));
})();
