# Schema für Blogbeiträge (verbindlich)

Stand: 19.10.2026 · Anna: „Jeder Artikel muss ab jetzt nach einem gleichen Schema aufgebaut sein“ – Vorbild ist Teil 1 der Reihe „Website-Fragen“ (`/blog/was-kostet-eine-website/`). Ziel: gut für Leser:innen **und** für KI-Suche (GEO) und KI-Agenten.
Die Schreibregeln (Ton, Antwort zuerst, Belege, Wortwahl) stehen im Skill `texte-studio-aah`; hier steht, wie ein Beitrag auf der Website gebaut wird.

## Bauen
- Jeder Beitrag = `werkzeuge/blog/<slug>-inhalt.html` (Inhalt) + `werkzeuge/blog/<slug>.py` (Daten, FAQ), der nur `bauen(...)` aus `werkzeuge/blog/beitrag.py` aufruft. Kopf, Fuß, Metadaten, Lesezeit und strukturierte Daten (JSON-LD) entstehen dort für alle gleich. Keinen eigenen Seitenrahmen schreiben.
- Neuer Beitrag: Eintrag in `werkzeuge/inhalte/blog.json` (oben), Zeile in `werkzeuge/alle-erzeugen.sh` (vor `inhalte-erzeugen.py`), Eintrag in `website/sitemap.xml`, Titel- und Vorschaubild (1200 × 800 WebP, 1200 × 630 JPG). Dann `bash werkzeuge/alle-erzeugen.sh` und `bash werkzeuge/pruefen.sh`.
- `bauen()` bricht ab, wenn ein Pflichtteil fehlt.

## Aufbau (Reihenfolge)
1. Brotkrumen (Blog / Kategorie), bei Reihen Dachzeile „Reihe „…“ · Teil n: …“
2. `h1` – die Frage, die der Beitrag beantwortet
3. Lead (`artikel-lead`): ein bis zwei Sätze, worum es geht
4. Meta-Zeile: Autorin, Datum, Lesezeit, „Stand“ für Zahlen oder Preise
5. Titelbild mit beschreibendem Alternativtext
6. **„Kurz gesagt“** (`section.kurz`, Pflicht): 4–5 Punkte, **die Antwort zuerst**, mit den wichtigsten Zahlen samt Quelle in Klammern. Jeder Punkt ist ohne den Rest lesbar. Wird als `abstract` in die strukturierten Daten übernommen.
7. Inhaltsverzeichnis (`nav.inhalt-verzeichnis`, Pflicht) mit Sprungmarken
8. Hauptteil: `h2` je Kapitel, `h3`/`h4` darunter, **jede Zwischenüberschrift mit `id`** (Agenten und Links zeigen direkt auf Abschnitte). Keine Sprünge in der Überschriften-Reihenfolge. Tabellen mit `caption` oder `aria-label`, am Handy ohne seitliches Scrollen lesbar. Grafiken aus vorhandenen Bausteinen.
9. Fazit (wenn der Text eins hat)
10. **„Häufige Fragen“** (`h2#faq`, Pflicht): 6–10 Fragen in `bauen(faq=...)`. Fragen so, wie Menschen sie in eine Suche oder einen KI-Chat tippen. Antworten 2–4 Sätze, eigenständig verständlich, der erste Satz beantwortet die Frage direkt, keine Links. Mindestens eine Brückenfrage zum Angebot von STUDIO AAH!. Nur belegte Aussagen (aus dem Artikel, aus Teil 1 oder neu belegt). Wird als `FAQPage` ausgegeben.
11. **„Ihr nächster Schritt“** (`section.artikel-schluss`, Pflicht): Frage als Überschrift, 1–2 Sätze, Knöpfe „Projekt anfragen →“ (bzw. „Erstgespräch vereinbaren →“) und „Zum Kostenrechner →“
12. Reihen-Kasten (`aside.reihe`) bei Reihen, aktueller Teil mit `aria-current="page"`
13. Über die Autorin (`section.autorin`, Pflicht)
14. **Quellen** (`h2#quellen` + `ul.quellen`, Pflicht bei Zahlen): je Quelle Herausgeber, verlinkter Titel mit ↗, Datum. Erreichbarkeit vor dem Hochladen prüfen (Weiterleitungen auf allgemeine Seiten zählen als kaputt). Die Links werden als `citation` übernommen.
15. Beitragsnavigation (Zurück / Weiter); beim vorigen Beitrag „Weiter“ ergänzen.

## Strukturierte Daten (macht `bauen()`)
`BlogPosting` (headline, description, abstract, image, datePublished, dateModified, wordCount, keywords, about, mentions, citation, author mit Profil, publisher, isPartOf Blog und ggf. `CreativeWorkSeries` mit `position`), `FAQPage`, `BreadcrumbList`, `ProfessionalService`. Dazu `article:published_time` und `article:modified_time`. Ändert sich ein veröffentlichter Beitrag, `geaendert` und `lastmod` in der Sitemap auf das Datum setzen.

## Prüfliste vor dem Hochladen
- Text gegen die freigegebene Fassung gelegt (Prüfer-Agent), neue Teile (Kurz gesagt, FAQ, Abschluss) Anna als neu gemeldet
- 320 und 390 px ohne seitliches Verschieben, Überschriften-Reihenfolge, Alternativtexte
- alle Quellen erreichbar, interne Links stimmen, `pruefen.sh` ohne Meldung
- Was der Artikel fordert (Handy, Barrierefreiheit, klare Handlungsaufforderung), erfüllt die eigene Seite
