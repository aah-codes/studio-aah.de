// Anfrageformular (Kontaktseite und Kostenrechner): baut aus den Feldern eine fertige E-Mail an info@studio-aah.de
// und öffnet das E-Mail-Programm. Die Website selbst speichert und sendet nichts (Anna 16.10.2026: Versand über das E-Mail-Programm).
// Ohne JavaScript schickt das Formular die Felder per mailto-Formular (action) – schlichter, aber es geht.
window.Anfrage = (() => {
  const ADRESSE = 'info@studio-aah.de';
  const wert = (form, n) => (form.elements[n] ? form.elements[n].value.trim() : '');

  function text(form, { einleitung = '', angaben = '' } = {}) {
    const nachricht = wert(form, 'nachricht');
    const kontakt = [`Name: ${wert(form, 'name')}`, `E-Mail: ${wert(form, 'email')}`];
    if (wert(form, 'website')) kontakt.push(`Website: ${wert(form, 'website')}`);
    return ['Hallo Anna,', einleitung, angaben, nachricht ? `Nachricht:\n${nachricht}` : '', kontakt.join('\n')].filter(Boolean).join('\n\n') + '\n';
  }

  // Hinweis nach dem Klick: Die E-Mail muss im E-Mail-Programm noch abgeschickt werden; Text zum Kopieren, falls sich nichts öffnet
  function danach(form, t, meldung) {
    const box = form.querySelector('.anfrage-danach');
    if (!box) return;
    box.innerHTML = `<p><b>${meldung || 'Ihr E-Mail-Programm öffnet sich mit der fertigen Nachricht.'}</b> Bitte senden Sie sie dort ab – erst dann kommt Ihre Anfrage bei mir an.</p>`
      + `<p>Öffnet sich nichts? <button type="button" class="anfrage-kopieren">Nachricht kopieren</button> und an ${ADRESSE} schicken. <span class="anfrage-kopiert" aria-live="polite"></span></p>`;
    box.hidden = false;
    const knopf = box.querySelector('.anfrage-kopieren'), status = box.querySelector('.anfrage-kopiert');
    if (!navigator.clipboard) { knopf.replaceWith('Nachricht unten markieren'); return; }
    knopf.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(`An: ${ADRESSE}\n\n${t}`); status.textContent = 'Kopiert'; }
      catch (e) { status.textContent = 'Kopieren ging nicht – bitte die Adresse oben nutzen.'; }
    });
  }

  function senden(form, opt = {}) {
    const t = text(form, opt);
    window.location.href = `mailto:${ADRESSE}?subject=${encodeURIComponent(opt.betreff || 'Projektanfrage')}&body=${encodeURIComponent(t)}`;
    danach(form, t, opt.meldung);
    return t;
  }

  // Kontaktseite: Formulare mit data-anfrage (= Betreff) selbst verbinden; Pflichtfelder prüft der Browser vor dem Absenden
  document.querySelectorAll('form[data-anfrage]').forEach((form) => form.addEventListener('submit', (e) => {
    e.preventDefault();
    senden(form, { betreff: form.dataset.anfrage });
  }));

  return { senden, text, danach };
})();
