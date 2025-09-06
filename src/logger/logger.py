import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def console_handler() -> logging.StreamHandler:
    """
    Создание обработчика для вывода в консоль.
    """
    # Форматтер для консольного обработчика
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Выбираем поток для вывода - sys.stdout для стандартного вывода в консоль
    handler = logging.StreamHandler(sys.stdout)
    # Устанавливаем форматтер для обработчика
    handler.setFormatter(formatter)

    return handler

def file_handler(
    name: str,
    log_file: str,
    log_dir: str,
) -> logging.FileHandler:
    """
    Создание обработчика для вывода в файл.

    Args:
        name: Имя логгера
        log_file: Имя файла для логов
        log_dir: Директория для файлов логов
    """
    log_file = log_file or f".{name}.log"
    # Создаем директорию для логов, если её нет
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Форматтер для консольного обработчика
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Выбираем поток для вывода - файл для вывода логов
    handler = RotatingFileHandler(
        filename = log_path / log_file,
        maxBytes = 10 * 1024 * 1024, # 10MB
        backupCount = 5, # 5 файлов
        encoding = "utf-8",
    )
    # Устанавливаем форматтер для обработчика
    handler.setFormatter(formatter)

    return handler

def setup_logger(
    name: str,
    log_file: str = "",
    log_level: int = logging.INFO,
    log_dir: str = "",
):
    """
    Настройка логгера с выводом в файл и консоль.

    Args:
        name: Имя логгера
        log_file: Имя файла для логов
        log_level: Уровень логирования
        log_dir: Директория для файлов логов

    Returns:
        logging.Logger: Настроенный логгер
    """
    new_logger = logging.getLogger(name)
    new_logger.setLevel(log_level)

    new_logger.handlers.clear()
    new_logger.addHandler(console_handler())
    new_logger.addHandler(file_handler(name, log_file, log_dir))

    # Отключаем передачу логов родительскому логгеру
    new_logger.propagate = False

    return new_logger

logger = setup_logger("ragpy")
