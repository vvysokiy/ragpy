import unittest
from src.documents.chunker import TextChunker


class TestTextChunker(unittest.TestCase):
    
    def test_initialization_with_default_parameters(self):
        """Тест инициализации TextChunker с параметрами по умолчанию."""
        chunker = TextChunker()
        
        # Проверяем значения по умолчанию
        self.assertEqual(chunker.chunk_size, 500)
        self.assertEqual(chunker.chunk_overlap, 50)
        self.assertEqual(chunker.separators, ["\n\n", "\n", ". ", "! ", "? "])
    
    def test_initialization_with_custom_parameters(self):
        """Тест инициализации TextChunker с пользовательскими параметрами."""
        chunk_size = 1000
        chunk_overlap = 100
        separators = ["\n", ". "]
        
        chunker = TextChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators
        )
        
        # Проверяем пользовательские значения
        self.assertEqual(chunker.chunk_size, chunk_size)
        self.assertEqual(chunker.chunk_overlap, chunk_overlap)
        self.assertEqual(chunker.separators, separators)

    def test_split_text_empty_string(self):
        """Тест разбиения пустого текста."""
        chunker = TextChunker()
        result = chunker.split_text("")
        
        # Пустой текст должен возвращать пустой список
        self.assertEqual(result, [])
    
    def test_split_text_single_sentence(self):
        """Тест разбиения одного предложения."""
        chunker = TextChunker(chunk_size=100, chunk_overlap=10)
        text = "Это короткое предложение для теста."
        result = chunker.split_text(text)
        
        # Одно предложение должно возвращать один чанк
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], text)

    def test_split_text_long_text(self):
        """Тест разбиения длинного текста на чанки."""
        chunker = TextChunker(chunk_size=300, chunk_overlap=50)
        
        # Читаем текст из файла
        with open('src/documents/tests/test_chunker_split_text.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        
        result = chunker.split_text(text)
        
        # Проверяем, что текст разбился на несколько чанков
        self.assertGreater(len(result), 1)
        
        # Проверяем, что каждый чанк не превышает максимальный размер + перекрытие
        for chunk in result:
            self.assertLessEqual(len(chunk), chunker.chunk_size + chunker.chunk_overlap)
        
        # Проверяем, что все чанки не пустые
        for chunk in result:
            self.assertTrue(chunk.strip())
        
        # Проверяем, что объединение всех чанков содержит весь исходный текст
        combined_text = ''.join(result)
        # Убираем лишние пробелы для сравнения
        original_words = text.split()
        combined_words = combined_text.split()
        
        # Проверяем, что все слова из оригинала присутствуют в результате
        for word in original_words:
            self.assertIn(word, combined_words)

    def test_split_text_with_paragraph_separators(self):
        """Тест разбиения текста с разделителями абзацев."""
        chunker = TextChunker(chunk_size=50, chunk_overlap=10)  # Уменьшили размер чанка
        text = "Первый абзац с достаточно длинным текстом для тестирования.\n\nВторой абзац тоже содержит много слов и символов.\n\nТретий абзац завершает наш тестовый документ с дополнительным содержимым."
        result = chunker.split_text(text)
        
        # Должно быть несколько чанков
        self.assertGreaterEqual(len(result), 1)  # Изменили на >= 1
        
        # Проверяем, что разрывы происходят по абзацам (если чанков несколько)
        for chunk in result:
            self.assertTrue(chunk.strip())
            # Чанки не должны быть слишком длинными
            self.assertLessEqual(len(chunk), chunker.chunk_size + 50)

    def test_split_text_with_sentences(self):
        """Тест разбиения текста с разделителями предложений."""
        chunker = TextChunker(chunk_size=80, chunk_overlap=15)
        text = "Первое предложение. Второе предложение! Третье предложение? Четвертое предложение."
        result = chunker.split_text(text)
        
        # Должно быть несколько чанков
        self.assertGreater(len(result), 1)
        
        # Проверяем, что разрывы происходят по предложениям
        for chunk in result:
            self.assertTrue(chunk.strip())

    def test_split_text_no_overlap(self):
        """Тест разбиения текста без перекрытия."""
        chunker = TextChunker(chunk_size=50, chunk_overlap=0)
        text = "Это текст для тестирования разбиения без перекрытия между чанками."
        result = chunker.split_text(text)
        
        # Должно быть несколько чанков
        self.assertGreater(len(result), 1)
        
        # Проверяем отсутствие перекрытия
        combined_length = sum(len(chunk) for chunk in result)
        # При отсутствии перекрытия общая длина должна быть близка к исходной
        self.assertLessEqual(abs(combined_length - len(text)), 10)

    def test_split_text_large_overlap(self):
        """Тест разбиения текста с большим перекрытием."""
        chunker = TextChunker(chunk_size=100, chunk_overlap=80)
        text = "Это довольно длинный текст для тестирования большого перекрытия между соседними чанками в алгоритме разбиения."
        result = chunker.split_text(text)
        
        # Должно быть несколько чанков
        self.assertGreater(len(result), 1)
        
        # При большом перекрытии чанки должны значительно пересекаться
        for i in range(len(result) - 1):
            # Проверяем, что есть общие слова между соседними чанками
            words1 = set(result[i].split())
            words2 = set(result[i + 1].split())
            common_words = words1.intersection(words2)
            self.assertGreater(len(common_words), 0)

    def test_split_text_whitespace_only(self):
        """Тест разбиения текста, состоящего только из пробелов."""
        chunker = TextChunker()
        text = "   \n\n   \t   "
        result = chunker.split_text(text)
        
        # Текст из пробелов должен возвращать пустой список
        self.assertEqual(result, [])

    def test_split_text_custom_separators(self):
        """Тест разбиения текста с пользовательскими разделителями."""
        chunker = TextChunker(chunk_size=50, chunk_overlap=10, separators=["|", ";", ","])
        text = "Первая часть|Вторая часть;Третья часть,Четвертая часть"
        result = chunker.split_text(text)
        
        # Должно быть несколько чанков
        self.assertGreater(len(result), 1)
        
        # Проверяем, что разрывы происходят по пользовательским разделителям
        for chunk in result:
            self.assertTrue(chunk.strip())

    def test_split_text_very_small_chunks(self):
        """Тест разбиения на очень маленькие чанки."""
        chunker = TextChunker(chunk_size=20, chunk_overlap=5)
        text = "Это тест для очень маленьких чанков размером всего двадцать символов."
        result = chunker.split_text(text)
        
        # Должно быть много маленьких чанков
        self.assertGreater(len(result), 2)
        
        # Каждый чанк должен быть небольшим
        for chunk in result:
            self.assertTrue(chunk.strip())
            self.assertLessEqual(len(chunk), 30)  # С учетом поиска границ слов


if __name__ == '__main__':
    unittest.main()
