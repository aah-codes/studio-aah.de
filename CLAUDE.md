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
- `python3 werkzeuge/blog/was-kostet-eine-website.py` – Blogbeitrag „Was kostet eine Website“ aus `werkzeuge/blog/was-kostet-eine-website-inhalt.html` (Inhalt) und Kopf/Fuß des KI-Artikels; Texte nur in der Inhaltsdatei ändern
- `python3 werkzeuge/grafiken/ci-film.py` – CI-Grafik (`werkzeuge/grafiken/corporate-identity.html`)
- Erzeugte Bereiche nie direkt in `website/` ändern, sondern in der Quelle, dann neu erzeugen.
- Nach CSS- oder JS-Änderungen die Cache-Version `?v=…` überall erhöhen (z. B. `sed` über `grep -rl` in `website` und `werkzeuge`), dann alle Generatoren laufen lassen.
- Prüfen mit `bash werkzeuge/pruefen.sh` (Meldungen zu Entwurfsseiten `website/entwurf-…` ignorieren, falls es welche gibt; sie haben bewusst keinen Kopf und Fuß).
- Python 3.9: keine verschachtelten f-Strings mit gleichen Anführungszeichen.

## Gestaltungsregeln (Kurzfassung der Branding-Richtlinien)
- Farben: Schwarz `#0e1011`, Weiß, Creme `#eeece7` (Flächen, Plakatgrund), Blau `#2f6bff` als einziger Akzent, Grau `#d6d8d9` / `#9a9d9e`. Kein Rot, Gelb, Grün.
- Ausnahme Farbband (Anna, 13.10.2026): 12 px hohes Regenbogen-Band mit rotem Block am unteren Rand des Fußes (`.fuss::after`, Variable `--farbband` in `stil.css`). Nur dort; sonst gilt die Farbregel.
- Kein Blau auf Schwarz (Kontrast). Kein blaues Herz; Herzen nur als Grundform-Herz (siehe Erweiterte Formen).
- Buttons: Primär blau gefüllt (`--farbe-primaer` `#2a5fe6`), Sekundär schwarze Outline (`button button-zweit`), Tertiär unterstrichener Textlink. Jeder Button und jeder eigenständige Link hat einen Pfeil (→, extern ↗, Download ↓).
- Dachzeilen über Überschriften beginnen mit blauem Punkt (per CSS automatisch).
- Leitsatz: „Form follows function“ immer mit kurzer Erklärung („Die Form folgt der Funktion.“).
- Icons aus gefüllten Bauhaus-Grundformen (Kreis, Halbkreis, Quadrat, Dreieck, Balken), jedes mit Schwarz. Clay-Icons (`website/bilder/icons/`) bleiben.
- Erweiterte Formen (Anna, 13.10.2026), alle aus den Grundformen gebaut, Vorlagen in `werkzeuge/grafiken/formen/`: Herz (gedrehtes Quadrat + zwei Halbkreise), Zackenkreis (Kreis mit 16 kleinen Kreisen am Rand), Kreis in Klammern (Kreis zwischen zwei Sicheln). Herzen nur in dieser Konstruktion und nie blau.
- Bewegung, die von selbst startet, hält nach höchstens 5 s an oder hat eine Pause-Taste.
- Startseiten-H1 bleibt ohne Farbverlauf und ohne Formen-Animation (Anna hat die Idee am 13.10.2026 verworfen).
- Kartenreihen: Unterzeilen, Listen und Buttons auf einer Linie; H1 nie breiter als die Seite.
- Website-Screenshots kommen aus der Bildbibliothek `website/bilder/referenzen/` (1440 px breit).
- Wiedererkennung (Anna, 13.10.2026), immer gleich einsetzen:
  1. Eigene Figur aus Bauhaus-Grundformen nach Oskar Schlemmers Triadischem Ballett: Kopf Kreis mit weißem Auge, Rumpf Quadrat, blauer Halbkreis-Rock, Glieder als Balken; Arme sitzen immer direkt am Rumpf, ohne Abstand; ein herabhängender Arm ist abgespreizt, die Hand sichtbar neben dem Rock, nie dahinter; Beine mit Eckenradius 4 (Anna, 13.10.2026); weiße Fugen statt Blau an Schwarz. Konstruktion in `werkzeuge/grafiken/blog/geld-und-zeit-titel.py`.
  2. Ausrufe als Pointe („AAH!“, „OHO!“, „WOW!“), knallhart Schwarz-Weiß in Anton.
  3. Redaktioneller Rahmen: Linien mit Beschriftung, gedrehte Wörter am Rand, wiederholte Schriftbänder.
  4. Echte Fotos von Anna statt KI-Bilder: Schwarz-Weiß ausgeschnitten, kombiniert mit blauen Flächen (bestätigt 13.10.2026: Person Schwarz-Weiß auf Blau, nicht blau getönt). Freistellen mit `werkzeuge/grafiken/freistellen.py`; fertige Fotos (Schwarz-Weiß und blau, freigestellt) liegen unveröffentlicht in `werkzeuge/grafiken/bilder-blau/`.
- Logo (Anna, 13.10.2026): Wortmarke „STUDIO AAH!“ mit gedehntem erstem A – `website/bilder/logo-studio-aah.svg` (Schwarz) und `logo-studio-aah-weiss.svg`. Nur in Kopf und Fuß der Website sowie für Social Media und Print.
- Social Media darf lauter sein (ganze Flächen Schwarz oder Blau, sehr große Schrift); die Website bleibt ruhig: viel Weiß, feine Linien (1,5 px), wenig Creme.

## Inspiration (von Anna gesammelt, „passt zu meinem Stil“) – keine Regel, nicht kopieren
- 13.10.2026, Dribbble „Mall Website Retail Shopping Center“ (https://dribbble.com/shots/27796777): Foto im ganzen Bild, einfarbig eingefärbt (Duoton, duotone) in Orangerot, große weiße Serifen-Überschrift im Bild, kleine Zeichen (Kreuz, Stern, Plus) als Schmuck. Anna will ihre Bilder so – in Blau, leicht bewegt. Die Animation selbst war in der Cloud nicht sichtbar.
- 13.10.2026, Farbtafel: `#8B1D00` (Rostrot), `#1B100F` (warmes Fast-Schwarz), `#F8F8F8`, `#EFE7EF` (blasses Flieder) – als Raster aus Quadraten und Kreisen im Wechsel.
- 13.10.2026, Abspann „Thanks for watching“: fette geometrische Groteske in Versalien, langer dünner Pfeil →, Auge als Zeichen (weiße Ellipse, rote Iris, schwarze Pupille), Fließtext mit kursiven Einzelwörtern, Zeichenreihe am Ende (Herz, Zackenkreis/Siegel, Kreis in Klammern), heller Fliederhintergrund.
- 13.10.2026, Wortmarke „INFLURY“: breite Groteske in Weiß über Foto, ein einzelner Buchstabe (das F) fließend und handschriftlich geformt. Anna: so etwas für ein A in „STUDIO AAH!“ – etwas langgezogen, „fluffiger, handschriftlicher“.
- Widerspruch zu den Regeln oben (Kein Rot): Inspiration ändert die Regeln nicht; erst nach Annas Entscheidung anpassen. Herz, Zackenkreis und Kreis in Klammern sind übernommen (siehe Erweiterte Formen).

## Arbeitsweise
- Antworten auf Deutsch, in Stichpunkten, Schritt für Schritt; Fachbegriffe mit dem englischen Begriff in Klammern.
- Nichts erfinden; Unsicheres als „Unsicher“ kennzeichnen.
- Vor jedem Schritt mit Wirkung nach außen fragen: Hochladen (Push) auf `main` – jeder Push auf `main` geht sofort live –, Installationen, Änderungen bei IONOS. In Cloud-Sitzungen auf einem eigenen Zweig arbeiten; Anna führt ihn über GitHub Desktop zusammen.
- Kleine Commits mit deutscher Beschreibung.
- Nicht öffentlich nennen, wie und wo studio-aah.de gebaut und gehostet ist (Anna, 13.10.2026).
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
