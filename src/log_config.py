import logging
import os

log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)

log_format = "%(asctime)s - %(name)s -  %(funcName)s - %(levelname)s - %(message)s"


def setup_logger(name: str, log_file: str, level: int = logging.DEBUG) -> logging.Logger:
    """ Запись логов в отдельный файл."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(os.path.join(log_dir, log_file), mode="w", encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format))

    # Проверка: существуют ли обработчики и удаляются старые, чтобы избежать дублирования записей
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(file_handler)

    return logger


masks_logger = setup_logger("masks", "masks.log", logging.DEBUG)
utils_logger = setup_logger("utils", "utils.log", logging.DEBUG)
