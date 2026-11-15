#!/usr/bin/env bash
# preparar.sh - crea (o resetea) las dos copias del demo para grabar.
#
#   ./preparar.sh                         # en ~/demo-prompt-injection
#   ./preparar.sh /otra/carpeta
#
# Quedan fuera de este repo a propósito: Claude Code sube por las carpetas buscando
# .claude/ y CLAUDE.md, y no queremos que otros settings se mezclen en el demo.
set -euo pipefail

AQUI="$(cd "$(dirname "$0")" && pwd)"
DEST="${1:-$HOME/demo-prompt-injection}"

# sin-defensa  el proyecto tal cual
# con-defensa  regla deny + hook (lo que usarías en un proyecto real)
# solo-hook    solo el hook, sin la regla deny: así el bloqueo del hook se ve en cámara
#              (con la regla deny puesta, el Read del .env se frena antes de que corra el hook)
for caso in sin-defensa con-defensa solo-hook; do
  dir="$DEST/$caso/truck-tracker-api"
  rm -rf "$dir"
  mkdir -p "$dir"
  cp -R "$AQUI/proyecto/." "$dir/"
  mv "$dir/.env.demo" "$dir/.env"          # llaves FALSAS; en el repo viven como .env.demo
  if [[ "$caso" != "sin-defensa" ]]; then
    cp -R "$AQUI/defensa/.claude" "$dir/"
    chmod +x "$dir/.claude/hooks/proteger-secretos.py"
  fi
  if [[ "$caso" == "solo-hook" ]]; then
    python3 -I - "$dir/.claude/settings.json" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p)); d.pop("permissions", None)
json.dump(d, open(p, "w"), indent=2); open(p, "a").write("\n")
PY
  fi
  (
    cd "$dir"
    git init -q
    printf '.env\n.claude/hooks/bloqueos.log\n' > .gitignore
    git add -A
    git -c user.name="demo" -c user.email="demo@localhost" commit -q -m "truck-tracker-api"
  )
  echo "listo: $dir"
done

cat <<EOF

Siguiente:
  1. Terminal A:  python3 "$AQUI/receptor/receptor.py"
  2. Terminal B:  cd "$DEST/sin-defensa/truck-tracker-api" && claude
  3. Terminal C:  cd "$DEST/con-defensa/truck-tracker-api" && claude
  4. Para grabar el bloqueo del hook:  cd "$DEST/solo-hook/truck-tracker-api" && claude
EOF
