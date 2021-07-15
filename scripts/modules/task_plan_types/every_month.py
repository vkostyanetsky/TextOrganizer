# каждый месяц, 5 день
# каждый месяц, последний день
#
# каждый месяц, 5 день, начиная с 29.12.1983
# каждый месяц, 5 день с 29.12.1983

import datetime
import modules.conditions as conditions

def is_task_current(task, date):

    def is_type_correct():

        return task['recurrence'].startswith('каждый месяц, ')

    def day_number():

        def last_day_of_month():

            next_month = date.replace(day = 28) + datetime.timedelta(days = 4)

            return next_month - datetime.timedelta(days = next_month.day)

        recurrence = task['recurrence'].split(' ')
        day_number = recurrence[2]

        if day_number == 'последний':
            day_number = last_day_of_month().day

        return int(day_number)

    def current_day_number():

        day_number = date.strftime('%d')

        return int(day_number)

    result = None
    
    if is_type_correct():

        is_day = day_number() == current_day_number()
        result = is_day and conditions.is_task_started(task, date)
    
    return result