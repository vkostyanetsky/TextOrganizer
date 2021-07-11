# каждый будний день
# по будням

def is_type(task):

    return task['recurrence'] == 'каждый будний день' or task['recurrence'] == 'по будням'

def is_relevant_for_date(task, date):

    weekday = date.weekday()

    return weekday >=0 and weekday <=4