# Erzeugt website/audio/<slug>.mp3: der Artikel vorgelesen von der freien Stimme „Thorsten“ (Piper, lokal, nichts wird gesendet).
# Anna 17.11.2026: „Die Stimme … der Mann, der hier immer antwortet … die Stimmen müssen echt klingen“, ohne Tempo-Regler.
# Voraussetzungen: pip install piper-tts; Stimme de_DE-thorsten-medium.onnx (+ .json) im Ordner MODELL_ORDNER; ffmpeg.
# Aufruf im Repository-Ordner: python3 werkzeuge/blog/vorlesen.py <slug> [Modellordner]   danach den Blogbeitrag neu erzeugen.
import html, pathlib, re, subprocess, sys, tempfile
from html.parser import HTMLParser

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
slug = sys.argv[1]
MODELL_ORDNER = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else pathlib.Path.home() / 'bin' / 'piper')
MODELL = MODELL_ORDNER / 'de_DE-thorsten-medium.onnx'

AUSLASSEN = ('inhalt-verzeichnis', 'tabelle-scroll', 'quellen', 'artikel-schluss', 'autorin', 'artikel-faq', 'artikel-leiste', 'artikel-seite', 'vergleich-fuss', 'foto-nachweis')
BLOECKE = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'figcaption'}


class Leser(HTMLParser):
    def __init__(self):
        super().__init__(); self.tiefe = []; self.aus = 0; self.text = []; self.teile = []; self.in_text = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); klasse = a.get('class', '') or ''
        if tag in ('sup', 'script', 'style', 'svg', 'table') or any(k in klasse.split() for k in AUSLASSEN) or a.get('aria-hidden') == 'true' or a.get('id') == 'quellen':
            self.tiefe.append(True); self.aus += 1
        else:
            self.tiefe.append(False)

    def handle_endtag(self, tag):
        if tag in BLOECKE and not self.aus:
            t = re.sub(r'\s+', ' ', ''.join(self.text)).strip()
            if t: self.teile.append(t)
            self.text = []
        if self.tiefe and self.tiefe.pop(): self.aus -= 1

    def handle_data(self, d):
        if not self.aus: self.text.append(d)


seite = (REPO / 'website' / 'blog' / slug / 'index.html').read_text(encoding='utf-8')
artikel = seite[seite.index('<article class="artikel'):seite.index('<nav class="artikel-nav"')]
artikel = re.sub(r'<p class="artikel-meta">.*?</p>', '', artikel, flags=re.S)
artikel = re.sub(r'<div class="anhoeren">.*?</div>', '', artikel, flags=re.S)
artikel = re.sub(r'<nav class="meta".*?</nav>', '', artikel, flags=re.S)
leser = Leser(); leser.feed(artikel)
text = '\n'.join(leser.teile).replace('­', '')
# Aussprache-Hilfen für die Stimme
for alt, neu in (('KI', 'K I'), ('STUDIO AAH!', 'Studio A A H'), ('z. B.', 'zum Beispiel'), ('ca.', 'circa'), ('€', ' Euro'), ('$', ' Dollar'), ('%', ' Prozent'), (' / ', ', '), ('Vibe-Coding', 'Waib-Koding'), ('Claude', 'Klod'), ('Base44', 'Base vierundvierzig'), ('v0', 'v null'), ('SSL', 'S S L'), ('DNS', 'D N S'), ('DSGVO', 'D S G V O'), ('CLAUDE.md', 'Klod Punkt M D')):
    text = text.replace(alt, neu)
text = re.sub(r':innen', 'innen', text)
text = re.sub(r':in\b', 'in', text)
# weitere Aussprache-Hilfen (Anna 18.11.2026: „Jeden Artikel … mit Voice“), Abkürzungen nur als ganze Wörter
for alt, neu in ((r'\bEU AI Act\b', 'E U A I Act'), (r'\bAI Act\b', 'A I Act'), (r'\bAVV\b', 'A V V'), (r'\bDPA\b', 'D P A'), (r'\bHGB\b', 'H G B'),
                 (r'\bAO\b', 'A O'), (r'\bGmbHG\b', 'G m b H Gesetz'), (r'\bGmbH\b', 'G m b H'), (r'\bOHG\b', 'O H G'), (r'\bKG\b', 'K G'),
                 (r'\bTLS\b', 'T L S'), (r'\bAPI\b', 'A P I'), (r'\bAGB\b', 'A G B'), (r'\bKMU\b', 'K M U'), (r'\bSEO\b', 'S E O'),
                 (r'§\s*', 'Paragraf '), (r'\bArt\.\s*', 'Artikel '), (r'\bAbs\.\s*', 'Absatz '), (r'\bNr\.\s*', 'Nummer '), (r'\bRn\.\s*', 'Randnummer '),
                 (r'\bMwSt\.', 'Mehrwertsteuer'), (r'\binkl\.', 'inklusive'), (r'\bu\. a\.', 'unter anderem'), (r'\bMio\.', 'Millionen'),
                 (r'\bChatGPT\b', 'Tschätt G P T'), (r'\bGmail\b', 'G-Mail'), (r'\biCloud\+?', 'Ei-Klaud'), (r'\bCopilot\b', 'Ko-Pailot'),
                 (r'\bGemini\b', 'Dschemini'), (r'\bClickUp\b', 'Klick-App'), (r'\bWorkspace\b', 'Wörkspäis'), (r'\bOpenAI\b', 'Open A I'),
                 (r'\bAnthropic\b', 'Änthropic'), (r'\bLovable\b', 'Lavabel'), (r'\bFigma\b', 'Figma')):
    text = re.sub(alt, neu, text)
ziel = REPO / 'website' / 'audio' / f'{slug}.mp3'
ziel.parent.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    t = pathlib.Path(tmp)
    (t / 'text.txt').write_text(text, encoding='utf-8')
    subprocess.run([sys.executable, '-m', 'piper', '-m', str(MODELL), '-f', str(t / 'a.wav'), '--sentence-silence', '0.35'],
                   stdin=open(t / 'text.txt', encoding='utf-8'), check=True, capture_output=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(t / 'a.wav'), '-ac', '1', '-b:a', '40k', str(ziel)], check=True)
print(ziel.relative_to(REPO), ziel.stat().st_size // 1024, 'KB', len(text.split()), 'Wörter')
