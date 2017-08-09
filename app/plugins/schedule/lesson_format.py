from .sqlighter import SQLighter
from . import week_info


def format_lesson(lesson):
    db = SQLighter()

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
    db = SQLighter()

    finish_hour, finish_minute = [int(n) for n in lesson[4].split(':')]
    l_left = week_info.remaining_time(finish_hour, finish_minute)

    response = format_lesson(lesson)
    response += '\nДо конца пары осталось ' + str(l_left)

    db.close()
    return response


def format_lesson_start(lesson):
    db = SQLighter()

    start_hour, start_minute = [int(n) for n in lesson[3].split(':')]
    l_left = week_info.remaining_time(start_hour, start_minute)

    response = format_lesson(lesson)
    response += '\nДо начала пары осталось ' + str(l_left)

    db.close()
    return response
