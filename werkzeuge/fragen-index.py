# Fragen-Index für das Frag-Feld im Hero der Startseite (Anna 16.11.2026, Konzept Stufe 1):
# sammelt alle häufigen Fragen mit Antwort aus den fertigen Seiten unter website/ (eine Quelle: was auf der Website steht)
# und schreibt website/daten/fragen.json. Die Suche läuft nur im Browser (js/frag.js), nichts wird gesendet.
# Aufruf im Repository-Ordner (läuft in alle-erzeugen.sh nach den Seiten-Generatoren):  python3 werkzeuge/fragen-index.py
import html, json, re

from gemeinsam import WEBSITE, WERKZEUGE

# Reihenfolge: speziellere Seiten zuerst; bei gleicher Frage gewinnt die erste
VORRANG = ['service/', 'ki-arbeits-setup/', 'website-check/', 'employer-branding/', 'marken-regelwerk/', 'branchen/', 'preise/', 'profil/', '']


def text(s):
    s = re.sub(r'</?span[^>]*>', '', s)   # Inline-Spans (z. B. ohne-umbruch) ohne Leerzeichen entfernen
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


ABK = re.compile(r'\b(Dr|Nr|ca|bzw|inkl|z\. B|u\. a|vgl|bspw|evtl)\. ')


def saetze(t):
    """In Sätze teilen; „STUDIO AAH!“, Zahlen wie „2.450 €“ und Abkürzungen wie „Dr.“ bleiben ganz."""
    t = ABK.sub(lambda m: m.group(1) + '.\u2060 ', t.replace('STUDIO AAH!', 'STUDIO AAH\u00a7'))
    return [x.replace('STUDIO AAH\u00a7', 'STUDIO AAH!').replace('\u2060', '').strip() for x in re.split(r'(?<=[.?!])\s+(?=[A-ZÄÖÜ„])', t) if x.strip()]


def kuerzen(x, laenge=160):
    """Stichpunkt ohne Schlusspunkt, lange Sätze an einer Wortgrenze gekürzt."""
    x = x.rstrip('.')
    return x if len(x) <= laenge else x[:laenge].rsplit(' ', 1)[0] + ' …'


def rang(pfad):
    return next(i for i, v in enumerate(VORRANG) if pfad.startswith(v))


def main():
    seiten = sorted((p for p in WEBSITE.rglob('index.html') if 'entwurf' not in str(p) and '/danke' not in str(p)),
                    key=lambda p: (rang(str(p.parent.relative_to(WEBSITE)) + '/'), str(p)))
    eintraege, gesehen = [], set()
    for p in seiten:
        rel = str(p.parent.relative_to(WEBSITE))
        url = '' if rel == '.' else rel + '/'
        t = p.read_text(encoding='utf-8')
        titel = text(re.search(r'<title>(.*?)</title>', t, re.S).group(1)).split(' | ')[0]
        for m in re.finditer(r'<details class="faq-eintrag"[^>]*>\s*<summary>(.*?)</summary>\s*<div class="faq-antwort">(.*?)</div>\s*</details>', t, re.S):
            frage, antwort = text(m.group(1)), text(m.group(2))
            if frage.lower() in gesehen or not antwort:
                continue
            gesehen.add(frage.lower())
            eintraege.append({'f': frage, 'a': antwort, 'u': url, 's': titel})
    # Themen (kuratiert, Anna 17.11.2026: freie Suche über alle Fragen war zu ungenau): Antwort aus der genannten Frage
    nach_frage = {e['f']: e for e in eintraege}
    themen = []
    for t in json.loads((WERKZEUGE / 'inhalte' / 'hero-themen.json').read_text(encoding='utf-8'))['themen']:
        if 'antwort' in t:
            links = t.get('links') or [[t['seite'], t['url']]]
            themen.append({'g': t['g'], 'a': t['antwort'], 'p': t.get('punkte', []), 'l': links})
            continue
        e = nach_frage.get(t['frage'])
        if not e:
            raise SystemExit(f'Frage nicht auf der Website gefunden: {t["frage"]}')
        # Wie eine KI-Übersicht bei Google (Anna 17.11.2026): Kurzfassung, ein paar Stichpunkte, Link zur Quelle
        satz = saetze(e['a'])
        kurz = satz.pop(0)
        if kurz == 'Ja.':   # freundlicher (Anna 17.11.2026: „ja klar, motivierender und netter“)
            kurz = 'Ja, klar!'
        while len(kurz) < 60 and satz:   # „Ja.“ allein ist keine Zusammenfassung
            kurz += ' ' + satz.pop(0)
        themen.append({'g': t['g'], 'a': kurz, 'p': [kuerzen(x) for x in satz[:3]], 'l': [[e['s'].split(':')[0].split(' – ')[0], e['u']]]})   # Linktext = Kern des Seitentitels
    ziel = WEBSITE / 'daten' / 'fragen.json'
    ziel.parent.mkdir(exist_ok=True)
    ziel.write_text(json.dumps(themen, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f'Frag-Feld: {len(themen)} Themen (aus {len(eintraege)} Fragen auf {len(seiten)} Seiten)')


if __name__ == '__main__':
    main()
