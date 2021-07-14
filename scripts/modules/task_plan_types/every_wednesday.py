# каждая среда
# каждая ср
# каждую среду
# каждую ср

def is_task_current(task, date):
   
    result          = None
    type_is_correct = task['recurrence'] == 'каждая среда' or task['recurrence'] == 'каждая ср' or task['recurrence'] == 'каждую среду' or task['recurrence'] == 'каждую ср'
    
    if type_is_correct:
        result = date.strftime('%a') == "Wed"
    
    return result