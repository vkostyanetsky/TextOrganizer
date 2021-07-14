# каждая пятница
# каждая пт
# каждую пятницу
# каждую пт

def is_task_current(task, date):
   
    result          = None
    type_is_correct = task['recurrence'] == 'каждая пятница' or task['recurrence'] == 'каждая пт' or task['recurrence'] == 'каждую пятницу' or task['recurrence'] == 'каждую пт'
    
    if type_is_correct:
        result = date.strftime('%a') == "Fri"
    
    return result