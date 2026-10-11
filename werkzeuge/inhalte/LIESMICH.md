# Inhalte mit Schlagworten

Jede Inhaltsart hat eine eigene Datei. Ein Eintrag erscheint automatisch überall, wo sein Schlagwort (tags) passt.

| Datei | Inhalt | erscheint auf |
|---|---|---|
| projekte.json | Referenzen (Name, Branche, Zeitraum, Leistungen, Links) | Startseite (alle), Leistungsseiten (nach Schlagwort) |
| stimmen.json | Kundenstimmen | Startseite, Profil (alle), Leistungsseiten (bis 3 nach Schlagwort) |
| blog.json | Blogartikel (neueste zuerst) | Startseite und Profil (neueste 3), Blogübersicht (alle), Leistungsseiten „Passende Artikel“ (bis 3) |
| kennzahlen.json | Kennzahlen | Startseite, Profil, alle Leistungsseiten |
| faq-gemeinsam.json | Fragen für alle Leistungsseiten | am Ende jeder FAQ |

Schlagworte: brand, ui-ux, website, marketing, print, illustration, motion, retainer, ki (wie die Leistungen), dazu z. B. team, allgemein.

Nach jeder Änderung im Repository-Ordner:
    python3 werkzeuge/inhalte-erzeugen.py
    python3 werkzeuge/leistungsseiten.py
Ein neuer Blogartikel braucht zusätzlich seine eigene Seite unter website/blog/<slug>/.
