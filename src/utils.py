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
