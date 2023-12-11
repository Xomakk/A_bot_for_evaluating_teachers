import telebot
import json
import call_handlers

TOKEN = "6453702749:AAG6IB09_ZuLcOKcOA8citO5cl91WUy9xrQ"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    kb = telebot.types.InlineKeyboardMarkup()
    call_handlers.set_menu_btns(kb)
    bot.send_message(message.chat.id, 'Доступные команды:', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # создаем новую клавиатуру
    kb = telebot.types.InlineKeyboardMarkup()

    # делаем клавиатуру со списком курсов
    if call.data == 'set_mark':
        call_handlers.set_courses_btns(kb)

    # делаем клавиатуру со списком учителей по выбранному курсу
    if 'set_mark' in call.data and 'selected_course' in call.data:
        selected_course = call.data.split('=')[-1]
        call_handlers.set_teachers_btns(kb, selected_course)

    if 'set_mark&selected_teacher' in call.data:
        selected_teacher = call.data.split('=')[-1]
        call_handlers.set_action_btns(kb, selected_teacher, call, bot)

    if 'set_mark&action' in call.data:
        selected_teacher = call.data.split('=')[-1]
        action = call.data[16]
        call_handlers.set_mark_handle_action(selected_teacher, action, call,
                                             bot, kb)

    if 'teachers_rate' == call.data:
        call_handlers.show_rate(kb, call, bot)

    # заменяем старую клавиатуру на новую
    bot.edit_message_reply_markup(call.message.chat.id,
                                  call.message.id,
                                  reply_markup=kb)


bot.polling(non_stop=True, interval=1)
