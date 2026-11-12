# Hero-Illustrationen der Seiten „Für wen“, Problem-, Branchen- und Produktseite (Anna, 10.11.2026: „im Hero auf der anderen
# Seite eine Illustration im Bauhaus-Stil … möglichst genau erzählen, was die Seite will: das Problem oder die Lösung oder beides“).
# Bauhaus-Grundformen in den CI-Farben, Figur nach Oskar Schlemmer wie in werkzeuge/grafiken/blog/geld-und-zeit-titel.py:
# Kopf Kreis mit weißem Auge, Rumpf Quadrat, blauer Halbkreis-Rock mit weißer Fuge, Glieder als Balken, Arme direkt am Rumpf,
# herabhängender Arm abgespreizt, Beine mit Eckenradius 4. Blau berührt nie Schwarz (weiße Fugen).
# Aufruf vom Repository-Ordner: python3 werkzeuge/grafiken/fuer-wen-hero.py  → website/bilder/fuer-wen/<name>.svg
import math, pathlib

SCH, BL, WS, GR, MG = '#0e1011', '#2a5fe6', '#fff', '#d6d8d9', '#9a9d9e'
# Farbtafel „modernes Bauhaus“ wie im Hero der Startseite und im Farbband des Fußes (Anna 10.11.2026: Illustrationen farbig)
# Seit 12.11.2026 nur Schwarz, Weiß und Blau (Anna: „komplett zu bunt … alle einfach schwarz-weiß-blau“); die Namen bleiben als Rollen
ROT, PINK, ROSA, GELB = SCH, BL, GR, BL
FUGE = 14
ZIEL = pathlib.Path(__file__).resolve().parent.parent.parent / 'website' / 'bilder' / 'fuer-wen'
B, H, BODEN = 800, 640, 600


def balken(sx, sy, w, laenge=120, breite=16, hand=True, radius=0):
    r = f' rx="{radius}"' if radius else ''
    t = f'<g transform="translate({sx} {sy}) rotate({w})"><rect x="{-breite/2}" y="0" width="{breite}" height="{laenge}"{r} fill="{SCH}"/>'
    if hand:
        t += f'<circle cx="0" cy="{laenge+4}" r="11" fill="{SCH}"/>'
    return t + '</g>'


def figur(x, y, s=1.0, arm_l=30, arm_r=-30, bein_l=6, bein_r=-6, blick=1, helm=False, rock=None):
    """Füße auf (x, y). Winkel: 0 = Arm hängt, +30 links abgespreizt, -30 rechts abgespreizt, -135 rechts nach oben, 135 links nach oben."""
    t = balken(-22, -150, bein_l, 150, 18, False, 4) + balken(22, -150, bein_r, 150, 18, False, 4)
    t += f'<rect x="-42" y="-302" width="84" height="96" fill="{SCH}"/>'
    t += balken(-30, -290, arm_l, 132) + balken(30, -290, arm_r, 132)
    t += f'<path d="M-80 -150 A80 80 0 0 1 80 -150 Z" fill="{rock or BL}" stroke="{WS}" stroke-width="{FUGE}" paint-order="stroke"/>'
    t += f'<circle cx="0" cy="-352" r="34" fill="{SCH}"/><circle cx="{12*blick}" cy="-358" r="7" fill="{WS}"/>'
    if helm:  # Bauhelm als blauer Halbkreis mit weißer Fuge
        t += f'<path d="M-44 -372 A44 44 0 0 1 44 -372 Z" fill="{GELB}" stroke="{WS}" stroke-width="10" paint-order="stroke"/>'
    return f'<g transform="translate({x} {y}) scale({s})">{t}</g>'


def browser(x, y, w, h, inhalt=''):
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{WS}" stroke="{SCH}" stroke-width="4"/>'
         f'<line x1="{x}" y1="{y+40}" x2="{x+w}" y2="{y+40}" stroke="{SCH}" stroke-width="3"/>')
    for i in range(3):
        t += f'<circle cx="{x+24+i*20}" cy="{y+20}" r="6" fill="{SCH}"/>'
    return t + inhalt


def knopf(x, y, w=150, h=46):
    """Blauer Anfrage-Button mit weißem Pfeil."""
    m = y + h / 2
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{BL}"/>'
            f'<rect x="{x+24}" y="{m-4}" width="{w-82}" height="8" rx="4" fill="{WS}"/>'
            f'<path d="M{x+w-46} {m-12} L{x+w-30} {m} L{x+w-46} {m+12}" fill="none" stroke="{WS}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')


def zeilen(x, y, breiten, abstand=22, farbe=GR, dicke=10):
    return ''.join(f'<rect x="{x}" y="{y+i*abstand}" width="{b}" height="{dicke}" rx="{dicke/2}" fill="{farbe}"/>' for i, b in enumerate(breiten))


def pfad(d, farbe=SCH):
    return f'<path d="{d}" fill="none" stroke="{farbe}" stroke-width="4" stroke-dasharray="4 12" stroke-linecap="round" marker-end="url(#spitze)"/>'


def boden():
    return f'<line x1="20" y1="{BODEN}" x2="{B-20}" y2="{BODEN}" stroke="{SCH}" stroke-width="3"/>'


def svg(titel, inhalt):
    kopf = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {B} {H}" width="{B}" height="{H}" role="img"><title>{titel}</title>'
            f'<defs><marker id="spitze" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 Z" fill="{SCH}"/></marker></defs>')
    return kopf + inhalt + '</svg>'


BILDER = {}

# 1 Neue Kunden: Die Mundpropaganda (zwei graue Figuren) verblasst; neue Kundschaft kommt über die Website und landet beim Anfrage-Button.
t = boden()
t += f'<g opacity=".35">{figur(80, BODEN, .42, 30, -100, blick=1)}{figur(170, BODEN, .42, 100, -30, blick=-1)}</g>'
t += f'<path d="M100 380 h70 a14 14 0 0 1 14 14 v28 a14 14 0 0 1 -14 14 h-40 l-14 16 v-16 h-16 a14 14 0 0 1 -14 -14 v-28 a14 14 0 0 1 14 -14z" fill="{ROSA}" opacity=".6"/>'
t += browser(250, 110, 380, 300, zeilen(280, 180, [220, 300, 260]) + f'<rect x="280" y="260" width="140" height="90" rx="8" fill="{GELB}"/><rect x="440" y="260" width="160" height="90" rx="8" fill="{PINK}"/>' + knopf(450, 360 - 2, 150, 40))
t += figur(330, BODEN, .5, 30, -150, blick=1)
t += figur(660, BODEN, .32, 30, -30, blick=-1, rock=ROT) + figur(730, BODEN, .32, 30, -30, blick=-1, rock=PINK)
t += pfad('M670 450 C 670 420, 650 400, 616 386') + pfad('M740 450 C 740 400, 700 380, 618 372')
BILDER['neue-kunden'] = ('Neue Kundschaft findet über die Website zum Anfrage-Button, während die Mundpropaganda verblasst', t)

# 2 Fachkräfte: Großer grauer Konzernturm, daneben Ihr Haus mit offener blauer Tür und Karriereseite; Fachkräfte kommen zu Ihnen.
t = boden()
t += f'<rect x="40" y="90" width="190" height="510" fill="{GR}"/>' + ''.join(f'<rect x="{60+c*56}" y="{120+r*60}" width="34" height="34" fill="{WS}"/>' for c in range(3) for r in range(7))
t += f'<rect x="420" y="330" width="250" height="270" fill="{SCH}"/><path d="M400 340 L545 210 L690 340 Z" fill="{SCH}"/>'
t += f'<rect x="510" y="440" width="70" height="160" fill="{BL}" stroke="{WS}" stroke-width="10" paint-order="stroke"/>'
t += f'<g transform="translate(545 290) scale(.55)"><rect x="-34" y="-34" width="68" height="68" transform="rotate(45)" fill="{ROSA}"/><circle cx="-24" cy="-24" r="34" fill="{ROSA}"/><circle cx="24" cy="-24" r="34" fill="{ROSA}"/></g>'
t += browser(600, 120, 170, 150, zeilen(618, 180, [110, 90]) + knopf(618, 222, 110, 34))
t += figur(370, BODEN, .42, 30, -150, blick=1)
t += figur(270, BODEN, .32, 30, -30, blick=1, rock=ROT)
t += pfad('M300 470 C 360 430, 440 430, 505 470')
BILDER['fachkraefte'] = ('Fachkräfte gehen am großen grauen Konzern vorbei zu Ihrem Haus mit offener Tür und Karriereseite', t)

# 3 KI im Team: Ein großer Bildschirm mit der KI als blauem Kreis in der Mitte, verbunden mit den Aufgaben des Teams;
#   die Figur erklärt, zwei aus dem Team schauen zu. Links ein grauer, ungenutzter Werkzeugstapel.
t = boden()
t += ''.join(f'<rect x="40" y="{470+i*42}" width="{150-i*14}" height="34" rx="6" fill="{GR}"/>' for i in range(3))
t += f'<rect x="250" y="90" width="480" height="320" rx="16" fill="{WS}" stroke="{SCH}" stroke-width="4"/><rect x="455" y="410" width="70" height="40" fill="{SCH}"/><rect x="400" y="450" width="180" height="14" rx="7" fill="{SCH}"/>'
t += f'<circle cx="490" cy="250" r="54" fill="{BL}"/>' + ''.join(
    f'<line x1="490" y1="250" x2="{x}" y2="{y}" stroke="{SCH}" stroke-width="3"/><rect x="{x-26}" y="{y-26}" width="52" height="52" rx="6" fill="{f}"/>'
    for (x, y), f in zip([(330, 150), (650, 150), (330, 350), (650, 350)], [ROT, GELB, PINK, ROSA]))
t += f'<circle cx="490" cy="250" r="54" fill="{BL}" stroke="{WS}" stroke-width="10" paint-order="stroke"/>'
t += figur(200, BODEN, .42, 30, -140, blick=1)
t += figur(640, BODEN, .34, 30, -30, blick=-1, rock=GELB) + figur(720, BODEN, .34, 30, -30, blick=-1, rock=PINK)
BILDER['ki-im-team'] = ('Eine Figur erklärt ihrem Team die KI als blauen Kreis, der mit den Aufgaben verbunden ist; daneben ungenutzte graue Werkzeuge', t)

# 4 Entlastung: Links trägt die Figur einen wackligen Stapel Aufgaben; in der Mitte nimmt die KI (blauer Kreis) Aufgaben ab;
#   rechts liegt alles ordentlich als aufgeschriebener Ablauf.
t = boden()
t += figur(130, BODEN, .42, 150, -150, blick=1)
t += ''.join(f'<rect x="{78+(i%2)*14-7}" y="{400-i*44}" width="90" height="38" rx="4" fill="{SCH if i%2 else MG}"/>' for i in range(7))
t += pfad('M230 260 C 280 230, 320 230, 350 260')
t += f'<rect x="340" y="250" width="170" height="170" rx="20" fill="{WS}" stroke="{SCH}" stroke-width="4"/><circle cx="425" cy="335" r="56" fill="{BL}"/>'
t += f'<rect x="395" y="420" width="60" height="180" fill="{SCH}"/>'
t += pfad('M515 335 C 545 335, 560 320, 585 300')
t += f'<rect x="585" y="160" width="170" height="230" rx="10" fill="{WS}" stroke="{SCH}" stroke-width="4"/>' + ''.join(
    f'<circle cx="612" cy="{200+i*44}" r="9" fill="{[ROT, GELB, PINK, BL][i]}"/><rect x="632" y="{194+i*44}" width="{100-i*10}" height="12" rx="6" fill="{SCH}"/>' for i in range(4))
t += figur(670, BODEN, .4, 30, -30, blick=-1, rock=ROSA)
BILDER['entlastung'] = ('Links trägt eine Figur einen wackligen Stapel Aufgaben, die KI als blauer Kreis nimmt Routine ab, rechts liegen die Abläufe ordentlich aufgeschrieben', t)

# 5 Bau: Kran und Gebäude aus Quadraten; daneben die Website mit dem Referenzprojekt; Figur mit Bauhelm zeigt darauf.
t = boden()
t += f'<rect x="70" y="80" width="16" height="520" fill="{SCH}"/><rect x="70" y="80" width="330" height="16" fill="{SCH}"/><line x1="320" y1="96" x2="320" y2="210" stroke="{SCH}" stroke-width="3"/><rect x="295" y="210" width="50" height="50" fill="{BL}" stroke="{WS}" stroke-width="10" paint-order="stroke"/>'
t += ''.join(f'<rect x="{150+c*62}" y="{352+r*62}" width="56" height="56" fill="{SCH if (c+r)%3 else [GELB, ROT, PINK, ROSA][(c+2*r) % 4]}"/>' for c in range(4) for r in range(4) if not (r == 0 and c == 3))
t += browser(470, 130, 300, 260, f'<rect x="490" y="190" width="120" height="120" fill="{SCH}"/><rect x="510" y="210" width="34" height="34" fill="{WS}"/><rect x="556" y="210" width="34" height="34" fill="{WS}"/>'
             + zeilen(630, 200, [120, 100, 80]) + knopf(490, 330, 140, 38))
t += figur(640, BODEN, .42, 30, -145, blick=-1, helm=True)
BILDER['bau'] = ('Ein Bauprojekt aus Quadraten mit Kran, daneben dasselbe Projekt als Referenzseite auf der Website; eine Figur mit Bauhelm zeigt darauf', t)

# 6 Elektro: Blitz, Steckdose und Kabel zur Karriereseite; Fachkräfte folgen dem Kabel.
t = boden()
t += f'<path d="M150 70 L70 300 L150 300 L100 520 L260 240 L175 240 L230 70 Z" fill="{GELB}"/>'
t += f'<rect x="300" y="420" width="110" height="110" rx="18" fill="{WS}" stroke="{SCH}" stroke-width="4"/><circle cx="335" cy="475" r="10" fill="{SCH}"/><circle cx="375" cy="475" r="10" fill="{SCH}"/>'
t += f'<path d="M410 475 C 480 475, 470 300, 520 300" fill="none" stroke="{SCH}" stroke-width="8" stroke-linecap="round"/>'
t += browser(510, 120, 260, 260, zeilen(535, 180, [180, 150, 120]) + f'<rect x="535" y="250" width="200" height="50" rx="8" fill="{PINK}"/>' + knopf(535, 318, 150, 40))
t += figur(560, BODEN, .36, 30, -140, blick=-1) + figur(700, BODEN, .36, 30, -30, blick=-1, rock=ROT)
BILDER['elektro'] = ('Ein blauer Blitz und eine Steckdose, deren Kabel zur Karriereseite führt; Fachkräfte kommen dazu', t)

# 7 Software: Großer Bildschirm mit Oberfläche; drei Menschen aus dem Entscheidungsteam schauen gemeinsam darauf, eine zeigt.
t = boden()
t += f'<rect x="120" y="70" width="560" height="340" rx="16" fill="{WS}" stroke="{SCH}" stroke-width="4"/><rect x="120" y="70" width="120" height="340" rx="16" fill="{SCH}"/><rect x="200" y="70" width="40" height="340" fill="{SCH}"/>'
t += zeilen(150, 110, [60, 60, 60, 60], 44, MG, 12)
t += f'<rect x="270" y="100" width="380" height="36" rx="8" fill="{GR}"/>' + ''.join(f'<rect x="{270+i*130}" y="160" width="120" height="110" rx="10" fill="{[GELB, BL, PINK][i]}"/>' for i in range(3))
t += f'<rect x="270" y="290" width="380" height="90" rx="10" fill="{ROSA}"/><path d="M520 210 L520 250 L530 241 L538 258 L545 255 L537 238 L550 238 Z" fill="{SCH}" stroke="{WS}" stroke-width="3"/>'
t += f'<rect x="370" y="410" width="60" height="40" fill="{SCH}"/><rect x="320" y="450" width="160" height="14" rx="7" fill="{SCH}"/>'
t += figur(180, BODEN, .36, 30, -140, blick=1) + figur(600, BODEN, .36, 30, -30, blick=-1, rock=ROT) + figur(700, BODEN, .3, 30, -30, blick=-1, rock=GELB)
BILDER['software'] = ('Ein großer Bildschirm mit einer klaren Software-Oberfläche; drei Menschen aus dem Entscheidungsteam schauen gemeinsam darauf', t)

# 8 Employer Branding: Haus mit Herz und blauer Fahne, ein Handy mit Bewerbungs-Button, Bewerber:innen kommen von beiden Seiten.
t = boden()
t += f'<rect x="270" y="300" width="260" height="300" fill="{SCH}"/><path d="M250 310 L400 180 L550 310 Z" fill="{SCH}"/>'
t += f'<rect x="398" y="70" width="8" height="120" fill="{SCH}"/><path d="M406 74 L486 100 L406 126 Z" fill="{ROT}"/>'
t += f'<g transform="translate(400 400)"><rect x="-34" y="-34" width="68" height="68" transform="rotate(45)" fill="{WS}"/><circle cx="-24" cy="-24" r="34" fill="{WS}"/><circle cx="24" cy="-24" r="34" fill="{WS}"/></g>'
t += f'<rect x="360" y="490" width="80" height="110" fill="{WS}"/>'
t += f'<rect x="600" y="170" width="150" height="270" rx="22" fill="{WS}" stroke="{SCH}" stroke-width="4"/>' + zeilen(624, 220, [100, 80, 90]) + f'<rect x="624" y="300" width="102" height="60" rx="8" fill="{GELB}"/>' + knopf(624, 380, 102, 34)
t += figur(130, BODEN, .36, 30, -30, blick=1, rock=PINK) + figur(210, BODEN, .32, 30, -30, blick=1, rock=GELB) + figur(660, BODEN, .34, 30, -30, blick=-1, rock=ROT)
t += pfad('M160 420 C 220 400, 280 440, 350 520') + pfad('M640 470 C 600 480, 520 500, 450 540')
BILDER['employer-branding'] = ('Ein Haus mit Herz und Fahne als Arbeitgebermarke, daneben ein Handy mit Bewerbungs-Button; Bewerber:innen kommen von beiden Seiten', t)

# 9 Übersicht „Für wen“: Vier Karten wie ein aufgefächertes Blatt, jede mit ihrem Symbol; die Figur zeigt darauf.
ICONS = [
    f'<rect x="-40" y="0" width="22" height="30" fill="{SCH}"/><rect x="-12" y="-18" width="22" height="48" fill="{SCH}"/><circle cx="30" cy="-30" r="12" fill="{BL}"/><rect x="18" y="-4" width="22" height="34" fill="{MG}"/>',
    f'<circle cx="-22" cy="-28" r="14" fill="{SCH}"/><rect x="-36" y="-6" width="28" height="40" fill="{SCH}"/><circle cx="22" cy="-28" r="14" fill="{BL}"/><rect x="8" y="-6" width="28" height="40" fill="{MG}"/>',
    f'<rect x="-40" y="-40" width="34" height="34" fill="{SCH}"/><circle cx="22" cy="-23" r="17" fill="{BL}"/><path d="M-40 34 L-23 0 L-6 34 Z" fill="{MG}"/><path d="M6 34 A17 17 0 0 1 40 34 Z" fill="{SCH}"/>',
    f'<path d="M-30 -6 L0 -44 L30 -6 Z" fill="{SCH}"/><rect x="-12" y="0" width="24" height="34" fill="{SCH}"/><circle cx="30" cy="24" r="11" fill="{BL}"/>']
t = boden()
for i, (w, x) in enumerate([(-18, 300), (-6, 400), (6, 500), (18, 600)]):
    t += (f'<g transform="translate({x} 330) rotate({w})"><rect x="-80" y="-120" width="160" height="230" rx="16" fill="{WS}" stroke="{SCH}" stroke-width="4"/>'
          f'<rect x="-80" y="-120" width="160" height="26" rx="12" fill="{[ROT, GELB, PINK, ROSA][i]}"/><g transform="translate(0 -6)">{ICONS[i]}</g><rect x="-50" y="60" width="100" height="10" rx="5" fill="{GR}"/><rect x="-50" y="80" width="70" height="10" rx="5" fill="{GR}"/></g>')
t += figur(140, BODEN, .44, 30, -140, blick=1)
BILDER['fuer-wen'] = ('Vier Karten wie ein aufgefächertes Kartenblatt, jede mit dem Symbol eines Problems; eine Figur zeigt darauf', t)


# 10 Industrie & Maschinenbau (12.11.2026): Fabrikhalle mit Sheddach und Schornstein, ein Zahnrad (Zackenkreis);
#    daneben die Website mit Produktkacheln; eine Figur zeigt darauf.
t = boden()
t += f'<rect x="60" y="360" width="330" height="240" fill="{SCH}"/>' + ''.join(f'<path d="M{60+i*82} 360 L{60+i*82} 290 L{142+i*82} 360 Z" fill="{SCH}"/>' for i in range(4))
t += f'<rect x="320" y="170" width="34" height="190" fill="{SCH}"/>' + ''.join(f'<rect x="{90+i*72}" y="420" width="44" height="44" fill="{[GELB, WS, ROT, WS][i]}"/>' for i in range(4))
t += f'<g fill="{ROT}"><circle cx="180" cy="200" r="58"/>' + ''.join(f'<circle cx="{180+66*math.cos(2*math.pi*i/12):.1f}" cy="{200+66*math.sin(2*math.pi*i/12):.1f}" r="13"/>' for i in range(12)) + f'</g><circle cx="180" cy="200" r="22" fill="{WS}"/>'
t += browser(450, 110, 320, 280, zeilen(475, 170, [200, 160]) + ''.join(f'<rect x="{475+i*94}" y="225" width="80" height="80" rx="8" fill="{[GELB, PINK, ROSA][i]}"/>' for i in range(3)) + knopf(475, 325, 150, 40))
t += figur(640, BODEN, .4, 30, -145, blick=-1)
BILDER['industrie'] = ('Eine Fabrikhalle mit Sheddach, Schornstein und rotem Zahnrad, daneben die Website mit Produktkacheln; eine Figur zeigt darauf', t)

# 11 Energie & Umwelttechnik: Windrad aus Balken, gelbe Sonne, Solarmodul aus schwarzen Quadraten; die Website erklärt und führt zur Anfrage.
t = boden()
t += f'<circle cx="300" cy="120" r="52" fill="{GELB}"/>'
t += f'<rect x="132" y="230" width="16" height="370" fill="{SCH}"/>' + ''.join(f'<g transform="translate(140 230) rotate({w})"><rect x="-9" y="-150" width="18" height="150" rx="9" fill="{SCH}"/></g>' for w in (0, 120, 240)) + f'<circle cx="140" cy="230" r="16" fill="{WS}" stroke="{SCH}" stroke-width="6"/>'
t += f'<g transform="translate(250 470) skewX(-18)">' + ''.join(f'<rect x="{c*52}" y="{r*44}" width="46" height="38" fill="{SCH}"/>' for c in range(3) for r in range(2)) + '</g>'
t += f'<rect x="300" y="558" width="12" height="42" fill="{SCH}"/><rect x="380" y="558" width="12" height="42" fill="{SCH}"/>'
t += browser(470, 140, 300, 260, zeilen(495, 200, [180, 140]) + f'<rect x="495" y="250" width="110" height="70" rx="8" fill="{ROSA}"/><rect x="620" y="250" width="125" height="70" rx="8" fill="{GELB}"/>' + knopf(495, 340, 150, 40))
t += figur(690, BODEN, .36, 30, -30, blick=-1, rock=ROT)
BILDER['energie'] = ('Ein Windrad, eine gelbe Sonne und ein Solarmodul, daneben eine Website, die das Angebot erklärt und zur Anfrage führt', t)

# 12 Gesundheit & Praxen: Ein Haus mit Herz als Praxis, ein Handy mit Terminkalender (ein Feld gewählt); eine Figur hält das Handy.
t = boden()
t += f'<rect x="60" y="320" width="270" height="280" fill="{SCH}"/><path d="M40 330 L195 200 L350 330 Z" fill="{SCH}"/>'
t += f'<g transform="translate(195 400) scale(.9)"><rect x="-34" y="-34" width="68" height="68" transform="rotate(45)" fill="{ROSA}"/><circle cx="-24" cy="-24" r="34" fill="{ROSA}"/><circle cx="24" cy="-24" r="34" fill="{ROSA}"/></g>'
t += f'<rect x="160" y="500" width="70" height="100" fill="{WS}"/>'
t += f'<rect x="470" y="110" width="200" height="340" rx="26" fill="{WS}" stroke="{SCH}" stroke-width="4"/>' + zeilen(495, 150, [120, 90])
t += ''.join(f'<rect x="{495+c*38}" y="{210+r*38}" width="30" height="30" rx="5" fill="{GELB if (c, r) == (2, 1) else GR}"/>' for c in range(4) for r in range(4)) + knopf(495, 380, 150, 40)
t += figur(390, BODEN, .4, 30, -140, blick=1) + figur(720, BODEN, .32, 30, -30, blick=-1, rock=PINK)
BILDER['gesundheit'] = ('Eine Praxis als Haus mit Herz, daneben ein Handy mit Terminkalender und gewähltem Termin; zwei Figuren', t)

# 13 Beratung & Dienstleistung: Zwei Figuren im Gespräch mit Sprechblasen; dahinter die Website mit Angebot und Termin-Button.
t = boden()
t += browser(400, 80, 360, 280, zeilen(425, 140, [240, 200, 260]) + f'<rect x="425" y="220" width="150" height="70" rx="8" fill="{PINK}"/><rect x="590" y="220" width="145" height="70" rx="8" fill="{GELB}"/>' + knopf(425, 305, 150, 40))
t += f'<rect x="150" y="470" width="300" height="14" rx="7" fill="{SCH}"/><rect x="200" y="484" width="12" height="116" fill="{SCH}"/><rect x="388" y="484" width="12" height="116" fill="{SCH}"/>'
t += f'<rect x="70" y="200" width="170" height="80" rx="20" fill="{ROSA}"/><path d="M120 280 L110 312 L150 280 Z" fill="{ROSA}"/>'
t += f'<rect x="300" y="390" width="120" height="60" rx="18" fill="{GELB}"/>'
t += figur(120, BODEN, .4, 30, -60, blick=1) + figur(520, BODEN, .4, 60, -30, blick=-1, rock=ROT)
BILDER['beratung'] = ('Zwei Figuren im Gespräch am Tisch mit Sprechblasen, dahinter eine Website mit Angebot und Termin-Button', t)


if __name__ == '__main__':
    ZIEL.mkdir(parents=True, exist_ok=True)
    for name, (titel, inhalt) in BILDER.items():
        (ZIEL / f'{name}.svg').write_text(svg(titel, inhalt), encoding='utf-8')
        print('geschrieben:', f'website/bilder/fuer-wen/{name}.svg')
