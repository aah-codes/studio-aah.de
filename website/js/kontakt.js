// Kopier-Symbol neben der E-Mail-Adresse: hilft, wenn beim Klick auf den E-Mail-Link kein Mailprogramm aufgeht.
// Ohne JavaScript bleibt das Symbol versteckt; die Adresse steht trotzdem sichtbar da.
(() => {
  const knopf = document.querySelector('[data-kopieren]');
  const status = document.querySelector('.kopiert');
  if (!knopf || !navigator.clipboard) return;
  knopf.hidden = false;
  knopf.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(knopf.dataset.kopieren);
      knopf.classList.add('ok');
      if (status) status.textContent = 'Kopiert';
      setTimeout(() => { knopf.classList.remove('ok'); if (status) status.textContent = ''; }, 2500);
    } catch (e) {
      if (status) status.textContent = 'Bitte Adresse markieren';
    }
  });
})();
