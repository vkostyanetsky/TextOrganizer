# каждые 2 недели по Пн, начиная с 01.01.2021
# каждая 3 неделя по Сб, начиная с 29.19.1983

import re
import datetime

def is_task_current(task, date):
   
    def get_day_of_week(name):

        if name == 'пн' or name == 'понедельникам':
            return 'Mon'
        elif name == 'вт' or name == 'вторникам':
            return 'Tue'
        elif name == 'ср' or name == 'средам':
            return 'Wed'
        elif name == 'чт' or name == 'четвергам':
            return 'Thu'
        elif name == 'пт' or name == 'пятницам':
            return 'Fri'                
        elif name == 'сб' or name == 'субботам':
            return 'Sat'
        elif name == 'вс' or name == 'воскресеньям':
            return 'Sun'
        else:
            return ''

    def get_event_start_date(day_of_week_string, start_date_string):

        event_day_of_week = get_day_of_week(day_of_week_string)

        event_start_date                = datetime.datetime.strptime(start_date_string, "%d.%m.%Y")
        event_start_date_day_of_week    = event_start_date.strftime('%a')

        while event_day_of_week != event_start_date_day_of_week:

            event_start_date               += datetime.timedelta(days = 1)
            event_start_date_day_of_week    = event_start_date.strftime('%a')

        return event_start_date

    result = None
    regexp = '(каждый|каждые) ([0-9]+) (недели|неделя) по ([А-Яа-я]+)(, начиная с| с) ([0-9]{1,2}.[0-9]{1,2}.[0-9]{4})'
    groups = re.match(regexp, task['condition'])

    type_is_correct = groups != None
    
    if type_is_correct:

        event_week_number   = int(groups[2])    
        event_start_date    = get_event_start_date(groups[4], groups[6])

        if date >= event_start_date:

            weeks   = abs(date - event_start_date).days / 7
            result  = weeks % event_week_number == 0

        else:

            result = False
    
    return result