import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
import random
import math
import sys
import string
from functools import reduce


# Создаем экземпляр бота
bot = telebot.TeleBot('TOKEN')


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
# Добавляем две кнопки
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Получить надежный пароль')
    button2 = types.KeyboardButton('Тотальный контроль')
    markup.add(button1)
    markup.add(button2)
    bot.send_message(m.chat.id, '\n\n*🔐 Проверь свой пароль на надежность, '
                     'просто отправь его боту в виде сообщения*\n\n'
                     '💪🏻 Также бот может предложить усилить твой пароль\n\n'
                     '*Либо можешь сгенерировать уже готовый\!*\n\n'
                     '1️⃣ Получить надежный пароль \(*18 символов*\)\n'
                     'Можешь нажимать бесконечное кол\-во раз\n'
                     '\n2️⃣ Тотальный контроль \(*95 уникальных символов*\)\n',
                     reply_markup=markup, parse_mode='MarkdownV2')


# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id, 'По всем вопросам работы бота '
                     'писать *@halltape*\n', parse_mode='MarkdownV2')


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):

    flag = True
    check_string = string.ascii_lowercase + string.ascii_uppercase + \
        string.punctuation + string.digits

    if message.text.strip() == 'Тотальный контроль':
        answer = strong_pass(True)
        bot.send_message(message.chat.id, answer)
    elif message.text.strip() == 'Получить надежный пароль':
        answer = strong_pass(False)
        bot.send_message(message.chat.id, '*'f'{answer}*',
                         parse_mode='MarkdownV2')
    else:
        for char in message.text.strip():
            if char not in (check_string):
                flag = False
        if flag:
            get_pass(message)
        else:
            bot.send_message(message.chat.id,
                             '❌ *Недопустимые символы*\n'
                             'Проверьте вводимый текст\n\n'
                             '\- Есть пробелы\n'
                             '\- Перепутана русская *A* и латинская\n'
                             '\- Есть нестандартные символы\n\n'
                             '*P\.S\. Бот различает русский и латинский алфавит*',
                             parse_mode='MarkdownV2')


def get_pass(message: types.Message):   # Функция проверки пароля
    if len(message.text) <= 50:
        bit, time, unique, dict_answer = check_pass(message.text)
        verdict, time_final = '', ''
        # Функция, которая возвращает строку с числом и периодом времени
        period = period_result(time)
        if dict_answer['digit'] is False:
            verdict += '⚠️ Нет цифр\n'
        if dict_answer['lower'] is False:
            verdict += '⚠️ Нет букв в нижнем регистре\n'
        if dict_answer['upper'] is False:
            verdict += '⚠️ Нет букв в верхнем регистре\n'
        if dict_answer['special'] is False:
            verdict += '⚠️ Нет специальных символов\n'
        if dict_answer['length'] < 16:
            verdict += '⚠️ Длина пароля меньше 16 символов\n'
        if dict_answer['duplicates'][0] is True:
            verdict += '⚠️ Больше четырех чисел друг за другом\n'
        if dict_answer['duplicates'][1] is True:
            verdict += '⚠️ Повторяющиеся символы\n'
        if unique < 0.6:
            verdict += '⚠️ Малая уникальность пароля\n'

        if (time // 3600 // 24) < 183:
            if time < 1:  # Если время меньше 1 секунды, чтобы не писать мск
                time_final = '\n⏳ Пароль взломают моментально\n'
            else:
                time_final = '\n⏳ На его взлом уйдет 'f'{period}\n'

        bit_final = '\nСила пароля 'f'{bit} бит\nОптимальное значение' \
            'от 97 и больше'
        if verdict != '' and bit < 97:
            if dict_answer['length'] < 16 \
                    and (time // 3600 // 24 // 365) > 1 and unique > 0.5:
                verdict_final = 'ℹ Пароль надежный,' \
                    ' но обрати внимание на комментарии ниже'
                if period is True:
                    time_final = '\n⏳ Солнце уже потухнет, '\
                        'а твой пароль все еще будут подбирать\n'
                else:
                    time_final = '\n⏳ На его взлом уйдет 'f'{period}\n'
                verdict_final += '\n\n' + verdict + time_final + bit_final
            else:
                verdict_final = '❌ Тебе нужно усилить твой пароль!\n\n' \
                    + verdict + time_final + bit_final
        if bit > 96 and unique > 0.6 and dict_answer['duplicates'][0] is False\
                and dict_answer['duplicates'][1] is False:
            if period is True:
                time_final = '\n⏳ Солнце уже потухнет, '\
                    'а твой пароль все еще будут подбирать\n'
            else:
                time_final = '\nНа его взлом уйдет 'f'{time}\n'
            verdict_final = '✅ У тебя хороший пароль!\n' \
                + time_final + bit_final
        else:
            if bit > 96:
                bit_final = ''
                verdict_final = '❌ Тебе нужно усилить твой пароль!\n\n' \
                    + verdict + time_final + bit_final
    else:
        verdict_final = '♾ Пароль слишком длинный, в этом нет смысла'

    bot.send_message(message.chat.id, verdict_final)
    if verdict_final[0] == '❌':
        # инлайновая клавиатура
        inMurkup = types.InlineKeyboardMarkup(row_width=1)
        inline_button1 = types.InlineKeyboardButton('Максимальная ' \
                                                    'защита (Рекомендуется)', callback_data='1' + "|" + message.text)
        inline_button2 = types.InlineKeyboardButton('Немного усложнить',
                                                   callback_data='2' + "|" + message.text)
        inMurkup.add(inline_button1)
        inMurkup.add(inline_button2)
        bot.send_message(message.chat.id, 'Ты можешь усилить свой пароль',
                         reply_markup=inMurkup)

    if verdict_final[0] == 'ℹ':
        # инлайновая клавиатура
        inMurkup = types.InlineKeyboardMarkup(row_width=1)
        inline_button3 = types.InlineKeyboardButton('Немного усложнить',
                                                   callback_data='3' + "|" + message.text)
        inMurkup.add(inline_button3)
        bot.send_message(message.chat.id, 'Ты можешь усилить свой пароль',
                         reply_markup=inMurkup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    import string
    check_string = string.ascii_lowercase + string.ascii_uppercase + string.punctuation + string.digits
    call_back_pass = call.data[2:]
    if call.data[0] == '1':  # Максимальное усложнение
        # Из множества в строку
        s = ''.join(set(call_back_pass))
        corrected_pass = s + strong_pass(False)

        # shuffle corrected_pass
        corrected_pass = ''.join(random.sample(corrected_pass,
                                               len(corrected_pass)))
        digits, letters = check_corrected_pass(corrected_pass)
        unique = len(set(corrected_pass)) / len(corrected_pass)

        # Пока измененный пароль не будет содержать дубликатов и цифр
        while digits is not False and letters is not False:
            corrected_pass = s + strong_pass(False)
            corrected_pass = ''.join(random.sample(corrected_pass,
                                                   len(corrected_pass)))
            digits, letters = check_corrected_pass(corrected_pass)
            unique = len(set(corrected_pass)) / len(corrected_pass)

        bot.send_message(call.message.chat.id, f'{corrected_pass[:18]}')
    elif call.data[0] in ('2', '3'):
        bit, time, unique, dict_answer = check_pass(call_back_pass)
        while (len(call_back_pass) <= len(call.data[2:])):
            if dict_answer['duplicates'][1] is True:
                call_back_pass = delete_most_popular(call_back_pass, check_string)
            if dict_answer['digit'] is False:
                call_back_pass += random.choice(string.digits)
            if dict_answer['lower'] is False:
                call_back_pass += random.choice(string.ascii_lowercase)
            if dict_answer['upper'] is False:
                call_back_pass += random.choice(string.ascii_uppercase)
            if dict_answer['special'] is False:
                call_back_pass += random.choice('!#$%&()*+-:;=>?@_')
            if call_back_pass == call.data[2:]:
                dict = {'digit': True, 'lower': True, 'upper': True,
                        'special': True, 'replace': False}
                call_back_pass += generate_password(dict)
                break
        # shuffle corrected_pass
        call_back_pass = ''.join(random.sample(call_back_pass,
                                               len(call_back_pass)))
        bot.send_message(call.message.chat.id, call_back_pass)
    return 0


# Function that delete the most popular symbol in the string
def delete_most_popular(string, check_string):
    most_popular = max(string, key=string.count)
    string = string.replace(most_popular, '')
    string += random.choice(check_string)
    return string


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
    if button is True:
        pass_length = 95
        answer_dict = {'digit': True, 'lower': True, 'upper': True,
                       'special': True, 'replace': False}
    else:
        pass_length = 18
        answer_dict = {'digit': True, 'lower': True, 'upper': True,
                       'special': False, 'replace': True}
    password = final_pass(answer_dict, pass_length)
    digits, letters = check_corrected_pass(password)
    while digits is not False and letters is not False:
        password = final_pass(answer_dict, pass_length)
    return password


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


# Запускаем бота
bot.polling(none_stop=True, interval=0)
