import re
from collections import Counter
from src.search_transactions import search_transactions_by_description, count_transactions_by_categories
import pytest


@pytest.fixture()
def sample_categories():
    """Фикстура с примерами категорий"""
    return ['Перевод', 'Открытие']


@pytest.fixture()
def valid_transactions():
    """Фикстура с примерами транзакций"""
    return [
        {'id': 5341558.0, 'state': 'EXECUTED', 'date': '2022-11-11T12:32:14Z', 'amount': 20026.0,
         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'Mastercard 6912592331129080',
         'to': 'Счет 82572989412689103220', 'description': 'Перевод организации'},
        {'id': 3789074.0, 'state': 'EXECUTED', 'date': '2022-10-14T06:58:47Z', 'amount': 24034.0,
         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'Mastercard 3924656650212459',
         'to': 'American Express 9881727426631376', 'description': 'Перевод с карты на карту'},
        {'id': 4361453.0, 'state': 'EXECUTED', 'date': '2021-12-05T01:35:38Z', 'amount': 30045.0,
         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'Mastercard 3665700271480451',
         'to': 'American Express 0562165846839124', 'description': 'Перевод с карты на карту'},
        {'id': '5429839', 'state': 'EXECUTED', 'date': '2023-06-23T19:46:34Z', 'amount': '25261',
         'currency_name': 'Hryvnia', 'currency_code': 'UAH', 'from': '', 'to': 'Счет 76768135089446747029',
         'description': 'Открытие вклада'}
    ]

def test_search_transactions_by_description(valid_transactions):
    """Проверка успешной работы функции."""
    search_words = 'Перевод с карты на карту'
    expected_result = [
        {'id': 3789074.0, 'state': 'EXECUTED', 'date': '2022-10-14T06:58:47Z', 'amount': 24034.0,
         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'Mastercard 3924656650212459',
         'to': 'American Express 9881727426631376', 'description': 'Перевод с карты на карту'},
        {'id': 4361453.0, 'state': 'EXECUTED', 'date': '2021-12-05T01:35:38Z', 'amount': 30045.0,
         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'Mastercard 3665700271480451',
         'to': 'American Express 0562165846839124', 'description': 'Перевод с карты на карту'}
    ]
    result = search_transactions_by_description(valid_transactions, search_words)
    assert result == expected_result


def test_search_transactions_by_description_no_match(valid_transactions):
    """Тест функции, когда отсутствует подходящее описание операции"""
    search_words = "Покупка"
    expected_result = []
    result = search_transactions_by_description(valid_transactions, search_words)
    assert result == expected_result, f"Ошибка в поиске транзакций по запросу '{search_words}', ожидалось []"


def test_search_transactions_by_description_ignorecase(valid_transactions):
    """Проверка нечувствительности к регистру"""
    search_words = "открытие"
    expected_result = [
        {'id': '5429839', 'state': 'EXECUTED', 'date': '2023-06-23T19:46:34Z', 'amount': '25261',
         'currency_name': 'Hryvnia', 'currency_code': 'UAH', 'from': '', 'to': 'Счет 76768135089446747029',
         'description': 'Открытие вклада'}
    ]
    result = search_transactions_by_description(valid_transactions, search_words)
    assert result == expected_result,  (
      f"Ошибка в поиске транзакций по запросу '{search_words}', нечувствительность к регистру нарушена."
    )


def test_search_transactions_by_description_empty():
    """Проверка поиска в пустом списке транзакций."""
    transactions = []
    search_words = "открытие"
    expected_result = []

    result = search_transactions_by_description(transactions, search_words)
    assert result == expected_result, (
        f"Ошибка в поиске транзакций по запросу '{search_words}', пустой список транзакций."
    )


def test_pattern_compile_normal():
    """Проверка формирования регулярного выражения."""
    search_words = "Перевод"
    pattern = re.compile(re.escape(search_words), re.IGNORECASE)
    assert isinstance(pattern, re.Pattern)


def test_pattern_compile_special_chars():
    """Проверка формирования регулярного выражения с поиском специальной строки."""
    search_words = ".NET"
    pattern = re.compile(re.escape(search_words), re.IGNORECASE)
    assert isinstance(pattern, re.Pattern)


def test_search_transactions_by_description_missing_desc():
    """Проверка генерации результата при отсутствующем описании."""
    transactions = [{"description": None}, {"description": ""}]
    search_words = "Перевод"
    result = search_transactions_by_description(transactions, search_words)
    assert len(result) == 0


def test_search_transactions_by_description_multi_matches():
    """Проверка генерации результата, если совпадает с несколькими транзакциями."""
    transactions = [{"description": "Оплата налогов"}, {"description": "Оплата интернета"}]
    search_words = "Оплата"

    result = search_transactions_by_description(transactions, search_words)
    assert len(result) == 2


def test_create_counter():
    counter= Counter()
    assert isinstance(counter, Counter)


def test_get_and_lower_existing_desc():
    transaction = {"description": "Оплата интернета"}
    desc = transaction.get('description').lower()
    assert desc == "оплата интернета"


def test_update_counter_category():
    counter = Counter()
    found_categories = ['Оплата']
    counter.update(found_categories)
    assert counter['Оплата'] == 1


def test_update_counter_without_category():
    counter = Counter()
    found_categories = []
    counter.update(found_categories)
    assert sum(counter.values()) == 0


def test_count_transactions_by_categories(valid_transactions, sample_categories):
    """Проверка подсчета транзакций по существующим категориям."""
    expected_result = {
        'Перевод': 3,
        'Открытие': 1
    }

    result = count_transactions_by_categories(valid_transactions, sample_categories)
    assert result == expected_result, f"Ошибка подсчета транзакций по категориям"


def test_count_transactions_by_categories_not_category(valid_transactions, sample_categories):
    new_categories = sample_categories + ["Другие"]
    expected_result = {
        'Перевод': 3,
        'Открытие': 1,
        'Другие' : 0
    }

    result = count_transactions_by_categories(valid_transactions, new_categories)
    assert result == expected_result, f"Ошибка подсчета транзакций с дополнительной категорией."


def test_count_transactions_by_categories_empty_transactions(transactions, sample_categories):
    """Проверка подсчета категорий при пустом списке транзакций."""
    transactions = []
    expected_result = {
        'Перевод': 0,
        'Открытие': 0,
    }

    result = count_transactions_by_categories(transactions,sample_categories)
    assert result == expected_result, f"Ошибка подсчета транзакций: список транзакций не должен быть пустым."


def test_count_transactions_by_categories_empty_category(valid_transactions):
    """Проверка подсчета транзакций при отсутствии категорий."""
    empty_categories = []
    expected_result = {}

    result = count_transactions_by_categories(valid_transactions, empty_categories)
    assert result == expected_result, f"Ошибка подсчета транзакций: список категорий не должен быть пустым."


def test_count_transactions_by_categories_ignorcase(valid_transactions, sample_categories):
    new_sample_categories = ['ПЕРЕВОД', 'ОтКрЫтИе']
    expected_result = {
        'ПЕРЕВОД': 3,
        'ОтКрЫтИе': 1
    }

    result = count_transactions_by_categories(valid_transactions, new_sample_categories)
    assert result == expected_result, f"Ошибка нечувствительности к регистру."


def test_final_result_by_categories():
    counter = Counter({"Оплата": 2})
    categories = ["Оплата", "Покупка"]
    result = {category: counter[category] for category in categories}
    assert result == {"Оплата": 2, "Покупка": 0}

