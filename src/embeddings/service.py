from abc import (
    ABC, # ABC - для создания абстрактных классов
    abstractmethod # abstractmethod - для абстрактных методов
)
from typing import Optional

from ..logger import logger

class BaseEmbeddingService(ABC):
    """Базовый абстрактный класс для всех сервисов эмбеддингов."""

    cache_folder: str = "./.cache"
    model_name: Optional[str] = None

    @abstractmethod
    def create_embedding(self, text: str) -> list[float]:
        """
        Создает эмбеддинг для одного текста.
        
        Args:
            text: входной текст
            
        Returns:
            list[float]: векторное представление текста
        """
        pass

    @abstractmethod
    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Создает эмбеддинги для списка текстов.
        
        Args:
            texts: список текстов
            batch_size: размер батча для оптимизации памяти
            
        Returns:
            List[List[float]]: список векторных представлений
        """
        pass

    @property
    @abstractmethod
    def dimension(self) -> int | None:
        """Возвращает размерность эмбеддингов."""
        pass

    def _logger_info(self, message: str):
        """
        Логирует информационное сообщение с указанием имени класса.

        Args:
            message (str): Сообщение для логирования.
        """
        name = self.__class__.__name__
        logger.info("[%s] %s", name, message)

    def _logger_error(self, message: str):
        """
        Логирует сообщение об ошибке с указанием имени класса.

        Args:
            message (str): Сообщение об ошибке для логирования.
        """
        name = self.__class__.__name__
        logger.error("[%s] %s", name, message)

