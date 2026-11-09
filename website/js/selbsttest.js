/* Selbsttest „Wo hakt es?“ und KI-Zeitrechner (Anna 10.11.2026). Alles wird im Browser gerechnet, nichts gesendet oder gespeichert. */
(function () {
  'use strict';
  var test = document.querySelector('[data-selbsttest]');
  if (test) {
    var box = document.querySelector('[data-ergebnis-box]');
    test.addEventListener('submit', function (e) {
      e.preventDefault();
      var punkte = {}, offen = 0;
      test.querySelectorAll('.st-frage').forEach(function (f) {
        var w = f.querySelector('input:checked');
        f.classList.toggle('st-fehlt', !w);
        if (!w) { offen++; return; }
        punkte[f.dataset.ziel] = (punkte[f.dataset.ziel] || 0) + Number(w.value);
      });
      var hinweis = test.querySelector('[data-hinweis]');
      if (offen) { hinweis.textContent = offen === 1 ? 'Bitte beantworten Sie noch eine Aussage.' : 'Bitte beantworten Sie noch ' + offen + ' Aussagen.'; var erste = test.querySelector('.st-fehlt input'); if (erste) erste.focus(); return; }
      hinweis.textContent = '';
      var liste = box.querySelector('.st-liste');
      var eintraege = Array.prototype.slice.call(liste.children);
      eintraege.sort(function (a, b) { return (punkte[b.dataset.ergebnis] || 0) - (punkte[a.dataset.ergebnis] || 0); });
      eintraege.forEach(function (li, i) {
        var p = punkte[li.dataset.ergebnis] || 0;
        li.style.setProperty('--wert', (p / 4 * 100) + '%');
        li.classList.toggle('st-oben', i === 0 && p > 0);
        liste.appendChild(li);
      });
      var hoechst = punkte[eintraege[0].dataset.ergebnis] || 0;
      var gleich = eintraege.filter(function (li) { return (punkte[li.dataset.ergebnis] || 0) === hoechst; });
      eintraege.forEach(function (li) { li.classList.toggle('st-oben', hoechst > 0 && gleich.indexOf(li) >= 0); });
      box.querySelector('[data-ergebnis-titel]').textContent = hoechst === 0
        ? 'Glückwunsch: Bei Ihnen hakt es kaum.'
        : gleich.length > 1 ? 'Mehrere Themen sind gleich stark. Fangen Sie oben an.'
        : 'Hier hakt es am meisten: ' + eintraege[0].querySelector('.st-titel').textContent;
      box.hidden = false; box.focus();
      document.dispatchEvent(new Event('konfetti'));
    });
  }

  var rechner = document.querySelector('[data-ki-rechner]');
  if (rechner) {
    var zahl = new Intl.NumberFormat('de-DE');
    var rechne = function () {
      var klemme = function (v, a, b) { return Math.min(b, Math.max(a, v)); };
      var personen = klemme(Number(rechner.personen.value) || 0, 0, 500);
      var stunden = Number(rechner.stunden.value) || 0;
      var anteil = Number((rechner.querySelector('[name="anteil"]:checked') || {}).value || 0.25);
      var satz = klemme(Number(rechner.satz.value) || 0, 0, 300);
      var monat = personen * stunden * anteil * 4.3;
      rechner.stunden_aus.value = stunden + (stunden === 1 ? ' Stunde' : ' Stunden');
      rechner.stunden.setAttribute('aria-valuetext', rechner.stunden_aus.value);
      document.querySelector('[data-kr-stunden]').textContent = zahl.format(Math.round(monat));
      document.querySelector('[data-kr-euro]').textContent = zahl.format(Math.round(monat * 12 * satz / 10) * 10);
    };
    rechner.addEventListener('input', rechne);
    rechner.addEventListener('submit', function (e) { e.preventDefault(); });
    rechne();
  }
})();
