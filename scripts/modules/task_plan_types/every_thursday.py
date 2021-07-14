# каждый четверг
# каждый чт

def is_task_current(task, date):
   
    result          = None
    type_is_correct = task['recurrence'] == 'каждый четверг' or task['recurrence'] == 'каждый чт'
    
    if type_is_correct:
        result = date.strftime('%a') == "Thu"
    
    return result