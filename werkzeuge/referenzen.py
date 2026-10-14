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
                      + handy3d(b['handy'], pre, b['handy_alt'], 'iph') + '</div>')
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
        features = ''.join(f'<figure class="vd-feature"><div class="vd-fenster"><img src="{pre}{bild}" alt="{esc(alt)}" loading="lazy"></div><figcaption class="meta">{esc(titel)}</figcaption></figure>' for bild, titel, alt in b.get('features', []))
        return (f'  <section class="cs-block cs-visual" aria-labelledby="vd-titel">\n    <div class="vd-text"><p class="meta">{esc(b["meta"])}</p><h2 class="bn-titel" id="vd-titel">{esc(b["titel"])}</h2><ul>{punkte}</ul></div>\n'
                f'    <div class="vd-icon"><img src="{pre}{b["favicon"]}" alt="Favicon von Wolfgang Bauer Ingenieurbau" width="512" height="512" loading="lazy"><span class="meta">{esc(b["favicon_text"])}</span></div>\n'
                f'    <figure class="vd-varianten"><img src="{pre}{b["varianten"]}" alt="{esc(b["varianten_alt"])}" loading="lazy"><figcaption class="meta">{esc(b["varianten_text"])}</figcaption></figure>\n'
                + (f'    <div class="vd-features">{features}</div>\n' if features else '') + '  </section>')
    if b['typ'] == 'personas':
        # Zwei Zielgruppen, zwei Sprachen (Anna 14.10.2026): Auftraggeber gesiezt, Bewerber geduzt.
        # Ruhig wie bei Apple (Anna 14.10.2026: „zu viele Schrifttypen und Farben“): eine Schrift, eine Akzentfarbe, Personen als Zeilen
        def person(x):
            return (f'<li class="pe-person"><img src="{pre}{x["bild"]}" alt="" width="800" height="1000" loading="lazy"><div>'
                    f'<p class="pe-name">{esc(x["name"])}</p><p class="pe-rolle">{esc(x["rolle"].replace(" · ", ", "))}</p>'
                    f'<blockquote>„{esc(x["zitat"])}“</blockquote><p class="pe-sucht"><span>Sucht zuerst</span>{" · ".join(esc(t) for t in x["sucht"])}</p></div></li>')
        def seite(s):
            beispiele = ''.join(f'<li>„{esc(x)}“</li>' for x in s['beispiele'])
            return (f'<div class="pe-seite"><p class="pe-anrede">„{esc(s["anrede"])}“</p><p class="pe-gruppe">{esc(s["meta"])}</p>'
                    f'<h3 class="pe-titel">{esc(s["titel"])}</h3><p class="pe-ton">{esc(s["ton"])}</p>'
                    f'<ul class="pe-personen">{"".join(person(x) for x in s["personas"])}</ul>'
                    f'<div class="pe-beispiele"><p class="pe-klein">So klingt es auf der Website</p><ul>{beispiele}</ul></div></div>')
        return (f'  <section class="cs-block cs-personas" aria-labelledby="pe-titel"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3" id="pe-titel">{esc(b["titel"])}</h2>'
                f'<p class="weg-einleitung">{esc(b["text"])}</p><div class="pe-zwei">{seite(b["auftraggeber"])}{seite(b["bewerber"])}</div>'
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
        return (f'  <section class="cs-block cs-galerie" aria-labelledby="ga-{b["id"]}"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3" id="ga-{b["id"]}">{esc(b["titel"])}</h2>'
                + (f'<p class="weg-einleitung">{esc(b["text"])}</p>' if b.get('text') else '') + f'<div class="ga-raster">{f}</div></section>')
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
        halb = (len(li) + 1) // 2
        spalten = ''.join(f'<figure class="grafik grafik-prozess"><ol class="zeitleiste" start="{s + 1}">{"".join(li[s:s + halb])}</ol></figure>' for s in (0, halb))
        return (f'  <section class="cs-block cs-prozess" aria-labelledby="ablauf-titel"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3" id="ablauf-titel">{esc(b["titel"])}</h2>'
                + (f'<p class="weg-einleitung">{esc(b["text"])}</p>' if b.get('text') else '') + f'<div class="cs-prozess-spalten">{spalten}</div></section>')
    if b['typ'] == 'klickstrecke':
        # Klickstrecke als Treppe: Schritte versetzt, Beschriftung neben der Karte statt darauf (Anna 14.10.2026)
        punkte = ''.join(f'<li>{esc(x)}</li>' for x in b['punkte'])
        stufen = ''.join(f'<li class="kl-stufe{" kl-oder" if oder else ""}" style="--n:{i}"><span class="kl-label"><b>{i + 1:02d}</b>{esc(titel)}</span>'
                         f'<div class="kl-fenster"><img src="{pre}{bild}" alt="{esc(titel)}" loading="lazy"></div></li>' for i, (bild, titel, oder) in enumerate(b['stufen']))
        return (f'  <section class="cs-block cs-klick" aria-labelledby="klick-titel">\n    <div class="kl-text"><p class="meta">{esc(b["meta"])}</p><h2 class="kr-titel" id="klick-titel">{b["titel_html"]}</h2>'
                f'<p>{esc(b["text"])}</p><ul>{punkte}</ul></div>\n    <ol class="kl-treppe">{stufen}</ol>\n  </section>')
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
            eingaben = ''.join(f'<span class="st-eingabe" data-text="{esc(x)}" style="--x:{ex};--t:{ey};--w:{ew}"></span>' for x, ex, ey, ew in s.get('eingaben', []))
            notizen = ''.join(f'<span class="st-notiz st-notiz-{s["phase"]}" style="left:{nx}%;top:{ny}%;--r:{(-2.5 if j % 2 else 2)}deg">{esc(n)}</span>' for j, (n, nx, ny, nt) in enumerate(s.get('notizen', [])))
            szenen += (f'<div class="st-szene" data-i="{i}"><div class="st-zoom"><div class="st-seite"><img src="{pre}{s["bild"]}" alt="{esc(s["alt"])}" loading="lazy">{eingaben}</div></div>{notizen}</div>')
        kapitel = ''.join(f'<button type="button" class="st-kapitel" data-ziel="{i}">{esc(s["kapitel"])}</button>' for i, s in enumerate(b['szenen']) if s.get('kapitel'))
        daten = json.dumps([{k: s.get(k) for k in ('pfad', 'phase', 'titel', 'von', 'bis', 'dauer', 'notizen', 'zoom', 'klick', 'tippen_ab')} for s in b['szenen']], ensure_ascii=False)
        return (f'  <figure class="cs-block cs-story" data-story aria-label="{esc(b["titel"])}">\n    <figcaption class="cs-block-kopf"><p class="meta">{esc(b["meta"])}</p><h2 class="gr-h3">{esc(b["titel"])}</h2></figcaption>\n'
                f'    <div class="st-rahmen"><span class="cs-etikett st-phase">{esc(b["alt_text"])}</span>'
                f'<div class="st-browser"><div class="vf-leiste"><span class="vf-adresse">bauer-ingbau.de/</span></div><div class="st-fenster">{szenen}'
                f'<span class="vf-zeiger" aria-hidden="true"></span><div class="vf-blende" aria-hidden="true"><b>{esc(b["blende_text"])}</b></div></div></div>'
                f'<div class="st-leiste"><button type="button" class="ks-knopf st-knopf" aria-label="Film anhalten">❚❚</button><div class="st-kapitelreihe">{kapitel}</div>'
                f'<p class="st-titel"></p></div></div>\n'
                f'    <script type="application/json" class="st-daten" data-alt="{esc(b["alt_text"])}" data-neu="{esc(b["neu_text"])}">{daten}</script>\n  </figure>')
    if b['typ'] in ('fotofilm', 'buch'):
        # Foto-Mockup (Canva, Anna 14.10.2026: passend zur Zielgruppe): Foto mit Maske liegt über der Seite, die im Bildschirm läuft
        fo = b['foto']
        schirme = ''
        for s in b['schirme']:
            if b['typ'] == 'fotofilm':
                szenen = ''.join(f'<div class="st-szene" data-i="{i}"><div class="st-zoom"><div class="st-seite"><img src="{pre}{z["bild"]}" alt="{esc(z["alt"])}" loading="lazy">'
                                 + ''.join(f'<span class="st-eingabe" data-text="{esc(x)}" style="--x:{ex};--t:{ey};--w:{ew}"></span>' for x, ex, ey, ew in z.get('eingaben', []))
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
        if not b.get('text'):
            return f'  <div class="cs-block fm-block">{szene}</div>'
        punkte = ''.join(f'<li>{esc(x)}</li>' for x in b.get('punkte', []))
        return (f'  <section class="cs-block fm-mit-text{" fm-dunkel" if b.get("dunkel") else ""}" aria-labelledby="fm-{b["id"]}">\n    <div class="fm-text"><p class="meta">{esc(b["meta"])}</p>'
                f'<h2 class="kr-titel" id="fm-{b["id"]}">{b["titel_html"]}</h2><p>{esc(b["text"])}</p>' + (f'<ul>{punkte}</ul>' if punkte else '') + f'</div>\n    {szene}\n  </section>')
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
    ablauf = ''
    def mit_anker(b):
        # Sprungziel für die Schritte im Ablauf: id auf das erste Element des Blocks
        h = block(b, pre)
        return re.sub(r'<(figure|section|div)\b', lambda m: f'<{m.group(1)} id="{b["anker"]}"', h, count=1) if b.get('anker') else h
    bilder = '\n'.join(mit_anker(b) for b in p.get('bilder', []))
    main = f'''<main id="inhalt" class="cs" style="--pc-farbe: {farbe}">

  <section class="seitenkopf cs-kopf">
    <p class="meta brotkrumen"><a href="../">Projekte</a> / <span aria-current="page">{esc(p["kurzname"])}</span></p>
    <h1 class="cs-titel">{esc(p["kurzname"]).replace("Ingenieurbau", "Ingenieur&shy;bau")}</h1>
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
