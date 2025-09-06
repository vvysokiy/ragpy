from src.db import ChromaDB
from src.logger import logger
from src.documents import DirectoryLoader, TextChunker, Document, DocumentChunk


from typing import Any

from src.utils import save_text_chunker_results, save_chunks_analysis, save_formatted_results

if __name__ == "__main__":
    logger.info("Приложение запущено")
    # example_logging()

    dir_loader = DirectoryLoader()
    documents = dir_loader.load_from_directory(
        'docs',
        glob_pattern='*.*'
    )

    # Создаем чанкер
    text_chunker = TextChunker(
        chunk_size=500,
        chunk_overlap=50
    )

    # Создаем чанки для каждого документа
    for document in documents:
        chunks = text_chunker.create_chunks(document)
        
        # Сохраняем результаты TextChunker
        save_text_chunker_results(
            chunks, 
            f".results/TextChunker_results_{document.metadata.get('filename', 'unknown')}.txt"
        )

    # from src.embeddings import AllMiniLMService

    # Создаем сервис
    # embedding_service = AllMiniLMService()

    # Тестовые тексты
    # texts = [
    #     "Python - высокоуровневый язык программирования",
    #     "Программирование на питоне очень удобное",
    #     "Машинное обучение - это интересно"
    # ]

    # Создаем эмбеддинги
    # embeddings = embedding_service.create_embeddings(texts)

    # Информация о размерности
    # print(f"Размерность эмбеддингов: {embedding_service.dimension}")
    # print(f"Количество векторов: {len(embeddings)}")
    # print(f"Размер первого вектора: {len(embeddings[0])}")

    # chroma_db = ChromaDB()

    # for document in documents:
    #     # if document.metadata.get('filename') == '336869551.pdf':
    #     chunks = text_chunker.create_chunks(document)
    #     save_chunks_analysis(chunks, f".results/{document.metadata.get('filename')}_chunks_analysis.txt")
    #     embeddings = embedding_service.create_embeddings([chunk.content for chunk in chunks])
    #     chroma_db.add_documents(chunks, embeddings)
    
    # query = "Что такое сингулярное разложение?"
    # query_1 = "Психологизм и философия в произведениях Достоевского и Толстого"
    # query_2 = "Особенности драматургии Чехова и влияние Серебряного века"
    # query_3 = "Русская литература XIX–XX вв. и её мировое значение"
    # query_4 = "Национальный характер произведений"
    # query_embedding = embedding_service.create_embedding(query)

    # results = chroma_db.search(
    #     query_embedding=query_embedding,
    #     n_results=2
    # )

    # save_formatted_results(results)

    # save_formatted_results(
    #     formatted_results = chroma_db.search(
    #         query_embedding = embedding_service.create_embedding(query_1),
    #         n_results=2
    #     ),
    #     output_file = ".results/russian_literature_1.txt",
    # )

    # save_formatted_results(
    #     formatted_results = chroma_db.search(
    #         query_embedding = embedding_service.create_embedding(query_2),
    #         n_results=2
    #     ),
    #     output_file = ".results/russian_literature_2.txt",
    # )

    # save_formatted_results(
    #     formatted_results = chroma_db.search(
    #         query_embedding = embedding_service.create_embedding(query_3),
    #         n_results=2
    #     ),
    #     output_file = ".results/russian_literature_3.txt",
    # )

    # save_formatted_results(
    #     formatted_results = chroma_db.search(
    #         query_embedding = embedding_service.create_embedding(query_4),
    #         n_results=2
    #     ),
    #     output_file = ".results/russian_literature_4.txt",
    # )
    


    
