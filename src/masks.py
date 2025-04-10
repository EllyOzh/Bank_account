from typing import Union

from src.log_config import masks_logger


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """Функция get_mask_card_number принимает на вход номер карты и возвращает ее маску"""

    masks_logger.info(f"Попытка маскирования номера карты: {card_number}")

    number_str = str(card_number)
    if number_str.isdigit() and len(number_str) == 16:
        masked_number = f"{number_str[0:4]} {number_str[4:6]}** **** {number_str[-4:]}"
        masks_logger.info(f"Маскированный номер карты: {masked_number}")
        return masked_number
    else:
        masks_logger.warning(f"Неверный формат номера карты: {card_number}")
        return ""


def get_mask_account(account_number: Union[int, str]) -> str:
    """Функция get_mask_account принимает на вход номер счета и возвращает его маску"""

    masks_logger.info(f"Попытка маскирования номера счета: {account_number}")

    account_str = str(account_number)
    if account_str.isdigit() and len(account_str) == 20:
        masked_account = f"**{account_str[-4:]}"
        masks_logger.info(f"Маскированный номер счета: {masked_account}")
        return masked_account

    else:
        masks_logger.warning(f"Неверный формат номера счета: {account_number}")
        return ""


if __name__ == "__main__":
    print(get_mask_card_number("9632587412365478"))
    print(get_mask_account("85479632145879632147"))
