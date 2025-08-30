from src.logger import logger
from src.documents import TextFileLoader, DirectoryLoader

# __eq__ для сравнения
# doc1 = Document(content="текст", metadata={})
# doc2 = Document(content="текст", metadata={})
# doc_chunk1 = DocumentChunk(content="текст", metadata={})
# doc_chunk2 = DocumentChunk(content="текст", metadata={})
# print(doc1)
# __repr__ для удобного вывода
# print(doc2)
# print(doc1 == doc2)
# print(doc_chunk1)
# print(doc_chunk2)
# print(doc_chunk1 == doc_chunk2)  # True



# from pathlib import Path
# from typing import Optional

# from fastapi import FastAPI
# from pydantic_settings import BaseSettings

# Создание логгера для текущего модуля
# logger = setup_logger(__name__)

# Конфигурация приложения
# class Settings(BaseSettings):
#     """Базовые настройки приложения."""
#     # Название приложения
#     APP_NAME: str = "RAG Service"
#     # Версия приложения
#     APP_VERSION: str = "0.1.0"
#     # Путь к директории с данными
#     DATA_DIR: Path = Path("data")
#     # URL для подключения к векторной БД
#     VECTOR_DB_URL: Optional[str] = None
#     # Модель для создания эмбеддингов
#     EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
#     class Config:
#         env_file = ".env"

# Инициализация приложения
# app = FastAPI(
#     title=Settings().APP_NAME,
#     version=Settings().APP_VERSION,
#     description="RAG (Retrieval Augmented Generation) сервис для работы с документами"
# )

# @app.on_event("startup")
# async def startup_event():
#     """Действия при запуске приложения."""
#     logger.info("Инициализация приложения...")
    
#     # Создаем директорию для данных, если её нет
#     settings = Settings()
#     settings.DATA_DIR.mkdir(exist_ok=True)
    
#     logger.info(f"Приложение {settings.APP_NAME} v{settings.APP_VERSION} запущено")

# @app.get("/health")
# async def health_check():
#     """Эндпоинт для проверки работоспособности сервиса."""
#     return {"status": "ok"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Примеры использования разных уровней логирования
# def example_logging():
#     """Пример использования логгера."""
#     logger.debug("Это debug сообщение")
#     logger.info("Это info сообщение")
#     logger.warning("Это warning сообщение")
#     logger.error("Это error сообщение")
#     logger.critical("Это critical сообщение")

if __name__ == "__main__":
    logger.info("Приложение запущено")
    # example_logging()

    loader = TextFileLoader(encoding='utf-8')

    # Загружаем один файл
    # document = loader.load('docs/336869551.pdf')
    # if document:
    #     print(f"Загружен документ: {document.metadata['filename']}")

    dir_loader = DirectoryLoader(loader)
    documents = dir_loader.load_from_directory(
        'docs',
        glob_pattern='*.*'
    )

    