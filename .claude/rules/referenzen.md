---
paths:
  - "website/referenzen/**"
  - "website/css/referenzen.css"
  - "website/js/referenzen.js"
  - "werkzeuge/referenzen.py"
  - "werkzeuge/inhalte/projekte.json"
  - "werkzeuge/anleitung-referenzseite.md"
  - "werkzeuge/grafiken/bild/**"
  - "werkzeuge/grafiken/schrift*.swift"
---
# Projektseiten (Referenzen, Case Studies)

- **Vor jeder neuen Referenzseite lesen:** `werkzeuge/anleitung-referenzseite.md`. Vollständige Fassung in Betrieb `Studio AAH/Website/2026-10-15_anleitung-referenzseite.md`.
- **Vor Arbeit an einer bestehenden Projektseite die Notiz in Betrieb lesen:**
  - Bauer: `Kunden Studio AAH/Bauer Ingenieurbau/01_Basics/referenzseite-studio-aah.md`
  - Deinetwegen: `Kunden Studio AAH/Deinetwegen/01_Basics/referenzseite-studio-aah.md`
  - Goldhammer: `Kunden Studio AAH/simone-goldhammer/01_Basics/referenzseite-studio-aah.md`
  - Jana Voigtmann: `Kunden Studio AAH/Studio AAH/Website/referenzen/jana-voigtmann_referenzseite.md`
  - Down to Earth: keine eigene Notiz; keine Lebenselemente-Icons zeigen.
  - In Cloud-Sitzungen ohne Betrieb: nichts an Texten oder Gezeigtem ändern, Anna fragen.
- `referenzen.py` übernimmt Kopf und Fuß von der Profil- bzw. Webdesign-Seite; `referenzen.js` hat dieselbe Version wie `menue.js`.
- Alle Projektseiten werden aus `varianten.b` erzeugt (`hauptvariante: "b"`). Vorlagen: Deinetwegen für Onepager, Bauer für KMU-Websites.
- Aufbau wie Branchenseiten: Inhalt als Ankerleiste (graue Spur, eine weiße Pille), alles linksbündig zum Kopf; Ergebnis-Spalten mit Überschriften und Texten auf einer Höhe. Nur zeigen, was Anna selbst gemacht hat. Projektübersicht ohne Unterzeile unter dem Kartentitel (`satz=False`).
- Typografie überall mit Baustein `designsystem` (Farbkarten, „Aa“, Schriftstufen H1 bis Button mit Werten der Live-Seite). Schriften ohne freie Lizenz nur als Bild je Stufe (`werkzeuge/grafiken/schriftstufen.swift`), freie Schriften lokal als woff2.
- Stopp-Button der Bildschirmwand unten rechts über den Kacheln (`.hw-knopf`). Pause-Tasten über die Hilfsfunktion in `referenzen.js`.
- Farben der Kund:innen erlaubt; Kopf, Fuß, Navigation in Studio-Farben. Anfrage-Button in der schwarzen Abschlussbox blau.
- Keine Mitarbeitenden der Kund:innen zeigen: Ausschnitte mit Personen ersetzen statt weichzeichnen. Vor jeder Veröffentlichung Prüfer-Agent auf Personen, Platzhalter und interne Inhalte.
- Bilder, die keine Seite mehr nutzt, aus `website/` entfernen, sonst sind sie öffentlich abrufbar.
- Bildwerkzeuge (Zusammensetzen, Ausschnitt, Kontaktbogen, Retusche) in `werkzeuge/grafiken/bild/`.
