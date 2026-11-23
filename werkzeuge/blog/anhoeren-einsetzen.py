# Setzt den Player „Artikel anhören“ in die älteren Blogartikel, die nicht mit beitrag.py gebaut sind.
# Aufnahme: python3 werkzeuge/blog/vorlesen.py <slug> → website/audio/<slug>.mp3. Neue Artikel (beitrag.py) bauen den Player selbst ein.
# Der Player steht zwischen <!-- ANHOEREN:START --> und <!-- ANHOEREN:ENDE --> direkt unter der Zeile mit Autorin und Datum; ohne Aufnahme kein Player.
# Aufruf vom Repository-Ordner: python3 werkzeuge/blog/anhoeren-einsetzen.py
import hashlib, pathlib, re

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
WEBSITE = REPO / 'website'

for seite in sorted((WEBSITE / 'blog').glob('*/index.html')):
    html = seite.read_text(encoding='utf-8')
    if 'artikel-raster' in html:  # mit beitrag.py gebaut, Player kommt von dort
        continue
    slug = seite.parent.name
    audio = WEBSITE / 'audio' / f'{slug}.mp3'
    html = re.sub(r'\n?    <!-- ANHOEREN:START -->.*?<!-- ANHOEREN:ENDE -->', '', html, flags=re.S)
    if audio.exists():
        meta = html.index('<p class="artikel-meta">', html.index('<article class="artikel'))
        ende = html.index('</p>', meta) + len('</p>')
        block = (f'\n    <!-- ANHOEREN:START -->\n    <div class="anhoeren">\n      <p class="meta">Artikel anhören · KI-Stimme</p>\n'
                 f'      <audio controls preload="none" src="../../audio/{slug}.mp3?v={hashlib.md5(audio.read_bytes()).hexdigest()[:8]}"></audio>\n'
                 f'    </div>\n    <!-- ANHOEREN:ENDE -->')
        html = html[:ende] + block + html[ende:]
    seite.write_text(html, encoding='utf-8')
    print(slug, 'mit Player' if audio.exists() else 'ohne Aufnahme')
