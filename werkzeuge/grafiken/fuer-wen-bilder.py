# Erzeugt die Bilder für den Abschnitt „Für wen“ der Startseite (Entwurf 16.10.2026):
#   werkzeuge/grafiken/fuer-wen-mittelstand.svg   – Team aus drei Bauhaus-Figuren vor einer Website mit vielen Unterseiten
#   werkzeuge/grafiken/fuer-wen-selbststaendige.svg – eine Figur winkt neben einem Onepager
# Vereine & Kultur nutzen das bekannte Foto website/bilder/programm-haende.webp.
# Bildidee: eine Figur (Selbstständige) – ein Team (Mittelstand) – viele Hände (Vereine).
# Figur wie in werkzeuge/grafiken/blog/geld-und-zeit-titel.py (Konstruktion nach Anna, 13.10.2026). Blau berührt nie Schwarz.
# Aufruf vom Repository-Ordner: python3 werkzeuge/grafiken/fuer-wen-bilder.py
# Danach rendern und als website/bilder/fuer-wen-*.webp (1200 × 900) speichern.
import math, os
SCH, BL, WS, GR, MG, CR = '#0e1011', '#2a5fe6', '#fff', '#d6d8d9', '#9a9d9e', '#eeece7'
FUGE = 14
SCHULTER_X, SCHULTER_Y, ARM = 30, -290, 132
ARM_UNTEN, BEIN_RADIUS = -34, 4
B, H = 1200, 900


def balken(sx, sy, w, laenge=120, breite=16, hand=True, radius=0):
    r = f' rx="{radius}"' if radius else ''
    t = f'<g transform="translate({sx} {sy}) rotate({w})"><rect x="{-breite/2}" y="0" width="{breite}" height="{laenge}"{r} fill="{SCH}"/>'
    if hand: t += f'<circle cx="0" cy="{laenge+4}" r="11" fill="{SCH}"/>'
    return t + '</g>'


def ende(sx, sy, w, laenge=ARM):
    a = math.radians(w); return sx - (laenge + 4) * math.sin(a), sy + (laenge + 4) * math.cos(a)


def figur(arm_l, arm_r, bein_l=16, bein_r=-12, blick=1, mann=False):
    # mann=True: Entwurf 16.10.2026 – statt Halbkreis-Rock ein blauer Balken als Hose (Bauhaus-Grundform), Beine gerader
    t = balken(-22, -150, bein_l, 150, 18, False, BEIN_RADIUS) + balken(22, -150, bein_r, 150, 18, False, BEIN_RADIUS)
    t += f'<rect x="-42" y="-302" width="84" height="96" fill="{SCH}"/>'
    t += balken(-SCHULTER_X, SCHULTER_Y, arm_l, ARM) + balken(SCHULTER_X, SCHULTER_Y, arm_r, ARM)
    if mann:
        t += f'<rect x="-46" y="-212" width="92" height="66" fill="{BL}" stroke="{WS}" stroke-width="{FUGE}" paint-order="stroke"/>'
    else:
        t += f'<path d="M-80 -150 A80 80 0 0 1 80 -150 Z" fill="{BL}" stroke="{WS}" stroke-width="{FUGE}" paint-order="stroke"/>'
    t += f'<circle cx="0" cy="-352" r="34" fill="{SCH}"/><circle cx="{12*blick}" cy="-358" r="7" fill="{WS}"/>'
    return t


def grund():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {B} {H}" width="{B}" height="{H}">'
            f'<defs><pattern id="punkte" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="1.3" fill="{GR}"/></pattern></defs>'
            f'<rect width="{B}" height="{H}" fill="{WS}"/><rect width="{B}" height="{H}" fill="url(#punkte)"/>')


LINIE = f'fill="{WS}" stroke="{SCH}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
GRAU = f'stroke="{MG}" stroke-width="2" stroke-linecap="round"'


def textzeilen(x, y, breiten, abstand=20):
    return ''.join(f'<line x1="{x}" y1="{y+i*abstand}" x2="{x+b}" y2="{y+i*abstand}" {GRAU}/>' for i, b in enumerate(breiten))


def fenster(x, y, w, h):
    return (f'<g {LINIE}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16"/><line x1="{x}" y1="{y+46}" x2="{x+w}" y2="{y+46}"/>'
            f'<circle cx="{x+30}" cy="{y+23}" r="6"/><circle cx="{x+52}" cy="{y+23}" r="6"/><circle cx="{x+74}" cy="{y+23}" r="6"/></g>')


def schreiben(name, inhalt):
    ziel = os.path.join(os.path.dirname(__file__), name)
    open(ziel, 'w').write(inhalt + '\n')
    print('geschrieben:', ziel)


# --- Mittelstand: Website mit vielen Unterseiten (gestapelte Seiten), davor ein Team ---
s = [grund()]
for i in (2, 1):  # Unterseiten dahinter
    s.append(fenster(90 + i * 34, 70 - i * 30, 640, 560))
s.append(fenster(90, 70, 640, 560))
x0, y0 = 90, 70
s.append(f'<rect x="{x0+40}" y="{y0+76}" width="70" height="14" rx="3" fill="{SCH}"/>')
s.append(''.join(f'<line x1="{x0+330+i*80}" y1="{y0+83}" x2="{x0+380+i*80}" y2="{y0+83}" stroke="{SCH}" stroke-width="2" stroke-linecap="round"/>' for i in range(3)))
s.append(f'<rect x="{x0+40}" y="{y0+124}" width="300" height="34" rx="4" fill="{SCH}"/><rect x="{x0+40}" y="{y0+170}" width="230" height="34" rx="4" fill="{SCH}"/>')
s.append(textzeilen(x0 + 40, y0 + 232, [260, 230, 190]))
s.append(f'<rect x="{x0+40}" y="{y0+300}" width="150" height="38" rx="19" fill="{BL}"/>')
s.append(f'<g {LINIE}><rect x="{x0+380}" y="{y0+124}" width="220" height="214" rx="10"/></g>'
         f'<path d="M{x0+420} {y0+300} L{x0+470} {y0+230} L{x0+505} {y0+275} L{x0+530} {y0+250} L{x0+565} {y0+300} Z" fill="{GR}"/><circle cx="{x0+545}" cy="{y0+170}" r="16" fill="{GR}"/>')
for i in range(3):  # Karten: Leistungen, Branchen, Karriere
    kx = x0 + 40 + i * 190
    s.append(f'<g {LINIE}><rect x="{kx}" y="{y0+372}" width="170" height="150" rx="10"/></g>')
    s.append([f'<circle cx="{kx+32}" cy="{y0+404}" r="14" fill="{SCH}"/>',
              f'<rect x="{kx+18}" y="{y0+390}" width="28" height="28" fill="{SCH}"/>',
              f'<path d="M{kx+18} {y0+418} L{kx+46} {y0+418} L{kx+32} {y0+390} Z" fill="{SCH}"/>'][i])
    s.append(textzeilen(kx + 18, y0 + 446, [120, 100, 80]))
s.append(f'<line x1="680" y1="840" x2="1150" y2="840" stroke="{SCH}" stroke-width="2"/>')
k = 0.7  # Arme nie im Schritt oder am Rock der Nachbarn (Anna 16.10.2026): hängende Arme nur nach außen, sonst nach oben
team = [(765, figur(150, -165, 14, -10, blick=-1)),                            # Frau zeigt auf die Website, anderer Arm oben
        (935, figur(160, -160, 6, -6, blick=-1, mann=True)),                   # Mann hält ein blaues Modul hoch
        (1095, figur(165, -150, 12, -14, blick=-1))]                          # Frau jubelt, beide Arme oben
for fx, f in team:
    s.append(f'<g transform="translate({fx} 840) scale({k})">{f}</g>')
# blaues Modul über dem Mann, mit weißer Fuge zu den Händen
s.append(f'<rect x="{935-62}" y="{840-k*500}" width="124" height="70" fill="{BL}" stroke="{WS}" stroke-width="{FUGE}" paint-order="stroke"/>')
s.append('</svg>')
schreiben('fuer-wen-mittelstand.svg', '\n'.join(s))

# --- Selbstständige: ein Onepager (lange Seite) und eine Figur, die winkt ---
s = [grund()]
px, py, pw, ph = 170, 60, 420, 780
s.append(f'<g {LINIE}><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="36"/></g>')
s.append(f'<rect x="{px+150}" y="{py+22}" width="120" height="10" rx="5" fill="{SCH}"/>')
s.append(f'<rect x="{px+36}" y="{py+70}" width="60" height="12" rx="3" fill="{SCH}"/><g stroke="{SCH}" stroke-width="3" stroke-linecap="round"><line x1="{px+350}" y1="{py+70}" x2="{px+384}" y2="{py+70}"/><line x1="{px+350}" y1="{py+82}" x2="{px+384}" y2="{py+82}"/></g>')
s.append(f'<rect x="{px+36}" y="{py+118}" width="290" height="40" rx="4" fill="{SCH}"/><rect x="{px+36}" y="{py+170}" width="210" height="40" rx="4" fill="{SCH}"/>')
s.append(textzeilen(px + 36, py + 240, [320, 290, 250]))
s.append(f'<rect x="{px+36}" y="{py+306}" width="160" height="42" rx="21" fill="{BL}"/>')
s.append(f'<g {LINIE}><rect x="{px+36}" y="{py+380}" width="348" height="190" rx="12"/></g><circle cx="{px+210}" cy="{py+460}" r="48" fill="{GR}"/>')
s.append(f'<rect x="{px+36}" y="{py+600}" width="170" height="24" rx="3" fill="{SCH}"/>')
s.append(textzeilen(px + 36, py + 652, [330, 300, 210]))
s.append(f'<g stroke="{MG}" stroke-width="2" stroke-dasharray="4 8" stroke-linecap="round"><line x1="{px+pw+40}" y1="{py+40}" x2="{px+pw+40}" y2="{py+ph-40}"/></g>')
s.append(f'<line x1="700" y1="840" x2="1120" y2="840" stroke="{SCH}" stroke-width="2"/>')
s.append(f'<g transform="translate(900 840) scale(1.5)">{figur(34, -150, 14, -12, blick=-1)}</g>')
s.append('</svg>')
schreiben('fuer-wen-selbststaendige.svg', '\n'.join(s))

