# каждая суббота
# каждая сб
# каждую субботу
# каждую сб

def is_type(task):

    return task['recurrence'] == 'каждая суббота' or task['recurrence'] == 'каждая сб' or task['recurrence'] == 'каждую субботу' or task['recurrence'] == 'каждую сб'

def is_relevant_for_date(task, date):

    return date.strftime('%a') == "Sat"