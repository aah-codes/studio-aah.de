// Kostenrechner auf der Preisseite: rechnet nur im Browser, speichert und sendet nichts.
// Daten kommen aus js/pakete-daten.js (erzeugt aus werkzeuge/preise-daten.json).
// Ergebnis ist ein unverbindlicher Kostenvoranschlag (netto); weiter per E-Mail oder als PDF (Druckdialog des Browsers).
(() => {
  const form = document.getElementById('rechner-wahl');
  const D = window.PREISE;
  if (!form || !D) return;
  const euro = (n) => Math.round(n).toLocaleString('de-DE');
  const el = (id) => document.getElementById(id);
  const preisAnzeige = (e) => e.anfrage ? 'auf Anfrage' : e.monat ? `ab ${e.monat} € / Monat` : e.anteil ? `+${Math.round(e.anteil * 100)} %` : `${e.ab ? 'ab ' : ''}${euro(e.preis)} €`;
  // Eine Zeile je Paket; name = Gruppen-ID (Pakete) bzw. „x“ (Zusatz)
  const zeile = (name, e) => {
    const liste = (e.items || []).map((x) => `<li>${x}</li>`).join('');
    let h = `<div class="wahl-zeile" data-id="${e.id}"><div class="wahl-oben"><label class="wahl-check"><input type="checkbox" name="${name}" value="${e.id}"><span class="wahl-name">${e.name.replace(/(Unternehmens|Mitbewerber)(?=\S)/g, '$1&shy;')}</span>${e.gefragt ? '<span class="wahl-gefragt">gefragt</span>' : ''}</label>`;
    if (liste) h += `<button type="button" class="wahl-pfeil" aria-expanded="false" aria-label="Inhalt von ${e.name} anzeigen"><svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 6l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>`;
    h += `<span class="wahl-preis">${preisAnzeige(e)}</span></div>`;
    if (e.wer) h += `<p class="wahl-wer">${e.wer}</p>`;
    // Frage oben, Eingabe darunter; Vorgabe von 3 bis zur enthaltenen Anzahl (Anna 12.10.2026)
    if (e.inkl) h += `<div class="wahl-seiten"><p>Wie viele Unterseiten wird Ihre Website ungefähr haben?</p><p class="wahl-seiten-felder">von <input class="wahl-anzahl" type="number" name="von-${e.id}" min="1" max="80" value="${Math.min(3, e.inkl)}" aria-label="Unterseiten von"> bis <input class="wahl-anzahl" type="number" name="bis-${e.id}" min="1" max="80" value="${e.inkl}" aria-label="Unterseiten bis"> Unterseiten</p></div>`;
    if (e.art === 'anzahl') h += `<label class="wahl-mehr">Anzahl <input class="wahl-anzahl" type="number" name="n-${e.id}" min="1" max="30" value="1"></label>`;
    if (e.wahl) h += `<label class="wahl-mehr">Form <select class="wahl-auswahl" name="w-${e.id}">${e.wahl.map((w) => `<option>${w}</option>`).join('')}</select></label>`;
    h += '<span class="wahl-hinweis"></span>';
    if (liste) h += `<div class="wahl-auf" hidden>${e.plus ? `<p class="wahl-plus">${e.plus}</p>` : ''}<ul>${liste}</ul></div>`;
    return h + '</div>';
  };

  let html = '';
  D.gruppen.forEach((g) => {
    html += `<fieldset class="wahl-gruppe" id="r-${g.id}"><legend>${g.name}${g.wahl === 'mehrere' ? ' <span>mehrere möglich</span>' : ''}</legend>`;
    if (g.hinweis) html += `<p class="wahl-gruppen-hinweis">${g.hinweis}</p>`;
    html += '<div class="wahl-zeilen">' + g.pakete.map((e) => zeile(g.id, e)).join('');
    if (g.extras) {
      html += `<p class="wahl-zwischen">Zusätzlich zur ${g.name} – auch für bestehende Websites</p>`;
      html += `<p class="wahl-pflicht" id="wahl-launch" hidden>✓ Launch ${euro(D.launch)} € – bei jeder neuen Website dabei (Domain, DNS, Umzug, Livegang)</p>`;
      html += g.extras.map((e) => zeile('x', e)).join('');
    }
    html += '</div></fieldset>';
  });
  form.innerHTML = html;

  // Akkordeon: Pfeil neben dem Namen klappt den Inhalt auf
  form.addEventListener('click', (ev) => {
    const b = ev.target.closest('.wahl-pfeil');
    if (!b) return;
    const offen = b.getAttribute('aria-expanded') === 'true';
    b.setAttribute('aria-expanded', String(!offen));
    b.closest('.wahl-zeile').querySelector('.wahl-auf').hidden = offen;
  });
  // Wer Unterseiten einträgt, wählt damit das Website-Paket
  form.addEventListener('input', (ev) => {
    if (!ev.target.closest('.wahl-seiten')) return;
    const cb = ev.target.closest('.wahl-zeile').querySelector('input[type="checkbox"]');
    if (!cb.checked) { cb.checked = true; cb.dispatchEvent(new Event('change', { bubbles: true })); }
  });
  // In Gruppen mit „eins“ nimmt ein neues Häkchen das alte weg
  form.addEventListener('change', (ev) => {
    const g = D.gruppen.find((x) => x.id === ev.target.name);
    if (!g || g.wahl !== 'eins' || !ev.target.checked) return;
    form.querySelectorAll(`input[name="${g.id}"]`).forEach((i) => { if (i !== ev.target) i.checked = false; });
  });

  function auswahl() {
    const posten = [];
    let einmalig = 0, monatlich = 0, webPreis = 0, mitPaket = false;
    D.gruppen.forEach((g) => {
      g.pakete.forEach((e) => {
        if (!form.querySelector(`[data-id="${e.id}"] input`).checked) return;
        if (e.anfrage) { posten.push([e.name, null]); return; }
        let p = e.preis, name = `${g.name}: ${e.name}`;
        if (e.inkl) {
          // Spanne „von – bis“: der Richtwert rechnet mit dem unteren Wert
          const von = Math.max(1, +form.elements[`von-${e.id}`].value || e.inkl);
          const bis = Math.max(von, +form.elements[`bis-${e.id}`].value || von);
          if (von > e.inkl) p += (von - e.inkl) * e.seite;
          name += ` (${von === bis ? von : `${von}–${bis}`} Unterseiten)`;
        }
        posten.push([name, p]); einmalig += p;
        if (e.launch) { mitPaket = true; webPreis = p; }
      });
    });
    el('wahl-launch').hidden = !mitPaket;
    if (mitPaket) { posten.push(['Launch (bei jeder neuen Website)', D.launch]); einmalig += D.launch; }
    D.gruppen.forEach((g) => (g.extras || []).forEach((e) => {
      const z = form.querySelector(`[data-id="${e.id}"]`);
      const cb = z.querySelector('input[type="checkbox"]');
      const gesperrt = Boolean(e.ohnePaket && mitPaket);
      cb.disabled = gesperrt; if (gesperrt) cb.checked = false;
      z.classList.toggle('gesperrt', gesperrt);
      z.querySelector('.wahl-hinweis').textContent = gesperrt ? 'im Website-Paket enthalten' : '';
      if (!cb.checked) return;
      const n = e.art === 'anzahl' ? Math.max(1, +form.elements[`n-${e.id}`].value || 1) : 1;
      const extra = e.wahl ? ` – ${form.elements[`w-${e.id}`].value}` : '';
      const name = `${e.name}${n > 1 ? ` × ${n}` : ''}${extra}`;
      if (e.anfrage) { posten.push([name, null]); return; }
      if (e.monat) { monatlich += e.monat; posten.push([name, e.monat, 'monat']); return; }
      if (e.anteil) { if (!webPreis) { posten.push([name, null]); return; } const p = webPreis * e.anteil * n; posten.push([name, p]); einmalig += p; return; }
      const p = e.preis * n; posten.push([name, p]); einmalig += p;
    }));
    return { posten, einmalig, monatlich };
  }

  const setzen = (w) => { el('summe-einmalig').textContent = euro(w); el('summe-brutto').textContent = euro(w * 1.19); };

  const betrag = ([, p, art]) => p === null ? 'auf Anfrage' : art === 'monat' ? `ab ${euro(p)} € / Monat` : `ab ${euro(p)} €`;
  function aktualisieren() {
    const a = auswahl();
    setzen(a.einmalig);
    el('summe-monat-zeile').hidden = !a.monatlich;
    el('summe-monat').textContent = euro(a.monatlich);
    el('summe-liste').innerHTML = a.posten.length ? a.posten.map((x) => `<li><span>${x[0]}</span><b>${betrag(x).replace('ab ', '')}</b></li>`).join('') : '<li class="gedaempft">Noch nichts ausgewählt.</li>';
    const zeilen = a.posten.map((x) => `– ${x[0]}: ${betrag(x)}`).join('\n');
    const text = `Hallo Anna,\n\nich habe mir mit dem Kostenrechner auf studio-aah.de folgendes zusammengestellt:\n\n${zeilen || '– (noch nichts ausgewählt)'}\n\nRichtwert: ab ${euro(a.einmalig)} € netto einmalig${a.monatlich ? ` zzgl. ab ${euro(a.monatlich)} € / Monat` : ''}\n\nIch würde gern ein kostenloses Erstgespräch vereinbaren.\n\nÜber mich / mein Vorhaben:\n`;
    el('rechner-mail').href = `mailto:info@studio-aah.de?subject=${encodeURIComponent('Kostenvoranschlag über den Rechner')}&body=${encodeURIComponent(text)}`;
    const datum = new Date().toLocaleDateString('de-DE');
    el('druck-bereich').innerHTML = `<p class="druck-marke">STUDIO AAH!</p><h1>Kostenvoranschlag (unverbindlich)</h1><p>Erstellt am ${datum} mit dem Kostenrechner auf studio-aah.de</p>
      <table>${a.posten.map((x) => `<tr><td>${x[0]}</td><td>${betrag(x)}</td></tr>`).join('')}
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
  const leiste = document.querySelector('.preis-leiste');
  const links = leiste ? [...leiste.querySelectorAll('a[href^="#"]')] : [];
  if (!links.length || !('IntersectionObserver' in window)) return;
  const ziele = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const beob = new IntersectionObserver((eintraege) => {
    eintraege.forEach((e) => {
      if (!e.isIntersecting) return;
      links.forEach((a) => a.classList.toggle('aktiv', a.getAttribute('href') === `#${e.target.id}`));
      const aktiv = links.find((a) => a.classList.contains('aktiv'));
      // nur die Leiste waagerecht nachführen – nie die Seite selbst scrollen
      if (aktiv) leiste.scrollTo({ left: aktiv.offsetLeft - 16, behavior: 'smooth' });
    });
  }, { rootMargin: '-35% 0px -60% 0px' });
  ziele.forEach((z) => beob.observe(z));
})();
