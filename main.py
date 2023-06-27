from telebot import TeleBot
from db import BotDB
from telebot.types import Message

token = '6001783957:AAGjtyLX2728zncYkhCDMIq0_MsasMBtOY0'
bot = TeleBot(token)
db = BotDB('db_file')


@bot.message_handler(commands=['start'])
def reply_start_command(message: Message):
    if not db.user_exist(message.chat.id):
        bot.send_message(message.chat.id, "Приветсвите перед регитрацией")
        db.user_add(message.chat.id, message.from_user.first_name)
    else:
        bot.send_message(message.chat.id, "Приветстивие зареганого пользователя")


bot.infinity_polling()
# Вставил комментарий
