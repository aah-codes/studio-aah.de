# Landingpage /website-check/: setzt die 8 Prüfpunkte, die häufigen Fragen und die strukturierten Daten
# aus werkzeuge/inhalte/website-check.json zwischen die Marker der Seite (CHECK-PUNKTE, CHECK-FAQ, CHECK-LD).
# Der Rest der Seite (auch Kopf und Fuß, eigene Fassung ohne Hauptnavigation) steht direkt in website/website-check/index.html.
# Aufruf im Repository-Ordner: python3 werkzeuge/website-check.py
import json, re

from gemeinsam import STUDIO_ID, WEBSITE, einsetzen, esc, lade_json

URL = 'https://studio-aah.de/website-check/'
SEITE = WEBSITE / 'website-check' / 'index.html'
D = lade_json('inhalte/website-check.json')


def punkte():
    """Prüfpunkte mit Icon: Punkte mit "kurz" als Icon-Reihe, die übrigen als breite Karten."""
    reihe = [p for p in D['pruefpunkte'] if p.get('kurz')]
    karten = [p for p in D['pruefpunkte'] if not p.get('kurz')]
    h = ['    <ul class="wc-icons">']
    for p in reihe:
        h.append(f'      <li><img src="../bilder/symbole/{p["icon"]}.svg" alt="" width="48" height="48" loading="lazy"><h3>{esc(p["titel"])}</h3><p>{esc(p["kurz"])}</p></li>')
    h += ['    </ul>', '    <div class="wc-karten">']
    for p in karten:
        h.append(f'      <div class="wc-karte"><img src="../bilder/symbole/{p["icon"]}.svg" alt="" width="48" height="48" loading="lazy"><div><h3>{esc(p["titel"])}</h3><p>{esc(p["text"])}</p></div></div>')
    h.append('    </div>')
    return '\n'.join(h)


def zahlen():
    """Statistik aus der eigenen Stichprobe als große, statische Zahlen."""
    st = D['stichprobe']
    n = st['anzahl']
    h = [f'    <ul class="wc-zahlen" role="list" aria-label="Anteil der {n} untersuchten Websites, bei denen die Angabe fehlt">']
    for w in st['werte']:
        prozent = round(100 * w['anzahl'] / n)
        h.append(f'      <li><b class="wc-zahl">{prozent}&nbsp;%</b>'
                 f'<span class="wc-zahl-name">{esc(w["name"])}</span><small>{esc(w["fach"])}</small></li>')
    h.append('    </ul>')
    return '\n'.join(h)


def fragen():
    """Fragen als (Frage, Absätze, Sprungmarke). Eintrag in der JSON: [Frage, Antwort] oder
    {"id": …, "frage": …, "antwort": [Absatz, …]} – mit id lässt sich die Frage verlinken (z. B. vom Formular)."""
    for g in D['faq']:
        liste = []
        for f in g['fragen']:
            if isinstance(f, dict):
                antwort = f['antwort'] if isinstance(f['antwort'], list) else [f['antwort']]
                liste.append((f['frage'], antwort, f.get('id')))
            else:
                liste.append((f[0], [f[1]], None))
        yield g['gruppe'], liste


def faq():
    h = []
    for gruppe, liste in fragen():
        h.append(f'    <h3 class="wc-faq-gruppe">{esc(gruppe)}</h3>\n    <div class="faq-liste">')
        for frage, absaetze, anker in liste:
            id_attr = f' id="{anker}"' if anker else ''
            text = ''.join(f'<p>{esc(a)}</p>' for a in absaetze)
            h.append(f'      <details class="faq-eintrag"{id_attr}>\n        <summary>{esc(frage)}</summary>\n'
                     f'        <div class="faq-antwort">{text}</div>\n      </details>')
        h.append('    </div>')
    return '\n'.join(h)


def ld(seite):
    # Studio-Angaben wie auf den Leistungsseiten (aus der Webdesign-Seite) übernehmen
    start = (WEBSITE / 'service' / 'webdesign' / 'index.html').read_text(encoding='utf-8')
    studio = re.search(r'\{\s*"@type": "ProfessionalService".*?"areaServed": \[[^\]]*\]\s*\}', start, re.S)
    beschreibung = re.search(r'<meta name="description" content="([^"]*)">', seite).group(1)
    alle = [(f, ' '.join(a)) for _, liste in fragen() for f, a, _ in liste]
    graph = [json.loads(studio.group(0)) if studio else {"@id": STUDIO_ID},
             {"@type": "Service", "@id": URL + '#leistung', "name": "Website-Check", "description": beschreibung, "url": URL,
              "provider": {"@id": STUDIO_ID}, "areaServed": "DE",
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR", "url": URL}},
             {"@type": "FAQPage", "@id": URL + '#faq', "url": URL, "inLanguage": "de",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in alle]}]
    daten = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{daten}\n  </script>'


def main():
    t = SEITE.read_text(encoding='utf-8')
    neu = einsetzen(einsetzen(einsetzen(t, 'CHECK-PUNKTE', punkte()), 'CHECK-FAQ', faq()), 'CHECK-LD', ld(t))
    neu = einsetzen(neu, 'CHECK-ZAHLEN', zahlen())
    if neu != t:
        SEITE.write_text(neu, encoding='utf-8')
    print('Website-Check: Prüfpunkte, Stichprobe, Fragen und strukturierte Daten gesetzt')


if __name__ == '__main__':
    main()
