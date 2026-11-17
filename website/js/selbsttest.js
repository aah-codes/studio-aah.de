/* Selbsttest „Wo hakt es?“ und KI-Zeitrechner (Anna 10.11.2026, Rechner neu 17.11.2026: Zeit auf Menschenarbeit verteilen). Alles wird im Browser gerechnet, nichts gesendet oder gespeichert. */
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
      var monat = personen * stunden * anteil * 4.3;
      rechner.stunden_aus.value = stunden + ' Std.';
      rechner.stunden.setAttribute('aria-valuetext', stunden + (stunden === 1 ? ' Stunde' : ' Stunden'));
      var gesamt = Math.round(monat);
      document.querySelector('[data-kr-stunden]').textContent = zahl.format(gesamt);
      // Frei gewordene Zeit nach Gewichtung auf Menschenarbeit verteilen (Anna 17.11.2026)
      var regler = Array.prototype.slice.call(rechner.querySelectorAll('[name^="b_"]'));
      var summe = regler.reduce(function (s, r) { return s + Number(r.value); }, 0);
      // Ganze Zahlen so runden, dass die Teile zusammen das Ganze ergeben (größter Rest zuerst)
      var verteile = function (ganz) {
        var t = regler.map(function (r, i) { var roh = summe ? ganz * Number(r.value) / summe : 0; return { i: i, n: Math.floor(roh), rest: roh - Math.floor(roh) }; });
        var fehlt = summe ? ganz - t.reduce(function (s, x) { return s + x.n; }, 0) : 0;
        t.slice().sort(function (a, b) { return b.rest - a.rest || a.i - b.i; }).slice(0, fehlt).forEach(function (x) { x.n++; });
        return t.map(function (x) { return x.n; });
      };
      var std = verteile(gesamt), prozent = verteile(100), lernStd = null;
      regler.forEach(function (r, i) {
        var id = r.name.slice(2);
        rechner.querySelector('[data-kr-aus="' + id + '"]').value = prozent[i] + ' %';
        r.setAttribute('aria-valuetext', prozent[i] + ' Prozent der frei gewordenen Zeit');
        document.querySelector('[data-kr-std="' + id + '"]').textContent = zahl.format(std[i]) + ' Std.';
        document.querySelector('[data-kr-balken="' + id + '"]').style.flexGrow = summe ? Number(r.value) / summe : 0;
        if (id === 'lernen') lernStd = std[i];
      });
      var warnung = document.querySelector('[data-kr-warnung]');
      if (!warnung.dataset.text) warnung.dataset.text = warnung.textContent;
      warnung.textContent = summe ? warnung.dataset.text : 'Verteilen Sie die Zeit auf mindestens einen Bereich.';
      warnung.hidden = !(gesamt > 0 && (!summe || lernStd === 0));
    };
    rechner.addEventListener('input', rechne);
    rechner.addEventListener('submit', function (e) { e.preventDefault(); });
    rechne();
  }
})();
