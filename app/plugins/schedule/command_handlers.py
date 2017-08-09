from app import bot
from .sqlighter import SQLighter
from . import lesson_format, week_info


@bot.message_handler(commands=["rasp"])
def get_current_lesson(message):
    chat_id = message.chat.id
    db = SQLighter()

    msg = ""
    lesson = db.current_lesson(chat_id)

    if lesson is not None:
        msg += lesson_format.format_lesson_end_left(lesson)

    else:
        msg += 'Сейчас пары нет'

    db.close()
    bot.send_message(chat_id, msg)


@bot.message_handler(commands=["next"])
def get_next_lesson(message):
    chat_id = message.chat.id
    db = SQLighter()

    msg = ""
    lesson = db.next_lesson(chat_id)

    if lesson is not None:
        msg += "Следующая пара сегодня:\n"
        msg += lesson_format.format_lesson_start_left(lesson)

    else:
        msg += "Сегодня больше нет пар.\n"
        msg += "Следующая пара "

        # ищем следующую первую пару
        day = week_info.week_day()
        for offset in range(7):
            day = (day + 1) % 7
            lesson = db.first_lesson_of_day(chat_id, day)
            if lesson is not None:
                msg += "(" + week_info.day_name(day) + "):\n"
                msg += lesson_format.format_lesson(lesson)
                break

    db.close()
    bot.send_message(chat_id, msg)
