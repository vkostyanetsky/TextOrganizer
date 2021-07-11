# каждый 3 день, начиная с 16.01.2021
# каждые 2 дня с 29.12.1983

import re
import datetime

def get_regexp():

    return '(каждый|каждые) ([0-9]+) (день|дня)(, начиная с| с) ([0-9]{1,2}.[0-9]{1,2}.[0-9]{4})'

def is_type(task):

    regexp = get_regexp()
    string = task['recurrence']
    groups = re.match(regexp, string)

    return groups != None

def is_relevant_for_date(task, date):

    regexp = get_regexp()
    string = task['recurrence']
    groups = re.match(regexp, string)

    event_day_number = int(groups[2])
    event_start_date = datetime.datetime.strptime(groups[5], "%d.%m.%Y")

    if date >= event_start_date:

        days    = abs(date - event_start_date).days
        result  = days % event_day_number == 0

    else:

        result = False

    return result