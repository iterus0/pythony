current_lesson = (
    'SELECT subject, teacher, classroom, time_begin, time_end, number '
    'FROM Schedule sch '
    'LEFT JOIN Subjects subj ON subj.id = sch.subject '
    'LEFT JOIN Teachers t ON t.id = sch.teacher '
    'WHERE time_begin <= "{current_time}" AND '
    'time_end BETWEEN "{current_time}" AND "{finish_time}" AND '
    'week_day = {day} AND '
    'week_parity IN ({parity}, -1) '
    'ORDER BY number')

next_lesson = (
    'SELECT subject, teacher, classroom, time_begin, time_end, number '
    'FROM Schedule sch '
    'LEFT JOIN Subjects subj ON subj.id = sch.subject '
    'LEFT JOIN Teachers t ON t.id = sch.teacher '
    'WHERE time_begin > "{current_time}" AND '
    'week_day = {day} AND '
    'week_parity IN ({parity}, -1) '
    'ORDER BY number')

day_lessons = (
    'SELECT subject, teacher, classroom, time_begin, time_end, number '
    'FROM Schedule sch '
    'LEFT JOIN Subjects subj ON subj.id = sch.subject '
    'LEFT JOIN Teachers t ON t.id = sch.teacher '
    'WHERE week_day = {day} AND '
    'week_parity IN ({parity}, -1) '
    'ORDER BY number')

subject_name_by_id = (
    'SELECT name FROM Subjects WHERE id = {id}')

teacher_name_by_id = (
    'SELECT surname, name, patronymic FROM Teachers WHERE id = {id}')
