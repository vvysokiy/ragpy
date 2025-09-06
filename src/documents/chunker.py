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
        separator: str = "\n"
        # separators: list[str] = ["\n\n", "\n", ". ", "! ", "? "]  # приоритетные разделители
    ):
        """
        Args:
            chunk_size: Максимальный размер чанка в символах
            chunk_overlap: Количество символов перекрытия между чанками
            separator: Символ или строка для разделения текста
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator

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

        # Разбиваем текст по сепаратору
        parts = text.split(self.separator)
        chunks: list[str] = []
        current_chunk: list[str] = []
        current_length = 0

        for part in parts:
            part_length = len(part)
            # print(f"current_chunk: {current_chunk}")

            if current_length + part_length <= self.chunk_size:
                current_chunk.append(part)
                current_length += part_length + len(self.separator)
            else:
                # Строка из текущего чанка
                current_chunk_str = self.separator.join(current_chunk)
                current_chunk = []
                # Строка из предыдущего чанка
                previous_chunk_str = chunks[-1] if len(chunks) > 0 else ''
                # print(f"previous_chunk_str: {previous_chunk_str}")

                if previous_chunk_str:
                    overlap = previous_chunk_str[-self.chunk_overlap:]
                    chunks.append(overlap + '' + current_chunk_str)
                else:
                    chunks.append(current_chunk_str)
                current_length = 0

        if current_chunk:
            # Строка из текущего чанка
            current_chunk_str = self.separator.join(current_chunk)
            # Строка из предыдущего чанка
            previous_chunk_str = chunks[-1] if len(chunks) > 0 else ''

            if previous_chunk_str:
                overlap = previous_chunk_str[-self.chunk_overlap:]
                chunks.append(overlap + '' + current_chunk_str)
            else:
                chunks.append(current_chunk_str)
            current_chunk = []

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