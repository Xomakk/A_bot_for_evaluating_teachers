import json
import telebot


def set_courses_btns(kb):
    with open('./db/courses.json', 'r', encoding='UTF-8') as db_file:
        courses = json.load(db_file)

    for key, course_name in courses.items():
        btn = telebot.types.InlineKeyboardButton(
            course_name, callback_data=f'set_mark&selected_course={key}')
        kb.row(btn)


def set_teachers_btns(kb, selected_course):
    with open('./db/teachers.json', 'r', encoding='UTF-8') as db_file:
        teachers = json.load(db_file)

    selected_teachers = []
    for id, t in teachers.items():
        if selected_course in t.get('courses'):
            selected_teachers.append((id, t))

    for id, t in selected_teachers:
        btn = telebot.types.InlineKeyboardButton(
            f'{t.get("name")} {t.get("lastname")}',
            callback_data=f'set_mark&selected_teacher={id}')
        kb.row(btn)


def set_action_btns(kb, selected_teacher, call, bot):
    with open('./db/teachers.json', 'r', encoding='UTF-8') as db_file:
        teachers = json.load(db_file)

    teacher = teachers.get(selected_teacher)

    bot.edit_message_text(
        f'{teacher.get("name")} {teacher.get("lastname")} \n'
        f'Лайков: {teacher.get("likes")}\n'
        f'Дизлайков: {teacher.get("dislikes")}\n', call.message.chat.id,
        call.message.id)
    btn_like = telebot.types.InlineKeyboardButton(
        'Лайк',
        callback_data=f'set_mark&action=1/selected_teacher={selected_teacher}')
    btn_dislike = telebot.types.InlineKeyboardButton(
        'Дизлайк',
        callback_data=f'set_mark&action=0/selected_teacher={selected_teacher}')
    kb.row(btn_like, btn_dislike)


def set_mark_handle_action(selected_teacher, action, call, bot, kb):
    with open('./db/teachers.json', 'r', encoding='UTF-8') as db_file:
        teachers = json.load(db_file)

    t = teachers.get(selected_teacher)

    if action == '1':
        t['likes'] = t['likes'] + 1
    else:
        t['dislikes'] = t['dislikes'] + 1

    with open('./db/teachers.json', 'w', encoding='UTF-8') as db_file:
        json.dump(teachers, db_file, ensure_ascii=False)

    bot.edit_message_text('Доступные команды:', call.message.chat.id,
                          call.message.id)

    set_menu_btns(kb)


def set_menu_btns(kb):
    btn_rate = telebot.types.InlineKeyboardButton(
        'Рейтинг преподавателей', callback_data='teachers_rate')
    btn_set_mark = telebot.types.InlineKeyboardButton('Поставить оценку',
                                                      callback_data='set_mark')
    kb.row(btn_rate)
    kb.row(btn_set_mark)


def show_rate(kb, call, bot):
    with open('./db/teachers.json', 'r', encoding='UTF-8') as db_file:
        teachers = json.load(db_file)

    teachers_list = sorted(teachers.values(),
                           key=lambda t: t.get('likes') - t.get('dislikes'),
                           reverse=True)

    text = 'Рейтинг преподавателей: \n\n'
    for teacher in teachers_list:
        text += f"{teacher.get('name')} {teacher.get('lastname')} | {teacher.get('likes') - teacher.get('dislikes')}\n"
    bot.edit_message_text(text, call.message.chat.id, call.message.id)
