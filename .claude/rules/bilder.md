---
paths:
  - "website/bilder/**"
  - "werkzeuge/grafiken/**"
---
# Bilder, Mockups und Grafik-Werkzeuge

## Format
- Bilder in `website/bilder/`, für das Web verkleinern, `website/` klein halten.
- WebP, höchstens 250 KB; Schärfe geht vor. JPG bleiben: lange Seitenaufnahmen (höher als 2,5 × breit), Vorschaubilder `og:image`, Bilder, die als WebP nicht ohne sichtbaren Verlust unter 250 KB kommen. Umwandeln nur mit Prüfung (SSIM ≥ 0,985 je Farbkanal, Stichprobe in doppelter Vergrößerung). JPGs verlustfrei mit `jpegtran -copy icc -optimize -progressive`.
- Quellbilder mindestens doppelt so breit wie angezeigt. Website-Screenshots aus `website/bilder/referenzen/` (1440 px breit).

## Mockups
- Nur hochwertige, echte Foto-Mockups moderner Geräte; keine gezeichneten oder per CSS nachgebauten Geräte, keine KI-Bilder. Lizenz für gewerbliche Nutzung (z. B. Canva, Mockuptree, Bendito Mockup), Nachweis im Impressum unter „Bildnachweise“. Foto-Mockups in `website/bilder/mockups/` (Inhalt per `matrix3d`).
- Gerät nach den Besucher:innen der Kund:innen: HR/B2B iMac, Behörden schwarzer Büromonitor, Ärztinnen vor allem Handy, Kreative Laptop und Handy.

## KI-Bilder (Bildwelt A)
- `bash werkzeuge/grafiken/bildwelt-a.sh ROH.png ZIELORDNER NAME FORM`: aus einem KI-Rohbild (Canva) vier WebP-Formate (1200×800, 1200×630, 1080×1080, 1080×1350), Blau auf `#2a5fe6` angeglichen, Bauhaus-Form (`kreis`, `halbkreis`, `dreieck`) auf der ruhigen Seite oder `keine` für Branchenbilder (Schwarz-Weiß, Blau 40–60 % der Fläche, Werkzeug meldet den Anteil). Keine Kennzeichnung in der Datei (nur mit `KENNZEICHNUNG=1`, z. B. Social Media).
- Auf der Website: jedes KI-Bild mit Menschen bekommt ein sichtbares „KI“-Label per CSS in der Bildecke und „KI-generiert“ im Alternativtext (AI Act Art. 50 Abs. 4; Impressum oder Metadaten allein reichen nicht; Details Bildkonzept Abschnitt 11 in Betrieb).
- Rohbild nie verändern (Canva-Bedingungen: Herkunftsdaten nicht entfernen); jedes WebP bekommt per `c2patool` (`~/bin`) die Herkunftskette (`bildwelt-herkunft.json`, ohne Vorschaubilder laut `bildwelt-herkunft.toml`), bisher mit Testzertifikat. Kein Bild aus Bildwelt A ohne diese Daten veröffentlichen. Rohbilder, `sets.json` und Sets in Betrieb `Studio AAH/Bildwelten/`, nie im Repository; ins `website/` erst, wenn eine Seite das Bild nutzt.

## Icons und Formen
- Icon-Regeln: `gestaltung.md`. 3D-Fassung: `bash werkzeuge/grafiken/icons-3d.sh ZIELORDNER website/bilder/symbole/<name>.svg …` (Blender auf dem MacBook; Kamera 12° von oben, Licht oben links, ohne Schatten, `SCHATTEN=1` holt ihn zurück; 1024 px). 3D nur als Beispiel im Marken-Regelwerk (`website/bilder/marken-regelwerk/3d/`, 480 px WebP); nicht im Hero, nicht auf LinkedIn. Rezepte: Betrieb `Studio AAH/Bildwelten/icon-system/`.
- Clay-Icons: siehe `gestaltung.md` („Einzelne Seiten“).

## Weitere Werkzeuge
- `fotostudio.py` – Porträts mit blauer Studiowand (Entwurf). Freistellen mit `freistellen.py`; Farb-Originale nie ins Repository. Fotostil: Farbfoto, Wand in Markenblau wie im Studio ausgeleuchtet, Kleidung in Blautönen, Gesicht in echter Farbe.
- `bild/varianten.sh` – kleine Fassungen langer Seitenaufnahmen (`<bild>-<breite>.webp`) für `srcset` über `bild_attr()`; braucht `sips` und `cwebp` (`~/bin`). Danach alle Generatoren.
- `bild/startseite-varianten.sh` – kleine Fassungen für die Startseite (Diashow 640/960, Fokus-Karten 640, Icons 96, rundes Porträt 192), in `index.html` von Hand per `srcset`/`sizes` (Diashow ab Folie 2 per `data-srcset`). Neues Bild dort: Variante ergänzen, sonst lädt das Handy das Original (PageSpeed 19.11.2026).
- Nie Einrasten (`scroll-snap`) mit Innenabstand ohne passendes `scroll-padding`: die Spur rastet beim Laden ein, Chrome wertet das als Scrollen und PageSpeed meldet keinen LCP (NO_LCP, 19.11.2026).
- `druck-mockup.py PFAD/schreibtisch.jpg` – Druck-Mockup Visitenkarten; Foto nicht im Repository.
- Musterbericht des Website-Checks (8 Seiten, Layout wie die echten Berichte seit 18.11.2026): `pruefbericht/musterbericht.html`. Ohne Playwright: Chrome `--headless=new --print-to-pdf`, dann `swift pruefbericht/pdfseiten.swift PDF ORDNER 2.5` und `swift pruefbericht/faecher.swift ZIEL.png ORDNER` (aufgefächert: Seiten 1, 2, 3, 7, 8, alle sichtbar, nichts angeschnitten), dann sips + cwebp → `website/bilder/website-check/pruefbericht-mockup*.webp` (2400, 1200, 1200-640). Mit Playwright weiter `rendern.py`. Immer mit erfundener Website (Platzhalter wie „Mustermann“), nie mit einer echten; kein Hinweis wie „erfunden“ oder „Beispiel“; PDF nicht ins Repository.
- `ci-film.py` – CI-Grafik (`corporate-identity.html`): steht sofort fertig, nur die Punkte laufen dauerhaft (`data-dauerhaft`, Pause-Taste sichtbar).
