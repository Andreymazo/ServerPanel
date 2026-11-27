#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$APP_DIR/server-panel.desktop"

chmod +x "$PROJECT_DIR/scripts/run.sh"
mkdir -p "$APP_DIR"

cat << EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=Пульт управления VPS
Comment=Управление проектами на skewer-public-api
Exec=$PROJECT_DIR/scripts/run.sh
Path=$PROJECT_DIR
Icon=utilities-terminal
Terminal=false
Categories=Development;System;
EOF

chmod +x "$DESKTOP_FILE"

if [ -d "$HOME/Desktop" ]; then
    cp "$DESKTOP_FILE" "$HOME/Desktop/"
elif [ -d "$HOME/Рабочий стол" ]; then
    cp "$DESKTOP_FILE" "$HOME/Рабочий стол/"
fi

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APP_DIR" 2>/dev/null || true
fi

echo "✅ Ярлык «Пульт управления VPS» установлен из $PROJECT_DIR"
