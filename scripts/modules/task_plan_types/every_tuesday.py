# каждый вторник
# каждый вт

def is_type(task):

    return task['recurrence'] == 'каждый вторник' or task['recurrence'] == 'каждый вт'

def is_relevant_for_date(task, date):

    return date.strftime('%a') == "Tue"