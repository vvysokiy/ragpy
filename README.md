# ragpy

RAG (Retrieval-Augmented Generation) система для работы с документами на основе векторного поиска и семантических эмбеддингов.

## 🚀 Возможности

- **Загрузка документов** из директории с поддержкой различных форматов
- **Интеллектуальное разбиение** текста на чанки с сохранением контекста
- **Векторные эмбеддинги** с использованием sentence-transformers
- **Семантический поиск** по базе документов с высокой точностью
- **Персистентное хранение** в ChromaDB
- **Детальное логирование** всех операций

## 📁 Структура проекта

```
ragpy/
├── src/
│   ├── documents/           # Работа с документами
│   │   ├── chunker.py      # Разбиение текста на чанки
│   │   ├── loader.py       # Загрузка документов
│   │   ├── models.py       # Модели данных
│   │   └── tests/          # Тесты для документов
│   │       └── test_chunker.py
│   ├── embeddings/         # Создание эмбеддингов
│   │   ├── sentence_transformers.py
│   │   └── service.py
│   ├── db/                 # База данных
│   │   └── chromadb.py     # ChromaDB интеграция
│   ├── logger/             # Логирование
│   │   └── logger.py
│   └── utils.py            # Утилиты
├── docs/                   # Тестовые документы
│   ├── russian_literature_1.txt
│   ├── russian_literature_2.txt
│   ├── russian_literature_3.txt
│   ├── russian_literature_4.txt
│   └── russian_literature_5.txt
├── .results/               # Результаты обработки
│   ├── search_results.txt
│   ├── TextChunker_results_*.txt
│   └── AllMiniLMService_results_*.txt
├── main.py                 # Основной скрипт
├── Makefile               # Команды для разработки
├── requirements.txt       # Зависимости
└── README.md
```

## 🛠 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd ragpy
```

### 2. Установка зависимостей
```bash
make install
# или
pip install -r requirements.txt
```

### 3. Запуск системы
```bash
python main.py
```

### 4. Запуск тестов
```bash
make test
```

## 🔧 Основные компоненты

### 📄 Загрузка документов (`DirectoryLoader`)
- Автоматическая загрузка всех текстовых файлов из директории
- Извлечение метаданных (имя файла, размер, дата создания)
- Поддержка различных кодировок

### ✂️ Разбиение на чанки (`TextChunker`)
- Интеллектуальное разбиение с учетом структуры текста
- Настраиваемые параметры размера и перекрытия
- Сохранение целостности слов и предложений
- Приоритетные разделители: `\n\n`, `\n`, `. `, `! `, `? `

### 🧠 Создание эмбеддингов (`AllMiniLMService`)
- Модель: `sentence-transformers/all-MiniLM-L6-v2`
- Размерность векторов: 384
- Нормализованные эмбеддинги (L2 норма = 1.0)
- Поддержка батчевой обработки

### 🗄️ Векторная база данных (`ChromaDB`)
- Персистентное хранение в директории `.db/`
- Cosine similarity для поиска
- Автоматическая индексация
- Поддержка метаданных

## 📊 Результаты работы

Система автоматически сохраняет результаты в директории `.results/`:

- **`search_results.txt`** - результаты поиска по запросам
- **`TextChunker_results_*.txt`** - детали разбиения документов
- **`AllMiniLMService_results_*.txt`** - информация об эмбеддингах

## 🎯 Пример использования

```python
from src.documents import DirectoryLoader, TextChunker
from src.embeddings import AllMiniLMService
from src.db import ChromaDB

# Загрузка документов
loader = DirectoryLoader("docs")
documents = loader.load()

# Разбиение на чанки
chunker = TextChunker(chunk_size=500, chunk_overlap=50)
chunks = []
for doc in documents:
    chunks.extend(chunker.create_chunks(doc))

# Создание эмбеддингов
embedding_service = AllMiniLMService()
embeddings = embedding_service.create_embeddings([chunk.content for chunk in chunks])

# Сохранение в базу
chroma_db = ChromaDB()
chroma_db.add_documents(chunks, embeddings)

# Поиск
query = "What are the main themes in Russian literature?"
query_embedding = embedding_service.create_embedding(query)
results = chroma_db.search(query_embedding, n_results=3)
```

## 🧪 Тестирование

Система включает комплексные тесты для проверки:

- **Инициализации** компонентов
- **Разбиения текста** на различных данных
- **Качества эмбеддингов** и поиска
- **Обработки граничных случаев**

Запуск тестов:
```bash
make test                    # Все тесты
make test-chunker           # Только тесты чанкера
make test-verbose           # Подробный вывод
```

## 📈 Качество поиска

Система демонстрирует высокое качество семантического поиска:

| Тип запроса | Точность | Сходство |
|-------------|----------|----------|
| Конкретные произведения | 83-86% | Отлично |
| Философские темы | 78-85% | Очень хорошо |
| Литературные направления | 86-89% | Превосходно |

## 🔧 Настройки

### Параметры чанкинга
```python
TextChunker(
    chunk_size=500,        # Размер чанка в символах
    chunk_overlap=50,      # Перекрытие между чанками
    separators=["\n\n", "\n", ". ", "! ", "? "]  # Приоритеты разделителей
)
```

### Режим отладки
Установите `_DEBUG_ = True` в `main.py` для:
- Очистки базы данных при каждом запуске
- Детального логирования операций
- Сохранения промежуточных результатов

## 📋 Зависимости

- **sentence-transformers** - создание эмбеддингов
- **chromadb** - векторная база данных  
- **numpy** - математические операции
- **pathlib** - работа с путями файлов

## 🤝 Разработка

Проект использует:
- **Python 3.11+**
- **Type hints** для всех функций
- **Подробное логирование** операций
- **Модульная архитектура** для легкого расширения
- **Comprehensive testing** с unittest

## 📝 Лицензия

MIT License
