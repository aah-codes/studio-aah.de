# Baut website/blog/geschaeftsmail-auftragsverarbeitung/index.html mit dem gemeinsamen Baustein werkzeuge/blog/beitrag.py.
# Anna 18.11.2026: „Ja, bauen“ (mit Claudes Empfehlungen: Anthropic-Verbraucherbedingungen nennen, Hoster-Tipp, Kategorie KI-Beratung, echtes Foto).
# Entwurf mit Quellen und Prüfvermerken: Betrieb › Studio AAH › Website › 2026-11-17_blogbeitrag-entwurf_geschaeftsmail-avv.md,
# Recherche: 2026-11-17_recherche_geschaeftsmail-avv.md. Titelfoto: Nataliya Vaitkevich, Pexels (Nachweis im Impressum).
# Aufruf im Repository-Ordner: python3 werkzeuge/blog/geschaeftsmail-auftragsverarbeitung.py
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from beitrag import bauen

faq = [
("Brauche ich für mein E-Mail-Postfach einen Vertrag zur Auftragsverarbeitung?",
 "In der Regel ja. Die Datenschutzkonferenz der deutschen Aufsichtsbehörden nennt die „Auslagerung der E-Mail-Verwaltung“ im Kurzpapier Nr. 13 als typisches Beispiel für Auftragsverarbeitung nach Art. 28 DSGVO. Bei vielen deutschen Hostern ist der Vertrag Teil der Geschäftsbedingungen."),
("Darf ich Gmail geschäftlich nutzen?",
 "Für Kundendaten eignet sich Google Workspace, weil Google dafür einen Vertrag zur Auftragsverarbeitung anbietet; für das kostenlose Gmail ist kein solcher Vertrag auffindbar. Workspace beginnt laut Googles Preisseite bei 6,80 Euro netto pro Person und Monat (Business Starter, Stand November 2026)."),
("Hat IONOS einen Vertrag zur Auftragsverarbeitung?",
 "Ja. Laut IONOS ist die Vereinbarung zur Auftragsverarbeitung seit dem 19. Juli 2022 Bestandteil der Geschäftsbedingungen. Wer einen älteren Vertrag hat, kann sie kostenlos im Kundenkonto abschließen."),
("Welche Angaben müssen in eine geschäftliche E-Mail?",
 "Für eingetragene Kaufleute verlangt § 37a HGB Firma, Rechtsform, Ort der Niederlassung, Registergericht und Registernummer, für GmbHs § 35a GmbHG zusätzlich alle Geschäftsführer:innen. Die Angaben gelten für Geschäftsbriefe gleich welcher Form, also auch für E-Mails."),
("Wie lange muss ich geschäftliche E-Mails aufbewahren?",
 "Nach § 257 HGB und § 147 AO sechs Jahre für Geschäftsbriefe, acht Jahre für Buchungsbelege wie Rechnungen und zehn Jahre für Bücher und Abschlüsse. Die Frist beginnt mit dem Ende des Kalenderjahres."),
("Darf ich mein Geschäftspostfach mit Claude oder ChatGPT verbinden?",
 "In der Regel nur mit einem Tarif, der einen Vertrag zur Auftragsverarbeitung enthält. Bei Claude sind das laut Anthropic Team, Enterprise und die API, bei ChatGPT laut OpenAI Business, Enterprise und die API. Claude Pro und ChatGPT Plus laufen unter den Bedingungen für Privatpersonen."),
("Darf ich als Beschäftigte:r das Firmenpostfach mit meinem privaten KI-Konto verbinden?",
 "Nein. Nach Art. 29 DSGVO verarbeiten Beschäftigte personenbezogene Daten nur auf Weisung des Arbeitgebers, und die Datenschutzkonferenz empfiehlt, dass Arbeitgeber die KI-Konten stellen. Auch mit Erlaubnis geht es nur über einen Firmentarif, für den der Arbeitgeber einen Vertrag zur Auftragsverarbeitung hat."),
("Hilft STUDIO AAH! bei der Einrichtung?",
 "Ja. Anna Härtelt von STUDIO AAH! in Leipzig richtet mit dem KI-Arbeits-Setup KI für kleine Teams ein, mit passenden Tarifen, Konnektoren und klaren Regeln. Das ist keine Rechtsberatung, aber ein praktischer Weg, KI datenschutzbewusst zu starten."),
]

bauen('geschaeftsmail-auftragsverarbeitung',
      titel='Geschäfts-E-Mail und Auftragsverarbeitung: Welcher Tarif passt?',
      h1='Geschäfts-E-Mail und Auftragsverarbeitung: Welcher Tarif ist der richtige?',
      beschr='Brauche ich für mein Firmenpostfach einen Vertrag zur Auftragsverarbeitung? Welche Anbieter ihn mitbringen, was in jede Geschäfts-E-Mail gehört und ob Sie Ihr Postfach mit Claude oder ChatGPT verbinden dürfen.',
      datum='2026-11-18', geaendert='2026-11-18',
      bild='blog-geschaeftsmail.webp', og_bild='blog-geschaeftsmail-og.jpg',
      og_alt='Ein Mann sitzt am Laptop und hebt ratlos die Hände.',
      keywords=["Auftragsverarbeitungsvertrag", "AVV E-Mail", "Gmail geschäftlich", "Google Workspace", "IONOS", "KI Konnektoren", "Claude", "ChatGPT", "Datenschutz", "KI-Beratung Leipzig"],
      faq=faq, abschnitt='KI-Beratung', ohne_figuren=True,
      about=["Auftragsverarbeitung", "DSGVO", "Geschäfts-E-Mail", "KI-Konnektoren", "Datenschutz"])
