import os
import shutil
import datetime
import winsound

import modules.yaml_wrapper as yaml_wrapper
import modules.tasks_reader as tasks_reader
import modules.tasks_writer as tasks_writer
import modules.common_logic as common_logic

def copy_current_tasks_file_to_history():

    def get_history_filename():
        
        result = get_date_string(parameters['last_date'])
        
        return "{}.md".format(result)
    
    history_filename = get_history_filename()
    history_filepath = os.path.join(paths['history_tasks_dirpath'], history_filename)

    if os.path.exists(history_filepath):

        print("Текущий день уже сохранен в истории!")
        return False

    shutil.copyfile(paths['current_tasks_filepath'], history_filepath)

    return True

def refill_current_tasks_file(postfix = '', include_uncompleted_tasks = True):

    def write_tasks(tasks):

        for task in tasks:

            tasks_writer.write_title(handle, task['title'], '-')
            tasks_writer.write_notes(handle, task)

    def write_planned_tasks():

        # Возможные шаблоны повторения:
        #
        #   каждый день
        #   каждый будний день (или «по будням»)
        #            
        #   каждый месяц, X день (X — номер дня в пределах месяца)
        #                
        #   каждый понедельник
        #   каждый вторник
        #   каждая среда (или «каждую среду»)
        #   каждый четверг
        #   каждая пятница (или «каждую пятница»)
        #   каждая суббота (или «каждую суббота»)
        #   каждое воскресенье
        #
        #   (вместо полных названий дней недели можно использовать сокращения — ПН, ВТ и так далее)
        #
        # Теги: #напоминать, #пропускать

        def get_planned_tasks():

            tasks = tasks_reader.get_tasks_from_file(paths['planned_tasks_filepath'], current_date)
            
            for group in tasks:

                for task in group['tasks']:

                    substrings          = task['title'].split(';')
                    substrings_counter  = len(substrings)

                    is_pattern  = substrings_counter >= 2
                    is_time     = substrings_counter > 2

                    if is_pattern:

                        task['title']           = substrings[0].strip()
                        task['recurrence']      = substrings[1].strip().lower()

                        if is_time:

                            time_substrings = substrings[2].strip().split(':')

                            hour   = int(time_substrings[0])
                            minute = int(time_substrings[1])

                            task['datetime'] = task['datetime'].replace(hour = hour, minute = minute, second = 0, microsecond = 0)

            return tasks

        def is_weekday(date, weekday_abbreviation):

            weekday_abbreviation_for_date = date.strftime('%a')

            return weekday_abbreviation_for_date == weekday_abbreviation
        
        def check_pattern_every_day(task, tasks_for_date):

            result = False

            if task['recurrence'] == 'каждый день':

                tasks_for_date.append(task)
                result = True

            return result

        def check_pattern_every_month(task, tasks_for_date):

            def day_number():

                def last_day_of_month():

                    next_month = current_date.replace(day = 28) + datetime.timedelta(days = 4)

                    return next_month - datetime.timedelta(days = next_month.day)

                recurrence = task['recurrence'].split(' ')
                day_number = recurrence[2]

                if day_number == 'последний':
                    day_number = last_day_of_month().day

                return int(day_number)

            def current_day_number():

                day_number = current_date.strftime('%d')

                return int(day_number)

            result = False

            if task['recurrence'].startswith('каждый месяц, '):

                result = True

                day_number = day_number()

                if day_number == current_day_number():
                    tasks_for_date.append(task)                    

            return result

        def check_pattern_every_monday(task, tasks_for_date):

            def is_match():

                return task['recurrence'] == 'каждый понедельник' or task['recurrence'] == 'каждый пн'

            result = False

            if is_match():
                
                result = True
                 
                if is_weekday(current_date, "Mon"):
                    tasks_for_date.append(task)

            return result                
            
        def check_pattern_every_tuesday(task, tasks_for_date):

            def is_match():

                return task['recurrence'] == 'каждый вторник' or task['recurrence'] == 'каждый вт'

            result = False

            if is_match():
                
                result = True

                if is_weekday(current_date, "Tue"):
                    tasks_for_date.append(task)

            return result

        def check_pattern_every_wednesday(task, tasks_for_date):

            def is_match():

                return task['recurrence'] == 'каждая среда' or task['recurrence'] == 'каждая ср' or task['recurrence'] == 'каждую среду' or task['recurrence'] == 'каждую ср'

            result = False

            if is_match():
                
                result = True
                
                if is_weekday(current_date, "Wed"):
                    tasks_for_date.append(task)                

            return result

        def check_pattern_every_thursday(task, tasks_for_date):

            def is_match():

                return task['recurrence'] == 'каждый четверг' or task['recurrence'] == 'каждый чт'

            result = False

            if is_match():
                
                result = True

                if is_weekday(current_date, "Thu"):
                    tasks_for_date.append(task)

            return result

        def check_pattern_every_friday(task, tasks_for_date):

            def is_match():

                return task['recurrence'] == 'каждая пятница' or task['recurrence'] == 'каждая пт' or task['recurrence'] == 'каждую пятницу' or task['recurrence'] == 'каждую пт'

            result = False

            if is_match():
                
                result = True
                
                if is_weekday(current_date, "Fri"):
                    tasks_for_date.append(task)

            return result

        def check_pattern_every_saturday(task, tasks_for_date):

            def is_match():

                return task['recurrence'] == 'каждая суббота' or task['recurrence'] == 'каждая сб' or task['recurrence'] == 'каждую субботу' or task['recurrence'] == 'каждую сб'

            result = False
            
            if is_match():

                result = True

                if is_weekday(current_date, "Sat"):
                    tasks_for_date.append(task)

            return result

        def check_pattern_every_sunday(task, tasks_for_date):

            def is_match():

                return task['recurrence'] == 'каждое воскресенье' or task['recurrence'] == 'каждое вс'

            result = False

            if is_match():

                result = True

                if is_weekday(current_date, "Sun"):
                    tasks_for_date.append(task)

            return result

        def check_pattern_certain_date(task, tasks_for_date):

            def is_match():

                return task['recurrence'].count('.') == 2
        
            def is_equal():

                parts = task['recurrence'].split('.')

                day     = int(parts[0])
                month   = int(parts[1])
                year    = int(parts[2])

                task_date = task['datetime'].replace(year = year, month = month, day = day, hour = 0, minute = 0, second = 0, microsecond = 0)

                if task_date < current_date:
                    task['outdated'] = True

                #return current_date.day == day and current_date.month == month and current_date.year == year
                return current_date == task_date

            result = False

            if is_match():

                result = True

                if is_equal():
                    tasks_for_date.append(task)

            return result

        def check_pattern_every_weekday(task, tasks_for_date):

            def is_match():

                return task['recurrence'] == 'каждый будний день' or task['recurrence'] == 'по будням'

            def is_equal():

                weekday = current_date.weekday()

                return weekday >=0 and weekday <=4

            result = False

            if is_match():
                
                result = True
                
                if is_equal():
                    tasks_for_date.append(task)

            return result

        def check_pattern_every_year(task, tasks_for_date):

            def is_match():

                return task['recurrence'].startswith('каждый год')

            def is_equal():

                def year_day():

                    return int(date[0])

                def year_month():

                    if date[1] == 'январь':
                        return 1
                    elif date[1] == 'февраль':
                        return 2
                    elif date[1] == 'март':
                        return 3
                    elif date[1] == 'апрель':
                        return 4
                    elif date[1] == 'май':
                        return 5
                    elif date[1] == 'июнь':
                        return 6
                    elif date[1] == 'июль':
                        return 7
                    elif date[1] == 'август':
                        return 8
                    elif date[1] == 'сентябрь':
                        return 9
                    elif date[1] == 'октябрь':
                        return 10                                                                                                                                                                                                
                    elif date[1] == 'ноябрь':
                        return 11
                    elif date[1] == 'декабрь':
                        return 12                        

                parts   = task['recurrence'].split(',')
                date    = parts[1].strip()
                date    = date.split(' ')
                
                return current_date.day == year_day() and current_date.month == year_month()

            result = False

            if is_match():
                
                result = True
                
                if is_equal():
                    tasks_for_date.append(task)

            return result            

        def check_pattern_every_n_week(task, tasks_for_date):

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

            def is_basic_match():

                parts = task['recurrence'].split(' ')

                return parts[0] == 'каждые' and (parts[2] == 'недели' or parts[2] == 'неделя') and parts[3] == 'по'

            def is_match():
                
                return is_weekday(occurs_from, occurs_when['week_day'])

            def is_equal():

                if current_date < occurs_from:
                    return False
                elif current_date == occurs_from:
                    return True

                date_to_occur   = occurs_from
                week_number     = 1

                while date_to_occur <= current_date:
                    
                    if is_weekday(date_to_occur, occurs_when['week_day']) and week_number == occurs_when['week_number']:

                        if date_to_occur == current_date:
                            return True
                        else:
                            week_number = 0

                    date_to_occur   += datetime.timedelta(days = 7)
                    week_number     += 1

                return False

            result = False

            if is_basic_match():

                occurs = task['recurrence'].split(',')

                occurs_when = occurs_when()
                occurs_from = occurs_from()

                if is_match():
                            
                    result = True
                            
                    if is_equal():
                        tasks_for_date.append(task)

            return result

        def split_tasks_for_date():

            for task in tasks_for_date:

                is_task_with_time = task['datetime'].hour > 0 or task['datetime'].minute > 0

                if is_task_with_time:
                    tasks_with_time.append(task)
                else:
                    tasks_without_time.append(task)

        def write_actual_tasks():

            with open(paths['planned_tasks_filepath'], 'w+', encoding = 'utf-8-sig') as planned_tasks_file_handle:

                are_there_tasks_before = False

                for group in planned_tasks:

                    if are_there_tasks_before:
                        tasks_writer.write_empty_line(planned_tasks_file_handle)

                    tasks_writer.write_title(planned_tasks_file_handle, group['title'])
                    tasks_writer.write_empty_line(planned_tasks_file_handle)

                    are_there_tasks_before = False;

                    for task in group['tasks']:

                        if task['outdated']:
                            continue

                        tasks_writer.write_title(planned_tasks_file_handle, task['original_title'], '-')
                        tasks_writer.write_notes(planned_tasks_file_handle, task)
                        
                        are_there_tasks_before = True

        planned_tasks = get_planned_tasks()

        tasks_for_date = []

        for group in planned_tasks:

            for task in group['tasks']:

                if tasks_reader.is_task_with_tag(task, 'пропускать'):
                    continue

                if check_pattern_every_day(task, tasks_for_date):
                    continue

                if check_pattern_every_n_week(task, tasks_for_date):
                    continue            

                if check_pattern_every_weekday(task, tasks_for_date):
                    continue

                if check_pattern_every_month(task, tasks_for_date):
                    continue

                if check_pattern_every_monday(task, tasks_for_date):
                    continue

                if check_pattern_every_tuesday(task, tasks_for_date):
                    continue

                if check_pattern_every_wednesday(task, tasks_for_date):
                    continue

                if check_pattern_every_thursday(task, tasks_for_date):
                    continue

                if check_pattern_every_friday(task, tasks_for_date):
                    continue

                if check_pattern_every_saturday(task, tasks_for_date):
                    continue

                if check_pattern_every_sunday(task, tasks_for_date):
                    continue

                if check_pattern_certain_date(task, tasks_for_date):
                    continue

                if check_pattern_every_year(task, tasks_for_date):
                    continue

                for _ in range(3):
                    winsound.Beep(400, 800)

                print("Неизвестный шаблон повторения:", task['title'])

        if len(tasks_for_date) > 0:            

            tasks_with_time     = []
            tasks_without_time  = []

            split_tasks_for_date()

            if len(tasks_with_time) > 0:

                tasks_with_time = sorted(tasks_with_time, key = lambda task: task['datetime'])

                write_tasks(tasks_with_time)

            if len(tasks_without_time) > 0:

                tasks_writer.write_empty_line(handle)

                write_tasks(tasks_without_time)

        write_actual_tasks()

    def write_uncompleted_tasks():

        for group in current_tasks:

            uncompleted_tasks = list((task for task in group['tasks'] if not task['completed']))

            if len(uncompleted_tasks) > 0:

                tasks_writer.write_empty_line(handle)
                tasks_writer.write_title(handle, group['title'])
                tasks_writer.write_empty_line(handle)

                write_tasks(uncompleted_tasks)

    if postfix == '':
        tasks_filepath = paths['current_tasks_filepath']
    else:
        tasks_filepath = os.path.join(paths['tasks_dirpath'], 'today {}.md'.format(postfix))

    with open(tasks_filepath, 'w+', encoding = 'utf-8-sig') as handle:

        title = current_date.strftime('%Y-%m-%d')

        tasks_writer.write_title(handle, title, '#')        
        tasks_writer.write_empty_line(handle)

        write_planned_tasks()

        if include_uncompleted_tasks:
            write_uncompleted_tasks()

def get_date_string(date):

    return date.strftime('%Y-%m-%d')

script_dirpath  = os.path.abspath(os.path.dirname(__file__))
paths           = common_logic.get_paths(script_dirpath)

parameters      = yaml_wrapper.get_data_from_file(paths['parameters_filepath'])
current_date    = common_logic.get_current_date()

if parameters['last_date'] != None:

    if current_date == parameters['last_date']:
    
        print("Задачи на сегодня уже распланированы!")
        exit()

    date_today = current_date
    
    date_delta = (date_today - parameters['last_date']).days
    date_delta = abs(date_delta)

    if date_delta > 1:

        current_date = parameters['last_date']

        while current_date != date_today:
            
            current_date += datetime.timedelta(days = 1)
            
            if current_date == date_today:
                break

            postfix = get_date_string(current_date)
            postfix = '({})'.format(postfix)

            refill_current_tasks_file(postfix, False)

current_tasks = tasks_reader.get_tasks_from_file(paths['current_tasks_filepath'], current_date)

if copy_current_tasks_file_to_history():

    refill_current_tasks_file()

    parameters['last_date'] = current_date

    yaml_wrapper.put_data_to_file(paths['parameters_filepath'], parameters)