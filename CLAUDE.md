# studio-aah.de – Hinweise für Claude Code

## Was dieses Repository ist
- Die statische Website von Studio AAH (Anna). Reines HTML und CSS – kein Baukasten, kein Bau-Schritt, kein npm.
- Maßgeblich ist die Spezifikation (von Anna freigegeben am 03.10.2026): lokal `doku/spezifikation.md` (nicht im Repository), Original im iCloud-Ordner `Betrieb` unter `Kunden Studio AAH/Studio AAH/Website/`. Bei Widerspruch gilt die Spezifikation; Widerspruch Anna melden.
- Veröffentlicht wird nur der Ordner `website/` (GitHub Pages, Workflow `.github/workflows/github-pages.yml`). Alles andere (Werkzeuge) bleibt draußen.
- Das Repository ist öffentlich: nur Dateien hinein, die jeder sehen darf. Nur Schriften mit freier Lizenz (SIL OFL), keine internen Notizen, Preise oder Kundendaten.

## Vorlage
- Der Stand, der nachgebaut wird, liegt im Nachbarordner `../studio-aah-website` (Export aus WordPress/Kadence): `seiten/*.html`, `blog/*.html`, `css/zusatz.css`, `design/customizer.json`, `navigation/menues.json`.
- Der Blockcode dort ist Vorlage für Inhalt und Aufbau, kein Code zum Übernehmen: Kadence-Klassen und Block-Kommentare gehören nicht in die neue Website.
- Texte werden unverändert übernommen. Keine neuen Texte erfinden, nichts kürzen oder umformulieren.

## Arbeitsweise
- Antworten auf Deutsch, in Stichpunkten, Schritt für Schritt; Fachbegriffe mit dem englischen Begriff in Klammern.
- Nichts erfinden; Unsicheres als „Unsicher“ kennzeichnen.
- Reihenfolge und Stopps aus der Spezifikation einhalten: nach der fertigen Startseite stoppen und Anna das Ergebnis zeigen.
- Vor jedem Schritt mit Wirkung nach außen fragen: Hochladen (Push) – jeder Push geht sofort live –, Installationen, Änderungen bei IONOS.
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
- Die Bilder liegen in der Mediathek der lokalen Sandbox (Programm „Local“, Site `kadence-sandbox`), nicht im Repository. Den genauen Ordner mit Anna klären, bevor Bilder kopiert werden.
- Für das Web verkleinern; Ziel: ganzer Ordner `website/` unter 50 MB.
