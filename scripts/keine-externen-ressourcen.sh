#!/usr/bin/env bash
# DSGVO §7 als Pruefung statt als Bitte.
# Kein Frontend darf Ressourcen von fremden Servern laden.
set -euo pipefail

ZIEL="${1:-frontend/static}"
[ -d "$ZIEL" ] || { echo "kein Frontend unter $ZIEL — uebersprungen"; exit 0; }

# Nur geladene Ressourcen, keine gewoehnlichen Verweise:
#   src=/srcset= …        Script, Bild, iframe
#   <link … href=…        Stylesheet, Font, Icon
#   url(…) / @import …    CSS-Hintergruende, @font-face, Importe
# (https?:)? faengt auch protokoll-relative URLs wie //cdn.example/x.js
# Bewusst NICHT beanstandet: <a href="https://…"> — ein Verweis laedt nichts.
MUSTER='(src|srcset)=["'"'"']?(https?:)?//|<link[^>]+href=["'"'"']?(https?:)?//|url\(["'"'"']?(https?:)?//|@import[[:space:]]+["'"'"'](https?:)?//'

# Fremde und erzeugte Verzeichnisse bleiben aussen vor - dort stehen zwangslaeufig
# externe URLs, die nie ausgeliefert werden.
AUS=(--exclude-dir=node_modules --exclude-dir=dist --exclude-dir=.git
     --exclude-dir=.venv --exclude-dir=__pycache__ --exclude-dir=vendor)

if grep -rEni "${AUS[@]}" "$MUSTER" "$ZIEL"; then
  echo
  echo "FEHLER: externe Ressource gefunden (siehe oben)."
  echo "Kein CDN: Fonts, Skripte und Bilder lokal einbinden."
  exit 1
fi
echo "keine externen Ressourcen"
