from typing import Union


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """Функция get_mask_card_number принимает на вход номер карты и возвращает ее маску"""

    number_str = str(card_number)
    if number_str.isdigit() and len(number_str) == 16:
        return f"{number_str[0:4]} {number_str[4:6]}** **** {number_str[-4:]}"
    else:
        return ""


def get_mask_account(account_number: Union[int, str]) -> str:
    """Функция get_mask_account принимает на вход номер счета и возвращает его маску"""
    account_str = str(account_number)
    if account_str.isdigit() and len(account_str) == 20:
        return f"**{account_str[-4:]}"

    else:
        return ""


if __name__ == "__main__":
    print(get_mask_card_number("9632587412365478"))
    print(get_mask_account("85479632145879632147"))
