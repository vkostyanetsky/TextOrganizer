# каждая пятница
# каждая пт
# каждую пятницу
# каждую пт

def is_type(task):

    return task['recurrence'] == 'каждая пятница' or task['recurrence'] == 'каждая пт' or task['recurrence'] == 'каждую пятницу' or task['recurrence'] == 'каждую пт'

def is_relevant_for_date(task, date):

    return date.strftime('%a') == "Fri"