# Seitenfarbe je Seite (Anna 23.11.2026: „geh alle Seiten durch und zieh das neue Farbkonzept mutig durch“, Farb-Richtlinie 1.1).
# Setzt --lf (Voll), --lf-zart, --lf-hauch am <main id="inhalt">; CSS färbt damit Seitenkopf, Fragen und Abschluss.
# Läuft als letzter Schritt in alle-erzeugen.sh; idempotent. Leistungsseiten setzen ihre Farbe selbst (leistungsseiten.py).
import pathlib, re
W = pathlib.Path(__file__).resolve().parents[1] / 'website'
GELB, PINK, ORCHIDEE, MINT, HIMMEL, ROT = '#FFF329', '#FF4FA3', '#EF87F9', '#07F0A5', '#5FD2FF', '#FF3B2F'
# Zwei verwandte Farben je Seite (Anna 23.11.2026: „ja, überall Paare“), wie auf den Leistungsseiten
FARBE = {
    'branchen/bau-ingenieurwesen-architektur': (GELB, MINT), 'branchen/handwerk-gebaeudetechnik': (ROT, PINK), 'branchen/industrie-maschinenbau': (HIMMEL, ORCHIDEE),
    'branchen/energie-umwelttechnik': (MINT, GELB), 'branchen/gesundheit-praxen': (ORCHIDEE, PINK), 'branchen/beratung-dienstleistung': (PINK, ROT), 'branchen/software-it': (HIMMEL, MINT),
    'fuer-wen': (ORCHIDEE, PINK), 'neue-kunden': (PINK, ROT), 'fachkraefte': (MINT, HIMMEL), 'ki-im-team': (GELB, MINT), 'employer-branding': (MINT, GELB),
    'referenzen': (HIMMEL, ORCHIDEE), 'blog': (GELB, MINT), 'preise': (GELB, MINT), 'website-check': (HIMMEL, ORCHIDEE), 'marken-regelwerk': (ROT, PINK), 'ki-arbeits-setup': (GELB, MINT),
    'kontakt': (MINT, HIMMEL), 'selbsttest': (ORCHIDEE, PINK), 'ki-zeitrechner': (ORCHIDEE, HIMMEL), 'demokratie-braucht-sichtbarkeit': (PINK, ORCHIDEE), 'aah-codes': (GELB, ROT),
}
def stufen(paar):
    a, b = paar
    mix = lambda v, t: '#%02X%02X%02X' % tuple(round(int(v[i:i + 2], 16) * (1 - t) + 255 * t) for i in (1, 3, 5))
    return f'--lf: {a}; --lf-zart: {mix(a, .55)}; --lf-hauch: {mix(a, .8)}; --lf2: {b}; --lf2-zart: {mix(b, .55)}'
n = 0
for pfad, v in FARBE.items():
    f = W / pfad / 'index.html'
    if not f.exists(): continue
    h = f.read_text(encoding='utf-8')
    neu = re.sub(r'<main id="inhalt"( class="[^"]*")?( data-seitenfarbe style="[^"]*")?', lambda m: f'<main id="inhalt"{m.group(1) or ""} data-seitenfarbe style="{stufen(v)}"', h, count=1)
    if neu != h: f.write_text(neu, encoding='utf-8'); n += 1
print('Seitenfarben gesetzt:', n)
