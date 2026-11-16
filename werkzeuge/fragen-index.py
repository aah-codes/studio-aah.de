# Fragen-Index für das Frag-Feld im Hero der Startseite (Anna 16.11.2026, Konzept Stufe 1):
# sammelt alle häufigen Fragen mit Antwort aus den fertigen Seiten unter website/ (eine Quelle: was auf der Website steht)
# und schreibt website/daten/fragen.json. Die Suche läuft nur im Browser (js/frag.js), nichts wird gesendet.
# Aufruf im Repository-Ordner (läuft in alle-erzeugen.sh nach den Seiten-Generatoren):  python3 werkzeuge/fragen-index.py
import html, json, re

from gemeinsam import WEBSITE

# Reihenfolge: speziellere Seiten zuerst; bei gleicher Frage gewinnt die erste
VORRANG = ['service/', 'ki-arbeits-setup/', 'website-check/', 'employer-branding/', 'marken-regelwerk/', 'branchen/', 'preise/', 'profil/', '']


def text(s):
    s = re.sub(r'</?span[^>]*>', '', s)   # Inline-Spans (z. B. ohne-umbruch) ohne Leerzeichen entfernen
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


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
    ziel = WEBSITE / 'daten' / 'fragen.json'
    ziel.parent.mkdir(exist_ok=True)
    ziel.write_text(json.dumps(eintraege, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f'Fragen-Index: {len(eintraege)} Fragen aus {len(seiten)} Seiten')


if __name__ == '__main__':
    main()
