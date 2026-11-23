# Baut website/blog/agentische-markensysteme/index.html mit dem gemeinsamen Baustein werkzeuge/blog/beitrag.py.
# Texte nur in agentische-markensysteme-inhalt.html und in der FAQ unten ändern. Grafiken: werkzeuge/grafiken/blog/markensysteme.sh
# Aufruf im Repository-Ordner: python3 werkzeuge/blog/agentische-markensysteme.py
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from beitrag import bauen

faq = [
("Was ist ein agentisches Markensystem?",
 "Ein agentisches Markensystem ist ein Paket aus Text-, Daten- und Codedateien, das Menschen lesen und KI-Agenten auslesen können. Es enthält die Regeln einer Marke für Ton, Wörter, Farben, Schrift, Bildsprache und Layout, jeweils mit Begründung. Die Agentur Little Plains beschreibt es als gemeinsame Quelle für Menschen und Agenten."),
("Was ist der Unterschied zwischen einem Markenhandbuch und einem agentischen Markensystem?",
 "Ein Markenhandbuch zeigt Entscheidungen für bereits gestaltete Seiten, meist als PDF für Menschen. Ein agentisches Markensystem beschreibt laut der Agentur Little Plains die Regeln dahinter so genau, dass auch eine KI sie auf neue Seiten anwenden kann. Beide ergänzen sich: das Handbuch zum Verstehen, das System zum Machen."),
("Braucht ein kleines Unternehmen ein agentisches Markensystem?",
 "Meiner Meinung nach braucht ein kleines Unternehmen kein großes System, aber eine Markendatei für die KI lohnt sich, sobald das Team mit KI schreibt oder gestaltet. Eine einzige Markdown-Datei mit Ton, Wörtern, Farben und Schrift reicht für den Anfang. Wichtig ist, sie an echten Aufgaben zu testen."),
("Was ist eine Markdown-Datei?",
 "Eine Markdown-Datei ist eine einfache Textdatei mit der Endung .md, in der Überschriften und Listen mit wenigen Zeichen markiert sind. Menschen können sie ohne besonderes Programm lesen, KI-Werkzeuge lesen Überschriften und Listen darin als Gliederung. Die Agentur Little Plains und Google mit DESIGN.md setzen für Anweisungen an KI-Agenten Markdown-Dateien ein."),
("In welchen KI-Werkzeugen lässt sich eine Markendatei hinterlegen?",
 "Eine Markendatei lässt sich in jedem KI-Werkzeug hinterlegen, das eigene Anweisungen oder Dateien erlaubt. Je nach Tarif geht das in ChatGPT in einem eigenen GPT oder Projekt, in Claude als Projekt-Anweisung oder Skill und in Gemini als Gem."),
("Was sind Design Tokens?",
 "Design Tokens sind die Werte eines Designs, etwa Farben, Schriftgrößen und Abstände, gespeichert in einem festen Datenformat. Aus ihnen entstehen zum Beispiel das CSS einer Website oder die Farben in Figma. Die Design Tokens Community Group beim W3C hat das Format am 28. Oktober 2025 erstmals in einer stabilen Fassung veröffentlicht, als Empfehlung der Gruppe und nicht als offiziellen W3C-Standard."),
("Wer pflegt ein agentisches Markensystem?",
 "Ein agentisches Markensystem braucht eine verantwortliche Person im Unternehmen, die Änderungen freigibt und mit Datum und Grund festhält. Laut der Agentur Little Plains ist offen, wer über Änderungen entscheidet, wenn mehrere Beteiligte sie vorschlagen. Die Agentur Focus Lab testet die Dateien erneut, wenn sich die Sprachmodelle ändern."),
("Was kostet ein Marken-Regelwerk mit KI-Markenanweisung bei STUDIO AAH!?",
 "Ein Marken-Regelwerk mit KI-Markenanweisung kostet bei STUDIO AAH! ab 1.450 € netto im Paket Start und ab 2.650 € netto im Paket Team. Den genauen Festpreis nennt Anna Härtelt nach dem kostenlosen Erstgespräch, das 30 Minuten dauert und online stattfindet."),
]

bauen('agentische-markensysteme',
      titel='Agentische Markensysteme: Warum das Marken-PDF ausgedient hat',
      h1='Agentische Markensysteme: Warum hat das Marken-PDF ausgedient?',
      beschr='Was ein agentisches Markensystem ist, was hineingehört und wie ein Unternehmen im Mittelstand mit einer einzigen Markendatei für die KI anfängt.',
      datum='2026-11-18', geaendert='2026-11-18',
      bild='blog-markensysteme/titel.webp', og_bild='blog-markensysteme/titel-og.jpg',
      og_alt='Links ein graues PDF-Dokument mit Fragezeichen, rechts ein Ordner mit Dateien für Ton, Farben und Bilder in Blau, Schwarz und Weiß.',
      keywords=["agentische Markensysteme", "Markenhandbuch KI", "Brand Guidelines KI", "Markendatei", "Design Tokens", "DESIGN.md", "Markenbildung", "KI-Markenanweisung"],
      faq=faq, abschnitt='Markenbildung',
      about=["Markenrichtlinien", "Corporate Design", "Künstliche Intelligenz", "Design Tokens"],
      mentions=())
