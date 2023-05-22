from library import *
from func_pass import strong_pass
from period_time import period_result
from check_pass import check_pass, delete_most_popular
from func_pass import generate_password, check_corrected_pass
from func_pass import beautiful_password_first, beautiful_password_second
from func_pass import social_password, pass_corrector

# Создаем экземпляр бота
bot = telebot.TeleBot('TOKEN')


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
# Добавляем две кнопки
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Красивый пароль\n(I вариант)', 'Красивый пароль\n(II вариант)')
    markup.row('Пароль для соц сетей', 'Обычный пароль')
    markup.row('Проверить свой пароль')
    bot.send_message(m.chat.id, '\n\n*🔐 Проверь и усложни свой пароль\\!\n'
                     'Отправь его боту в виде сообщения*\n\n'
                     '*Либо можешь сгенерировать уже готовый\!*\n\n'
                     '1️⃣ Красивый пароль\n'
                     '\n2️⃣ Пароль для соц сетей\n'
                     '\n3️⃣ Обычный пароль',
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

    if message.text.strip() == 'Красивый пароль\n(I вариант)':
        bot.send_message(message.chat.id,
                         f'{beautiful_password_first()}',)
    elif message.text.strip() == 'Красивый пароль\n(II вариант)':
        bot.send_message(message.chat.id,
                         f'{beautiful_password_second()}',)
    elif message.text.strip() == 'Пароль для соц сетей':
        markup = telebot.types.ReplyKeyboardMarkup(True)
        markup.row('🗺 Google', '📮 Yandex', '📘 Vk', '📬 Mail')
        markup.row('💬 Facebook', '📺 Avito', '📱 Instagram')
        markup.row('📄 Gosuslugi', '🆓 Универсальный')
        markup.row('🏠 Назад в меню')
        bot.send_message(message.chat.id, '*Выбери* к чему тебе нужно придумать пароль',
                         reply_markup=markup, parse_mode='MarkdownV2')

    elif message.text.strip() == 'Проверить свой пароль':
        bot.send_message(message.chat.id, '*🤖 Отправь свой пароль в виде сообщения*',
                         parse_mode='MarkdownV2')

    elif message.text.strip() in ('🗺 Google', '📮 Yandex', '📘 Vk', '📬 Mail',
                                  '💬 Facebook', '📺 Avito', '📱 Instagram',
                                  '📄 Gosuslugi'):
        text_to_function = message.text.lower()
        bot.send_message(message.chat.id, social_password(text_to_function[2:]))

    elif message.text.strip() == '🆓 Универсальный':
        bot.send_message(message.chat.id, social_password('*****'))

    elif message.text.strip() == '🏠 Назад в меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Красивый пароль\n(I вариант)', 'Красивый пароль\n(II вариант)')
        markup.row('Пароль для соц сетей', 'Обычный пароль')
        markup.row('Проверить свой пароль')
        bot.send_message(message.chat.id, '🏝 Ты в меню', reply_markup=markup)

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

    attention = '❌ Тебе нужно усилить твой пароль!\n\n'
    good_attention = '✅ У тебя хороший пароль!\n'
    sun_attention = '\n⏳ Солнце уже потухнет, а твой пароль все еще будут подбирать\n'

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
                verdict_final = good_attention
                if period is True:
                    time_final = sun_attention
                else:
                    time_final = '\n⏳ На его взлом уйдет 'f'{period}\n'
                verdict_final += time_final
            else:
                verdict_final = attention + verdict + time_final + bit_final

        if bit > 96 and unique > 0.6 and dict_answer['duplicates'][0] is False\
                and dict_answer['duplicates'][1] is False:
            if period is True:
                time_final = sun_attention
            else:
                time_final = '\nНа его взлом уйдет 'f'{time}\n'
            verdict_final = good_attention + time_final
        else:
            if bit > 96:
                bit_final = ''
                verdict_final = attention + verdict + time_final + bit_final
    else:
        verdict_final = '♾ Пароль слишком длинный, в этом нет смысла'

    bot.send_message(message.chat.id, verdict_final)

    if verdict_final[0] == '❌':
        # инлайновая клавиатура
        inMurkup = types.InlineKeyboardMarkup(row_width=1)
        inline_button = types.InlineKeyboardButton('💪🏻 Усложнить пароль',
                                                   callback_data=message.text)
        inMurkup.add(inline_button)
        bot.send_message(message.chat.id,
                         '*Нажми кнопку*, чтобы усложнить свой пароль\n' +
                         12 * '\t' + '*Жми сколько влезет\\!*',
                         parse_mode='MarkdownV2', reply_markup=inMurkup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    corrected_password = pass_corrector(call.data)
    bot.send_message(call.message.chat.id, corrected_password)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
