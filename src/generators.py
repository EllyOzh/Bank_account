from typing import Dict, List, Union

def filter_by_currency(transactions: List[Dict[str, Union[str, int]]], currency: str) -> List[Dict[str, Union[str, int]]]:
    filter_by_transactions = []
    for transaction in transactions:
        if transaction['operationAmount']['code'] == currency:
            filter_by_transactions.append(transaction)
    return filter_by_transactions


def transaction_descriptions(transactions: List[Dict[str, Union[str, int]]]) -> None:
    for transaction in transactions:
        if transaction.get('description'):
            yield transaction['description']


def card_number_generator(low_limit: int, upper_limit: int) -> int:
    """Генератор банковских карт. Выдаёт номера банковских карт в формате ХХХХ ХХХХ ХХХХ ХХХХ где Х - цифра"""
    numbers_generate = (x for x in range(low_limit, upper_limit))
    for number in numbers_generate:
        number = str(number).zfill(16)
        yield f"{number[0:4]} {number[4:8]} {number[8:12]} {number[12:16]}"


for card_number in card_number_generator(1, 5):
    print(card_number)
