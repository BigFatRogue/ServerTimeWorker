"""
Генерация рабочего календаря по заданным годам, где Сб и Вс выходные
Пн - Чт - рабочий день 8.5 часов
Пт - рабочий день 8 часов

Данный календарь не учитывает праздничные выходные
"""

from datetime import datetime
import json


if __name__ == '__main__':
    'type_day, week_day, number_day, hour'

    lst_week_day = [*range(7)]
    lst_name_mouth = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    dct = {}
    for year in range(2023, 2031):
        dct[year] = {}
        for mouth in range(12):
            dct[year][mouth] = []
            for day in range(1, 32):
                try:
                    date = datetime(year, mouth + 1, day)
                    week_day = date.weekday()

                    type_day = 0 if week_day in (5, 6) else 1
                    hour = 8.5 * 60
                    if week_day == 4:
                        hour = 8 * 60
                    elif week_day in (5, 6):
                        hour = 0

                    dct[year][mouth].append([type_day, week_day, day, hour])
                except ValueError:
                    continue

    with open('standart_calendar_json_2024.json', 'w', encoding='utf') as file:
        json.dump(dct, file)
