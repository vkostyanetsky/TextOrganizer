import re
import datetime

def is_task_started(task, date):

    result = True

    regexp = '.*(, начиная с| с) ([0-9]{1,2}.[0-9]{1,2}.[0-9]{4})$'
    groups = re.match(regexp, task['recurrence'])

    if groups != None:

        start_date  = datetime.datetime.strptime(groups[2], '%d.%m.%Y')
        result      = date >= start_date

    return result