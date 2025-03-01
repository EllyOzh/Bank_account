from typing import Union


def get_mask_card_number(card_number: Union[int, str]) -> Union[int, str]:
    """Функция get_mask_card_number принимает на вход номер карты и возвращает ее маску"""

    return f"({card_number[0:4]} {card_number[4:6]}** **** {card_number[-4:]})"


def get_mask_account(account_number: Union[int, str]) -> Union[int, str]:
    """Функция get_mask_account принимает на вход номер счета и возвращает его маску"""

    return f"(**{account_number[-4:]})"


if __name__ == "__main__":
    print(get_mask_card_number("9632587412365478"))
    print(get_mask_account("85479632145879632147"))
