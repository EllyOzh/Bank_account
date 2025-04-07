import json
from typing import List, Dict

def reading_json(path: str) -> List[Dict]:
    """ Получение списка словарей с банковскими операциями.
     Принимает: path: Путь до JSON-файла.
     Возвращает: Список словарей с данными операций. """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []  # Файл не является списком
    except FileNotFoundError:
        print(f"Файл '{path}' не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка декодирования файла '{path}'. Возможно, файл поврежден или имеет неверный формат.")
        return []

if __name__ == '__main__':
        print(reading_json('../data/operations.json'))

