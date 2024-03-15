import json
from function import __get_data_json, __update_json


def get_user_calendar_json(username=None, user_id=None) -> dict:
    if user_id:
        with open(f'users/user_{user_id}.json', 'r', encoding='utf-8') as users:
            data = json.load(users)
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

            old[year][mouth][number_day - 1][3] = item['hour']
            old[year][mouth][number_day - 1][0] = item['type_day']

            with open(f'users/user_{user_id}.json', 'w', encoding='utf-8') as users:
                json.dump(old, users)

            return True
    except Exception as err:
        return False


if __name__ == '__main__':
    res = get_user_calendar_json(user_id=1)
    print(res)


