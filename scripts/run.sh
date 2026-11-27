#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)"
cd "$PROJECT_DIR"

if ! python3 -c "import tkinter" >/dev/null 2>&1; then
    echo "❌ Модуль tkinter не установлен. Запустите: ./scripts/install_deps.sh"
    exit 1
fi

bash "$PROJECT_DIR/scripts/setup_env.sh"

exec python3 "$PROJECT_DIR/main.py"
