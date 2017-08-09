from app import bot
from .sqlighter import SQLighter, week_day
import datetime
import math
import os


dir_path = os.path.dirname(os.path.abspath(__file__))
db_name = 'schedule.db'
db_path = os.path.join(dir_path, db_name)


def remaining_time(hour, minute):
    current_time = datetime.datetime.now()
    current_date = current_time.date()
    finish_time = datetime.time(hour=hour, minute=minute)
    finish_dt = datetime.datetime.combine(current_date, finish_time)
    remaining_time = finish_dt - current_time
    remaining_mins = math.ceil(remaining_time.total_seconds() / 60)

    return str(remaining_mins) + ' минут'


def day_name(day):
    week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    return week[day]


def format_lesson(lesson):
    db = SQLighter(db_path)

    l_name = db.subject_name(lesson[0])
    l_teacher = db.teacher_full_name(lesson[1])
    l_aud = lesson[2]
    l_start = lesson[3]
    l_end = lesson[4]

    db.close()
    return ('Предмет: {name}\n'
            'Аудитория: {aud}\n'
            'Препод: {teacher}\n'
            'Начало: {start}\n'
            'Окончание: {end}').format(name=l_name,
                                       aud=l_aud,
                                       teacher=l_teacher,
                                       start=l_start,
                                       end=l_end)


def format_lesson_end(lesson):
    db = SQLighter(db_path)

    finish_hour, finish_minute = [int(n) for n in lesson[4].split(':')]
    l_left = remaining_time(finish_hour, finish_minute)

    response = format_lesson(lesson)
    response += '\nДо конца пары осталось ' + str(l_left)

    db.close()
    return response


def format_lesson_start(lesson):
    db = SQLighter(db_path)

    start_hour, start_minute = [int(n) for n in lesson[4].split(':')]
    l_left = remaining_time(start_hour, start_minute)

    response = format_lesson(lesson)
    response += '\nДо начала пары осталось ' + str(l_left)

    db.close()
    return response


@bot.message_handler(commands=["rasp"])
def get_current_lesson(message):
    db = SQLighter(db_path)

    msg = ""
    lessons = db.current_lesson()

    if len(lessons) == 0:
        msg += 'Сейчас пары нет'

    elif len(lessons) == 1:
        msg += format_lesson_end(lessons[0])

    else:
        msg += '[!] Произошла ошибка'

    db.close()
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["next"])
def get_next_lesson(message):
    db = SQLighter(db_path)

    msg = ""
    lessons = db.next_lesson()

    if len(lessons) == 1:
        msg += "Следующая пара сегодня:\n"
        msg += format_lesson_start(lessons[0])

    else:
        msg += "Сегодня больше нет пар.\n"
        msg += "Следующая пара "

        # ищем следующую первую пару
        day = week_day()
        for offset in range(7):
            day = (day + 1) % 7
            lessons = db.first_lesson_of_day(day)
            if len(lessons) == 1:
                msg += "(" + day_name(day) + "):\n"
                msg += format_lesson(lessons[0])
                break

    db.close()
    bot.send_message(message.chat.id, msg)


print("Schedule plugin loaded.")
