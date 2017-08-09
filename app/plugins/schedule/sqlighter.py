import datetime
import sqlite3
import os

from . import sql_queries, week_info

dir_path = os.path.dirname(os.path.abspath(__file__))
db_name = 'schedule.db'
db_path = os.path.join(dir_path, db_name)


class SQLighter:
    """ Простая обертка над сырыми SQL запросами """

    def __init__(self):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def current_lesson(self):
        """ Возвращает текущую пару """

        dt_current_time = datetime.datetime.now()
        dt_finish_time = dt_current_time + week_info.lesson_length

        current_time = dt_current_time.strftime(week_info.time_format)
        finish_time = dt_finish_time.strftime(week_info.time_format)
        day = week_info.week_day()
        parity = week_info.week_parity()

        query = sql_queries.current_lesson.format(current_time=current_time,
                                                  finish_time=finish_time,
                                                  day=day,
                                                  parity=parity)

        lessons = self.execute(query)
        return None if (len(lessons) == 0) else lessons[0]

    def next_lesson(self):
        """ Возвращает следующую пару текущего дня """

        current_time = datetime.datetime.now().strftime(week_info.time_format)
        day = week_info.week_day()
        parity = week_info.week_parity()

        query = sql_queries.next_lesson.format(current_time=current_time,
                                               day=day,
                                               parity=parity)

        lessons = self.execute(query)
        return None if (len(lessons) == 0) else lessons[0]

    def first_lesson_of_day(self, day):
        """ Возвращает первую пару дня с учетом четности недели """

        parity = week_info.week_parity_day(day)

        query = sql_queries.day_lessons.format(day=day,
                                               parity=parity)

        lessons = self.execute(query)
        return None if (len(lessons) == 0) else lessons[0]

    def subject_name(self, id):
        """ Возвращает название предмета по его id """
        query = sql_queries.subject_name_by_id.format(id=id)

        subjects = self.execute(query)
        return '' if (len(subjects) == 0) else subjects[0][0]

    def teacher_full_name(self, id):
        """ Возвращает ФИО препода по id """
        query = sql_queries.teacher_name_by_id.format(id=id)

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
