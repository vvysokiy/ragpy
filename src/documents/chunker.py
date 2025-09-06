import uuid  # Для генерации уникальных идентификаторов

from .models import Document, DocumentChunk

from src.logger import logger

class BaseChunker:
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
            logger.warning("Текст пустой")
            return []

        chunks: list[str] = []
        start = 0
        
        while start < len(text):
            # Определяем конец текущего чанка
            end = start + self.chunk_size
            
            if end >= len(text):
                # Последний чанк - берем весь оставшийся текст
                chunk = text[start:]
                if chunk.strip():  # Добавляем только если не пустой
                    chunks.append(chunk)
                break
            
            # Ищем лучшее место для разрыва, используя разделители
            best_split = end
            for separator in self.separators:
                # Ищем последнее вхождение разделителя в пределах чанка
                sep_pos = text.rfind(separator, start, end)
                if sep_pos > start:  # Найден разделитель после начала чанка
                    best_split = sep_pos + len(separator)
                    break
            
            # Создаем чанк
            chunk = text[start:best_split]
            if chunk.strip():  # Добавляем только если не пустой
                chunks.append(chunk)
            
            # Вычисляем начало следующего чанка с учетом перекрытия
            if self.chunk_overlap > 0 and best_split < len(text):
                # Начинаем следующий чанк с перекрытием, но гарантируем продвижение вперед
                overlap_start = best_split - self.chunk_overlap
                start = max(start + 1, overlap_start)  # Гарантируем продвижение минимум на 1 символ
            else:
                start = best_split
            
            # Дополнительная защита от бесконечного цикла
            if start >= len(text):
                break

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