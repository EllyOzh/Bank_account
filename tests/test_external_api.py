from src.external_api import convert_currency
import pytest
from unittest.mock import patch, MagicMock
import requests
import os


# Фиктивное значение API_KEY для тестов
FAKE_API_KEY = os.getenv("API_KEY")


# Фиксируем значение API_KEY
@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("API_KEY", FAKE_API_KEY)


# Тест на успешное выполнение конверсии
def test_convert_currency_success(mock_requests_get):
    # Настраиваем мок на успешный ответ от API
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 1500.00}
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    # Вызываем функцию
    result = convert_currency(1000, "EUR", "USD")

    # Проверяем результат
    assert result == 1500.00
    mock_requests_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert?to=USD&from=EUR&amount=1000",
        headers={"apikey": FAKE_API_KEY},
        timeout=10
    )


# Тест на ошибку валидации ключа API
def test_convert_currency_invalid_api_key(mock_requests_get):
    # Настраиваем мок на ошибку API
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": {"code": 401, "message": "Invalid API key."}}
    mock_response.status_code = 401
    mock_requests_get.return_value = mock_response

    # Вызываем функцию
    result = convert_currency(1000, "EUR", "USD")

    # Проверяем результат
    assert result is None
    mock_requests_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert?to=USD&from=EUR&amount=1000",
        headers={"apikey": FAKE_API_KEY},
        timeout=10
    )


# Тест на ошибку подключения
def test_convert_currency_connection_error(mock_requests_get):
    # Настраиваем мок на ошибку подключения
    mock_requests_get.side_effect = requests.exceptions.ConnectionError

    # Вызываем функцию
    result = convert_currency(1000, "EUR", "USD")

    # Проверяем результат
    assert result is None


# Фиксируем вызов get для тестов
@pytest.fixture
def mock_requests_get(monkeypatch):
    with patch("src.external_api.requests.get") as mock_get:
        yield mock_get
