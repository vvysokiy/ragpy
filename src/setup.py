from .db import ChromaDB
from .embeddings import AllMiniLMService
from .logger import LoggerService
from config import (
    VectorDBType,
    EmbeddingModelsType,
    LLMModelsType,
    config,
)

class Setup(LoggerService):
    """Инициализация компонентов системы на основе конфигурации"""

    @staticmethod
    def get_db():
        """Создает экземпляр базы данных согласно конфигурации"""
        db_type = config.DB_NAME.value
        
        if db_type == VectorDBType.CHROMA.value:
            return ChromaDB()
        elif db_type == VectorDBType.LANCE.value:
            # TODO: Добавить поддержку LanceDB
            raise NotImplementedError("LanceDB пока не поддерживается")
        else:
            raise ValueError(f"Неизвестный тип базы данных: {db_type}")

    @staticmethod
    def get_embedding_service():
        """Создает сервис эмбеддингов согласно конфигурации"""
        model_name = config.EMBEDDING_MODEL.value
        
        if model_name == EmbeddingModelsType.ALL_MINI_LM_L6_V2.value:
            return AllMiniLMService()
        elif model_name == EmbeddingModelsType.QWEN3_EMBEDDING_4B.value:
            # TODO: Добавить поддержку Qwen3 эмбеддингов
            raise NotImplementedError("Qwen3 эмбеддинги пока не поддерживаются")
        else:
            raise ValueError(f"Неизвестная модель эмбеддингов: {model_name}")

    def create_pipeline(self):
        """Создает полный пайплайн обработки"""
        self._logger_info(f"Инициализация пайплайна с конфигурацией: {config.__class__.__name__}")
        
        try:
            # Создаем базу данных
            db = self.get_db()
            self._logger_info(f"База данных инициализирована: {config.DB_NAME}")
            
            # Создаем сервис эмбеддингов
            embedding_service = self.get_embedding_service()
            self._logger_info(f"Сервис эмбеддингов инициализирован: {config.EMBEDDING_MODEL}")
            
            return db, embedding_service
            
        except Exception as e:
            self._logger_error(f"Ошибка инициализации пайплайна: {e}")
            raise
