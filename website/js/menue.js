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
