import datetime
import sqlite3
import os

from . import week_info

dir_path = os.path.dirname(os.path.abspath(__file__))
db_name = 'schedule.db'
db_path = os.path.join(dir_path, db_name)


class SQLighter:
    """ Простая обертка над сырыми SQL запросами """

    def __init__(self):
        print("Opening db at", db_path)
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def current_lesson(self):
        """ Возвращает текущую пару """

        current_time = datetime.datetime.now()
        finish_time = current_time + week_info.lesson_length

        str_current_time = current_time.strftime(week_info.time_format)
        str_finish_time = finish_time.strftime(week_info.time_format)

        query = ('SELECT subject, teacher, classroom, time_begin, time_end, number FROM Schedule sch '
                 'LEFT JOIN Subjects subj ON subj.id = sch.subject '
                 'LEFT JOIN Teachers t ON t.id = sch.teacher '
                 'WHERE time_begin <= "' + str_current_time + '" AND '
                 'time_end BETWEEN "' + str_current_time + '" AND "' + str_finish_time + '" AND '
                 'week_day = ' + str(week_info.week_day()) + ' AND '
                 'week_parity IN (' + str(week_info.week_parity()) + ', -1) '
                 'ORDER BY number')

        lessons = self.execute(query)
        return None if (len(lessons) == 0) else lessons[0]

    def next_lesson(self):
        """ Возвращает следующую пару текущего дня """

        str_current_time = datetime.datetime.now().strftime(week_info.time_format)

        query = ('SELECT subject, teacher, classroom, time_begin, time_end, number FROM Schedule sch '
                 'LEFT JOIN Subjects subj ON subj.id = sch.subject '
                 'LEFT JOIN Teachers t ON t.id = sch.teacher '
                 'WHERE time_begin > "' + str_current_time + '" AND '
                 'week_day = ' + str(week_info.week_day()) + ' AND '
                 'week_parity IN (' + str(week_info.week_parity()) + ', -1) '
                 'ORDER BY number')

        lessons = self.execute(query)
        return None if (len(lessons) == 0) else lessons[0]

    def first_lesson_of_day(self, day):
        """ Возвращает первую пару дня с учетом четности недели """
        parity = week_info.week_parity_day(day)

        query = ('SELECT subject, teacher, classroom, time_begin, time_end, number FROM Schedule sch '
                 'LEFT JOIN Subjects subj ON subj.id = sch.subject '
                 'LEFT JOIN Teachers t ON t.id = sch.teacher '
                 'WHERE week_day = ' + str(day) + ' AND '
                 'week_parity IN (' + str(parity) + ', -1) '
                 'ORDER BY number')

        lessons = self.execute(query)
        return None if (len(lessons) == 0) else lessons[0]

    def subject_name(self, id):
        """ Возвращает название предмета по его id """
        query = 'SELECT name FROM Subjects WHERE id = ' + str(id)
        subjects = self.execute(query)
        return '' if (len(subjects) == 0) else subjects[0][0]

    def teacher_full_name(self, id):
        """ Возвращает ФИО препода по id """
        query = 'SELECT surname, name, patronymic FROM Teachers WHERE id = ' + str(id)
        teachers = self.execute(query)
        return '' if (len(teachers) == 0) else ' '.join(teachers[0])

    def execute(self, request):
        """ Выполняет запрос к базе данных """
        print(request)
        with self.connection:
            return self.cursor.execute(request).fetchall()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
