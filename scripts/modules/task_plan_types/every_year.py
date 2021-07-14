# каждый год, 16 декабря

def is_task_current(task, date):

    def year_day():

        return int(task_date[0])

    def year_month():

        if task_date[1] == 'январь':
            return 1
        elif task_date[1] == 'февраль':
            return 2
        elif task_date[1] == 'март':
            return 3
        elif task_date[1] == 'апрель':
            return 4
        elif task_date[1] == 'май':
            return 5
        elif task_date[1] == 'июнь':
            return 6
        elif task_date[1] == 'июль':
            return 7
        elif task_date[1] == 'август':
            return 8
        elif task_date[1] == 'сентябрь':
            return 9
        elif task_date[1] == 'октябрь':
            return 10
        elif task_date[1] == 'ноябрь':
            return 11
        elif task_date[1] == 'декабрь':
            return 12

    result          = None
    type_is_correct = task['recurrence'].startswith('каждый год')
    
    if type_is_correct:
    
        parts = task['recurrence'].split(',')

        task_date = parts[1].strip()
        task_date = task_date.split(' ')
                    
        result = date.day == year_day() and date.month == year_month()
    
    return result