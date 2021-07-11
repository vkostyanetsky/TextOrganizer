# каждое воскресенье
# каждое вс

def is_type(task):

    return task['recurrence'] == 'каждое воскресенье' or task['recurrence'] == 'каждое вс'

def is_relevant_for_date(task, date):

    return date.strftime('%a') == "Sun"