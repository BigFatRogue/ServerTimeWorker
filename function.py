import json


def __get_data_json(filename: str) -> dict:
    try:
        json_file = open(f'server/{filename}.json', 'r', encoding='utf-8')
    except FileNotFoundError:
        json_file = open(f'{filename}.json', 'r', encoding='utf-8')
    dct: dict = json.load(json_file)
    json_file.close()
    return dct


def __update_json(filename: str, data: dict):
    try:
        json_file = open(f'server/{filename}.json', 'w', encoding='utf-8')
    except FileNotFoundError:
        json_file = open(f'{filename}.json', 'w', encoding='utf-8')
    json.dump(data, json_file)
    json_file.close()