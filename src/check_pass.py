import random
import string
import math
import sys


def check_pass(password):
    total, count, summ = 0, 0, 0
    dictionary = {'digit': False, 'lower': False,
                  'upper': False, 'special': False,
                  'length': len(password), 'duplicates': [False, False]}
    if any(c.isdigit() for c in password):
        total += 10
        dictionary['digit'] = True
    if any(c in string.ascii_lowercase for c in password):
        total += 26
        dictionary['lower'] = True
    if any(c in string.ascii_uppercase for c in password):
        total += 26
        dictionary['upper'] = True
    if any(c in string.punctuation for c in password):
        total += 33
        dictionary['special'] = True

# Функция считает количество подряд идущих цифр
    for c in password:
        if c in ('1234567890'):
            count += 1
            if count > 4:
                dictionary['duplicates'][0] = True
        else:
            count = 0

#  Функция считает количество подряд идущих символов
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            summ += 1
            if summ > 2:
                dictionary['duplicates'][1] = True
        else:
            summ = 0

    entropy = round(math.log2(total**len(password)))  # Энтропия
    if sys.float_info.max > total**len(password):
        # Время подбора в секундах
        time_seconds = (round(total**len(password) / 3900000000))
    metric_unique = len(set(password)) / len(password)
    return entropy, time_seconds, metric_unique, dictionary


# Function that delete the most popular symbol in the string
def delete_most_popular(string, check_string):
    most_popular = max(string, key=string.count)
    string = string.replace(most_popular, '')
    string += random.choice(check_string)
    return string
