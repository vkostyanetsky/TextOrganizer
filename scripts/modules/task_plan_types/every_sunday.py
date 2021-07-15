# каждое воскресенье
# каждое вс
#
# каждое воскресенье, начиная с 29.12.1983
# каждое воскресенье с 29.12.1983

import re
import modules.conditions as conditions

def is_task_current(task, date):
   
    def is_type_correct():

        pattern = '(каждое воскресенье|каждое вс).*'
        match   = re.match(pattern, task['recurrence'])

        return match != None

    def is_date_correct():

        is_sunday = date.strftime('%a') == 'Sun'

        return is_sunday and conditions.is_task_started(task, date)

    result = None
    
    if is_type_correct():
        result = is_date_correct()
    
    return result