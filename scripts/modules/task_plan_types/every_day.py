# каждый день

def is_task_current(task, date):

    result = None
    
    if task['recurrence'] == 'каждый день':
        result = True

    return result