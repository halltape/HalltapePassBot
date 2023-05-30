import string
import telebot


from library import *
from func_pass import strong_pass
from faq_bot import faq_about
from end_of_words import period_result, end_of_word
from func_pass import social_password, pass_corrector
from checking_pass import check_pass, check_table_words
from func_pass import beautiful_password_first, create_nickname


# Add telegram token
bot = telebot.TeleBot('6172414813:AAGLvVUX0JQfxqEcSkuy9S8TNvp31cEXs6M')


# A function that handles the /start command
@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Легкий пароль')
    markup.row('Пароль для соц сетей', 'Сложный пароль')
    markup.row('Проверить свой пароль')
    markup.row('Создать никнейм')
    bot.send_message(m.chat.id,
                     '\n\n*🔐 Напиши боту свой пароль и'
                     ' он проверит его на надежность*\\!\n'
                     '*Либо можешь сгенерировать уже готовый\\!*\n\n'
                     '1️⃣ Легкий пароль\n'
                     '\n2️⃣ Пароль для соц сетей\n'
                     '\n3️⃣ Сложный пароль\n'
                     '\n4️⃣ Создать никнейм',
                     reply_markup=markup, parse_mode='MarkdownV2')


# A function that handles the /help command
@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id, 'По всем вопросам работы бота '
                     'писать *@halltape*\n'
                     '\n*Подробное описание проекта*, а также весь'
                     ' исходный код доступен по ссылке:\n\n'
                     'https:\\/\\/github\\.com\\/halltape\\/HalltapePassBot',
                     parse_mode='MarkdownV2')


# A function that handles the /about command
@bot.message_handler(commands=["about"])
def help(m, res=False):
    result = faq_about()
    bot.send_message(m.chat.id, result, parse_mode='MarkdownV2')


# Receiving messages from the user
@bot.message_handler(content_types=["text"])
def handle_text(message):

    flag = True
    check_string = string.ascii_lowercase + string.ascii_uppercase + \
        string.punctuation + string.digits

    if message.text.strip() == 'Легкий пароль':
        bot.send_message(message.chat.id,
                         f'{beautiful_password_first()}',)
    elif message.text.strip() == 'Пароль для соц сетей':
        markup = telebot.types.ReplyKeyboardMarkup(True)
        markup.row('🗺 Google', '📮 Yandex', '📘 Vk', '📬 Mail')
        markup.row('💬 Facebook', '📺 Avito', '📱 Instagram')
        markup.row('📄 Gosuslugi', '🔥 Свой вариант')
        markup.row('🏠 Назад в меню')
        bot.send_message(message.chat.id,
                         '*Выбери* к чему тебе нужно придумать пароль',
                         reply_markup=markup, parse_mode='MarkdownV2')

    elif message.text.strip() == 'Проверить свой пароль':
        bot.send_message(message.chat.id,
                         '*🤖 Отправь свой пароль в виде сообщения*',
                         parse_mode='MarkdownV2')
    elif message.text.strip() == 'Создать никнейм':
        bot.send_message(message.chat.id, f'{create_nickname()}',)

    elif message.text.strip() in ('🗺 Google', '📮 Yandex', '📘 Vk', '📬 Mail',
                                  '💬 Facebook', '📺 Avito', '📱 Instagram',
                                  '📄 Gosuslugi'):
        text_to_function = message.text.lower()
        bot.send_message(message.chat.id,
                         social_password(text_to_function[2:]))

    elif message.text.strip() == '🔥 Свой вариант':
        bot.send_message(message.chat.id,
                         'Напиши название *сайта* или *приложения*',
                         parse_mode='MarkdownV2')
        bot.register_next_step_handler(message, get_individual)

    elif message.text.strip() == '🏠 Назад в меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Пароль\n(легко запомнить)')
        markup.row('Пароль для соц сетей', 'Обычный пароль')
        markup.row('Проверить свой пароль')
        markup.row('Создать никнейм')
        bot.send_message(message.chat.id, '🏝 Ты в меню', reply_markup=markup)

    elif message.text.strip() == 'Сложный пароль':
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
                             '\\- Есть пробелы\n'
                             '\\- Перепутана русская *A* и латинская\n'
                             '\\- Есть нестандартные символы\n\n'
                             '*P\\.S\\. Бот различает русский и '
                             'латинский алфавит*',
                             parse_mode='MarkdownV2')


# Function for processing user input of a website name
def get_individual(message: types.Message):

    check_string = string.ascii_lowercase + string.ascii_uppercase + \
        string.punctuation + string.digits
    text = message.text
    flag = True
    for char in message.text.strip():
        if char not in (check_string):
            flag = False

    if message.text.strip() in ('🗺 Google', '📮 Yandex', '📘 Vk', '📬 Mail',
                                '💬 Facebook', '📺 Avito', '📱 Instagram',
                                '📄 Gosuslugi'):
        text = message.text[2:].lower()
        bot.send_message(message.chat.id, '💎 Вот *пять вариантов* для тебя\\!',
                         parse_mode='MarkdownV2')
        for _ in range(0, 5):
            bot.send_message(message.chat.id, social_password(text))
    elif flag is False:
        bot.send_message(message.chat.id,
                         '❌ *Недопустимые символы*\n'
                         'Проверьте вводимый текст\n\n'
                         '\\- Есть пробелы\n'
                         '\\- Перепутана русская *A* и латинская\n'
                         '\\- Есть нестандартные символы\n\n'
                         '*P\\.S\\. Бот различает русский и '
                         'латинский алфавит*',
                         parse_mode='MarkdownV2')
        return 0
    else:
        bot.send_message(message.chat.id, '💎 Вот *пять вариантов* для тебя\\!',
                         parse_mode='MarkdownV2')
        for _ in range(0, 5):
            bot.send_message(message.chat.id, social_password(text))


def get_pass(message: types.Message):   # Password verification function

    attention = '❌ Тебе нужно усилить твой пароль!\n\n'
    middle_attention = 'ℹ️ Пароль неплохой,' \
        ' но обрати внимание на замечания\n\n'
    good_attention = '✅ У тебя хороший пароль!\n'
    sun_attention = '\n⏳ Солнце уже потухнет,' \
        ' а твой пароль все еще будут подбирать\n'

    if len(message.text) <= 50:

        bit, time, unique, dict_answer = check_pass(message.text)
        leaked_passwords = check_table_words(message.text)

        verdict, time_final, verdict_final = '', '', ''
        difference = 9 - dict_answer['length']
        difference_word_end = end_of_word(difference)
        verdict_final = 'test'

        # Function that returns a string with a number and a time period
        period = period_result(time)

        if dict_answer['digit'] is False:
            verdict += '⚠️ Нет цифр\n'
        if dict_answer['lower'] is False:
            verdict += '⚠️ Нет букв в нижнем регистре\n'
        if dict_answer['upper'] is False:
            verdict += '⚠️ Нет букв в верхнем регистре\n'
        if dict_answer['special'] is False:
            verdict += '⚠️ Нет специальных символов\n'
        if dict_answer['length'] < 9:
            verdict += '⚠️ Добавь в пароль' \
                ' еще 'f'{difference} 'f'{difference_word_end}\n'
        if dict_answer['duplicates'][0] is True:
            verdict += '⚠️ Больше четырех чисел друг за другом\n'
        if dict_answer['duplicates'][1] is True:
            verdict += '⚠️ Повторяющиеся символы\n'
        if unique < 0.6:
            verdict += '⚠️ Малая уникальность пароля\n'
        if leaked_passwords != '':
            verdict += '⚠️ Твой пароль полностью или частично слит в сеть\n' \
                '\n⬇️ Слитые пароли\n' + leaked_passwords

        if (time // 3600 // 24) < 183:
            if time < 1:  # If time is smaller than 1 second
                time_final = '\n⏳ Пароль взломают моментально\n'
            else:
                time_final = '\n⏳ На его взлом уйдет 'f'{period}\n'
        elif period is True:
            time_final = sun_attention
        else:
            time_final = '\n⏳ На его взлом уйдет 'f'{period}\n'

        bit_final = '\nНадежность пароля 'f'{round(bit / 97 * 100)} %'

        if verdict != '' and bit < 97:
            if dict_answer['length'] > 9 \
                    and (time // 3600 // 24 // 365) > 1 and unique > 0.5 \
                    and dict_answer['duplicates'][0] is False \
                    and dict_answer['duplicates'][1] is False \
                    and leaked_passwords == '':
                verdict_final = middle_attention + verdict + time_final
            else:
                if (time // 3600 // 24) > 183:
                    time_final = ''
                verdict_final = attention + verdict + time_final + bit_final

        if bit > 96 and unique > 0.6 \
                and dict_answer['duplicates'][0] is False\
                and dict_answer['duplicates'][1] is False:
            verdict_final = good_attention + time_final
        else:
            if bit > 96:
                bit_final = ''
                verdict_final = attention + verdict + bit_final
        if verdict == '':
            verdict_final = good_attention + time_final
    else:
        verdict_final = '♾ Пароль слишком длинный, в этом нет смысла'

    bot.send_message(message.chat.id, verdict_final)

    if verdict_final[0] in ('❌', 'ℹ'):
        # In-line keyboard
        inMurkup = types.InlineKeyboardMarkup(row_width=1)
        inline_button = types.InlineKeyboardButton('💪🏻 Усложнить пароль',
                                                   callback_data=message.text)
        inMurkup.add(inline_button)
        bot.send_message(message.chat.id,
                         '*Нажми кнопку*, чтобы усложнить свой пароль\n' +
                         12 * '\t' + '*Жми сколько влезет\\!*',
                         parse_mode='MarkdownV2', reply_markup=inMurkup)
    if verdict_final[0] in ('✅'):
        # In-line keyboard
        inMurkup = types.InlineKeyboardMarkup(row_width=1)
        inline_button = types.InlineKeyboardButton('👁 Сделай красиво',
                                                   callback_data=message.text)
        inMurkup.add(inline_button)
        bot.send_message(message.chat.id,
                         '*Могу поработать над красотой пароля*\n' +
                         12 * '\t' + '*Жми сколько влезет\\!*',
                         parse_mode='MarkdownV2', reply_markup=inMurkup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    corrected_password = pass_corrector(call.data)
    bot.send_message(call.message.chat.id, corrected_password)


# Start the bot
bot.polling(none_stop=True, interval=0)
