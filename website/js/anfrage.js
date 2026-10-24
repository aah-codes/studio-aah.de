// Anfrageformular (Projekt anfragen und Kostenrechner): schickt die Felder an den Formulardienst Formspark (Anna 16.10.2026),
// der sie per E-Mail an info@studio-aah.de weiterleitet; danach geht es auf die Danke-Seite. Kein fremdes Skript, keine Cookies.
// Klappt das Senden nicht, steht die Nachricht zum Kopieren bereit.
// Die Formulare liegen auf Seiten eine Ebene tief (kontakt/, preise/), daher die Pfade mit ../
window.Anfrage = (() => {
  const ENDPUNKT = 'https://submit-form.com/PQ3YFrvCS'; // Formspark-Adresse (auch im HTML von kontakt/ und demokratie-braucht-sichtbarkeit/ als Ersatz ohne JavaScript)
  const ADRESSE = 'info@studio-aah.de';
  const wert = (form, n) => (form.elements[n] ? form.elements[n].value.trim() : '');

  function text(form, { einleitung = '', angaben = '' } = {}) {
    const nachricht = wert(form, 'nachricht');
    const kontakt = [wert(form, 'name') ? `Name: ${wert(form, 'name')}` : '', `E-Mail: ${wert(form, 'email')}`].filter(Boolean);
    if (wert(form, 'organisation')) kontakt.push(`Organisation: ${wert(form, 'organisation')}`);
    if (wert(form, 'website')) kontakt.push(`Website: ${wert(form, 'website')}`);
    form.querySelectorAll('input[type="checkbox"][name]').forEach((h) => kontakt.push(`${(h.closest('label')?.textContent || h.name).trim()} ${h.checked ? 'ja' : 'nein'}`));
    return ['Hallo Anna,', einleitung, angaben, nachricht ? `Nachricht:\n${nachricht}` : '', kontakt.join('\n')].filter(Boolean).join('\n\n') + '\n';
  }

  const box = (form) => form.querySelector('.anfrage-danach');
  function kopierKnopf(b, t) {
    const knopf = b.querySelector('.anfrage-kopieren'), status = b.querySelector('.anfrage-kopiert');
    if (!knopf) return;
    if (!navigator.clipboard) { knopf.replaceWith('Nachricht markieren und kopieren'); return; }
    knopf.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(`An: ${ADRESSE}\n\n${t}`); status.textContent = 'Kopiert'; }
      catch { status.textContent = 'Kopieren ging nicht – bitte die Adresse oben nutzen.'; }
    });
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
    const knopf = form.querySelector('button[type="submit"]');
    const alt = knopf ? knopf.innerHTML : '';
    if (knopf) { knopf.disabled = true; knopf.textContent = 'Wird gesendet …'; }
    const daten = { betreff: opt.betreff || 'Projektanfrage', name: wert(form, 'name'), email: wert(form, 'email'), website: wert(form, 'website'), nachricht: wert(form, 'nachricht'), _honeypot: wert(form, '_honeypot') };
    if (opt.angaben) daten.kostenrechner = opt.angaben;
    if (form.elements.organisation) daten.organisation = wert(form, 'organisation');
    // Häkchen (z. B. Schnell-Check auf website-check/): immer mitschicken, angehakt oder nicht
    form.querySelectorAll('input[type="checkbox"][name]').forEach((h) => { daten[h.name] = h.checked ? 'ja' : 'nein'; });
    // Betreff und Absendername der Benachrichtigung (Formspark-Felder _email.subject und _email.from; im Namen kein @, < oder >)
    daten['_email.subject'] = `${daten.betreff}: ${daten.name || daten.website}`;
    daten['_email.from'] = daten.name.replace(/[@<>]/g, '') || 'Website studio-aah.de';
    try {
      const antwort = await fetch(ENDPUNKT, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(daten) });
      if (!antwort.ok) throw new Error(String(antwort.status));
      if (knopf) { knopf.disabled = false; knopf.innerHTML = alt; }
      if (opt.fertig) { opt.fertig(); return; }
      window.location.href = opt.weiter || '../danke/';
    } catch {
      if (knopf) { knopf.disabled = false; knopf.innerHTML = alt; }
      fehler(form, t);
    }
  }

  // Hinweis unter dem Formular zum Versandweg (Datenschutz)
  const HINWEIS = 'Ihre Angaben gehen über den Formulardienst Formspark (Belgien, Speicherung in der EU) per E-Mail an mich. Mehr in der <a href="../datenschutz/#kontakt">Datenschutzerklärung</a>.';

  // Projekt anfragen: Formulare mit data-anfrage (= Betreff, data-weiter = eigene Danke-Seite) selbst verbinden; Pflichtfelder prüft der Browser vor dem Absenden
  document.querySelectorAll('form[data-anfrage]').forEach((form) => form.addEventListener('submit', (e) => {
    e.preventDefault();
    senden(form, { betreff: form.dataset.anfrage, weiter: form.dataset.weiter });
  }));

  return { senden, ENDPUNKT, HINWEIS };
})();
