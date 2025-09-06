export PYTHONPATH := $(PWD):$(PYTHONPATH)

.PHONY: test test-verbose clean install

# Запуск всех тестов
test:
	PYTHONPATH=. python -m pytest src/ -v

# Запуск тестов с подробным выводом
test-verbose:
	PYTHONPATH=. python -m pytest src/ -v -s

# Запуск конкретного теста
test-chunker:
	PYTHONPATH=. python -m pytest src/documents/tests/test_chunker.py -v

# Установка зависимостей
install:
	pip install -r requirements.txt

# Очистка кэша pytest
clean:
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
