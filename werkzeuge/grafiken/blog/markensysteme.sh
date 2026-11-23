#!/bin/bash
# Rendert die drei Grafiken zum Artikel „Agentische Markensysteme“ aus markensysteme.html.
# Aufruf vom Repository-Ordner aus: bash werkzeuge/grafiken/blog/markensysteme.sh
# Braucht Google Chrome und cwebp (in ~/bin). Ergebnis: website/bilder/blog-markensysteme/{titel,ordner,zwei-fassungen}.webp und titel-og.jpg
set -euo pipefail
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
QUELLE="$(cd "$(dirname "$0")" && pwd)/markensysteme.html"
ZIEL="website/bilder/blog-markensysteme"; mkdir -p "$ZIEL"
TMP="$(mktemp -d)"
nr=1
for name in titel ordner zwei-fassungen; do
  "$C" --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files --force-device-scale-factor=2 --window-size=1200,800 \
    --virtual-time-budget=3000 --screenshot="$TMP/$name.png" "file://$QUELLE?b=$nr" 2>/dev/null
  sips -z 800 1200 "$TMP/$name.png" --out "$TMP/$name-1200.png" >/dev/null
  "$HOME/bin/cwebp" -quiet -q 90 "$TMP/$name-1200.png" -o "$ZIEL/$name.webp"
  nr=$((nr + 1))
done
# Vorschaubild für soziale Netzwerke 1200 × 630 (Mitte des Titelbilds)
sips -c 630 1200 "$TMP/titel-1200.png" --out "$TMP/og.png" >/dev/null
sips -s format jpeg -s formatOptions 85 "$TMP/og.png" --out "$ZIEL/titel-og.jpg" >/dev/null
ls -la "$ZIEL"
