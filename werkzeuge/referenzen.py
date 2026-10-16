# Erzeugt die Projektübersicht (website/referenzen/index.html) und je Projekt mit "case": true eine Projektseite
# (website/referenzen/<slug>/index.html) aus werkzeuge/inhalte/projekte.json – Aufbau wie bei Behance (Anna 14.10.2026):
# Kopf mit Eckdaten, großes Titelbild oder Film, kurze Texte nur aus Quellen, danach Bildblöcke in voller Breite.
# Kopf und Fuß kommen von der Profilseite (Übersicht) bzw. der Webdesign-Seite (Projektseiten, gleiche Ordnertiefe).
# Aufruf im Repository-Ordner:  python3 werkzeuge/referenzen.py
import copy, html, importlib.util, json, pathlib, re

basis = pathlib.Path(__file__).resolve().parent.parent
esc = lambda s: html.escape(s, quote=False)
_spec = importlib.util.spec_from_file_location('inhalte', basis / 'werkzeuge' / 'inhalte-erzeugen.py')
I = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(I)
ALLE = I.PROJEKTE
CASES = [p for p in ALLE if p.get('case')]
TRENNEN = {'Herausforderung': 'Heraus&shy;forderung', 'Vergabestellen': 'Vergabe&shy;stellen', 'Vertrauensfaktor': 'Vertrauens&shy;faktor', 'Referenzprojekte': 'Referenz&shy;projekte', '60 Sekunden': '60&nbsp;Sekunden', 'Zielgruppenführung': 'Zielgruppen&shy;führung', 'Eignungsnachweis': 'Eignungs&shy;nachweis', 'Bauunternehmen': 'Bau&shy;unternehmen', 'Ingenieurbau &': 'Ingenieur&shy;bau &', 'Rebranding': 'Re&shy;branding', 'Webentwicklung': 'Web&shy;entwicklung', 'Unternehmenspräsentation': 'Unternehmens&shy;präsentation', 'vertrauenswürdig': 'vertrauens&shy;würdig', 'Spezialisierung': 'Spezia&shy;lisierung', 'Kernkompetenzen': 'Kern&shy;kompetenzen'}


def trennen(s):
    # weiche Trennstriche für lange Wörter in schmalen Spalten (Anna 14.10.2026: „Zielgruppenführung“)
    for a, b in TRENNEN.items(): s = s.replace(a, b)
    return s

LINKEDIN = 'https://www.linkedin.com/in/anna-h%C3%A4rtelt-8513b8213/details/recommendations/'


def rahmen(vorlage, main, titel, beschreibung, url, ld):
    t = (basis / 'website' / vorlage).read_text(encoding='utf-8')
    t = re.sub(r'<main id="inhalt">.*?</main>', lambda m: main, t, count=1, flags=re.S)
    t = re.sub(r'<title>.*?</title>', f'<title>{esc(titel)}</title>', t, count=1)
    for name in ('name="description"', 'property="og:description"'):
        t = re.sub(rf'<meta {name} content="[^"]*">', f'<meta {name} content="{html.escape(beschreibung)}">', t, count=1)
    t = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', t, count=1)
    t = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', t, count=1)
    t = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(titel)}">', t, count=1)
    t = re.sub(r'<meta name="robots" content="[^"]*">\n?', '', t)
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: f'<script type="application/ld+json">\n{json.dumps(ld, ensure_ascii=False, indent=2)}\n  </script>', t, count=1, flags=re.S)
    return t


def fakten(p):
    links = '<br>'.join(f'<a class="textlink" href="{l["url"]}" target="_blank" rel="noopener">{esc(l["text"])} <span aria-hidden="true">↗</span></a>' for l in p.get('links', [])[:1])
    zeilen = [('Branche', trennen(esc(p['branche']))), ('Leistungen', trennen(esc(p['leistungen']))), ('Zeitraum', esc(p['zeitraum']))] + ([('Website', links)] if links else [])
    return '<dl class="cs-fakten">' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in zeilen) + '</dl>'


def wand_bild(b, pre):
    # Eintrag der Bildschirmwand: Pfad oder {bild, link, label}; mit Link wird das Bild zum Button (CTA in der Mitte, Anna 14.10.2026)
    if isinstance(b, str): return f'<img src="{pre}{b}" alt="" loading="lazy">'
    return f'<a class="cs-wand-cta" href="{pre}{b["link"]}" aria-label="{esc(b["label"])}"><img src="{pre}{b["bild"]}" alt="" loading="lazy"></a>'


def wand(bilder, pre, spalten=3, reihen=None):
    # Einstieg wie bei Behance („Hedwig“, Anna 14.10.2026): viele Key-Screens schräg gestaffelt auf hellgrauer Fläche;
    # reihen = Spalten fest vorgegeben (CTA-Wand: jede Spalte lang genug, keine leeren Flächen)
    reihen = reihen or [bilder[i::spalten] for i in range(spalten)]
    return ('<div class="cs-wand"><div class="cs-wand-innen">' + ''.join('<div>' + ''.join(wand_bild(b, pre) for b in s) + '</div>' for s in reihen)
            + '</div></div>')


def jpg_mass(datei):
    # Breite und Höhe aus dem JPEG-Kopf (ohne Zusatzbibliothek), für width/height gegen Springen beim Laden
    d = open(datei, "rb").read(); i = 2
    while i < len(d):
        m = d[i + 1]; n = int.from_bytes(d[i + 2:i + 4], 'big')
        if m in (0xC0, 0xC1, 0xC2): return int.from_bytes(d[i + 7:i + 9], 'big'), int.from_bytes(d[i + 5:i + 7], 'big')
        i += 2 + n
    return 0, 0


def svg_mass(datei):
    # width/height aus der viewBox einer SVG-Datei bzw. aus dem Kopf von PNG/JPEG (gegen Springen beim Laden)
    pfad = basis / 'website' / datei
    if datei.endswith('.png'):
        d = pfad.read_bytes()[16:24]; return f' width="{int.from_bytes(d[:4], "big")}" height="{int.from_bytes(d[4:], "big")}"'
    if datei.endswith(('.jpg', '.jpeg')):
        w, h = jpg_mass(pfad); return f' width="{w}" height="{h}"'
    m = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', (basis / 'website' / datei).read_text(encoding='utf-8'))
    return f' width="{round(float(m.group(1)))}" height="{round(float(m.group(2)))}"' if m else ''


def buehne(p, pre):
    if p.get('buehne_wand'):
        # Variante B (Anna 14.10.2026): Wand aus 25 Sections in fünf Spalten, die endlos nach oben laufen, parallel zur Bauer-Schräge;
        # Startseite als Kachel in der mittleren Spalte (schwebender Hero auf Annas Wunsch raus). Pause-Taste, steht bei „Bewegung reduzieren“ still.
        w = p['buehne_wand']
        def spalte(liste, i):
            bilder = ''.join(f'<img src="{pre}{b}" alt="" width="{jpg_mass(basis / "website" / b)[0]}" height="{jpg_mass(basis / "website" / b)[1]}" decoding="async">' for b in liste)
            if i == w.get('fest'):  # mittlere Spalte steht still, der Hero sitzt genau in der Mitte des Rasters (Anna 14.10.2026)
                ganz = ' hw-fest-ganz' if w.get('fest_ganz') else ''  # Jana (Anna 16.10.2026): ganze Startseite in der Mitte, von oben bis unten sichtbar
                return f'<div class="hw-spalte hw-fest{ganz}">{bilder}</div>'
            return f'<div class="hw-spalte" style="--dauer:{w["dauer"][i]}s;--start:{w["start"][i]}"><div class="hw-lauf">{bilder * 3}</div></div>'
        spalten = ''.join(spalte(s, i) for i, s in enumerate(w['spalten']))
        grund = (f';background:#fff url({pre}{w["grund"]}) center / cover no-repeat' if w.get('grund') else '') + (f';--hw-luecke:{w["luecke"]}' if w.get('luecke') else '')  # Jana: Tusche-Striche hinter dem Raster (Anna 16.10.2026)
        if w.get('farbe'):  # Jana (Anna 16.10.2026): einfarbiger Grund (Flieder aus dem Roboterfoto) statt Tusche
            grund += f';background:{w["farbe"]}'
        hell = ' hw-hell' if w.get('grund') or w.get('farbe') else ''
        if w.get('muster'):  # Jana (Anna 16.10.2026): gleichmäßiges Muster ohne feste Mitte, Kacheln gleich groß, leicht schräg aufsteigend, ohne Umriss
            hell += ' hw-muster'
        if w.get('winkel') is not None:
            grund += f';--hw-winkel:{w["winkel"]}deg'
        form = 'nl-voll' if w.get('gerade') else 'nl-schraege'  # gerade: ohne Schräge und ohne Streifen, das Band beginnt gerade (Anna 16.10.2026)
        return (f'  <div class="nl-band {form} nl-blau cs-hero cs-hero-wand{hell}" style="--von:var(--pc-farbe);--bis:var(--pc-farbe){grund}">'
                f'<div class="hw-buehne"><div class="hw-wand" role="img" aria-label="{esc(w["alt"])}">{spalten}</div>'
                f'<button type="button" class="ks-knopf hw-knopf" aria-label="Bewegung anhalten">❚❚</button></div></div>')
    if p.get('buehne_laptop'):  # Deinetwegen (Anna 15.10.2026): Bühne auf dem Markenverlauf, Logo oben links; Gerät nur als echtes Foto-Mockup
        # ("mockup": fertiges Bild aus Canva o. Ä., Gerät nach Zielgruppe); ohne Mockup das flache Bildschirmbild, nie ein gezeichnetes Gerät
        b = p['buehne_laptop']
        logo = f'<img class="bl-logo" src="{pre}{b["logo"]}" alt="" width="160" height="79">' if b.get('logo') else ''
        bild = b.get('mockup') or b['bild']; w, h = jpg_mass(basis / 'website' / bild) if bild.endswith('.jpg') else (b.get('breite', 2400), b.get('hoehe', 1500))
        kl = 'bl-mockup' if b.get('mockup') else 'bl-flach'
        if b.get('mockup'):  # Foto über die ganze Breite (heller Fotogrund), Logo und Dachzeile dunkel darauf
            logo = f'<img class="bl-logo" src="{pre}{b.get("logo_mockup", b["logo"])}" alt="" width="160" height="79">'
            return (f'  <div class="nl-band nl-voll cs-hero bl-hero bl-mit-mockup" style="--von:{b.get("grund", "#f3f3f3")};--bis:{b.get("grund", "#f3f3f3")}"><div class="bl-kopf">{logo}<p class="meta">{esc(b["meta"])}</p></div>'
                    f'<div class="bl-mockup"><img src="{pre}{bild}" alt="{esc(b["alt"])}" width="{w}" height="{h}" fetchpriority="high" decoding="async"></div></div>')
        return (f'  <div class="nl-band nl-dunkel cs-hero bl-hero" style="--von:{b["von"]};--bis:{b["bis"]}"><div class="bl-kopf">{logo}<p class="meta">{esc(b["meta"])}</p></div>'
                f'<div class="{kl}"><img src="{pre}{bild}" alt="{esc(b["alt"])}" width="{w}" height="{h}" fetchpriority="high" decoding="async"></div></div>')
    if p.get('buehne_bild'):  # Variante B (Anna 14.10.2026): EIN scharfer Screen auf Bauer-Blau, harte Kante, keine Maske, nichts darauf
        b = p['buehne_bild']
        return (f'  <div class="nl-band nl-schraege nl-blau cs-hero" style="--von:var(--pc-farbe);--bis:var(--pc-farbe)">'
                f'<div class="cs-hero-rahmen"><img class="cs-hero-bild" src="{pre}{b["bild"]}" alt="{esc(b["alt"])}" width="2880" height="1800" fetchpriority="high" decoding="async"></div></div>')
    if p.get('wand_reihen'):  # feste Spalten (Variante B: vier Spalten, keine Wiederholung direkt untereinander)
        return f'  <div class="cs-buehne">{wand([], pre, reihen=p["wand_reihen"])}</div>'
    if p.get('wand'):
        return f'  <div class="cs-buehne">{wand(p["wand"], pre)}</div>'
    f = p.get('film')
    if f:  # Film mit Steuerung, startet nicht von selbst
        return (f'  <figure class="cs-buehne cs-film">\n    <video controls preload="none" playsinline poster="{pre}{f["vorschau"]}" src="{pre}{f["datei"]}"></video>\n'
                f'    <figcaption class="unsichtbar">{esc(f["titel"])}</figcaption>\n  </figure>')
    return f'  <div class="cs-buehne">{I.cover(p, pre)}</div>'


def eingabe(e):
    # nachgestellte Formulareingabe: [Text, x, y, Breite, Optionen]; Optionen (Anna 14.10.2026, ganzer Funnel):
    # fertig = steht schon da (aus der vorigen Szene), decke = überdeckt den Platzhalter (Auswahlfeld), mehrzeilig = Textfeld, marke = Häkchen/Punkt
    x, ex, ey, ew = e[:4]; opt = e[4] if len(e) > 4 else ''
    kl = ' '.join(o for o in opt.split() if o in ('decke', 'mehrzeilig', 'marke'))
    return (f'<span class="st-eingabe{" " + kl if kl else ""}" data-text="{esc(x)}"' + (' data-fertig' if 'fertig' in opt.split() else '')
            + f' style="--x:{ex};--t:{ey};--w:{ew}"></span>')


def block(b, pre):
    titel = f'<figcaption class="meta">{esc(b["titel"])}</figcaption>' if b.get('titel') else ''
    if b['typ'] == 'vorher-nachher':
        # zwei Seiten nebeneinander (vorher/nachher oder Wireframe/fertig); lange Seiten scrollen beim Überfahren
        kopf = f'<figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2></figcaption>' if b.get('titel') else ''
        hoch = ' cs-vergleich-hoch' if b.get('hoch') else ''
        return (f'  <figure class="cs-block cs-vergleich{hoch}">\n    {kopf}<div><img src="{pre}{b["vorher"]}" alt="{esc(b.get("vorher_alt", "Vorher"))}" loading="lazy"><span class="cs-marke">{esc(b["vorher_text"])}</span></div>\n'
                f'    <div><img src="{pre}{b["nachher"]}" alt="{esc(b.get("nachher_alt", "Nachher"))}" loading="lazy"><span class="cs-marke cs-marke-neu">{esc(b["nachher_text"])}</span></div>\n  </figure>')
    if b['typ'] == 'tabelle':
        zeilen = ''.join(f'<tr><th scope="row">{trennen(esc(a))}</th><td>{esc(v)}</td><td class="cs-neu"><span class="cs-haken" aria-hidden="true"></span>{esc(n)}</td></tr>' for a, v, n in b['zeilen'])
        return (f'  <figure class="cs-block cs-kachel cs-tabelle">\n    <figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2></figcaption>\n'
                f'    <div class="cs-tabelle-rahmen"><table><thead><tr><th scope="col"></th><th scope="col">{esc(b.get("spalte_vorher", "Vorher"))}</th><th scope="col" class="cs-neu">{esc(b.get("spalte_nachher", "Nachher"))}</th></tr></thead><tbody>{zeilen}</tbody></table></div>\n  </figure>')
    if b['typ'] == 'sitemap':
        # Sitemap (Anna 14.10.2026): Hauptseiten mit kleinem Wireframe, alle Boxen gleich hoch; Linien und Boxen bauen sich beim Einblenden auf
        def box(k, i):
            bild = f'<img src="{pre}{k[2]}" alt="" loading="lazy">' if len(k) > 2 and k[2] else ''
            unter = ('<ul>' + ''.join(f'<li style="--i:{i + j + 1}"><span>{esc(u[0])}</span></li>' for j, u in enumerate(k[1])) + '</ul>') if len(k) > 1 and k[1] else ''
            return f'<li style="--i:{i}"><span class="sm-haupt">{bild}<b>{esc(k[0])}</b></span>{unter}</li>'
        wbild = '<img src="' + pre + b['wurzel_bild'] + '" alt="" loading="lazy">' if b.get('wurzel_bild') else ''
        wurzel = f'<span class="sm-wurzel">{wbild}<b>{esc(b["wurzel"])}</b></span>'
        return (f'  <figure class="cs-block cs-kachel cs-sitemap">\n    <figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p>' + (f'<h2 class="gr-h3">{esc(b["titel"])}</h2>' if b.get('titel') else '') + '</figcaption>\n'
                f'    <div class="sm" data-einblenden>{wurzel}<ul>{"".join(box(k, n * 2 + 1) for n, k in enumerate(b["seiten"]))}</ul></div>\n  </figure>')
    if b['typ'] == 'schieber':
        # Wireframe und fertige Seite übereinander, Regler zum Vergleichen; beim ersten Einblenden wischt die fertige Seite einmal herein
        kopf = f'<figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2></figcaption>' if b.get('titel') else ''
        return (f'  <figure class="cs-block cs-schieber-block">\n    {kopf}\n    <div class="cs-schieber" data-einblenden style="--pos: 50%">'
                f'<span class="cs-etikett">{esc(b["links_text"])}</span><span class="cs-etikett cs-etikett-rechts">{esc(b["rechts_text"])}</span>'
                f'<div class="cs-schieber-bild"><img src="{pre}{b["links"]}" alt="{esc(b["links_alt"])}" loading="lazy">'
                f'<div class="cs-schieber-oben"><img src="{pre}{b["rechts"]}" alt="{esc(b["rechts_alt"])}" loading="lazy"></div><span class="cs-schieber-linie" aria-hidden="true"></span></div>'
                f'<input type="range" min="0" max="100" value="50" aria-label="{esc(b["links_text"])} und {esc(b["rechts_text"])} vergleichen"></div>\n  </figure>')
    if b['typ'] == 'texte':
        k = ''.join(f'<div class="cs-kachel"><h2 class="gr-h3">{esc(a)}</h2><p>{esc(x)}</p></div>' for a, x in b['abschnitte'])
        return f'  <div class="cs-block cs-texte cs-texte-block">{k}</div>'
    if b['typ'] == 'geraete':
        handy = f'<span class="pc-handy"><img src="{pre}{b["handy"]}" alt="" loading="lazy"></span>' if b.get('handy') else ''
        return (f'  <figure class="cs-block cs-geraete{" mit-handy" if handy else ""}">\n    <div class="cs-flaeche"><span class="pc-desktop"><img src="{pre}{b["desktop"]}" alt="" loading="lazy"></span>{handy}</div>\n    {titel}\n  </figure>')
    if b['typ'] == 'raster':
        bilder = ''.join(f'<img src="{pre}{x}" alt="" loading="lazy">' for x in b['bilder'])
        return f'  <figure class="cs-block cs-raster">\n    <div>{bilder}</div>\n    {titel}\n  </figure>'
    if b['typ'] == 'film':
        f = b
        return (f'  <figure class="cs-block cs-kachel-film">\n    <video controls preload="none" playsinline poster="{pre}{f["vorschau"]}" src="{pre}{f["datei"]}"></video>\n    {titel}\n  </figure>')
    if b['typ'] == 'bento':
        # Kacheln auf hellgrauem Grund (Bento-Raster); "breit" = zwei Drittel, "dunkel" = schwarze Kachel
        k = ''.join(f'<div class="cs-kachel{" breit" if x.get("breit") else ""}{" dunkel" if x.get("dunkel") else ""}"><img src="{pre}{x["bild"]}" alt="" loading="lazy">'
                    + (f'<p class="meta">{esc(x["titel"])}</p>' if x.get('titel') else '') + '</div>' for x in b['kacheln'])
        return f'  <figure class="cs-block cs-bento">\n    {k}\n  </figure>'
    if b['typ'] == 'stil':
        farben = ''.join(f'<div class="cs-farbe"><span style="background: {c}"></span><p><b>{esc(n)}</b><br><small>{esc(c.upper())}</small></p></div>' for c, n in b['farben'])
        schrift = f'<div class="cs-kachel cs-schrift"><p class="meta">Schrift</p><p class="cs-schrift-name">{esc(b["schrift"])}</p><p class="gedaempft">{esc(b.get("schrift_text", ""))}</p></div>' if b.get('schrift') else ''
        return f'  <figure class="cs-block cs-stil">\n    <div class="cs-kachel cs-farben"><p class="meta">Farben</p><div>{farben}</div></div>{schrift}\n    {titel}\n  </figure>'
    if b['typ'] == 'handys':
        h = ''.join(f'<span class="pc-handy"><img src="{pre}{x}" alt="" loading="lazy"></span>' for x in b['bilder'])
        return f'  <figure class="cs-block cs-handys">\n    <div class="cs-flaeche-grau">{h}</div>\n    {titel}\n  </figure>'
    if b['typ'] == 'stapel':
        # Seiten-Stapel wie bei Behance „CreativMinds“ („12+ Pages, One Unified Experience“): große Zahl links, Seiten gefächert rechts
        s = ''.join(f'<img src="{pre}{x}" alt="" loading="lazy">' for x in b['bilder'])
        return (f'  <figure class="cs-block cs-kachel cs-stapel">\n    <div><p class="cs-stapel-zahl">{b["zahl_html"]}</p><p class="gedaempft">{esc(b["text"])}</p></div>\n'
                f'    <div class="cs-stapel-seiten">{s}</div>\n  </figure>')
    if b['typ'] == 'split':
        return (f'  <figure class="cs-block cs-split">\n    <div class="cs-kachel"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2><p class="gedaempft">{esc(b["text"])}</p></div>\n'
                f'    <div class="cs-kachel cs-split-bild{" hoch" if b.get("hoch") else ""}"><img src="{pre}{b["bild"]}" alt="{esc(b.get("alt", ""))}" loading="lazy"></div>\n  </figure>')
    if b['typ'] == 'designsystem':
        # Farben und Schrift wie ein Designsystem (Anna 14.10.2026): große Farbfelder, Schriftmuster H1 bis Fließtext in der echten Schrift
        # Farbkarten wie Behance „Skin First“ (Anna 14.10.2026): Name groß, darunter Zeilen mit Linien; RGB aus dem HEX-Wert berechnet
        rgb = lambda c: ' '.join(str(int(c[i:i + 2], 16)) for i in (1, 3, 5))
        hell = lambda c: sum(int(c[i:i + 2], 16) for i in (1, 3, 5)) > 450
        farben = ''.join(f'<div class="ds-farbe{" ds-hell" if hell(c) else ""}" style="--f: {c}"><b>{esc(n)}</b><dl><div><dt>Digital HEX</dt><dd>{esc(c.upper())}</dd></div>'
                         f'<div><dt>RGB</dt><dd>{rgb(c)}</dd></div><div><dt>Einsatz</dt><dd>{esc(r)}</dd></div></dl></div>' for c, n, r in b['farben'])
        farben = f'<div class="ds-farben-kopf"><span>Farbpalette</span><span>{esc(b.get("farben_text", ""))}</span></div>' + farben
        def stufe(s):
            if len(s) == 4:  # [Stufe, Maß, Bild, Alternativtext]: Probe als Bild in der echten Schrift, in halber Pixelgröße (Bild in doppelter Auflösung)
                name, mass, bild, alt = s
                d = (basis / 'website' / bild).read_bytes()[16:24]; w, h = int.from_bytes(d[:4], 'big') // 2, int.from_bytes(d[4:], 'big') // 2
                return f'<li><span class="ds-mass">{esc(name)}<br><small>{esc(mass)}</small></span><span class="ds-probe ds-probe-bild"><img src="{pre}{bild}" alt="{esc(alt)}" width="{w}" height="{h}" loading="lazy"></span></li>'
            name, mass, gr, gew, zh, zusatz, probe = s
            return f'<li><span class="ds-mass">{esc(name)}<br><small>{esc(mass)}</small></span><span class="ds-probe" style="font-size: {gr}; font-weight: {gew}; line-height: {zh};{zusatz}">{esc(probe)}</span></li>'
        stufen = ''.join(stufe(s) for s in b.get('stufen', []))
        stufen_html = f'<ol class="ds-stufen">{stufen}</ol>'
        aa_html = (f'<p class="ds-aa ds-aa-bild"><img src="{pre}{b["aa_bild"]}" alt="Aa in {esc(b["schrift"])}"{svg_mass(b["aa_bild"])} loading="lazy"></p>' if b.get('aa_bild') else '<p class="ds-aa">Aa</p>')
        return (f'  <figure class="cs-block cs-designsystem" style="--ds-schrift: {b["schrift_css"].replace(chr(34), "&quot;")}">\n    <figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2></figcaption>\n'
                f'    <div class="ds-farben">{farben}</div>\n'
                f'    <div class="ds-schrift"><div class="ds-schrift-kopf">{aa_html}<p class="ds-name">{esc(b["schrift"])}</p><p class="ds-warum">{esc(b["warum"])}</p></div>{stufen_html}</div>\n  </figure>')
    if b['typ'] == 'film-vergleich':
        # Vorher/Nachher als inszenierter Film im Browserfenster (Anna 14.10.2026): durch die alte Seite klicken, Wischblende, dieselben Seiten neu.
        # Läuft nur, solange sichtbar; Pause-Taste (Bewegung über 5 s braucht eine Pause-Taste)
        seiten = ''.join(f'<img class="vf-seite" data-phase="{ph}" data-pfad="{esc(pfad)}" data-x="{x}" src="{pre}{bild}" alt="{esc(alt)}" loading="lazy">'
                         for ph, liste in (('alt', b['alt']), ('neu', b['neu'])) for bild, pfad, x, alt in liste)
        return (f'  <figure class="cs-block cs-vfilm" data-vfilm>\n    <figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2></figcaption>\n'
                f'    <div class="vf-rahmen"><span class="cs-etikett vf-phase" aria-live="polite">{esc(b["alt_text"])}</span>'
                f'<div class="vf-browser"><div class="vf-leiste"><span class="vf-adresse">bauer-ingbau.de/</span></div><div class="vf-fenster">{seiten}'
                f'<span class="vf-zeiger" aria-hidden="true"></span><div class="vf-blende" aria-hidden="true"><b>{esc(b["blende_text"])}</b></div></div></div>'
                f'<div class="vf-steuerung"><button type="button" class="ks-knopf vf-knopf" aria-label="Film anhalten">❚❚</button><span class="vf-texte" data-alt="{esc(b["alt_text"])}" data-neu="{esc(b["neu_text"])}"></span></div></div>\n  </figure>')
    if b['typ'] == 'karriere':
        # Schwerpunkt Karriere (Anna 14.10.2026: Fachkräftemangel groß, höchstens zwei Seiten, die durchlaufen)
        punkte = ''.join(f'<li>{esc(x)}</li>' for x in b['punkte'])
        seiten = ''.join(f'<div class="kr-seite"><span class="cs-etikett">{esc(n)}</span><div class="kr-fenster"><img src="{pre}{bild}" alt="{esc(alt)}" loading="lazy"></div></div>' for bild, n, alt in b['seiten'])
        return (f'  <section class="cs-block cs-karriere" aria-labelledby="karriere-titel">\n    <div class="kr-text"><p class="meta">{esc(b["meta"])}</p><h2 class="kr-titel" id="karriere-titel">{b["titel_html"]}</h2>'
                f'<p>{esc(b["text"])}</p><ul>{punkte}</ul><p class="kr-steuerung"><button type="button" class="ks-knopf kr-knopf" aria-label="Bewegung anhalten">❚❚</button></p></div>\n    <div class="kr-seiten" data-einblenden>{seiten}</div>\n  </section>')
    if b['typ'] == 'vollbild':
        # großes Foto über die ganze Breite als Kapitelanfang (Anna 14.10.2026, Vorbild Behance „H&P Bauingenieure“)
        return (f'  <figure class="cs-block cs-vollbild"><img src="{pre}{b["bild"]}" alt="{esc(b["alt"])}" loading="lazy">'
                f'<figcaption><p class="meta">{esc(b["meta"])}</p><p class="cs-vollbild-titel">{esc(b["titel"])}</p></figcaption></figure>')
    if b['typ'] == 'buehne':
        # Bühne wie Behance „CreativMinds – Core Interface“ (Anna 14.10.2026): Hintergrundbild oder Verlauf, Text oben, große Muster oder Website darüber
        text = f'<div class="bn-text"><p class="meta">{esc(b["meta"])}</p><h2 class="bn-titel">{trennen(esc(b["titel"]))}</h2>' + (f'<p>{esc(b["text"])}</p>' if b.get('text') else '') + '</div>'
        if b.get('muster'):
            inhalt = '<div class="bn-muster">' + ''.join(f'<img src="{pre}{m}" alt="{esc(a)}" loading="lazy">' for m, a in b['muster']) + '</div>'
        else:
            inhalt = (f'<div class="bn-geraete"><div class="bn-browser"><span class="bn-leiste"></span><div class="bn-fenster"><img src="{pre}{b["browser"]}" alt="{esc(b["browser_alt"])}" loading="lazy"></div></div>'
                      + handy3d(b['handy'], pre, b['handy_alt'], 'iph') + '</div>'
                      # Handy scrollt endlos → Pause-Taste (WCAG 2.2.2, Prüfer 15.10.2026)
                      + '<p class="bn-steuerung"><button type="button" class="ks-knopf bn-knopf" aria-label="Bewegung anhalten">❚❚</button></p>')
        return f'  <section class="cs-block cs-buehne-bild" data-einblenden style="--bn-bild: url({pre}{b["hintergrund"]})">{text}{inhalt}</section>'
    if b['typ'] == 'weg':
        # Wireframes der wichtigsten Seiten als Weg (Anna 14.10.2026, Vorbild Behance „CreativMinds – UX Process“)
        schritte = ''
        for i, (bild, titel, unter, oder) in enumerate(b['schritte'], 1):
            kl = ' class="oder"' if oder else ''
            schritte += (f'<li{kl}><span class="weg-nr">{i:02d}</span><span class="weg-titel">{esc(titel)}</span>'
                         f'<div class="weg-bild"><img src="{pre}{bild}" alt="Wireframe: {esc(titel)}" loading="lazy"></div><span class="weg-unter">{esc(unter)}</span></li>')
        return (f'  <figure class="cs-block cs-kachel cs-weg">\n    <figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p>' + (f'<h2 class="gr-h3">{esc(b["titel"])}</h2>' if b.get('titel') else '')
                + (f'<p class="weg-einleitung">{esc(b["text"])}</p>' if b.get('text') else '') + f'</figcaption>\n    <ol class="weg-schritte">{schritte}</ol>\n  </figure>')
    if b['typ'] == 'section':
        # eine echte Section groß im Browserfenster
        return (f'  <figure class="cs-block cs-section"><div class="cs-section-fenster"><img src="{pre}{b["bild"]}" alt="{esc(b["alt"])}" loading="lazy"></div>'
                + (f'<figcaption class="meta">{esc(b["titel"])}</figcaption>' if b.get('titel') else '') + '</figure>')
    if b['typ'] == 'handy-duo':
        # zwei räumliche Handys, versetzt, scrollen von selbst (Pause-Taste); rechts füllt sich das Formular (nachgestellt, nichts wird gesendet)
        felder = ''.join(f'<span class="hd-eingabe" data-text="{esc(x)}" style="left:{l:.2f}%;top:{o:.3f}%;width:{w:.2f}%"></span>' for x, l, o, w in b['eingaben'])
        return (f'  <section class="cs-block cs-handy-duo" data-handyduo aria-label="{esc(b["titel"])}">\n    <div class="hd-text"><p class="meta">{esc(b["meta"])}</p><h2 class="bn-titel">{trennen(esc(b["titel"]))}</h2><p>{esc(b["text"])}</p>'
                f'<p><button type="button" class="ks-knopf hd-knopf" aria-label="Bewegung anhalten">❚❚</button></p></div>\n'
                f'    <div class="hd-buehne">{handy3d(b["links"], pre, b["links_alt"], "hd-links")}{handy3d(b["rechts"], pre, b["rechts_alt"], "hd-rechts", felder, b.get("form_start", 0))}</div>\n  </section>')
    if b['typ'] == 'visual-design':
        # Visual Design wie Behance „CreativMinds – Visual Language“ (Anna 14.10.2026): Entscheidungen, gewähltes Favicon, Varianten (optional; Storyline 15.10.2026 ohne), zwei Features
        punkte = ''.join(f'<li><b>{esc(a)}</b> {esc(x)}</li>' for a, x in b['entscheidungen'])
        features = ''.join(f'<figure class="vd-feature"><div class="vd-fenster"><img src="{pre}{bild}" alt="{esc(alt)}" loading="lazy"></div><figcaption class="meta">{esc(titel)}</figcaption></figure>' for bild, titel, alt in b.get('features', []))
        return (f'  <section class="cs-block cs-visual" aria-labelledby="vd-titel">\n    <div class="vd-text"><p class="meta">{esc(b["meta"])}</p><h2 class="bn-titel" id="vd-titel">{trennen(esc(b["titel"]))}</h2><ul>{punkte}</ul></div>\n'
                f'    <div class="vd-icon"><img src="{pre}{b["favicon"]}" alt="Favicon von Wolfgang Bauer Ingenieurbau" width="512" height="512" loading="lazy"><span class="meta">{esc(b["favicon_text"])}</span></div>\n'
                + (f'    <figure class="vd-varianten"><img src="{pre}{b["varianten"]}" alt="{esc(b["varianten_alt"])}" loading="lazy"><figcaption class="meta">{esc(b["varianten_text"])}</figcaption></figure>\n' if b.get('varianten') else '')
                + (f'    <div class="vd-features">{features}</div>\n' if features else '') + '  </section>')
    if b['typ'] == 'personas':
        # Zwei Zielgruppen, zwei Sprachen (Anna 14.10.2026): zwei klar getrennte Welten (Auftraggeber hell, Bewerber in Bauer-Blau),
        # große Fotos, Zitate als Sprechblasen, „Sie“ / „Du“ als runder Störer am Ende; eine Schrift
        def person(x):
            return (f'<li class="pe-person"><figure class="pe-foto"><img src="{pre}{x["bild"]}" alt="" width="800" height="1000" loading="lazy"></figure>'
                    f'<blockquote class="pe-blase">„{esc(x["zitat"])}“</blockquote>'
                    f'<p class="pe-name">{esc(x["name"])} <span>{esc(x["rolle"].replace(" · ", ", "))}</span></p>'
                    f'<p class="pe-sucht"><span>Sucht zuerst</span>{" · ".join(esc(t) for t in x["sucht"])}</p></li>')
        def seite(s, kl):
            beispiele = ''.join(f'<li>„{esc(x)}“</li>' for x in s['beispiele'])
            return (f'<div class="pe-seite {kl}"><p class="pe-gruppe">{esc(s["meta"])}</p>'
                    f'<h3 class="pe-titel">{esc(s["titel"])}</h3><p class="pe-ton">{esc(s["ton"])}</p>'
                    f'<ul class="pe-personen pe-anzahl-{len(s["personas"])}">{"".join(person(x) for x in s["personas"])}</ul>'
                    f'<div class="pe-beispiele"><p class="pe-klein">So klingt es auf der Website</p><ul>{beispiele}</ul></div>'
                    f'<p class="pe-stoerer"><span class="unsichtbar">Ansprache: </span>„{esc(s["anrede"])}“</p></div>')
        if b.get('nur'):
            kl = {'auftraggeber': 'pe-sie', 'bewerber': 'pe-du'}[b['nur']]
            kopf_pe = (f'<p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2>' if b.get('mit_kopf') else '')
            hinweis = '<p class="pe-hinweis">Personas: Hypothesen aus Referenzen und Marktrecherche · Fotos: Symbolbilder</p>' if b.get('hinweis') else ''
            return (f'  <section class="cs-block cs-personas pe-einzeln" aria-label="Persona {esc(b[b["nur"]]["meta"])}">{kopf_pe}'
                    f'{seite(b[b["nur"]], kl)}{hinweis}</section>')
        return (f'  <section class="cs-block cs-personas" aria-labelledby="pe-titel"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3" id="pe-titel">{esc(b["titel"])}</h2>'
                + (f'<p class="weg-einleitung">{esc(b["text"])}</p>' if b.get('text') else '') + f'<div class="pe-zwei">{seite(b["auftraggeber"], "pe-sie")}{seite(b["bewerber"], "pe-du")}</div>'
                f'<p class="pe-hinweis">Personas: Hypothesen aus Referenzen und Marktrecherche · Fotos: Symbolbilder</p></section>')
    if b['typ'] == 'heft':
        # Unternehmenspräsentation als flaches Heft mit Klammerheftung (Anna 14.10.2026: flach, Ecken sauber);
        # die rechte Seite blättert in 3D um (js/menue.js), Pause-Taste
        bogen = json.dumps([[pre + l if l else '', pre + r if r else ''] for l, r in b['doppelseiten']])
        # Startbild: erste vollständige Doppelseite (ohne JavaScript sieht man so ein aufgeschlagenes Heft)
        l, r = next((x, y) for x, y in b['doppelseiten'] if x and y)
        return (f'  <figure class="cs-block cs-heft" data-heft data-seiten=\'{bogen}\'><div class="hf-flaeche"><div class="hf-heft">'
                f'<img class="hf-l" src="{pre}{l}" alt="{esc(b["alt"])}" loading="lazy"><img class="hf-r" src="{pre}{r}" alt="" loading="lazy">'
                f'<div class="hf-blatt"><img class="hf-vorn" src="{pre}{r}" alt=""><img class="hf-hinten" src="{pre}{l}" alt=""></div>'
                f'<span class="hf-klammer" aria-hidden="true"></span><span class="hf-klammer hf-klammer-2" aria-hidden="true"></span></div></div>'
                f'<div class="st-leiste"><button type="button" class="ks-knopf hf-knopf" aria-label="Blättern anhalten">❚❚</button><span class="meta">{esc(b["unterschrift"])}</span></div></figure>')
    if b['typ'] == 'galerie':
        # große, scharfe Bildschirmausschnitte mit Unterschrift (z. B. Mega-Menü und Footer)
        f = ''.join(f'<figure class="ga-bild{" ga-breit" if x.get("breit") else ""}"><div class="ga-fenster"><img src="{pre}{x["bild"]}" alt="{esc(x["alt"])}" loading="lazy"></div><figcaption class="meta">{esc(x["titel"])}</figcaption></figure>' for x in b['bilder'])
        kopf = (f'<p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3" id="ga-{b["id"]}">{esc(b["titel"])}</h2>' if b.get('titel') else '')
        return (f'  <section class="cs-block cs-galerie" ' + (f'aria-labelledby="ga-{b["id"]}"' if b.get('titel') else f'aria-label="{esc(b.get("meta", "Galerie"))}"') + f'>{kopf}'
                + (f'<p class="weg-einleitung">{esc(b["text"])}</p>' if b.get('text') else '') + f'<div class="ga-raster">{f}</div></section>')
    if b['typ'] == 'inhalt':
        # Inhaltsverzeichnis mit Sprungmarken (Recherche 15.10.2026: Überblick in den ersten Sekunden, wie IKEA bei Work & Co)
        li = ''.join(f'<li><a href="#{a}">{esc(x)} <span aria-hidden="true">↓</span></a></li>' for x, a in b['punkte'])
        return f'  <nav class="cs-block cs-inhalt" aria-label="{esc(b.get("titel", "Inhalt"))}"><p class="meta">{esc(b.get("titel", "Inhalt"))}</p><ol>{li}</ol></nav>'
    if b['typ'] == 'ergebnis':
        # Ergebnis (Recherche 15.10.2026): jedes Ziel vom Anfang bekommt eine Antwort, dazu Credits und ein Abschluss für die Zielgruppe
        karten = ''.join(f'<li><h3>{trennen(esc(z))}</h3><p>{esc(a)}</p></li>' for z, a in b['ziele'])
        ab = b.get('abschluss')
        abschluss = (f'<div class="eg-abschluss"><p class="eg-frage">{esc(ab["frage"])}</p><a class="button" href="{ab["link"]}">{esc(ab["knopf"])} <span aria-hidden="true">→</span></a></div>') if ab else ''
        liste = f'<ul class="eg-karten eg-anzahl-{len(b["ziele"])}">{karten}</ul>'
        if b.get('_stimme_html'):  # Kundenstimme neben den Antworten (Anna 15.10.2026: Zitat unten „ziemlich lost“)
            liste = f'<div class="eg-mit-stimme">{liste}<div class="eg-stimme">{b["_stimme_html"]}</div></div>'
        return (f'  <section class="cs-block cs-ergebnis" aria-label="Ergebnis">{liste}'
                + (f'<p class="eg-credits">{esc(b["credits"])}</p>' if b.get('credits') else '') + abschluss + '</section>')
    if b['typ'] == 'figma':
        # ein Board in nachgebauter Figma-Oberfläche (Anna 15.10.2026: „links und rechts das User Interface von Figma, damit klar ist: das liegt in Figma“);
        # Oberfläche nur Kulisse (aria-hidden), Beschriftungen nur aus dem Board selbst und allgemeine Programmbegriffe
        akt = ' class="fg-aktiv"'
        eb = ''.join(f'<li{akt if e == b["rahmen"] else ""}><span>#</span>{esc(e)}</li>' for e in b['ebenen'])
        teile = ''.join(f'<div class="fg-teil"><b>{esc(x)}</b><i></i><i></i></div>' for x in ('Rahmen', 'Auto-Layout', 'Füllung', 'Kontur', 'Effekte', 'Exportieren'))
        return (f'  <figure class="cs-block cs-figma"><div class="fg-app">'
                f'<div class="fg-oben" aria-hidden="true"><span class="fg-werkzeuge"><i></i><i></i><i></i><i></i><i></i></span><span class="fg-datei">{esc(b["datei"])}</span><span class="fg-teilen">Teilen</span></div>'
                f'<div class="fg-links" aria-hidden="true"><p class="fg-kopf">Seiten</p><ul><li class="fg-aktiv">{esc(b["seite"])}</li></ul><p class="fg-kopf">Ebenen</p><ul>{eb}</ul></div>'
                f'<div class="fg-flaeche"><div class="fg-board"><span class="fg-name" aria-hidden="true">{esc(b["rahmen"])}</span><img src="{pre}{b["bild"]}" alt="{esc(b["alt"])}" loading="lazy"></div></div>'
                f'<div class="fg-rechts" aria-hidden="true"><p class="fg-reiter"><b>Design</b><span>Prototyp</span></p>{teile}</div>'
                f'</div><figcaption class="meta">{esc(b["titel"])}</figcaption></figure>')
    if b['typ'] == 'cta-wand':
        # alle Call-to-Actions schräg nebeneinander (Anna 14.10.2026, wie die Bildschirmwand oben)
        return (f'  <figure class="cs-block cs-cta-wand"><figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2>'
                + (f'<p class="weg-einleitung">{esc(b["text"])}</p>' if b.get('text') else '') + f'</figcaption><div class="cs-cta-flaeche" style="--spalten:{len(b["reihen"]) if b.get("reihen") else b.get("spalten", 3)}">{wand(b.get("bilder", []), pre, b.get("spalten", 3), b.get("reihen"))}</div></figure>')
    if b['typ'] == 'kapitel':
        # Kapitel nach den Schritten der Übersicht (Anna 14.10.2026): große schwarze Überschrift wie „Leistungen“ auf der Startseite, ohne Nummer
        return f'  <div class="cs-block cs-kapitel"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-xxl lang-wort kp-titel">{esc(b["titel"])}</h2></div>'
    if b['typ'] == 'ablauf':
        # Prozess in der gewohnten Zeitleiste, einspaltig untereinander (Anna 14.10.2026, nicht im Zickzack)
        # jeder Schritt springt zu seinem Abschnitt weiter unten (Anna 14.10.2026: „Anker zur jeweiligen Section“)
        def titel_link(x, a):
            return f'<a class="zl-anker" href="#{a}">{esc(x)} <span aria-hidden="true">↓</span></a>' if a else esc(x)
        li = [f'<li><span class="zl-marke"><small>Schritt</small><b>{i:02d}</b></span><div class="zl-text"><p class="meta">{esc(s[0])}</p><h3>{titel_link(s[1], s[2] if len(s) > 2 else "")}</h3></div></li>' for i, s in enumerate(b['schritte'], 1)]
        halb = (len(li) + 1) // 2 if b.get('spalten', 2) == 2 else len(li)  # spalten: 1 = eine Zeitleiste (wenige Schritte, Lesefolge 01–04)
        spalten = ''.join(f'<figure class="grafik grafik-prozess"><ol class="zeitleiste" start="{s + 1}">{"".join(li[s:s + halb])}</ol></figure>' for s in range(0, len(li), halb))
        return (f'  <section class="cs-block cs-prozess" aria-labelledby="ablauf-titel"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3" id="ablauf-titel">{esc(b["titel"])}</h2>'
                + (f'<p class="weg-einleitung">{esc(b["text"])}</p>' if b.get('text') else '') + f'<div class="cs-prozess-spalten">{spalten}</div></section>')
    if b['typ'] == 'klickstrecke':
        # Klickstrecke als Treppe: Schritte versetzt, Beschriftung neben der Karte statt darauf (Anna 14.10.2026)
        punkte = ''.join(f'<li>{esc(x)}</li>' for x in b['punkte'])
        stufen = ''.join(f'<li class="kl-stufe{" kl-oder" if oder else ""}" style="--n:{i}"><span class="kl-label"><b>{i + 1:02d}</b>{esc(titel)}</span>'
                         f'<div class="kl-fenster"><img src="{pre}{bild}" alt="{esc(titel)}" loading="lazy"></div></li>' for i, (bild, titel, oder) in enumerate(b['stufen']))
        return (f'  <section class="cs-block cs-klick" aria-labelledby="klick-titel">\n    <div class="kl-text"><p class="meta">{esc(b["meta"])}</p><h2 class="kr-titel" id="klick-titel">{b["titel_html"]}</h2>'
                f'<p>{esc(b["text"])}</p><ul>{punkte}</ul></div>\n    <ol class="kl-treppe">{stufen}</ol>\n  </section>')
    if b['typ'] == 'funnel-karte':
        # Beide Click-Funnels auf einen Blick (Anna 14.10.2026: „die zwei Zielgruppen … die eine hat einen anderen Klickfunnel als die andere“):
        # je Spur Störer, Zielgruppe, nummerierte Stationen mit der echten Seite; die Seiten scrollen langsam durch (Pause-Taste)
        def spur(sp):
            st = ''.join(f'<li class="fk-station{" fk-cta" if x.get("cta") else ""}{" fk-ganz" if x.get("ganz") else ""}"><span class="fk-nr">{i:02d}</span><span class="fk-label">{trennen(esc(x["label"]))}</span>'
                         f'<div class="fk-fenster"><img src="{pre}{x["bild"]}" alt="{esc(x["alt"])}" loading="lazy" style="--dauer:{x.get("dauer", 14)}s"></div></li>'
                         for i, x in enumerate(sp['stationen'], 1))
            return (f'<div class="fk-spur fk-{sp["art"]}"><div class="fk-kopf"><span class="fk-stoerer">„{esc(sp["anrede"])}“</span><p class="meta">{esc(sp["gruppe"])}</p></div>'
                    f'<ol class="fk-stationen" data-n="{len(sp["stationen"])}">{st}</ol></div>')
        kopf = (f'<p class="meta">{esc(b["meta"])}</p>' if b.get('meta') else '') + (f'<h2 class="fk-gross">{esc(b["titel"])}</h2>' if b.get('titel') else '')
        return (f'  <section class="cs-block cs-funnel-karte" data-einblenden aria-label="{esc(b.get("aria", "Click-Funnels der beiden Zielgruppen"))}">{kopf}'
                + ''.join(spur(sp) for sp in b['spuren'])
                + '<p class="fk-steuerung"><button type="button" class="ks-knopf fk-knopf" aria-label="Bewegung anhalten">❚❚</button></p></section>')
    if b['typ'] == 'mega-film':
        # Mega-Menü als kleiner Film (Anna 14.10.2026: „einen Film davon, wie das Ease-In, Ease-Out“): Zeiger fährt auf den Menüpunkt,
        # das Menü gleitet auf, die Seite darunter dunkelt ab, schließt wieder; Pause-Taste, bei reduzierter Bewegung steht das Menü offen
        menues = ''.join(f'<img class="mf-menue mf-menue-{i}" src="{pre}{m["bild"]}" alt="{esc(m["alt"])}" style="--kopf:{m.get("kopf", 17)}%" loading="lazy">' for i, m in enumerate(b['menues']))
        kopf = (f'<p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2>' if b.get('titel') else '')
        return (f'  <figure class="cs-block cs-mega-film" data-einblenden>{kopf}<div class="mf-browser"><span class="bn-leiste"></span><div class="mf-fenster">'
                f'<img class="mf-basis" src="{pre}{b["basis"]}" alt="{esc(b["basis_alt"])}" loading="lazy"><span class="mf-dunkel" aria-hidden="true"></span>{menues}'
                f'<span class="mf-zeiger" aria-hidden="true"></span></div></div>'
                f'<div class="st-leiste"><button type="button" class="ks-knopf mf-knopf" aria-label="Film anhalten">❚❚</button>'
                + (f'<span class="meta">{esc(b["unterschrift"])}</span>' if b.get('unterschrift') else '') + '</div></figure>')
    if b['typ'] == 'ziele-text':  # B (Anna 14.10.2026: „zu viele Icons … ganz schlichte Sache“): zwei Spalten, nur Text und Linien
        L, R = b['links'], b['rechts']
        def spalte(titel, punkte):
            li = ''.join(f'<li>{trennen(esc(x))}</li>' for x in punkte)
            return f'<div class="zt-spalte"><h2 class="zt-titel">{trennen(esc(titel))}</h2><ul class="zt-liste">{li}</ul></div>'
        return f'  <section class="cs-block cs-ziele-text">{spalte(L["titel"], [t for _, t in L["punkte"]])}{spalte(R["titel"], R["punkte"])}</section>'
    if b['typ'] == 'ziele-grafik':
        # Herausforderung → Website-Relaunch → Ziele als Grafik (Anna 14.10.2026): Linien laufen von links in den Kreis und weiter zu den Zielen
        def symbol(z):
            if z == '60':  # Stoppuhr
                return ('<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="20" y="2" width="8" height="5" rx="1.5"/><circle cx="24" cy="27" r="18" fill="none" stroke-width="4"/>'
                        '<path d="M24 9 A18 18 0 0 1 41.4 22.3" fill="none" stroke-width="4" class="zg-bogen"/><text x="24" y="32.5" text-anchor="middle">60</text></svg>')
            return f'<span>{esc(z)}</span>'
        L, M, R = b['links'], b['mitte'], b['rechts']
        links = ''.join(f'<li><span class="zg-symbol">{symbol(z)}</span><span class="zg-text">{esc(t)}</span></li>' for z, t in L['punkte'])
        rechts = ''.join(f'<li><span class="zg-haken" aria-hidden="true"></span><span class="zg-text">{esc(t)}</span></li>' for t in R['punkte'])
        nl, nr = len(L['punkte']), len(R['punkte'])
        pfade = ''.join(f'<path d="M0 {(k + .5) * 100 / nl:.2f} C 22 {(k + .5) * 100 / nl:.2f}, 22 50, 50 50" pathLength="1"/>' for k in range(nl))
        pfade += ''.join(f'<path d="M50 50 C 78 50, 78 {(k + .5) * 100 / nr:.2f}, 100 {(k + .5) * 100 / nr:.2f}" pathLength="1"/>' for k in range(nr))
        kopf = lambda x, k: f'<div class="zg-kopf zg-kopf-{k}"><img src="{pre}bilder/icons/{x["icon"]}" alt="" width="400" height="400" loading="lazy"><h2>{trennen(esc(x["titel"]))}</h2></div>'
        return (f'  <section class="cs-block cs-ziele-grafik" data-einblenden aria-label="{esc(L["titel"])} und {esc(R["titel"])}">'
                f'{kopf(L, "links")}<div class="zg-leer"></div>{kopf(R, "rechts")}'
                f'<ul class="zg-links">{links}</ul>'
                f'<div class="zg-mitte"><svg class="zg-linien" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">{pfade}</svg>'
                f'<div class="zg-kern"><img src="{pre}{M["bild"]}" alt="" width="512" height="512" loading="lazy"><span>{esc(M["text"])}</span></div></div>'
                f'<ul class="zg-rechts">{rechts}</ul></section>')
    if b['typ'] == 'zwei-karten':
        # zwei große Karten (Herausforderung, Ziele) statt kleinteiliger Chips (Anna 14.10.2026)
        k = ''.join(f'<div class="zk-karte"><img src="{pre}bilder/icons/{i}" alt="" width="400" height="400" loading="lazy"><h2>{esc(h)}</h2><ul>'
                    + ''.join(f'<li>{esc(x)}</li>' for x in liste) + '</ul></div>' for i, h, liste in b['karten'])
        return f'  <section class="cs-block cs-zwei-karten" aria-label="Herausforderung und Ziele">{k}</section>'
    if b['typ'] == 'storyfilm':
        # Storytelling-Film im Browserfenster (Anna 14.10.2026): durch die alte Seite klicken, Zettel zeigen, was schlecht war;
        # Blende; neue Seite mit Mega-Menü, Referenzen, CTA, Formularen. Szenen-Daten als JSON, Ablauf in js/menue.js
        szenen = ''
        for i, s in enumerate(b['szenen']):
            eingaben = ''.join(eingabe(e) for e in s.get('eingaben', []))
            # fünfter Wert „wichtig“: Hauptbefund als hellroter Zettel, sonst hellblau (Anna 15.10.2026)
            notizen = ''.join(f'<span class="st-notiz st-notiz-{s["phase"]}{" st-notiz-wichtig" if "wichtig" in z[4:] else ""}" style="left:{z[1]}%;top:{z[2]}%;--r:{(-2.5 if j % 2 else 2)}deg">{esc(z[0])}</span>' for j, z in enumerate(s.get('notizen', [])))
            szenen += (f'<div class="st-szene" data-i="{i}"><div class="st-zoom"><div class="st-seite"><img src="{pre}{s["bild"]}" alt="{esc(s["alt"])}" loading="lazy">{eingaben}</div></div>{notizen}</div>')
        kapitel = ''.join(f'<button type="button" class="st-kapitel" data-ziel="{i}">{esc(s["kapitel"])}</button>' for i, s in enumerate(b['szenen']) if s.get('kapitel'))
        daten = json.dumps([{k: s.get(k) for k in ('pfad', 'phase', 'titel', 'von', 'bis', 'dauer', 'notizen', 'zoom', 'klick', 'tippen_ab')} for s in b['szenen']], ensure_ascii=False)
        kopf_film = '' if b.get('ohne_kopf') else f'<figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2></figcaption>'
        return (f'  <figure class="cs-block cs-story" data-story aria-label="{esc(b["titel"])}">\n    {kopf_film}\n'
                f'    <div class="st-rahmen"><span class="cs-etikett st-phase">{esc(b["alt_text"])}</span>'
                + ((f'<div class="st-monitor st-monitor-foto" style="--sx:{b["monitor"]["schirm"][0]}%;--sy:{b["monitor"]["schirm"][1]}%;--sw:{b["monitor"]["schirm"][2]}%;--sh:{b["monitor"]["schirm"][3]}%;--fv:{b["monitor"]["verhaeltnis"]}">'
                    f'<img class="st-foto" src="{pre}{b["monitor"]["foto"]}" alt="" width="{jpg_mass(basis / "website" / b["monitor"]["foto"])[0]}" height="{jpg_mass(basis / "website" / b["monitor"]["foto"])[1]}" loading="lazy"><div class="st-schirm">')
                   if isinstance(b.get('monitor'), dict) else ('<div class="st-monitor">' if b.get('monitor') else ''))  # Standrechner (Anna 15.10.2026): Foto-Mockup oder (alt) gezeichnet
                + f'<div class="st-browser"><div class="vf-leiste"><span class="vf-adresse">bauer-ingbau.de/</span></div><div class="st-fenster">{szenen}'
                f'<span class="vf-zeiger" aria-hidden="true"></span><div class="vf-blende" aria-hidden="true"><b>{esc(b["blende_text"])}</b></div></div></div>'
                + ('</div></div>' if isinstance(b.get('monitor'), dict) else ('<span class="st-hals" aria-hidden="true"></span><span class="st-fuss" aria-hidden="true"></span></div>' if b.get('monitor') else ''))
                + f'<div class="st-leiste"><button type="button" class="ks-knopf st-knopf" aria-label="Film anhalten">❚❚</button><div class="st-kapitelreihe">{kapitel}</div>'
                f'<p class="st-titel"></p></div></div>\n'
                f'    <script type="application/json" class="st-daten" data-alt="{esc(b["alt_text"])}" data-neu="{esc(b["neu_text"])}">{daten}</script>\n  </figure>')
    if b['typ'] in ('fotofilm', 'buch'):
        # Foto-Mockup (Canva, Anna 14.10.2026: passend zur Zielgruppe): Foto mit Maske liegt über der Seite, die im Bildschirm läuft
        fo = b['foto']
        schirme = ''
        for s in b['schirme']:
            if b['typ'] == 'fotofilm':
                szenen = ''.join(f'<div class="st-szene" data-i="{i}"><div class="st-zoom"><div class="st-seite"><img src="{pre}{z["bild"]}" alt="{esc(z["alt"])}" loading="lazy">'
                                 + ''.join(eingabe(e) for e in z.get('eingaben', []))
                                 + '</div></div></div>' for i, z in enumerate(s['szenen']))
                inhalt = f'<div class="st-fenster" style="--basis:{s["breite"]}">{szenen}<span class="vf-zeiger" aria-hidden="true"></span></div>'
            else:
                inhalt = ''.join(f'<img class="bu-seite" src="{pre}{x}" alt="" loading="lazy">' for x in s['seiten'])
            schirme += f'<div class="fm-schirm" style="width:{s["breite"]}px;height:{s["hoehe"]}px;transform:{s["matrix"]}">{inhalt}</div>'
        maske = f'-webkit-mask-image:url({pre}{fo["maske"]});mask-image:url({pre}{fo["maske"]})'
        szene = (f'<div class="fm" data-fm style="--sb:{fo["breite"]};--sh:{fo["hoehe"]}"><div class="fm-szene">{schirme}'
                 f'<img class="fm-foto" src="{pre}{fo["bild"]}" alt="{esc(fo["alt"])}" style="{maske}" loading="lazy"></div></div>')
        knopf = '<button type="button" class="ks-knopf fm-knopf" aria-label="Bewegung anhalten">❚❚</button>'
        if b['typ'] == 'fotofilm':
            daten = json.dumps([{k: z.get(k) for k in ('von', 'bis', 'dauer', 'klick', 'tippen_ab')} for s in b['schirme'] for z in s['szenen']], ensure_ascii=False)
            szene = (f'<figure class="cs-story fm-story" data-story>{szene}<div class="st-leiste">{knopf.replace("fm-knopf", "st-knopf")}</div>'
                     f'<script type="application/json" class="st-daten">{daten}</script></figure>')
        else:
            szene = f'<figure class="fm-buch" data-buch>{szene}<div class="st-leiste">{knopf}<span class="meta">{esc(b.get("unterschrift", ""))}</span></div></figure>'
        if b.get('dazu'):  # zweites Gerät daneben (Anna 15.10.2026: Handy zum Fachkräftemangel, spart eine Section)
            szene = f'<div class="fm-paar">{szene}{block(dict(b["dazu"], typ="fotofilm"), pre)}</div>'
        if not b.get('text') and not b.get('titel_html'):
            return f'  <div class="cs-block fm-block">{szene}</div>'
        punkte = ''.join(f'<li>{esc(x)}</li>' for x in b.get('punkte', []))
        return (f'  <section class="cs-block fm-mit-text{" fm-dunkel" if b.get("dunkel") else ""}" aria-labelledby="fm-{b["id"]}">\n    <div class="fm-text"><p class="meta">{esc(b["meta"])}</p>'
                f'<h2 class="kr-titel" id="fm-{b["id"]}">{b["titel_html"]}</h2>' + (f'<p>{esc(b["text"])}</p>' if b.get('text') else '') + (f'<ul>{punkte}</ul>' if punkte else '') + f'</div>\n    {szene}\n  </section>')
    if b['typ'] == 'ueberblick':
        # Überblick wie Behance „Overview + Scope“ (Deinetwegen, Anna 15.10.2026): große Aussage links, Leistungen als Spalte rechts
        li = ''.join(f'<li>{esc(x)}</li>' for x in b['leistungen'])
        return (f'  <section class="cs-block cs-ueberblick" aria-labelledby="ub-titel"><div class="ub-text"><p class="meta">{esc(b["meta"])}</p>'
                f'<h2 class="ub-aussage" id="ub-titel">{trennen(esc(b["aussage"]))}</h2></div>'
                f'<div class="ub-leistungen"><p class="ub-klein">{esc(b.get("leistungen_titel", "Leistungen"))}</p><ul>{li}</ul></div></section>')
    if b['typ'] == 'hl-karten':
        # Herausforderung und Lösung als zwei große Karten (Behance „Challenge / Solution“), darunter die Ziele (Deinetwegen, Anna 15.10.2026)
        def inhalt_karte(x):  # Aussage (Deinetwegen) oder Liste (Bauer: Herausforderung und Ziele)
            if x.get('punkte'): return '<ul class="hk-liste">' + ''.join(f'<li>{trennen(esc(t))}</li>' for t in x['punkte']) + '</ul>'
            return f'<p class="hk-text">{trennen(esc(x["text"]))}</p>'
        k = ''.join(f'<div class="hk-karte{" hk-dunkel" if x.get("dunkel") else ""}{" hk-mit-liste" if x.get("punkte") else ""}"><h2 class="hk-etikett">{esc(x["etikett"])}</h2>{inhalt_karte(x)}</div>' for x in b['karten'])
        z = ''.join(f'<li><span class="hk-nr" aria-hidden="true">{i}</span><span>{esc(x)}</span></li>' for i, x in enumerate(b.get('ziele', []), 1))
        ziele = f'<div class="hk-ziele"><h3 class="ub-klein">{esc(b.get("ziele_titel", "Ziele"))}</h3><ol style="--n:{len(b.get("ziele", []))}">{z}</ol></div>' if z else ''
        return f'  <section class="cs-block cs-hl-karten" aria-label="Herausforderung und Lösung"><div class="hk-paar">{k}</div>{ziele}</section>'
    if b['typ'] == 'marke':
        # Corporate Design auf einen Blick (Deinetwegen, Anna 15.10.2026): Logos, Farben, Schrift als Bild (Lizenz der Schrift erlaubt keine Weitergabe)
        logos = ''.join(f'<figure class="mk-logo" style="--grund:{g}"><img src="{pre}{bild}" alt="{esc(alt)}"{svg_mass(bild)} loading="lazy"></figure>' for bild, alt, g in b['logos'])
        def lum(c):
            k = [int(c[i:i + 2], 16) / 255 for i in (1, 3, 5)]; k = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in k]
            return .2126 * k[0] + .7152 * k[1] + .0722 * k[2]
        hell = lambda c: 1.05 / (lum(c) + .05) < 4.5  # dunkle Schrift, wenn Weiß zu wenig Kontrast hat
        farben = ''.join(f'<li class="mk-farbe{" mk-hell" if hell(c) else ""}" style="--f:{c}"><b>{esc(n)}</b><span>{esc(c.upper())}</span><small>{esc(r)}</small></li>' for c, n, r in b.get('farben', []))
        return (f'  <section class="cs-block cs-cd" aria-labelledby="mk-titel"><div class="mk-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3" id="mk-titel">{esc(b["titel"])}</h2>'
                + (f'<p class="weg-einleitung">{esc(b["text"])}</p>' if b.get('text') else '') + f'</div>'
                f'<div class="mk-logos">{logos}</div>' + (f'<ul class="mk-farben">{farben}</ul>' if farben else '')
                + (f'<figure class="mk-schrift"><img src="{pre}{b["schrift_bild"]}" alt="{esc(b["schrift_alt"])}" width="1600" height="900" loading="lazy"><figcaption class="meta">{esc(b["schrift_text"])}</figcaption></figure>' if b.get('schrift_bild') else '')
                + '</section>')  # Farben und Schrift optional: bei Goldhammer zeigt sie das Designsystem wie bei Bauer (Anna 16.10.2026)
    if b['typ'] == 'langaufnahmen':
        # ganze Seite am Rechner und am Handy nebeneinander, unbewegt (Anna 15.10.2026: „fullscreenshot von desktop und handy nebeneinander“);
        # Breiten so, dass beide gleich hoch sind (Seitenverhältnisse aus den Bilddateien)
        dw, dh = jpg_mass(basis / 'website' / b['desktop']); hw, hh = jpg_mass(basis / 'website' / b['handy'])
        rd, rh = dw / dh, hw / hh
        lid = 'la-' + (b.get('anker') or b.get('id') or 'titel')  # eindeutige ID je Abschnitt (Prüfer 16.10.2026)
        return (f'  <section class="cs-block cs-lang" aria-labelledby="{lid}"><div class="la-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="la-titel" id="{lid}">{trennen(esc(b["titel"]))}</h2>'
                + (f'<p>{esc(b["text"])}</p>' if b.get('text') else '') + f'</div>'
                f'<div class="la-paar" style="--rd:{rd:.5f};--rh:{rh:.5f}"><figure class="la-karte la-desktop"><img src="{pre}{b["desktop"]}" alt="{esc(b["desktop_alt"])}" width="{dw}" height="{dh}" loading="lazy"><figcaption class="meta">Rechner</figcaption></figure>'
                f'<figure class="la-karte la-handy"><img src="{pre}{b["handy"]}" alt="{esc(b["handy_alt"])}" width="{hw}" height="{hh}" loading="lazy"><figcaption class="meta">Handy</figcaption></figure></div></section>')
    if b['typ'] == 'seiten-pillen':
        # weitere Seiten versetzt nebeneinander, beschriftet mit Pillen und Pfeil (Behance „Other Pages“, Deinetwegen, Anna 15.10.2026)
        pfeil = '<svg class="sp-pfeil" viewBox="0 0 60 34" aria-hidden="true"><path d="M2 6 C 18 2, 34 6, 44 24"/><path d="M34 22 L 45 26 L 49 14"/></svg>'
        seiten = ''.join(f'<figure class="sp-seite sp-{x.get("art", "desktop")}"><figcaption><span class="sp-pille">{esc(x["label"])}</span>{pfeil}</figcaption>'
                         f'<div class="sp-fenster"><img src="{pre}{x["bild"]}" alt="{esc(x["alt"])}" width="{jpg_mass(basis / "website" / x["bild"])[0]}" height="{jpg_mass(basis / "website" / x["bild"])[1]}" loading="lazy"></div></figure>' for x in b['seiten'])
        return (f'  <section class="cs-block cs-seiten-pillen" aria-labelledby="sp-titel"><div class="sp-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="la-titel" id="sp-titel">{trennen(esc(b["titel"]))}</h2>'
                + (f'<p>{esc(b["text"])}</p>' if b.get('text') else '') + f'</div><div class="sp-reihe">{seiten}</div></section>')
    if b['typ'] == 'durchklick':
        # Galerie der Kund:innen-Seite zum Durchklicken (Jana: Klick aufs Bild öffnet Slider mit Titel und Beschreibung, Anna 16.10.2026)
        zusatz = (' loading="lazy"', ' hidden')  # Folgebilder ohne lazy, damit sie beim Weiterklicken schon geladen sind
        bilder = ''.join(f'<img src="{pre}{x["bild"]}" alt="{esc(x["alt"])}" width="{jpg_mass(basis / "website" / x["bild"])[0]}" height="{jpg_mass(basis / "website" / x["bild"])[1]}"{zusatz[i > 0]}>' for i, x in enumerate(b['bilder']))
        return (f'  <section class="cs-block cs-durchklick" aria-labelledby="dk-{b["id"]}"><div class="la-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="la-titel" id="dk-{b["id"]}">{trennen(esc(b["titel"]))}</h2>'
                + (f'<p>{esc(b["text"])}</p>' if b.get('text') else '') + f'</div>'
                f'<div class="dk-fenster"><button type="button" class="dk-bilder" title="Nächstes Bild">{bilder}</button></div></section>')
    if b['typ'] == 'seiten-spalten':
        # mehrere Unterseiten in voller Länge nebeneinander, oben je ein Etikett (Jana: drei Werkbereiche, Anna 15.10.2026)
        sp = ''.join(f'<figure class="ss-seite"><figcaption><span class="ss-pille">{esc(x["label"])}</span></figcaption>'
                     f'<div class="ss-fenster"><img src="{pre}{x["bild"]}" alt="{esc(x["alt"])}" width="{jpg_mass(basis / "website" / x["bild"])[0]}" height="{jpg_mass(basis / "website" / x["bild"])[1]}" loading="lazy"></div></figure>' for x in b['seiten'])
        return (f'  <section class="cs-block cs-seiten-spalten" aria-labelledby="ss-{b["id"]}"><div class="la-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="la-titel" id="ss-{b["id"]}">{trennen(esc(b["titel"]))}</h2>'
                + (f'<p>{esc(b["text"])}</p>' if b.get('text') else '') + f'</div><div class="ss-reihe" style="--n:{len(b["seiten"])}">{sp}</div></section>')
    if b['typ'] == 'foto':  # großes Foto-Mockup über die ganze Breite (Jana: Atelier mit Monitor, Anna 16.10.2026)
        w, h = jpg_mass(basis / 'website' / b['bild'])
        return f'  <figure class="cs-block cs-foto"><img src="{pre}{b["bild"]}" alt="{esc(b["alt"])}" width="{w}" height="{h}" loading="lazy"></figure>'
    if b['typ'] == 'kennzahlen':  # Zahlen als eigener Block an beliebiger Stelle (Bauer: nach dem Überblick, Anna 15.10.2026)
        z = ''.join(f'<li><span class="kz-zahl">{esc(x)}</span> <span>{trennen(esc(t))}</span></li>' for x, t in b['zahlen'])
        return f'  <ul class="cs-block cs-kennzahlen" role="list" aria-label="Projekt in Kürze">{z}</ul>'
    raise SystemExit('Unbekannter Bildblock: ' + b['typ'])


def zahlen(p):
    # Kennzahlen des Projekts direkt unter dem Einstieg (Anna 14.10.2026: „14 Seiten, 40 Projekte“ weiter nach oben, ohne „Seiten, Seiten“)
    if not p.get('zahlen'): return ''
    if p.get('_variante'):  # B (Anna 14.10.2026): Zahlen als Text unter dem Bild, nie darauf; Lesefolge „83 Seiten online“
        z = ''.join(f'<li><span class="kz-zahl">{esc(a)}</span> <span>{trennen(esc(b))}</span></li>' for a, b in p['zahlen'])
        return f'  <ul class="cs-kennzahlen" role="list" aria-label="Projekt in Kürze">{z}</ul>\n'
    z = ''.join(f'<div><dt>{esc(b)}</dt><dd>{esc(a)}</dd></div>' for a, b in p['zahlen'])
    return f'  <dl class="cs-zahlen">{z}</dl>\n'


def handy3d(bild, pre, alt, klasse='', zusatz='', start=0):
    # räumliches Handy mit Spiegelung (Anna 14.10.2026, Vorbild Behance „CreativMinds“): Seite scrollt im Bildschirm
    return (f'<div class="h3d {klasse}" style="--start: {start}%"><div class="h3d-bildschirm"><div class="h3d-seite"><img src="{pre}{bild}" alt="{esc(alt)}" loading="lazy">{zusatz}</div></div></div>')


def stimme(p, pre):
    s = next((x for x in I.STIMMEN if x['name'] == p.get('stimme')), None)
    if not s: return ''
    return ('  <section class="cs-stimme" aria-label="Kundenstimme">\n    <div class="stimmen">\n' + I.stimmen([s], pre) + '\n    </div>\n'
            f'    <p class="stimmen-quelle"><a class="textlink" href="{LINKEDIN}" target="_blank" rel="noopener">Empfehlung auf LinkedIn <span aria-hidden="true">↗</span></a></p>\n  </section>')


def projektseite(p, nr):
    pre = '../../'
    nxt = CASES[(nr + 1) % len(CASES)]
    farbe = p['cover']['farbe']
    texte = ''.join(f'    <div class="cs-kachel"><h2 class="gr-h3">{esc(a)}</h2><p>{esc(b)}</p></div>\n' for a, b in p.get('abschnitte', []))
    texte = f'  <section class="cs-texte" aria-label="Projekt in Kürze">\n{texte}  </section>\n' if texte else ''
    ablauf = ''
    def mit_anker(b):
        # Sprungziel für die Schritte im Ablauf: id auf das erste Element des Blocks
        h = block(b, pre)
        return re.sub(r'<(figure|section|div)\b', lambda m: f'<{m.group(1)} id="{b["anker"]}"', h, count=1) if b.get('anker') else h
    stimme_unten = stimme(p, pre)
    for b in p.get('bilder', []):
        if b.get('typ') == 'ergebnis' and b.get('stimme') and stimme_unten:
            b['_stimme_html'] = stimme_unten.replace('<section class="cs-stimme" aria-label="Kundenstimme">', '<div class="cs-stimme-innen">').replace('</section>', '</div>'); stimme_unten = ''
    if p.get('_variante'):
        # Seamless (Anna 14.10.2026): jeder Block liegt in einem Band über die volle Breite; der Verlauf beginnt mit der Endfarbe
        # des vorigen Bands (--von = letztes --bis), damit nirgends eine Kante entsteht; Arten: schraege (Bauer-Schräge mit gelbem
        # Streifen oben), eng (wenig Abstand), voll (ohne Seitenrand)
        teile, letzt = [], '#ffffff'
        for b in p.get('bilder', []):
            bd = b.get('band', {})
            von = bd.get('von', letzt); bis = bd.get('bis', von); letzt = bis
            kl = ' '.join(['nl-band'] + [f'nl-{a}' for a in bd.get('art', [])])
            stil = f'--von:{von};--bis:{bis}' + (f';--davor:{bd["davor"]}' if bd.get('davor') else '')
            teile.append(f'<div class="{kl}" style="{stil}">\n{mit_anker(b)}\n</div>')
        bilder = '\n'.join(teile)
    else:
        bilder = '\n'.join(mit_anker(b) for b in p.get('bilder', []))
    main = f'''<main id="inhalt" class="cs{' cs-nahtlos' if p.get('_variante') else ''}{(' ' + p['klasse']) if p.get('klasse') else ''}" style="--pc-farbe: {farbe}{p.get('stil', '')}">

  <section class="seitenkopf cs-kopf">
    <p class="meta brotkrumen"><a href="../">Projekte</a> / <span aria-current="page">{esc(p["kurzname"])}</span></p>
    <h1 class="cs-titel">{esc(p["kurzname"]).replace("Ingenieurbau", "Ingenieur&shy;bau")}</h1>
    {('<p class="cs-einleitung">' + esc(p['einleitung']) + '</p>') if p.get('einleitung') else ''}
    {fakten(p)}
  </section>

{buehne(p, pre)}

{zahlen(p)}{texte}{ablauf}
  <section class="cs-bilder" aria-label="Projekt im Detail">
{bilder}
  </section>

{stimme_unten}

  <nav class="cs-weiter" aria-label="Weitere Projekte">
    <a class="pk-bild" href="../{nxt["slug"]}/" tabindex="-1" aria-hidden="true">{I.cover(nxt, pre)}</a>
    <div>
      <p class="meta">Nächstes Projekt</p>
      <p class="cs-weiter-name"><a href="../{nxt["slug"]}/">{esc(nxt["kurzname"])} <span aria-hidden="true">→</span></a></p>
      <p class="gedaempft">{esc(nxt["satz"])}</p>
    </div>
  </nav>

</main>'''
    url = f'https://studio-aah.de/referenzen/{p["slug"]}/'
    titel = f'{p["kurzname"]}: {p["kopf"]} | STUDIO AAH!'
    ld = {"@context": "https://schema.org", "@type": "CreativeWork", "@id": url + '#projekt', "name": f'{p["kurzname"]} – {p["kopf"]}', "description": p['satz'], "url": url,
          "creator": {"@id": "https://studio-aah.de/#studio"}, "inLanguage": "de"}
    ziel = basis / 'website' / 'referenzen' / p['slug'] / 'index.html'
    ziel.parent.mkdir(parents=True, exist_ok=True)
    # Bilder mit Versionsnummer (Änderungszeit), damit Browser nach neuen Aufnahmen nicht das alte Bild zeigen (Anna 14.10.2026)
    def version(m):
        datei = basis / 'website' / m.group(2)
        return m.group(1) + m.group(2) + (f'?v={int(datei.stat().st_mtime) % 1000000}' if datei.exists() else '')
    main = re.sub(r'(\.\./\.\./)(bilder/[^"\'()\s?]+\.(?:jpg|jpeg|png|webp))', version, main)
    seite = rahmen('service/webdesign/index.html', main, titel, p['satz'], url, ld)
    if p.get('_variante') and not p.get('_haupt'):  # Entwurfs-Variante: nicht verlinkt, nicht für Suchmaschinen
        seite = seite.replace('</head>', '  <meta name="robots" content="noindex, nofollow">\n</head>', 1)
    ziel.write_text(seite, encoding='utf-8')
    print('geschrieben: referenzen/' + p['slug'] + '/')


def uebersicht():
    pre = '../'
    karten = '\n'.join(f'      <li>{I.projekt_karte(p, pre, h="h2")}</li>' for p in CASES + [x for x in ALLE if not x.get('case')])
    main = f'''<main id="inhalt">

  <section class="seitenkopf">
    <p class="meta">Referenzen</p>
    <h1 class="gr-xxl">Projekte</h1>
    <p class="alt-klein">Lösungen, die Unternehmen sichtbar machen.</p>
  </section>

  <section class="ref-uebersicht" aria-label="Alle Projekte">
    <ul class="ref-raster">
{karten}
    </ul>
  </section>

</main>'''
    url = 'https://studio-aah.de/referenzen/'
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": url, "name": "Projekte von STUDIO AAH!", "url": url, "inLanguage": "de",
          "hasPart": [{"@id": f'{url}{p["slug"]}/#projekt'} for p in CASES]}
    (basis / 'website' / 'referenzen' / 'index.html').write_text(
        rahmen('profil/index.html', main, 'Projekte und Referenzen | STUDIO AAH!', 'Ausgewählte Projekte von STUDIO AAH!: Markenbildung, Websites und Druck für Unternehmen, Ärztinnen und Kreative.', url, ld), encoding='utf-8')
    print('geschrieben: referenzen/')


if __name__ == '__main__':
    uebersicht()
    for i, p in enumerate(CASES):
        # hauptvariante (Anna 15.10.2026: Bauer Variante B wird die Projektseite): dann keine Seite aus der Grundfassung,
        # die Variante erscheint unter der normalen Adresse und ist für Suchmaschinen sichtbar
        if not p.get('hauptvariante'): projektseite(p, i)
        # Varianten (Anna 14.10.2026: Variante B) – Blöcke aus der Hauptfassung per Nummer übernehmen, Felder weglassen oder ersetzen
        for k, liste in p.get('varianten', {}).items():
            bl, projekt = [], {}
            for e in liste:
                if 'projekt' in e:
                    projekt.update(e['projekt']); continue
                if 'aus' in e:
                    x = copy.deepcopy(p['bilder'][e['aus']])
                    for f in e.get('ohne', []): x.pop(f, None)
                    x.update(e.get('setze', {}))
                    if 'band' in e: x['band'] = e['band']
                    bl.append(x)
                else:
                    bl.append(e)
            haupt = p.get('hauptvariante') == k
            projektseite(dict(p, **projekt, bilder=bl, slug=p['slug'] if haupt else f'{p["slug"]}-{k}', _variante=k, _haupt=haupt), i)
