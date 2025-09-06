export PYTHONPATH := $(PWD):$(PYTHONPATH)

.PHONY: test test-verbose clean install

# Установка зависимостей
install:
	mkdir -p .cache/ollama
	mkdir -p .db
	mkdir -p .results
	pip install -r requirements.txt

# Запуск с простой конфигурацией
start-simple:
	python main.py --config_type simple_config

# Запуск с конфигурацией для Qwen3 Light
start-qwen3-light:
	python main.py --config_type qwen3_light_config

start: start-simple

# Запуск всех тестов
test:
	PYTHONPATH=. python -m pytest src/ -v

# Запуск тестов с подробным выводом
test-verbose:
	PYTHONPATH=. python -m pytest src/ -v -s

# Запуск конкретного теста
test-chunker:
	PYTHONPATH=. python -m pytest src/documents/tests/test_chunker.py -v

# Очистка кэша pytest
clean-pytest:
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Docker команды
ollama-start:
	docker compose build
	docker compose up

ollama-clean:
	docker compose down --rmi all
	docker system prune -f

# Тест LLM
ollama-test:
	curl -s http://localhost:11434/api/generate -d '{ \
		"model": "qwen3:8b", \
		"prompt": "Сколько будет 2+2?" \
	}'

# Полная очистка локального кэша моделей (если нужно пересеять из образа)
ollama-clean-local:
	rm -rf .cache/ollama/*