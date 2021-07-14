# каждый вторник
# каждый вт

def is_task_current(task, date):
   
    result          = None
    type_is_correct = task['recurrence'] == 'каждый вторник' or task['recurrence'] == 'каждый вт'
    
    if type_is_correct:
        result = date.strftime('%a') == "Tue"
    
    return result