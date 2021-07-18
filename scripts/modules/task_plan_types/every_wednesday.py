# каждая среда
# каждая ср
# каждую среду
# каждую ср
#
# каждая среда, начиная с 29.12.1983
# каждая среда с 29.12.1983

import re
import modules.conditions as conditions

def is_task_current(task, date):
   
    def is_type_correct():

        pattern = '(каждая среда|каждая ср|каждую среду|каждую ср).*'
        match   = re.match(pattern, task['condition'])

        return match != None

    def is_date_correct():

        is_wednesday = date.strftime('%a') == 'Wed'

        return is_wednesday and conditions.is_task_started(task, date)

    result = None
    
    if is_type_correct():
        result = is_date_correct()
    
    return result