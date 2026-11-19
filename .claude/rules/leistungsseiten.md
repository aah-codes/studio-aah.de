---
paths:
  - "website/service/**"
  - "website/preise/**"
  - "werkzeuge/leistungsseiten.py"
  - "werkzeuge/leistungen-inhalte.json"
  - "werkzeuge/preise-daten.json"
  - "werkzeuge/preise-erzeugen.py"
  - "werkzeuge/inhalte/prozess.html"
  - "werkzeuge/grafiken/leistungs-formen.py"
---
# Leistungsseiten und Preise

- Leistungsnamen: Markenbildung, UI/UX, Webdesign, Marketing & Vertrieb, Druck, Illustration & Infografik, Animation, Retainer, KI-Beratung. Adressen `service/markenbildung/`, `webdesign/`, `druck/`, `animation/`; KI-Beratung bleibt unter `service/ki-digitalisierung/` (Google). Alte Adressen `brand/`, `website/`, `print/`, `motion-design/` leiten weiter.
- Content-First (Vorbild IT-Sonix-Leistungsseiten): ein Abschnitt je Frage der Besucher:innen, jede Aussage genau einmal. Reihenfolge in `leistungsseiten.py`: Hero (H1, ein Satz, ein Button „Leistung im Überblick“) → „<Leistung>: Was ist das?“ (`zusammenfassung`, daneben „Was Sie davon haben“ (`gewinn`) und „Für Sie, wenn“ (`fuer_sie`, nur mit dem Schlagwort der Zielseite); Überschrift überschreibbar mit `frage`) → Inhaltsleiste (`ankerleiste()`) → Warum (`probleme`; Lösungskarte entfällt, wenn `loesung_text` den Einstieg wiederholt) → Leistung im Detail 01–0n (`loesungen`) → Ablauf mit Abstimmungsterminen (`zl-quer`) → Stimmen → Referenzen mit Kennzahlen → Preise (Pakete, Vergleich, Zusatzleistungen) → Häufige Fragen → Ansprechpartnerin mit Foto, Telefon, E-Mail → Artikel (immer zuletzt).
- Webdesign hat die Sektion `#selbst` (Feld `selbstbau`) und die Spiel-Sektion (Feld `spiel`).
- Leistungs-Icons (`werkzeuge/grafiken/leistungs-formen.py` → `website/bilder/formen/<id>.svg`, eingetragen in `leistungen-inhalte.json`) in Schwarz, Weiß und Blau; Blau berührt nie Schwarz. Markenbildung Zielscheibe (blauer Kreis, weißer Ring, schwarzer Punkt), Webdesign blaues Quadrat zwischen zwei gleich breiten schwarzen Balken, KI-Beratung blauer Stern mit kleinem schwarzem Stern. Das Icon steht über der Dachzeile (`lsx-kopf-icon`) und schwebt.
- Referenz Bauer nur auf Startseite, Webdesign und Branche Bau (plus Projektübersicht, Projektseite, Impressum); auf anderen Seiten keine Referenz statt Bauer (`ohne_bauer()`).
- Preise: zwei Paketkarten je Gruppe (Regel `gestaltung.md`). Gezeigt: Markenbildung Medium + Premium, UI/UX Audit Pro + Redesign kleine Webanwendung, Marketing LinkedIn + Post-Vorlagen, Druck Flyer + Unternehmenspräsentation, KI KI-Check + KI-Arbeits-Setup (Preisseite; die KI-Seite zeigt nur das Setup), Regelwerk Start + Team (Pflege als `mr-zusatz`).
- Offen: Prozess `werkzeuge/inhalte/prozess.html` an die neuen Schritte angleichen; Ausstieg nach Schritt 02 in Angebote und AGB übernehmen.
