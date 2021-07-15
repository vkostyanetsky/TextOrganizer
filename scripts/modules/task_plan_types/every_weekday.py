# каждый будний день
# по будням
#
# каждый будний день, начиная с 29.12.1983
# каждый будний день с 29.12.1983

import re
import modules.conditions as conditions

def is_task_current(task, date):
   
    def is_type_correct():

        pattern = '(каждый будний день|по будням).*'
        match   = re.match(pattern, task['recurrence'])

        return match != None

    result = None
    
    if is_type_correct():
    
        number = date.weekday()
        is_day = number >=0 and number <=4
        
        result = is_day and conditions.is_task_started(task, date)
    
    return result