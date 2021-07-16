import os
import datetime
import winsound

import modules.tasks_reader as tasks_reader
import modules.common_logic as common_logic

def is_task_now():

   return task['datetime'] <= time

def is_task_open():

   return task['completed'] == False

def is_task_with_tag(tag):

    marked_tag = '#{}'.format(tag)

    return task['title'].lower().find(marked_tag) != -1

script_dirpath    = os.path.abspath(os.path.dirname(__file__))
current_date      = common_logic.get_current_date()

paths = common_logic.get_paths(script_dirpath)
tasks = tasks_reader.get_tasks_from_file(paths['current_tasks_filepath'], current_date)

time = datetime.datetime.now()
ring = False

for group in tasks:

   for task in group['tasks']:

      if is_task_now() and is_task_open() and is_task_with_tag('напоминать'):
         ring = True
         break

if ring:
   winsound.Beep(300, 1200)