from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass # Декоратор, который автоматически добавляет методы __init__, __repr__, __eq__ и др.
class Document:
    """Базовый класс для представления документа."""
    # Содержимое документа в виде строки
    content: str
    # Словарь с метаданными документа (например: имя файла, размер, дата создания и т.д.)
    metadata: dict
    # Опциональный ID документа. None по умолчанию
    doc_id: Optional[str] = None
    # Дата и время создания документа, по умолчанию текущее время
    created_at: datetime = datetime.now()

@dataclass
class DocumentChunk(Document):
    """Представляет часть документа после разбиения."""
    # Опциональный ID чанка
    chunk_id: Optional[str] = None
    # Порядковый номер чанка в документе, начиная с 0
    chunk_index: int = 0
