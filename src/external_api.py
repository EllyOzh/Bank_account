import requests
import os
from dotenv import load_dotenv
import json
from typing import Dict


# Загружаем токен из .env файла
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise Exception("Переменная окружения API_KEY не найдена. Проверьте настройки.")


def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Конвертирует валюту с использованием внешнего API.
    Принимает:
              amount: Сумма транзакции
              from_currency: Валюта источника
              to_currency: Целевая валюта
    Возвращает:: Конвертированная сумма
    """
    url = (
        f"https://api.apilayer.com/exchangerates_data/convert?"
        f"to={to_currency}&from={from_currency}&amount={amount}"
    )
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            try:
                data = response.json()
                return data['result']
            except json.JSONDecodeError:
                print(f"Не удалось распознать JSON-данные: {response.text}")
                return None
        else:
            error_message = response.json().get('error', {}).get('message')
            print(
                f"Возникла ошибка при обращении к API. "
                f"Код: {response.status_code}, Сообщение: {error_message}"
            )
            return None

    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")
        return None


def transaction_amount(transaction: Dict) -> float:
    """ Расчет суммы транзакции в рублях.
        Принимает: transaction: Словарь с данными транзакции.
        Возвращает: Сумма транзакции в рублях. """

    if 'operationAmount' not in transaction or 'currency' not in transaction['operationAmount']:
        print(f"Некорректная транзакция: {transaction}")
        return 0.0

    amount = transaction['operationAmount']['amount']
    currency = transaction['operationAmount']['currency']['code']

    print(f"Исходная сумма: {amount}, валюта: {currency}")

    if currency == 'RUB':
        print(f"Сумма в рублях: {amount}")
        return amount
    else:
        converted_amount = convert_currency(amount, currency, 'RUB')
        if converted_amount is not None:
            print(f"Преобразованная сумма: {converted_amount}")
            return converted_amount
        else:
            print(f"Ошибка конвертации для валюты {currency}")
            return 0.0


if __name__ == '__main__':
    print(transaction_amount({
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }))
