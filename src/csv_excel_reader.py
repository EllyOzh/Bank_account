import csv
from typing import List, Dict
import pandas as pd


def csv_read(file_path: str) -> List[Dict]:
    """Функция чтения финансовых операций из CSV-файла.
    Принимает: путь к файлу, возвращает: список словарей."""
    transactions = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            if not reader.fieldnames:
                raise ValueError("Файл пуст или неверный формат")

            for row in reader:
                transactions.append(row)

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не найден.")
    except Exception as e:
        raise ValueError(f"Произошла ошибка при чтении файла {str(e)}")
    return transactions


def excel_read(path_to_file_excel: str) -> List[Dict]:
    """Функция чтения файла Excel.
    Принимает: путь к файлу, возвращает список словарей с транзакциями"""
    try:
        df = pd.read_excel(path_to_file_excel)
        if df.empty:
            raise ValueError("Файл пуст или неверный формат")
        transactions = df.to_dict('records')
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {path_to_file_excel} не найден.")
    except Exception as f:
        raise ValueError(f"Произошла ошибка при чтении файла {str(f)}")
    return transactions


if __name__ == '__main__':
    transactions_csv = csv_read('../data/transactions.csv')
    print(transactions_csv)

    transactions_excel = excel_read('../data/transactions_excel.xlsx')
    print(transactions_excel)
