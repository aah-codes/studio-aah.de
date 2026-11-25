---
paths:
  - "website/index.html"
  - "website/js/start.js"
  - "website/js/frag.js"
  - "website/js/menue.js"
  - "website/daten/**"
  - "werkzeuge/kopf-fuss.py"
  - "werkzeuge/inhalte-erzeugen.py"
  - "werkzeuge/fragen-index.py"
  - "werkzeuge/inhalte/hero-themen.json"
  - "werkzeuge/inhalte/projekte.json"
  - "werkzeuge/inhalte/linkedin.json"
---
# Startseite, Menü und Fuß

## Aufbau der Startseite
Hero `.hl` → Über mich kurz (Intro, darunter „Wo es gerade hakt“ als drei Links `.hakt-links`) → Im Fokus `.fokus` (feste Angebote ohne Preise) → Leistungen → Projekte als Liste `.pliste` → Stimmen → Aktuelles (LinkedIn) → Branchen → Häufige Fragen → Kontakt.

- Seitentitel „Webdesign in Leipzig für den Mittelstand | STUDIO AAH!“. H1 kurz: „Webdesign und Relaunch für den Mittelstand in Leipzig.“. Groß darüber, aber kein H1: „Du bist gut genug. Lass es auch die anderen wissen.“ mit Korrektur „wissen.“ → handschriftlich „sehen!“. Keine Dachzeile.
- **Hero neu `.kr.kr-neu`:** Dachzeile „STUDIO AAH! · Aus Leipzig für den B2B-Mittelstand“, H1 „Wir machen aus „ganz okay“ ein echtes AAH!“, Unterzeile, Buttons „Beratung anfragen“ und „Kostenloser Website-Check“, Pills „Wo hakt es bei euch gerade?“ (neue-kunden/, fachkraefte/, ki-im-team/, mindestens 44 px), Anna-Karte rechts (Handy darunter). Laufband: Über 40 Projekte und Branchen. Im Fokus: „Feste Angebote · Klare Preise“ / „Kein Agentur-Blabla. Sondern Pakete, die sofort helfen.“, Reihenfolge Website-Check, KI-Team-Setup, KI-Marken-Regelwerk, Retainer, je Karte Badge und Linktext. Ruhig, keine Comic-Optik.
- Zeichnungen schwarz-weiß: Strichzeichnungen ohne Farbe und ohne Versatz, Generator `werkzeuge/grafiken/zeichnungen-sw.py` (Auge, Bildschirm, Megafon, Glühbirne, Blitz, Pfeil, Stern, Herz), dekorativ mit `alt=""`.
- Hero links: blaue Fläche mit Frag-Feld und Chips; rechts Diashow (`js/start.js`, Bilder in `bilder/start/`, ab Folie 2 per `data-src` nachgeladen; Fotos in Naturfarben, Leipzig-Bilder nie nebeneinander, Pause-Button, Nachweise im Impressum). Feste Höhe.
- Frag-Feld: sucht nur in kuratierten Themen (`werkzeuge/inhalte/hero-themen.json`: Stichwort-Gruppen, Antwort = eine häufige Frage der Website im Wortlaut; Themen zu Anna aus der Profilseite mit Link zu LinkedIn; ohne Treffer Telefon und Beratung). Nichts wird gesendet. Platzhalter „Warum bringt meine Website keine Anfragen?“, Button „Antwort“, kein Hinweis darunter. Ton freundlich („Ja, klar!“, „Sehr gern!“).
- Chat nach der ersten Frage (`js/frag.js`, `.hl-chatfenster`): Überschrift einzeilig, H1 nur noch unsichtbar; Kopfzeile mit Foto und „Anna Härtelt“, Creme-Grund mit Bauhaus-Muster, „Heute“, Frage als blaue Blase rechts mit Uhrzeit und Haken, kurz „schreibt …“, Antwort als weiße Blase links mit rundem Foto, Links als Zeilen in der Blase; neueste Runde unten über dem Feld, höchstens drei Runden. Antwortblock: Kurzfassung, bis zu drei Stichpunkte, Links als Quellen (extern neues Fenster). Konzept: Betrieb `Studio AAH/Website/2026-11-16_konzept_hero-frag-feld.md`.
- Leistungen der Startseite: drei Kernkompetenzen (Markenbildung, Webdesign, KI-Beratung) nebeneinander, Form mittig in der Creme-Fläche, Name zentriert, ohne Unterzeile, am Handy untereinander; Retainer nicht hervorgehoben.
- Projekte: `projekt_liste()` in `inhalte-erzeugen.py`, Feld `kurzleistungen` in `projekte.json` (ohne Plattform-Namen, ohne Flyer). Große Projektkacheln (`projekt_raster()`, Feld `schlagzeile`) nutzen die Branchenseiten. Projektkacheln und Projekt-Karten überall mit schwarzem Grund (`KACHEL_GRUND`); Hausfarbe der Kund:innen nur auf der Projektseite.
- Projektkarten: Feld `vorschau` (Foto aus der Kundenwebsite) als Grund, darüber `vorschau_website` (oberer Website-Ausschnitt, 800 × 1000, unten angeschnitten); ohne `vorschau_website` nur das Foto (Down to Earth). Karten 5 : 6, Name 18 px, Link 15 px wie Name und Funktion bei den Stimmen. Strichel-Band unter dem Kopf schwarz.
- Aktuelles: eigene LinkedIn-Beiträge aus `werkzeuge/inhalte/linkedin.json`, Bilder lokal `website/bilder/linkedin/li-<id>.webp` (640 × 800), nichts von LinkedIn laden, keine Reposts; GIF mit `"datei": "gif"`, spielt beim Hineinscrollen einmal ab.
- Branchen-Mosaik über Marker `BRANCHEN`, Reihenfolge Bau, Software & IT, Handwerk, Energie, Industrie, Beratung (breite Kachel), Gesundheit (`reihenfolge` in `startseite_branchen()`).
- Köpfe von „Wo es gerade hakt“, Projekte, LinkedIn und Stimmen mittig (`sk-mitte`). Stimmen ohne Unterzeile.
- Der alte Leistungs-Slider wird nirgends eingebaut (gesichert in Betrieb `Studio AAH/Website/gestaltung/2026-11-09_hero-slider-leistungen/`); `js/hero.js` ist ungenutzt.
- Letzter Abschnitt der Startseite: nur der blaue Website-Check-Block „Fit für 2027? Finden wir es heraus.“ mit Namen aus dem Hero.

## Menü
- Hauptmenü am Desktop mittig zwischen Logo und Button: Leistungen · Branchen · Projekte (Adresse `/referenzen/`) · Über mich · Aktuelles (Adresse `/blog/`).
- Mega-Menüs „Leistungen“ und „Branchen“ (`js/menue.js`, `aria-controls`), über die Inhaltsbreite, mit Bauhaus-Icons (`mm-mit-icon`, 31 px). Menüpunkte in Manrope 600, 18 px, ohne Unterzeile; Karten rechts beige (`mm-karte-beige`) nur mit Dachzeile, Titel (Anton) und Button.
- Leistungen: Kernkompetenzen (Markenbildung, Webdesign, KI-Beratung) · Feste Angebote in der Reihenfolge Marken-Regelwerk, Website-Check, KI-Team-Setup, Retainer · Weitere Leistungen (UI/UX, Marketing & Vertrieb, Employer Branding, Druck, Animation, Illustration & Infografik).
- Branchen-Menü rechts mit dem KI-Team-Setup als Angebot. Mega- und Mobilmenü der Branchen stehen von Hand in `index.html`.
- Leistungs-Formen im Menü sind dieselben Dateien wie auf den Leistungsseiten (`formen/brand|website.svg`, KI der Zauberstab `symbole/skills.svg`); Website-Check `symbole/scanner.svg`.

## Fuß
- Kontakt · Leistungen (Kernkompetenzen, Feste Angebote, Weitere, Preise) · Branchen (alle sieben, darunter „Wo es hakt“) · Studio (Über mich, Projekte, Blog, Selbst testen, Initiative). Neue Seiten dort eintragen.

## Aktuell (geht vor älteren Zeilen)
- Seitentitel „Markenbildung, Webdesign & KI-Beratung in Leipzig | STUDIO AAH!“; H1 kurz „Design Studio aus Leipzig.“; Suchbegriffe stehen in Titel und Beschreibung, nicht im Hero.
- Auge im Hero zwinkert zweimal nach dem Laden (Animation im SVG, `werkzeuge/grafiken/zeichnungen-sw.py`), bei „Bewegung reduzieren“ offen.
- Chat: Name „Anna Härtelt“ nur im Chatkopf, nicht in den Antwortblasen; erste eigene Blase „Hallo, ich bin <Name>.“; im Chat kein Platzhalter, sondern blinkende Schreibmarke (`.fh-marke`).
- Leistungen: Korrekturzeile „Das kann ich für dich machen“.
