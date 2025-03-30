# import os
import shutil

import pytest

from src.decorators import log


# Фиктивные функции для тестирования
@log(filename="success.log")
def successful_function():
    return "Success!"


@log()
def function_with_exception():
    raise ValueError("Test exception")


@log()
def normal_function():
    return "Normal output"


# Фикстура для очистки файлов логов перед каждым тестом
@pytest.fixture(scope="function")
def clean_logs(tmpdir):
    yield tmpdir
    # Удаление временных файлов после теста
    shutil.rmtree(str(tmpdir), ignore_errors=True)


# # Тест успешного выполнения функции
# def test_successful_function(clean_logs, capsys):
#     result = successful_function()
#     captured = capsys.readouterr()
#
#     # Проверка результата функции
#     assert result == "Success!"
#
#     # Проверка содержимого файла логов
#     log_file_path = os.path.join(str(clean_logs), "success.log")
#     with open(log_file_path, "r") as f:
#         logs = f.read().strip()
#         assert "successful_function запущена" in logs
#         assert "успешно выполнена. Результат: Success!" in logs


# Тест функции с исключением
def test_function_with_exception(clean_logs, capsys):
    with pytest.raises(ValueError):
        function_with_exception()

    captured = capsys.readouterr()
    assert 'Ошибка в функции "function_with_exception". Тип ошибки: ValueError.' in captured.out.strip()


# Тест нормальной функции с выводом в консоль
def test_normal_function(clean_logs, capsys):
    result = normal_function()
    captured = capsys.readouterr()

    # Проверка результата функции
    assert result == "Normal output"

    # Проверка вывода в консоль
    assert 'Функция "normal_function" запущена' in captured.out
    assert 'Функция "normal_function" выполнена успешно. Результат: Normal output' in captured.out


# Запуск тестов
if __name__ == "__main__":
    pytest.main(["-v"])
