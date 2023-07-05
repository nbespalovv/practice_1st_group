from telebot import TeleBot
from db import BotDB
from telebot.types import Message
from celery_project.parser.tasks import parse_website

token = '6001783957:AAGjtyLX2728zncYkhCDMIq0_MsasMBtOY0'
bot = TeleBot(token)
db = BotDB()


@bot.message_handler(commands=['start'])
def reply_start_command(message: Message):
    if not db.user_exist(message.chat.id):
        bot.send_message(message.chat.id, "Приветствие перед регитрацией")
        db.user_add(message.chat.id, message.from_user.first_name)
    else:
        bot.send_message(message.chat.id, "Приветстивие зареганого пользователя")
    parse_website.delay("Том Холланд")



if __name__ == '__main__':
    print("Bot started")
    bot.infinity_polling()

# Вставил комментарий
