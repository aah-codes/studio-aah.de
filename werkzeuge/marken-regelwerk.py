# Landingpage /marken-regelwerk/ (07.11.2026): setzt die Paketkarten (aus preise-daten.json, Gruppe „regelwerk“),
# die häufigen Fragen (aus inhalte/marken-regelwerk.json) und die strukturierten Daten zwischen die Marker der Seite
# (REGELWERK-PAKETE, REGELWERK-FAQ, REGELWERK-LD). Der Rest der Seite steht direkt in website/marken-regelwerk/index.html.
# Aufruf im Repository-Ordner:  python3 werkzeuge/marken-regelwerk.py
import json, re

from gemeinsam import NETTO_SATZ, STUDIO_ID, TRENNEN_LEISTUNGEN, WEBSITE, einsetzen, esc, lade_json, paket_karte

URL = 'https://studio-aah.de/marken-regelwerk/'
SEITE = WEBSITE / 'marken-regelwerk' / 'index.html'
GRUPPE = next(g for g in lade_json('preise-daten.json')['gruppen'] if g['id'] == 'regelwerk')
FAQ = lade_json('inhalte/marken-regelwerk.json')['faq']


def pakete():
    karten = '\n'.join(paket_karte(e, TRENNEN_LEISTUNGEN) for e in GRUPPE['pakete'])
    return (f'    <div class="lsx-karten mr-karten">\n{karten}\n    </div>\n'
            f'    <p class="preis-netto gedaempft">{NETTO_SATZ}</p>')


def fragen():
    h = ['    <div class="faq-liste">']
    for frage, antwort in FAQ:
        h.append(f'      <details class="faq-eintrag">\n        <summary>{esc(frage)}</summary>\n'
                 f'        <div class="faq-antwort"><p>{esc(antwort)}</p></div>\n      </details>')
    h.append('    </div>')
    return '\n'.join(h)


def angebot(e):
    if e.get('monat'):
        return {"@type": "Offer", "name": e['name'], "priceCurrency": "EUR", "url": URL + '#pakete',
                "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": e['monat'], "priceCurrency": "EUR",
                                       "unitText": "Monat", "valueAddedTaxIncluded": False}}
    return {"@type": "Offer", "name": e['name'], "priceCurrency": "EUR", "url": URL + '#pakete',
            "priceSpecification": {"@type": "PriceSpecification", "minPrice": e['preis'], "priceCurrency": "EUR",
                                   "valueAddedTaxIncluded": False}}


def ld(seite):
    # Studio-Angaben wie auf den Leistungsseiten (aus der Webdesign-Seite) übernehmen
    start = (WEBSITE / 'service' / 'webdesign' / 'index.html').read_text(encoding='utf-8')
    studio = re.search(r'\{\s*"@type": "ProfessionalService".*?"areaServed": \[[^\]]*\]\s*\}', start, re.S)
    beschreibung = re.search(r'<meta name="description" content="([^"]*)">', seite).group(1)
    graph = [json.loads(studio.group(0)) if studio else {"@id": STUDIO_ID},
             {"@type": "Service", "@id": URL + '#leistung', "name": "Marken-Regelwerk", "serviceType": "Markenrichtlinien (Brand Guidelines)",
              "description": beschreibung, "url": URL, "provider": {"@id": STUDIO_ID}, "areaServed": "DE",
              "offers": [angebot(e) for e in GRUPPE['pakete']]},
             {"@type": "FAQPage", "@id": URL + '#faq', "url": URL, "inLanguage": "de",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
    daten = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{daten}\n  </script>'


def main():
    t = SEITE.read_text(encoding='utf-8')
    neu = einsetzen(einsetzen(einsetzen(t, 'REGELWERK-PAKETE', pakete()), 'REGELWERK-FAQ', fragen()), 'REGELWERK-LD', ld(t))
    if neu != t:
        SEITE.write_text(neu, encoding='utf-8')
    print('Marken-Regelwerk: Pakete, Fragen und strukturierte Daten gesetzt')


if __name__ == '__main__':
    main()
