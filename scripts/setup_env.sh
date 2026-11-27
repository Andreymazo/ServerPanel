#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)"
ENV_FILE="$PROJECT_DIR/.env"
EXAMPLE_FILE="$PROJECT_DIR/.env.example"

if [ -f "$ENV_FILE" ]; then
    echo "✅ Файл .env уже существует ($ENV_FILE)."
    exit 0
fi

if [ ! -f "$EXAMPLE_FILE" ]; then
    echo "❌ Шаблон .env.example не найден в $PROJECT_DIR."
    exit 1
fi

cp "$EXAMPLE_FILE" "$ENV_FILE"
chmod 600 "$ENV_FILE"
echo "🆕 Создан файл .env из шаблона. Заполни в нём SERVER_IP и токен перед запуском!"
