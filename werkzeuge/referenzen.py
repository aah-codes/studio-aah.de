# Erzeugt die Projektübersicht (website/referenzen/index.html) und je Projekt mit "case": true eine Projektseite
# (website/referenzen/<slug>/index.html) aus werkzeuge/inhalte/projekte.json – Aufbau wie bei Behance (Anna 14.10.2026):
# Kopf mit Eckdaten, großes Titelbild oder Film, kurze Texte nur aus Quellen, danach Bildblöcke in voller Breite.
# Kopf und Fuß kommen von der Profilseite (Übersicht) bzw. der Webdesign-Seite (Projektseiten, gleiche Ordnertiefe).
# Aufruf im Repository-Ordner:  python3 werkzeuge/referenzen.py
import html, importlib.util, json, pathlib, re

basis = pathlib.Path(__file__).resolve().parent.parent
esc = lambda s: html.escape(s, quote=False)
_spec = importlib.util.spec_from_file_location('inhalte', basis / 'werkzeuge' / 'inhalte-erzeugen.py')
I = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(I)
ALLE = I.PROJEKTE
CASES = [p for p in ALLE if p.get('case')]
TRENNEN = {'Zielgruppenführung': 'Zielgruppen&shy;führung', 'Eignungsnachweis': 'Eignungs&shy;nachweis'}


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
    zeilen = [('Branche', esc(p['branche'])), ('Leistungen', esc(p['leistungen'])), ('Zeitraum', esc(p['zeitraum']))] + ([('Website', links)] if links else [])
    return '<dl class="cs-fakten">' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in zeilen) + '</dl>'


def wand(bilder, pre):
    # Einstieg wie bei Behance („Hedwig“, Anna 14.10.2026): viele Key-Screens schräg gestaffelt auf hellgrauer Fläche
    spalten = [bilder[i::3] for i in range(3)]
    return ('<div class="cs-wand"><div class="cs-wand-innen">' + ''.join('<div>' + ''.join(f'<img src="{pre}{b}" alt="" loading="lazy">' for b in s) + '</div>' for s in spalten)
            + '</div></div>')


def buehne(p, pre):
    if p.get('wand'):
        return f'  <div class="cs-buehne">{wand(p["wand"], pre)}</div>'
    f = p.get('film')
    if f:  # Film mit Steuerung, startet nicht von selbst
        return (f'  <figure class="cs-buehne cs-film">\n    <video controls preload="none" playsinline poster="{pre}{f["vorschau"]}" src="{pre}{f["datei"]}"></video>\n'
                f'    <figcaption class="unsichtbar">{esc(f["titel"])}</figcaption>\n  </figure>')
    return f'  <div class="cs-buehne">{I.cover(p, pre)}</div>'


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
        return (f'  <figure class="cs-block cs-kachel cs-sitemap">\n    <figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2></figcaption>\n'
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
        stufen = ''.join(f'<li><span class="ds-mass">{esc(name)}<br><small>{esc(mass)}</small></span><span class="ds-probe" style="font-size: {gr}; font-weight: {gew}; line-height: {zh};{zusatz}">{esc(probe)}</span></li>'
                         for name, mass, gr, gew, zh, zusatz, probe in b['stufen'])
        return (f'  <figure class="cs-block cs-designsystem" style="--ds-schrift: {b["schrift_css"]}">\n    <figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2></figcaption>\n'
                f'    <div class="ds-farben">{farben}</div>\n'
                f'    <div class="ds-schrift"><div class="ds-schrift-kopf"><p class="ds-aa">Aa</p><p class="ds-name">{esc(b["schrift"])}</p><p class="ds-warum">{esc(b["warum"])}</p></div><ol class="ds-stufen">{stufen}</ol></div>\n  </figure>')
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
        text = f'<div class="bn-text"><p class="meta">{esc(b["meta"])}</p><h2 class="bn-titel">{esc(b["titel"])}</h2>' + (f'<p>{esc(b["text"])}</p>' if b.get('text') else '') + '</div>'
        if b.get('muster'):
            inhalt = '<div class="bn-muster">' + ''.join(f'<img src="{pre}{m}" alt="{esc(a)}" loading="lazy">' for m, a in b['muster']) + '</div>'
        else:
            inhalt = (f'<div class="bn-geraete"><div class="bn-browser"><span class="bn-leiste"></span><div class="bn-fenster"><img src="{pre}{b["browser"]}" alt="{esc(b["browser_alt"])}" loading="lazy"></div></div>'
                      + handy3d(b['handy'], pre, b['handy_alt']) + '</div>')
        return f'  <section class="cs-block cs-buehne-bild" data-einblenden style="--bn-bild: url({pre}{b["hintergrund"]})">{text}{inhalt}</section>'
    if b['typ'] == 'weg':
        # Wireframes der wichtigsten Seiten als Weg (Anna 14.10.2026, Vorbild Behance „CreativMinds – UX Process“)
        schritte = ''
        for i, (bild, titel, unter, oder) in enumerate(b['schritte'], 1):
            kl = ' class="oder"' if oder else ''
            schritte += (f'<li{kl}><span class="weg-nr">{i:02d}</span><span class="weg-titel">{esc(titel)}</span>'
                         f'<div class="weg-bild"><img src="{pre}{bild}" alt="Wireframe: {esc(titel)}" loading="lazy"></div><span class="weg-unter">{esc(unter)}</span></li>')
        return (f'  <figure class="cs-block cs-kachel cs-weg">\n    <figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2>'
                + (f'<p class="weg-einleitung">{esc(b["text"])}</p>' if b.get('text') else '') + f'</figcaption>\n    <ol class="weg-schritte">{schritte}</ol>\n  </figure>')
    if b['typ'] == 'section':
        # eine echte Section groß im Browserfenster
        return (f'  <figure class="cs-block cs-section"><div class="cs-section-fenster"><img src="{pre}{b["bild"]}" alt="{esc(b["alt"])}" loading="lazy"></div>'
                + (f'<figcaption class="meta">{esc(b["titel"])}</figcaption>' if b.get('titel') else '') + '</figure>')
    if b['typ'] == 'handy-duo':
        # zwei räumliche Handys, versetzt, scrollen von selbst (Pause-Taste); rechts füllt sich das Formular (nachgestellt, nichts wird gesendet)
        felder = ''.join(f'<span class="hd-eingabe" data-text="{esc(x)}" style="left:{l:.2f}%;top:{o:.3f}%;width:{w:.2f}%"></span>' for x, l, o, w in b['eingaben'])
        return (f'  <section class="cs-block cs-handy-duo" data-handyduo aria-label="{esc(b["titel"])}">\n    <div class="hd-text"><p class="meta">{esc(b["meta"])}</p><h2 class="bn-titel">{esc(b["titel"])}</h2><p>{esc(b["text"])}</p>'
                f'<p><button type="button" class="ks-knopf hd-knopf" aria-label="Bewegung anhalten">❚❚</button></p></div>\n'
                f'    <div class="hd-buehne">{handy3d(b["links"], pre, b["links_alt"], "hd-links")}{handy3d(b["rechts"], pre, b["rechts_alt"], "hd-rechts", felder, b.get("form_start", 0))}</div>\n  </section>')
    if b['typ'] == 'visual-design':
        # Visual Design wie Behance „CreativMinds – Visual Language“ (Anna 14.10.2026): Entscheidungen, gewähltes Favicon, Varianten, zwei Features
        punkte = ''.join(f'<li><b>{esc(a)}</b> {esc(x)}</li>' for a, x in b['entscheidungen'])
        features = ''.join(f'<figure class="vd-feature"><div class="vd-fenster"><img src="{pre}{bild}" alt="{esc(alt)}" loading="lazy"></div><figcaption class="meta">{esc(titel)}</figcaption></figure>' for bild, titel, alt in b['features'])
        return (f'  <section class="cs-block cs-visual" aria-labelledby="vd-titel">\n    <div class="vd-text"><p class="meta">{esc(b["meta"])}</p><h2 class="bn-titel" id="vd-titel">{esc(b["titel"])}</h2><ul>{punkte}</ul></div>\n'
                f'    <div class="vd-icon"><img src="{pre}{b["favicon"]}" alt="Favicon von Wolfgang Bauer Ingenieurbau" width="512" height="512" loading="lazy"><span class="meta">{esc(b["favicon_text"])}</span></div>\n'
                f'    <figure class="vd-varianten"><img src="{pre}{b["varianten"]}" alt="{esc(b["varianten_alt"])}" loading="lazy"><figcaption class="meta">{esc(b["varianten_text"])}</figcaption></figure>\n'
                f'    <div class="vd-features">{features}</div>\n  </section>')
    raise SystemExit('Unbekannter Bildblock: ' + b['typ'])


def zahlen(p):
    # Kennzahlen des Projekts direkt unter dem Einstieg (Anna 14.10.2026: „14 Seiten, 40 Projekte“ weiter nach oben, ohne „Seiten, Seiten“)
    if not p.get('zahlen'): return ''
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
    if p.get('ausgangslage'):
        # Ausgangslage (Anna 14.10.2026): weniger Text, Icons, dazu groß die alte Seite mit den Notizzetteln aus dem Expert-Review
        a = p['ausgangslage']
        zettel = ''.join(f'<span class="cs-zettel" style="left:{x}%;top:{y}%;--dreh:{d}deg">{esc(n)}</span>' for n, x, y, d in a['notizen'])
        karten = ''.join(f'<div class="cs-punkt"><img src="{pre}bilder/icons/{i}" alt="" width="400" height="400" loading="lazy"><div><h2>{esc(h)}</h2><ul>'
                         + ''.join(f'<li>{esc(x)}</li>' for x in liste) + '</ul></div></div>' for i, h, liste in a['karten'])
        texte = (f'  <section class="cs-ausgangslage" data-einblenden aria-label="Ausgangslage, Herausforderung und Ziele">\n'
                 f'    <figure class="cs-alt"><span class="cs-etikett">{esc(a["bild_text"])}</span><div class="cs-alt-bild"><img src="{pre}{a["bild"]}" alt="{esc(a["bild_alt"])}" loading="lazy">{zettel}</div></figure>\n'
                 f'    <div class="cs-punkte">{karten}</div>\n  </section>\n')
    ablauf = ''
    if p.get('ablauf'):
        # Schritte in einer Reihe von links nach rechts (NN/g 2017: Zickzack erschwert das Überfliegen), auf dem Handy untereinander
        li = ''.join(f'<li><span class="cs-schritt-nr">{i:02d}</span><p class="meta">{esc(z)}</p><h3>{esc(x)}</h3></li>' for i, (z, x) in enumerate(p['ablauf'], 1))
        ablauf = f'  <section class="cs-ablauf" aria-labelledby="ablauf-titel">\n    <p class="meta">Workflow</p>\n    <h2 class="gr-h3" id="ablauf-titel">So bin ich vorgegangen</h2>\n    <ol class="cs-schritte">{li}</ol>\n  </section>\n'
    bilder = '\n'.join(block(b, pre) for b in p.get('bilder', []))
    main = f'''<main id="inhalt" class="cs" style="--pc-farbe: {farbe}">

  <section class="seitenkopf cs-kopf">
    <p class="meta brotkrumen"><a href="../">Projekte</a> / <span aria-current="page">{esc(p["kurzname"])}</span></p>
    <h1 class="cs-titel">{esc(p["kurzname"]).replace("Ingenieurbau", "Ingenieur&shy;bau")}</h1>
    <p class="cs-satz">{esc(p["satz"])}</p>
    {fakten(p)}
  </section>

{buehne(p, pre)}

{zahlen(p)}{texte}{ablauf}
  <section class="cs-bilder" aria-label="Bilder aus dem Projekt">
{bilder}
  </section>

{stimme(p, pre)}

  <nav class="cs-weiter" aria-label="Weitere Projekte">
    <a class="pk-bild" href="../{nxt["slug"]}/" tabindex="-1" aria-hidden="true">{I.cover(nxt, pre)}</a>
    <div>
      <p class="meta">Nächstes Projekt</p>
      <p class="cs-weiter-name"><a href="../{nxt["slug"]}/">{esc(nxt["kurzname"])} <span aria-hidden="true">→</span></a></p>
      <p class="gedaempft">{esc(nxt["satz"])}</p>
      <p class="cs-knoepfe"><a class="button" href="{pre}kontakt/">Projekt anfragen <span aria-hidden="true">→</span></a> <a class="button button-zweit" href="../">Alle Projekte <span aria-hidden="true">→</span></a></p>
    </div>
  </nav>

</main>'''
    url = f'https://studio-aah.de/referenzen/{p["slug"]}/'
    titel = f'{p["kurzname"]}: {p["kopf"]} | STUDIO AAH!'
    ld = {"@context": "https://schema.org", "@type": "CreativeWork", "@id": url + '#projekt', "name": f'{p["kurzname"]} – {p["kopf"]}', "description": p['satz'], "url": url,
          "creator": {"@id": "https://studio-aah.de/#studio"}, "inLanguage": "de"}
    ziel = basis / 'website' / 'referenzen' / p['slug'] / 'index.html'
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(rahmen('service/webdesign/index.html', main, titel, p['satz'], url, ld), encoding='utf-8')
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
    for i, p in enumerate(CASES): projektseite(p, i)
