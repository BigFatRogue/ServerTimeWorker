import json
from function import __get_data_json, __update_json


def __create_calendar_new_user(user_id: int):
    standart_calendar: dict = __get_data_json('standart_calendar_json')
    users_calendar: dict = __get_data_json('users_calendar')

    users_calendar[user_id] = standart_calendar
    __update_json('users_calendar', users_calendar)


def check_authentication(user: str, password: str) -> tuple:
    dct: dict = __get_data_json('users')

    if dct.get(user):
        if dct[user]['password'] == password:
            return True, 'Success', dct[user]['id']
        else:
            return False, 'Неверный пароль', None
    else:
        return False, 'Такого пользователя нет !', None


def registration_user(user: str, password) -> tuple:
    dct: dict = __get_data_json('users')

    if dct.get(user) is None:
        count = len(dct)
        dct[user] = {"name": f"user_{count}", "id": count, "password": password}
        __update_json('users', dct)
        __create_calendar_new_user(user_id=count)

        return True, 'Success'
    return False, 'Такой пользователь уже есть'