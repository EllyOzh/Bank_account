from src.decorators import log


@log(filename="example.log")
def sum_numbers(a: int, b: int) -> int:
    return a + b


@log()
def divide_numbers(a: int, b: int) -> float:
    return a / b


sum_numbers(10, 20)
divide_numbers(100, 0)
