---
paths:
  - "website/**"
  - "werkzeuge/**"
---
# Gestaltung und Texte auf studio-aah.de

Kurzfassung der Branding-Richtlinien (Original in Betrieb: `Kunden Studio AAH/Studio AAH/branding-guidelines.md`). Herkunft und Datum jeder Regel: Archiv der alten CLAUDE.md in Betrieb (`Studio AAH/Website/archiv-claude-md/`).

## Farben
- Schwarz `#0e1011`, Weiß, Creme `#eeece7` (Flächen), Blau `#2a5fe6` (`--farbe-primaer`) als einziger Akzent, Grau `#d6d8d9` / `#9a9d9e`. Kein Rot, Gelb, Grün. Website ruhig: viel Weiß, feine Linien (1,5 px), wenig Creme.
- Ausnahmen, nur dort:
  - Projektseiten `/referenzen/…`: Farben der Kund:innen; Kopf, Fuß, Navigation bleiben in Studio-Farben.
  - Farbband: 12 px Regenbogen mit rotem Block am unteren Rand des Fußes (`.fuss::after`, `--farbband`).
  - Konfetti und Spiel: Farbtafel „modernes Bauhaus“.
  - Rotes Sternchen an Pflichtfeldern (`--farbe-pflicht`).
  - Blauer Anfrage-Button in der schwarzen Abschlussbox der Projektseiten.
- Farbenmeer wie auf der Startseite (Anna 22.11.2026: „das ist mir zu bunt“): Gründe ruhig (Papier A/B, Hauchtöne), kräftige Signalfarben nur auf Karten, Schildern und Chips mit Kontur; nie mehrere gesättigte Vollflächen hintereinander. Auch auf lauten Seiten wie der Demokratie-Seite.
- Genau ein Muster je Seite (Punkte, Karo, Streifen …; das breite Strichel-Band zählt mit), nie hinter Fließtext (Farb-Richtlinie 1.1). Ausnahmen: Startseite und Profil dürfen mehrere Muster haben (Anna 22.11.2026).
- Korrekturen (durchgestrichen und handschriftlich) und Zusätze in Annas Schrift immer rot, auch auf der Projektübersicht `--aah-rot`, Strich und Handschrift, auf jedem Grund (Anna 22.11.2026).
- Abläufe überall als dieselbe Zeitleiste `ol.zl-quer` wie auf den Leistungsseiten, keine eigenen Schritt-Karten (Anna 22.11.2026: „steps überall gleich“).
- Hero-Texte immer bündig links zum Logo, auf jeder Seite; kein zentrierter Inhaltsrahmen im Hero (Anna 22.11.2026).
- Häufige Fragen überall auf Mint-Hauch `--aah-mint-hauch`, Referenzen/Projekte und Branchen überall auf Weiß, Abschluss-CTA ohne farbigen Grund dahinter (Anna 22.11.2026).
- Handschrift in normaler Groß- und Kleinschreibung, keine Versalien (Anna 22.11.2026).
- Kein Blau auf Schwarz (Kontrast). Dachzeilen auf ihrem Grund lesbar: Gelb nur auf Blau oder Schwarz, auf hellen Karten Blau oder Schwarz.
- Illustrationen der Für-wen-, Problem-, Branchen- und Produktseiten nur Schwarz, Weiß, Blau.

## Typografie
- Laut ist nur Anton (Plakatzeilen `.gr-*`), alles andere leise.
- Schriftgrößen nur über `--groesse-1` bis `--groesse-8` im `:root`. Ausnahmen mit Kommentar: Zeilen, die die Breite füllen (`.gr-*`, vw-Formeln), große Kennzahlen, Spiel, gezeichnete Grafiken (`.kb-`, `.pc-`, `.ci-`), Eingabefelder (mindestens 16 px wegen Zoom am iPhone).
- JetBrains Mono nur in Dachzeilen und Versal-Beschriftungen (`.meta`, Kasten-Titel, Tabellen-Beschriftung); Zahlen, Nummern, Text in Manrope. Ausnahmen: `.wr-bon`, `.mr-b-`, Hex-Codes in `referenzen.css`.
- Eckenradien nur `--radius-pille`, `--radius-karte` (24 px) und 50 %. Ausgenommen gezeichnete Mini-Grafiken und Bauhaus-Halbkreise der Zeitleiste.
- Unterzeile deutlich kleiner als ihre Überschrift (etwa Goldener Schnitt). Abschluss-H2 so groß wie möglich. H1 nie breiter als die Seite.
- Anton-Versalien mit Zeilenabstand mindestens 1,15, bei Umlauten 1,2; Satzzeichen und Umlaut-Punkte berühren nie die Nachbarzeile.
- Überschriften ohne Schlusspunkt, außer ganze Sätze; kleine Überschriften (Karten, Zeitleiste) nie. Nie nach dem ersten Wort eines Satzes umbrechen; zwei Sätze („Drei Teile. Ein Regelwerk.“) mit `<br>` nach dem ersten.
- Nie nach kurzem Vorderglied trennen (IT-Projekt, KI-Check, E-Mail): `kurzwoerter_schuetzen()` in `gemeinsam.py`, von Hand `<span class="ohne-umbruch">`. Lange Wörter in Überschriften mit `&shy;`. Jede Seite bei 320 px ohne seitliches Verschieben.
- Dachzeilen überall wie „Mein Studio“ auf dem Profil: Versalien, fett, Schwarz, ohne Punkt (Anna 22.11.2026).

## Buttons, Links, Begriffe
- Primär blau gefüllt, Sekundär schwarze Outline (`button button-zweit`), Tertiär unterstrichener Textlink. Jeder Button und eigenständige Link mit Pfeil (→, extern ↗, Download ↓).
- Im Hero immer nur ein Button. Alle Anfrage-Buttons und der Header-Button heißen „Beratung anfragen“. Ausnahme: Absende-Button im Formular der Kontaktseite heißt „Nachricht senden“; über dem Formular steht „Direkt Beratungstermin buchen ↗“ zur Google-Buchungsseite (Anna 19.11.2026).
- Immer „Button“, nie „Knopf“; Handlungsaufforderung „Call-to-Action-Button“ (CTA-Button).
- Prüfung der bestehenden Website heißt überall „Website-Check“ (auch erster Projektschritt); „Expert Review“ nur auf der Website-Check-Seite als Fachbegriff, im Glossar „Website-Check (Expert Review)“.
- Abläufe in der Sprache von Design Thinking: erster Schritt „Verstehen“, Entwürfe „Ideation“.
- „Form follows function“ immer mit „Die Form folgt der Funktion.“
- E-Mail-Adresse überall info@studio-aah.de.

## Texte
- Neue Texte nur nach Annas Vorgabe, nichts dazuerfinden. Keine Zahl ohne geprüfte Quelle.
- Gedankenstriche sparsam, in Überschriften gar nicht. Kartenüberschriften der Startseite höchstens zwei Zeilen.
- Jede Aussage genau einmal je Seite; was oben beantwortet ist, nicht noch einmal in den häufigen Fragen. Antworten der häufigen Fragen in Wir-Form oder allgemein (Ansprache siehe unten), nicht „Bei STUDIO AAH!“.
- Die vier Schmerzpunkte des Mittelstands überall mitdenken: Neugeschäft (Empfehlungen reichen nicht), Fachkräfte (als Arbeitgeber unsichtbar), Digitalisierung/KI (welche Werkzeuge, wie nutzt das Team sie), Effizienz (alles läuft über den Chef). Nicht: Finanzen, Bürokratie. Nutzen herausstellen, Einwände beantworten („zu klein?“, „erfahren genug?“, „lohnt sich das?“). Keine ERP-, Schnittstellen- oder IT-Sicherheitsversprechen. Konzept: Betrieb `Studio AAH/Website/2026-11-09_konzept_website-als-werkzeug.md`.
- Zielgruppe „baut selbst“ (Vibe-Coding, Baukasten): vorher KI-Arbeits-Setup, mittendrin Hilfe nach Aufwand, vor dem Livegang Website-Check, danach Retainer. Steht auf Webdesign (`#selbst`, Feld `selbstbau`), KI-Beratung, Retainer und im Frag-Feld (`_quelle` „baut selbst“). „Vibe-Coding“ und „KI-Design“ ab und zu als Suchbegriffe.
- Erstgespräch 30 Minuten, online, kostenlos; wöchentliche Abstimmungstermine in Projekten 45 Minuten.

## Bausteine
- Häufige Fragen einspaltig, mittig, ohne weiße Fläche, Plus wird beim Öffnen zum X (CSS für jede `.faq-liste`).
- Abläufe und Zeitpläne immer als Zeitleiste (`ol.zeitleiste`; quer `zl-quer`; in schmalen Spalten `figure.grafik-prozess`). Lesereihenfolge spaltenweise, nie Zickzack (greift per CSS bei vier Schritten).
- Kartenreihen: Unterzeilen, Listen und Buttons auf einer Linie. Keine Sections mit viel leerem Weißraum: eine einzelne Karte mittig und doppelt so breit, eine einzelne Referenz mit Kennzahlen daneben (`referenz_mit_zahlen()`).
- Preise: höchstens zwei Paketkarten nebeneinander (die meistgesuchten, Feld `karten` je Gruppe in `preise-daten.json`, `zwei_pakete()` / `weitere_pakete()` in `gemeinsam.py`); übrige in „Außerdem buchbar“. Baut ein gezeigtes Paket auf ein ausgeblendetes auf, übernimmt es dessen Inhalte.
- Keine Leiste über dem Kopf, auf keiner Seite (`dachzeile()` in `kopf-fuss.py` entfernt Reste).
- Bewegung, die von selbst startet, hält nach höchstens 5 s an oder hat eine Pause-Taste. Einblend-Animationen verstecken Inhalte nur unter `:where(.js)`.

## Formulare
- Pflicht nur mit `required`, rotes Sternchen per CSS, kein Hinweis „Pflichtfeld“. Möglichst nur die E-Mail-Adresse Pflicht. Nachrichtenfeld mit vorbereitetem Text („Guten Tag Frau Härtelt, …“) und darunter `p.anfrage-hilfe`: „Sie können den vorbereiteten Text direkt abschicken oder mit Ihrem Anliegen ergänzen.“ Umgesetzt bei Kontakt und Entwurf Markenhandbuch; Annas Vorschlag: bei allen Formularen so, vorher kurz fragen.
- Newsletter-Häkchen (freiwillig, nicht vorausgewählt) in einem Satz, Text in `NEWSLETTER()` in `js/anfrage.js`. Bei Kontakt- und Angebotsanfragen bleibt es.
- Kostenlose Angebote mit E-Mail-Feld (künftig Downloads und Tests): kein Häkchen, Absenden meldet zum Newsletter an (`data-newsletter-gekoppelt`, Double-Opt-in bleibt), Hinweis fett direkt über dem Button, Datenschutzerklärung Abschnitt 4 und 5. Rechts-Check dazu liegt in Betrieb.
- Website-Check (Anna 20.11.2026): ganz ohne Newsletter und ohne Werbung (`data-ohne-newsletter`), kein Häkchen, keine Anmeldung bei Brevo; Datenschutzerklärung `#website-check` sagt das ausdrücklich.
- Konfetti bei jedem Absenden: `document.dispatchEvent(new Event('konfetti'))` ohne Seitenwechsel, `data-konfetti` am `<main>` jeder Danke-Seite. Neue Formulare und Danke-Seiten immer anschließen. Höchstens 4,5 s, bei „Bewegung reduzieren“ keins (Code in `js/menue.js`).

## Einzelne Seiten
- Kontakt: volle Breite, Formular ohne Dachzeile und Titel, freiwillige Auswahl „Wie haben Sie von mir gehört?“ (Feld `quelle`, steht in der Datenschutzerklärung; `anfrage.js` schickt Auswahlfelder mit).
- Profil (Über mich): Ablauf (`ol.zl-quer`) unter `/profil/#so-arbeite-ich`, dort auch die Fragen zu Erfahrung und KI.
- Grafik „Website als Herzstück“ (Webdesign, Retainer, Marketing & Vertrieb) ohne Link darunter.
- Keine Clay-Icons (`website/bilder/icons/`) neben großen Überschriften auf Profil, Blog und Kontakt; sie werden nach Annas Freigabe der Icon-Übersicht ersetzt.

## Formen, Icons, Wiedererkennung
- Icon-Set: höchstens 50 Icons, immer dieselben; Generator `werkzeuge/grafiken/symbole.py` → `website/bilder/symbole/`, Übersicht lokal `/entwurf-icons/`. Schwarz, Weiß und Blau; Gelb nur als Akzent (Stern, Idee, Warnung, Geld). Gefüllte Bauhaus-Grundformen bis an den Rand, viewBox = Rand der Form (`RAND`), `xMinYMin`. Icons einer Gruppe in einer Farbe. Neues Icon nur, wenn keins passt.
- Erweiterte Formen aus Grundformen (`werkzeuge/grafiken/formen/`): Herz (gedrehtes Quadrat + zwei Halbkreise, nie blau), Zackenkreis, Kreis in Klammern.
- Figur nach Schlemmers Triadischem Ballett: Kopf Kreis mit weißem Auge, Rumpf Quadrat, blauer Halbkreis-Rock, Glieder als Balken direkt am Rumpf; herabhängender Arm abgespreizt, Hand neben dem Rock; Beine Eckenradius 4; weiße Fugen statt Blau an Schwarz. Konstruktion in `werkzeuge/grafiken/blog/geld-und-zeit-titel.py`.
- Ausrufe als Pointe („AAH!“, „OHO!“, „WOW!“) Schwarz-Weiß in Anton. Redaktioneller Rahmen: Linien mit Beschriftung, gedrehte Wörter, Schriftbänder.
- Logo „STUDIO AAH!“ nur aus `website/bilder/logo-studio-aah.svg` / `-weiss.svg`, nur in Kopf und Fuß.
- Porträt überall `anna-haertelt-studio-blau.webp` (rund: `…-rund.jpg`). Echte Fotos von Anna statt KI-Bilder.
- Formensprache 2D; 3D nur als Beispiel im Angebot Marken-Regelwerk.

## Typografie: zwei Schriften (Anna 22.11.2026, geht vor älteren Zeilen zu Manrope, JetBrains Mono und Handschrift-Überschriften)
- Instrument Sans für Überschrift und Text (`--schrift-text`, `--schrift-ueberschrift` und `--schrift-meta` zeigen darauf). Überschriften Stärke 500, eng gesetzt (−0,03 em), Groß- und Kleinschreibung, gerade (nicht gekippt). Manrope ist Anna „zu rund“.
- Annas Handschrift (`--schrift-hand`) nur als Akzent: Korrektur unter einem durchgestrichenen Wort, Dachzeile `.meta`, Randnotiz, Band, Fuß-Notizen. Nie Fließtext, nie eine ganze Überschrift.
- Durchgestrichenes steht immer in der Textschrift, nie in Handschrift.
- Alle H2 gleich groß wie die Hero-Zeile der Startseite (`clamp(38px, 4.9vw, 84px)`), Seitentitel H1 eine Stufe darüber, Unterzeile im Seitenkopf `--groesse-5`.
- Ausnahmen: Schriften der Kund:innen auf Projektseiten (Schriftproben), Anzeigen-Beispiele im Marken-Regelwerk, Logo als Datei.
- Prüfen nach Schriftänderungen: alle Seiten der `sitemap.xml` bei 320 und 1280 px messen (Überlauf, gerenderte Schriftfamilien, Versalien).
- Kontrast selbst prüfen, bevor Anna etwas sieht (Anna 22.11.2026: „grau auf hellblau funktioniert nicht, checke selbst solche Kontraste“): nach jeder Farb- oder Hintergrundänderung `werkzeuge/kontrast-check.html` nach `website/_kontrast.html` kopieren, mit Chrome headless `--dump-dom` laden (misst jeden Text gegen seinen echten Hintergrund auf allen Seiten der Sitemap, Grenze 4,5 : 1, groß 3 : 1), danach wieder entfernen. Auf Hauch-Räumen sind Karten weiß, Text Dunkel; Grau nur `--aah-grau`. Ausnahme: Schriftproben in Kundenfarben auf Projektseiten.
- Hintergründe je Abschnittsart überall wie auf der Startseite (Anna 23.11.2026): Stimmen helles Papier A, Projekte/Referenzen beiges Papier B, Seitenkopf helles Papier A; Seitenfarben nur in den Räumen dazwischen (Anlässe voll, Warum weiß mit Zetteln in Zart, Ergebnis Zart der zweiten Farbe, Fragen Hauch, Abschluss Zart).
- Anmerkungen Anna 22.11.2026: „Das bekommst du“ immer vier Tarotkarten (I–IV) auf Orchidee zart; Referenzen überall als Slider (läuft langsam, hält bei Maus, Fokus und Pause-Button an, bei „Bewegung reduzieren“ still), nur `/referenzen/` behält Raster/Liste; keine Sticker; Artikelvorschau heißt überall „Das könnte dich auch interessieren“; Website-Check-Hero zentriert (Ausnahme zur Hero-Regel).
- Ansprache (Anna 22./23.11.2026): Grundton Wir, immer Du. Wir, wo das Studio arbeitet und liefert (Leistungen, Abläufe, Angebote, Preise, Häufige Fragen), weil Anna mit Agenten und ihrem Netzwerk arbeitet. Ich, wo Anna als Chefin spricht oder für etwas einsteht: Zitate, Anna-Karte, Profil und Über mich, eigene Praxis, Blogartikel, das Versprechen „direkt mit der Chefin“. Faustregel: Leistung = Wir, Haltung, Erfahrung oder Versprechen = Ich.
  - Wir: Leistungen, Abläufe („So gehen wir vor“, „Wie wir arbeiten“), Preise, Kontakt („Schreib uns“, „Wir melden uns“), Referenztexte („haben wir gestaltet“).
  - Ich: Annas Zitate, Anna-Karten („Du arbeitest direkt mit mir“), Profil/Über mich, eigene Praxis („Aus meiner eigenen Praxis“, „Mein Studio läuft mit …“), Erfahrung (Agentur, Studium, Bauhaus), Haltung („Für mich ist eine Website …“), Versprechen („Was ich zusage“, „ich sehe mir jede Website selbst an“), Blog, aah-codes. Gemischt erlaubt: „Was wir dir einrichten, nutze ich selbst jeden Tag.“
  - Frag-Feld der Startseite: Anna antwortet persönlich („Frag mich“, „Ruf mich an“), Leistungsangaben darin trotzdem Wir.
  - Bleibt unverändert: Kundenzitate, Fragen aus Lesersicht („Was brauche ich dafür?“), Texte von Kundenwebsites in Referenzen, rechtliche Texte (Impressum, Datenschutz, Haftung, Formular-Hinweise: Anna ist verantwortlich).
- Keine Comic-Optik: keine harten Versatzschatten, keine dicken schwarzen Konturen, keine schräg gestellten Karten (Anna 22.11.2026: „nicht diese comic optik“). Erlaubt: Fotos im Riso-Look (Graustufen auf Blau oder Pink) mit gelbem Klebestreifen, leicht gedreht, wie im Startseiten-Hero.
- Handschrift-Korrekturen: Kontrast und Lesbarkeit immer prüfen (Anna 22.11.2026). Auf farbigen Flächen (Rot, Blau, Schwarz) Handschrift und Strich weiß, sonst Rot; Handschrift mindestens so groß, dass sie bei 320 px lesbar bleibt.
- Im Abschluss-Call-to-Action (Schluss-Karte) keine Handschrift-Korrekturen (Anna 23.11.2026). Korrekturen nur, wo der Satz danach Sinn ergibt; sonst Überschrift ohne Korrektur.
- Überschriften (Anna 23.11.2026, „Mischung“): Markensätze bleiben auf allen Seiten gleich („Stimmen, die zählen.“, „Ehrliche Antworten“, „Fangen wir klein an.“); Ablauf und Preise je Seite mit Suchbegriff („Webdesign in vier Schritten“, „Was Webdesign kostet“).
