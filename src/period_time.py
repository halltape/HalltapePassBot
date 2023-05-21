# Function for converting the time

def period_result(period):
    dict_period = {'seconds': 'секунд',
                   'minutes': 'минут',
                   'hours': 'час',
                   'days': 'д',
                   'years': '',
                   'century': 'век'}

    dict_ends = {'seconds': ['', 'а', 'ы'],
                 'minutes': ['', 'а', 'ы'],
                 'hours': ['ов', '', 'а'],
                 'days': ['ней', 'ень', 'ня'],
                 'years': ['лет', 'год', 'года'],
                 'century': ['ов', '', 'а']}

    if period // 3600 // 24 // 365 // 100 > 60000000:
        result = True
        return result
    if period < 60:
        word = dict_period['seconds']
    elif 60 <= period < 3600:
        word = dict_period['minutes']
        period = period // 60  # Количество часов
    elif 3600 <= period < (24 * 3600):
        word = dict_period['hours']
        period = period // 3600  # Количество часов
    elif 24 * 3600 <= period < (24 * 3600) * 365:
        word = dict_period['days']
        period = period // 3600 // 24  # количество дней
    elif ((24 * 3600) * 365) <= period < ((24 * 3600) * 365 * 100):
        word = dict_period['years']
        period = period // 3600 // 24 // 365  # Количество лет
    elif period >= ((24 * 3600) * 365 * 100):
        word = dict_period['century']
        period = period // 3600 // 24 // 365 // 100  # Количество веков
    # 15
    if int(period) % 10 in (0, 5, 6, 7, 8, 9) or int(period) in range(11, 20):
        if word == dict_period['seconds']:
            word += dict_ends['seconds'][0]

        if word == dict_period['minutes']:
            word += dict_ends['minutes'][0]

        if word == dict_period['hours']:
            word += dict_ends['hours'][0]

        if word == dict_period['days']:
            word += dict_ends['days'][0]

        if word == dict_period['years']:
            word += dict_ends['years'][0]

        if word == dict_period['century']:
            word += dict_ends['century'][0]

    elif int(period) % 10 == 1 and int(period) not in range(11, 20):  # 1
        if word == dict_period['seconds']:
            word += dict_ends['seconds'][1]

        if word == dict_period['minutes']:
            word += dict_ends['minutes'][1]

        if word == dict_period['hours']:
            word += dict_ends['hours'][1]

        if word == dict_period['days']:
            word += dict_ends['days'][1]

        if word == dict_period['years']:
            word += dict_ends['years'][1]

        if word == dict_period['century']:
            word += dict_ends['century'][1]

    elif int(period) % 10 in (2, 3, 4):  # 4
        if word == dict_period['seconds']:
            word += dict_ends['seconds'][2]

        if word == dict_period['minutes']:
            word += dict_ends['minutes'][2]

        if word == dict_period['hours']:
            word += dict_ends['hours'][2]

        if word == dict_period['days']:
            word += dict_ends['days'][2]

        if word == dict_period['years']:
            word += dict_ends['years'][2]

        if word == dict_period['century']:
            word += dict_ends['century'][2]
    result = str(f'{period:,}') + ' ' + word
    return result
