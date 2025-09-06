from src.db import ChromaDB
from src.logger import logger
from src.documents import DirectoryLoader, TextChunker
from src.setup import Setup
from src.utils import save_embeddings_results, save_text_chunker_results, save_search_results

_DEBUG_ = True

query_list = [
    "How does Tolstoy's *War and Peace* intertwine personal destinies with the Napoleonic Wars, and what philosophical questions about history and individual agency does it raise?",
    "What moral and psychological conflicts drive Raskolnikov in Dostoevsky's *Crime and Punishment*, particularly around free will, guilt, and redemption?",
    "Key traits of Russia's Silver Age poetry—symbolism, acmeism, futurism—and how Akhmatova, Blok, Mayakovsky, and Tsvetaeva embody them.",
]

if __name__ == "__main__":
    logger.info("Приложение запущено")

    db, embedding_service, dir_loader, text_chunker = Setup().create_pipeline()

    # Очищаем базу данных в режиме отладки
    if _DEBUG_: db.clear_collection()

    # Создаем DirectoryLoader
    # dir_loader = DirectoryLoader()

    # Загружаем документы
    documents = dir_loader.load_from_directory(
        'docs',
        glob_pattern='*.*'
    )

    # Создаем чанкер
    # text_chunker = TextChunker(
    #     chunk_size=500,
    #     chunk_overlap=50
    # )

    # Создаем чанки для каждого документа
    for document in documents:
        chunks = text_chunker.create_chunks(document)
        
        # Сохраняем результаты TextChunker
        if _DEBUG_: save_text_chunker_results(
            chunks, 
            f".results/TextChunker_results_{document.metadata.get('filename', 'unknown')}.txt"
        )

        embeddings = embedding_service.create_embeddings([chunk.content for chunk in chunks])

        # Сохраняем результаты AllMiniLMService
        if _DEBUG_:save_embeddings_results(
            chunks,
            embeddings,
            output_file=f".results/AllMiniLMService_results_{document.metadata.get('filename', 'unknown')}.txt"
        )

        db.add_documents(chunks, embeddings)

    # Выполняем поиск по запросам и сохраняем результаты
    logger.info("Начинаем поиск по запросам...")
    save_search_results(query_list, db, embedding_service)
    logger.info("Поиск завершен!")
