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


if __name__ == '__main__':
    unittest.main()
