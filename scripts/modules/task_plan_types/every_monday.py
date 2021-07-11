# каждый понедельник
# каждый пн

def is_type(task):

    return task['recurrence'] == 'каждый понедельник' or task['recurrence'] == 'каждый пн'

def is_relevant_for_date(task, date):

    return date.strftime('%a') == "Mon"