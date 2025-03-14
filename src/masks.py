from typing import Union

def get_mask_card_number(card_number: Union[int, str]) -> Union[int, str]:
    """Функция get_mask_card_number принимает на вход номер карты и возвращает ее маску"""

    if card_number.isdigit():
        for num in card_number:
            if len(card_number) == 16:
                return f"(card_number[0:4] card_number[4:6]** **** card_number[-4:])"
            elif len(card_number) == 13:
                return f"(card_number[0:4] card_number[4:5]**** card_number[-4:])"
            elif len(card_number) == 19:
                return f"(card_number[0:4] card_number[4:6]** **** *** card_number[-4:])"
    else:
        return ""


def get_mask_account(account_number: Union[int, str]) -> Union[int, str]:
    """Функция get_mask_account принимает на вход номер счета и возвращает его маску"""

    if account_number.isdigit():
        for element in account_number:
            if len(account_number) == 20:
                return f"(**account_number[-4:])"

    else:
        return ""



if __name__ == "__main__":
    print(get_mask_card_number("9632587412365478"))
    print(get_mask_account("85479632145879632147"))
