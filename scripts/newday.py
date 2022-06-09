import os
import errno
import zipfile
import datetime
import winsound

import modules.yaml_wrapper as yaml_wrapper
import modules.tasks_reader as tasks_reader
import modules.tasks_writer as tasks_writer
import modules.common_logic as common_logic

import modules.task_plan_types.every_year as task_plan_type_every_year
import modules.task_plan_types.every_month as task_plan_type_every_month
import modules.task_plan_types.every_n_week as task_plan_type_every_n_week
import modules.task_plan_types.every_n_day as task_plan_type_every_n_day
import modules.task_plan_types.every_day as task_plan_type_every_day
import modules.task_plan_types.every_weekday as task_plan_type_every_weekday
import modules.task_plan_types.every_monday as task_plan_type_every_monday
import modules.task_plan_types.every_tuesday as task_plan_type_every_tuesday
import modules.task_plan_types.every_wednesday as task_plan_type_every_wednesday
import modules.task_plan_types.every_thursday as task_plan_type_every_thursday
import modules.task_plan_types.every_friday as task_plan_type_every_friday
import modules.task_plan_types.every_saturday as task_plan_type_every_saturday
import modules.task_plan_types.every_sunday as task_plan_type_every_sunday
import modules.task_plan_types.date as task_plan_type_date


def write_current_tasks_file(postfix='', include_uncompleted_tasks=True):
    def write_tasks(tasks):

        for task in tasks:
            tasks_writer.write_title(handle, task['title'], '-')
            tasks_writer.write_notes(handle, task)

    def write_planned_tasks_in_current_tasks_file():

        def add_current_task():

            is_task_with_time = task['datetime'].hour > 0 or task['datetime'].minute > 0

            if is_task_with_time:
                current_tasks_with_time.append(task)
            else:
                current_tasks_without_time.append(task)

        def get_planned_tasks():

            tasks = tasks_reader.get_tasks_from_file(paths['planned_tasks_filepath'], current_date)

            for group in tasks:

                for task in group['tasks']:

                    substrings = task['title'].split(';')
                    substrings_counter = len(substrings)

                    if substrings_counter >= 2:
                        task['title'] = substrings[0].strip()
                        task['condition'] = substrings[1].strip().lower()

            return tasks

        def write_planned_tasks_file():

            with open(paths['planned_tasks_filepath'], 'w+', encoding='utf-8-sig') as planned_tasks_file_handle:

                are_there_tasks_before = False

                for group in planned_tasks:

                    if are_there_tasks_before:
                        tasks_writer.write_empty_line(planned_tasks_file_handle)

                    tasks_writer.write_title(planned_tasks_file_handle, group['title'])
                    tasks_writer.write_empty_line(planned_tasks_file_handle)

                    are_there_tasks_before = False

                    for task in group['tasks']:

                        if task['outdated']:
                            continue

                        tasks_writer.write_title(planned_tasks_file_handle, task['original_title'], '-')
                        tasks_writer.write_notes(planned_tasks_file_handle, task)

                        are_there_tasks_before = True

        def does_task_belong_to_plan_type_every_year():

            result = False
            task_is_current = task_plan_type_every_year.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_month():

            result = False
            task_is_current = task_plan_type_every_month.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_n_week():

            result = False
            task_is_current = task_plan_type_every_n_week.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_n_day():

            result = False
            task_is_current = task_plan_type_every_n_day.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_weekday():

            result = False
            task_is_current = task_plan_type_every_weekday.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_monday():

            result = False
            task_is_current = task_plan_type_every_monday.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_tuesday():

            result = False
            task_is_current = task_plan_type_every_tuesday.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_wednesday():

            result = False
            task_is_current = task_plan_type_every_wednesday.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_thursday():

            result = False
            task_is_current = task_plan_type_every_thursday.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_friday():

            result = False
            task_is_current = task_plan_type_every_friday.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_saturday():

            result = False
            task_is_current = task_plan_type_every_saturday.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_sunday():

            result = False
            task_is_current = task_plan_type_every_sunday.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_date():

            result = False
            task_is_current = task_plan_type_date.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        def does_task_belong_to_plan_type_every_day():

            result = False
            task_is_current = task_plan_type_every_day.is_task_current(task, current_date)

            if task_is_current != None:

                if task_is_current:
                    add_current_task()

                result = True

            return result

        planned_tasks = get_planned_tasks()

        current_tasks_with_time = []
        current_tasks_without_time = []

        for group in planned_tasks:

            for task in group['tasks']:

                if does_task_belong_to_plan_type_every_year():
                    continue

                if does_task_belong_to_plan_type_every_month():
                    continue

                if does_task_belong_to_plan_type_every_n_week():
                    continue

                if does_task_belong_to_plan_type_every_n_day():
                    continue

                if does_task_belong_to_plan_type_every_n_day():
                    continue

                if does_task_belong_to_plan_type_every_day():
                    continue

                if does_task_belong_to_plan_type_every_weekday():
                    continue

                if does_task_belong_to_plan_type_every_monday():
                    continue

                if does_task_belong_to_plan_type_every_tuesday():
                    continue

                if does_task_belong_to_plan_type_every_wednesday():
                    continue

                if does_task_belong_to_plan_type_every_thursday():
                    continue

                if does_task_belong_to_plan_type_every_friday():
                    continue

                if does_task_belong_to_plan_type_every_saturday():
                    continue

                if does_task_belong_to_plan_type_every_sunday():
                    continue

                if does_task_belong_to_plan_type_date():
                    continue

                for _ in range(3):
                    winsound.Beep(400, 800)

                print("Неизвестный шаблон повторения:", task['title'])

        if len(current_tasks_with_time) > 0:
            tasks_with_time = sorted(current_tasks_with_time, key=lambda task: task['datetime'])

            write_tasks(tasks_with_time)

        if len(current_tasks_without_time) > 0:
            tasks_writer.write_empty_line(handle)

            write_tasks(current_tasks_without_time)

        if postfix == '':
            write_planned_tasks_file()

    def write_uncompleted_tasks_in_current_tasks_file():

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

    with open(tasks_filepath, 'w+', encoding='utf-8-sig') as handle:

        title = current_date.strftime('%Y-%m-%d')

        tasks_writer.write_title(handle, title, '#')
        tasks_writer.write_empty_line(handle)

        write_planned_tasks_in_current_tasks_file()

        if include_uncompleted_tasks:
            write_uncompleted_tasks_in_current_tasks_file()


def make_tasks_archive(comment: str):
    def make_sure_path_exists(path):

        try:

            os.makedirs(path)

        except OSError as exception:

            if exception.errno != errno.EEXIST:
                raise

    make_sure_path_exists(paths['history_dirpath'])

    archive_filedate = current_date.strftime('%Y-%m-%d')
    archive_filename = '{0}, {1}.zip'.format(archive_filedate, comment)
    archive_filepath = os.path.join(paths['history_dirpath'], archive_filename)

    zf = zipfile.ZipFile(archive_filepath, 'w')

    files = os.listdir(paths['tasks_dirpath'])

    for file in files:

        filepath = os.path.join(paths['tasks_dirpath'], file)

        if os.path.isfile(filepath) and filepath != paths['settings_filepath'] and filepath != paths['cache_filepath']:
            zf.write(filepath, file)

    zf.close()


script_dirpath = os.path.abspath(os.path.dirname(__file__))
paths = common_logic.get_paths(script_dirpath)

cache = yaml_wrapper.get_data_from_file(paths['cache_filepath'])
current_date = common_logic.get_current_date()

if cache['last_date'] != None:

    if current_date == cache['last_date']:
        print("Задачи на сегодня уже распланированы!")
        exit()

    make_tasks_archive('last day')

    date_today = current_date

    date_delta = (date_today - cache['last_date']).days
    date_delta = abs(date_delta)

    if date_delta > 1:

        current_date = cache['last_date']

        while current_date != date_today:

            current_date += datetime.timedelta(days=1)

            if current_date == date_today:
                break

            postfix = current_date.strftime('%Y-%m-%d')
            postfix = '({})'.format(postfix)

            write_current_tasks_file(postfix, False)

current_tasks = tasks_reader.get_tasks_from_file(paths['current_tasks_filepath'], current_date)

write_current_tasks_file()

cache['last_date'] = current_date

yaml_wrapper.put_data_to_file(paths['cache_filepath'], cache)

make_tasks_archive('this day')
