# каждый месяц, X день (где X — номер дня в месяце)
# каждый месяц, последний день

import datetime

def is_task_current(task, date):
   
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

    type_is_correct = task['recurrence'].startswith('каждый месяц, ')
    
    if type_is_correct:
        result = day_number() == current_day_number()
    
    return result