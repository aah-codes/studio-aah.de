# studio-aah.de – Hinweise für Claude Code

## Was dieses Repository ist
- Die statische Website von Studio AAH (Anna). Reines HTML und CSS – kein Baukasten, kein Bau-Schritt, kein npm.
- Maßgeblich ist die Spezifikation (von Anna freigegeben am 03.10.2026): lokal `doku/spezifikation.md` (nicht im Repository), Original im iCloud-Ordner `Betrieb` unter `Kunden Studio AAH/Studio AAH/Website/`. Bei Widerspruch gilt die Spezifikation; Widerspruch Anna melden.
- Veröffentlicht wird nur der Ordner `website/` (GitHub Pages, Workflow `.github/workflows/github-pages.yml`). Alles andere (Werkzeuge) bleibt draußen.
- Das Repository ist öffentlich: nur Dateien hinein, die jeder sehen darf. Nur Schriften mit freier Lizenz (SIL OFL), keine internen Notizen, Preise oder Kundendaten.

## Stand (12.10.2026)
- Die Website ist umgesetzt und live. Die WordPress-Vorlage im Nachbarordner ist nur noch Archiv. Texte ändert Anna laufend; neue Texte nur nach ihrer Vorgabe, nichts dazuerfinden.
- In Cloud-Sitzungen gibt es keinen Zugriff auf den iCloud-Ordner `Betrieb` (Projektstatus, Branding-Richtlinien). Die wichtigsten Regeln stehen deshalb unten. Was in `Betrieb` eingetragen werden müsste, am Ende als Liste für Anna ausgeben.

## Generatoren (immer nach Änderungen an Daten oder Vorlagen, vom Repository-Ordner aus)
- `python3 werkzeuge/preise-erzeugen.py` – Preise, Kostenrechner-Daten, Leiste, Glossar
- `python3 werkzeuge/leistungsseiten.py` – alle Seiten unter `website/service/` aus `werkzeuge/leistungen-inhalte.json` und `werkzeuge/preise-daten.json`; Prozess, Kopf und Fuß kommen aus `website/index.html`
- `python3 werkzeuge/inhalte-erzeugen.py` – Referenzen, „Für wen“, Stimmen, Blog-Vorschau, Kennzahlen (Marker `<!-- NAME:START -->` … `<!-- NAME:ENDE -->`)
- `python3 werkzeuge/grafiken/ci-film.py` – CI-Grafik (`werkzeuge/grafiken/corporate-identity.html`)
- Erzeugte Bereiche nie direkt in `website/` ändern, sondern in der Quelle, dann neu erzeugen.
- Nach CSS- oder JS-Änderungen die Cache-Version `?v=…` überall erhöhen (z. B. `sed` über `grep -rl` in `website` und `werkzeuge`), dann alle Generatoren laufen lassen.
- Prüfen mit `bash werkzeuge/pruefen.sh` (Meldungen zu `website/entwurf-hero` ignorieren).
- Python 3.9: keine verschachtelten f-Strings mit gleichen Anführungszeichen.

## Gestaltungsregeln (Kurzfassung der Branding-Richtlinien)
- Farben: Schwarz `#0e1011`, Weiß, Creme `#eeece7` (Flächen, Plakatgrund), Blau `#2f6bff` als einziger Akzent, Grau `#d6d8d9` / `#9a9d9e`. Kein Rot, Gelb, Grün.
- Kein Blau auf Schwarz (Kontrast). Kein blaues Herz, Herzen generell vermeiden.
- Buttons: Primär blau gefüllt (`--farbe-primaer` `#2a5fe6`), Sekundär schwarze Outline (`button button-zweit`), Tertiär unterstrichener Textlink. Jeder Button und jeder eigenständige Link hat einen Pfeil (→, extern ↗, Download ↓).
- Dachzeilen über Überschriften beginnen mit blauem Punkt (per CSS automatisch).
- Leitsatz: „Form follows function“ immer mit kurzer Erklärung („Die Form folgt der Funktion.“).
- Icons aus gefüllten Bauhaus-Grundformen (Kreis, Halbkreis, Quadrat, Dreieck, Balken), jedes mit Schwarz. Clay-Icons (`website/bilder/icons/`) bleiben.
- Bewegung, die von selbst startet, hält nach höchstens 5 s an oder hat eine Pause-Taste.
- Kartenreihen: Unterzeilen, Listen und Buttons auf einer Linie; H1 nie breiter als die Seite.
- Website-Screenshots kommen aus der Bildbibliothek `website/bilder/referenzen/` (1440 px breit).

## Arbeitsweise
- Antworten auf Deutsch, in Stichpunkten, Schritt für Schritt; Fachbegriffe mit dem englischen Begriff in Klammern.
- Nichts erfinden; Unsicheres als „Unsicher“ kennzeichnen.
- Vor jedem Schritt mit Wirkung nach außen fragen: Hochladen (Push) auf `main` – jeder Push auf `main` geht sofort live –, Installationen, Änderungen bei IONOS. In Cloud-Sitzungen auf einem eigenen Zweig arbeiten; Anna führt ihn über GitHub Desktop zusammen.
- Kleine Commits mit deutscher Beschreibung.
- Vor dem Melden prüfen: Seite im Browser ansehen (Desktop und Handy-Breite), Links und Bilder laden, Kopf und Fuß auf allen Seiten gleich.

## Regeln für den Code
- Eine CSS-Datei `website/css/stil.css`; Farben, Schriften und Abstände als CSS-Variablen am Anfang.
- Schriften lokal aus `website/schriften/` (woff2), nichts von fremden Servern laden.
- Keine Fremddienste, keine Cookies, kein Analyse-Werkzeug, kein JavaScript-Rahmenwerk. JavaScript nur, wo es ohne nicht geht (z. B. Mobilmenü), und dann wenige Zeilen.
- Nur relative Pfade – der Benutzername ist auf den beiden Macs verschieden.
- Zugänglichkeit: sinnvolle Überschriften-Reihenfolge, Alternativtexte, sichtbarer Fokus, ausreichender Kontrast.
- Nie ins Repository: Zugangsdaten, `.env`, Kundendaten, PDFs (siehe `.gitignore`).

## Bilder
- Bilder liegen in `website/bilder/`. Für das Web verkleinern; Ziel: ganzer Ordner `website/` klein halten.
