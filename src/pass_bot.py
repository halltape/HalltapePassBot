import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import random
import math
import sys


# Создаем экземпляр бота
bot = telebot.TeleBot('6241297991:AAGNcDf_teJPYv-B1qCqDXUtJi1ebUe1TT8')


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
# Добавляем две кнопки 
def start(m, res=False):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=types.KeyboardButton('Получить надежный пароль')
    button2=types.KeyboardButton('CRAZY MODE')
    markup.add(button1)
    markup.add(button2)
    bot.send_message(m.chat.id,
                     '*Нажми нужную кнопку\!*\n\n'
                     '1️⃣ Получить надежный пароль \(*18 символов*\)\n'
                     'Можешь нажимать бесконечное кол\-во раз\n'
                     '\n2️⃣ *CRAZY MODE*\n'
                     '\n*Для проверки своего пароля просто отправь его боту*\n',
                      reply_markup=markup, parse_mode='MarkdownV2')


# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id, 'По всем вопросам работы бота писать *@halltape*\n', parse_mode='MarkdownV2')


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
        
    if message.text.strip() == 'CRAZY MODE':
        answer = strong_pass(True)
        bot.send_message(message.chat.id, answer)
    elif message.text.strip() == 'Получить надежный пароль':
        answer = strong_pass(False)
        bot.send_message(message.chat.id, answer)
    else:
        get_pass(message)


def get_pass(message: types.Message):   # Функция проверки пароля
    if len(message.text) <= 50:
        bit, time, unique, dict_answer = check_pass(message.text)
        verdict, time_final = '', ''
        period = period_result(time) # Функция, которая возвращает строку с числом и периодом времени
        
        if dict_answer['digit'] == False:
            verdict += '⚠️ Нет цифр\n' # Попробовать вписать сюда Markdown mode
        if dict_answer['lower'] == False:
            verdict += '⚠️ Нет букв в нижнем регистре\n'
        if dict_answer['upper'] == False:
            verdict += '⚠️ Нет букв в верхнем регистре\n'
        if dict_answer['special'] == False:
            verdict += '⚠️ Нет специальных символов\n'
        if dict_answer['length'] < 16:
            verdict += '⚠️ Длина пароля меньше 16 символов\n'
        if dict_answer['duplicates'][0] == True:
            verdict += '⚠️ Больше трех чисел друг за другом\n'
        if dict_answer['duplicates'][1] == True:
            verdict += '⚠️ Повторяющиеся символы\n'
        if unique < 0.6:
            verdict += '⚠️ Малая уникальность пароля\n'

        if (time // 3600 // 24) < 7:
            if time < 1: # Если время меньше 1 секунды, чтобы не писать мск
                time_final = '\n⏳ Пароль взломают моментально\n'
            else:
                time_final = '\n⏳ На его взлом уйдет 'f'{period}\n'

        bit_final = '\nСила пароля 'f'{bit} бит\nОптимальное значение от 97 и больше'

        if verdict != '' and bit < 97:
            verdict_final = '❌ Тебе нужно усилить твой пароль!\n\n' + verdict + time_final + bit_final


        if bit > 96 and unique > 0.6 and dict_answer['duplicates'][0] == False and dict_answer['duplicates'][1] == False:
            if period == True:
                time_final = '\nСолнце быстрее погаснет, чем подберут твой пароль\n'
            else:
                time_final = '\nНа его взлом уйдет 'f'{time}\n'
            verdict_final = '✅ У тебя хороший пароль!\n' + time_final + bit_final
        else:
            verdict_final = '❌ Тебе нужно усилить твой пароль!\n\n' + verdict + time_final + bit_final
    else:
        verdict_final = 'ℹ Пароль слишком длинный, в этом нет смысла'

    bot.send_message(message.chat.id, verdict_final)
    if verdict_final[0] == '❌':
        #инлайновая клавиатура
        inMurkup = types.InlineKeyboardMarkup(row_width=1)
        inline_button = types.InlineKeyboardButton('Усилить', callback_data=message.text)
        inMurkup.add(inline_button)
        bot.send_message(message.chat.id, 'Ты можешь усилить свой пароль', reply_markup=inMurkup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        bot.send_message(call.message.chat.id, f'{call.data}')
    elif call.message == 'strong':
        bot.send_message(call.message.chat.id, strong_pass(False))
    return 0


def check_pass(password):
    total, count, summ = 0, 0, 0
    dictionary = {'digit':False, 'lower':False,
                  'upper':False, 'special':False, 
                  'length':len(password), 'duplicates':[False, False]} 
    if any(c.isdigit() for c in password):
        total += 10
        dictionary['digit'] = True
    if any(c.isalpha() for c in password):
        total += 26
        dictionary['lower'] = True
    if any(c.isalpha() for c in password if c == c.upper()):
        total += 26
        dictionary['upper'] = True
    if any(c for c in password if c in ('":,.;^*!@#$%&*()><}{[]?')):
        total += 22
        dictionary['special'] = True

    for c in password:
        if c in ('1234567890'):
            count += 1
            if count > 3:
                dictionary['duplicates'][0] = True
        else:
            count = 0

    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            summ += 1
            if summ > 2:
                dictionary['duplicates'][1] = True
        else:
            summ = 0

    entropy = round(math.log2(total**len(password)))  # Энтропия
    
    if sys.float_info.max > total**len(password):
        time_seconds = (round(total**len(password) / 3900000000)) # Время подбора в секундах
    else:
        time_seconds = math.inf
    
    metric_unique = len(set(password)) / len(password)

    return entropy, time_seconds, metric_unique, dictionary


def question_input(custom):
    # Опрос пользователя по сложности пароля
    if custom == False:
        qa_list = ['1', '1', '1', '0', '1'] # Включен режим максимльной надежности
        return qa_list
    # else:
    #     qa_list = ['0', '0', '0', '0', '0']
    # return steps(qa_list)


def generate_password(lst):
    # По полученному опроснику генерируем sample
    # пароля из максимум 4 элементов и пишем в строку
    sample_password = ''
    if lst[0] == '1':
        sample_password += random.choice('0123456789')
    if lst[1] == '1':
        sample_password += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    if lst[2] == '1':
        sample_password += random.choice('abcdefghijklmnopqrstuvwxyz')
    if lst[3] == '1':
        sample_password += random.choice('!@#$%&*()><}{[]?')
    if lst[4] == '1':
        sample_password = sample_password.replace('i', 'F').replace('l', 'g') \
            .replace('1', 'p').replace('L', '7').replace('o', 't') \
            .replace('0', '2').replace('O', 'z')
    return sample_password


def final_pass(answ_list, length): # Собираем финальный пароль из сэмплов (каждый из 4 элементов)
    final_password = '' # Создаем пустую строку для будущего сэмпла
    while len(final_password) <= length: # Собираем пароль, пока длина не превысит нужную
        for _ in range(math.ceil(length / 4)): # Если длина будет n, то сэмпл соберается длиной n + 1
            final_password += generate_password(answ_list) # Конкатенация строк сэмплов пароля
    final_password = final_password[:length]
    final_password = ''.join(random.sample(final_password, len(final_password))) # Перемешиваем пароль
    return final_password[:length]


def strong_pass(button):
    if button == True:
        pass_length = 1000
    else:
        pass_length = 18
    answer_list = question_input(False)
    password = final_pass(answer_list, pass_length)
    return password


def period_result(period):
    dict_period = {'seconds':'секунд',
                'hours':'час',
                'days':'д',
                'years':'',
                'century':'век'}

    dict_ends = {'seconds':['','а','ы'],
                'hours':['ов', '', 'а'],
                'days':['ней', 'ень', 'ня'],
                'years':['лет', 'год', 'года'],
                'century':['ов', '', 'а']}

    if period // 3600 // 24 // 365 // 100 > 60000000:
        result = True
        return result
    if period < 3600:
        word = dict_period['seconds']
    elif 3600 <= period < (24 * 3600):
        word = dict_period['hours']
        period = period // 3600 # Количество секунд
    elif 24 * 3600 <= period < (24 * 3600) * 365:
        word = dict_period['days']
        period = period // 3600 // 24 # количество дней
    elif ((24 * 3600) * 365) <= period < ((24 * 3600) * 365 * 100):
        word = dict_period['years']
        period = period // 3600 // 24 // 365 # Количество лет
    elif period >= ((24 * 3600) * 365 * 100):
        word = dict_period['century']
        period = period // 3600 // 24 // 365 // 100 # Количество веков


    if int(period) % 10 in (0, 5, 6, 7, 8, 9) or int(period) in range(11, 20): # 15
        if word == dict_period['seconds']:
            word += dict_ends['seconds'][0]

        if word == dict_period['hours']:
            word += dict_ends['hours'][0]

        if word == dict_period['days']:
            word += dict_ends['days'][0]

        if word == dict_period['years']:
            word += dict_ends['years'][0]
        
        if word == dict_period['century']:
            word += dict_ends['century'][0]

    elif int(period) % 10 == 1 and int(period) not in range(11, 20): # 1
        if word == dict_period['seconds']:
            word += dict_ends['seconds'][1]

        if word == dict_period['hours']:
            word += dict_ends['hours'][1]

        if word == dict_period['days']:
            word += dict_ends['days'][1]

        if word == dict_period['years']:
            word += dict_ends['years'][1]

        if word == dict_period['century']:
            word += dict_ends['century'][1]

    elif int(period) % 10 in (2, 3, 4): # 4
        if word == dict_period['seconds']:
            word += dict_ends['seconds'][2]

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
