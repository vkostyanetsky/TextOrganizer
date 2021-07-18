# каждый вторник
# каждый вт
#
# каждый вторник, начиная с 29.12.1983
# каждый вторник с 29.12.1983

import re
import modules.conditions as conditions

def is_task_current(task, date):
   
    def is_type_correct():

        pattern = '(каждый вторник|каждый вт).*'
        match   = re.match(pattern, task['condition'])

        return match != None

    def is_date_correct():

        is_thursday = date.strftime('%a') == 'Tue'

        return is_thursday and conditions.is_task_started(task, date)

    result = None
    
    if is_type_correct():
        result = is_date_correct()
    
    return result