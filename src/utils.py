import json
from typing import Dict, List

from src.log_config import utils_logger


def reading_json(path: str) -> List[Dict]:
    """ Получение списка словарей с банковскими операциями.
     Принимает: path: Путь до JSON-файла.
     Возвращает: Список словарей с данными операций. """

    utils_logger.debug(f"Проверка возможности открыть файл {path}")
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                utils_logger.info(f"Файл {path} успешно загружен. Найдено {len(data)} записей.")
                return data
            else:
                utils_logger.warning(f"Файл {path} не содержит список транзакций.")
                return []  # Файл не является списком
    except FileNotFoundError:
        print(f"Файл '{path}' не найден.")
        utils_logger.error(f"Файл {path} не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка декодирования файла '{path}'. Возможно, файл поврежден или имеет неверный формат.")
        utils_logger.error(
            f"Ошибка декодирования файла '{path}'. Возможно, файл поврежден или имеет неверный формат."
        )
        return []


if __name__ == '__main__':
    print(reading_json('../data/operations.json'))
