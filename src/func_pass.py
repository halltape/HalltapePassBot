from library import *


def generate_password(dict) -> str:
    # По полученному словарю генерируем sample
    # пароля из максимум 4 элементов и пишем в строку
    sample_password = ''
    if dict['digit'] is True:
        sample_password += random.choice(string.digits)
    if dict['lower'] is True:
        sample_password += random.choice(string.ascii_lowercase)
    if dict['upper'] is True:
        sample_password += random.choice(string.ascii_uppercase)
    if dict['special'] is True:
        sample_password += random.choice(string.punctuation)
    if dict['replace'] is True:
        sample_password = sample_password.replace('i', 'F').replace('l', 'g') \
            .replace('1', 'p').replace('L', '7').replace('o', 't') \
            .replace('0', '2').replace('O', 'z')
    return sample_password


def final_pass(answ_dict, length) -> str:
    # Собираем финальный пароль из сэмплов (каждый из 4 элементов)
    build_password = ''  # Создаем пустую строку для будущего сэмпла
    if length == 95:
        build_password = string.digits + string.ascii_lowercase + \
            string.ascii_uppercase + string.punctuation
        # Обрезаем пароль до нужной длины
        final_password = list(build_password[:95])
        random.shuffle(final_password)  # Перемешиваем пароль
        final_password = ''.join(final_password)  # Склеиваем обратно в строку
    else:
        # Собираем пароль, пока длина не превысит нужную
        while len(build_password) <= length:
            # Если длина будет n, то сэмпл соберается длиной n + 1
            for _ in range(math.ceil(length / 4)):
                # Конкатенация строк сэмплов пароля
                build_password += generate_password(answ_dict)
        # Обрезаем пароль до нужной длины
        final_password = list(build_password[:length])
        random.shuffle(final_password)  # Перемешиваем пароль
        final_password = ''.join(final_password)  # Склеиваем обратно в строку
    return final_password


def strong_pass(button):
    if button is False:
        pass_length = 18
        answer_dict = {'digit': True, 'lower': True, 'upper': True,
                       'special': False, 'replace': True}
    password = final_pass(answer_dict, pass_length)
    digits, letters = check_corrected_pass(password)
    while digits is not False and letters is not False:
        password = final_pass(answer_dict, pass_length)
    return password


def check_corrected_pass(correct_pass) -> tuple[bool, bool]:
    count, summ, duplicates_digits, duplicates_letters = 0, 0, False, False
    # Функция считает количество подряд идущих цифр
    for c in correct_pass:
        if c in ('1234567890'):
            count += 1
            if count > 4:
                duplicates_digits = True
        else:
            count = 0

#  Функция считает количество подряд идущих символов
    for i in range(1, len(correct_pass)):
        if correct_pass[i] == correct_pass[i - 1]:
            summ += 1
            if summ > 2:
                duplicates_letters = True
        else:
            summ = 0
    return duplicates_digits, duplicates_letters


def beautiful_password_first():
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    word_length = random.randint(3, 6)  # длина слова будет от 3 до 6 символов
    word = ''
    for j in range(2):
        for i in range(word_length):
            if i % 2 == 0:
                if i == 0:
                    word += random.choice(consonants.upper())
                else:
                    word += random.choice(consonants)
            else:
                if i == 0:
                    word += random.choice(vowels.upper())
                else:
                    word += random.choice(vowels)
        if j < 1:
            word += '_'
    word += random.choice(string.digits) + random.choice('!@#$%*')
    return word


def beautiful_password_second():
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    word_length = random.randint(3, 6)  # длина слова будет от 3 до 6 символов
    word = ''
    for j in range(2):
        for i in range(word_length):
            if i % 2 == 0:
                if i == 0:
                    word += random.choice(consonants.upper())
                else:
                    word += random.choice(consonants)
            else:
                if i == 0:
                    word += random.choice(vowels.upper())
                else:
                    word += random.choice(vowels)
    word += random.choice(string.digits) + random.choice('!@#$%*')
    return word


def social_password(social_name):
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    word_length = random.randint(3, 6)  # длина слова будет от 3 до 6 символов
    word = ''
    for j in range(2):
        for i in range(word_length):
            if i % 2 == 0:
                if i == 0:
                    word += random.choice(consonants.upper())
                else:
                    word += random.choice(consonants)
            else:
                if i == 0:
                    word += random.choice(vowels.upper())
                else:
                    word += random.choice(vowels)
        if j < 1:
            word += '_' + social_name + '_'
    word += random.choice(string.digits) + random.choice('!@#$%*')
    return word
