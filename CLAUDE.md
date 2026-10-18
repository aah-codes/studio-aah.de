# studio-aah.de – Hinweise für Claude Code

## Was dieses Repository ist
- Die statische Website von Studio AAH (Anna). Reines HTML und CSS – kein Baukasten, kein Bau-Schritt, kein npm.
- Maßgeblich ist die Spezifikation (von Anna freigegeben am 03.10.2026): lokal `doku/spezifikation.md` (nicht im Repository), Original im iCloud-Ordner `Betrieb` unter `Kunden Studio AAH/Studio AAH/Website/`. Bei Widerspruch gilt die Spezifikation; Widerspruch Anna melden.
- Veröffentlicht wird nur der Ordner `website/` (GitHub Pages, Workflow `.github/workflows/github-pages.yml`). Alles andere (Werkzeuge) bleibt draußen.
- Das Repository ist öffentlich: nur Dateien hinein, die jeder sehen darf. Nur Schriften mit freier Lizenz (SIL OFL), keine internen Notizen, Preise oder Kundendaten.

## Stand (13.10.2026)
- Die Website ist umgesetzt und live. Die WordPress-Vorlage im Nachbarordner ist nur noch Archiv. Texte ändert Anna laufend; neue Texte nur nach ihrer Vorgabe, nichts dazuerfinden.
- In Cloud-Sitzungen gibt es keinen Zugriff auf den iCloud-Ordner `Betrieb` (Projektstatus, Branding-Richtlinien). Die wichtigsten Regeln stehen deshalb unten. Was in `Betrieb` eingetragen werden müsste, am Ende als Liste für Anna ausgeben.

## Generatoren (immer nach Änderungen an Daten oder Vorlagen, vom Repository-Ordner aus)
- **`bash werkzeuge/alle-erzeugen.sh`** – startet die Seiten-Generatoren in der richtigen Reihenfolge (Kopf und Fuß → Preise → Blogbeitrag → Inhalte → Leistungsseiten → Referenzen). Einzeln nur, wenn man genau weiß, was man tut:
- `python3 werkzeuge/kopf-fuss.py` – Kopf und Fuß aus `website/index.html` in alle Seiten (Pfade passend zur Ordnertiefe, 404-Seite ab der Wurzel). Kopf und Fuß nur in `website/index.html` ändern.
- `python3 werkzeuge/preise-erzeugen.py` – Preise, Kostenrechner-Daten, Leiste, Glossar
- **Blogbeiträge** (Anna, 19.10.2026: jeder Artikel nach demselben Schema): `werkzeuge/blog/<slug>.py` je Beitrag ruft `bauen()` aus `werkzeuge/blog/beitrag.py` auf (Kopf/Fuß des KI-Artikels, Kurz gesagt, FAQ, strukturierte Daten). **Vor jedem neuen Beitrag lesen:** `werkzeuge/blog/schema-blogbeitrag.md`; Schreibregeln im Skill `texte-studio-aah`. Texte nur in `werkzeuge/blog/<slug>-inhalt.html` und der FAQ im Skript ändern. Bisher: `was-kostet-eine-website.py` (Reihe Website-Fragen, Teil 1), `was-sollte-eine-website-2027-koennen.py` (Teil 2)
- `python3 werkzeuge/inhalte-erzeugen.py` – Referenzen, „Für wen“, Stimmen, Blog-Vorschau, Kennzahlen (Marker `<!-- NAME:START -->` … `<!-- NAME:ENDE -->`)
  - Kennzahl „Jahre selbstständig“ wird aus `"seit": 2020` in `werkzeuge/inhalte/kennzahlen.json` berechnet (Anna, 16.10.2026); sie zählt bei jedem Erzeugen weiter – nach dem Jahreswechsel einmal alle Generatoren laufen lassen und hochladen.
  - Liest die Lesezeit aus den fertigen Blogseiten, läuft also nach dem Blog-Skript.
- `python3 werkzeuge/leistungsseiten.py` – alle Seiten unter `website/service/` aus `werkzeuge/leistungen-inhalte.json` und `werkzeuge/preise-daten.json`; der Prozess kommt aus `website/index.html`, Kopf und Fuß bleiben aus der bestehenden Seite erhalten
- `python3 werkzeuge/referenzen.py` – Projektübersicht und Projektseiten unter `website/referenzen/` aus `werkzeuge/inhalte/projekte.json`; Kopf und Fuß von der Profil- bzw. Webdesign-Seite. Bild-Versionen `?v=` aus dem Dateiinhalt
- `python3 werkzeuge/grafiken/ci-film.py` – CI-Grafik (`werkzeuge/grafiken/corporate-identity.html`)
- `python3 werkzeuge/grafiken/druck-mockup.py PFAD/schreibtisch.jpg` – Druck-Mockup (Goldhammer-Visitenkarten auf Schreibtisch); Foto liegt nicht im Repository
- `python3 werkzeuge/grafiken/fotostudio.py` – Porträts mit blauer Studiowand (Entwurf, Schwarz-Weiß-Vorlagen)
- Erzeugte Bereiche nie direkt in `website/` ändern, sondern in der Quelle, dann neu erzeugen.
- Gemeinsame Hilfsfunktionen der Generatoren (Pfade, `esc`, `euro`, `einsetzen`, Seitenrahmen, Bildmaße, Paketkarte) stehen in `werkzeuge/gemeinsam.py` – dort ändern, nicht in den Skripten kopieren. Ersetzungen brechen mit Meldung ab, wenn ein Marker fehlt. Texte von „Für wen“ (Startseite) in `werkzeuge/inhalte/fuer-wen.json`.
- Nach CSS- oder JS-Änderungen die Cache-Version `?v=…` überall erhöhen (z. B. `sed` über `grep -rl` in `website` und `werkzeuge`), dann alle Generatoren laufen lassen.
- Prüfen mit `bash werkzeuge/pruefen.sh` – Kopf und Fuß, Links und Bilder, und ob die erzeugten Bereiche aktuell sind (Meldungen zu Entwurfsseiten `website/entwurf-…` ignorieren, falls es welche gibt; sie haben bewusst keinen Kopf und Fuß).
- Python 3.9: keine verschachtelten f-Strings mit gleichen Anführungszeichen.

## Gestaltungsregeln (Kurzfassung der Branding-Richtlinien)
- Farben: Schwarz `#0e1011`, Weiß, Creme `#eeece7` (Flächen, Plakatgrund), Blau `#2a5fe6` (`--farbe-primaer`) als einziger Akzent (bis 16.10.2026 auch `#2f6bff`, auf Annas Wunsch vereinheitlicht), Grau `#d6d8d9` / `#9a9d9e`. Kein Rot, Gelb, Grün.
- Ausnahme Projektseiten (Anna, 14.10.2026): Auf Projektseiten (`/referenzen/…`) gelten die Farben der Kund:innen; dort darf die Farbregel gebrochen werden (z. B. Bauer-Blau `#003466`, Bauer-Gelb `#FBD52A`). Kopf, Fuß und Navigation bleiben in Studio-Farben.
- Ausnahme Farbband (Anna, 13.10.2026): 12 px hohes Regenbogen-Band mit rotem Block am unteren Rand des Fußes (`.fuss::after`, Variable `--farbband` in `stil.css`). Nur dort; sonst gilt die Farbregel.
- Dachzeilen müssen auf ihrem Grund lesbar sein (Anna, 15.10.2026): Gelb nur auf Blau oder Schwarz, auf hellen Karten Blau oder Schwarz.
- Kein Blau auf Schwarz (Kontrast). Kein blaues Herz; Herzen nur als Grundform-Herz (siehe Erweiterte Formen).
- Ausnahme (Anna, 15.10.2026): Anfrage-Knopf in der schwarzen Abschlussbox der Projektseiten ist blau (`--farbe-primaer`, Knopf zur Fläche 3,4 : 1, Schrift 5,4 : 1).
- Buttons: Primär blau gefüllt (`--farbe-primaer` `#2a5fe6`), Sekundär schwarze Outline (`button button-zweit`), Tertiär unterstrichener Textlink. Jeder Button und jeder eigenständige Link hat einen Pfeil (→, extern ↗, Download ↓).
- Dachzeilen über Überschriften beginnen mit blauem Punkt (per CSS automatisch).
- Leitsatz: „Form follows function“ immer mit kurzer Erklärung („Die Form folgt der Funktion.“).
- Icons aus gefüllten Bauhaus-Grundformen (Kreis, Halbkreis, Quadrat, Dreieck, Balken), jedes mit Schwarz. Clay-Icons (`website/bilder/icons/`) bleiben.
- Erweiterte Formen (Anna, 13.10.2026), alle aus den Grundformen gebaut, Vorlagen in `werkzeuge/grafiken/formen/`: Herz (gedrehtes Quadrat + zwei Halbkreise), Zackenkreis (Kreis mit 16 kleinen Kreisen am Rand), Kreis in Klammern (Kreis zwischen zwei Sicheln). Herzen nur in dieser Konstruktion und nie blau.
- Bewegung, die von selbst startet, hält nach höchstens 5 s an oder hat eine Pause-Taste.
- Einblend-Animationen: Inhalte im CSS nur unter `:where(.js)` verstecken (`js/menue.js` setzt die Klasse `js` am `<html>`), damit ohne JavaScript alles sichtbar bleibt.
- Startseiten-H1 bleibt ohne Farbverlauf und ohne Formen-Animation (Anna hat die Idee am 13.10.2026 verworfen).
- Kartenreihen: Unterzeilen, Listen und Buttons auf einer Linie; H1 nie breiter als die Seite.
- Prozesse und Zeitpläne (Abläufe, Timelines) immer mit derselben Zeitleisten-Grafik wie auf der Startseite (`ol.zeitleiste`, Anna 13.10.2026); in schmalen Spalten wie Artikeln einspaltig (`figure.grafik-prozess`). Blaue Marken in `--farbe-primaer` (Kontrast 5,4 : 1).
- Satzzeichen und Umlaut-Punkte dürfen sich nie mit der Zeile darüber oder darunter berühren (Anna, 15.10.2026): Versal-Überschriften in Anton mit Zeilenabstand mindestens 1,15, bei Umlauten in Versalien 1,2.
- Lange Wörter in Überschriften (z. B. „Unternehmens&shy;präsentation“) mit weichem Trennstrich `&shy;` versehen; jede Seite bei 320 px Breite ohne seitliches Verschieben prüfen.
- Website-Screenshots kommen aus der Bildbibliothek `website/bilder/referenzen/` (1440 px breit).
- Mockups (Anna, 15.10.2026, gilt für alle Referenzen und die ganze Website): immer hochwertige, echte Foto-Mockups von echten, modernen Geräten (State of the Art, z. B. moderner silberner Laptop). Keine gezeichneten oder per CSS nachgebauten Geräte, keine KI-Bilder. Lizenz für gewerbliche Nutzung (z. B. Canva-Mockups, Mockuptree), Nachweis im Impressum unter „Bildnachweise“. Quellbild mindestens doppelt so breit wie angezeigt. Gerät nach Zielgruppe der Kund:innen wählen (Anna, 15.10.2026): Wie schauen deren Besucher:innen auf die Website? HR/B2B (z. B. Deinetwegen) → moderner Apple-Standrechner (iMac) im Hero; Behörden/öffentliche Auftraggeber (z. B. Bauer) → schwarzer Büromonitor mit dunklem Standfuß, hochmodern, kein iMac; Ärztinnen (z. B. Simone) → vor allem Handy; Kreative (z. B. Jana) → Laptop und Handy.
- Wiedererkennung (Anna, 13.10.2026), immer gleich einsetzen:
  1. Eigene Figur aus Bauhaus-Grundformen nach Oskar Schlemmers Triadischem Ballett: Kopf Kreis mit weißem Auge, Rumpf Quadrat, blauer Halbkreis-Rock, Glieder als Balken; Arme sitzen immer direkt am Rumpf, ohne Abstand; ein herabhängender Arm ist abgespreizt, die Hand sichtbar neben dem Rock, nie dahinter; Beine mit Eckenradius 4 (Anna, 13.10.2026); weiße Fugen statt Blau an Schwarz. Konstruktion in `werkzeuge/grafiken/blog/geld-und-zeit-titel.py`.
  2. Ausrufe als Pointe („AAH!“, „OHO!“, „WOW!“), knallhart Schwarz-Weiß in Anton.
  3. Redaktioneller Rahmen: Linien mit Beschriftung, gedrehte Wörter am Rand, wiederholte Schriftbänder.
  4. Echte Fotos von Anna statt KI-Bilder, Stil seit 13.10.2026 (Anna): Farbfoto, Wand in Markenblau wie im Fotostudio ausgeleuchtet (Mitte heller, außen dunkler, Licht und Schatten passend zum Gesicht), Kleidung in Blautönen, Gesicht in echter Farbe. Website-Porträt: `website/bilder/anna-haertelt-studio-blau.webp` (rund: `…-rund.jpg`). Freistellen mit `werkzeuge/grafiken/freistellen.py`; Farb-Originale nie ins Repository.
- Logo (Anna, 13.10.2026): Wortmarke „STUDIO AAH!“ mit gedehntem erstem A – `website/bilder/logo-studio-aah.svg` (Schwarz) und `logo-studio-aah-weiss.svg`. Nur in Kopf und Fuß der Website sowie für Social Media und Print.
- Social Media darf lauter sein (ganze Flächen Schwarz oder Blau, sehr große Schrift); die Website bleibt ruhig: viel Weiß, feine Linien (1,5 px), wenig Creme.

## Startseite und Leistungen (Anna 13.10.2026)
- Leistungsnamen: Markenbildung, UI/UX, Webdesign, Marketing & Vertrieb, Druck, Illustration & Infografik, Animation, Retainer, KI & Digitalisierung. Adressen: `service/markenbildung/`, `webdesign/`, `druck/`, `animation/` (alte Adressen `brand/`, `website/`, `print/`, `motion-design/` leiten weiter).
- H1 der Startseite: „Hier werden Sie gesehen.“ (Desktop einzeilig).
- Hero-Leiste: Kategorien wie bei Dribbble, verlinkt, mit Pause-Taste (Daten in `werkzeuge/preise-erzeugen.py`, `KATEGORIEN` und `BEISPIELE`). Regel „ein Kunde, ein Platz“: jeder Kunde höchstens einmal, Lücken mit STUDIO AAH! selbst. Foto-Mockups liegen in `website/bilder/mockups/` (Inhalt per `matrix3d` im Bildschirm). Alle Bilder müssen scharf sein: Quellbilder mindestens doppelt so breit wie angezeigt.
- Leistungskarten der Startseite: keine Kundenbilder, sondern nur das Clay-Icon (multiply), ohne Formen. Kunden stehen in den Success Stories.
- Leistungsseiten: weiter unten „Aus der Praxis“ mit passendem Kundenbeispiel (`MOCKUPS` in `werkzeuge/leistungsseiten.py`).
- Mockup-Nachweise (Mockuptree, Bendito Mockup) stehen im Impressum unter „Bildnachweise“.

## Referenzseiten (Case Studies)
- **Vor jeder neuen Referenzseite lesen:** `werkzeuge/anleitung-referenzseite.md` (Ablauf, Storyline-Schablone, Bausteine, Prüfliste, Recherche-Erkenntnisse). Vollständige Fassung mit Briefing der nächsten Referenz in `Betrieb` (Studio AAH/Website/2026-10-15_anleitung-referenzseite.md).
- Bildwerkzeuge (Zusammensetzen, Ausschnitt, Kontaktbogen, Retusche) in `werkzeuge/grafiken/bild/`.

## Projektseite Bauer (Stand 15.10.2026)
- `/referenzen/bauer/` wird aus `varianten.b` erzeugt (`hauptvariante: "b"` in `werkzeuge/inhalte/projekte.json`); Variante A nur im Tag `bauer-variante-a-2026-10-14`.
- Heft (Unternehmenspräsentation) ausgeblendet bis zur Abnahme der Druckdatei; Einstellungen in `varianten_ablage.heft`. Vor dem Einblenden Seiten neu erzeugen und auf Personen und Platzhalter prüfen.
- Mockup (Anna, 15.10.2026): Vorher-Film läuft im echten Foto „heller Monitor auf Holzschreibtisch“ (Sora Sagano, Unsplash; MacBook und Controller wegretuschiert, `bilder/referenzen/bauer/monitor-foto.jpg`, Option `monitor` mit `foto`/`schirm`). Anna hatte zuerst einen schwarzen Büromonitor gewünscht und dann dieses Foto gewählt.
- Einstieg wie Deinetwegen (Anna, 15.10.2026: Deinetwegen ist der Blueprint für den Einstieg): H1 ohne Einleitung, Bildschirmwand, Überblick (Aussage + Leistungen), Inhalt; Ausgangslage: Karte Herausforderung (Liste, weiß) + Karte Lösung (Bauer-Blau), darunter Ziele 1–4 nummeriert. Kennzahlen 83/69/13 stehen im Ergebnis, nicht im Einstieg.
- Bauer-Farben auf der Projektseite (Anna, 15.10.2026): alle Überschriften schwarz, nie blau; Punkt der Dachzeile gelb, auf hellem Grund mit feinem dunkelblauem Rand (Gelb allein auf Weiß zu schwach).
- Vorher-Film mit Knöpfen „Vorher“ und „Nachher“ (Anna, 15.10.2026: direkt zur neuen Seite springen); Nachher-Folge nur aus geprüften Aufnahmen ohne Personen (Startseite, Referenz, Karriere).
- Keine Mitarbeitenden zeigen: Ausschnitte mit Personen ersetzen statt weichzeichnen. Vor jeder Veröffentlichung Prüfer-Agent auf Personen, Platzhalter und interne Inhalte.
- Bilder, die keine Seite mehr nutzt, aus `website/` entfernen – sonst sind sie öffentlich abrufbar.
- Übergabe mit allen Details liegt in `Betrieb` (Studio AAH/Website/2026-10-15_uebergabe-bauer-projektseite.md).

## Projektseite Deinetwegen (Stand 15.10.2026)
- `/referenzen/deinetwegen/` aus `varianten.b` (`hauptvariante: "b"`); alte Fassung verworfen. **Vorlage für Onepager-Referenzen** (nächste: Jana Voigtmann); Bauer ist die Vorlage für KMU-Websiteprojekte (Anna, 15.10.2026).
- Kein Kapitel „Vorgehen / Vier Schritte“ (Anna, 15.10.2026, gestrichen).
- Nicht erwähnen: Folgeauftrag „People First“ (nie online), Gründungsumstände, Absage/Plattform. Live-Link nur mit „Stand 10/2026“; entfernen, sobald Franziskas neue Seite online ist.
- Schrift Satoshi (ITF, keine OFL) nie als Datei ins Repository; nur als Bild (`werkzeuge/grafiken/schriftmuster.swift`).

## Projektseite Jana Voigtmann (Stand 16.10.2026)
- `/referenzen/jana-voigtmann/` aus `varianten.b` (`hauptvariante: "b"`), alte Fassung verworfen. Muster Deinetwegen (Einstieg) plus Bauer (Raster aller Seiten oben). Texte von Anna freigegeben (16.10.2026).
- Raster (Anna, 16.10.2026): gleichmäßiges Muster (`buehne_wand.muster`), fünf gleich breite laufende Spalten ohne feste Mitte, stark gezoomt („plakativ“, Details zeigt die Seite weiter unten), leicht schräg aufsteigend (`winkel: -6`), Kacheln ohne Umriss, gerade Kante, Grund Weiß. Kacheln = 16 Abschnitte aus Annas Auswahl (`wl/abschnitt-*.jpg`) in Seitenreihenfolge: Startseite (Hero, Ausstellungen, Fuß), Mixed Media, Malerei, Grafik, Über.
- Über und Kontakt nur Hero bis Stipendien plus Fuß mit Kontakt (Anna: „viel Textwüste“); am Handy Ausstellungen und Sammlungen herausgeschnitten.
- Nicht nennen: Plattform (Wix). Kein „Branding“ (kein eigenes Logo; Wortmarke = Instagram-Name „@JANA_VOIGTMANN“, aus Helvetica nachgesetzt).
- Stopp-Knopf der Bildschirmwand sitzt unten rechts über den Kacheln (`.hw-knopf`, vorher unerreichbar, alle Referenzen).
- Galerie (Anna, 16.10.2026: „bei Klick auf Bild geht Slider auf mit Titel und Beschreibung“): eigene schwarze Sektion zwischen den drei Genres und „Über und Kontakt“, Baustein `durchklick` (drei Aufnahmen `galerie-1…3.jpg`, Klick aufs Bild zeigt die nächste; keine eigenen Pfeile oder Zähler – Anna: „irreführend“). Text von Anna freigegeben (16.10.2026).
- Kein Geräte-Mockup (Anna, 16.10.2026: „mockup raus“; Atelier-Monitor und MacBook entfernt, Bildnachweise gelöscht).

## Typografie auf Referenzseiten (Anna, 16.10.2026)
- Überall wie bei Bauer: Baustein `designsystem` (Farbkarten, „Aa“, Schriftstufen H1 bis Button mit den Werten der Live-Seite). Schriften ohne freie Lizenz (Satoshi, Helvetica) als Bild je Stufe (`werkzeuge/grafiken/schriftstufen.swift`), freie Schriften (Inter, Montserrat) lokal als woff2. Details in `werkzeuge/anleitung-referenzseite.md`.

## Projektseite Dr. Simone Goldhammer (Stand 16.10.2026)
- `/referenzen/goldhammer/` aus `varianten.b` (`hauptvariante: "b"`), Duplikat von Janas Aufbau (Anna, 16.10.2026: „dupliziere die seite von jana und füge die inhalte zu simone ein“). Texte (Überblick, Ausgangslage, Ziele, Ergebnis, Credits, Abschluss) von Anna freigegeben am 16.10.2026.
- Website ist von Anna (jetzige Seite); Plattform nicht nennen und Simones Website nicht verlinken (Anna, 16.10.2026). Gezeigt: Website, Logo/Branding, Flyer, Visitenkarten. Simone einverstanden laut Anna.
- Farben laut Quelltext: Gelb `#FFED00`, Überschriften `#3A3A3A`; Schrift Montserrat + Helvetica (als Bildausschnitt der Website). Logo = Logo der Website (nicht das neuere Logo-Paket vom August 2026).
- Aufnahmen: Desktop mit `AUFNAHME_BREITE=1920` (darunter ist der Kopf abgeschnitten), Handy mit `AUFNAHME_HANDY_BREITE=320`.

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
- Nach jeder Änderung den aktuellen Stand selbst in der Vorschau öffnen (Browser-Bereich der Desktop-App, `.claude/launch.json` → `website`, Port 8123) und die Adresse nennen, z. B. `http://localhost:8123/referenzen/bauer/` (Anna, 14.10.2026). GitHub Desktop zeigt nur Code, die Live-Seite erst nach dem Hochladen.

## Regeln für den Code
- CSS: `website/css/stil.css` für alle Seiten, Farben, Schriften und Abstände als CSS-Variablen im einen `:root` am Anfang (keine festen Farbwerte im Rest der Datei). Bausteine der Projektseiten in `website/css/referenzen.css`, nur dort geladen (Anna, 16.10.2026; `referenzen.py` setzt den Link mit derselben Version wie `stil.css`).
- Breakpoints (Anna, 18.10.2026): nur noch die Stufen 400 / 600 / 768 / 900 / 1024 / 1200 px, geschrieben als `max-width: 767.98px` / `min-width: 768px`, `max-width: 900px` / `min-width: 900.02px`, `max-width: 1024px` / `min-width: 1024.02px` (keine Lücke bei Zwischenbreiten durch Zoom). Einzige Ausnahme: 1100 px für Sitemap und Weg der Projektseiten (darunter 3 Spalten). Neue Regeln an diese Stufen hängen.
- Schriften lokal aus `website/schriften/` (woff2), nichts von fremden Servern laden.
- JavaScript: `js/menue.js` für alle Seiten (ein Block, nichts global), Abläufe der Projektseiten in `js/referenzen.js` (nur dort geladen, Version wie `menue.js`). Pause-Tasten über die gemeinsame Hilfsfunktion in `referenzen.js`.
- Keine Fremddienste, keine Cookies, kein Analyse-Werkzeug, kein JavaScript-Rahmenwerk. Ausnahmen (Anna, 16.10.2026): Formspark für die Anfrageformulare und Brevo für den Newsletter; beide stehen in der Datenschutzerklärung. Neue Dienste nur nach Annas OK und mit Eintrag in der Datenschutzerklärung. JavaScript nur, wo es ohne nicht geht (z. B. Mobilmenü), und dann wenige Zeilen.
- Nur relative Pfade – der Benutzername ist auf den beiden Macs verschieden.
- Zugänglichkeit: sinnvolle Überschriften-Reihenfolge, Alternativtexte, sichtbarer Fokus, ausreichender Kontrast.
- Nie ins Repository: Zugangsdaten, `.env`, Kundendaten, PDFs (siehe `.gitignore`).

## Bilder
- Bilder liegen in `website/bilder/`. Für das Web verkleinern; Ziel: ganzer Ordner `website/` klein halten.
- Format (Anna, 18.10.2026): WebP, höchstens 250 KB; Schärfe geht vor. Ausnahmen bleiben JPG: lange Seitenaufnahmen (höher als 2,5 × breit; WebP kann höchstens 16 383 px hoch sein), Vorschaubilder für soziale Netzwerke (`og:image`) und Bilder, die als WebP nicht unter 250 KB kommen, ohne sichtbar zu verlieren. Umwandeln nur mit Prüfung (Ähnlichkeit SSIM ≥ 0,985 je Farbkanal, Stichprobe in doppelter Vergrößerung). JPGs verlustfrei mit `jpegtran -copy icc -optimize -progressive`.
