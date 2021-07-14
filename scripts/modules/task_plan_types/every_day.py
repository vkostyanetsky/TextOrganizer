# каждый день

def is_task_current(task, date):

    result          = None    
    type_is_correct = task['recurrence'] == 'каждый день'

    if type_is_correct:
        result = True

    return result