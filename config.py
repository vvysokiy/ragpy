from enum import Enum
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Загружаем .env файл
load_dotenv()

class VectorDBType(Enum):
    """Векторный тип базы данных."""
    CHROMA = "chromadb"
    LANCE = "lancedb"

class EmbeddingModelsType(Enum):
    """Эмбеддинг модели."""
    QWEN3_EMBEDDING_4B = "Qwen3-Embedding-4B"
    ALL_MINI_LM_L6_V2 = "all-MiniLM-L6-v2"

class LLMModelsType(Enum):
    """LLM модели."""
    QWEN3_8B_INSTRUCT = "Qwen3-8B-Instruct"
    QWEN3_14B_INSTRUCT = "Qwen3-14B-Instruct"

class BaseConfig:
    """Базовый класс для всех конфигураций"""
    DB_NAME: VectorDBType
    EMBEDDING_MODEL: EmbeddingModelsType
    FAST_LLM_MODEL: LLMModelsType
    
    # Общие настройки по умолчанию
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    DOCS_DIR: Path = Path("docs")
    RESULTS_DIR: Path = Path(".results")

class SimpleConfig(BaseConfig):
    """Простая конфигурация для тестирования"""
    DB_NAME = VectorDBType.CHROMA
    EMBEDDING_MODEL = EmbeddingModelsType.ALL_MINI_LM_L6_V2
    FAST_LLM_MODEL = LLMModelsType.QWEN3_8B_INSTRUCT

class Qwen3LightConfig():
    """Конфигурация для Qwen3"""
    DB_NAME = VectorDBType.LANCE
    EMBEDDING_MODEL = EmbeddingModelsType.QWEN3_EMBEDDING_4B
    FAST_LLM_MODEL = LLMModelsType.QWEN3_8B_INSTRUCT


# Создаем глобальный экземпляр
simple_config = SimpleConfig()
qwen3_light_config = Qwen3LightConfig()