# каждая суббота
# каждая сб
# каждую субботу
# каждую сб

def is_task_current(task, date):
   
    result          = None
    type_is_correct = task['recurrence'] == 'каждая суббота' or task['recurrence'] == 'каждая сб' or task['recurrence'] == 'каждую субботу' or task['recurrence'] == 'каждую сб'
    
    if type_is_correct:
        result = date.strftime('%a') == "Sat"
    
    return result