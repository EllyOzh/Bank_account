from typing import List, Dict
from typing import Union


def filter_by_state(
        info_client: List[Dict[str, Union[str, int]]],
        state: str = 'EXECUTED') -> List[Dict[str, Union[str, int]]]:
    """Функция возвращает новый список словарей, содержащий только те словари, у которых ключ
state соответствует указанному значению."""

    new_list_dict = []
    for i in info_client:
        for key, value in i.items():
            if i['state'] == 'EXECUTED':
                new_list_dict.append(i)
    return new_list_dict


def sort_by_date(
                info_client: List[Dict[str, Union[str, int]]],
                ascending: bool = 'True') -> List[Dict[str, Union[str, int]]]:
    """Функция возвращает новый список, отсортированный по дате."""
    sorted_date_ascending = []
    sorted_date_descending = []
    for i in info_client:
        if ascending is False:
            sorted_date_descending = sorted(info_client, key=lambda i: i['date'], reverse=True)
            return sorted_date_descending
        else:
            sorted_date_ascending = sorted(info_client, key=lambda i: i['date'])
            return sorted_date_ascending


if __name__ == "__main__":
    print(filter_by_state(
                         [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                          {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                          {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                          {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]))

    print(sort_by_date(
                      [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                       {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                       {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                       {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]))
