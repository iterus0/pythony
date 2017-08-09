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


def week_parity_day(day):
    current_day = week_day()
    current_parity = week_parity()
    next_parity = (current_parity + 1) % 2

    return current_parity if (day >= current_day) else next_parity


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

        str_current_time = datetime.datetime.now().strftime(time_format)

        query = ('SELECT subject, teacher, classroom, time_begin, time_end, number FROM Schedule sch '
                 'LEFT JOIN Subjects subj ON subj.id = sch.subject '
                 'LEFT JOIN Teachers t ON t.id = sch.teacher '
                 'WHERE time_begin > "' + str_current_time + '" AND '
                 'week_day = ' + str(week_day()) + ' AND '
                 'week_parity IN (' + str(week_parity()) + ', -1) '
                 'ORDER BY number')

        lessons = self.execute(query)
        return [] if (len(lessons) == 0) else lessons

    def first_lesson_of_day(self, day):
        parity = week_parity_day(day)

        query = ('SELECT subject, teacher, classroom, time_begin, time_end, number FROM Schedule sch '
                 'LEFT JOIN Subjects subj ON subj.id = sch.subject '
                 'LEFT JOIN Teachers t ON t.id = sch.teacher '
                 'WHERE week_day = ' + str(day) + ' AND '
                 'week_parity IN (' + str(parity) + ', -1) '
                 'ORDER BY number')

        lessons = self.execute(query)
        return [] if (len(lessons) == 0) else lessons

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
