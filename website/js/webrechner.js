// Kostenrechner Webdesign auf der Preisseite: fünf Schritte wie an einer Kasse (Konzept Anna 16.10.2026).
// Marke → Neu oder Redesign (Basispreis) → Seitenstruktur (Sitemap zum Bauen) → Extras → Ihr Bon. Der Kassenbon rechnet mit.
// Rechnet nur im Browser, speichert nichts. Anfrage über den Formulardienst (js/anfrage.js), PDF über den Druckdialog.
// Daten: js/pakete-daten.js (erzeugt aus werkzeuge/preise-daten.json).
(() => {
  const D = window.WEBRECHNER;
  const wurzel = document.getElementById('rechner');
  if (!D || !wurzel) return;
  const $ = (id) => document.getElementById(id);
  const euro = (n) => Math.round(n).toLocaleString('de-DE');
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const X = D.extras;
  const MODULE = Object.fromEntries(Object.entries(X).filter(([, e]) => e.funktion));
  const SCHULUNG = X.schulung.wahl;
  const PFEIL = '<span aria-hidden="true">→</span>';

  /* ---------- Zustand ---------- */
  let uid = 0;
  const neu = (name, typ = 'seite', kinder = []) => ({ id: ++uid, name, typ, kinder });
  const Z = {
    marke: '', bestand: 'neu', texte: 'studio',
    sitemap: D.sitemap.map((s) => neu(s.name, 'seite', s.kinder.map((k) => neu(k)))),
    funk: new Set(), extras: new Set(), sprachen: 0,
    schulung: 'nein', wartung: 'nein', retainer: 'nein', mehrOffen: false,
  };
  const SCHRITTE = [
    { id: 'marke', nm: 'Marke', dt: 'Schritt 1 · Definieren' },
    { id: 'basis', nm: 'Neu oder Redesign', dt: 'Schritt 2 · Verstehen' },
    { id: 'sitemap', nm: 'Seitenstruktur', dt: 'Schritt 3 · Ideen finden' },
    { id: 'extras', nm: 'Extras', dt: 'Schritt 4 · Umsetzung' },
    { id: 'bon', nm: 'Ihr Bon', dt: 'Schritt 5 · Zusammenfassung' },
  ];
  let aktiv = 0, maxErreicht = 0;

  /* ---------- Sitemap ---------- */
  const alle = (liste = Z.sitemap, aus = []) => { liste.forEach((k) => { aus.push(k); alle(k.kinder, aus); }); return aus; };
  function finde(id, liste = Z.sitemap, eltern = null) {
    for (const k of liste) { if (k.id === +id) return { k, liste, eltern }; const r = finde(id, k.kinder, k); if (r) return r; }
    return null;
  }
  const seitenzahl = () => alle().filter((k) => k.typ === 'seite').length;
  const module = () => {
    const m = new Set(alle().filter((k) => k.typ !== 'seite').map((k) => k.typ));
    Z.funk.forEach((t) => m.add(t));
    return Object.keys(MODULE).filter((t) => m.has(t));
  };
  const nimmRaus = (id) => { const r = finde(id); r.liste.splice(r.liste.indexOf(r.k), 1); return r.k; };
  const istNachfahre = (k, id) => k.kinder.some((c) => c.id === +id || istNachfahre(c, id));
  function setzeModul(typ, an) {
    if (!MODULE[typ].bereich) { if (an) Z.funk.add(typ); else Z.funk.delete(typ); return; }
    const da = alle().find((k) => k.typ === typ);
    if (an && !da) Z.sitemap.push(neu(MODULE[typ].name, typ));
    if (!an && da) nimmRaus(da.id);
  }

  /* ---------- Bon ---------- */
  const webpreis = () => D.basis + (Z.bestand === 'redesign' ? D.redesign : 0) + seitenzahl() * D.seite;
  const OFFEN = { offen: true, sub: 'klären wir im Gespräch' };
  function posten() {
    const L = [], add = (phase, o) => L.push({ phase, ...o });
    const m = D.marke.find((x) => x.id === Z.marke);
    if (Z.marke) add('Marke', m.anfrage ? { name: m.name, anfrage: true } : { name: m.name, preis: m.preis, ab: true });
    add('Website', { name: 'Basispreis Website', sub: `Analyse, Look and Feel, ${Z.texte === 'studio' ? 'Texte und Bilder, ' : ''}Startseite, Pflichtseiten, Technik, SEO/GEO, barrierefrei, 2 Feedbackrunden, Launch`, preis: D.basis, ab: true });
    if (Z.bestand === 'redesign') add('Website', { name: 'Redesign', sub: 'Sicherung, Inhalte übernehmen, Weiterleitungen, Search Console', preis: D.redesign });
    const n = seitenzahl();
    if (n) add('Website', { name: `${n} Unterseite${n > 1 ? 'n' : ''}`, sub: `${n} × ${D.seite} €`, preis: n * D.seite, ab: n > D.gross_ab });
    module().forEach((t) => { const e = MODULE[t]; add('Funktionen', e.anfrage ? { name: e.name, anfrage: true } : { name: e.name, sub: e.kurz, preis: e.preis, ab: !!e.ab }); });
    if (Z.sprachen) add('Extras', { name: `${Z.sprachen} weitere Sprache${Z.sprachen > 1 ? 'n' : ''}`, sub: `+30 % auf ${euro(webpreis())} € je Sprache`, preis: webpreis() * X.sprache.anteil * Z.sprachen, ab: true });
    Z.extras.forEach((id) => { const e = X[id]; add('Extras', e.anfrage ? { name: e.name, anfrage: true } : { name: e.name, preis: e.preis }); });
    const s = SCHULUNG.find((w) => w.name === Z.schulung);
    if (s) add('Nach dem Start', { name: `Schulung (${s.name})`, preis: s.preis });
    if (Z.schulung === 'offen') add('Nach dem Start', { name: 'Schulung', ...OFFEN });
    if (Z.wartung === 'ja') add('Nach dem Start', { name: 'Wartung', sub: 'Updates, Sicherheit, kleine Änderungen', monat: X.wartung.monat });
    if (Z.wartung === 'offen') add('Nach dem Start', { name: 'Wartung', ...OFFEN });
    if (Z.retainer === 'ja') add('Nach dem Start', { name: 'Retainer', sub: X['retainer-web'].mindestens, anfrage: true });
    if (Z.retainer === 'offen') add('Nach dem Start', { name: 'Retainer', ...OFFEN });
    return L;
  }
  const betrag = (p) => p.offen ? 'offen' : p.anfrage ? 'auf Anfrage' : p.monat ? `${euro(p.monat)} € / Monat` : `${p.ab ? 'ab ' : ''}${euro(p.preis)} €`;
  function summen(L = posten()) {
    return { einmalig: L.reduce((s, p) => s + (p.preis || 0), 0), monat: L.reduce((s, p) => s + (p.monat || 0), 0), anfrage: L.some((p) => p.anfrage), offen: L.some((p) => p.offen) };
  }
  function bonHTML() {
    const L = posten(), S = summen(L);
    let h = '<p class="wr-bon-titel">Kassenbon</p><p class="wr-bon-klein">Kostenvoranschlag · unverbindlich</p>', phase = '';
    L.forEach((p) => {
      if (p.phase !== phase) { phase = p.phase; h += `<p class="wr-bon-phase">${phase}</p>`; }
      h += `<div class="wr-bon-z${p.offen ? ' wr-offen' : ''}"><span class="wr-bon-n">${esc(p.name)}${p.sub ? `<small>${esc(p.sub)}</small>` : ''}</span><span class="wr-bon-b">${betrag(p)}</span></div>`;
    });
    h += `<div class="wr-bon-linie"></div><div class="wr-bon-summe"><span>Summe</span><span class="wr-bon-b">ab ${euro(S.einmalig)} €</span></div>
      <div class="wr-bon-neben"><span>netto, einmalig</span><span>${euro(S.einmalig * 1.19)} € inkl. 19 % USt.</span></div>
      ${S.monat ? `<div class="wr-bon-neben"><span>zzgl. monatlich</span><span>${euro(S.monat)} € netto</span></div>` : ''}
      ${S.anfrage ? '<div class="wr-bon-neben"><span>+ Posten auf Anfrage</span></div>' : ''}
      ${S.offen ? '<div class="wr-bon-neben"><span>+ offene Punkte – klären wir im Gespräch</span></div>' : ''}
      <p class="wr-bon-fuss">Richtwert aus dem Rechner. Hosting und Domain sind nicht enthalten. Den genauen Preis klären wir im kostenlosen Erstgespräch.</p>`;
    return h;
  }

  /* ---------- Bausteine ---------- */
  const kachel = (name, wert, gewaehlt, titel, unter = '', preis = '', { mehrfach = false, items = null, breit = false } = {}) => `
    <label class="wr-kachel${mehrfach ? ' wr-mehrfach' : ''}${breit ? ' wr-breit' : ''}">
      <input type="${mehrfach ? 'checkbox' : 'radio'}" name="${name}" value="${esc(wert)}"${gewaehlt ? ' checked' : ''}>
      <span class="wr-k-t">${titel}</span>${unter ? `<span class="wr-k-u">${unter}</span>` : ''}${preis ? `<span class="wr-k-p">${preis}</span>` : ''}
      ${items && items.length ? `<details><summary>Was ist drin?</summary><ul>${items.map((i) => `<li>${esc(i)}</li>`).join('')}</ul></details>` : ''}
    </label>`;
  // Eine Zeile je Leistung mit Auswahl Ja · Nein · Weiß ich noch nicht (Anna 16.10.2026)
  const zeile = (name, titel, frage, text, wahl, items) => `
    <fieldset class="wr-zeile"><legend><b>${titel}</b><span>${frage}</span></legend>
      ${text ? `<p class="wr-zeile-text">${text}</p>` : ''}
      ${items ? `<details class="wr-zeile-mehr"><summary>Was ist drin?</summary><ul>${items.map((i) => `<li>${esc(i)}</li>`).join('')}</ul></details>` : ''}
      <div class="wr-segmente">${wahl.map(([w, t]) => `<label><input type="radio" name="${name}" value="${esc(w)}"${Z[name] === w ? ' checked' : ''}><span>${t}</span></label>`).join('')}</div>
    </fieldset>`;
  const preisText = (e) => e.anfrage ? 'auf Anfrage' : `${e.ab ? 'ab ' : ''}${euro(e.preis)} €`;

  /* ---------- Schritte ---------- */
  const R = {
    marke() {
      return `<h3 class="wr-h">Gibt es schon eine Marke?</h3><p class="wr-warum">Eine Website wirkt nur so klar wie die Marke dahinter. Wenn Logo und Erscheinungsbild schon da sind und passen, bauen wir darauf auf.</p>
      <div class="wr-kacheln wr-drei">${D.marke.map((m) => kachel('marke', m.id, Z.marke === m.id, m.titel, m.wer, m.anfrage ? 'auf Anfrage' : m.preis ? `ab ${euro(m.preis)} €` : '0 €', { items: m.items, breit: m.breit })).join('')}</div>`;
    },
    basis() {
      const re = Z.bestand === 'redesign';
      const gruppen = D.basis_inhalt.map((g) => {
        const items = g.items.map((i) => i === 'TEXTE' ? D.texte[Z.texte] : i).concat(re ? (D.redesign_inhalt[g.titel] || []) : []);
        return `<div><h4>${g.titel}</h4><ul>${items.map((i) => `<li>${esc(i)}</li>`).join('')}</ul></div>`;
      }).join('');
      return `<h3 class="wr-h">Neue Website oder Redesign?</h3><p class="wr-warum">Der Basispreis enthält alles, was jede Website braucht, damit sie gut wird. Das lässt sich nicht abwählen.</p>
      <div class="wr-kacheln">${kachel('bestand', 'neu', !re, 'Neue Website', 'Es gibt noch keine Website.', `ab ${euro(D.basis)} €`)}${kachel('bestand', 'redesign', re, 'Redesign', 'Die bestehende Website wird neu – Inhalte übernehmen, alte Adressen weiterleiten.', `+ ${euro(D.redesign)} €`)}</div>
      <p class="wr-frage">Wer liefert Texte und Bilder?<small>Beides ist im Basispreis.</small></p>
      <div class="wr-kacheln">${kachel('texte', 'studio', Z.texte === 'studio', 'Ich liefere Texte und Bilder', 'Mit KI erstellt auf Basis der Analyse, von mir geprüft und überarbeitet. Sie können sich Ihrem Tagesgeschäft widmen.')}${kachel('texte', 'selbst', Z.texte === 'selbst', 'Sie liefern Texte und Bilder', 'Schicken Sie mir Ihre Texte und Bilder, wie es Ihnen passt – zum Beispiel als Dokument. Ich übernehme sie in die Website.')}</div>
      <div class="wr-basis"><h4 class="wr-basis-titel">Im Basispreis enthalten <span>ab ${euro(D.basis)} €${re ? ` + ${euro(D.redesign)} € Redesign` : ''}</span></h4>
        ${gruppen}
        <div class="wr-nicht"><h4>Nicht enthalten</h4><ul>${D.nicht_enthalten.map((i) => `<li>${esc(i)}</li>`).join('')}</ul></div>
      </div>`;
    },
    sitemap() {
      const n = seitenzahl(), mod = new Set(module()), namen = new Set(alle().map((k) => k.name.trim().toLowerCase()));
      const karte = (k) => `<div class="wr-karte${k.typ !== 'seite' ? ' wr-modul' : ''}" data-id="${k.id}">${k.typ !== 'seite' ? '<span class="wr-typ">Funktion</span>' : ''}<span class="wr-griff" aria-hidden="true">⠿</span><input value="${esc(k.name)}" data-name="${k.id}" aria-label="Seitenname ${esc(k.name)}, mit Alt und Pfeiltasten verschieben"><button type="button" class="wr-x" data-weg="${k.id}" aria-label="${esc(k.name)} entfernen">×</button></div>`;
      const fchip = ([t, e]) => `<button type="button" class="wr-chip wr-chip-modul" data-modul="${t}"${mod.has(t) ? ' disabled' : ''}>+ ${esc(e.name)}</button>`;
      const funkAktiv = [...Z.funk].filter((t) => MODULE[t]);
      const weitere = Object.entries(MODULE).filter(([, e]) => !e.oft);
      const text = n > D.gross_ab ? `Mehr als ${D.gross_ab} Unterseiten – das ist ein großes Projekt. Den Preis klären wir am besten im Gespräch.`
        : n === 0 ? 'Nur die Startseite – alles steht auf einer Seite (Onepager). Es gilt der Basispreis.'
          : `Unterseiten × ${D.seite} € = <b>${euro(n * D.seite)} €</b>. Je Unterseite mit Texten und Bildern. Startseite, Impressum und Datenschutz sind im Basispreis. Typisch: Selbstständige 1–6, Unternehmen 8–25.`;
      return `<h3 class="wr-h">Welche Seiten braucht Ihre Website?</h3><p class="wr-warum">Hier sehen Sie den Aufbau einer typischen kleinen Unternehmenswebsite. Entfernen Sie mit ×, was Sie nicht brauchen, fügen Sie mit + Unterseiten hinzu und ziehen Sie Seiten an eine andere Stelle. Seitennamen können Sie direkt überschreiben.</p>
      <div class="wr-sitemap"><div class="wr-baum">
        <div class="wr-start"><div class="wr-karte wr-fest" data-ziel="start">Startseite<span class="wr-schloss">im Basispreis</span></div></div>
        <div class="wr-ebene">${Z.sitemap.map((k) => `<div class="wr-spalte">${karte(k)}${k.kinder.length ? `<div class="wr-kinder">${k.kinder.map(karte).join('')}</div>` : ''}${k.typ === 'seite' ? `<button type="button" class="wr-plus" data-kind="${k.id}" data-ziel="kind" aria-label="Unterseite zu ${esc(k.name)} hinzufügen">+</button>` : ''}</div>`).join('')}
          <div class="wr-spalte${Z.sitemap.length ? ' wr-leer' : ''}"><button type="button" class="wr-neu" data-neu data-ziel="ende" aria-label="Seite hinzufügen" title="Seite hinzufügen">+</button></div></div>
        ${funkAktiv.length ? `<div class="wr-funk-reihe"><span>Funktionen auf Ihrer Website:</span>${funkAktiv.map((t) => `<span class="wr-funk-chip">${esc(MODULE[t].name)}<button type="button" data-funk-weg="${t}" aria-label="${esc(MODULE[t].name)} entfernen">×</button></span>`).join('')}</div>` : ''}
        <div class="wr-pflicht"><span>Immer dabei, im Basispreis:</span><span class="wr-k">Impressum</span><span class="wr-k">Datenschutz</span></div>
      </div></div>
      <p class="wr-tipp">Tastatur: Seitennamen auswählen, dann Alt + ← → zum Umsortieren, Alt + ↓ macht die Seite zur Unterseite der Seite davor, Alt + ↑ holt sie eine Ebene hoch.</p>
      <div class="wr-palette">
        <div><h4>Seiten hinzufügen</h4><div class="wr-vorschlaege">${D.vorschlaege.map((v) => `<button type="button" class="wr-chip" data-vorschlag="${esc(v)}"${namen.has(v.toLowerCase()) ? ' disabled' : ''}>+ ${esc(v)}</button>`).join('')}</div></div>
        <div><h4>Funktionen hinzufügen</h4><div class="wr-vorschlaege">${Object.entries(MODULE).filter(([, e]) => e.oft).map(fchip).join('')}</div>
          <details class="wr-mehr-funk"${Z.mehrOffen ? ' open' : ''}><summary>Weitere Funktionen (${weitere.length})</summary><div class="wr-vorschlaege">${weitere.map(fchip).join('')}</div></details>
          <p class="wr-tipp">Preise siehe Kassenbon. Ohne Preis: auf Anfrage.</p></div>
      </div>
      <div class="wr-zaehler" aria-live="polite">${n ? `<span class="wr-zahl">${n}</span>` : ''}<span class="wr-zahl-text">${text}</span></div>`;
    },
    extras() {
      const mod = module(), w = X.wartung, r = X['retainer-web'];
      const nein = ['nein', 'Nein'], offen = ['offen', 'Weiß ich noch nicht'];
      return `<h3 class="wr-h">Was soll Ihre Website noch können?</h3><p class="wr-warum">Ihre Funktionen aus der Seitenstruktur sind schon ausgewählt. Hier können Sie Extras dazunehmen.</p>
      <p class="wr-frage">Ihre Funktionen<small>Aus Ihrer Seitenstruktur. Haken entfernen nimmt die Funktion auch dort heraus.</small></p>
      ${mod.length ? `<div class="wr-kacheln">${mod.map((t) => kachel('modul', t, true, esc(MODULE[t].name), esc(MODULE[t].kurz), preisText(MODULE[t]), { mehrfach: true })).join('')}</div>` : '<p class="wr-tipp">Noch keine Funktion gewählt.</p>'}
      <p class="wr-mit-abstand"><button type="button" class="button button-zweit" data-geh-zu="2">Funktionen hinzufügen ${PFEIL}</button></p>
      <p class="wr-frage">Extras</p>
      <div class="wr-kacheln">${D.extras_schritt4.map((id) => kachel('extra', id, Z.extras.has(id), esc(X[id].name), esc(X[id].kurz), X[id].anfrage ? 'auf Anfrage' : `${euro(X[id].preis)} €`, { mehrfach: true })).join('')}</div>
      <p class="wr-frage">In wie vielen weiteren Sprachen?<small>+30 % auf den Website-Preis (Basis und Unterseiten) je Sprache. Die Übersetzung liefern Sie.</small></p>
      <div class="wr-stepper"><button type="button" data-sprache="-1" aria-label="eine Sprache weniger">−</button><output aria-live="polite">${Z.sprachen}</output><button type="button" data-sprache="1" aria-label="eine Sprache mehr">+</button></div>
      <div class="wr-hinweis"><b>Cookie-Banner und Tracking</b><br>Ob Sie das brauchen, hängt von Ihrer Website ab. Ich berate Sie dazu, die Kosten stehen dann im Angebot.</div>
      <p class="wr-frage wr-frage-gross">Nach dem Start</p>
      ${zeile('schulung', 'Schulung', 'Möchten Sie Inhalte selbst pflegen?', esc(X.schulung.kurz), [...SCHULUNG.map((s) => [s.name, `Ja, ${s.name === 'PDF-Anleitung' ? 'als PDF' : 'online'} · ${euro(s.preis)} €`]), nein, offen])}
      ${zeile('wartung', 'Wartung', 'Soll sich jemand um Technik und Sicherheit kümmern?', esc(w.wer), [['ja', `Ja · ${euro(w.monat)} € / Monat`], nein, offen], w.items)}
      ${zeile('retainer', 'Retainer', 'Soll die Website nach dem Start weiterentwickelt werden?', `${esc(r.rechner)} Laufende Betreuung über ${esc(r.mindestens)}.`, [['ja', 'Ja · auf Anfrage'], nein, offen])}`;
    },
    bon() {
      const re = Z.bestand === 'redesign', a = angaben();
      return `<h3 class="wr-h">Ihr Kostenvoranschlag</h3><p class="wr-warum">Das ist ein erster Richtwert. Den genauen Preis klären wir gemeinsam im kostenlosen Erstgespräch.</p>
      <ol class="wr-ablauf"><li><span class="wr-ablauf-k">01</span><span><b>Kostenvoranschlag</b> – unverbindlich, aus diesem Rechner</span></li><li><span class="wr-ablauf-k">02</span><span><b>Erstgespräch</b> – kostenlos: Wo stehen Sie, was wollen Sie, wen wollen Sie erreichen?</span></li><li><span class="wr-ablauf-k">03</span><span><b>Angebot</b> – auf dieser Grundlage</span></li><li><span class="wr-ablauf-k">04</span><span><b>Vertrag</b> – und los geht’s</span></li></ol>
      <form class="wr-uebergabe anfrage-form" id="wr-anfrage" action="${window.Anfrage.ENDPUNKT}" method="post">
        <h4 class="wr-box-titel">Das geht mit Ihrer Anfrage an STUDIO AAH!</h4>
        <ul class="wr-uebersicht">${a.map(([t, v]) => `<li><span>${t}</span><span>${esc(v)}</span></li>`).join('')}</ul>
        ${felder('wr')}
        <p class="anfrage-knoepfe"><button type="submit" class="button">Projekt anfragen ${PFEIL}</button><button type="button" class="button button-zweit" data-pdf>Als PDF speichern <span aria-hidden="true">↓</span></button></p>
        <p class="hinweis-klein">Alle Angaben aus dem Rechner gehen mit Ihrer Anfrage an mich und sind die Grundlage für unser Erstgespräch. Unverbindlich und kostenlos. <span class="anfrage-hinweis">${window.Anfrage.HINWEIS}</span></p>
        <div class="anfrage-danach" role="status" hidden></div>
      </form>
      ${re ? `<div class="wr-review"><p class="meta">Für bestehende Websites</p><h4 class="wr-box-titel">Kostenloses Website-Review</h4>
        <p>30 Minuten online: Ich schaue mir Ihre Website mit dem Blick Ihrer Kundschaft und Ihrer Bewerberinnen und Bewerber an und nenne Ihnen konkrete Ansatzpunkte. Kostenlos und unverbindlich.</p>
        <p>Ihre Angaben aus dem Rechner schicken Sie mir vorab – Sie müssen nichts herunterladen. Dafür oben Name und E-Mail eintragen. <a href="../website-review/">Mehr zum Website-Review <span aria-hidden="true">→</span></a></p>
        <ol class="wr-review-schritte"><li>Angaben senden.</li><li>Termin buchen in Google Kalender.</li></ol>
        <p><button type="button" class="button button-zweit" data-review>Angaben senden ${PFEIL}</button></p>
        <div id="wr-review-termin" role="status" hidden><p><b>Danke, Ihre Angaben sind bei mir angekommen.</b> Jetzt noch den Termin wählen:</p>
          <p><a class="button button-zweit" href="${esc(D.review)}" target="_blank" rel="noopener">Jetzt Termin buchen <span aria-hidden="true">↗</span></a></p></div>
        <p class="hinweis-klein">Die Terminbuchung läuft über Google Kalender. Dort gelten die Datenschutzhinweise von Google.</p></div>` : ''}`;
    },
  };
  const felder = (p) => `<div class="anfrage-felder">
      <label for="${p}-name">Name<input id="${p}-name" name="name" autocomplete="name" required value="${esc(F.name)}"></label>
      <label for="${p}-email">E-Mail<input id="${p}-email" name="email" type="email" autocomplete="email" required value="${esc(F.email)}"></label>
      <label for="${p}-website" class="anfrage-ganz">Ihre Website (falls vorhanden)<input id="${p}-website" name="website" type="text" inputmode="url" autocomplete="url" placeholder="www.ihre-website.de" value="${esc(F.website)}"></label>
      <label for="${p}-nachricht" class="anfrage-ganz">Nachricht (freiwillig)<textarea id="${p}-nachricht" name="nachricht" rows="3">${esc(F.nachricht)}</textarea></label>
    </div>
    <p class="anfrage-falle" aria-hidden="true"><label>Bitte leer lassen<input name="_honeypot" tabindex="-1" autocomplete="off"></label></p>`;
  // Formularfelder überleben das Neuzeichnen
  const F = { name: '', email: '', website: '', nachricht: '' };

  /* ---------- Angaben für Anfrage und PDF ---------- */
  const baumText = (liste, tiefe = 0) => liste.map((k) => `${'  '.repeat(tiefe)}– ${k.name}${k.typ !== 'seite' ? ' (Funktion)' : ''}\n${baumText(k.kinder, tiefe + 1)}`).join('');
  function angaben() {
    const m = D.marke.find((x) => x.id === Z.marke), n = seitenzahl();
    const struktur = Z.sitemap.filter((k) => k.typ === 'seite').map((k) => k.name + (k.kinder.length ? ` (${k.kinder.length})` : '')).join(', ');
    const s = SCHULUNG.find((w) => w.name === Z.schulung);
    const wahl = (v, ja) => v === 'ja' ? ja : v === 'offen' ? 'offen – klären wir im Gespräch' : 'nein';
    const extras = [...[...Z.extras].map((id) => X[id].name), Z.sprachen ? `${Z.sprachen} weitere Sprache${Z.sprachen > 1 ? 'n' : ''}` : ''].filter(Boolean);
    return [
      ['Marke', m && m.name ? m.name : 'Logo und Erscheinungsbild passen'],
      ['Neu oder Redesign', Z.bestand === 'redesign' ? 'Redesign' : 'Neue Website'],
      ['Texte und Bilder', Z.texte === 'studio' ? 'liefert STUDIO AAH!' : 'liefere ich selbst'],
      ['Seitenstruktur', n ? `${n} Unterseite${n > 1 ? 'n' : ''}: ${struktur}` : 'Onepager'],
      ['Funktionen', module().map((t) => MODULE[t].name).join(', ') || '–'],
      ['Extras', extras.join(', ') || '–'],
      ['Schulung', s ? s.name : Z.schulung === 'offen' ? 'offen – klären wir im Gespräch' : 'nein'],
      ['Wartung', wahl(Z.wartung, 'ja')],
      ['Retainer', wahl(Z.retainer, 'ja')],
      ['Kostenvoranschlag', kurzSumme()],
    ];
  }
  function kurzSumme() {
    const S = summen();
    return `ab ${euro(S.einmalig)} € netto${S.monat ? `, zzgl. ${euro(S.monat)} € / Monat` : ''}${S.anfrage ? ', + Posten auf Anfrage' : ''}`;
  }
  function mailAngaben() {
    const L = posten(), S = summen(L);
    return 'Meine Angaben aus dem Kostenrechner:\n'
      + angaben().filter(([t]) => t !== 'Kostenvoranschlag').map(([t, v]) => `${t}: ${v}`).join('\n')
      + `\n\nSeitenstruktur:\n– Startseite\n${baumText(Z.sitemap)}– Impressum, Datenschutz`
      + '\n\nKostenvoranschlag (Richtwert, netto):\n' + L.map((p) => `– ${p.name}: ${betrag(p)}`).join('\n')
      + `\nSumme: ab ${euro(S.einmalig)} € netto (${euro(S.einmalig * 1.19)} € inkl. 19 % USt.)${S.monat ? `\nzzgl. monatlich: ${euro(S.monat)} € netto` : ''}${S.anfrage ? '\n+ Posten auf Anfrage' : ''}`;
  }

  /* ---------- PDF (Druckdialog) ---------- */
  function drucken() {
    const L = posten(), S = summen(L), datum = new Date().toLocaleDateString('de-DE');
    $('druck-bereich').innerHTML = `<p class="druck-marke">STUDIO AAH!</p><h1>Kostenvoranschlag Website (unverbindlich)</h1><p>Erstellt am ${datum} mit dem Kostenrechner auf studio-aah.de</p>
      <table>${L.map((p) => `<tr><td>${esc(p.name)}${p.sub ? `<br><small>${esc(p.sub)}</small>` : ''}</td><td>${betrag(p)}</td></tr>`).join('')}
      <tr class="druck-summe"><td>Richtwert einmalig (netto)</td><td>ab ${euro(S.einmalig)} €</td></tr><tr><td>inkl. 19 % USt.</td><td>ab ${euro(S.einmalig * 1.19)} €</td></tr>${S.monat ? `<tr><td>monatlich (netto)</td><td>${euro(S.monat)} €</td></tr>` : ''}</table>
      <h2>Ihre Angaben</h2><table>${angaben().filter(([t]) => t !== 'Kostenvoranschlag').map(([t, v]) => `<tr><td>${t}</td><td>${esc(v)}</td></tr>`).join('')}</table>
      <h2>Seitenstruktur</h2><pre>– Startseite\n${esc(baumText(Z.sitemap))}– Impressum, Datenschutz</pre>
      <p><b>So geht es weiter:</b> 1. Kostenvoranschlag · 2. kostenloses Erstgespräch · 3. Angebot · 4. Vertrag</p>
      <p>Richtwert aus dem Rechner. Hosting und Domain sind nicht enthalten. Den genauen Preis klären wir im kostenlosen Erstgespräch. Kontakt: info@studio-aah.de · studio-aah.de</p>`;
    document.body.classList.add('druck-rechner');
    window.print();
  }
  window.addEventListener('afterprint', () => document.body.classList.remove('druck-rechner'));

  /* ---------- Zeichnen ---------- */
  // Fokus nach dem Neuzeichnen an dieselbe Stelle zurück (Tastatur, Bildschirmleser)
  function fokusMerken() {
    const a = document.activeElement;
    if (!a || !wurzel.contains(a)) return null;
    if (a.id) return `#${a.id}`;
    if (a.name && a.value !== undefined && a.type === 'radio') return `[name="${a.name}"][value="${CSS.escape(a.value)}"]`;
    if (a.name && a.type === 'checkbox') return `[name="${a.name}"][value="${CSS.escape(a.value)}"]`;
    for (const k of ['name', 'kind', 'modul', 'vorschlag', 'sprache', 'gehZu', 'funkWeg']) if (a.dataset[k]) return `[data-${k.replace(/[A-Z]/g, (c) => '-' + c.toLowerCase())}="${CSS.escape(a.dataset[k])}"]`;
    return null;
  }
  function bonZeichnen() {
    $('wr-bon').innerHTML = bonHTML();
    const S = summen();
    $('wr-bon-summe').innerHTML = `<small>Summe netto</small>ab ${euro(S.einmalig)} €`;
    $('wr-ansage').textContent = `Summe: ab ${euro(S.einmalig)} Euro netto`;
  }
  function zeichne(schrittWechsel = false) {
    const fokus = schrittWechsel ? null : fokusMerken();
    maxErreicht = Math.max(maxErreicht, aktiv);
    const s = SCHRITTE[aktiv];
    $('wr-leiste').innerHTML = SCHRITTE.map((x, j) => `<li class="${j < aktiv ? 'fertig' : j === aktiv ? 'aktiv' : j > maxErreicht ? 'zu' : ''}"><button type="button" data-geh="${j}"${j > maxErreicht ? ' disabled' : ''}${j === aktiv ? ' aria-current="step"' : ''}><span class="wr-nr">${String(j + 1).padStart(2, '0')}</span><span class="wr-nm">${x.nm}</span></button></li>`).join('');
    $('wr-leiste-mobil').innerHTML = `<div class="wr-lm-oben"><span>Schritt ${aktiv + 1} von ${SCHRITTE.length}</span><span>${s.nm}</span></div><div class="wr-lm-balken"><i style="width:${(aktiv + 1) / SCHRITTE.length * 100}%"></i></div>`;
    const el = $('wr-schritt');
    el.innerHTML = `<p class="meta wr-dach">${s.dt}</p>` + R[s.id]();
    $('wr-zurueck').hidden = aktiv === 0;
    $('wr-kein-kauf').hidden = aktiv !== 0;
    const w = $('wr-weiter');
    w.hidden = aktiv === SCHRITTE.length - 1;
    if (!w.hidden) w.innerHTML = `Weiter: ${SCHRITTE[aktiv + 1].nm} ${PFEIL}`;
    bonZeichnen();
    if (fokus) { const f = el.querySelector(fokus) || wurzel.querySelector(fokus); if (f) f.focus({ preventScroll: true }); }
    if (schrittWechsel) {
      el.focus({ preventScroll: true });
      const oben = wurzel.getBoundingClientRect().top;
      if (oben < 0) wurzel.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    }
  }
  const geh = (j) => { aktiv = Math.max(0, Math.min(SCHRITTE.length - 1, j)); zeichne(true); };
  $('wr-weiter').addEventListener('click', () => geh(aktiv + 1));
  $('wr-zurueck').addEventListener('click', () => geh(aktiv - 1));
  $('wr-leiste').addEventListener('click', (e) => { const b = e.target.closest('[data-geh]'); if (b && !b.disabled) geh(+b.dataset.geh); });
  $('wr-bon-auf').addEventListener('click', (e) => {
    const o = $('wr-bon').classList.toggle('offen');
    e.currentTarget.setAttribute('aria-expanded', String(o));
    e.currentTarget.innerHTML = o ? 'Bon schließen <span aria-hidden="true">↓</span>' : 'Bon ansehen <span aria-hidden="true">↑</span>';
  });
  // Handy: Bon-Leiste nur zeigen, solange der Rechner im Bild ist
  if ('IntersectionObserver' in window) new IntersectionObserver(([e]) => wurzel.classList.toggle('wr-im-bild', e.isIntersecting)).observe(wurzel);
  else wurzel.classList.add('wr-im-bild');

  const schritt = $('wr-schritt');
  schritt.addEventListener('change', (e) => {
    const t = e.target, v = t.value;
    switch (t.name) {
      case 'marke': Z.marke = v; break;
      case 'bestand': Z.bestand = v; break;
      case 'texte': Z.texte = v; break;
      case 'modul': setzeModul(v, t.checked); break;
      case 'extra': if (t.checked) Z.extras.add(v); else Z.extras.delete(v); break;
      case 'schulung': case 'wartung': case 'retainer': Z[t.name] = v; break;
      default: return;
    }
    zeichne();
  });
  schritt.addEventListener('input', (e) => {
    const id = e.target.dataset.name;
    if (id) { finde(id).k.name = e.target.value; bonZeichnen(); return; }
    if (e.target.form && e.target.form.id === 'wr-anfrage' && e.target.name in F) F[e.target.name] = e.target.value;
  });
  // Nach dem Umbenennen neu zeichnen (Vorschläge, Bon), aber erst, wenn der Fokus die Sitemap verlässt
  schritt.addEventListener('focusout', (e) => {
    if (e.target.dataset.name && !(e.relatedTarget && e.relatedTarget.closest && e.relatedTarget.closest('.wr-sitemap'))) zeichne();
  });
  const fokusName = (id) => { const i = schritt.querySelector(`[data-name="${id}"]`); if (i) { i.focus(); i.select(); } };
  const anfrageForm = () => $('wr-anfrage');
  schritt.addEventListener('submit', (e) => {
    if (e.target.id !== 'wr-anfrage') return;
    e.preventDefault();
    window.Anfrage.senden(e.target, { betreff: 'Projektanfrage über den Kostenrechner', einleitung: 'ich habe mir mit dem Kostenrechner auf studio-aah.de einen Kostenvoranschlag für meine Website zusammengestellt und frage unverbindlich an.', angaben: mailAngaben() });
  });
  let gezogen = false;
  schritt.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b || gezogen) return;
    if (b.dataset.weg) { nimmRaus(b.dataset.weg); zeichne(); const n = schritt.querySelector('[data-neu]'); if (n) n.focus(); }
    else if (b.dataset.kind) { const { k } = finde(b.dataset.kind); const c = neu(`Unterseite ${k.kinder.length + 1}`); k.kinder.push(c); zeichne(); fokusName(c.id); }
    else if (b.hasAttribute('data-neu')) { const c = neu('Neue Seite'); Z.sitemap.push(c); zeichne(); fokusName(c.id); }
    else if (b.dataset.vorschlag) { Z.sitemap.push(neu(b.dataset.vorschlag)); zeichne(); }
    else if (b.dataset.modul) { Z.mehrOffen = Boolean(b.closest('.wr-mehr-funk')); setzeModul(b.dataset.modul, true); zeichne(); }
    else if (b.dataset.funkWeg) { Z.funk.delete(b.dataset.funkWeg); zeichne(); }
    else if (b.dataset.gehZu) geh(+b.dataset.gehZu);
    else if (b.dataset.sprache) { Z.sprachen = Math.max(0, Math.min(5, Z.sprachen + +b.dataset.sprache)); zeichne(); }
    else if (b.hasAttribute('data-pdf')) drucken();
    else if (b.hasAttribute('data-review')) {
      // Website-Review in zwei Schritten (Anna 16.10.2026): erst Angaben per E-Mail, dann der Termin-Link
      const f = anfrageForm();
      if (!f.reportValidity()) return;
      window.Anfrage.senden(f, { betreff: 'Website-Review (Angaben aus dem Kostenrechner)', einleitung: 'ich möchte ein kostenloses Website-Review buchen. Vorab meine Angaben aus dem Kostenrechner.', angaben: mailAngaben(), meldung: 'Ihr E-Mail-Programm öffnet sich mit Ihren Angaben für das Website-Review.',
        fertig: () => { $('wr-review-termin').hidden = false; $('wr-review-termin').querySelector('a').focus(); } });
    }
  });
  // Tastatur: Alt + Pfeiltasten verschiebt die Seite
  schritt.addEventListener('keydown', (e) => {
    const id = e.target.dataset.name;
    if (!id) return;
    if (e.key === 'Enter') { e.preventDefault(); e.target.blur(); return; }
    if (!e.altKey || !e.key.startsWith('Arrow')) return;
    e.preventDefault();
    const { k, liste, eltern } = finde(id), i = liste.indexOf(k);
    if (e.key === 'ArrowLeft' && i > 0) { liste.splice(i, 1); liste.splice(i - 1, 0, k); }
    if (e.key === 'ArrowRight' && i < liste.length - 1) { liste.splice(i, 1); liste.splice(i + 1, 0, k); }
    if (e.key === 'ArrowDown' && !eltern && i > 0 && liste[i - 1].typ === 'seite' && k.typ === 'seite') { liste.splice(i, 1); liste[i - 1].kinder.push(k, ...k.kinder); k.kinder = []; }
    if (e.key === 'ArrowUp' && eltern) { liste.splice(i, 1); Z.sitemap.splice(Z.sitemap.indexOf(eltern) + 1, 0, k); }
    zeichne(); fokusName(id);
  });

  /* ---------- Ziehen und Ablegen (Maus, Stift und Finger) ---------- */
  let zug = null;
  schritt.addEventListener('pointerdown', (e) => {
    const karte = e.target.closest('.wr-karte[data-id]');
    if (!karte || e.button) return;
    if (e.target.closest('button') || (e.target.matches('input') && e.pointerType === 'mouse' && document.activeElement === e.target)) return;
    zug = { id: karte.dataset.id, x: e.clientX, y: e.clientY, karte, aktiv: false, ziel: null };
  });
  window.addEventListener('pointermove', (e) => {
    if (!zug) return;
    if (!zug.aktiv) {
      if (Math.hypot(e.clientX - zug.x, e.clientY - zug.y) < 6) return;
      zug.aktiv = true; zug.karte.classList.add('wr-zieht');
      zug.geist = Object.assign(document.createElement('div'), { className: 'wr-geist', textContent: finde(zug.id).k.name });
      document.body.append(zug.geist);
      if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    }
    e.preventDefault();
    zug.geist.style.left = `${e.clientX}px`; zug.geist.style.top = `${e.clientY}px`;
    schritt.querySelectorAll('.wr-ziel-vor,.wr-ziel').forEach((x) => x.classList.remove('wr-ziel-vor', 'wr-ziel'));
    const unter = document.elementFromPoint(e.clientX, e.clientY);
    const k = unter && unter.closest('.wr-karte[data-id], [data-ziel]');
    zug.ziel = null;
    if (!k || !schritt.contains(k)) return;
    const gezogeneKarte = finde(zug.id).k;
    if (k.dataset.id) { if (k.dataset.id !== zug.id && !istNachfahre(gezogeneKarte, k.dataset.id)) { k.classList.add('wr-ziel-vor'); zug.ziel = { art: 'vor', id: k.dataset.id }; } }
    else if (k.dataset.ziel === 'kind') { if (k.dataset.kind !== zug.id && gezogeneKarte.typ === 'seite' && !istNachfahre(gezogeneKarte, k.dataset.kind)) { k.classList.add('wr-ziel'); zug.ziel = { art: 'kind', id: k.dataset.kind }; } }
    else { (k.dataset.ziel === 'ende' ? k : schritt.querySelector('[data-neu]')).classList.add('wr-ziel'); zug.ziel = { art: 'ende' }; }
  }, { passive: false });
  window.addEventListener('pointerup', () => {
    if (!zug) return;
    const z = zug; zug = null;
    if (!z.aktiv) return;
    z.geist.remove(); gezogen = true; setTimeout(() => { gezogen = false; }, 0);
    if (!z.ziel) { zeichne(); return; }
    const k = nimmRaus(z.id);
    if (z.ziel.art === 'ende') Z.sitemap.push(k);
    else if (z.ziel.art === 'kind') { const p = finde(z.ziel.id).k; p.kinder.push(k, ...k.kinder); k.kinder = []; }
    else { const r = finde(z.ziel.id); r.liste.splice(r.liste.indexOf(r.k), 0, k); if (r.eltern) { r.liste.splice(r.liste.indexOf(k) + 1, 0, ...k.kinder); k.kinder = []; } }
    zeichne();
  });
  window.addEventListener('pointercancel', () => { if (zug && zug.geist) zug.geist.remove(); zug = null; zeichne(); });

  wurzel.classList.add('wr-bereit');
  zeichne();
})();
