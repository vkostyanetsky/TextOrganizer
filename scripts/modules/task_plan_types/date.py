# DD.MM.YYYY (DD — номер дня, MM — номер месяца, YYYY — номер года)

import re
import datetime

def is_task_current(task, date):
   
    result = None
    groups = re.match('([0-9]{1,2}).([0-9]{1,2}).([0-9]{4})', task['recurrence'])
    
    if groups != None:
        
        task_date_year  = int(groups[3])
        task_date_month = int(groups[2])
        task_date_day   = int(groups[1])
        task_date       = datetime.datetime(task_date_year, task_date_month, task_date_day)

        task['outdated'] = task_date < date

        result = date == task_date
    
    return result