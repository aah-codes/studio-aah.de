// Anfrageformular (Projekt anfragen und Kostenrechner): schickt die Felder an den Formulardienst Formspark (Anna 16.10.2026),
// der sie per E-Mail an info@studio-aah.de weiterleitet; danach geht es auf die Danke-Seite. Kein fremdes Skript, keine Cookies.
// Solange ENDPUNKT leer ist, baut das Formular wie bisher eine fertige E-Mail im E-Mail-Programm (mailto).
// Die Formulare liegen auf Seiten eine Ebene tief (kontakt/, preise/), daher die Pfade mit ../
window.Anfrage = (() => {
  const ENDPUNKT = 'https://submit-form.com/PQ3YFrvCS'; // Formspark-Adresse des Formulars, z. B. 'https://submit-form.com/AbC123xy'
  const ADRESSE = 'info@studio-aah.de';
  const wert = (form, n) => (form.elements[n] ? form.elements[n].value.trim() : '');

  function text(form, { einleitung = '', angaben = '' } = {}) {
    const nachricht = wert(form, 'nachricht');
    const kontakt = [`Name: ${wert(form, 'name')}`, `E-Mail: ${wert(form, 'email')}`];
    if (wert(form, 'website')) kontakt.push(`Website: ${wert(form, 'website')}`);
    return ['Hallo Anna,', einleitung, angaben, nachricht ? `Nachricht:\n${nachricht}` : '', kontakt.join('\n')].filter(Boolean).join('\n\n') + '\n';
  }

  const box = (form) => form.querySelector('.anfrage-danach');
  function kopierKnopf(b, t) {
    const knopf = b.querySelector('.anfrage-kopieren'), status = b.querySelector('.anfrage-kopiert');
    if (!knopf) return;
    if (!navigator.clipboard) { knopf.replaceWith('Nachricht markieren und kopieren'); return; }
    knopf.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(`An: ${ADRESSE}\n\n${t}`); status.textContent = 'Kopiert'; }
      catch (e) { status.textContent = 'Kopieren ging nicht – bitte die Adresse oben nutzen.'; }
    });
  }
  // Nur ohne Formulardienst: Die E-Mail muss im E-Mail-Programm noch abgeschickt werden; Text zum Kopieren, falls sich nichts öffnet
  function danach(form, t, meldung) {
    const b = box(form);
    if (!b) return;
    b.innerHTML = `<p><b>${meldung || 'Ihr E-Mail-Programm öffnet sich mit der fertigen Nachricht.'}</b> Bitte senden Sie sie dort ab – erst dann kommt Ihre Anfrage bei mir an.</p>`
      + `<p>Öffnet sich nichts? <button type="button" class="anfrage-kopieren">Nachricht kopieren</button> und an ${ADRESSE} schicken. <span class="anfrage-kopiert" aria-live="polite"></span></p>`;
    b.hidden = false;
    kopierKnopf(b, t);
  }
  function fehler(form, t) {
    const b = box(form);
    if (!b) return;
    b.innerHTML = '<p><b>Das Senden hat leider nicht geklappt.</b> Bitte versuchen Sie es gleich noch einmal – oder schreiben Sie mir direkt an '
      + `<a href="mailto:${ADRESSE}">${ADRESSE}</a>.</p><p><button type="button" class="anfrage-kopieren">Nachricht kopieren</button> <span class="anfrage-kopiert" aria-live="polite"></span></p>`;
    b.hidden = false;
    kopierKnopf(b, t);
  }

  // opt: betreff, einleitung, angaben (Kostenrechner), weiter (Danke-Seite) oder fertig (Rückruf statt Danke-Seite, z. B. Website-Review)
  async function senden(form, opt = {}) {
    const t = text(form, opt);
    if (!ENDPUNKT) {
      window.location.href = `mailto:${ADRESSE}?subject=${encodeURIComponent(opt.betreff || 'Projektanfrage')}&body=${encodeURIComponent(t)}`;
      danach(form, t, opt.meldung);
      if (opt.fertig) opt.fertig();
      return;
    }
    const knopf = form.querySelector('button[type="submit"]');
    const alt = knopf ? knopf.innerHTML : '';
    if (knopf) { knopf.disabled = true; knopf.textContent = 'Wird gesendet …'; }
    const daten = { betreff: opt.betreff || 'Projektanfrage', name: wert(form, 'name'), email: wert(form, 'email'), website: wert(form, 'website'), nachricht: wert(form, 'nachricht'), _honeypot: wert(form, '_honeypot') };
    if (opt.angaben) daten.kostenrechner = opt.angaben;
    try {
      const antwort = await fetch(ENDPUNKT, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(daten) });
      if (!antwort.ok) throw new Error(String(antwort.status));
      if (knopf) { knopf.disabled = false; knopf.innerHTML = alt; }
      if (opt.fertig) { opt.fertig(); return; }
      window.location.href = opt.weiter || '../danke/';
    } catch (e) {
      if (knopf) { knopf.disabled = false; knopf.innerHTML = alt; }
      fehler(form, t);
    }
  }

  // Hinweis unter dem Formular passend zum Versandweg
  const HINWEIS = 'Ihre Angaben gehen über den Formulardienst Formspark (Belgien, Speicherung in der EU) per E-Mail an mich. Mehr in der <a href="../datenschutz/#kontakt">Datenschutzerklärung</a>.';
  const hinweise = (wurzel = document) => { if (ENDPUNKT) wurzel.querySelectorAll('.anfrage-hinweis').forEach((p) => { p.innerHTML = HINWEIS; }); };
  hinweise();

  // Projekt anfragen: Formulare mit data-anfrage (= Betreff) selbst verbinden; Pflichtfelder prüft der Browser vor dem Absenden
  document.querySelectorAll('form[data-anfrage]').forEach((form) => form.addEventListener('submit', (e) => {
    e.preventDefault();
    senden(form, { betreff: form.dataset.anfrage });
  }));

  return { senden, text, danach, hinweise, mitDienst: Boolean(ENDPUNKT) };
})();
