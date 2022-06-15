import telebot
from telebot import types
from ai import image_to_text
import os

TOKEN = '5405570088:AAFOgu3BjIlAlp-S6mjea5E1aMZST8oInHc'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_reply(message):
    print(f'{message.from_user.username}: {message.text}')
    about_reply(message)


@bot.message_handler(content_types=['text'])
def handle_commands(message):
    match message.text.lower():
        case 'фото → текст':
            bot.send_message(message.chat.id, 'Выберите язык.', reply_markup=choose_language_markup())
            bot.register_next_step_handler(message, choose_lang)
        case 'обо мне':
            about_reply(message)
        case _:
            bot.send_message(message.chat.id,
                             'Я вас не понял...\n'
                             'Попробуйте использовать кнопки, чтобы взаимодействовать со мной.',
                             reply_markup=init_markup())


# @bot.message_handler(content_types=['photo', 'document'])
def handle_photo(message, lang):
    try:
        if message.content_type == 'photo':
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            src = rf'G:\PythonProjects\ComputerVisionBot\{file_info.file_path}'
        elif message.content_type == 'document':
            file_info = bot.get_file(message.document.file_id)
            src = rf'G:\PythonProjects\ComputerVisionBot\photos\{message.document.file_name}'
        else:
            bot.send_message(message.chat.id, 'Неверный тип файла.', reply_markup=init_markup())
            return
        print(message.content_type)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.send_message(message.chat.id, image_to_text(src, lang), reply_markup=init_markup())

        os.remove(src)

    except Exception as e:
        bot.send_message(message.chat.id, 'Не удалось преобразовать фото в текст.', reply_markup=init_markup())
        print(e)


def choose_lang(message):
    match message.text:
        case 'Английский':
            bot.send_message(message.chat.id,
                             'Отправьте мне изображение с текстом на английском языке.',
                             reply_markup=None)
            bot.register_next_step_handler(message, lambda x: handle_photo(x, lang='eng'))
        case 'Русский':
            bot.send_message(message.chat.id,
                             'Отправьте мне изображение с текстом на русском языке.',
                             reply_markup=None)
            bot.register_next_step_handler(message, lambda x: handle_photo(x, lang='rus'))
        case 'Назад':
            bot.send_message(message.chat.id,
                             'Воспользуйтесь кнопками, чтобы со мной взаимодействовать.',
                             reply_markup=init_markup())
        case _:
            bot.send_message(message.chat.id,
                             'Выбран несуществующий язык. Попробуйте ещё раз.',
                             reply_markup=choose_language_markup())


def about_reply(message):
    bot.send_message(message.chat.id,
                     'Привет!\n'
                     'Я бот, который поможет вам преобразовать фото в текст.\n'
                     'Используте кнопки, чтобы взаимодействовать со мной.',
                     reply_markup=init_markup())


def choose_language_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    eng_button = types.KeyboardButton('Английский')
    rus_button = types.KeyboardButton('Русский')
    back_button = types.KeyboardButton('Назад')
    markup.row(eng_button, rus_button)
    markup.row(back_button)
    return markup


def init_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Фото → Текст')
    button2 = types.KeyboardButton('Обо мне')
    markup.add(button1, button2)
    return markup


bot.infinity_polling()
