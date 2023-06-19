from telebot import TeleBot

bot = TeleBot('6001783957:AAGjtyLX2728zncYkhCDMIq0_MsasMBtOY0')


@bot.message_handler(commands=['start'])
def reply_start_command(message):
    bot.send_message(message.chat.id, "Текст приветсвия пользователя")


bot.infinity_polling()
