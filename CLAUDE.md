# studio-aah.de – Hinweise für Claude Code

## Was dieses Repository ist
- Statische Website von STUDIO AAH! (Anna Härtelt): reines HTML, CSS, wenig JavaScript; kein Baukasten, kein npm. Veröffentlicht wird nur `website/`; jeder Push auf `main` geht sofort live.
- Maßgeblich ist die Spezifikation (lokal `doku/spezifikation.md`, nicht im Repository; Original in Betrieb `Kunden Studio AAH/Studio AAH/Website/`). Bei Widerspruch gilt sie; Widerspruch Anna melden.
- **Das Repository ist öffentlich.** Nichts hinein, was nicht jede:r sehen darf: keine internen Notizen, interne Preise oder Kalkulationen, Kundenhinweise, Kundendaten, Zugangsdaten, `.env`, PDFs (Ausnahme: öffentliche Downloads in `website/downloads/`, aus Skripten erzeugt). Nur Schriften mit freier Lizenz (SIL OFL). Interne Hinweise gehören in den iCloud-Ordner Betrieb.
- Fachregeln stehen in `.claude/rules/` und laden nur, wenn passende Dateien bearbeitet werden: Gestaltung und Texte, Generatoren, Startseite und Menü, Leistungsseiten, Für-wen und Branchen, Blog, Referenzen, Bilder, Spiel.
- In Cloud-Sitzungen gibt es keinen Zugriff auf Betrieb. Was dort eingetragen werden müsste, am Ende als Liste für Anna ausgeben.

## Befehle (vom Repository-Ordner aus)
- `bash werkzeuge/alle-erzeugen.sh` – alle Seiten-Generatoren in der richtigen Reihenfolge; nach jeder Änderung an Daten oder Vorlagen.
- `bash werkzeuge/pruefen.sh` – Kopf und Fuß, Links, Bilder, Aktualität der erzeugten Bereiche (Meldungen zu `website/entwurf-…` ignorieren).
- Vorschau: `.claude/launch.json` → `website`, `http://localhost:8123/`.
- Erzeugte Bereiche nie direkt in `website/` ändern, sondern in der Quelle unter `werkzeuge/`, dann neu erzeugen. Kopf und Fuß nur in `website/index.html`. Gemeinsame Hilfsfunktionen nur in `werkzeuge/gemeinsam.py`.
- Nach CSS- oder JS-Änderungen die Cache-Version `?v=…` überall erhöhen (`sed` über `grep -rl` in `website` und `werkzeuge`), dann alle Generatoren.
- Python 3.9: keine verschachtelten f-Strings mit gleichen Anführungszeichen.

## Arbeitsweise
- Antworten auf Deutsch, in Stichpunkten, Schritt für Schritt; Fachbegriffe mit englischem Begriff in Klammern. Nichts erfinden; Unsicheres als „Unsicher“ kennzeichnen. Neue Texte nur nach Annas Vorgabe.
- Vor jedem Schritt mit Wirkung nach außen fragen: Push auf `main`, Installationen, Änderungen beim Hosting. In Cloud-Sitzungen auf eigenem Zweig arbeiten; Anna führt ihn über GitHub Desktop zusammen.
- Vor jedem Push `git fetch` und `git log origin/main..main`: Mehrere Sitzungen arbeiten auf `main`. Fremde Commits Anna vorher nennen, sonst gehen sie ungefragt live.
- Kleine Commits mit deutscher Beschreibung.
- Nicht öffentlich nennen, wie und wo studio-aah.de gebaut und gehostet ist.
- Vor dem Melden prüfen: Seite im Browser bei Desktop- und Handy-Breite (auch 320 px ohne seitliches Verschieben), Links und Bilder laden, Kopf und Fuß überall gleich.
- Den Stand Anna immer direkt im Chat zeigen: Screenshots oder die Seite als eigenständige HTML-Datei per SendUserFile `display: "render"`, dazu die Adresse. Den Browser-Bereich nur zusätzlich, wenn `get_layout` zeigt, dass die Sitzung in einem Fenster offen ist; nie „ist im Browser offen“ melden, ohne das geprüft zu haben.

## Regeln für den Code
- CSS: `website/css/stil.css` für alle Seiten; Farben, Schriften, Größen, Abstände als Variablen im einen `:root` am Anfang, keine festen Farbwerte im Rest. Projektseiten zusätzlich `website/css/referenzen.css` (nur dort geladen, gleiche Version wie `stil.css`).
- Breakpoints nur 400 / 600 / 768 / 900 / 1024 / 1200 px, geschrieben als `max-width: 767.98px` / `min-width: 768px`, `max-width: 900px` / `min-width: 900.02px`, `max-width: 1024px` / `min-width: 1024.02px`. Einzige Ausnahme: 1100 px für Sitemap und Weg der Projektseiten.
- Schriften lokal aus `website/schriften/` (woff2), nichts von fremden Servern.
- JavaScript: `js/menue.js` für alle Seiten (ein Block, nichts global), `js/referenzen.js` nur auf Projektseiten. JavaScript nur, wo es ohne nicht geht. Ohne JavaScript bleibt alles sichtbar.
- Keine Fremddienste, Cookies, Analyse-Werkzeuge oder JavaScript-Rahmenwerke. Ausnahmen: Formspark (Anfragen), Brevo (Newsletter) und YouTube-Videos in Blogartikeln nur als Zwei-Klick-Lösung über youtube-nocookie.com; alle in der Datenschutzerklärung. Neue Dienste nur nach Annas OK und mit Eintrag dort.
- Nur relative Pfade (Benutzername auf den beiden Macs verschieden).
- Zugänglichkeit: sinnvolle Überschriften-Reihenfolge, Alternativtexte, sichtbarer Fokus, ausreichender Kontrast.

## Gestaltung in einem Satz
Ruhig und plakativ: viel Weiß, Schwarz, Creme, Blau `#2a5fe6` als einziger Akzent; zwei Schriften: Instrument Sans für Überschrift und Text, Annas Handschrift nur als Akzent (Anton nur im Logo); Details in `.claude/rules/gestaltung.md`, Original-Richtlinien in Betrieb `Kunden Studio AAH/Studio AAH/branding-guidelines.md`. E-Mail-Adresse überall info@studio-aah.de; immer „Button“, nie „Knopf“.
