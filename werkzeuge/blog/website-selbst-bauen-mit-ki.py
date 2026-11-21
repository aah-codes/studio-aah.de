# Baut website/blog/website-selbst-bauen-mit-ki/index.html mit dem gemeinsamen Baustein werkzeuge/blog/beitrag.py.
# Text nach Annas Freigabe vom 17.11.2026 („Okay, das passt alles so … dann können wir den Artikel hochladen“);
# Entwurf mit Quellen und Prüfvermerken: Betrieb › Studio AAH › Website › 2026-11-17_blogbeitrag-entwurf_website-selbst-bauen-mit-ki.md.
# Bilder: Titel/Vorschau aus werkzeuge/grafiken/blog/website-selbst-bauen-titel.py, Memes aus Annas Serie „Lacher v3“ (Fotos Pexels, Nachweis im Impressum).
# Aufruf im Repository-Ordner: python3 werkzeuge/blog/website-selbst-bauen-mit-ki.py
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from beitrag import bauen

faq = [
("Kann ich als Laie meine Website mit KI selbst bauen?",
 "Ja. Baukästen im Browser wie Lovable oder Base44 brauchen weder Programmierkenntnisse noch eine Installation. Nach der Erfahrung von Anna Härtelt von STUDIO AAH! braucht man beim ersten Mal für mehrere Unterseiten mindestens eine Woche."),
("Was ist Vibe-Coding?",
 "Vibe-Coding heißt, eine Website oder Software zu bauen, indem man der KI in normaler Sprache sagt, was man will. Die KI schreibt den Code, der Mensch gibt Richtung und Rückmeldung."),
("Welches KI-Werkzeug ist für Anfänger am besten?",
 "Für den Einstieg eignen sich Lovable oder Base44, weil Bauen und Veröffentlichen an einem Ort passieren. Claude Code passt eher zu Fortgeschrittenen, die auf dem eigenen Rechner arbeiten und den Hoster selbst wählen wollen."),
("Was kostet es, eine Website mit KI selbst zu bauen?",
 "Laut den Preisseiten der Anbieter im November 2026 kosten die bezahlten Tarife umgerechnet etwa 15 Euro (bei Jahreszahlung) bis 27 Euro im Monat, meist zuzüglich Mehrwertsteuer. Hinzu kommen eine Domain für etwa 10 bis 12 Euro im Jahr und, je nach Weg, das Hosting."),
("Ist KI-generierter Code sicher?",
 "Nicht automatisch. In der Untersuchung „GenAI Code Security Report“ von Veracode aus dem Jahr 2025 hatte fast die Hälfte der KI-Lösungen eine bekannte Sicherheitslücke. Vor dem Livegang lohnt deshalb die Sicherheitsprüfung, die viele Werkzeuge mitbringen."),
("Was ist der Unterschied zwischen Domain und Hosting?",
 "Die Domain ist die Adresse, unter der man deine Website findet. Das Hosting ist der Speicherplatz auf einem Server, von dem aus die Website ausgeliefert wird. Verbunden werden beide über DNS-Einträge."),
("Darf ich meine Firmenwebsite kostenlos bei GitHub Pages oder Vercel hosten?",
 "Für Vercel nein, für GitHub Pages ist es ein Graubereich. Laut den Nutzungsbedingungen von Vercel ist der kostenlose Tarif nur für private Zwecke erlaubt. GitHub schließt aus, Pages als kostenloses Hosting für ein Online-Geschäft, einen Shop oder Seiten zu nutzen, die vor allem Geschäfte abwickeln; ob eine reine Firmen-Visitenkarte darunter fällt, ist offen."),
("Muss ich KI-Bilder auf meiner Website kennzeichnen?",
 "Bei Bildern, die echt wirken sollen, ja: Der EU AI Act verlangt seit dem 2. August 2026, solche Deepfakes offenzulegen. Laut eRecht24 kann auch das Wettbewerbsrecht eine Kennzeichnung verlangen, wenn Kund:innen sonst getäuscht würden. Bei Rechtsfragen hilft eine Kanzlei."),
("Wie groß dürfen Bilder und Videos auf einer Website sein?",
 "Anna Härtelt von STUDIO AAH! empfiehlt als Faustwert Bilder im Format WebP mit höchstens 250 KB und Videos mit höchstens 5 MB. So bleibt auch eine lange Seite am Handy schnell."),
("Wer hilft mir, wenn ich beim Selbstbauen nicht weiterkomme?",
 "Anna Härtelt von STUDIO AAH! in Leipzig begleitet Selbstbauer:innen vor dem Start, mittendrin und nach dem Livegang. Sie hilft stundenweise nach Aufwand für 50–85 € netto pro Stunde je nach Unternehmensgröße; den Website-Check gibt es kostenlos."),
]

bauen('website-selbst-bauen-mit-ki',
      titel='Website selbst bauen mit KI: Anleitung für Einsteiger',
      h1='Website selbst bauen mit KI: Wie geht das, und was brauche ich dafür?',
      beschr='Vibe-Coding Schritt für Schritt: Werkzeuge im Vergleich, Zeit und Kosten, sauberer Code, Domain und Hosting, Recht und Checkliste vor dem Livegang.',
      datum='2026-11-17', geaendert='2026-11-17',
      bild='blog-website-selbst-bauen.webp', og_bild='blog-website-selbst-bauen-og.jpg',
      og_alt='Titel „Website selbst bauen mit KI“ neben einem Browserfenster, in dem eine Website aus Bauhaus-Grundformen entsteht, und dem Ausruf „OHO!“.',
      keywords=["Website selbst bauen mit KI", "Vibe-Coding", "KI-Design", "Lovable", "Base44", "Claude Code", "Domain und Hosting", "Website-Check", "Webdesign Leipzig"],
      faq=faq, ohne_figuren=True,
      ersetzen={'ALT_TITELBILD': 'Figur aus Bauhaus-Grundformen zeigt auf ein Browserfenster, in dem eine Website aus Grundformen entsteht. Ein blaues Quadrat fliegt in die noch leere Karte, darüber steht groß „OHO!“.'},
      about=["Vibe-Coding", "Website", "KI-Werkzeuge", "Webhosting", "Datenschutz", "Barrierefreiheit", "EU AI Act"])
