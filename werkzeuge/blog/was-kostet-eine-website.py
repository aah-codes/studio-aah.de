# Baut website/blog/was-kostet-eine-website/index.html (Reihe „Website-Fragen“, Teil 1) mit dem gemeinsamen Baustein werkzeuge/blog/beitrag.py.
# Texte nur in was-kostet-eine-website-inhalt.html und in der FAQ unten ändern. Schema: werkzeuge/blog/schema-blogbeitrag.md
# Aufruf im Repository-Ordner: python3 werkzeuge/blog/was-kostet-eine-website.py
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from beitrag import bauen

faq=[
("Was kostet eine einfache Website für Selbstständige?",
 "Bei STUDIO AAH! beginnt eine neue Website bei 2.450 € netto, auch als Onepager; der Launch ist enthalten. Jede Unterseite kostet 190 € mit Texten und Bildern, ein Redesign 400 € mehr."),
("Was kostet eine Website im Monat?",
 "Nach dem Launch zahlen Sie Hosting, Domain und eventuelle Lizenzen direkt an die Anbieter; die Höhe hängt von Anbieter und Tarif ab. Wer Unterstützung möchte: Wartung kostet bei STUDIO AAH! ab 45 € im Monat, Änderungen und Weiterentwicklung 50–85 € netto pro Stunde, je nach Unternehmensgröße."),
("Wie lange dauert es, eine Website erstellen zu lassen?",
 "Ein Onepager dauert bei STUDIO AAH! etwa 4 bis 6 Wochen. Eine Website mit mehreren Unterseiten dauert etwa 3 bis 4 Monate, je nach Umfang bis zu 6 Monate. Wie schnell es geht, hängt auch davon ab, wie zügig Texte, Bilder und Feedback vorliegen."),
("Was kostet eine zusätzliche Unterseite?",
 "Bei STUDIO AAH! kostet jede Unterseite 190 € mit Texten und Bildern, dazu kommt der Basispreis ab 2.450 €. Eine Website mit 10 Unterseiten kostet damit ab 4.350 € netto, Launch eingerechnet."),
("Was kostet eine mehrsprachige Website?",
 "Jede weitere Sprache kostet 30 % des Website-Preises. Die Übersetzung liefern Sie. Eine zweisprachige Website mit 6 Unterseiten kostet damit ab 4.667 € netto, Launch eingerechnet."),
("Woher kommen die Bilder für meine Website?",
 "Sie können eigene Fotos liefern. Außerdem kann STUDIO AAH! Bilder liefern: lizenzfreie Bilder von Plattformen wie Unsplash oder mit KI erstellte Bilder. Ein Fotoshooting führt STUDIO AAH! nicht selbst durch, kann es aber vermitteln."),
("Muss ich alles auf einmal bezahlen?",
 "Nein. Größere Projekte zahlen Sie bei STUDIO AAH! in drei Raten: bei Start, nach Freigabe des Konzepts und beim Go-live."),
("Was passiert, wenn ich mehr Änderungen möchte?",
 "Zwei Korrekturrunden sind im Festpreis enthalten. Jede weitere Runde rechnet STUDIO AAH! nach Aufwand ab, 50–85 € netto pro Stunde, je nach Unternehmensgröße."),
("Lohnt sich ein Relaunch oder reicht eine Überarbeitung?",
 "Eine Überarbeitung reicht, wenn Marke, Angebot, Technik und Seitenstruktur noch passen und es um einzelne Seiten, Texte oder die Sichtbarkeit geht. Ein Relaunch lohnt sich, wenn sich Angebot oder Marke verändert haben, die Seite auf dem Handy schlecht funktioniert oder die Technik veraltet ist. Beim Relaunch müssen alte Adressen auf die neuen Seiten weiterleiten."),
("Sind die Preise netto?",
 "Ja. Alle genannten Preise sind Einstiegspreise ohne Umsatzsteuer. Den Festpreis erhalten Sie nach einem kostenlosen Erstgespräch."),
]

bauen('was-kostet-eine-website',
      titel='Was kostet eine Website? Preise, laufende Kosten und Dauer 2026',
      h1='Was kostet eine Website – und wie lange dauert sie?',
      beschr='Was kostet eine Website 2026? Preise ab 2.450 €, laufende Kosten und realistische Dauer – mit Beispielrechnungen und Erfahrungen aus Projekten eines Leipziger Studios.',
      datum='2026-10-13', geaendert='2026-10-19',
      bild='blog-geld-und-zeit.webp', og_bild='blog-geld-und-zeit-og.jpg',
      og_alt='Titel „Was kostet eine Website – und wie lange dauert sie?“ neben einer Figur aus Bauhaus-Grundformen mit blauem Modul und einer Uhr.',
      keywords=["Website Kosten", "Was kostet eine Website", "Website erstellen lassen Dauer", "laufende Kosten Website", "Relaunch", "Webdesign Leipzig"],
      faq=faq, reihe='website-fragen', teil=1,
      about=["Website-Kosten", "Webdesign", "Hosting"])
