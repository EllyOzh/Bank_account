import re
import os
from src.csv_excel_reader import csv_read, excel_read
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.search_transactions import search_transactions_by_description
from src.utils import reading_json
from src.widget import get_date, mask_account_card


DATA_PATH = {
    "JSON": "data/operations.json",
    "CSV": "data/transactions.csv",
    "XLSX": "data/transactions_excel.xlsx",
}
STATUSES = ["CANCELED", "PENDING", "EXECUTED"]


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    while True:
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        choice_type_file = input("Ваш выбор: ")
        try:
            file_type = {
                '1': 'json',
                '2': 'csv',
                '3': 'xlsx'
            }.get(choice_type_file.strip())

            if not file_type:
                raise ValueError("Неверный выбор пункта меню")

            path_to_file = DATA_PATH.get(file_type.upper())

            if path_to_file is None or not os.path.exists(path_to_file):
                print("Ошибка: Файл не найден!")
                continue

            break
        except Exception as e:
            print(e)
            continue

    transactions = []
    if file_type == "json":
        transactions = reading_json(path_to_file)
    elif file_type == "csv":
        transactions = csv_read(path_to_file)
    elif file_type == "xlsx":
        transactions = excel_read(path_to_file)

    print(f"\nДля обработки выбран {file_type.upper()}-файл.\n")

    while True:
        status_input = input(
            "Введите статус операции, по которому необходимо выполнить фильтрацию."
            "\nДоступные для фильтрации статусы: {}\n".format(', '.join(STATUSES))
        )
        edited_status = status_input.strip().upper()
        if edited_status in STATUSES:
            break
        else:
            print("Статус операции '{edited_status}' недоступен")

    try:
        filtered_transactions = filter_by_state(transactions, edited_status)
    except KeyError as ke:
        print(f"Произошла ошибка при фильтрации: {ke}")

    print(f"\nОперации отфильтрованы по статусу {edited_status}.\n")

    while True:
        should_sort_by_date = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
        if should_sort_by_date.startswith('да'):
            order_choice = input("Отсортировать по возрастанию или убыванию?: ").strip().lower()
            if order_choice in ['возрастание', 'убывание']:
                is_ascending = False if order_choice.startswith('убывание') else True
                filtered_transactions = sort_by_date(filtered_transactions, ascending=is_ascending)
                print(f"Операции успешно отсортированы по дате ({order_choice}).")
                break
            else:
                print("Ошибка: выберите корректный параметр сортировки (возрастание или убывание)")
        elif should_sort_by_date.startswith('нет'):
            print("Фильтрация по дате отменена.")
            break
        else:
            print("Ошибка: введите \"Да\" или \"Нет\", чтобы продолжить.")

    sort_by_rubles_only = input("Выводить только рублевые транзакции? Да/Нет").strip().lower()
    if sort_by_rubles_only.startswith("да"):
        filtered_transactions = filter_by_currency(filtered_transactions, "RUB")

    description_filter = input(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет"
    ).strip().lower()
    if description_filter.startswith("да"):
        word_to_desc_filter = input("Введите слово для фильтрации описания: ").strip()
        filtered_transactions = search_transactions_by_description(filtered_transactions, word_to_desc_filter)

    filtered_transactions = list(filtered_transactions)
    if len(filtered_transactions) > 0:
        print("\nРаспечатываю итоговый список транзакций... \n")
        print(f"Всего банковских операций в выборке {len(transactions)}")
        for ind, transaction in enumerate(transactions):
            date = transaction.get('date', '')
            description = transaction.get('description', '')
            if choice_type_file == "1":
                currency = transaction.get("operationAmount").get("currency").get("name")
                amount = transaction.get("operationAmount").get("amount")
            else:
                currency = transaction.get("currency_name")
                amount = transaction.get("amount")
            masked_to = mask_account_card(transaction.get("to"))
            masked_from = ""
            if not re.match("открытие", description, flags=re.I):
                masked_from = mask_account_card(transaction.get("from"))
                masked_to = " -> " + masked_to

            print(f"{date} {description}\n{masked_from}{masked_to}\nСумма: {amount} {currency}\n")
    else:
        print("\nНе найдено ни одной транзакции, которая соответствует вашим условиям фильтрации.")

if __name__ == "__main__":
    main()