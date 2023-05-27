from library import *
from checking_pass import check_table_words


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
    word_length = random.randint(3, 5)  # длина слова будет от 3 до 6 символов
    word = ''
    choice = random.randint(0, 1)
    for j in range(2):
        for i in range(word_length):
            if i % 2 == 0:
                if i == 0:
                    if choice == 1:
                        word += random.choice(consonants.upper())
                    else:
                        word += random.choice(vowels.upper())
                else:
                    if choice == 1:
                        word += random.choice(consonants)
                    else:
                        word += random.choice(vowels)
            else:
                if choice == 1:
                    word += random.choice(vowels)
                else:
                    word += random.choice(consonants)
        if j < 1:
            word += '_'
    word += random.choice(string.digits) + random.choice('!@#$%*')
    if check_table_words(word) != '':
        beautiful_password_first
    else:
        return word


def beautiful_password_second():
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    word_length = random.randint(4, 5)  # длина слова будет от 3 до 6 символов
    word = ''
    choice = random.randint(0, 1)
    for _ in range(2):
        for i in range(word_length):
            if i % 2 == 0:
                if i == 0:
                    if choice == 1:
                        word += random.choice(consonants.upper())
                    else:
                        word += random.choice(vowels.upper())
                else:
                    if choice == 1:
                        word += random.choice(consonants)
                    else:
                        word += random.choice(vowels)
            else:
                if choice == 1:
                    word += random.choice(vowels)
                else:
                    word += random.choice(consonants)
    word += random.choice(string.digits) + random.choice('!@#$%*')
    return word


def social_password(social_name):
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    word_length = random.randint(3, 5)  # длина слова будет от 3 до 6 символов
    word = ''
    choice = random.randint(0, 1)
    for j in range(2):
        for i in range(word_length):
            if i % 2 == 0:
                if i == 0:
                    if choice == 1:
                        word += random.choice(consonants.upper())
                    else:
                        word += random.choice(vowels.upper())
                else:
                    if choice == 1:
                        word += random.choice(consonants)
                    else:
                        word += random.choice(vowels)
            else:
                if choice == 1:
                    word += random.choice(vowels)
                else:
                    word += random.choice(consonants)
        if j < 1:
            word += '_' + social_name + '_'
    word += random.choice(string.digits) + random.choice('!@#$%*')
    return word


def beautiful_password_first():
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    word_length = random.randint(3, 5)  # длина слова будет от 3 до 6 символов
    word = ''
    choice = random.randint(0, 1)
    for j in range(2):
        for i in range(word_length):
            if i % 2 == 0:
                if i == 0:
                    if choice == 1:
                        word += random.choice(consonants.upper())
                    else:
                        word += random.choice(vowels.upper())
                else:
                    if choice == 1:
                        word += random.choice(consonants)
                    else:
                        word += random.choice(vowels)
            else:
                if choice == 1:
                    word += random.choice(vowels)
                else:
                    word += random.choice(consonants)
        if j < 1:
            word += '_'
    word += random.choice(string.digits) + random.choice('!@#$%*')
    if check_table_words(word) != '':
        beautiful_password_first
    else:
        return word


def beautiful_password_second():
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    word_length = random.randint(4, 5)  # длина слова будет от 3 до 6 символов
    word = ''
    choice = random.randint(0, 1)
    for _ in range(2):
        for i in range(word_length):
            if i % 2 == 0:
                if i == 0:
                    if choice == 1:
                        word += random.choice(consonants.upper())
                    else:
                        word += random.choice(vowels.upper())
                else:
                    if choice == 1:
                        word += random.choice(consonants)
                    else:
                        word += random.choice(vowels)
            else:
                if choice == 1:
                    word += random.choice(vowels)
                else:
                    word += random.choice(consonants)
    word += random.choice(string.digits) + random.choice('!@#$%*')
    return word


def social_password(social_name):
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    word_length = random.randint(3, 5)  # длина слова будет от 3 до 6 символов
    word = ''
    choice = random.randint(0, 1)
    for j in range(2):
        for i in range(word_length):
            if i % 2 == 0:
                if i == 0:
                    if choice == 1:
                        word += random.choice(consonants.upper())
                    else:
                        word += random.choice(vowels.upper())
                else:
                    if choice == 1:
                        word += random.choice(consonants)
                    else:
                        word += random.choice(vowels)
            else:
                if choice == 1:
                    word += random.choice(vowels)
                else:
                    word += random.choice(consonants)
        if j < 1:
            word += '_' + social_name + '_'
    word += random.choice(string.digits) + random.choice('!@#$%*')
    return word


def pass_corrector(call_pass):
    password = ''
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    list_vowels = []
    list_consonants = []
    list_digits = []
    list_punctuation = []

    for char in call_pass:
        if char in (vowels.upper() + vowels.lower()):
            list_vowels.append(char)
        elif char in (consonants.upper() + consonants.lower()):
            list_consonants.append(char)
        elif char in string.digits:
            list_digits.append(char)
        elif char in string.punctuation:
            list_punctuation.append(char)

    list_vowels = list(map(str, set(list_vowels)))
    list_consonants = list(map(str, set(list_consonants)))
    list_digits = list(map(str, set(list_digits)))
    list_punctuation = list(map(str, set(list_punctuation)))
    random_choice_variant = random.randint(1, 2)
    if random_choice_variant == 1:
        random_pass_length = random.randint(3, 5)
    else:
        random_pass_length = random.randint(4, 5)

    for j in range(2):
        for i in range(random_pass_length):
            if i % 2 == 0:
                if i == 0:
                    if len(list_consonants) != 0:
                        password += random.choice(str(list_consonants.pop()).upper())
                    else:
                        password += random.choice(consonants.upper())
                else:
                    if len(list_consonants) != 0:
                        password += random.choice(str(list_consonants.pop()).lower())
                    else:
                        password += random.choice(consonants.lower())
            else:
                if len(list_vowels) != 0:
                    password += random.choice(str(list_vowels.pop()).lower())
                else:
                    password += random.choice(vowels.lower())
        if random_choice_variant == 1:
            if j < 1:
                password += '_'

    if len(list_digits) != 0:
        password += random.choice(list_digits.pop())
    else:
        password += random.choice(string.digits)

    if len(list_punctuation) != 0:
        password += random.choice(list_punctuation.pop())
    else:
        password += random.choice('!@#$%*')
    return password
