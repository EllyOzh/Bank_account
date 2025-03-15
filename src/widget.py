from black import datetime

from src.masks import get_mask_account, get_mask_card_number

def mask_account_card(number_card_or_account: str) -> str:
    """Функция, возвращающая замаскированный номер карты или счёта"""
    info_card_or_account = number_card_or_account.split()
    number = info_card_or_account[-1]
    title = " ".join(info_card_or_account[:-1])
    # Длина последнего элемента = Количество цифр в номере счета
    if len(number) == 20:
        hidden_number = get_mask_account(number)
    else:
        hidden_number = get_mask_card_number(number)
    return f"{title} {hidden_number}"


def get_date(info_date: str) -> str:
    """Функция,  возвращающая строку с датой в формате 'ДД.ММ.ГГГГ'"""
    try:
        date_form = datetime.strptime(info_date, "%Y-%m-%dT%H:%M:%S.%f")
        return date_form.strftime("%d.%m.%Y")
    except ValueError:
        return 'Введите дату в правильном формате'


if __name__ == "__main__":
    print(mask_account_card(str("Счет 73654108430135874305")))
    print(get_date("2024-03-11T02:26:18.671407"))
    print(get_date("2024-03"))

