# каждый день

def is_type(task):

    return task['recurrence'] == 'каждый день'

def is_relevant_for_date(task, date):

    return True