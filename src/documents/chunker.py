import uuid  # Для генерации уникальных идентификаторов

from .models import Document, DocumentChunk

from ..logger import LoggerService

class BaseChunker(LoggerService):
    """Базовый класс для разбиения документов на чанки."""

    def split_text(self, text: str) -> list[str]:
        """
        Разбивает текст на части.

        Args:
            text: Исходный текст.
            
        Returns:
            Список частей текста (чанков).
        """
        raise NotImplementedError("split_text ожидает реализации.")

    def create_chunks(self, document: Document) -> list[DocumentChunk]:
        """
        Создает чанки из документа.
        
        Args:
            document: Исходный документ
            
        Returns:
            Список чанков
        """
        raise NotImplementedError("create_chunks ожидает реализации.")

class TextChunker(BaseChunker):
    """Чанкер для разбиения текста на части по размеру."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: list[str] = ["\n\n", "\n", ". ", "! ", "? "],
    ):
        """
        Args:
            chunk_size: Максимальный размер чанка в символах
            chunk_overlap: Количество символов перекрытия между чанками
            separators: Символы или строки для разделения текста
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators

    def split_text(self, text: str) -> list[str]:
        """
        Разбивает текст на чанки с учетом перекрытия.
        
        Args:
            text: Исходный текст
            
        Returns:
            Список чанков текста
        """

        if not text:
            self._logger_warning("Текст пустой")
            return []

        chunks: list[str] = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            # Определяем конец текущего чанка
            end = min(start + self.chunk_size, text_len)
            
            # Если это последний чанк
            if end >= text_len:
                chunk = text[start:].strip()
                if chunk:
                    chunks.append(chunk)
                break
            
            # Ищем лучшее место для разрыва
            best_split = end
            
            # Проверяем разделители в порядке приоритета
            for separator in self.separators:
                # Ищем разделитель в последних 100 символах чанка
                search_start = max(start, end - 100)
                pos = text.find(separator, search_start, end)
                
                # Ищем последнее вхождение в этом диапазоне
                last_pos = pos
                while pos != -1 and pos < end:
                    last_pos = pos
                    pos = text.find(separator, pos + 1, end)
                
                if last_pos != -1 and last_pos > start:
                    best_split = last_pos + len(separator)
                    break
            
            # Создаем чанк
            chunk = text[start:best_split].strip()
            if chunk:
                chunks.append(chunk)
            
            # Вычисляем следующую позицию с перекрытием
            if self.chunk_overlap > 0 and best_split < text_len:
                # Простое перекрытие с поиском пробела
                overlap_pos = max(start + 1, best_split - self.chunk_overlap)
                
                # Ищем пробел в расширенном диапазоне (до половины размера чанка)
                search_range = min(self.chunk_size // 2, self.chunk_overlap + 50)
                search_end = min(overlap_pos + search_range, best_split)
                
                # Ищем пробел, начиная с желаемой позиции и двигаясь в обе стороны
                found_space = False
                
                # Сначала ищем вперед (предпочтительно)
                for i in range(overlap_pos, search_end):
                    if i < text_len and text[i].isspace():
                        start = i + 1
                        found_space = True
                        break
                
                # Если не нашли вперед, ищем назад
                if not found_space:
                    search_start = max(start + 1, overlap_pos - 30)
                    for i in range(overlap_pos - 1, search_start - 1, -1):
                        if i > start and i < text_len and text[i].isspace():
                            start = i + 1
                            found_space = True
                            break
                
                # Если совсем не нашли пробел, используем исходную позицию
                if not found_space:
                    start = overlap_pos
            else:
                start = best_split
            
            # Защита от зацикливания
            if start >= best_split:
                start = best_split

        return chunks

    def create_chunks(self, document: Document) -> list[DocumentChunk]:
        """
        Создает чанки из документа по предложениям.
        
        Args:
            document: Исходный документ
            
        Returns:
            Список чанков с метаданными
        """
        text_chunks = self.split_text(document.content)
        
        return [
            DocumentChunk(
                content=chunk,
                metadata={
                    **document.metadata,
                    "chunk_index": idx,
                    "total_chunks": len(text_chunks),
                    "chunk_size": len(chunk),
                    "original_document_id": document.doc_id
                },
                chunk_id=str(uuid.uuid4()),
                doc_id=document.doc_id,
                chunk_index=idx
            )
            for idx, chunk in enumerate(text_chunks)
        ]