import chromadb
from chromadb.config import Settings
from typing import Optional, Sequence
from pathlib import Path

from ..documents.models import DocumentChunk, Metadata, ChunkID, Content
from ..logger import logger

class DBLogger:
    def _logger_info(self, message: str):
        """
        Логирует информационное сообщение с указанием имени класса.

        Args:
            message (str): Сообщение для логирования.
        """
        name = self.__class__.__name__
        logger.info("[%s] %s", name, message)

    def _logger_error(self, message: str):
        """
        Логирует сообщение об ошибке с указанием имени класса.

        Args:
            message (str): Сообщение об ошибке для логирования.
        """
        name = self.__class__.__name__
        logger.error("[%s] %s", name, message)


class ChromaDB(DBLogger):
    """Хранилище векторных представлений на основе ChromaDB."""

    client: chromadb.ClientAPI
    collection: chromadb.Collection

    def __init__(
        self,
        collection_name: str = 'default',
        persist_directory: Optional[str] = None,
    ):
        """
        Args:
            collection_name: название коллекции, откуда читать/писать данные
            persist_directory: директория для хранения базы
        """
        super().__init__()

        persist_directory_path = str(Path('./.db', persist_directory) if persist_directory else Path('./.db'))

        self._logger_info("Инициализация ChromaDB...")

        try:
            # Инициализируем клиент ChromaDB с постоянным хранилищем (встроенная SQLite)
            # Клиент chromadb.Client() хранит данные в памяти, не использует постоянные хранилища
            self.client = chromadb.PersistentClient(
                path=persist_directory_path,
                settings=Settings(
                    anonymized_telemetry=False,   # Отключаем отправку телеметрии
                    # is_persistent=True            # Используем постоянные хранилища
                )
            )
        except Exception as e:
            self._logger_error(f"Ошибка инициализации: {e}")
            raise

        try:
            # Получаем существующую коллекцию или создаем новую
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                configuration={
                    "hnsw": {
                        "space": "cosine",
                        # "ef_construction": 200 # 100 по умолчанию
                    }
                },
            )
        except Exception as e:
            self._logger_error(f"Ошибка коллекции {collection_name}: {e}")
            raise

        self._logger_info("Инициализация завершена!")

    def clear_collection(self):
        """
        Очищает все данные из коллекции.
        """
        try:
            self._logger_info("Очистка коллекции...")
            
            # Получаем все ID документов в коллекции
            all_data = self.collection.get()
            
            if all_data['ids']:
                # Удаляем все документы по их ID
                self.collection.delete(ids=all_data['ids'])
                self._logger_info(f"Удалено {len(all_data['ids'])} документов из коллекции")
            else:
                self._logger_info("Коллекция уже пуста")
                
        except Exception as e:
            self._logger_error(f"Ошибка очистки коллекции: {e}")
            raise

    def add_documents(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ):
        """
        Добавление документов в хранилище.
        
        Args:
            chunks: список чанков документов
            embeddings: список векторных представлений
        """
        try:
            self._logger_info(f"Добавление документов в хранилище...")
            # Подготавливаем данные для ChromaDB
            ids: list[ChunkID] = []
            documents: list[Content] = []
            metadatas: list[Metadata] = []

            for chunk in chunks:
                ids.append(chunk.chunk_id)
                documents.append(chunk.content)
                metadatas.append(chunk.metadata)

            # embeddings_seq: list[Sequence[float]] = [tuple(vec) for vec in embeddings]

            import time

            # Заснуть на 2 секунды
            time.sleep(2)

            self.collection.add(
                ids=ids,  # ID каждого чанка
                documents=documents,   # Содержимое каждого чанка
                metadatas=metadatas,   # Метаданные каждого чанка
                embeddings=embeddings, # type: ignore # Векторные представления, приведённые к float
            )

            # time.sleep(2)
            self._logger_info(f"Добавление документов в хранилище завершено!")

        except Exception as e:
            # print(e)
            # self._logger_error(f"Ошибка добавления документов!")
            # self._logger_error(f"Ошибка в test_vector_store: {e.__traceback__}")
            # self._logger_error(f"e.__class__.__name__: {e.__class__.__name__}")
            
            raise

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 3,
        **kwargs
    ):
        """
        Поиск похожих документов.
        
        Args:
            query_embedding: векторное представление поискового запроса
            n_results: количество результатов
            **kwargs: дополнительные параметры поиска
            
        Returns:
            Список найденных документов с метаданными
        """

        try:
            self._logger_info(f"Поиск похожих документов...")
            # Выполняем поиск в ChromaDB
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results,
                **kwargs
            )

            # Проверяем наличие результатов
            if not results['ids'] or not results['documents'] or not results['distances']:
                self._logger_info("Нет результатов поиска")
                return []

            # Берем первый список, так как query_embeddings был один
            ids = results['ids'][0]  # List[str]
            documents = results['documents'][0]  # List[str]
            distances = results['distances'][0]  # List[float]
            # metadatas может быть None, поэтому используем get
            # metadatas = results.get('metadatas')[0]  # List[Dict]

            # Форматируем результаты
            formatted_results = [
                {
                    'id': id_,
                    'content': doc,
                    'distance': dist
                }
                for id_, doc, dist in zip(ids, documents, distances)
            ]
            
            return formatted_results

        except Exception as e:
            self._logger_error(f"Ошибка поиска: {e}")
            raise

    def get_collection_stats(self):
        """Получение статистики о коллекции"""
        count = self.collection.count()  # Количество документов
        return {
            "total_documents": count,
            "collection_name": self.collection.name
        }