# Baut website/blog/was-sollte-eine-website-2027-koennen/index.html (Reihe „Website-Fragen“, Teil 2) mit dem gemeinsamen Baustein werkzeuge/blog/beitrag.py.
# Fließtext = Reinzeichnung, von Anna freigegeben 19.10.2026 – nur in was-sollte-eine-website-2027-koennen-inhalt.html ändern. Schema: werkzeuge/blog/schema-blogbeitrag.md
# „Kurz gesagt“ und FAQ fassen nur Aussagen aus dem Artikel bzw. aus Teil 1 zusammen (keine neuen Zahlen).
# Eingebunden: Golden Circle (werkzeuge/grafiken/golden-circle.html), CI-Grafik der Markenbildung und Ökosystem der Webdesign-Seite (dieselben Dateien wie dort).
# Aufruf im Repository-Ordner: python3 werkzeuge/blog/was-sollte-eine-website-2027-koennen.py
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from beitrag import bauen
from gemeinsam import WERKZEUGE

faq = [
("Was sollte eine Website 2027 können?",
 "Sie sollte das Angebot in Sekunden erklären, Vertrauen aufbauen, den Einstieg leicht machen, bei Google (SEO) und in KI-Suchen (GEO) gefunden werden und zu Anfragen führen. Dazu muss sie auf dem Handy funktionieren, gepflegt und barrierefrei sein. Das Fundament ist eine klare Markenidentität."),
("Was ist der Golden Circle?",
 "Der Golden Circle ist ein Modell von Simon Sinek: erst das Warum, dann das Wie, dann das Was. Wer beantworten kann, warum er macht, was er macht, wie er es macht und was genau er für wen anbietet, hat das Fundament für seine Marke und für seine Website."),
("Warum sehen sich viele Websites so ähnlich?",
 "Häufige Gründe sind zu wenig oder die falschen Informationen, kein klarer Weg zur Anfrage, fehlende Suchmaschinenoptimierung und eine Marke, die nur als Farben, Schrift und Logo verstanden wird. Oft wurden Werte, Haltung, Sprache und Zielgruppen nie geklärt, der Blick auf die Mitbewerber fehlt, und Funktionen wie Terminbuchung oder Newsletter fehlen. Wer austauschbar wirkt, wird schnell nur noch über Preis und Leistung verglichen."),
("Braucht jedes Unternehmen eine Website?",
 "Nein. Ein Google-Unternehmensprofil mit Öffnungszeiten, Telefonnummer und Bewertungen kann genügen, wenn der Betrieb sehr lokal ist und von Laufkundschaft lebt, voll ausgelastet ist und niemanden sucht und das Angebot nichts erklären muss. Ein Profil auf einer Plattform gehört Ihnen aber nicht: Google hat 2024 zum Beispiel die kostenlosen Websites im Unternehmensprofil abgeschaltet."),
("Warum braucht eine Arztpraxis eine Website?",
 "Weil sie das Telefon entlastet. 64 Prozent der Deutschen ab 16 Jahren haben schon einmal einen Arzttermin online vereinbart, und wer Online-Termine nutzt oder sich das vorstellen kann, nennt am häufigsten als Vorteil, nicht auf die telefonische Erreichbarkeit der Praxis angewiesen zu sein (Bitkom, Dezember 2025). Eine automatische Erinnerung vor dem Termin dürfte für die Praxis weniger leere Termine, weniger Ausfall und weniger Telefonate bedeuten. Für Werbung und Datenschutz gelten bei Arztpraxen besondere Regeln."),
("Gibt es wegen KI bald keine Websites mehr?",
 "Das lässt sich nicht belegen. Die Suche verändert sich: Zeigt Google eine KI-Übersicht an, klicken Menschen seltener auf Websites, in einer US-Studie bei 8 statt 15 Prozent der Suchen (Pew Research, 2025). Doch KI-Antworten stützen sich auf Inhalte aus dem Web, und die Nielsen Norman Group geht davon aus, dass Menschen weiter Oberflächen brauchen. Die Website wird zur Quelle, aus der Menschen und KI ihre Antworten holen."),
("Wie bereite ich meine Website auf KI-Suchen und KI-Agenten vor?",
 "Mit eigenen, fachkundigen Inhalten statt Allerweltstexten und mit konkreten Antworten auf echte Fragen: Was kostet das, wie lange dauert es, für wen ist das? Dazu kommen saubere Technik und Barrierefreiheit, denn klare Überschriften, beschriftete Formulare und sauberer Code helfen Menschen und KI-Agenten, die Websites lesen. Messen Sie den Erfolg an Anfragen, nicht an Klicks."),
("Bringt eine llms.txt-Datei etwas?",
 "Dafür gibt es bisher keinen Hinweis. Google unterstützt llms.txt nicht, und kein KI-Dienst hat öffentlich erklärt, die Datei zu nutzen (TechWyse, Juni 2026). Deshalb gilt vorerst: abwarten."),
("Gilt das Barrierefreiheits\u00adstärkungs\u00adgesetz für meine Website?",
 "Das Barrierefreiheits\u00adstärkungs\u00adgesetz gilt seit dem 28. Juni 2025 für bestimmte Produkte und Dienstleistungen, darunter Angebote im elektronischen Geschäftsverkehr. Kleinstunternehmen mit Dienstleistungen sind ausgenommen. Ob es für Sie gilt, sollten Sie prüfen lassen."),
("Was kostet eine Website bei STUDIO AAH!?",
 "Eine neue Website beginnt bei STUDIO AAH! bei 2.450 € netto, auch als Onepager; der Launch ist enthalten. Jede Unterseite kostet 190 € mit Texten und Bildern. Einen ersten Kostenvoranschlag gibt der Kostenrechner auf studio-aah.de, ausführlich erklärt Teil 1 der Reihe „Website-Fragen“ Preise, laufende Kosten und Dauer."),
]


def grafik(name):
    return (WERKZEUGE / 'grafiken' / f'{name}.html').read_text(encoding='utf-8').rstrip('\n')


def nur_figur(t):
    """Aus einer Grafik mit eigenem Abschnitt (Überschrift der Leistungsseite) nur die Abbildung samt Kommentar davor."""
    a = t.index('    <!-- Ökosystem'); e = t.rindex('</figure>') + len('</figure>')
    return t[a:e]


bauen('was-sollte-eine-website-2027-koennen',
      titel='Was sollte eine Website 2027 können?',
      h1='Was sollte eine Website 2027 können?',
      beschr='Markenidentität, Nutzen, Zukunft: was eine Website 2027 leisten muss – mit Beispielen aus Software, Arztpraxis und Handwerk und dem Blick auf KI.',
      datum='2026-10-20', geaendert='2026-10-20',
      bild='blog-website-2027.webp', og_bild='blog-website-2027-og.jpg',
      og_alt='Titel „Was sollte eine Website 2027 können?“ neben einer Figur aus Bauhaus-Grundformen und dem Golden Circle aus drei Kreisen.',
      keywords=["Website 2027", "Was muss eine Website können", "Corporate Identity", "Golden Circle", "Website und KI", "GEO", "KI-Agenten", "Webdesign Leipzig"],
      faq=faq, reihe='website-fragen', teil=2, ohne_figuren=True,
      ersetzen={'GOLDEN_CIRCLE': grafik('golden-circle'), 'CI_GRAFIK': grafik('corporate-identity'), 'OEKOSYSTEM': nur_figur(grafik('website-oekosystem')),
                'ALT_TITELBILD': 'Figur aus Bauhaus-Grundformen zeigt auf den Golden Circle: drei Kreise ineinander, innen schwarz das Warum, darum das Wie, außen das Was.'},
      about=["Website", "Corporate Identity", "Golden Circle", "Generative Engine Optimization", "KI-Suche", "Barrierefreiheit"],
      mentions=["Simon Sinek"])
