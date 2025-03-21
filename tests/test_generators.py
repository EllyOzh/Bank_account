import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_ok(transactions):
    # тест корректной фильтрации транзакции по заданной валюте
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 1
    assert usd_transactions[0]["id"] == 1


empty_list = []


# Проверка, что генератор не завершается ошибкой при обработке пустого списка
def test_filter_by_currency_empty():
    usd_transactions = list(filter_by_currency(empty_list, "USD"))
    assert len(usd_transactions) == 0


transactions_ = [
    {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
    {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
    {"id": 3, "operationAmount": {"amount": "1000"}},  # Нет ключа "currency"
]


def test_filter_by_currency_missing_currency():
    # тест на корректную обработку случаев, когда транзакции в заданной валюте отсутствуют
    usd_transactions = list(filter_by_currency(transactions_, "USD"))
    assert len(usd_transactions) == 1
    assert usd_transactions[0]["id"] == 1


def test_transaction_descriptions_ok(transactions_list):  # тест корректной отработки
    generator_ = transaction_descriptions(transactions_list)
    assert "Перевод организации" == next(generator_)
    assert "Перевод со счета на счет" == next(generator_)


def test_transaction_descriptions_not_descriptions(transactions):  # тест при отсутствии 'descriptions'
    generator_ = transaction_descriptions(transactions)

    assert "" == next(generator_)
    assert "" == next(generator_)


def test_card_number_generator_ok():  # тест корректной работы генератора
    generator_ = card_number_generator(1, 6)
    assert next(generator_) == "0000 0000 0000 0001"
    assert next(generator_) == "0000 0000 0000 0002"
    assert next(generator_) == "0000 0000 0000 0003"
    assert next(generator_) == "0000 0000 0000 0004"
    assert next(generator_) == "0000 0000 0000 0005"


def test_card_number_generator_error(params_card_number_generator_error):  # тестирование ошибок ValueError
    low_limit, upper_limit, expected = params_card_number_generator_error
    with pytest.raises(ValueError) as exc_info:
        for card_number in card_number_generator(low_limit, upper_limit):
            assert str(exc_info.value) == expected
