import os
import sys
import math
import string
import random


def check_table_words(password):
    file_path = os.getcwd() + '/text_files/leaked_passwords_1M.txt'
    word = ''
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.lower() in password.lower() and len(line) > 4:
                word += line + '\n'
    return word


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

# The function counts the number of consecutive digits
    for c in password:
        if c in ('1234567890'):
            count += 1
            if count > 4:
                dictionary['duplicates'][0] = True
        else:
            count = 0

#  The function counts the number of consecutive characters
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            summ += 1
            if summ > 2:
                dictionary['duplicates'][1] = True
        else:
            summ = 0

    entropy = round(math.log2(total**len(password)))  # Entropy
    if sys.float_info.max > total**len(password):
        # Time of brute force in seconds
        time_seconds = (round(total**len(password) / 3900000000))
    metric_unique = len(set(password)) / len(password)
    return entropy, time_seconds, metric_unique, dictionary


# Function that removes the most frequently occurring character
def delete_most_popular(string, check_string):
    most_popular = max(string, key=string.count)
    string = string.replace(most_popular, '')
    string += random.choice(check_string)
    return string
