# Baut website/blog/eu-ai-act-kleine-unternehmen/index.html mit dem gemeinsamen Baustein werkzeuge/blog/beitrag.py.
# Bilder: Titel aus werkzeuge/grafiken/blog/eu-ai-act-titel.py; Fotos und Symbole in website/bilder/blog-ai-act/ (Nachweis im Impressum).
# Checkliste zum Ausdrucken: werkzeuge/blog/eu-ai-act-checkliste.py → website/downloads/eu-ai-act-checkliste.pdf
# Aufruf im Repository-Ordner: python3 werkzeuge/blog/eu-ai-act-kleine-unternehmen.py
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from beitrag import bauen

faq = [
("Gilt der EU AI Act auch für Selbstständige und kleine Unternehmen?",
 "Ja. Der EU AI Act gilt für jedes Unternehmen, das KI beruflich nutzt, unabhängig von der Größe. Wer etwa ChatGPT oder Claude für Texte oder Übersetzungen einsetzt, ist nach der Verordnung „Betreiber“. Kleine und mittlere Unternehmen werden aber bei Bußgeldern milder behandelt."),
("Muss ich KI-generierte Texte auf meiner Website kennzeichnen?",
 "In der Regel nicht. Nach Artikel 50 der KI-Verordnung müssen nur KI-Texte zu Themen von öffentlichem Interesse gekennzeichnet werden, und auch die nicht, wenn ein Mensch sie inhaltlich geprüft hat und redaktionell verantwortet. Werbetexte und Produktbeschreibungen fallen laut den Leitlinien der EU-Kommission nicht darunter, außer sie machen Aussagen zu Gesundheit, Sicherheit oder Nachhaltigkeit."),
("Muss ich KI-Bilder kennzeichnen?",
 "Ja, wenn sie echt wirken. Seit dem 2. August 2026 müssen Betreiber nach Artikel 50 der KI-Verordnung Bilder, Videos und Töne offenlegen, die echten Personen, Orten oder Ereignissen ähneln und fälschlich für echt gehalten werden könnten. Ein sichtbarer Hinweis wie „KI-generiert“ am Bild erfüllt das."),
("Brauche ich eine Schulung oder ein Zertifikat zur KI-Kompetenz?",
 "Nein. Artikel 4 der KI-Verordnung verlangt Maßnahmen zur Förderung der KI-Kompetenz; seit dem Änderungspaket vom Juli 2026 steht ausdrücklich darin, dass kein bestimmtes Niveau verlangt wird. Die Bundesnetzagentur empfiehlt, die Maßnahmen zu dokumentieren. In Deutschland ist für Artikel 4 kein Bußgeld vorgesehen."),
("Muss mein Website-Chatbot sagen, dass er eine KI ist?",
 "Ja. Nach Artikel 50 Absatz 1 der KI-Verordnung müssen Menschen spätestens beim ersten Kontakt erfahren, dass sie mit einer KI sprechen, außer es ist offensichtlich. Die Pflicht trifft den Anbieter des Chatbots; bietest du ihn unter deinem Namen an, bist das in der Regel du. Ein kurzer Satz wie „Sie chatten mit einer KI“ über dem Eingabefeld erfüllt das."),
("Darf ich KI für Bewerbungen nutzen?",
 "Ja, aber ab dem 2. Dezember 2027 gelten strenge Regeln. KI, die Bewerbungen sichtet, filtert oder bewertet, ist dann nach Anhang III der KI-Verordnung Hochrisiko-KI. Betreiber müssen unter anderem menschliche Aufsicht sicherstellen, Protokolle aufbewahren und Bewerber:innen informieren. Eine Stellenanzeige mit KI zu formulieren, ist dagegen unkritisch."),
("Wie hoch sind die Bußgelder für kleine Unternehmen?",
 "Artikel 99 der KI-Verordnung nennt Höchstbeträge von bis zu 35 Millionen Euro oder 7 Prozent des Jahresumsatzes. Für kleine und mittlere Unternehmen gilt jeweils der niedrigere der beiden Werte, und bei Sanktionen ist ihr wirtschaftliches Überleben zu berücksichtigen. In Deutschland ist die Bundesnetzagentur zuständig."),
("Wo bekomme ich Hilfe zum EU AI Act?",
 "Bei der Bundesnetzagentur. Sie bietet einen KI-Service Desk und den „KI-Compliance Kompass“ an, mit dem Unternehmen ihre Pflichten selbst prüfen können. Kostenlose Lernangebote zur KI-Kompetenz gibt es laut Bundesnetzagentur zum Beispiel beim KI-Campus und bei den Mittelstand-Digital Zentren."),
("Hilft STUDIO AAH! bei der Einführung von KI im Team?",
 "Ja. Anna Härtelt von STUDIO AAH! in Leipzig richtet mit dem KI-Arbeits-Setup KI für kleine Teams ein, mit Anleitung und gemeinsamer Einführung. Das ist keine Rechtsberatung, aber ein praktischer Weg, die KI-Kompetenz im Team zu fördern."),
]

bauen('eu-ai-act-kleine-unternehmen',
      titel='EU AI Act für kleine Unternehmen: Was jetzt gilt',
      h1='EU AI Act: Was müssen kleine Unternehmen jetzt tun?',
      beschr='ChatGPT oder Claude im Büro? Was der EU AI Act von kleinen Unternehmen verlangt: KI-Kompetenz, Kennzeichnung, Verbote, Fristen, Bußgelder. Mit Checkliste.',
      datum='2026-11-17', geaendert='2026-11-17',
      bild='blog-eu-ai-act.webp', og_bild='blog-eu-ai-act-og.jpg',
      og_alt='Karte Europas in Blau mit dem gelben Sternenkranz der EU und den Buchstaben AI in der Mitte.',
      keywords=["EU AI Act", "KI-Verordnung", "KI-Kompetenz", "KI kennzeichnen", "KI-Bilder kennzeichnen", "Chatbot Hinweis", "KMU", "KI-Beratung Leipzig"],
      faq=faq, abschnitt='KI-Beratung', ohne_figuren=True,
      about=["EU AI Act", "KI-Verordnung", "KI-Kompetenz", "Transparenzpflichten", "Hochrisiko-KI", "Bußgelder"])
