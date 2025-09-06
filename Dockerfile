FROM ollama/ollama:latest

# На этапе сборки кладём модели в ОТДЕЛЬНУЮ папку, не ту, что будет монтироваться
ENV OLLAMA_MODELS=/models-baked

# Предзагрузка модели в образ (можешь добавить ещё pull'ов)
RUN ollama serve & \
    sleep 5 && \
    ollama pull qwen3:8b && \
    pkill ollama

# Скрипт запуска: при первом старте "засев" моделей в смонтированный volume
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# На рантайме вернём дефолтный путь моделей
ENV OLLAMA_MODELS=/root/.ollama/models

# В базовом образе ENTRYPOINT уже ["ollama"], но нам нужен свой,
# чтобы перед стартом засеять volume. Внутри скрипта вызовем `exec ollama serve`.
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
