import telebot
from telebot import types

bot = telebot.TeleBot('6613003847:AAEgJ0-Fv-rWETllnN8WwH7eyZGSeTOL8zc')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("ID")
    btn2 = types.KeyboardButton("5 Последних логов")
    btn3 = types.KeyboardButton("Помощь")

    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Бот-информатор".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "ID" or message.text == "/id":
        idchat = message.chat.id
        bot.send_message(message.chat.id, f"Id чата: {idchat}")
    elif message.text == "Помощь" or message.text == "/help":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id,
                         text="Для получения ID нажмите на кнопку ID или введите команду /id.\nДля получения 5 последних логов нажмите на кнопку 5 последних логов или введите команду /last5",
                         reply_markup=markup)

    elif message.text == "/last5" or message.text == "5 Последних логов":
        with open("list.txt", "r") as file1:
            lines = file1.readlines()
            if lines >5:
                for i in range(len(lines)):
                    bot.send_message(message.chat.id, f"{lines[i]}")
                    i += 1


    else:
        bot.send_message(message.chat.id, text="Неизвестная команда. Введите /help для справки")


bot.polling(none_stop=True, interval=0)