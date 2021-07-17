import os
import re
import datetime
import winsound

import modules.tasks_reader as tasks_reader
import modules.common_logic as common_logic

def get_notifications():

   def get_content():

      result = []

      result.append(task['title'])

      for note in task['notes']:
         result.append(note)

      return "/n".join(result)

   def find_notifications_before_start(content):

      def get_number(string):

         if string != '':
            result = int(string)
         else:
            result = 0

         return result

      groups = re.findall('(напоминать за( ([0-9]+) (часов|часа|час))?( ([0-9]+) (минуты|минуту|минут))? до начала)', content)

      for group in groups:
         
         hours    = get_number(group[2])
         minutes  = get_number(group[5])

         timedelta = datetime.timedelta(seconds = hours * 3600 + minutes * 60)
         task_date = task['datetime'] - timedelta

         if now >= task_date:
            notifications.append(group[0])

   def find_notifications_after_start(content):

      groups = re.findall('(напоминать)(?!за)', content)

      for group in groups:
         
         if now >= task['datetime']:

            if type(group) is str:
               notifications.append(group)
            else:
               notifications.append(group[0])

   notifications  = []
   content        = get_content()
  
   find_notifications_before_start(content)
   find_notifications_after_start(content)

   return notifications

script_dirpath    = os.path.abspath(os.path.dirname(__file__))
current_date      = common_logic.get_current_date()

paths = common_logic.get_paths(script_dirpath)
tasks = tasks_reader.get_tasks_from_file(paths['current_tasks_filepath'], current_date)

now = datetime.datetime.now()

ring = False

for group in tasks:

   for task in group['tasks']:

      if task['completed'] == True:
         continue

      notifications = get_notifications()

      if len(notifications) > 0:
         ring = True
         break

if ring:
   winsound.Beep(300, 1200)