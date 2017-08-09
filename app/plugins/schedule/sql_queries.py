current_lesson = (
    'SELECT subject, number, time_begin, time_end '
    'FROM Schedule sch '
    'LEFT JOIN Subjects subj ON subj.id = sch.subject '
    'LEFT JOIN Chats ch ON ch.[group] = subj.[group] '
    'WHERE ch.id = {chat_id} AND '
    'time_begin <= "{current_time}" AND '
    'time_end BETWEEN "{current_time}" AND "{finish_time}" AND '
    'week_day = {day} AND '
    'week_parity IN ({parity}, -1) '
    'ORDER BY number')

next_lesson = (
    'SELECT subject, number, time_begin, time_end '
    'FROM Schedule sch '
    'LEFT JOIN Subjects subj ON subj.id = sch.subject '
    'LEFT JOIN Chats ch ON ch.[group] = subj.[group] '
    'WHERE ch.id = {chat_id} AND '
    'time_begin > "{current_time}" AND '
    'week_day = {day} AND '
    'week_parity IN ({parity}, -1) '
    'ORDER BY number')

day_lessons = (
    'SELECT subject, number, time_begin, time_end '
    'FROM Schedule sch '
    'LEFT JOIN Subjects subj ON subj.id = sch.subject '
    'LEFT JOIN Chats ch ON ch.[group] = subj.[group] '
    'WHERE ch.id = {chat_id} AND '
    'week_day = {day} AND '
    'week_parity IN ({parity}, -1) '
    'ORDER BY number')

subject_info = (
    'SELECT name, classroom, teacher FROM Subjects WHERE id = {id}')

teacher_name_by_id = (
    'SELECT surname, name, patronymic FROM Teachers WHERE id = {id}')
