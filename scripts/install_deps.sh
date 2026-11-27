#!/bin/bash
set -e

echo "🔧 Установка системного пакета python3-tk..."
sudo apt update && sudo apt install -y python3-tk

echo "✅ Готово! Теперь можно запускать ./scripts/run.sh"
