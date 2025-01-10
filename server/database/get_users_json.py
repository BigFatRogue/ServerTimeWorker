import json
import re
from calendar import monthrange
import requests
from server.my_sitting import PROJECT_ROOT


def get_user_calendar_json(user_id=None) -> dict:
    if user_id:
        with open(f'{PROJECT_ROOT}/database/users/user_{user_id}.json', 'r', encoding='utf-8') as users:
            data = json.load(users)['calendar']
    return data


def check_user_bitrix_data(user_id) -> bool:
    with open(f'{PROJECT_ROOT}/database/users/user_{user_id}.json', 'r', encoding='utf-8') as users:
        return json.load(users).get('data_bitrix') is not None


def update_calendar_user_json(change_list: dict) -> bool:
    try:
        user_id = int(change_list['user_id'])
        data = change_list['data']

        with open(f'{PROJECT_ROOT}/database/users/user_{user_id}.json', 'r', encoding='utf-8') as users:
            old = json.load(users)

        for item in data:
            year = str(item['year'])
            mouth = str(item['mouth'])
            number_day = int(item['number_day'])

            old['calendar'][year][mouth][number_day - 1][3] = item['hour']
            old['calendar'][year][mouth][number_day - 1][0] = item['type_day']

            with open(f'{PROJECT_ROOT}/database/users/user_{user_id}.json', 'w', encoding='utf-8') as users:
                json.dump(old, users)

        return True
    except Exception as err:
        return False


def write_data_bitrix_user(user_id, string: str) -> bool:
    cookies = {'showStatsColumns': 'Y'}
    headers = {'bx-cache-mode': 'HTMLCACHE'}
    params = {
        'apply_filter': 'Y',
        'REPORT_PERIOD_datesel': 'RANGE',
        'REPORT_PERIOD_from': '01.02.2024',
        'REPORT_PERIOD_to': '29.02.2024',
    }

    try:
        templates = ("BITRIX_SM_UIDL", "BITRIX_SM_UIDD", "BX_USER_ID", "PHPSESSID", "BITRIX_SM_UIDH")
        for t in templates:
            response = re.findall(fr"({t}=.*?)[;|']", string)[0].split('=')
            cookies[response[0]] = response[1]
    except Exception:
        return False

    with open(f'{PROJECT_ROOT}/database/users/user_{user_id}.json', 'r', encoding='utf-8') as users:
        data: dict = json.load(users)

    with open(f'{PROJECT_ROOT}/database/users/user_{user_id}.json', 'w', encoding='utf-8') as users:
        data['data_bitrix'] = {"cookies": cookies, "headers": headers, "params": params}
        json.dump(data, users)
    return True


def get_users_time_bitrix(user_id, mouth, year):
    with open(f'{PROJECT_ROOT}/database/users/user_{user_id}.json', 'r', encoding='utf-8') as users:
        data: dict = json.load(users)['data_bitrix']
    cookies, headers, params = data['cookies'], data['headers'], data['params']

    start = f'01.{mouth:02}.{year}'
    end = f'{monthrange(year, mouth)[1]}.{mouth:02}.{year}'
    params['REPORT_PERIOD_from'], params['REPORT_PERIOD_to'] = start, end

    response = requests.get('https://alfalservice.bitrix24.ru/timeman/timeman.php',
                            params=params, cookies=cookies, headers=headers)

    res = re.findall(r'imeman-grid-stat">(.*?)</span></span>', response.text)[1]
    t = [''.join(d for d in i if d.isdigit()) for i in res.split()]

    return {'hours': t[0], 'minutes': t[1]}