from .logger import logger
from typing import Any
from .documents.models import DocumentChunk


def save_chunks_analysis(chunks: list[DocumentChunk], output_file: str):
    """
    Сохраняет чанки с аналитической информацией.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        # Общая информация
        f.write("Анализ разбиения документа на чанки\n")
        f.write(f"Всего чанков: {len(chunks)}\n")
        f.write(f"Исходный документ: {chunks[0].metadata['source']}\n\n")

        # Статистика
        sizes = [len(chunk.content) for chunk in chunks]
        f.write(f"Минимальный размер чанка: {min(sizes)} символов\n")
        f.write(f"Максимальный размер чанка: {max(sizes)} символов\n")
        f.write(f"Средний размер чанка: {sum(sizes)/len(sizes):.2f} символов\n\n")

        # Содержимое чанков
        for chunk in chunks:
            f.write(f"\nЧанк {chunk.chunk_index + 1}/{len(chunks)}\n")
            f.write(f"Размер: {len(chunk.content)} символов\n")
            f.write("Содержимое:\n")
            f.write("-" * 50 + "\n")
            f.write(chunk.content)
            f.write("\n" + "-" * 50 + "\n")


def save_formatted_results(
    formatted_results: list[dict[str, Any]],
    output_file: str = ".results/formatted_results.txt"
) -> None:
    """
    Сохраняет отформатированные результаты в файл.
    
    Args:
        formatted_results: список результатов поиска
        output_file: путь к файлу для сохранения
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write(f"Результаты поиска ({len(formatted_results)} найдено)\n")
            f.write("=" * 50 + "\n\n")
            
            for i, result in enumerate(formatted_results, 1):
                f.write(f"Документ {i}/{len(formatted_results)}\n")
                f.write(f"Расстояние: {result['distance']:.4f}\n")
                f.write(f"ID: {result['id']}\n")
                f.write("\nСодержание:\n")
                f.write(result['content'])
                f.write("\n\nМетаданные:\n")
                # for key, value in result['metadata'].items():
                #     f.write(f"  {key}: {value}\n")
                # f.write("\n" + "-" * 50 + "\n\n")
                
        logger.info(f"Результаты сохранены в файл: {output_file}")
        
    except Exception as e:
        logger.error(f"Ошибка при сохранении результатов: {str(e)}")
        raise


def save_text_chunker_results(
    chunks: list[DocumentChunk], 
    output_file: str = ".results/TextChunker_results.txt"
) -> None:
    """
    Сохраняет результаты работы TextChunker в файл.
    
    Args:
        chunks: список чанков, созданных TextChunker
        output_file: путь к файлу для сохранения результатов
    """
    try:
        # Создаем директорию, если её нет
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Заголовок
            f.write("=" * 60 + "\n")
            f.write("РЕЗУЛЬТАТЫ РАБОТЫ TEXT CHUNKER\n")
            f.write("=" * 60 + "\n\n")
            
            if not chunks:
                f.write("Чанки не найдены.\n")
                return
            
            # Общая статистика
            f.write("ОБЩАЯ СТАТИСТИКА:\n")
            f.write(f"Всего чанков: {len(chunks)}\n")
            f.write(f"Исходный документ: {chunks[0].metadata.get('source', 'Неизвестно')}\n")
            
            # Статистика размеров
            sizes = [len(chunk.content) for chunk in chunks]
            f.write(f"Минимальный размер чанка: {min(sizes)} символов\n")
            f.write(f"Максимальный размер чанка: {max(sizes)} символов\n")
            f.write(f"Средний размер чанка: {sum(sizes)/len(sizes):.2f} символов\n")
            f.write(f"Общий размер всех чанков: {sum(sizes)} символов\n\n")
            
            # Параметры чанкинга (если доступны в метаданных)
            first_chunk = chunks[0]
            f.write("ПАРАМЕТРЫ ЧАНКИНГА:\n")
            f.write(f"Общее количество чанков: {first_chunk.metadata.get('total_chunks', len(chunks))}\n")
            f.write(f"ID исходного документа: {first_chunk.metadata.get('original_document_id', 'Неизвестно')}\n\n")
            
            # Детальная информация по каждому чанку
            f.write("ДЕТАЛЬНАЯ ИНФОРМАЦИЯ ПО ЧАНКАМ:\n")
            f.write("=" * 60 + "\n\n")
            
            for i, chunk in enumerate(chunks):
                f.write(f"ЧАНК {chunk.chunk_index + 1}/{len(chunks)}\n")
                f.write(f"ID чанка: {chunk.chunk_id}\n")
                f.write(f"Индекс: {chunk.chunk_index}\n")
                f.write(f"Размер: {len(chunk.content)} символов\n")
                f.write(f"ID документа: {chunk.doc_id}\n")
                
                # Дополнительные метаданные
                if chunk.metadata:
                    f.write("Метаданные:\n")
                    for key, value in chunk.metadata.items():
                        if key not in ['chunk_index', 'total_chunks', 'chunk_size', 'original_document_id']:
                            f.write(f"  {key}: {value}\n")
                
                f.write("\nСОДЕРЖИМОЕ:\n")
                f.write("-" * 50 + "\n")
                f.write(chunk.content)
                f.write("\n" + "-" * 50 + "\n\n")
                
                # Разделитель между чанками
                if i < len(chunks) - 1:
                    f.write("~" * 30 + "\n\n")
            
            # Итоговая информация
            f.write("=" * 60 + "\n")
            f.write("АНАЛИЗ ЗАВЕРШЕН\n")
            f.write(f"Результаты сохранены: {output_file}\n")
            f.write("=" * 60 + "\n")
                
        logger.info(f"Результаты TextChunker сохранены в файл: {output_file}")
        
    except Exception as e:
        logger.error(f"Ошибка при сохранении результатов TextChunker: {str(e)}")
        raise
