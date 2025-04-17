import re
from collections import Counter
from typing import List, Dict


def search_transactions_by_description(transactions: List[Dict], search_words: str) -> List[Dict]:
    """Функция для поиска банковских операций по описанию.
    Принимает список словарей с данными о банковских операциях и строку поиска.
    Возвращает список словарей, у которых в писании есть данная строка."""

    pattern = re.compile(re.escape(search_words), re.IGNORECASE)
    return [
        transaction for transaction in transactions if pattern.search(str(transaction.get('description', '')))
    ]


def count_transactions_by_categories(transactions: List[Dict], categories: List[str]) -> dict:
    """Функция, которая считает количество операций в определенных категориях.
    Принимает список словарей с данными о банковских операциях и список возможных категорий операций.
    Возвращает словарь, в котором ключ - это категория, а значение - количество операций в этой категории."""

    counter = Counter()

    for transaction in transactions:
        description = transaction.get('description').lower()
        # Создаем список категорий, которые присутствуют в описании
        found_categories = [category for category in categories if category.lower() in description]
        # Добавляем найденные категории в счетчик
        counter.update(found_categories)

    return {category: counter[category] for category in categories}


if __name__ == '__main__':
    transactions = [
        {'id': '650703', 'state': 'EXECUTED', 'date': '2023-09-05T11:30:32Z', 'amount': '16210',
         'currency_name': 'Sol', 'currency_code': 'PEN', 'from': 'Счет 58803664561298323391',
         'to': 'Счет 39745660563456619397', 'description': 'Перевод организации'},
        {'id': '3598919', 'state': 'EXECUTED', 'date': '2020-12-06T23:00:58Z', 'amount': '29740',
         'currency_name': 'Peso', 'currency_code': 'COP', 'from': 'Discover 3172601889670065',
         'to': 'Discover 0720428384694643', 'description': 'Перевод с карты на карту'},
        {'id': '5429839', 'state': 'EXECUTED', 'date': '2023-06-23T19:46:34Z', 'amount': '25261',
         'currency_name': 'Hryvnia', 'currency_code': 'UAH', 'from': '', 'to': 'Счет 76768135089446747029',
         'description': 'Открытие вклада'}
    ]

    categories = ['Перевод', 'Открытие вклада']
    search_words = 'Перевод организации'

    search_transactions = search_transactions_by_description(transactions, search_words)
    print(search_transactions)

    count_transactions = count_transactions_by_categories(transactions, categories)
    print(count_transactions)
