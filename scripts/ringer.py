import os
import datetime
import winsound

import modules.tasks_reader as tasks_reader
import modules.common_logic as common_logic

script_dirpath    = os.path.abspath(os.path.dirname(__file__))
current_date      = common_logic.get_current_date()

paths = common_logic.get_paths(script_dirpath)
tasks = tasks_reader.get_tasks_from_file(paths['current_tasks_filepath'], current_date)

time = datetime.datetime.now()
ring = False

for group in tasks:

   for task in group['tasks']:

      is_time      = task['datetime'] <= time
      is_task_done = task['completed'] == False
      is_ring_need = tasks_reader.is_task_with_tag(task, 'напоминать')

      if is_time and is_task_done and is_ring_need:
         ring = True
         break

if ring:
   winsound.Beep(300, 1200)