from app import bot
from .sqlighter import SQLighter
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


def format_lesson(lesson):
    db = SQLighter(db_path)

    l_name = db.subject_name(lesson[0])
    l_teacher = db.teacher_full_name(lesson[1])
    l_aud = lesson[2]
    finish_hour, finish_minute = [int(n) for n in lesson[4].split(':')]
    l_left = remaining_time(finish_hour, finish_minute)

    db.close()
    return ('Предмет: {name}\n'
            'Аудитория: {aud}\n'
            'Препод: {teacher}\n'
            'До конца пары осталось {left}').format(name=l_name,
                                                    aud=l_aud,
                                                    teacher=l_teacher,
                                                    left=l_left)


@bot.message_handler(commands=["rasp"])
def get_current_lesson(message):
    db = SQLighter(db_path)

    msg = ""
    lessons = db.current_lesson()

    if len(lessons) == 0:
        msg += 'Сейчас пары нет'

    elif len(lessons) == 1:
        msg += format_lesson(lessons[0])

    else:
        msg += '[!] Произошла ошибка'

    db.close()
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["next"])
def get_next_lesson(message):
    db = SQLighter(db_path)
    msg = "Следующая пара"
    db.close()
    bot.send_message(message.chat.id, msg)


print("Schedule plugin loaded.")
