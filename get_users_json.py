import json
import re
from calendar import monthrange
import requests


def get_user_calendar_json(username=None, user_id=None) -> dict:
    if user_id:
        with open(f'users/user_{user_id}.json', 'r', encoding='utf-8') as users:
            data = json.load(users)['calendar']
    return data


def update_calendar_user_json(change_list: dict) -> bool:
    # data = [type_day, week_day, day, hours
    try:
        user_id = int(change_list['user_id'])
        data = change_list['data']

        with open(f'users/user_{user_id}.json', 'r', encoding='utf-8') as users:
            old = json.load(users)

        for item in data:
            year = str(item['year'])
            mouth = str(item['mouth'])
            number_day = int(item['number_day'])

            old['calendar'][year][mouth][number_day - 1][3] = item['hour']
            old['calendar'][year][mouth][number_day - 1][0] = item['type_day']

            with open(f'users/user_{user_id}.json', 'w', encoding='utf-8') as users:
                json.dump(old, users)

            return True
    except Exception as err:
        return False


def parser_request_headers_user(string: str):
    cookies = {'showStatsColumns': 'Y'}
    headers = {'bx-cache-mode': 'HTMLCACHE'}
    params = {
        'apply_filter': 'Y',
        'REPORT_PERIOD_datesel': 'RANGE',
        'REPORT_PERIOD_from': '01.02.2024',
        'REPORT_PERIOD_to': '29.02.2024',
    }

    templates = ("BITRIX_CALL_HASH", r"BITRIX_SM_LOGIN", "BITRIX_SM_UIDL", "BITRIX_SM_UIDD", "BX_USER_ID", "PHPSESSID", "BITRIX_SM_UIDH")
    for t in templates:
        res = re.findall(fr"({t}=.*?);", string)[0].split('=')
        cookies[res[0]] = res[1]

    return cookies, headers, params


def get_time_user_from_bitrix(cookies, headers, params, rng: tuple):
    params['REPORT_PERIOD_from'], params['REPORT_PERIOD_to'] = rng
    print(cookies, headers, params, sep='\n')

    response = requests.get('https://alfalservice.bitrix24.ru/timeman/timeman.php',
                            params=params, cookies=cookies, headers=headers)

    res = re.findall(r'imeman-grid-stat">(.*?)</span></span>', response.text)[1]
    t = [''.join(d for d in i if d.isdigit()) for i in res.split()]

    return {'hours': t[0], 'minutes': t[1]}


def get_users_time_bitrix(user_id, mouth, year):
    start = f'01.{mouth:02}.{year}'
    end = f'{monthrange(year, mouth)[1]}.{mouth:02}.{year}'
    with open(f'users/user_{user_id}.json', 'r', encoding='utf-8') as users:
        data: dict = json.load(users)['data_bitrix']

    return get_time_user_from_bitrix(**data, rng=(start, end))


if __name__ == '__main__':
    res = get_users_time_bitrix(user_id=1, mouth=1, year=2024)
    print(res)


