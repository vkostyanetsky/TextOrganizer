# каждая среда
# каждая ср
# каждую среду
# каждую ср

def is_type(task):

    return task['recurrence'] == 'каждая среда' or task['recurrence'] == 'каждая ср' or task['recurrence'] == 'каждую среду' or task['recurrence'] == 'каждую ср'

def is_relevant_for_date(task, date):

    return date.strftime('%a') == "Wed"