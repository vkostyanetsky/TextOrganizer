# каждая суббота
# каждая сб
# каждую субботу
# каждую сб
#
# каждая суббота, начиная с 29.12.1983
# каждая суббота с 29.12.1983

import re
import modules.conditions as conditions

def is_task_current(task, date):
   
    def is_type_correct():

        pattern = '(каждая суббота|каждая сб|каждую субботу|каждую сб).*'
        match   = re.match(pattern, task['recurrence'])

        return match != None

    def is_date_correct():

        is_saturday = date.strftime('%a') == 'Sat'

        return is_saturday and conditions.is_task_started(task, date)

    result = None
    
    if is_type_correct():
        result = is_date_correct()
    
    return result