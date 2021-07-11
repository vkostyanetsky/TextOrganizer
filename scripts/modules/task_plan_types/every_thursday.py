# каждый четверг
# каждый чт

def is_type(task):

    return task['recurrence'] == 'каждый четверг' or task['recurrence'] == 'каждый чт'

def is_relevant_for_date(task, date):

    return date.strftime('%a') == "Thu"