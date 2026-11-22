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

## Aufbau der Startseite (wie ein LinkedIn-Profil)
Hero `.hl` → Über mich kurz (Intro, darunter „Wo es gerade hakt“ als drei Links `.hakt-links`) → Im Fokus `.fokus` (feste Angebote ohne Preise) → Leistungen → Projekte als Liste `.pliste` → Stimmen → Aktuelles (LinkedIn) → Branchen → Häufige Fragen → Kontakt.

- Seitentitel „Webdesign in Leipzig für den Mittelstand | STUDIO AAH!“. H1 kurz: „Webdesign und Relaunch für den Mittelstand in Leipzig.“ (Anna 22.11.2026). Groß darüber, aber kein H1: „Du bist gut genug. Lass es auch die anderen wissen.“ mit Korrektur „wissen.“ → handschriftlich „sehen!“ (Anna 22.11.2026). Keine Dachzeile.
- Hero „ruhig“ `.kr` (Anna 22.11.2026, Vorbild farbenmeer.de): Zeile oben links in Manrope, blauer Strich durch „wissen.“, „sehen!“ in Annas Handschrift; unten links H1 und ein Textlink „Beratung anfragen →“; rechts unten eine Zeichnung aus dem Set `bilder/zeichnungen-sw/` (derzeit Auge). Keine Fotos, keine bunten Sticker im Hero. Laufband darunter bleibt.
- Zeichnungen schwarz-weiß (Anna 22.11.2026): Strichzeichnungen ohne Farbe und ohne Versatz, Generator `werkzeuge/grafiken/zeichnungen-sw.py` (Auge, Bildschirm, Megafon, Glühbirne, Blitz, Pfeil, Stern, Herz), dekorativ mit `alt=""`.
- Hero links: blaue Fläche mit Frag-Feld und Chips; rechts Diashow (`js/start.js`, Bilder in `bilder/start/`, ab Folie 2 per `data-src` nachgeladen; Fotos in Naturfarben, Leipzig-Bilder nie nebeneinander, Pause-Button, Nachweise im Impressum). Feste Höhe.
- Frag-Feld: sucht nur in kuratierten Themen (`werkzeuge/inhalte/hero-themen.json`: Stichwort-Gruppen, Antwort = eine häufige Frage der Website im Wortlaut; Themen zu Anna aus der Profilseite mit Link zu LinkedIn; ohne Treffer Telefon und Beratung). Nichts wird gesendet. Platzhalter „Warum bringt meine Website keine Anfragen?“, Button „Antwort“, kein Hinweis darunter. Ton freundlich („Ja, klar!“, „Sehr gern!“).
- Chat nach der ersten Frage wie WhatsApp (`js/frag.js`, `.hl-chatfenster`): Überschrift einzeilig, H1 nur noch unsichtbar; Kopfzeile mit Foto und „Anna Härtelt“, Creme-Grund mit Bauhaus-Muster, „Heute“, Frage als blaue Blase rechts mit Uhrzeit und Haken, kurz „schreibt …“, Antwort als weiße Blase links mit rundem Foto, Links als Zeilen in der Blase; neueste Runde unten über dem Feld, höchstens drei Runden. Antwort im Stil der KI-Übersicht bei Google: Kurzfassung, bis zu drei Stichpunkte, Links als Quellen (extern neues Fenster). Konzept: Betrieb `Studio AAH/Website/2026-11-16_konzept_hero-frag-feld.md`.
- Leistungen der Startseite: drei Kernkompetenzen (Markenbildung, Webdesign, KI-Beratung) nebeneinander, Form mittig in der Creme-Fläche, Name zentriert, ohne Unterzeile, am Handy untereinander; Retainer nicht hervorgehoben.
- Projekte: `projekt_liste()` in `inhalte-erzeugen.py`, Feld `kurzleistungen` in `projekte.json` (ohne Plattform-Namen, ohne Flyer). Große Projektkacheln (`projekt_raster()`, Feld `schlagzeile`) nutzen die Branchenseiten. Projektkacheln und Projekt-Karten überall mit schwarzem Grund (`KACHEL_GRUND`); Hausfarbe der Kund:innen nur auf der Projektseite.
- Aktuelles: eigene LinkedIn-Beiträge aus `werkzeuge/inhalte/linkedin.json`, Bilder lokal `website/bilder/linkedin/li-<id>.webp` (640 × 800), nichts von LinkedIn laden, keine Reposts; GIF mit `"datei": "gif"`, spielt beim Hineinscrollen einmal ab.
- Branchen-Mosaik über Marker `BRANCHEN`, Reihenfolge Bau, Software & IT, Handwerk, Energie, Industrie, Beratung (breite Kachel), Gesundheit (`reihenfolge` in `startseite_branchen()`).
- Köpfe von „Wo es gerade hakt“, Projekte, LinkedIn und Stimmen mittig (`sk-mitte`). Stimmen ohne Unterzeile.
- Der alte Leistungs-Slider wird nirgends eingebaut (gesichert in Betrieb `Studio AAH/Website/gestaltung/2026-11-09_hero-slider-leistungen/`); `js/hero.js` ist ungenutzt.
- Letzter Abschnitt der Startseite: nur der blaue Website-Check-Block „Fit für 2027? Finden wir es heraus.“ mit Namen aus dem Hero (Anna 22.11.2026); „Ab Dezember 2026 …“ ist damit entfallen.

## Menü
- Hauptmenü am Desktop mittig zwischen Logo und Button: Leistungen · Branchen · Projekte (Adresse `/referenzen/`) · Über mich · Aktuelles (Adresse `/blog/`).
- Mega-Menüs „Leistungen“ und „Branchen“ (`js/menue.js`, `aria-controls`), über die Inhaltsbreite, mit Bauhaus-Icons (`mm-mit-icon`, 31 px). Menüpunkte in Manrope 600, 18 px, ohne Unterzeile; Karten rechts beige (`mm-karte-beige`) nur mit Dachzeile, Titel (Anton) und Button.
- Leistungen: Kernkompetenzen (Markenbildung, Webdesign, KI-Beratung) · Feste Angebote in der Reihenfolge Marken-Regelwerk, Website-Check, KI-Arbeits-Setup, Retainer · Weitere Leistungen (UI/UX, Marketing & Vertrieb, Employer Branding, Druck, Animation, Illustration & Infografik).
- Branchen-Menü rechts mit dem KI-Arbeits-Setup als Angebot. Mega- und Mobilmenü der Branchen stehen von Hand in `index.html`.
- Leistungs-Formen im Menü sind dieselben Dateien wie auf den Leistungsseiten (`formen/brand|website.svg`, KI seit 22.11.2026 der Zauberstab `symbole/skills.svg`, Anna); Website-Check `symbole/scanner.svg`.

## Fuß
- Kontakt · Leistungen (Kernkompetenzen, Feste Angebote, Weitere, Preise) · Branchen (alle sieben, darunter „Wo es hakt“) · Studio (Über mich, Projekte, Blog, Selbst testen, Initiative). Neue Seiten dort eintragen.

## Stand 22.11.2026 (Anna, geht vor älteren Zeilen)
- Seitentitel „Markenbildung, Webdesign & KI-Beratung in Leipzig | STUDIO AAH!“; H1 kurz „Design Studio aus Leipzig.“; Suchbegriffe stehen in Titel und Beschreibung, nicht im Hero.
- Auge im Hero zwinkert zweimal nach dem Laden (Animation im SVG, `werkzeuge/grafiken/zeichnungen-sw.py`), bei „Bewegung reduzieren“ offen.
- Chat: Name „Anna Härtelt“ nur im Chatkopf, nicht in den Antwortblasen; erste eigene Blase „Hallo, ich bin <Name>.“; im Chat kein Platzhalter, sondern blinkende Schreibmarke (`.fh-marke`).
- Leistungen: Korrekturzeile „Das kann ich für dich machen“.
