#!/bin/sh
set -eu  # без pipefail — его нет в sh

# Куда монтируем (см. docker-compose.yml)
# Лучше явно задать в Dockerfile ENV OLLAMA_MODELS=/root/.ollama/models
TARGET_MODELS_DIR="${OLLAMA_MODELS:-/root/.ollama/models}"
BAKED_MODELS_DIR="/models-baked"

# Убедимся, что целевая папка есть
mkdir -p "$TARGET_MODELS_DIR"

# Проверяем, пуста ли она
is_empty=1
# Если ls что-то вернул — значит не пусто
if [ -n "$(ls -A "$TARGET_MODELS_DIR" 2>/dev/null || echo)" ]; then
  is_empty=0
fi

# Если пусто — засеваем запечёнными моделями
if [ $is_empty -eq 1 ] && [ -d "$BAKED_MODELS_DIR" ]; then
  echo "Seeding models into $TARGET_MODELS_DIR ..."
  cp -R "$BAKED_MODELS_DIR"/. "$TARGET_MODELS_DIR"/ || true
fi

# Стартуем сервер
exec ollama serve
