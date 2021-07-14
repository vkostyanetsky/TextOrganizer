# каждый понедельник
# каждый пн

def is_task_current(task, date):
   
    result          = None
    type_is_correct = task['recurrence'] == 'каждый понедельник' or task['recurrence'] == 'каждый пн'
    
    if type_is_correct:
        result = date.strftime('%a') == "Mon"
    
    return result