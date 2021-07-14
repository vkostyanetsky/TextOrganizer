# каждое воскресенье
# каждое вс

def is_task_current(task, date):
   
    result          = None
    type_is_correct = task['recurrence'] == 'каждое воскресенье' or task['recurrence'] == 'каждое вс'
    
    if type_is_correct:
        result = date.strftime('%a') == "Sun"
    
    return result