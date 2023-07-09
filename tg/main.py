from telebot import TeleBot
from telebot.types import Message
from db import BotDB
token = '6001783957:AAGjtyLX2728zncYkhCDMIq0_MsasMBtOY0'
bot = TeleBot(token)
db = BotDB()


@bot.message_handler(commands=['start'])
def reply_start_command(message: Message):
    if not db.user_exist(message.chat.id):
        bot.send_message(message.chat.id, "Приветствие перед регитрацией")
        db.user_add(message.chat.id, message.from_user.username)
    else:
        bot.send_message(message.chat.id, "Приветстивие зареганого пользователя")
    log_message(message)

@bot.message_handler(func=lambda message: True)
def log_message(message: Message):
    if db.user_exist(message.chat.id):
        db.add_log(message.from_user.username, message.chat.id, message.text, message.date)



bot.infinity_polling()
# Вставил комментарий
