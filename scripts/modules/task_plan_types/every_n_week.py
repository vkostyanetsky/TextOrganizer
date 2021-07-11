# каждые X недели по Y
# каждая X неделя по Y
#
# Пример: каждая 2 неделя по Сб

import datetime

def is_type(task):

    parts = task['recurrence'].split(' ')

    return (parts[0] == 'каждые' or parts[0] == 'каждая') and (parts[2] == 'недели' or parts[2] == 'неделя') and parts[3] == 'по'

def is_relevant_for_date(task, date):

    def is_day_of_week(date, weekday_abbreviation):

        weekday_abbreviation_for_date = date.strftime('%a')

        return weekday_abbreviation_for_date == weekday_abbreviation

    def occurs_when():

        def week_number():

            return int(when[1])

        def week_day():

            if when[4] == 'пн' or when[4] == 'понедельникам':
                return 'Mon'
            elif when[4] == 'вт' or when[4] == 'вторникам':
                return 'Tue'
            elif when[4] == 'ср' or when[4] == 'средам':
                return 'Wed'
            elif when[4] == 'чт' or when[4] == 'четвергам':
                return 'Thu'
            elif when[4] == 'пт' or when[4] == 'пятницам':
                return 'Fri'                
            elif when[4] == 'сб' or when[4] == 'субботам':
                return 'Sat'
            elif when[4] == 'вс' or when[4] == 'воскресеньям':
                return 'Sun'
            else:
                return ''

        when = occurs[0].strip().split(' ')

        return {
            'week_number':  week_number(),
            'week_day':     week_day()
        }

    def occurs_from():

        date_string = occurs[1].split(' ')
        date_string = date_string[len(date_string) - 1]
        date_string = date_string.strip().split('.')

        day     = int(date_string[0])
        month   = int(date_string[1])
        year    = int(date_string[2])

        return datetime.datetime(year, month, day)

    def is_match():
                
        return is_day_of_week(occurs_from, occurs_when['week_day'])

    def is_equal():

        if date < occurs_from:
            return False
        elif date == occurs_from:
            return True

        date_to_occur   = occurs_from
        week_number     = 1

        while date_to_occur <= date:
                    
            if is_day_of_week(date_to_occur, occurs_when['week_day']) and week_number == occurs_when['week_number']:

                if date_to_occur == date:
                    return True
                else:
                    week_number = 0

            date_to_occur   += datetime.timedelta(days = 7)
            week_number     += 1

        return False

    result = False

    occurs = task['recurrence'].split(',')

    occurs_when = occurs_when()
    occurs_from = occurs_from()

    if is_match():                            
        result = is_equal()
    else:
        result = False

    return result
