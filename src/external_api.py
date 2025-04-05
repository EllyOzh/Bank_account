import requests
import os
from dotenv import load_dotenv
import json

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
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"
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
            print(f"Возникла ошибка при обращении к API. Код: {response.status_code}, Сообщение: {error_message}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")
        return None
