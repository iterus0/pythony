from .sqlighter import SQLighter
from . import week_info


def format_lesson(lesson):
    db = SQLighter()

    subject_id = lesson[0]
    l_number = lesson[1]
    l_begin = lesson[2]
    l_end = lesson[3]

    subject = db.subject_info(subject_id)

    l_name = subject[0]
    l_aud = subject[1]
    teacher_id = subject[2]

    l_teacher = db.teacher_full_name(teacher_id)

    db.close()
    return ('Предмет: {name}\n'
            'Аудитория: {aud}\n'
            'Препод: {teacher}\n'
            'Начало: {begin}\n'
            'Окончание: {end}').format(name=l_name,
                                       aud=l_aud,
                                       teacher=l_teacher,
                                       begin=l_begin,
                                       end=l_end)


def format_lesson_starting(lesson):
    db = SQLighter()

    lesson_begin = lesson[2]
    start_hour, start_minute = [int(n) for n in lesson_begin.split(':')]

    l_left = week_info.remaining_time(start_hour, start_minute)

    reply = format_lesson(lesson)
    reply += '\nДо начала пары осталось {}'.format(l_left)

    db.close()
    return reply


def format_lesson_ending(lesson):
    db = SQLighter()

    lesson_end = lesson[3]
    finish_hour, finish_minute = [int(n) for n in lesson_end.split(':')]

    l_left = week_info.remaining_time(finish_hour, finish_minute)

    reply = format_lesson(lesson)
    reply += '\nДо конца пары осталось {}'.format(l_left)

    db.close()
    return reply
