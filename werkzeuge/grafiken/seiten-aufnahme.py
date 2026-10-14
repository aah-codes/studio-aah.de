#!/usr/bin/env python3
"""Nimmt Websites gestochen scharf auf (Anna 14.10.2026): ganze Seite und jeden Abschnitt einzeln, in doppelter Auflösung.
Steuert das installierte Google Chrome ohne Fenster über das DevTools-Protokoll – nur Python-Standardbibliothek, keine Installation.

Aufruf vom Repository-Ordner aus:
    python3 werkzeuge/grafiken/seiten-aufnahme.py ZIELORDNER URL [URL …]
    python3 werkzeuge/grafiken/seiten-aufnahme.py ZIELORDNER --sitemap https://kunde.de/page-sitemap1.xml
Optionen: --js "Code" (vor der Aufnahme im Browser ausführen, z. B. Slider weiterschalten) · --hover "CSS-Selektor" (Maus auf das Element, z. B. Mega-Menü; nimmt nur den sichtbaren Ausschnitt auf) · --felder (Lage der Formularfelder mit speichern, z. B. für nachgestellte Eingaben) · --handy (390 px breit, dreifache Auflösung) · --wireframe (Seite als Wireframe: graue Bildflächen, Textbalken) · --abschnitte "CSS-Selektor" (Standard: Kadence-Zeilen und <section>)
Ergebnis je Seite: <name>_ganz.jpg (sehr lange Seiten: _ganz_teil1.jpg, _teil2 …) und <name>_01.jpg, _02.jpg … (Abschnitte), dazu aufnahmen.json mit Lage und Text der Abschnitte.
Die Aufnahmen gehören nicht ins Repository; für die Website nur ausgewählte Ausschnitte verkleinert übernehmen.
"""
import base64, json, os, pathlib, re, socket, struct, subprocess, sys, tempfile, time, urllib.request

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PORT = int(os.environ.get('AUFNAHME_PORT', 9333))  # eigener Port, falls zwei Aufnahmen gleichzeitig laufen
STANDARD_ABSCHNITTE = 'main .kb-row-layout-wrap, main > section, main .wp-block-cover, main .wp-block-group.alignfull'
# Cookie-Banner und Chat-Knöpfe ausblenden (gängige WordPress-Erweiterungen)
# Wireframe-Ansicht (Anna 14.10.2026: fehlende Wireframes nachträglich aus der fertigen Seite erzeugen)
# Wireframe-Ansicht (Anna 14.10.2026: fehlende Wireframes nachträglich aus der fertigen Seite erzeugen, „ordentlich“):
# echte Überschriften und Texte in Grau, Bilder als Flächen mit Kreuz, Buttons als Rahmen, keine Farben
WIREFRAME = '''
* { color: #6b6f71 !important; -webkit-text-fill-color: currentColor !important; text-shadow: none !important; box-shadow: none !important;
    background-image: none !important; border-color: #c9cccd !important; font-family: -apple-system, "Helvetica Neue", Arial, sans-serif !important; }
h1, h2, h3, h4, h5, h6, h1 *, h2 *, h3 *, h4 * { color: #1d1f20 !important; }
html, body, header, footer, main, section, nav, article, aside, div, span, a, ul, li, p, figure, form, fieldset { background-color: transparent !important; }
body { background: #fff !important; }
section, .kb-row-layout-wrap, header, footer { outline: 1px dashed #c9cccd; outline-offset: -1px; }
img, video, iframe, picture, canvas { opacity: 0 !important; }
svg { filter: grayscale(1) opacity(.6); }
a.button, .button, button, .kb-button, .wp-block-button__link, input, select, textarea { background: #fff !important; border: 1.5px solid #3a3d3f !important; color: #1d1f20 !important; }
nav button, .dropdown-nav-toggle, .kadence-svg-iconset { border: 0 !important; }
'''
WIREFRAME_JS = '''(() => {
  const kreuz = 'linear-gradient(to top right, transparent calc(50% - 1px), #c9cccd calc(50% - 1px), #c9cccd calc(50% + 1px), transparent calc(50% + 1px)), linear-gradient(to bottom right, transparent calc(50% - 1px), #c9cccd calc(50% - 1px), #c9cccd calc(50% + 1px), transparent calc(50% + 1px)), #eef0f1';
  document.querySelectorAll('img, video, iframe, picture, canvas').forEach((e) => { const r = e.getBoundingClientRect(); if (r.width < 24 || r.height < 24) return;
    const d = document.createElement('div');
    d.style.cssText = `position:absolute;left:${r.left + scrollX}px;top:${r.top + scrollY}px;width:${r.width}px;height:${r.height}px;z-index:2147483646;pointer-events:none;border:1px solid #c9cccd;border-radius:4px`;
    d.style.setProperty('background', kreuz, 'important'); document.body.appendChild(d); });
  // Farben aus Inline-Stilen und Blöcken überschreiben: Überschriften dunkel, alles andere grau
  document.querySelectorAll('body *').forEach((e) => { e.style.setProperty('color', e.closest('h1,h2,h3,h4,h5,h6') ? '#1d1f20' : '#6b6f71', 'important'); });
  return 1; })()'''
STOERER = '#cmplz-cookiebanner-container, .cmplz-cookiebanner, #BorlabsCookieBox, #moove_gdpr_cookie_info_bar, .cky-consent-container, #cookie-law-info-bar, #usercentrics-root, .grecaptcha-badge, [data-hook="consent-banner-root"], [fs-cc="banner"], .fs-cc-banner_component, #wix-ad, #WIX_ADS'


class Verbindung:
    """Sehr kleiner WebSocket-Client (RFC 6455), reicht für das DevTools-Protokoll."""
    def __init__(self, url):
        m = re.match(r'ws://([^:/]+):(\d+)(/.*)', url)
        self.s = socket.create_connection((m.group(1), int(m.group(2))), timeout=120)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((f'GET {m.group(3)} HTTP/1.1\r\nHost: {m.group(1)}:{m.group(2)}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                        f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
        antwort = b''
        while b'\r\n\r\n' not in antwort: antwort += self.s.recv(1)
        self.nr = 0

    def _lies(self, n):
        b = b''
        while len(b) < n:
            teil = self.s.recv(n - len(b))
            if not teil: raise ConnectionError('Verbindung zu Chrome getrennt')
            b += teil
        return b

    def _rahmen(self):
        kopf = self._lies(2)
        laenge = kopf[1] & 127
        if laenge == 126: laenge = struct.unpack('>H', self._lies(2))[0]
        elif laenge == 127: laenge = struct.unpack('>Q', self._lies(8))[0]
        return kopf[0] & 15, self._lies(laenge)

    def senden(self, methode, **params):
        self.nr += 1
        daten = json.dumps({'id': self.nr, 'method': methode, 'params': params}).encode()
        maske = os.urandom(4)
        n = len(daten)
        kopf = bytes([0x81]) + (bytes([0x80 | n]) if n < 126 else bytes([0x80 | 126]) + struct.pack('>H', n) if n < 65536 else bytes([0x80 | 127]) + struct.pack('>Q', n))
        self.s.sendall(kopf + maske + bytes(b ^ maske[i % 4] for i, b in enumerate(daten)))
        nachricht = b''
        while True:
            op, teil = self._rahmen()
            nachricht += teil
            if op == 0 or op == 1:
                try: d = json.loads(nachricht)
                except ValueError: continue  # Nachricht kommt in mehreren Teilen
                nachricht = b''
                if d.get('id') == self.nr:
                    if 'error' in d: raise RuntimeError(f'{methode}: {d["error"]}')
                    return d.get('result', {})

    def js(self, ausdruck):
        r = self.senden('Runtime.evaluate', expression=ausdruck, awaitPromise=True, returnByValue=True)
        return r.get('result', {}).get('value')


def name_aus(url):
    pfad = re.sub(r'^https?://[^/]+', '', url).strip('/')
    return re.sub(r'[^a-z0-9]+', '-', pfad.lower()).strip('-') or 'startseite'


def speichern(pfad, b64):
    pathlib.Path(pfad).write_bytes(base64.b64decode(b64))


def aufnehmen(ws, url, ziel, handy, selektor, wireframe=False, felder=False, hover=None, vorher_js=None):
    breite, faktor = (390, 3) if handy else (1440, 2)
    ws.senden('Emulation.setDeviceMetricsOverride', width=breite, height=900, deviceScaleFactor=faktor, mobile=handy)
    ws.senden('Page.navigate', url=url)
    for _ in range(60):
        time.sleep(0.5)
        if ws.js('document.readyState') == 'complete': break
    # einmal ganz nach unten und zurück scrollen, damit nachgeladene Bilder und Einblend-Animationen fertig sind
    ws.js('''(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
            window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 1500)); return 1; })()''')
    ws.js(f'''(() => {{ const s = document.createElement('style'); s.textContent = `{STOERER} {{ display: none !important; }}
            *, *::before, *::after {{ animation-play-state: paused !important; transition: none !important; }}
            #masthead, #masthead *, .site-header, .kadence-sticky-header {{ transform: none !important; }}
            [class*="kb-animate"], [data-aos], .kt-animate, .aos-init {{ opacity: 1 !important; transform: none !important; }}`; document.head.appendChild(s); return 1; }})()''')
    if vorher_js:
        ws.js(f'(async () => {{ {vorher_js}; await new Promise(r => setTimeout(r, 1500)); return 1; }})()')
    if wireframe:
        ws.js(f'''(() => {{ const s = document.createElement('style'); s.textContent = {json.dumps(WIREFRAME)}; document.head.appendChild(s); return 1; }})()''')
        time.sleep(0.3)
        ws.js(WIREFRAME_JS)
    time.sleep(0.8)
    if hover:
        # Maus auf ein Element (z. B. Menüpunkt mit Mega-Menü) und nur den sichtbaren Ausschnitt aufnehmen
        pos = ws.js(f'''(() => {{ const e = document.querySelector({json.dumps(hover)}); if (!e) return null; const r = e.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }})()''')
        if not pos: raise SystemExit('Hover-Element nicht gefunden: ' + hover)
        ws.senden('Input.dispatchMouseEvent', type='mouseMoved', x=pos[0], y=pos[1])
        # Menüs, die sich per Klick öffnen (Kadence „sub-click“): Knopf anklicken
        ws.js(f'''(() => {{ const e = document.querySelector({json.dumps(hover)}); if (e.tagName === 'BUTTON') e.click(); return 1; }})()''')
        time.sleep(1.2)
        name = name_aus(url) + '_hover'
        bild = ws.senden('Page.captureScreenshot', format='jpeg', quality=82, clip={'x': 0, 'y': 0, 'width': breite, 'height': 900, 'scale': 1})
        speichern(f'{ziel}/{name}.jpg', bild['data'])
        print(name + ': Hover-Ausschnitt')
        return {'url': url, 'datei': f'{name}.jpg', 'breite': breite, 'faktor': faktor, 'hoehe': 900, 'abschnitte': [], 'hover': hover}
    hoehe = ws.js('Math.ceil(document.documentElement.scrollHeight)')
    # nur äußerste Abschnitte (verschachtelte Zeilen gehören zum umgebenden Abschnitt)
    abschnitte = ws.js(f'''(() => {{ const alle = [...document.querySelectorAll({json.dumps(selektor)})];
            return alle.filter(e => !alle.some(a => a !== e && a.contains(e))).map(e => {{ const r = e.getBoundingClientRect();
              return {{ y: Math.round(r.top + window.scrollY), h: Math.round(r.height), text: (e.innerText || '').trim().split('\\n').filter(Boolean).slice(0, 2).join(' · ').slice(0, 90) }}; }})
              .filter(a => a.h > 80); }})()''') or []
    feld_liste = ws.js('''[...document.querySelectorAll('input:not([type=hidden]):not([type=checkbox]):not([type=radio]):not([type=file]), select, textarea')]
        .filter(e => e.offsetWidth > 0).map(e => { const r = e.getBoundingClientRect(); const l = e.labels && e.labels[0] ? e.labels[0].innerText.trim() : (e.placeholder || e.name);
        return { x: Math.round(r.left), y: Math.round(r.top + scrollY), b: Math.round(r.width), h: Math.round(r.height), art: e.tagName.toLowerCase(), label: l.slice(0, 60) }; })''') if felder else None
    name = name_aus(url) + ('_handy' if handy else '') + ('_wireframe' if wireframe else '')
    # Chrome wiederholt bei Bildern über ca. 16 000 Pixel Höhe den oberen Teil: lange Seiten in Teilen aufnehmen
    teil = 16000 // faktor
    for n, y in enumerate(range(0, hoehe, teil), 1):
        ganz = ws.senden('Page.captureScreenshot', format='jpeg', quality=80, captureBeyondViewport=True,
                         clip={'x': 0, 'y': y, 'width': breite, 'height': min(teil, hoehe - y), 'scale': 1})
        speichern(f'{ziel}/{name}_ganz.jpg' if hoehe <= teil else f'{ziel}/{name}_ganz_teil{n}.jpg', ganz['data'])
    for i, a in enumerate(abschnitte, 1):
        bild = ws.senden('Page.captureScreenshot', format='jpeg', quality=80, captureBeyondViewport=True,
                         clip={'x': 0, 'y': a['y'], 'width': breite, 'height': a['h'], 'scale': 1})
        speichern(f'{ziel}/{name}_{i:02d}.jpg', bild['data'])
        a['datei'] = f'{name}_{i:02d}.jpg'
    print(f'{name}: {hoehe} px hoch, {len(abschnitte)} Abschnitte')
    e = {'url': url, 'datei': f'{name}_ganz.jpg', 'breite': breite, 'faktor': faktor, 'hoehe': hoehe, 'abschnitte': abschnitte}
    if feld_liste is not None: e['felder'] = feld_liste
    return e


def main():
    args = sys.argv[1:]
    if len(args) < 2: sys.exit(__doc__)
    ziel, handy, wireframe, felder = args.pop(0), '--handy' in args, '--wireframe' in args, '--felder' in args
    args = [a for a in args if a not in ('--handy', '--wireframe', '--felder')]
    selektor, hover, vorher_js = STANDARD_ABSCHNITTE, None, None
    if '--js' in args:
        i = args.index('--js'); vorher_js = args[i + 1]; del args[i:i + 2]
    if '--hover' in args:
        i = args.index('--hover'); hover = args[i + 1]; del args[i:i + 2]
    if '--abschnitte' in args:
        i = args.index('--abschnitte'); selektor = args[i + 1]; del args[i:i + 2]
    if args[0] == '--sitemap':
        xml = urllib.request.urlopen(urllib.request.Request(args[1], headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read().decode()
        urls = re.findall(r'<loc>([^<]+)</loc>', xml)
    else:
        urls = args
    pathlib.Path(ziel).mkdir(parents=True, exist_ok=True)
    profil = tempfile.mkdtemp(prefix='aufnahme-chrome-')
    chrome = subprocess.Popen([CHROME, '--headless=new', f'--remote-debugging-port={PORT}', f'--user-data-dir={profil}', '--hide-scrollbars',
                               '--no-first-run', '--no-default-browser-check', '--force-color-profile=srgb', 'about:blank'],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(40):
            try:
                seiten = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json', timeout=2).read()); break
            except OSError: time.sleep(0.25)
        ws = Verbindung(next(s for s in seiten if s['type'] == 'page')['webSocketDebuggerUrl'])
        ws.senden('Page.enable')
        protokoll = pathlib.Path(ziel) / 'aufnahmen.json'
        alt = json.loads(protokoll.read_text(encoding='utf-8')) if protokoll.exists() else []
        neu = [aufnehmen(ws, u, ziel, handy, selektor, wireframe, felder, hover, vorher_js) for u in urls]
        schluessel = {(e['url'], e['breite']) for e in neu}
        protokoll.write_text(json.dumps([e for e in alt if (e['url'], e['breite']) not in schluessel] + neu, ensure_ascii=False, indent=1), encoding='utf-8')
    finally:
        chrome.terminate()


if __name__ == '__main__':
    main()
