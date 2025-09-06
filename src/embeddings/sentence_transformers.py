from sentence_transformers import SentenceTransformer
from pathlib import Path

# from ..logger import logger

from .service import BaseEmbeddingService

class SentenceTransformersEmbeddingService(BaseEmbeddingService):
    """Сервис эмбеддингов Sentence Transformers."""

    model_name: str

    def __init__(self, model_name: str):
        self._logger_info(f"Инициализация SentenceTransformersEmbeddingService для модели {model_name}")  

        self.model_name = model_name

        cache_folder = str(Path(self.cache_folder, self.model_name))
        self.model = SentenceTransformer(self.model_name, cache_folder=cache_folder)
        self._dimension = self.model.get_sentence_embedding_dimension()
        self._logger_info(f"Модель инициализирована. Размерность эмбеддингов: {self._dimension}")

    def create_embedding(self, text: str) -> list[float]:
        try:
            return self.model.encode(text).tolist()
        except Exception as e:
            self._logger_error(f"Ошибка при создании эмбеддинга для текста {text}: {e}")
            raise

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        return [self.create_embedding(text) for text in texts]

    @property
    def dimension(self) -> int | None:
        return self._dimension
    

class AllMiniLMService(SentenceTransformersEmbeddingService):
    """Сервис эмбеддингов для модели All-MiniLM-L6-v2."""

    MODEL_NAME: str = "all-MiniLM-L6-v2"
    BATCH_SIZE = 64

    def __init__(self):
        """Инициализация с предопределенной моделью."""
        super().__init__(self.MODEL_NAME)

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Создает эмбеддинги для списка текстов.
        Оптимизированная версия для all-MiniLM-L6-v2.

        Args:
            texts: список текстов
            
        Returns:
            list[list[float]]: список векторных представлений
        """
        try:
            return self.model.encode(
                texts,                       # Тексты для эмбеддинга
                batch_size=self.BATCH_SIZE,  # Увеличенный batch_size для этой легкой модели
                show_progress_bar=True,      # Показывает прогресс бар
                convert_to_tensor=True,      # Ускоряет обработку
                normalize_embeddings=True    # Нормализация для лучшего сравнения
            ).tolist()
        except Exception as e:
            slice_texts = str([text[:10] for text in texts])
            self._logger_error(f"Ошибка при создании эмбеддингов для текстов {slice_texts}: {str(e)}")
            raise




