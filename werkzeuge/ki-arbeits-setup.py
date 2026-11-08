# Landingpage /ki-arbeits-setup/ (07.11.2026): setzt die häufigen Fragen und die strukturierten Daten
# aus werkzeuge/inhalte/ki-arbeits-setup.json zwischen die Marker der Seite (KI-FAQ, KI-LD).
# Der Rest der Seite steht direkt in website/ki-arbeits-setup/index.html; Kopf und Fuß kommen aus kopf-fuss.py.
# Aufruf im Repository-Ordner:  python3 werkzeuge/ki-arbeits-setup.py
import json, re

from gemeinsam import STUDIO_ID, WEBSITE, einsetzen, esc, lade_json

URL = 'https://studio-aah.de/ki-arbeits-setup/'
SEITE = WEBSITE / 'ki-arbeits-setup' / 'index.html'
D = lade_json('inhalte/ki-arbeits-setup.json')


def faq():
    h = ['    <div class="faq-liste">']
    for frage, antwort in D['faq']:
        h.append(f'      <details class="faq-eintrag">\n        <summary>{esc(frage)}</summary>\n'
                 f'        <div class="faq-antwort"><p>{esc(antwort)}</p></div>\n      </details>')
    h.append('    </div>')
    return '\n'.join(h)


def ld(seite):
    start = (WEBSITE / 'service' / 'webdesign' / 'index.html').read_text(encoding='utf-8')
    studio = re.search(r'\{\s*"@type": "ProfessionalService".*?"areaServed": \[[^\]]*\]\s*\}', start, re.S)
    beschreibung = re.search(r'<meta name="description" content="([^"]*)">', seite).group(1)
    graph = [json.loads(studio.group(0)) if studio else {"@id": STUDIO_ID},
             {"@type": "Service", "@id": URL + '#leistung', "name": D['name'], "description": beschreibung, "url": URL,
              "provider": {"@id": STUDIO_ID}, "areaServed": "DE",
              "offers": {"@type": "Offer", "price": str(D['preis']), "priceCurrency": "EUR", "url": URL,
                         "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(D['preis']), "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}},
             {"@type": "FAQPage", "@id": URL + '#faq', "url": URL, "inLanguage": "de",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in D['faq']]}]
    daten = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{daten}\n  </script>'


def main():
    seite = SEITE.read_text(encoding='utf-8')
    seite = einsetzen(seite, 'KI-FAQ', faq())
    seite = einsetzen(seite, 'KI-LD', ld(seite))
    SEITE.write_text(seite, encoding='utf-8')
    print('KI-Arbeits-Setup: Fragen und strukturierte Daten gesetzt')


if __name__ == '__main__':
    main()
