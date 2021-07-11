# DD.MM.YYYY (DD — номер дня, MM — номер месяца, YYYY — номер года)

def is_type(task):

    return task['recurrence'].count('.') == 2

def is_relevant_for_date(task, date):

    parts = task['recurrence'].split('.')

    day     = int(parts[0])
    month   = int(parts[1])
    year    = int(parts[2])

    task_date = task['datetime'].replace(year = year, month = month, day = day, hour = 0, minute = 0, second = 0, microsecond = 0)

    if task_date < date:
        task['outdated'] = True

    return date == task_date