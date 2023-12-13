import telebot
from telebot import types
import random

bot = telebot.TeleBot('6838639459:AAG-TzTvPF1jh_Q7P7KcZH9hFxjLUQugJVc')

games = {}

@bot.message_handler(commands=['Hi'])
def start(message):
    mess = f'Hi <b><u>{message.from_user.first_name}</u></b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("Задать вопрос❓")
    btn3 = types.KeyboardButton("Играем")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я помощник Менторов по Python".format(
                         message.from_user), reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Играем")
def start_game(message):
    chat_id = message.chat.id
    if chat_id not in games:
        secret_number = random.randint(1, 10)
        games[chat_id] = {'secret_number': secret_number, 'attempts': 0}
        bot.send_message(chat_id, "Угадай число от 1 до 10. Введи свой вариант.")
    else:
        bot.send_message(chat_id, "Игра уже начата. Введи свой вариант числа.")

@bot.message_handler(func=lambda message: message.text.isdigit() and message.chat.id in games)
def handle_guess(message):
    chat_id = message.chat.id
    user_guess = int(message.text)
    correct_number = games[chat_id]['secret_number']
    games[chat_id]['attempts'] += 1

    if user_guess == correct_number:
        attempts = games[chat_id]['attempts']
        bot.send_message(chat_id, f"Поздравляю! Ты угадал число {correct_number} за {attempts} попыток.")


        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("Задать вопрос❓")
        button3 = types.KeyboardButton("Играем")
        markup.add(button1, button2, button3)
        bot.send_message(chat_id, text="Вы вернулись в главное меню", reply_markup=markup)

        del games[chat_id]
    elif user_guess < correct_number:
        bot.send_message(chat_id, "Попробуй число больше.")
    else:
        bot.send_message(chat_id, "Попробуй число меньше.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "👋 Поздороваться":
        bot.send_message(message.chat.id, text='За помощью ко мне правильное решение!')
    elif message.text == "Задать вопрос❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Что я могу?')
        btn2 = types.KeyboardButton('Кто мой создатель?')
        btn3 = types.KeyboardButton('Вернуться в главное меню')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text='Выбирай вопрос!', reply_markup=markup)
    elif message.text == 'Кто мой создатель?':
        bot.send_message(message.chat.id, text='Мой создатель BOOTCAMP_21')
    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Я могу показать 3х месячную программу по изучению (PYTHON)")
        markup_inline = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton(text='Показать', callback_data='yes')
        item_no = types.InlineKeyboardButton(text='Отменить', callback_data='no')
        markup_inline.row(item_yes, item_no)
        bot.send_message(message.chat.id, text="Показать вам список курса?", reply_markup=markup_inline)
    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("Задать вопрос❓")
        button3 = types.KeyboardButton("Играем")
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)



bot.polling(none_stop=True)