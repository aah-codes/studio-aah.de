---
paths:
  - "werkzeuge/**"
---
# Generatoren im Einzelnen

Normalfall: `bash werkzeuge/alle-erzeugen.sh` (Reihenfolge steht im Skript: Kopf und Fuß → Preise → Blog → Inhalte → Leistungsseiten → Website-Check → Marken-Regelwerk → KI-Team-Setup (`ki-arbeits-setup.py`) → Referenzen → Für wen → Brotkrumen → Fragen-Index). Einzeln nur, wenn man genau weiß, was man tut.

- `kopf-fuss.py` – Kopf und Fuß aus `website/index.html` in alle Seiten (Pfade nach Ordnertiefe, 404 ab der Wurzel). Kopf und Fuß nur in `website/index.html` ändern.
- `preise-erzeugen.py` – Preise, Kostenrechner-Daten, Leiste (`KATEGORIEN`, `BEISPIELE`; derzeit auf keiner Seite), Glossar, Leistungen der Startseite (`start_leistungen()`).
- `blog/<slug>.py` – je Beitrag, ruft `bauen()` aus `blog/beitrag.py` (siehe Regel `blog.md`).
- `inhalte-erzeugen.py` – Projekte, Stimmen, LinkedIn, Kennzahlen über Marker `<!-- NAME:START -->` … `<!-- NAME:ENDE -->`. Läuft nach dem Blog (liest die Lesezeit). Kennzahl „Jahre selbstständig“ aus `"seit": 2020` in `inhalte/kennzahlen.json`: nach dem Jahreswechsel einmal alle Generatoren laufen lassen und hochladen.
- `leistungsseiten.py` – `website/service/` aus `leistungen-inhalte.json` und `preise-daten.json`, Prozess aus `inhalte/prozess.html`; Kopf und Fuß bleiben aus der bestehenden Seite.
- `referenzen.py` – `website/referenzen/` aus `inhalte/projekte.json`; Bild-Versionen `?v=` aus dem Dateiinhalt.
- `fuer-wen-seiten.py` – `/fuer-wen/`, Problemseiten, Branchenseiten, Produktseite, Selbsttest, KI-Zeitrechner aus `inhalte/fuer-wen-seiten.json`. Neue Seiten auch in `website/sitemap.xml`.
- `fragen-index.py` – `daten/fragen.json` für das Frag-Feld der Startseite.
- `website-check.py`, `marken-regelwerk.py`, `ki-arbeits-setup.py` – die gleichnamigen Angebotsseiten.
- `brotkrumen.py` – Brotkrumen und BreadcrumbList auf Unterseiten. Neue Unterseiten dort eintragen.
- Grafik- und Bildwerkzeuge unter `werkzeuge/grafiken/`: siehe Regel `bilder.md`.
- Gemeinsame Hilfsfunktionen (Pfade, `esc`, `euro`, `einsetzen`, Seitenrahmen, Bildmaße, Paketkarte, `ankerleiste()`, Papierriss, Kringel) nur in `gemeinsam.py`. Ersetzungen brechen mit Meldung ab, wenn ein Marker fehlt.
