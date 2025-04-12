from unittest.mock import patch, mock_open
import pytest
from src.csv_excel_reader import csv_read, excel_read
import pandas as pd


# Фрагмент содержания CSV файла
CSV_CONTENT = """id;state;date;amount;currency_name;currency_code;from;to;description
650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации
3598919;EXECUTED;2020-12-06T23:00:58Z;29740;Peso;COP;Discover 3172601889670065;Discover 0720428384694643;Перевод с карты на карту""".strip()


@pytest.fixture(scope="function")
def mocked_csv_file(tmpdir_factory):
    """Создаем временный CSV файл для тестирования"""
    temp_dir = tmpdir_factory.mktemp("data")
    file_path = temp_dir.join("transactions.csv").strpath
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(CSV_CONTENT)
    yield file_path


def test_csv_read_success(mocked_csv_file):
    """Тестируем успешное чтение CSV файла"""
    expected_result = [
        {
            'id': '650703',
            'state': 'EXECUTED',
            'date': '2023-09-05T11:30:32Z',
            'amount': '16210',
            'currency_name': 'Sol',
            'currency_code': 'PEN',
            'from': 'Счет 58803664561298323391',
            'to': 'Счет 39745660563456619397',
            'description': 'Перевод организации'
        },
        {
            'id': '3598919',
            'state': 'EXECUTED',
            'date': '2020-12-06T23:00:58Z',
            'amount': '29740', 'currency_name':
            'Peso', 'currency_code': 'COP',
            'from': 'Discover 3172601889670065',
            'to': 'Discover 0720428384694643',
            'description': 'Перевод с карты на карту'

        }
    ]
    result = csv_read(mocked_csv_file)
    assert result == expected_result


@patch('src.csv_excel_reader.open', side_effect=FileNotFoundError)
def test_csv_read_file_not_found(mocked_open):
    """Тестируем случай отсутствия CSV файла"""
    with pytest.raises(FileNotFoundError):
        csv_read('/nonexistent/file/path.csv')


@patch('src.csv_excel_reader.open', new_callable=mock_open, read_data='')
def test_csv_read_empty_file(mocked_open):
    """Тестируем чтение пустого CSV файла"""
    with pytest.raises(ValueError):
        csv_read('/empty/file/path.csv')


EXCEL_DATA = {
    'date': ['2022-03-10', '2022-04-20'],
    'amount': [1500, -200],
    'description': ["Покупка товаров", "Комиссия"]
}


@pytest.fixture(scope="function")
def mocked_xlsx_file(tmpdir_factory):
    """Создаем временный XLSX файл для тестирования"""
    temp_dir = tmpdir_factory.mktemp("data")
    file_path = temp_dir.join("transactions.xlsx").strpath
    df = pd.DataFrame(EXCEL_DATA)
    df.to_excel(file_path, index=False)
    yield file_path


@patch('src.csv_excel_reader.pd.read_excel')
def test_excel_read_success(mock_read_excel, mocked_xlsx_file):
    """Тестируем успешное чтение XLSX файла"""
    mock_read_excel.return_value = pd.DataFrame(EXCEL_DATA)
    expected_result = [
        {'date': '2022-03-10', 'amount': 1500, 'description': 'Покупка товаров'},
        {'date': '2022-04-20', 'amount': -200, 'description': 'Комиссия'}
    ]
    result = excel_read(mocked_xlsx_file)
    assert result == expected_result


@patch('src.csv_excel_reader.pd.read_excel', side_effect=FileNotFoundError)
def test_excel_read_file_not_found(mock_read_excel):
    """Тестируем случай отсутствия XLSX файла"""
    with pytest.raises(FileNotFoundError):
        excel_read('/nonexistent/file/path.xlsx')


@patch('src.csv_excel_reader.pd.read_excel', return_value=pd.DataFrame())
def test_excel_read_empty_file(mock_read_excel):
    """Тестируем чтение пустого XLSX файла"""
    with pytest.raises(ValueError):
        excel_read('/empty/file/path.xlsx')
