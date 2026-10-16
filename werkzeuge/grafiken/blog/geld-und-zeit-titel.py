# Erzeugt werkzeuge/grafiken/blog/geld-und-zeit-titel.svg – Titelbild Blog „Geld und Zeit“ (Fassung 3, 13.10.2026)
# Website als Wireframe in feinen Linien, davor die Bauhaus-Figur (Konstruktionsvorschlag), die ein blaues Modul einsetzt.
# Farben laut CI. Blau berührt nie Schwarz: weiße Fugen bzw. Abstand.
# Aufruf vom Repository-Ordner: python3 werkzeuge/grafiken/blog/geld-und-zeit-titel.py
# Danach als Bild rendern (Schriften Anton und JetBrains Mono einbinden) und als website/bilder/blog-geld-und-zeit.webp speichern.
import math, os
SCH, BL, WS, GR, MG = '#0e1011', '#2a5fe6', '#fff', '#d6d8d9', '#9a9d9e'
FUGE = 14  # sichtbar 7 px: bleibt auch in kleinen Vorschauen als Fuge erkennbar
# Arme sitzen immer direkt am Rumpf, ohne Abstand (Anna, 13.10.2026): Drehpunkt innen im Rumpf, Arm entsprechend länger
SCHULTER_X, SCHULTER_Y, ARM = 30, -290, 132
# Herabhängender Arm abgespreizt, Hand sichtbar neben dem Rock – nie dahinter versteckt; Beine mit Eckenradius 4 (Anna, 13.10.2026)
ARM_UNTEN, BEIN_RADIUS = -34, 4

def balken(sx, sy, w, laenge=120, breite=16, hand=True, radius=0):
    r = f' rx="{radius}"' if radius else ''
    t = f'<g transform="translate({sx} {sy}) rotate({w})"><rect x="{-breite/2}" y="0" width="{breite}" height="{laenge}"{r} fill="{SCH}"/>'
    if hand: t += f'<circle cx="0" cy="{laenge+4}" r="11" fill="{SCH}"/>'
    return t + '</g>'

def ende(sx, sy, w, laenge=120):
    a = math.radians(w); return sx - (laenge + 4) * math.sin(a), sy + (laenge + 4) * math.cos(a)

def figur(arm_l, arm_r, bein_l, bein_r, blick=1):
    t = balken(-22, -150, bein_l, 150, 18, False, BEIN_RADIUS) + balken(22, -150, bein_r, 150, 18, False, BEIN_RADIUS)
    t += '<rect x="-42" y="-302" width="84" height="96" fill="%s"/>' % SCH
    t += balken(-SCHULTER_X, SCHULTER_Y, arm_l, ARM) + balken(SCHULTER_X, SCHULTER_Y, arm_r, ARM)
    t += f'<path d="M-80 -150 A80 80 0 0 1 80 -150 Z" fill="{BL}" stroke="{WS}" stroke-width="{FUGE}" paint-order="stroke"/>'
    t += f'<circle cx="0" cy="-352" r="34" fill="{SCH}"/><circle cx="{12*blick}" cy="-358" r="7" fill="{WS}"/>'
    return t

linie = f'fill="none" stroke="{SCH}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
grau = f'stroke="{MG}" stroke-width="2"'
s = []
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">')
s.append(f'<defs><pattern id="punkte" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="1.3" fill="{GR}"/></pattern></defs>')
s.append(f'<rect width="1200" height="800" fill="{WS}"/><rect width="1200" height="800" fill="url(#punkte)"/>')
# Browserfenster
s.append(f'<g {linie}><rect x="80" y="90" width="700" height="600" rx="16" fill="{WS}"/><line x1="80" y1="136" x2="780" y2="136"/>'
         f'<circle cx="110" cy="113" r="6"/><circle cx="132" cy="113" r="6"/><circle cx="154" cy="113" r="6"/><rect x="196" y="101" width="330" height="24" rx="12"/>'
         f'<line x1="470" y1="170" x2="510" y2="170"/><line x1="530" y1="170" x2="570" y2="170"/><line x1="590" y1="170" x2="630" y2="170"/>'
         f'<rect x="440" y="210" width="300" height="200" rx="8"/><line x1="440" y1="210" x2="740" y2="410" stroke-width="1.5"/><line x1="740" y1="210" x2="440" y2="410" stroke-width="1.5"/>'
         f'<rect x="120" y="460" width="190" height="190" rx="10"/><rect x="330" y="460" width="190" height="190" rx="10" stroke-dasharray="8 8"/><rect x="540" y="460" width="200" height="190" rx="10"/>'
         f'<circle cx="150" cy="492" r="12"/><path d="M558 504 L582 504 L570 480 Z"/></g>')
s.append(f'<g {grau}><line x1="120" y1="340" x2="390" y2="340"/><line x1="120" y1="360" x2="360" y2="360"/><line x1="120" y1="380" x2="320" y2="380"/>'
         f'<line x1="140" y1="540" x2="280" y2="540"/><line x1="140" y1="560" x2="250" y2="560"/><line x1="560" y1="540" x2="710" y2="540"/><line x1="560" y1="560" x2="680" y2="560"/></g>')
s.append(f'<rect x="120" y="162" width="74" height="16" rx="3" fill="{SCH}"/>')
s.append(f'<text x="214" y="118" font-family="JetBrains Mono, monospace" font-size="13" fill="{MG}">ihre-firma.de</text>')
s.append(f'<text x="118" y="250" font-family="Anton, Impact, sans-serif" font-size="54" fill="{SCH}" letter-spacing="1">IHRE</text>')
s.append(f'<text x="118" y="312" font-family="Anton, Impact, sans-serif" font-size="54" fill="{SCH}" letter-spacing="1">WEBSITE</text>')
s.append(f'<rect x="120" y="404" width="140" height="34" rx="17" fill="{BL}"/><rect x="142" y="418" width="58" height="6" rx="3" fill="{WS}"/>'
         f'<path d="M216 421 h22 m-8 -7 l8 7 l-8 7" fill="none" stroke="{WS}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
# Uhr (Zeit) und Preisschild (Geld), feine Linien
s.append(f'<g transform="translate(1040 170)"><circle r="80" fill="{WS}" stroke="{SCH}" stroke-width="2"/><path d="M12 -12 L12 -66 A54 54 0 0 1 66 -12 Z" fill="{BL}"/>'
         f'<g stroke="{SCH}" stroke-width="2" stroke-linecap="round"><line x1="0" y1="-80" x2="0" y2="-70"/><line x1="80" y1="0" x2="70" y2="0"/><line x1="0" y1="80" x2="0" y2="70"/><line x1="-80" y1="0" x2="-70" y2="0"/>'
         f'<line x1="0" y1="0" x2="0" y2="-56" stroke-width="3"/><line x1="0" y1="0" x2="44" y2="0" stroke-width="3"/></g><circle r="5" fill="{SCH}"/></g>')
s.append(f'<g transform="translate(600 610) rotate(-6)"><path d="M0 0 H170 L212 50 L170 100 H0 Z" fill="{WS}" stroke="{SCH}" stroke-width="2" stroke-linejoin="round"/>'
         f'<circle cx="180" cy="50" r="8" fill="none" stroke="{SCH}" stroke-width="2"/><text x="18" y="38" font-family="JetBrains Mono, monospace" font-size="14" fill="{SCH}">AB</text>'
         f'<text x="16" y="82" font-family="Anton, Impact, sans-serif" font-size="42" fill="{SCH}" letter-spacing="1">2.450 €</text></g>')
# Boden und Figur, die das blaue Modul in die gestrichelte Lücke setzt
s.append(f'<line x1="840" y1="700" x2="1150" y2="700" stroke="{SCH}" stroke-width="2"/>')
fx, fy, k = 985, 700, 1.0
s.append(f'<g transform="translate({fx} {fy}) scale({k})">' + figur(124, ARM_UNTEN, 16, -12, blick=-1) + '</g>')
hx, hy = ende(-SCHULTER_X, SCHULTER_Y, 124, ARM); hx, hy = fx + hx * k, fy + hy * k
s.append(f'<rect x="{hx-120}" y="{hy-76}" width="120" height="86" fill="{BL}" stroke="{WS}" stroke-width="{FUGE}" paint-order="stroke" transform="rotate(6 {hx-60} {hy-33})"/>')
s.append(f'<path d="M{hx-134} {hy+2} Q{hx-205} {hy+75} 430 520" fill="none" stroke="{SCH}" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round"/>')
s.append('</svg>')
ziel = os.path.join(os.path.dirname(__file__), 'geld-und-zeit-titel.svg')
open(ziel, 'w').write('\n'.join(s) + '\n')
print('geschrieben:', ziel)
