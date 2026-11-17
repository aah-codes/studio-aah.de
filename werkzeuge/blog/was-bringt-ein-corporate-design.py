# Baut website/blog/was-bringt-ein-corporate-design/index.html mit dem gemeinsamen Baustein werkzeuge/blog/beitrag.py.
# Roter Faden: das neue Corporate Design der Stadt Leipzig (Anna, 17.11.2026). Recherche: Betrieb, Studio AAH/Website/2026-11-17_blogbeitrag-entwurf_corporate-design-nutzen.md
# Texte nur in was-bringt-ein-corporate-design-inhalt.html und in der FAQ unten ändern. Schema: werkzeuge/blog/schema-blogbeitrag.md
# Aufruf im Repository-Ordner: python3 werkzeuge/blog/was-bringt-ein-corporate-design.py
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from beitrag import bauen

faq = [
("Was bringt ein Corporate Design einem kleinen Unternehmen?",
 "Ein Corporate Design sorgt dafür, dass Kundschaft und Bewerber:innen ein Unternehmen überall wiedererkennen, vom Angebot bis zur Stellenanzeige. Außerdem spart es Arbeitszeit, weil Vorlagen und Regeln nicht jedes Mal neu erfunden werden müssen. Eine Studie im Journal of Brand Management von 2020 zeigt, dass Logos, Figuren und Wortmarken das größte Potenzial haben, unverwechselbar zu einer Marke zu gehören, weil Mitbewerber sie selten teilen."),
("Wie viel Geld spart ein Corporate Design?",
 "Wie viel ein Corporate Design spart, hängt davon ab, wie viel ein Unternehmen nach außen gestaltet. Im Rechenbeispiel von STUDIO AAH! mit zehn Mitarbeitenden, die je ein Dokument pro Woche erstellen, sparen Vorlagen und klare Regeln rund 77 Stunden oder rund 3.000 Euro im Jahr. Das Beispiel rechnet mit angenommenen Werten und ist keine Messung."),
("Was hat das neue Corporate Design der Stadt Leipzig gekostet?",
 "Zählt man die Posten zusammen, die die Stadt Leipzig im November 2025 im Stadtrat genannt hat, kostete ihr neues Corporate Design rund 666.000 Euro. Eine Gesamtsumme nennt die Stadt selbst nicht. Davon entfielen rund 390.000 Euro auf die Entwicklung des Corporate Designs, rund 93.000 Euro auf die eigene Schrift Leipzig Sans und rund 114.000 Euro auf die Umsetzung auf leipzig.de. Das Logo selbst kostete rund 15.000 Euro."),
("Ist ein Logo schon ein Corporate Design?",
 "Nein. Ein Logo ist nur ein Teil des Corporate Designs. Zum Corporate Design gehören auch Farben, Schriften, Bildwelt, Gestaltungselemente und die Regeln, wie alles zusammen eingesetzt wird. Erst diese Regeln sorgen dafür, dass alle Dokumente eines Unternehmens zusammenpassen."),
("Was kostet ein Corporate Design bei STUDIO AAH!?",
 "Bei STUDIO AAH! in Leipzig beginnt eine Marke mit Positionierung, Logo und Erscheinungsbild im Paket Medium bei 2.500 Euro netto. Das Paket Premium mit Tonalität, ausführlichem Brand Manual und ersten Vorlagen beginnt bei 4.500 Euro netto. Den Festpreis erhalten Sie nach einem kostenlosen Erstgespräch."),
("Muss nach einem neuen Corporate Design alles neu gedruckt werden?",
 "Nein. Die Stadt Leipzig zum Beispiel verwendet vorhandene Materialien weiter und setzt das neue Design nur bei Neuanschaffungen ein. Auch Unternehmen können ein neues Corporate Design schrittweise einführen und alte Drucksachen erst aufbrauchen."),
("Was kostet es, eine Marke anzumelden?",
 "Beim Deutschen Patent- und Markenamt kostet die Anmeldung einer Marke laut dessen Gebührenübersicht online 290 Euro für bis zu drei Klassen, jede weitere Klasse kostet 100 Euro. Eine Unionsmarke für die ganze EU kostet beim EU-Markenamt EUIPO online 850 Euro für eine Klasse."),
("Was ist ein Marken-Regelwerk?",
 "Ein Marken-Regelwerk ist eine kurze, praktische Anleitung dafür, wie ein Unternehmen aussieht und klingt, mit Beispielen und Vorlagen für das Team. Bei STUDIO AAH! gehört eine KI-Markenanweisung dazu, damit auch KI-Werkzeuge wie ChatGPT oder Claude im Stil der Marke schreiben. Das Marken-Regelwerk beginnt bei 1.450 Euro netto."),
]

bauen('was-bringt-ein-corporate-design',
      titel='Was bringt ein Corporate Design? Nutzen und Ersparnis am Beispiel Leipzig',
      h1='Was bringt ein Corporate Design, und was spart es?',
      beschr='Was bringt ein Corporate Design, und was spart es? Am Beispiel der Stadt Leipzig: offengelegte Kosten, Nutzen, Ersparnis und ein Rechenbeispiel für kleine Unternehmen.',
      datum='2026-11-18', geaendert='2026-11-18',
      bild='blog-corporate-design-leipzig.webp', og_bild='blog-corporate-design-leipzig-og.jpg',
      og_alt='Das Neue Rathaus in Leipzig mit seinem hohen Turm vor hellem Himmel.',
      keywords=["Corporate Design", "Corporate Design Kosten", "Corporate Design Nutzen", "Markenbildung", "Logo", "Stadt Leipzig Logo", "Form follows function", "Markenbildung Leipzig"],
      faq=faq, abschnitt='Markenbildung',
      about=["Corporate Design", "Corporate Identity", "Markenbildung", "Markenrichtlinien"],
      mentions=["Rayan Abdullah"])
