import telebot
import json


TOKEN = "6453702749:AAG6IB09_ZuLcOKcOA8citO5cl91WUy9xrQ"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    kb = telebot.types.InlineKeyboardMarkup()
    btn_rate = telebot.types.InlineKeyboardButton(
        'Рейтинг преподавателей', callback_data='teachers_rate')
    btn_set_mark = telebot.types.InlineKeyboardButton('Поставить оценку',
                                                      callback_data='set_mark')
    kb.row(btn_rate)
    kb.row(btn_set_mark)
    bot.send_message(message.chat.id, 'Доступные команды:', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # создаем новую клавиатуру
    kb = telebot.types.InlineKeyboardMarkup()

    # делаем клавиатуру со списком курсов
    if call.data == 'set_mark':
        with open('./db/courses.json', 'r', encoding='UTF-8') as db_file:
            courses = json.load(db_file)

        for key, course_name in courses.items():
            btn = telebot.types.InlineKeyboardButton(
                course_name,
                callback_data=f'set_mark&selected_course={key}'
            )
            kb.row(btn)

    # делаем клавиатуру со списком учителей по выбранному курсу
    if 'set_mark' in call.data and 'selected_course' in call.data:
        with open('./db/teachers.json', 'r', encoding='UTF-8') as db_file:
            teachers = json.load(db_file)
            
        selected_course = call.data.split('=')[-1]
        selected_teachers = []
        for t in teachers:
            if selected_course in t.get('courses'):
                selected_teachers.append(t)

        for i, t in enumerate(selected_teachers):
            btn = telebot.types.InlineKeyboardButton(
                f'{t.get("name")} {t.get("lastname")}',
                callback_data=f'set_mark&selected_teacher={i}'
            )
            kb.row(btn)

    # заменяем старую клавиатуру на новую
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id, reply_markup=kb
    )

        
    
bot.polling(non_stop=True, interval=1)
