# Anleitung: Referenzseite (Case Study) erstellen

Stand: 15.10.2026 · Vorbilder: `/referenzen/bauer/` (KMU-Website) und `/referenzen/deinetwegen/` (Onepager)

Diese Datei ist öffentlich (Repository). Sie enthält nur Technik, Gestaltungs- und Prüfregeln. Kundeninterna, Briefings und die vollständige Recherche liegen in `Betrieb` unter `Kunden Studio AAH/Studio AAH/Website/`:
- `2026-10-15_anleitung-referenzseite.md`: diese Anleitung plus Briefing der nächsten Referenz
- `2026-10-15_recherche_beste-referenz-bauer.md`: 25 Case Studies mit Quellen

---

## 1. Ziel und Maßstab

Jede Referenz soll die beste sein, die man für diesen Kunden machen kann (Anna, 15.10.2026). Sie muss leisten:
- **informativ für Annas Zielgruppe:** KMU, Bauunternehmen, Ärzt:innen. Sie muss ohne Gespräch überzeugen, denn Entscheider recherchieren vor allem allein.
- **Storyline und Storytelling:** Der Kunde ist der Held, Anna die Begleiterin mit Plan.
- **Gestaltung:** in den Farben der Kund:innen (Ausnahme von der Studio-Farbregel); Kopf, Fuß und Navigation bleiben in Studio-Farben.
- **Umsetzung:** Desktop, Mobil (bis 320 px) und barrierefrei. Barrierefreiheit belegen, nicht nur behaupten.

## 2. Ablauf in Schritten

### Schritt 0 – Vorbereiten (vor jeder Gestaltung)
1. **Material sammeln** aus dem Kundenordner in `Betrieb`:
   - Aufnahmen der Website
   - Corporate Design
   - Protokolle, Ziele, Angebot (für die Leistungen)
2. **Nutzungsrecht prüfen:** Vertrag oder AGB. Bei Bauer gibt es dazu eine eigene Prüfung im Kundenordner.
3. **Klären und freigeben lassen:**
   - Kundenzitat: nur mit Freigabe, Name und Rolle.
   - Ergebniszahlen: nur belegte, mit Stand-Datum.
   - Annas Rolle oder Credits.
   - Zeitraum.
4. **Personen:** keine Mitarbeitenden der Kund:innen zeigen, solange es nicht ausdrücklich erlaubt ist.
   - Abschnitte mit Personen weglassen oder ersetzen, nicht weichzeichnen; Flecken wirken schlecht.
   - Symbolbilder (z. B. Personas) als „Symbolbilder“ kennzeichnen.

### Schritt 1 – Storyline festlegen
Schablone (bewährt bei Bauer, abgeleitet aus der Recherche):

| Teil | Inhalt |
|---|---|
| Kopf | Name (H1), **ein Einleitungssatz** mit der Kernaussage, Steckbrief (Branche, Leistungen, Zeitraum, Website ↗) |
| Bühne | ein starkes Bild als Einstieg (Bauer: laufende Wand aus Sections, Startseite fest mittig, Pause-Taste) |
| Kennzahlen | höchstens 3, davon möglichst eine **Wirkung** (z. B. „13 Bewerbungen seit dem Launch“), nicht nur Mengen |
| Inhaltsverzeichnis | Sprungmarken zu den Kapiteln |
| Ausgangslage | Herausforderung und Ziele (gleich viele Punkte), Vorher kurz (nur Vorher-Szenen, kein Nachher) |
| Konzept | Struktur und Weg (Sitemap, Navigation, Funnels); jeder Schritt mit einer Entscheidung: „herausgefunden … darum …“ |
| Wege je Zielgruppe | bei zwei Zielgruppen je ein Kapitel: Persona, Funnel, Beleg (Bauer: Auftraggeber „Sie“, Bewerber „Du“) |
| Gestaltung | Herleitung aus dem Gegenstand, Style Guide, Favicon, wichtigste Muster |
| Ergebnis | **jedes Ziel vom Anfang einzeln beantwortet**, Kundenstimme (falls freigegeben), Credits, Abschluss für die Zielgruppe mit Anfrage-Knopf |
| Ende | „Nächstes Projekt“ (automatisch) |

- Kapitelüberschriften groß, schwarz, **ohne Nummer**.
- Dachzeilen kurz.
- Jede Information nur einmal: dieselben Bildschirme nicht mehrfach zeigen.

### Schritt 2 – Aufnahmen
- `python3 werkzeuge/grafiken/seiten-aufnahme.py ZIEL URL … [--handy] [--abschnitte "CSS"] [--js "Code"] [--felder]`
  - Desktop in doppelter, Handy in dreifacher Auflösung.
  - Abschnitts-Lage in `aufnahmen.json` in CSS-Pixeln.
  - Eigenen Port mit `AUFNAHME_PORT`, wenn zwei Aufnahmen gleichzeitig laufen.
  - Aufnahmen gehören nicht ins Repository; nur ausgewählte Ausschnitte verkleinert übernehmen.
- Werkzeuge in `werkzeuge/grafiken/bild/` (Swift, `swiftc -O -o NAME NAME.swift` oder `swift NAME.swift …`):

| Werkzeug | Aufgabe |
|---|---|
| `stitch` | Seitenansicht aus Kopf und ausgewählten Abschnitten zusammensetzen (z. B. ohne Abschnitte mit Personen) |
| `ausschnitt` | Rechteck ausschneiden und verkleinern |
| `kontakt` | Kontaktbogen vieler Bilder zum Durchsehen |
| `reihe` | Bilder nebeneinander vergleichen |
| `stempel` | Retusche: Fläche weich mit einer Fläche daneben überdecken (z. B. eine kleine Figur im Hintergrund) |
| `anonym` | ganzes Bild unlesbar machen (nur Notlösung; besser weglassen) |

- Weitere: `werkzeuge/grafiken/unkenntlich.swift`, `heft-druck.swift`, `schriftmuster.swift` (Schriftmuster als PNG, wenn die Schriftlizenz keine Weitergabe der Datei erlaubt, z. B. Satoshi; Repository nur SIL OFL).
- **Schärfe:** Quellbild mindestens doppelt so breit wie angezeigt.
- **Mockups (Anna, 15.10.2026):** nur hochwertige, echte Foto-Mockups moderner Geräte (z. B. silberner Laptop, Canva-Mockups oder Mockuptree, Lizenz gewerblich, Nachweis im Impressum). Keine gezeichneten/CSS-Geräte, keine KI-Bilder. Gerät nach Zielgruppe der Kund:innen wählen (Anna, 15.10.2026): Wie schauen deren Besucher:innen auf die Website? HR/B2B (z. B. Deinetwegen) → moderner Apple-Standrechner (iMac) im Hero; Behörden/öffentliche Auftraggeber (z. B. Bauer) → schwarzer Büromonitor mit dunklem Standfuß, hochmodern, kein iMac; Ärztinnen (z. B. Simone) → vor allem Handy; Kreative (z. B. Jana) → Laptop und Handy.

### Schritt 3 – Daten und Generator
- **Einstieg überall gleich (Anna, 15.10.2026, Blueprint Deinetwegen):** H1 ohne Einleitung → Bühne → Überblick (Aussage + Leistungen) → Inhalt → Ausgangslage (zwei Karten + Ziele). Kennzahlen gehören ins Ergebnis. Überschriften schwarz; Projektfarben über `stil`.
- **Vorlagen (Anna, 15.10.2026):** Referenzseiten funktionieren wie ein CMS – wiederkehrende Bausteine, nur die Inhalte wechseln.
  - **KMU-Websiteprojekt** (mehrere Seiten, zwei Zielgruppen): Variante `b` von **Bauer** kopieren.
  - **Onepager** (auch mit Blog): Variante `b` von **Deinetwegen** kopieren. Nächste Anwendung: **Jana Voigtmann**.
  - Kopieren heißt: Liste `varianten.b` übernehmen, Texte, Bilder und Projektfarben (`stil`) tauschen; Bausteine, die nicht passen, weglassen.
- **Daten:** `werkzeuge/inhalte/projekte.json`, Generator: `werkzeuge/referenzen.py`. Erzeugte Seite: `website/referenzen/<slug>/`.
- **Varianten:**
  - `varianten.<k>` ist eine Liste aus:
    - `{"projekt": {...}}`: überschreibt Projektfelder, z. B. `buehne_wand`, `zahlen`, `einleitung`;
    - `{"aus": n, "setze": {...}, "ohne": [...], "band": {...}}`: übernimmt Block n der Grundfassung `bilder`;
    - eigene Blöcke.
  - Eine Variante erscheint unter `/<slug>-<k>/` mit noindex.
  - Mit `"hauptvariante": "<k>"` wird sie die Projektseite: normale Adresse, sichtbar für Suchmaschinen. `varianten_ablage` parkt Blöcke.
- **Bänder** (nur in Varianten, „Seamless“):
  - Jeder Block liegt in `nl-band` mit `von` und `bis` (Farben).
  - Arten: `schraege` (Kundenschräge), `blau`, `raster`, `eng`, `voll`, `figma`.
  - Ein Kapitel direkt vor einer Schräge bekommt automatisch mehr Abstand.
- **Projektfarben** (in `{"projekt": {...}}` der Variante): `klasse` (z. B. `cs-deinetwegen`) und `stil` mit CSS-Variablen `--pc-dunkel`, `--pc-akzent`, `--pc-zweit`, `--pc-hell`, `--pc-meta-dunkel` (Dachzeile auf dunklem Grund, Kontrast ≥ 4,5 : 1 prüfen), `--pc-marke` (erste/letzte Marke der Zeitleiste). Band-Art `dunkel` = weiße Schrift auf dunklem Band.
- **Bühnen:** `buehne_wand` (Bauer), `buehne_bild`, `buehne_laptop` (Laptop mit Startseite auf dem Markenverlauf, Logo oben links; Deinetwegen).
- **Bausteine** (`typ`):
  - **Kapitel und Rahmen:** `kapitel` (mit `anker`), `inhalt`, `ueberblick` (große Aussage + Leistungsspalte), `kennzahlen` (eigener Block, z. B. im Ergebnis), `ergebnis` (Option `stimme: true` = Kundenstimme daneben)
  - **Ausgangslage:** `hl-karten` (zwei Karten mit Aussage `text` oder Liste `punkte`, darunter `ziele` nummeriert), `ziele-text`, `ziele-grafik`, `storyfilm` (Option `monitor`; Notizen `[Text, x, y, ms, "wichtig"]`), `vorher-nachher`, `film-vergleich`
  - **Konzept und Wege:** `sitemap`, `personas`, `funnel-karte`, `weg`, `klickstrecke`, `ablauf` (Option `spalten: 1` bei wenigen Schritten), `mega-film`
  - **Gestaltung:** `marke` (Logos; Farben und Schriftbild optional), `designsystem`, `visual-design`, `stil`, `tabelle`
  - **Typografie auf allen Referenzseiten wie bei Bauer (Anna, 16.10.2026):** Baustein `designsystem` mit Farbkarten, „Aa“-Karte und Schriftstufen (H1 bis Button) mit den Werten der Live-Seite (Größe / Zeilenhöhe · Gewicht, im Browser auslesen). Freie Schrift (SIL OFL, z. B. Inter, Montserrat): als woff2 nach `website/schriften/`, `@font-face` in `stil.css`, Stufen als Text. Schrift ohne freie Lizenz (Satoshi, Helvetica): Proben als Bild mit `werkzeuge/grafiken/schriftstufen.swift` (`"einzeln": true`, `"breite": 456`), Stufe als `[Name, Maß, Bild, Alternativtext]`, „Aa“ mit `nur_aa` als `aa_bild`. Anführungszeichen in `stufen`-Stilen nur einfach (`'Helvetica Neue'`).
  - **Bilder:** `langaufnahmen` (ganze Seite Rechner + Handy nebeneinander, gleich hoch, unbewegt), `seiten-pillen` (weitere Seiten versetzt mit Pillen und Pfeil), `buehne`, `galerie`, `geraete`, `handys`, `handy-duo`, `fotofilm` (Option `dazu` = zweites Gerät), `heft`, `figma`, `bento`, `raster`, `split`, `stapel`, `vollbild`, `zwei-karten`, `cta-wand`, `karriere`
  - **Text:** `texte`, `section`, `schieber`
- **Danach:**
  - alle Generatoren laufen lassen (`CLAUDE.md`);
  - nach CSS- oder JS-Änderungen die Cache-Version `?v=` erhöhen;
  - `bash werkzeuge/pruefen.sh`.

### Schritt 4 – Prüfen (vor jedem Melden und vor jedem Push)
**Technik**
- [ ] Desktop 1440, Handy 390 und **320 px**: kein seitliches Verschieben; auch keine Kästen, die innen unsichtbar seitlich scrollen (z. B. Sitemap).
- [ ] Alle Bilder laden. **Bilder, die keine Seite mehr nutzt, aus `website/` löschen**, sonst sind sie öffentlich abrufbar.
- [ ] Schriften im Style Guide wirklich geladen. Werte mit Anführungszeichen in `style`-Attributen maskieren (`&quot;`); `esc()` maskiert sie nicht.

**Gestaltung und Barrierefreiheit**
- [ ] Alles, was sich von selbst bewegt, hat eine Pause-Taste oder hält nach 5 s an. Bei `prefers-reduced-motion` steht es still, und Knöpfe ohne Funktion sind ausgeblendet.
- [ ] Genau eine H1, Überschriften ohne Sprünge, Sprungmarken haben Ziele, Alternativtexte sinnvoll.
- [ ] **Satzzeichen und Umlaut-Punkte berühren sich nie:** Versal-Überschriften in Anton mit Zeilenabstand mindestens 1,15, bei Umlauten 1,2.
- [ ] Dachzeilen lesbar: Gelb nur auf Blau oder Schwarz. **Kein Blau auf Schwarz** (auch kein blauer Knopf).

**Inhalt**
- [ ] Jeder neue Text gegen die Quelle gelegt; nichts dazuerfinden; Vorschläge als „Textvorschlag – Freigabe Anna“ melden.
- [ ] Keine Personen (siehe Schritt 0), keine internen Platzhalter („[… ergänzen]“), keine Preise, nichts darüber, wie studio-aah.de gebaut oder gehostet ist.

**Freigabe**
- [ ] **Prüfer-Agent vor dem Push:** Personen, Platzhalter, interne Inhalte, Texte gegen Quellen. Er findet regelmäßig etwas, was die eigene Prüfung übersehen hat.
- [ ] Vorschau öffnen (`http://localhost:8123/referenzen/<slug>/`) und die Adresse nennen.

### Schritt 5 – Veröffentlichen
- Lokal committen; **Anna pusht selbst**, jeder Push auf `main` geht sofort live. Erst nach dem Prüfer-Ergebnis pushen.
- Danach live prüfen: Personen, Platzhalter, Bilder.

## 3. Erkenntnisse aus der Recherche (25 Case Studies, 15.10.2026)

**Was fast alle machen**
- Kopf mit Name, Satz und Leistungen, dann ein großes Bild.
- Bogen Ausgangslage → Strategie → Gestaltung → Ergebnis.
- 270–460 Wörter, Bilder machen 65–95 % der Seite aus.
- Höchstens ein Kundenzitat, 3 große Zahlen, am Ende „nächstes Projekt“.

**Was fast niemand macht – Annas Alleinstellung**
- Vorher-Zustand zeigen
- Prozess als Bild (Personas, Sitemap, Zeitleiste)
- Click-Funnel und Bewerbungsweg
- zwei Zielgruppen als zwei Wege erzählen
- Ziele einzeln beantworten
- Inhaltsverzeichnis mit Sprungmarken
- Abschluss für die Zielgruppe
- wirklich barrierefrei (fast alle anderen: Bilder ohne Alternativtext, Videos ohne Pause, mehrere H1)

**Storyline**
- Wichtigstes zuerst (umgekehrte Pyramide): In 10–20 s entscheidet sich, ob jemand bleibt; 57 % der Blickzeit entfallen auf den ersten Bildschirm.
- Jeder Prozessschritt hängt an einer Entscheidung.
- Wendepunkt sichtbar machen.
- Ergebnis an die Anfangsziele knüpfen, ehrlich mit Stand-Datum.

**Bewegung**
- Auf B2B-Seiten keine Wartezeit durch Animation.
- Nichts, was beim Scrollen die Kontrolle übernimmt (kein Scrolljacking).
- Bewegung nur mit Pause.

**Glaubwürdigkeit**
- Überprüfbare Details, echte Fotos, Namen, Zahlen mit Bezug.
- Ein Steckbrief wie eine Vergabe-Referenz (Leistung, Zeitraum, Empfänger) wirkt auf Bau-Kunden vertraut.

**Zielgruppe der Kund:innen ernst nehmen**
- Echte Menschen und Orte zeigen statt Stockfotos, solange Personen erlaubt sind.
- Einen Sinn-Satz zur Arbeit zeigen.

## 4. Häufige Fehler (aus dem Bauer-Projekt)

| Fehler | Regel |
|---|---|
| Push vor dem Prüfer-Ergebnis; danach waren Platzhalter und eine Person live | erst Prüfer, dann Push |
| Druck-Entwurf mit Platzhaltern auf der Website | Druckseiten erst nach Abnahme zeigen |
| Weichgezeichnete Personen als graue Flecken | Abschnitte ersetzen, kleine Figuren per `stempel` retuschieren |
| Nicht mehr verlinkte Bilder blieben öffentlich | unbenutzte Dateien löschen |
| Zu viele Wiederholungen derselben Bildschirme, Ergebnis zu früh, Ende zu schwach | Schablone aus Schritt 1 |
| CSS-Gitter mit `grid-auto-flow: column` ignorierte Spaltenangaben | `grid-auto-flow: row` mitsetzen |
| Zahlen ohne Beleg („Mehr Bewerbungen“, „in 60 Sekunden“) | streichen oder belegen |

## 5. Begriffe

- **Seamless Presentation** (auch Continuous Scrolling, Behance): Die Projektseite wirkt wie ein einziges langes Bild ohne Kanten. Im Generator umgesetzt als Varianten mit Bändern (`nl-band`).
- **Click-Funnel:** der Weg einer Zielgruppe von der Einstiegsseite bis zur Anfrage oder Bewerbung.
