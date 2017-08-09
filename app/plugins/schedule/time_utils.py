import datetime
import math


lesson_length = datetime.timedelta(hours=1, minutes=30)
time_format = '%H:%M'


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
