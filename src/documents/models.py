from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Mapping

Content = str
Metadata = Mapping[str, str | int | float | bool | None]
DocID = Optional[str]
ChunkID = str
ChunkIndex = int
CreatedAt = datetime

@dataclass # Декоратор, который автоматически добавляет методы __init__, __repr__, __eq__ и др.
class Document:
    """Базовый класс для представления документа."""
    # Содержимое документа в виде строки
    content: Content
    # Словарь с метаданными документа (например: имя файла, размер, дата создания и т.д.)
    metadata: Metadata
    # Опциональный ID документа. None по умолчанию
    doc_id: DocID = None
    # Дата и время создания документа, по умолчанию текущее время
    created_at: CreatedAt = datetime.now()

@dataclass
class DocumentChunk(Document):
    """Представляет часть документа после разбиения."""
    # Опциональный ID чанка
    chunk_id: ChunkID = ''
    # Порядковый номер чанка в документе, начиная с 0
    chunk_index: ChunkIndex = 0
