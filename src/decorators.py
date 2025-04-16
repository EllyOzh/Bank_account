import os
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable], Callable]:
    """
    Декоратор для логирования начала и конца выполнения функции.
    Параметр filename: Имя файла для записи логов. Если не указано, логи выводятся в консоль.
    Возвращает: Обертка над функцией.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_message = f'Функция "{func.__name__}" запущена'

            if filename:
                os.makedirs("logs", exist_ok=True)
                filepath = os.path.join("logs", f"{filename}.txt")
                with open(filepath, "a", encoding="utf-8") as file:
                    file.write(start_message + "\n")
            else:
                print(start_message)

            try:
                result = func(*args, **kwargs)
                end_message = f'Функция "{func.__name__}" выполнена успешно. Результат: {result}'

                if filename:
                    with open(filepath, "a", encoding="utf-8") as file:
                        file.write(end_message + "\n")
                else:
                    print(end_message)

                return result
            except Exception as e:
                error_message = (
                    f'Ошибка в функции "{func.__name__}". Тип ошибки: {type(e).__name__}. '
                    f'Входные аргументы: args={args}, kwargs={kwargs}'
                )

                if filename:
                    with open(filepath, "a", encoding="utf-8") as file:
                        file.write(error_message + "\n")
                else:
                    print(error_message)

                raise e

        return wrapper

    return decorator
