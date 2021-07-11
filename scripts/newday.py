import os
import datetime
import winsound

import modules.yaml_wrapper as yaml_wrapper
import modules.tasks_reader as tasks_reader
import modules.tasks_writer as tasks_writer
import modules.common_logic as common_logic

import modules.task_plan_types.every_year       as task_plan_type_every_year
import modules.task_plan_types.every_month      as task_plan_type_every_month
import modules.task_plan_types.every_n_week     as task_plan_type_every_n_week
import modules.task_plan_types.every_n_day      as task_plan_type_every_n_day
import modules.task_plan_types.every_day        as task_plan_type_every_day
import modules.task_plan_types.every_weekday    as task_plan_type_every_weekday
import modules.task_plan_types.every_monday     as task_plan_type_every_monday
import modules.task_plan_types.every_tuesday    as task_plan_type_every_tuesday
import modules.task_plan_types.every_wednesday  as task_plan_type_every_wednesday
import modules.task_plan_types.every_thursday   as task_plan_type_every_thursday
import modules.task_plan_types.every_friday     as task_plan_type_every_friday
import modules.task_plan_types.every_saturday   as task_plan_type_every_saturday
import modules.task_plan_types.every_sunday     as task_plan_type_every_sunday
import modules.task_plan_types.date             as task_plan_type_date

def refill_current_tasks_file(postfix = '', include_uncompleted_tasks = True):

    def write_tasks(tasks):

        for task in tasks:

            tasks_writer.write_title(handle, task['title'], '-')
            tasks_writer.write_notes(handle, task)

    def write_planned_tasks():

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

                if task_plan_type_every_year.is_type(task):

                    if task_plan_type_every_year.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_every_month.is_type(task):

                    if task_plan_type_every_month.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_every_n_week.is_type(task):

                    if task_plan_type_every_n_week.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_every_n_day.is_type(task):

                    if task_plan_type_every_n_day.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue                

                if task_plan_type_every_day.is_type(task):

                    if task_plan_type_every_day.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_every_weekday.is_type(task):

                    if task_plan_type_every_weekday.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_every_monday.is_type(task):

                    if task_plan_type_every_monday.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_every_tuesday.is_type(task):

                    if task_plan_type_every_tuesday.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_every_wednesday.is_type(task):

                    if task_plan_type_every_wednesday.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_every_thursday.is_type(task):

                    if task_plan_type_every_thursday.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_every_friday.is_type(task):

                    if task_plan_type_every_friday.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_every_saturday.is_type(task):

                    if task_plan_type_every_saturday.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_every_sunday.is_type(task):

                    if task_plan_type_every_sunday.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

                    continue

                if task_plan_type_date.is_type(task):

                    if task_plan_type_date.is_relevant_for_date(task, current_date):
                        tasks_for_date.append(task)

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

        if postfix == '':
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

def update_git(comment):

    def git_add():

        command = 'git -C "{}" add :/'.format(paths['tasks_dirpath'])    
        print(command)

        os.system(command)

    def git_commit():

        comment_date = current_date.strftime('%Y-%m-%d')
        full_comment = '{0}, {1}'.format(comment_date, comment)

        command = 'git -C "{}" commit -a -m "{}"'.format(paths['tasks_dirpath'], full_comment)
        print(command)

        os.system(command)

    def git_status():

        command = 'git -C "{}" status'.format(paths['tasks_dirpath'])
        print(command)

        os.system(command)

    git_status()
    git_add()
    git_commit()

script_dirpath  = os.path.abspath(os.path.dirname(__file__))
paths           = common_logic.get_paths(script_dirpath)

parameters      = yaml_wrapper.get_data_from_file(paths['parameters_filepath'])
current_date    = common_logic.get_current_date()

if parameters['last_date'] != None:

    if current_date == parameters['last_date']:
    
        print("Задачи на сегодня уже распланированы!")
        exit()

    update_git('last day')

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

refill_current_tasks_file()

parameters['last_date'] = current_date

yaml_wrapper.put_data_to_file(paths['parameters_filepath'], parameters)

update_git('this day')