import datetime
import sqlite3


lesson_length = datetime.timedelta(hours=1, minutes=30)
time_format = '%H:%M'


def week_parity():
    current_time = datetime.datetime.today()
    week_number = current_time.strftime('%W')
    return (int(week_number) + 1) % 2


def week_day():
    current_time = datetime.datetime.today()
    return current_time.weekday()


class SQLighter:
    """ Простая обертка над сырыми SQL запросами """

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def current_lesson(self):
        """ Возвращает текущую пару """

        current_time = datetime.datetime.now()
        finish_time = current_time + lesson_length

        str_current_time = current_time.strftime(time_format)
        str_finish_time = finish_time.strftime(time_format)

        query = ('SELECT subject, teacher, classroom, time_begin, time_end, number FROM Schedule sch '
                 'LEFT JOIN Subjects subj ON subj.id = sch.subject '
                 'LEFT JOIN Teachers t ON t.id = sch.teacher '
                 'WHERE time_begin <= "' + str_current_time + '" AND '
                 'time_end BETWEEN "' + str_current_time + '" AND "' + str_finish_time + '" AND '
                 'week_day = ' + str(week_day()) + ' AND '
                 'week_parity IN (' + str(week_parity()) + ', -1)')

        return self.execute(query)

    def next_lesson(self):
        """ Возвращает следующую пару текущего дня """

        lessons = self.current_lesson()

        if len(lessons) == 1:
            lesson = lessons[0]
            lesson_number = lesson[5]
            next_lesson_number = lesson_number + 1

            query = ('SELECT subject, teacher, classroom, time_begin, time_end, number FROM Schedule sch '
                     'LEFT JOIN Subjects subj ON subj.id = sch.subject '
                     'LEFT JOIN Teachers t ON t.id = sch.teacher '
                     'WHERE number = ' + str(next_lesson_number) + ' AND '
                     'week_day = ' + str(week_day()) + ' AND '
                     'week_parity IN (' + str(week_parity()) + ', -1)')

            return self.execute(query)

        else:
            return []

    def subject_name(self, id):
        query = 'SELECT name FROM Subjects WHERE id = ' + str(id)
        return self.execute(query)[0][0]

    def teacher_full_name(self, id):
        query = 'SELECT surname, name, patronymic FROM Teachers WHERE id = ' + str(id)
        return ' '.join(self.execute(query)[0])

    def execute(self, request):
        """ Выполняет запрос к базе данных """
        print(request)
        with self.connection:
            return self.cursor.execute(request).fetchall()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
