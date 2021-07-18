# каждый день
# каждый день с 29.12.1983
# каждый день, начиная с 29.12.1983

import modules.conditions as conditions

def is_task_current(task, date):

    def is_type_correct():

        return task['condition'].startswith('каждый день')

    def is_date_correct():

        return conditions.is_task_started(task, date)

    result = None    

    if is_type_correct():
        result = is_date_correct()

    return result