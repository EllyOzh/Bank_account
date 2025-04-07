import pytest
import json
from unittest.mock import patch, mock_open
from src.utils import reading_json


@pytest.fixture
def valid_json():
    return [
        {"operation": "deposit", "amount": 1000},
        {"operation": "withdrawal", "amount": 500}
    ]

@pytest.fixture
def invalid_json():
    return '{"invalid":'

def test_reading_valid_file(monkeypatch, valid_json):
    """ Проверка успешного чтения корректного JSON-файла. """
    monkeypatch.setattr("builtins.open", mock_open(read_data=json.dumps(valid_json)))
    result = reading_json("/some/path")
    assert result == valid_json


def test_missing_file(monkeypatch):
    """ Проверяем случай отсутствия файла. """
    # Создаем Mock объект, который вызовет исключение FileNotFoundError
    mock_file = mock_open()
    mock_file.side_effect = FileNotFoundError
    monkeypatch.setattr("builtins.open", mock_file)

    result = reading_json("/nonexistent_path")
    assert result == []

def test_invalid_json_format(monkeypatch, invalid_json):
    """ Проверка случая некорректного формата JSON. """
    monkeypatch.setattr("builtins.open", mock_open(read_data=invalid_json))
    result = reading_json("/some/path")
    assert result == []