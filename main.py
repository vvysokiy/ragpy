from src.db import ChromaDB
from src.logger import logger
from src.documents import DirectoryLoader, TextChunker, Document, DocumentChunk
from src.embeddings import AllMiniLMService

from typing import Any

from src.utils import save_embeddings_results, save_text_chunker_results

_DEBUG_ = True

if __name__ == "__main__":
    logger.info("Приложение запущено")

    # Создаем DirectoryLoader
    dir_loader = DirectoryLoader()

    # Загружаем документы
    documents = dir_loader.load_from_directory(
        'docs',
        glob_pattern='*.*'
    )

    # Создаем чанкер
    text_chunker = TextChunker(
        chunk_size=500,
        chunk_overlap=50
    )

    # Создаем ChromaDB
    chroma_db = ChromaDB()
    if _DEBUG_:
        chroma_db.clear_collection()

    # Создаем сервис эмбеддингов
    embedding_service = AllMiniLMService()

    # Создаем чанки для каждого документа
    for document in documents:
        chunks = text_chunker.create_chunks(document)
        
        if _DEBUG_:
            # Сохраняем результаты TextChunker
            save_text_chunker_results(
                chunks, 
                f".results/TextChunker_results_{document.metadata.get('filename', 'unknown')}.txt"
            )

        embeddings = embedding_service.create_embeddings([chunk.content for chunk in chunks])

        if _DEBUG_:
            # Сохраняем результаты AllMiniLMService
            save_embeddings_results(
                chunks,
                embeddings,
                output_file=f".results/AllMiniLMService_results_{document.metadata.get('filename', 'unknown')}.txt"
            )

        chroma_db.add_documents(chunks, embeddings)
