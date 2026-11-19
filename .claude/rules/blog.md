---
paths:
  - "werkzeuge/blog/**"
  - "website/blog/**"
  - "website/audio/**"
  - "website/downloads/**"
---
# Blogbeiträge (Aktuelles)

- Jeder Artikel nach demselben Schema: `werkzeuge/blog/<slug>.py` ruft `bauen()` aus `werkzeuge/blog/beitrag.py` (Kopf/Fuß, Kurz gesagt, FAQ, strukturierte Daten). **Vor jedem neuen Beitrag lesen:** `werkzeuge/blog/schema-blogbeitrag.md`; Schreibregeln im Skill `texte-studio-aah`. Texte nur in `<slug>-inhalt.html` und der FAQ im Skript ändern.
- Neue Beitrags-Skripte in `werkzeuge/alle-erzeugen.sh` eintragen (vor `anhoeren-einsetzen.py`). Beispiele: `was-kostet-eine-website.py` (Reihe Website-Fragen, Teil 1), `was-sollte-eine-website-2027-koennen.py` (Teil 2), `eu-ai-act-kleine-unternehmen.py` (Kategorie KI-Beratung; Titelbild aus `werkzeuge/grafiken/blog/eu-ai-act-titel.py` mit Natural-Earth-Daten; Checkliste als PDF aus `werkzeuge/blog/eu-ai-act-checkliste.py` nach `website/downloads/`).
- Leselayout (`_raster` in `beitrag.py`, „Leselayout“ in `stil.css`): Kopf zweispaltig (Text links, Bild rechts), ab 1200 px links Kapitel-Leiste mit kleinen Punkten und Fortschritt, rechts Thema und ähnliche Artikel, beide bis an den Rand; Brotkrumen fein (Start / Aktuelles / Kategorie / Artikel, 12 px).
- „Artikel anhören“ nur als Aufnahme mit echt klingender Stimme (`website/audio/<slug>.mp3`), kein Tempo.
- Je Abschluss nur ein Button. Viel Weißraum. Kästen nur `box-tipp` („Tipp & Wissenswertes“, Creme, Titel „Tipp: …“ oder „Wissenswert“) und `box-achtung` („Wichtiger Hinweis“: Gesetz, Pflicht). Vergleiche als `table.vergleich` (Kriterien als Zeilen, erste Spalte steht beim Wischen). Nummerierte Listen ohne hervorgehobene erste Zahl.
- Keine LinkedIn-Meme-Vorlagen: nur einzelne Bilder, zwei nebeneinander oder Mosaik. Bildsprache (Entwurf): Betrieb `Studio AAH/2026-11-17_bildkonzept_ki-bildsprache.md`.
- Blog-Kategorien als Ankerleiste wie auf den Leistungsseiten. Unten auf `/blog/` steht die Spiel-Sektion (Marker `SPIEL`).
