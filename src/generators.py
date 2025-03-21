from typing import Dict, Iterator, List

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    """Ф-я принимает на вход список словарей c транзакциями, возвращает итератор, который поочередно
    выдает транзакции, где валюта операции соответствует заданной."""
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            # значение по ключам
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> None:
    """Генератор, - принимает список словарей с транзакциями и
    возвращает описание каждой операции по очереди."""
    for transaction in transactions:
        if transaction.get("description"):  # проверка значения по ключу description
            yield transaction["description"]
        else:
            yield ""


def card_number_generator(low_limit: int, upper_limit: int) -> Iterator[str]:
    """Генератор банковских карт. Выдаёт номера банковских карт в формате ХХХХ ХХХХ ХХХХ ХХХХ где Х - цифра"""
    if not isinstance(low_limit, int) or not isinstance(upper_limit, int):
        raise ValueError("Значения диапазона - целые числа")
    if low_limit < 1 or upper_limit > 9999999999999999:
        raise ValueError("Некорректный диапазон. [low_limit:upper_limit] = [1:9999999999999999]")
    if low_limit > upper_limit:
        raise ValueError("Некорректный диапазон. [low_limit:upper_limit] = [1:9999999999999999]")

    numbers_generate = (x for x in range(low_limit, upper_limit))
    for number in numbers_generate:
        number = str(number).zfill(16)
        yield f"{number[0:4]} {number[4:8]} {number[8:12]} {number[12:16]}"


if __name__ == "__main__":
    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))

    descriptions = transaction_descriptions(transactions)
    for _ in range(5):
        print(next(descriptions))

    for card_number in card_number_generator(1, 5):
        print(card_number)
