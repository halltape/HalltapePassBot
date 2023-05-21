from library import *
from func_pass import strong_pass
from period_time import period_result
from check_pass import check_pass, delete_most_popular
from func_pass import generate_password, check_corrected_pass
from func_pass import beautiful_password_first, beautiful_password_second
from func_pass import social_password

# Создаем экземпляр бота
bot = telebot.TeleBot('TOKEN')


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
# Добавляем две кнопки
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Красивый пароль (I вариант)')
    markup.row('Красивый пароль (II вариант)')
    markup.row('Пароль для соц сетей')
    markup.row('Обычный пароль')
    bot.send_message(m.chat.id, '\n\n*🔐 Проверь и усложни свой пароль\\!\n'
                     'Отправь его боту в виде сообщения*\n\n'
                     '*Либо можешь сгенерировать уже готовый\!*\n\n'
                     '1️⃣ Красивый пароль\n'
                     '\n2️⃣ Пароль для соц сетей\n'
                     '\n3️⃣ Обычный пароль',
                     reply_markup=markup, parse_mode='MarkdownV2')


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["social"])
# Добавляем две кнопки
def social(m, res=True):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Google', 'Yandex', 'Vk', 'Mail')
    markup.row('Facebook', 'Avito', 'Instagram')
    markup.row('Gosuslugi', 'Универсальный')
    bot.send_message(m.chat.id, '*Выбери* к чему тебе нужно придумать пароль',
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

    if message.text.strip() == 'Красивый пароль (I вариант)':
        bot.send_message(message.chat.id,
                         f'{beautiful_password_first()}',)
    elif message.text.strip() == 'Красивый пароль (II вариант)':
        bot.send_message(message.chat.id,
                         f'{beautiful_password_second()}',)
    elif message.text.strip() == 'Пароль для соц сетей':
        bot.send_message(message.chat.id, 'Выскакивает картинка, куда нажать для команды')

    elif message.text.strip() in ('Google', 'Yandex', 'Vk', 'Mail',
                                  'Facebook', 'Avito', 'Instagram',
                                  'Gosuslugi'):
        bot.send_message(message.chat.id, social_password(message.text.lower()))

    elif message.text.strip() == 'Универсальный':
        bot.send_message(message.chat.id, social_password('*****'))

    elif message.text.strip() == 'Обычный пароль':
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
    return 0


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

        bit_final = '\nНадежность пароля 'f'{round(bit / 97 * 100)} %'
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
                call_back_pass = delete_most_popular(call_back_pass,
                                                     check_string)
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


# Запускаем бота
bot.polling(none_stop=True, interval=0)
