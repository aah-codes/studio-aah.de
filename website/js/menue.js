// Mega-Menü „Service“: öffnet per Klick, schließt mit Esc oder Klick daneben.
// Ohne JavaScript führt „Service“ einfach auf /service/.
(() => {
  const schalter = document.querySelector('.mm-toggle');
  const menue = document.getElementById('mm');
  const schleier = document.querySelector('.mm-schleier');
  if (!schalter || !menue || !schleier) return;

  function oeffnen() {
    menue.hidden = false;
    schleier.hidden = false;
    requestAnimationFrame(() => { menue.classList.add('offen'); schleier.classList.add('offen'); });
    schalter.setAttribute('aria-expanded', 'true');
    const erster = menue.querySelector('a');
    if (erster) erster.focus({ preventScroll: true });
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
    schalter.getAttribute('aria-expanded') === 'true' ? schliessen(false) : oeffnen();
  });
  schleier.addEventListener('click', () => schliessen(false));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') schliessen(true); });
  menue.addEventListener('focusout', (e) => {
    if (!menue.contains(e.relatedTarget) && e.relatedTarget !== schalter) schliessen(false);
  });
})();
