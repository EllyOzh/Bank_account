from black import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(number_card_or_account: str) -> str:
    """Функция, возвращающая замаскированный номер карты или счёта"""
    info_card_or_account = number_card_or_account.split()
    # Длина последнего элемента = Количество цифр в номере счета
    if len(info_card_or_account[-1]) == 20:
        info_card_or_account[-1] = get_mask_account(info_card_or_account[-1])
        return " ".join(info_card_or_account)
    else:
        info_card_or_account[-1] = get_mask_card_number(info_card_or_account[-1])
        return " ".join(info_card_or_account)


def get_date(info_date: str) -> str:
    """Функция,  возвращающая строку с датой в формате 'ДД.ММ.ГГГГ'"""

    date_form = datetime.strptime(info_date, "%Y-%m-%dT%H:%M:%S.%f")
    return date_form.strftime("%d.%m.%Y")


if __name__ == "__main__":
    print(mask_account_card(str("Visa Platinum 2202345612340099")))
    print(get_date("2024-03-11T02:26:18.671407"))
