from typing import Dict, List, Union

from datetime import datetime


def filter_by_state(
    info_client: List[Dict[str, Union[str, int]]], state: str = "EXECUTED"
) -> List[Dict[str, Union[str, int]]]:
    """Функция возвращает новый список словарей, содержащий только те словари, у которых ключ
    state соответствует указанному значению."""

    new_list_dict = []
    for element in info_client:
        if element["state"] == state:
            new_list_dict.append(element)
    return new_list_dict


def sort_by_date(
    info_client: List[Dict[str, Union[str, int]]], reverse: bool = True
) -> List[Dict[str, Union[str, int]]]:
    """Возвращает список, отсортированный по дате"""
    return sorted(info_client, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=reverse)


if __name__ == "__main__":
    print(
        filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )

    print(
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )
