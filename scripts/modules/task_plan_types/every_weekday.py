# каждый будний день
# по будням

def is_task_current(task, date):
   
    result          = None
    type_is_correct = task['recurrence'] == 'каждый будний день' or task['recurrence'] == 'по будням'
    
    if type_is_correct:
    
        number = date.weekday()
        result = number >=0 and number <=4
    
    return result