#!/bin/bash
# 3D-Fassung der Bauhaus-Icons mit Blender rechnen (Formensprache STUDIO AAH!, Anna 18.11.2026).
# Aufruf vom Repository-Ordner aus:
#   bash werkzeuge/grafiken/icons-3d.sh ZIELORDNER website/bilder/formen/brand.svg [weitere.svg …]
# Braucht Blender (kostenlos, auf dem MacBook in ~/Applications/Blender.app, installiert 18.11.2026 mit Annas OK).
set -euo pipefail
BLENDER="${BLENDER:-$HOME/Applications/Blender.app/Contents/MacOS/Blender}"
[ -x "$BLENDER" ] || { echo "Blender fehlt: $BLENDER"; exit 1; }
"$BLENDER" -b --factory-startup --python "$(dirname "$0")/icons-3d.py" -- "$@" 2>&1 | grep -E "3D-Icon geschrieben|Error|Fehler" || true
