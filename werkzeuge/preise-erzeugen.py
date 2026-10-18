# Erzeugt aus EINER Datenquelle (preise-daten.json): Daten des Kostenrechners Webdesign js/pakete-daten.js,
# Bereichsleiste, Preislisten + Glossar der Preisseite und Leistungskarten der Startseite. Preise und Paketinhalte nur in preise-daten.json ändern.
# Aufruf im Repository-Ordner:  python3 werkzeuge/preise-erzeugen.py
import json, re

from gemeinsam import NETTO_SATZ, PFEIL, TRENNEN_LEISTUNGEN, WEBSITE, einsetzen, ersetze_einmal, esc, lade_json, paket_karte

daten = lade_json('preise-daten.json')
# Preislisten der übrigen Leistungen; Webdesign hat stattdessen den Kostenrechner (Anna 16.10.2026)
LISTEN = [g for g in daten['gruppen'] if g['id'] != 'website']


def rechner_daten():
    """Kostenrechner Webdesign (js/webrechner.js) bekommt nur die Gruppe „website“ und den Block „webrechner“."""
    web = next(g for g in daten['gruppen'] if g['id'] == 'website')
    paket = {e['id']: e for e in web['pakete']}
    rechner = {'basis': paket['neu']['preis'], 'redesign': paket['redesign']['preis'] - paket['neu']['preis'], 'seite': paket['neu']['seite'],
               'extras': {e['id']: {k: v for k, v in e.items() if k != 'id'} for e in web['extras']},
               **{k: v for k, v in daten['webrechner'].items() if not k.startswith('_')}}
    if len(rechner) != 4 + sum(not k.startswith('_') for k in daten['webrechner']):
        raise SystemExit('Schlüssel in „webrechner“ überschreibt basis/redesign/seite/extras')
    return ('// Erzeugt von werkzeuge/preise-erzeugen.py aus werkzeuge/preise-daten.json – nicht von Hand ändern\nwindow.WEBRECHNER = '
            + json.dumps(rechner, ensure_ascii=False, indent=1) + ';\n')


def preisliste(g):
    """Preisliste einer Leistung mit denselben Paketkarten wie auf der Leistungsseite (Anna 16.10.2026)."""
    mehr = f'<p><a class="textlink" href="{g["link"]}">Mehr zu {esc(g["name"])}{PFEIL}</a></p>' if g.get('link') else ''
    return (f'<section class="preisliste" id="r-{g["id"]}" aria-labelledby="r-{g["id"]}-titel">\n  <div class="preisliste-kopf"><p class="meta">Preisliste</p>'
            f'<h2 class="preis-h2" id="r-{g["id"]}-titel">{esc(g["name"])}</h2><p class="gedaempft">{esc(g.get("intro") or "")}</p>{mehr}</div>\n'
            '    <div class="lsx-karten">\n' + '\n'.join(paket_karte(e, TRENNEN_LEISTUNGEN) for e in g['pakete']) + '\n    </div>\n</section>')


def glossar():
    zeilen = ''.join(f'    <div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>\n' for a, b in daten['glossar'])
    return ('<section class="glossar" id="glossar" aria-labelledby="glossar-titel">\n  <p class="meta">Begriffe kurz erklärt</p>\n'
            '  <h2 class="preis-h2" id="glossar-titel">Glossar</h2>\n  <dl class="glossar-liste">\n' + zeilen + '  </dl>\n</section>')


def preisseite(t):
    # Bereichsleiste: Kostenrechner (nur Webdesign), dann die Preislisten der übrigen Leistungen (Anna 16.10.2026)
    leiste = ''.join(f'<a href="#r-{g["id"]}">{esc(g["kurz"])}</a>' for g in LISTEN)
    t = ersetze_einmal(r'(<nav class="preis-leiste"[^>]*>\n  <a href="#rechner">Kostenrechner Webdesign</a>).*?(<a href="#glossar">Glossar</a>)',
                       lambda m: m.group(1) + leiste + m.group(2), t, 'Bereichsleiste der Preisseite', re.S)
    preislisten = '\n'.join(preisliste(g) for g in LISTEN) + f'\n<p class="preis-netto gedaempft preisliste-netto">{NETTO_SATZ}</p>'
    return einsetzen(einsetzen(t, 'GLOSSAR', glossar()), 'PREISLISTEN', preislisten)


def start_leistungen():
    """Startseite: Leistungen als Karten (9 Stück) mit Chips darüber.
    Ohne Kundenbilder (Anna 13.10.2026: Kunden stehen in den Success Stories): nur das Clay-Icon, ohne Formen."""
    icons = {k: v['icon'] for k, v in lade_json('leistungen-inhalte.json').items() if isinstance(v, dict) and 'icon' in v}
    chips = ''.join(f'<a href="#k-{k["id"]}">{esc(k["titel"])}</a>' for k in daten['startseite'])
    karten = ''.join(f'<a class="ls-karte" href="{k["link"]}" id="k-{k["id"]}"><span class="ls-bild"><img src="{icons[k["id"]]}" alt="" width="400" height="400" loading="lazy"></span>'
                     f'<span class="ls-karte-titel">{esc(k["titel"])}</span><span class="ls-karte-text">{esc(k["text"])}</span></a>' for k in daten['startseite'])
    return ('  <section class="start-leistungen" aria-labelledby="leistungen">\n    <div class="sektionskopf"><p class="meta">Was ich mache</p>'
            '<h2 class="gr-xxl" id="leistungen">Leistungen</h2></div>\n'
            f'    <nav class="leistungs-chips" aria-label="Leistungen">{chips}<a href="preise/#rechner">Kostenrechner →</a></nav>\n'
            f'    <div class="ls-raster">{karten}</div>\n'
            f'    <p class="ls-grundsatz"><a class="textlink" href="service/markenbildung/#corporate-identity">Grundlage für alles, was ich gestalte: die Corporate Identity{PFEIL}</a></p>\n  </section>')


# --- Startseite, Hero: Leistungen als Kategorie-Leiste wie bei Dribbble (Anna 13.10.2026) ---
# Jede Karte führt zur Leistungsseite. Wo es ein echtes Beispiel gibt, steht es als Mockup in der Karte, sonst das Kartenbild der Leistung.
BEISPIELE = {
    # Mobil (Anna 13.10.2026, Vorbild Dribbble „Mobile“): zwei Handys nebeneinander, führt zu UI/UX
    # Mobil wie bei Dribbble: zwei Handys mit dünnem schwarzem Rahmen, heller Grund mit Lichtkante, eine große Form dahinter (Anna 13.10.2026)
    'mobil': ('<span class="kb-mobil"><i class="kb-form-gross"></i>'
              + ''.join(f'<span class="kb-phone"><span class="kb-phone-screen"><img src="bilder/referenzen/{n}" alt="" width="860" height="{h}" decoding="async"></span></span>'
                        for n, h in [('deinetwegen-handy.jpg', 9000), ('studio-aah-handy.jpg', 9923)]) + '</span>'),
    # Webdesign: Foto-Mockup Laptop auf Podest (Vorlage von Anna, Mockuptree, 13.10.2026); die Website sitzt per matrix3d
    # genau im Bildschirm (Ecken im 2000 × 1500 px großen Foto: 530|440, 1248|401, 1334|926, 615|1012) und scrollt wie bisher
    'website': ('<span class="kb-szene" style="--sb:2000;--sh:1500"><img class="kb-szene-bild" src="bilder/mockups/laptop-podest.webp" alt="" width="1000" height="750" loading="lazy">'
                '<span class="kb-szene-schirm" style="transform:matrix3d(0.5768583309,-0.002993487456,0,6.037555358e-05,0.08645866767,0.6267902485,0,-1.30273683e-05,0,0,1,0,528,438,0,1)">'
                '<span class="laptop-seite"><img src="bilder/referenzen/bauer-website.jpg" alt="" width="1440" height="6000" loading="lazy"></span></span></span>'),
    # Druck: Visitenkarten von Dr. Simone Goldhammer auf dem Schreibtisch (werkzeuge/grafiken/druck-mockup.py)
    'print': '<img src="bilder/mockups/druck-schreibtisch.webp" alt="" width="1200" height="900" loading="lazy">',
    # Markenbildung: STUDIO AAH! als eigenes Beispiel (Anna 13.10.2026: ein Kunde, ein Platz; Bauer steht bei Webdesign):
    # Logo auf Creme, Markenfarben, Kreis auf Blau, „AAH!“ auf Schwarz
    'brand': ('<span class="kb-raster kb-eigen"><span class="kb-e-logo"><img src="bilder/logo-studio-aah.svg" alt="" width="180" height="33"></span>'
              '<span class="kb-r-farben"><i style="--f:#0e1011"></i><i style="--f:#2a5fe6"></i><i style="--f:#eeece7"></i><i style="--f:#d6d8d9"></i></span>'
              '<span class="kb-e-blau"><i></i></span><span class="kb-e-schwarz">AAH!</span></span>'),
    # Animation: Foto-Mockup Laptop in Händen vor Wolken (Bendito Mockup); im Bildschirm der eigene Erklärfilm Corporate Identity
    # als kurze Animation (einmal 4,7 s, dann Standbild; beim Darüberfahren neu, js/hero.js); bei „Bewegung reduzieren“ nur das Standbild
    'motion': ('<span class="kb-szene" style="--sb:1777;--sh:1333"><img class="kb-szene-bild" src="bilder/mockups/laptop-wolken.webp" alt="" width="1000" height="750" loading="lazy">'
               '<span class="kb-szene-schirm" style="transform:matrix3d(0.4712927933,-0.01449482037,0,-2.30025695e-05,0.01573352095,0.5063413888,0,1.697912788e-05,0,0,1,0,528,455,0,1)">'
               '<picture><source media="(prefers-reduced-motion: reduce)" srcset="bilder/mockups/ci-animation-still.webp">'
               '<img class="kb-anim" src="bilder/mockups/ci-animation.webp" alt="" width="720" height="450"></picture></span></span>'),
    # Produktdesign wie bei Dribbble: Website von Down to Earth (Kerstin Hack) und daneben ihre Markenfarben ohne Beschriftung
    'ui-ux': ('<span class="kb-produkt"><span class="kb-p-buehne"><span class="kb-p-seite"><img src="bilder/referenzen/leben-website.webp?v=2" alt="" loading="lazy"></span></span>'
              '<span class="kb-p-farben">' + ''.join(f'<i style="--f:{f};--t:{t}">{f.upper()}</i>' for f, t in
                  [('#2d3b42', '#fff'), ('#3f9961', '#fff'), ('#a88b45', '#fff'), ('#f0eadb', '#2d3b42'), ('#ffffff', '#2d3b42')]) + '</span></span>'),
    # Illustration von STUDIO AAH! selbst (Bauhaus-Figur aus dem Blog)
    'illustration': '<img src="bilder/blog-geld-und-zeit.webp" alt="" loading="lazy">',
    # Typografie: Schriftmuster aus den Hausschriften von STUDIO AAH! (Anton, Manrope, JetBrains Mono)
    'typo': '<span class="kb-typo"><span class="kb-typo-aa">Aa</span><span class="kb-typo-text">Manrope</span><span class="kb-typo-meta">Anton · JetBrains Mono</span></span>',
}
# Kategorien oben (Anna 13.10.2026), unabhängig von den Leistungskarten unten; ohne Beispiel steht das Kartenbild der Leistung
KATEGORIEN = [
    {'id': 'brand', 'titel': 'Markenbildung', 'link': 'service/markenbildung/'},
    {'id': 'print', 'titel': 'Druck', 'link': 'service/druck/'},
    {'id': 'mobil', 'titel': 'Mobil', 'link': 'service/ui-ux/'},
    {'id': 'motion', 'titel': 'Animation', 'link': 'service/animation/'},
    {'id': 'illustration', 'titel': 'Illustration', 'link': 'service/illustration-infografik/'},
    {'id': 'website', 'titel': 'Webdesign', 'link': 'service/webdesign/'},
    {'id': 'ui-ux', 'titel': 'Produktdesign', 'link': 'service/ui-ux/'},
    {'id': 'typo', 'titel': 'Typografie', 'link': 'service/markenbildung/'},
]


def heroband():
    kategorien = ''.join('      <a class="kat" href="' + k['link'] + '"><span class="kat-stapel"><span class="kat-bild">' + BEISPIELE[k['id']]
                         + '</span></span><span class="kat-name">' + esc(k['titel']) + '</span></a>\n' for k in KATEGORIEN)
    return ('  <nav class="hero-band" aria-label="Leistungen im Überblick">\n    <div class="hero-spur">\n' + kategorien + '    </div>\n'
            '    <button type="button" class="band-pause" aria-pressed="false"><span class="unsichtbar">Laufband anhalten</span></button>\n  </nav>')


def schreibe(datei, aendern):
    pfad = WEBSITE / datei
    pfad.write_text(aendern(pfad.read_text(encoding='utf-8')), encoding='utf-8')


if __name__ == '__main__':
    (WEBSITE / 'js' / 'pakete-daten.js').write_text(rechner_daten(), encoding='utf-8')
    schreibe('preise/index.html', preisseite)
    schreibe('index.html', lambda t: einsetzen(einsetzen(t, 'LEISTUNGEN', start_leistungen()), 'HEROBAND', heroband()))
    print('Rechner-Daten, Leiste, Glossar und Startseite geschrieben')
