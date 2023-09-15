from telebot import TeleBot
from db import BotDB
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup
from celery_project.parser.tasks import parse_website
from datetime import datetime
from visualization import draw_social_graph

token = '5995097596:AAFNDm8tv_31RkT7XbdeEupqrs8vezAUlwM'
bot = TeleBot(token)
db = BotDB()

# Кнопки для главного меню
main_menu = InlineKeyboardMarkup()
search_btn = InlineKeyboardButton(text = 'Поиск', callback_data="search_btn")
profile_btn = InlineKeyboardButton(text = 'Личный кабинет', callback_data="profile_btn") #
main_menu.add(search_btn, profile_btn)

# Кнопки для выбора роли
role_keyboard = InlineKeyboardMarkup()
manager_btn = InlineKeyboardButton(text='Менеджер', callback_data="manager_btn") #
user_btn = InlineKeyboardButton(text='Пользователь', callback_data="user_btn") #
role_keyboard.add(manager_btn, user_btn)

user_profile_keyboard = InlineKeyboardMarkup()
edit_btn = InlineKeyboardButton('Редактировать данные',callback_data="edit_btn")#
history_btn = InlineKeyboardButton('История',callback_data="history_btn")#
favorites_btn = InlineKeyboardButton('Избранное',callback_data="favourite_btn")#
balance_btn = InlineKeyboardButton('Баланс',callback_data="balance_btn") #
#buy_tokens_btn = InlineKeyboardButton('Купить токены',callback_data="buy_tokens_btn")
main_menu_btn = InlineKeyboardButton('В главное меню',callback_data="main_menu_btn")#
user_profile_keyboard.add(edit_btn, history_btn, favorites_btn, balance_btn)
user_profile_keyboard.add(main_menu_btn)

manager_profile_keyboard = InlineKeyboardMarkup()
search_user_btn = InlineKeyboardButton('Найти пользователя',callback_data="search_user_btn")#
change_balance_btn = InlineKeyboardButton('Изменить баланс',callback_data="change_balance_btn")
activity_btn = InlineKeyboardButton('Активность',callback_data="activity_btn")#
new_users_btn = InlineKeyboardButton('Новые пользователи',callback_data="new_users_btn")#
manager_profile_keyboard.add(edit_btn, history_btn, favorites_btn, balance_btn)
manager_profile_keyboard.add(search_user_btn, change_balance_btn, activity_btn, new_users_btn)
manager_profile_keyboard.add(main_menu_btn)

edit_keyboard = InlineKeyboardMarkup()
username_btn = InlineKeyboardButton('Изменить имя',callback_data="username_btn")#
age_btn = InlineKeyboardButton('Изменить возраст',callback_data="age_btn")#
email_btn = InlineKeyboardButton('Изменить почту',callback_data="email_btn")#
phone_btn = InlineKeyboardButton('Изменить телефон',callback_data="phone_btn")#
back_to_profile_btn = InlineKeyboardButton('Назад', callback_data="profile_btn") #
edit_keyboard.add(username_btn, age_btn)
edit_keyboard.add(email_btn, phone_btn)
edit_keyboard.add(back_to_profile_btn)



@bot.message_handler(commands=['start'])
def reply_start_command(message: Message):
    if not db.user_exist(message.chat.id):
        bot.send_message(message.chat.id, 'Выберите роль', reply_markup=role_keyboard)
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрировались", reply_markup=main_menu)
    #parse_website("Том Холланд")
    #log_message(message)

@bot.callback_query_handler(func=lambda call: call.data == 'activity_btn')
def activity(call):
    msg = bot.send_message(call.message.chat.id, 'За сколько дней вы хотите видеть активность?')
    bot.register_next_step_handler(msg, activity_step, call)
def activity_step(message, call):
    time = int(message.text)
    total_activity = 0 #один серый, другой белый, два веселых total_activity
    total_activity = 0
    history = db.get_all_history()
    for query in history:
        diff =datetime.now().date()-query.date
        if diff.days<=time:
            total_activity += 1
    bot.send_message(call.message.chat.id, f'За {time} дней активность составляет {total_activity} запросов',
                     reply_markup=manager_profile_keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'change_balance_btn')

def change_balance(call):
    msg = bot.send_message(call.message.chat.id, 'Введите ID пользователя:')
    bot.register_next_step_handler(msg, get_user_id_step,call)
def get_user_id_step(message,call):
    user_id = message.text
    msg = bot.send_message(call.message.chat.id, 'Введите новый баланс:')
    bot.register_next_step_handler(msg, change_balance_step, user_id,call)
def change_balance_step(message, user_id,call):
    new_balance = message.text
    user = db.get_user(user_id)
    if user:
        user.points = new_balance
        db.session.commit()
        bot.send_message(call.message.chat.id, 'Баланс успешно изменен!',reply_markup=manager_profile_keyboard)
    else:
        bot.send_message(call.message.chat.id, 'Пользователь не найден!')
@bot.callback_query_handler(func=lambda call: call.data == 'new_users_btn')
def new_users(call):
    msg = bot.send_message(call.message.chat.id, 'За сколько дней вы хотите видеть новых пользователей?')
    bot.register_next_step_handler(msg, new_users_step, call)
def new_users_step(message, call):
    time = int(message.text)
    new_users = 0
    users = db.session.query(db.users).all()
    for user in users:
        reg_date = datetime(user.reg_data.year, user.reg_data.month, user.reg_data.day)
        now_date = datetime.now()
        a = now_date - reg_date
        if a.days <= time:
            new_users += 1
    bot.send_message(call.message.chat.id, f'За {time} дней появилось {new_users} новых пользователей')
    profile(call)




@bot.callback_query_handler(func=lambda call: call.data == 'search_user_btn')
def search_user(call):
    msg = bot.send_message(call.message.chat.id, 'Введите id пользователя')
    bot.register_next_step_handler(msg, search_step, call)

def search_user_step(message, call):
    id = message.text
    user = db.get_user(id)
    if db.user_exist(id):
        bot.send_message(call.message.chat.id,
                     f'Информация о пользователе  {id}:\nИмя - {user.username}\nРоль - {user.role}\nБаланс - {user.points}\nВозраст - {user.age}\nПочта - {user.email}\nТелефон - {user.phone}\nДата регистрации - {datetime(user.reg_data.year, user.reg_data.month, user.reg_data.day)}')
    else: bot.send_message(call.message.chat.id,"Пользователь не найден!")
    profile(call)


@bot.callback_query_handler(func=lambda call: call.data == 'search_btn')
def search(call):
    msg = bot.send_message(call.message.chat.id, 'Введите имя актера')
    bot.register_next_step_handler(msg, search_step, call)

def search_step(message, call):
    actor = message.text
    time = datetime.now()
    event = [actor,time]

    bot.send_message(message.chat.id, 'Поиск начат!!')
    #parse_website(actor)
    #draw_social_graph(actor)
    bot.send_message(message.chat.id, 'Поиск выполнен\nХотите добавить поиск в избранное?\nДа/Нет')
    bot.register_next_step_handler(message, history_add_step, call,event)
def history_add_step(message, call, event):
    answer = message.text
    user = db.get_user(message.chat.id)
    user.points = user.points - 1

    # Create a new history entry
    is_favourite = answer == 'Да'
    db.add_history(user_id=user.user_id, request=event, is_favourite=is_favourite)

    db.user_update(user)
    bot.send_message(message.chat.id, 'Запрос выполнен успешно! С вашего счета снимается 1 токен')
    show_main_menu(call)
@bot.callback_query_handler(func=lambda call: call.data == 'main_menu_btn')
def show_main_menu(call):
    bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=main_menu)
@bot.callback_query_handler(func=lambda call: call.data == 'manager_btn')
def manager(call):
    db.user_add(call.message.chat.id,call.message.chat.username,'Manager')
    bot.send_message(call.message.chat.id, "Вы зарегистрировались как Менеджер!",reply_markup=main_menu)
@bot.callback_query_handler(func=lambda call: call.data == 'user_btn')
def user(call):
    db.user_add(call.message.chat.id,call.message.from_user.username,'User')
    bot.send_message(call.message.chat.id, "Вы зарегистрировались как Пользователь!",reply_markup=main_menu)
@bot.callback_query_handler(func=lambda call: call.data == 'profile_btn')
def profile(call):
    temp_role_keyboard = None
    if db.get_user(call.message.chat.id).role=='User':
        temp_role_keyboard=user_profile_keyboard
    elif db.get_user(call.message.chat.id).role=='Manager':
        temp_role_keyboard=manager_profile_keyboard
    user = db.get_user(call.message.chat.id)
    bot.send_message(call.message.chat.id, f'Личный кабинет\nИмя - {user.username}\nРоль - {user.role}\nВозраст - {user.age}\nПочта - {user.email}\nТелефон - {user.phone}', reply_markup=temp_role_keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'balance_btn')
def balance(call):
    user =db.get_user(call.message.chat.id)
    bot.send_message(call.message.chat.id, f'Ваш баланс - {user.points} токенов.')
    profile(call)
@bot.callback_query_handler(func=lambda call: call.data == 'edit_btn')
def edit(call):
    bot.send_message(call.message.chat.id, 'Режим редактирования',reply_markup=edit_keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'username_btn')
def edit_username(call):
    msg = bot.send_message(call.message.chat.id, 'Введите новое имя')
    bot.register_next_step_handler(msg, username_step, call)
def username_step(message,call):
    user = db.get_user(message.chat.id)
    user.username = message.text
    db.user_update(user)
    bot.send_message(message.chat.id, 'Новое имя выбрано!')
    edit(call)

@bot.callback_query_handler(func=lambda call: call.data == 'age_btn')
def edit_age(call):
    msg = bot.send_message(call.message.chat.id, 'Введите новый возраст')
    bot.register_next_step_handler(msg, age_step,call)
def age_step(message,call):
    user = db.get_user(message.chat.id)
    user.age = message.text
    db.user_update(user)
    bot.send_message(message.chat.id, 'Новый возраст выбран!')
    edit(call)
@bot.callback_query_handler(func=lambda call: call.data == 'email_btn')

def edit_email(call):
    msg = bot.send_message(call.message.chat.id, 'Введите новый email')
    bot.register_next_step_handler(msg, email_step,call)
def email_step(message,call):
    user = db.get_user(message.chat.id)
    user.email = message.text
    db.user_update(user)
    bot.send_message(message.chat.id, 'Новый email выбран!')
    edit(call)
@bot.callback_query_handler(func=lambda call: call.data == 'phone_btn')
def edit_phone(call):
    msg = bot.send_message(call.message.chat.id, 'Введите новый номер телефона')
    bot.register_next_step_handler(msg, phone_step,call)
def phone_step(message,call):
    user = db.get_user(message.chat.id)
    user.phone = message.text
    db.user_update(user)
    bot.send_message(message.chat.id, 'Новый номер телефона выбран!')
    edit(call)


@bot.callback_query_handler(func=lambda call: call.data == 'history_btn')
def show_history(call):
    history = db.get_history(call.message.chat.id)

    text = 'Ваша история:\n'
    if len(history)!=0:
        for event in history:
            #date = datetime.fromtimestamp(event[1])
            text += f'{event.request} - {event.date}\n'
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')
    else:
        bot.send_message(call.message.chat.id, "История пуста!")
    profile(call)


@bot.callback_query_handler(func=lambda call: call.data == 'favourite_btn')
def show_favourite(call):
    favourite = db.get_favourite(call.message.chat.id)
    text = 'Ваше избранное:\n'
    if len(favourite)!=0:
        for event in favourite:
            #date = datetime.fromtimestamp(event[1])
            text += f'{event.request} - {event.date}\n'
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')
    else:
        bot.send_message(call.message.chat.id, "Избранные пусты!")
    profile(call)
@bot.message_handler(func=lambda message: True)
def log_message(message: Message):
    if db.user_exist(message.chat.id):
        db.add_log(message.from_user.username, message.chat.id, message.text, message.date)

if __name__ == '__main__':
    print("Bot started")
    bot.infinity_polling()

# Вставил комментарий
